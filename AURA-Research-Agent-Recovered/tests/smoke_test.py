from app.main import run_aura

QUESTION = """
I want to build a solar flare prediction system using machine learning.
Find relevant papers, datasets and code, compare existing approaches,
identify limitations, and propose an implementation roadmap.
"""

result = run_aura(
    QUESTION,
    max_papers=2,
    max_datasets=2,
    max_repositories=2,
    save_output=True,
)

for key in ["research_plan", "evidence", "verification", "analysis", "decision", "roadmap", "report"]:
    assert key in result
assert len(result["report"]) > 100
print("🎉 AURA FINAL MVP TEST PASSED.")
