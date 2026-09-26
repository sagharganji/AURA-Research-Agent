
/* AURA Studio: static preview + FastAPI live-mode client. API secrets stay server-side. */
(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const backend = String(window.AURA_BACKEND_URL || "").trim().replace(/\/$/, "");
  const questionEl = $("q");
  const defaultQuestion = questionEl.value;
  let reportText = "";
  let reportKind = null;
  let reportCounts = null;
  let reportQuestion = "";
  let activeTab = "summary";
  const headings = ["Plan", "Discover", "Verify", "Analyze", "Decide", "Build"];

  function setStatus(message, error = false) {
    $("status").textContent = message;
    $("status").classList.toggle("error", error);
  }
  function setSession(label, description) {
    $("session-state").textContent = label;
    $("session-description").textContent = description;
  }
  function clearText(node) { node.replaceChildren(); }
  function textNode(tag, str, className = "") {
    const node = document.createElement(tag);
    node.textContent = str;
    if (className) node.className = className;
    return node;
  }
  function sectionFromMarkdown(markdown, title) {
    const headingsRe = /^## (.+)\s*$/gm;
    let match;
    while ((match = headingsRe.exec(markdown)) !== null) {
      if (match[1].trim().toLowerCase() !== title.toLowerCase()) continue;
      const tail = markdown.slice(headingsRe.lastIndex);
      const next = tail.search(/^## /m);
      return (next < 0 ? tail : tail.slice(0, next)).trim();
    }
    return "";
  }
  function parseList(markdownSection) {
    return markdownSection.split(/\r?\n/).filter(s => /^-\s+/.test(s.trim())).map(s => s.replace(/^\s*-\s+/, "").replace(/\*\*/g, "").trim());
  }
  function parseEvidence(markdown) {
    const section = sectionFromMarkdown(markdown, "Evidence Sources");
    const sources = [];
    for (const line of section.split(/\r?\n/)) {
      const match = line.match(/^\s*\d+\.\s*\[([^\]]+)\]\s*(.*?)\s+[—–-]\s*(https?:\/\/\S+)/);
      if (!match) continue;
      sources.push({ type: match[1].trim(), title: match[2].trim(), url: match[3].trim() });
    }
    return sources;
  }
  function sampleCounts(markdown) {
    const section = sectionFromMarkdown(markdown, "Sources Discovered");
    const numberFor = re => Number((section.match(re) || [])[1] || 0);
    return {
      papers: numberFor(/-\s*Papers:\s*(\d+)/i),
      datasets: numberFor(/-\s*Datasets:\s*(\d+)/i),
      repositories: numberFor(/-\s*Code repositories:\s*(\d+)/i),
      evidence: numberFor(/-\s*Unified evidence items:\s*(\d+)/i)
    };
  }
  function updateCounters(counts, kind, elapsed) {
    const sourceCount = counts ? (counts.papers || 0) + (counts.datasets || 0) + (counts.repositories || 0) : null;
    $("sources-number").textContent = sourceCount === null ? "—" : String(sourceCount);
    $("evidence-number").textContent = counts ? String(counts.evidence ?? "—") : "—";
    $("duration-number").textContent = kind === "live" && Number.isFinite(Number(elapsed)) ? `${elapsed}s` : "—";
    $("sources-detail").textContent = kind === "sample" ? "Recorded sample · not a live search" : kind === "live" ? "Found in this live research run" : "Awaiting research";
    $("evidence-detail").textContent = kind === "sample" ? "From the saved research report" : kind === "live" ? "Organized during this run" : "Awaiting research";
    $("duration-detail").textContent = kind === "sample" ? "Not measured for recorded sample" : kind === "live" ? "Elapsed time from the backend" : "Not measured yet";
  }
  function showSources(markdown, kind) {
    const list = $("source-list");
    clearText(list);
    const sources = parseEvidence(markdown);
    $("evidence-label").textContent = kind === "sample" ? "Recorded example" : "Live report sources";
    if (!sources.length) {
      const empty = textNode("p", "No source links were extracted from this report. Inspect the full report for references.", "muted-note");
      list.appendChild(empty);
      return;
    }
    for (const source of sources) {
      const row = textNode("article", "", "source-item");
      row.appendChild(textNode("span", source.type, "source-kind"));
      const meta = textNode("div", "", "source-meta");
      meta.appendChild(textNode("strong", source.title));
      let url;
      try { url = new URL(source.url); } catch { url = null; }
      if (url && ["https:", "http:"].includes(url.protocol)) {
        const link = document.createElement("a");
        link.textContent = source.url;
        link.href = url.href;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        meta.appendChild(link);
      }
      row.appendChild(meta);
      list.appendChild(row);
    }
  }
  function paragraphFromSection(section) {
    const lines = section.split(/\r?\n/).map(s => s.trim());
    const paragraphs = [];
    let group = [];
    for (const line of lines) {
      if (/^#{1,6} /.test(line) || /^[-*] /.test(line)) break;
      if (!line) { if (group.length) { paragraphs.push(group.join(" ")); group = []; } }
      else group.push(line.replace(/\*\*/g, ""));
    }
    if (group.length) paragraphs.push(group.join(" "));
    return paragraphs[0] || "";
  }
  function renderPreview(markdown) {
    const recommendation = sectionFromMarkdown(markdown, "Recommendation");
    const findings = parseList(sectionFromMarkdown(markdown, "Key Findings"));
    const direction = paragraphFromSection(recommendation) || "Open the full report to read the research findings and implementation direction.";
    $("recommendation-text").textContent = direction;
    clearText($("finding-list"));
    for (const finding of findings.slice(0, 3)) $("finding-list").appendChild(textNode("li", finding));
    if (!findings.length) $("finding-list").appendChild(textNode("li", "See the full report for research details."));
    $("preview-empty").classList.add("hidden");
    $("preview-content").classList.remove("hidden");
    $("report-label").textContent = reportKind === "sample" ? "Recorded sample" : "Live output";
  }
  // Safe, minimal Markdown renderer. It intentionally doesn't accept HTML or execute code.
  function appendInline(parent, source) {
    const parts = source.split(/(\*\*[^*]+\*\*|\[[^\]]+\]\(https?:\/\/[^ )]+\))/g);
    for (const part of parts) {
      if (part.startsWith("**") && part.endsWith("**")) parent.appendChild(textNode("strong", part.slice(2, -2)));
      else {
        const m = part.match(/^\[([^\]]+)\]\((https?:\/\/[^ )]+)\)$/);
        if (m) {
          const link = textNode("a", m[1]);
          link.href = m[2]; link.target = "_blank"; link.rel = "noopener noreferrer";
          parent.appendChild(link);
        } else parent.appendChild(document.createTextNode(part));
      }
    }
  }
  function renderMarkdown(target, markdown) {
    clearText(target);
    const body = textNode("div", "", "report-document");
    const lines = markdown.split(/\r?\n/);
    let list = null;
    let listType = null;
    let paragraph = [];
    function flushParagraph() {
      if (paragraph.length) {
        const p = document.createElement("p");
        appendInline(p, paragraph.join(" "));
        body.appendChild(p);
        paragraph = [];
      }
    }
    function flushList() { list = null; listType = null; }
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) { flushParagraph(); flushList(); continue; }
      const heading = trimmed.match(/^(#{1,3})\s+(.+)/);
      if (heading) { flushParagraph(); flushList(); body.appendChild(textNode(`h${heading[1].length}`, heading[2])); continue; }
      const bullet = trimmed.match(/^[-*]\s+(.+)/);
      const numbered = trimmed.match(/^\d+\.\s+(.+)/);
      if (bullet || numbered) {
        flushParagraph();
        const type = bullet ? "ul" : "ol";
        if (!list || type !== listType) { list = document.createElement(type); body.appendChild(list); listType = type; }
        const li = document.createElement("li");
        appendInline(li, (bullet || numbered)[1]);
        list.appendChild(li);
        continue;
      }
      flushList(); paragraph.push(trimmed);
    }
    flushParagraph();
    target.appendChild(body);
  }
  function makeSubpanel(title, items, fallback) {
    const panel = textNode("article", "", "report-subpanel");
    panel.appendChild(textNode("h3", title));
    if (items.length) {
      const ul = document.createElement("ul");
      for (const item of items) { const li = document.createElement("li"); appendInline(li, item); ul.appendChild(li); }
      panel.appendChild(ul);
    } else panel.appendChild(textNode("p", fallback));
    return panel;
  }
  function renderSummary(target, markdown) {
    clearText(target);
    const layout = textNode("div", "", "report-layout-split");
    const recommendation = paragraphFromSection(sectionFromMarkdown(markdown, "Recommendation"));
    const findingPanel = makeSubpanel("Key findings", parseList(sectionFromMarkdown(markdown, "Key Findings")), "Read the full report for details.");
    const riskPanel = makeSubpanel("Research gaps", parseList(sectionFromMarkdown(markdown, "Research Gaps")), "No research gaps extracted from this report.");
    layout.appendChild(findingPanel); layout.appendChild(riskPanel);
    if (recommendation) {
      const note = textNode("div", "", "report-document");
      const h = textNode("h3", "Research direction");
      const p = textNode("p", recommendation, "report-note");
      note.append(h,p); target.appendChild(note);
    }
    target.appendChild(layout);
  }
  function changeTab(tab) {
    activeTab = tab;
    document.querySelectorAll(".report-tabs .tab").forEach(button => {
      const selected = button.dataset.tab === tab;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
    });
    const tabButton = document.querySelector(`.tab[data-tab="${tab}"]`);
    $("report-view").setAttribute("aria-labelledby", tabButton.id);
    if (tab === "summary") renderSummary($("report-view"), reportText);
    else if (tab === "roadmap") {
      const roadmap = sectionFromMarkdown(reportText, "Implementation Roadmap");
      renderMarkdown($("report-view"), roadmap ? `## Implementation Roadmap\n${roadmap}` : "## Implementation roadmap\nNo roadmap section was extracted from this report.");
    } else renderMarkdown($("report-view"), reportText);
  }
  function showReport(markdown, kind, counts, question, elapsed) {
    reportText = markdown;
    reportKind = kind;
    reportCounts = counts;
    reportQuestion = question;
    updateCounters(counts, kind, elapsed);
    showSources(markdown, kind);
    renderPreview(markdown);
    $("full-report").classList.remove("hidden");
    $("report-mode").textContent = kind === "sample" ? "RECORDED EXAMPLE · NOT A LIVE RUN" : "LIVE RESEARCH RESULT";
    $("report-question").textContent = kind === "sample" ? "Saved example: solar flare forecasting" : question;
    $("report-disclaimer").textContent = kind === "sample"
      ? "Recorded example: this was saved from an earlier solar-flare session. It is not generated for the question currently in the text box. Verify its sources before reuse."
      : "Live agent output: verify citations and technical claims before use. Stage-level telemetry is not available.";
    setSession(kind === "sample" ? "Example loaded" : "Research complete", kind === "sample" ? "Viewing a previously saved solar-flare report." : "Your live research report is available below.");
    $("pipeline-indicator").textContent = kind === "sample" ? "Architecture preview · no new run" : "Research run complete";
    changeTab("summary");
    $("reports").scrollIntoView({behavior:"smooth",block:"start"});
  }
  function countChars() { $("char-count").textContent = `${questionEl.value.length} / 1200`; }
  function resetReport() {
    reportText = "";
    reportKind = null;
    reportCounts = null;
    reportQuestion = "";
    $("full-report").classList.add("hidden");
    $("preview-empty").classList.remove("hidden");
    $("preview-content").classList.add("hidden");
    $("evidence-label").textContent = "No run loaded";
    $("report-label").textContent = "Awaiting output";
    clearText($("source-list"));
    $("source-list").appendChild(textNode("p", "No evidence loaded yet. Load the recorded example or connect the live engine.", "empty-state"));
    updateCounters(null, null, null);
    setSession("Ready to explore", "Launch your question or open the recorded example.");
    $("pipeline-indicator").textContent = "Ready · no active run";
    setStatus(backend ? "Backend URL configured. Start a research run." : "Demo mode. Open the recorded example or connect your backend.");
  }
  async function loadSample() {
    $("sample").disabled = true;
    setSession("Loading example", "Reading the saved report from this package…");
    setStatus("Loading a recorded example. This is not a new agent run.");
    try {
      const response = await fetch("./sample_report.md", { cache: "no-store" });
      if (!response.ok) throw new Error(`Sample report unavailable (HTTP ${response.status}).`);
      const markdown = await response.text();
      showReport(markdown, "sample", sampleCounts(markdown), "Solar flare forecasting — saved example", null);
      setStatus("Saved example loaded. Connect the backend to generate new research.");
    } catch (error) {
      setStatus(`Could not load the example: ${error.message}. Verify that sample_report.md was published with the website.`, true);
      setSession("Sample unavailable", "Please verify the package and local web server.");
    } finally { $("sample").disabled = false; }
  }
  async function runResearch() {
    const question = questionEl.value.trim();
    if (question.length < 12) { setStatus("Enter a research question of at least 12 characters.", true); questionEl.focus(); return; }
    if (!backend) {
      setStatus("Demo mode: loading the saved solar-flare example instead. It is not based on your newly entered question.");
      return loadSample();
    }
    const button = $("run");
    button.disabled = true;
    setSession("Research in progress", "The backend is running; detailed per-agent progress is unavailable.");
    $("pipeline-indicator").textContent = "Backend processing · no stage telemetry";
    setStatus("Contacting the AURA backend. External research and LLM calls may take several minutes.");
    try {
      const response = await fetch(`${backend}/research`, {
        method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question})
      });
      const contentType = response.headers.get("content-type") || "";
      const data = contentType.includes("json") ? await response.json() : {};
      if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : `Server returned HTTP ${response.status}`);
      if (typeof data.report !== "string" || !data.report.trim()) throw new Error("Server returned no report text.");
      const c = data.counts || {};
      showReport(data.report, "live", c, question, data.elapsed_seconds);
      setStatus("Live research completed. Review sources and save your report below.");
    } catch (error) {
      setStatus(`Live run failed: ${error.message}. Check the backend URL, CORS, Cloud Run logs, and API quota.`, true);
      setSession("Request unsuccessful", "Check your backend and retry.");
      $("pipeline-indicator").textContent = "Backend request failed";
    } finally { button.disabled = false; }
  }
  function downloadReport() {
    if (!reportText) return;
    const blob = new Blob([reportText], {type:"text/markdown;charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = reportKind === "sample" ? "AURA-recorded-example.md" : "AURA-live-report.md";
    document.body.appendChild(link);
    link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function openDialog() {
    $("dialog-status").textContent = backend
      ? "A live backend URL is configured. If requests fail, check the backend's health, credentials, CORS, and logs."
      : "Demo mode is active. The current page uses a clearly labeled saved report instead of running agents.";
    $("backend-address").textContent = backend || "Not connected";
    if (!$("connection-dialog").open) $("connection-dialog").showModal();
  }
  const closeSidebar = () => { $("sidebar").classList.remove("open"); $("sidebar-scrim").hidden = true; $("mobile-toggle").setAttribute("aria-expanded", "false"); };
  $("mobile-toggle").addEventListener("click", () => { const opening = !$("sidebar").classList.contains("open"); $("sidebar").classList.toggle("open", opening); $("sidebar-scrim").hidden = !opening; $("mobile-toggle").setAttribute("aria-expanded", String(opening)); });
  $("sidebar-scrim").addEventListener("click", closeSidebar);
  document.querySelectorAll(".nav-link[data-nav]").forEach(link => {
    link.addEventListener("click", () => {
      document.querySelectorAll(".nav-link[data-nav]").forEach(n => n.classList.toggle("active", n === link));
      closeSidebar();
    });
  });
  document.querySelectorAll(".prompt-chip").forEach(btn => btn.addEventListener("click", () => {
    questionEl.value = btn.dataset.question || defaultQuestion;
    countChars(); questionEl.focus();
    setStatus("Question updated. Start Research to run the backend, or load the recorded example.");
  }));
  $("run").addEventListener("click", runResearch);
  $("sample").addEventListener("click", loadSample);
  $("download").addEventListener("click", downloadReport);
  $("connect-btn").addEventListener("click", openDialog);
  $("settings-btn").addEventListener("click", () => { closeSidebar(); openDialog(); });
  $("close-dialog").addEventListener("click", () => $("connection-dialog").close());
  $("dialog-done").addEventListener("click", () => $("connection-dialog").close());
  $("connection-dialog").addEventListener("click", e => { if (e.target === $("connection-dialog")) $("connection-dialog").close(); });
  $("q").addEventListener("input", countChars);
  document.querySelectorAll(".report-tabs .tab").forEach(button => button.addEventListener("click", () => changeTab(button.dataset.tab)));
  document.querySelector(".new-session").addEventListener("click", () => { questionEl.value = ""; countChars(); resetReport(); questionEl.focus({preventScroll:true}); });
  document.addEventListener("keydown", e => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); runResearch(); }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); questionEl.focus(); }
    if (e.key === "Escape") closeSidebar();
  });
  countChars();
  $("mode-label").textContent = backend ? "Live API configured" : "Demo / recorded sample";
  $("connection-led").classList.toggle("live", Boolean(backend));
  setStatus(backend ? "Backend URL configured. Start Research to run the agents." : "Demo mode: view the recorded example. Configure the backend for new research.");
  // The original six-stage pipeline is architecture only. Never fake individual agent progress.
  void headings;
})();
// Additional Atlas controls are kept separate from the core research client.
(() => {
  const q = document.getElementById('q');
  const focus = document.getElementById('focus-question');
  if (focus && q) focus.addEventListener('click', () => { q.scrollIntoView({behavior:'smooth',block:'center'}); q.focus({preventScroll:true}); });
  document.querySelectorAll('.template-btn').forEach(button => button.addEventListener('click', () => {
    if (!q) return;
    q.value = button.dataset.question || '';
    q.dispatchEvent(new Event('input', {bubbles:true}));
    q.scrollIntoView({behavior:'smooth',block:'center'});
    q.focus({preventScroll:true});
    document.getElementById('sidebar')?.classList.remove('open');
    const scrim = document.getElementById('sidebar-scrim');
    if (scrim) scrim.hidden = true;
    document.getElementById('mobile-toggle')?.setAttribute('aria-expanded','false');
  }));
})();

