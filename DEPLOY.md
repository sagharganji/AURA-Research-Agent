# Deployment guide — AURA Atlas

This guide uses the architecture discussed for AURA: **Vercel for the static frontend** and (optionally) **Google Cloud Run for the Python agents**.

## 1. Publish the frontend first (no local server required)

1. Go to [Vercel](https://vercel.com/new) and sign in with GitHub.
2. Import `sagharganji/AURA-Research-Agent` **after the Atlas feature branch is merged**.
3. Choose Framework Preset **Other** and Root Directory **AURA_demo_UI**. There is no framework build command; Output Directory may be left at its default for the selected static preset.
4. Deploy, then visit your new `https://…vercel.app` URL.
5. Select **Open recorded example**. That saved report is a demo, not fresh agent execution.
6. Use the Vercel URL in your GitHub About section and LinkedIn post—never `localhost:5500`.

## 2. Prepare the backend locally

Use Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\python.exe -m pip install -r requirements.backend.txt
# macOS/Linux:
.venv/bin/python -m pip install -r requirements.backend.txt
python -m pip install pytest httpx
python -m pytest tests/test_api.py -q
```

Set `GEMINI_API_KEY` **only in your server environment** and run:

```bash
python -m uvicorn app.api:app --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080/health`. The health check can succeed without a key, but live research will return 503 until a valid key is supplied.

## 3. Optional Cloud Run backend

**Prerequisites:** Eligible Google Cloud account, billing enabled, access to Gemini API, and the necessary IAM permissions. Availability depends on your location and account.

In Google Cloud, create/select a project and enable Cloud Run, Cloud Build, Artifact Registry and Secret Manager. Add your Gemini API key to a Secret Manager secret named `aura-gemini-key`. Give the Cloud Run **runtime service account** the Secret Manager Secret Accessor role for that secret.

In a shell signed in with the matching Google Cloud project:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com

# Replace the Vercel domain and service-account email first.
gcloud run deploy aura-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account YOUR_RUNTIME_SERVICE_ACCOUNT_EMAIL \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 1 \
  --concurrency 1 \
  --timeout 900 \
  --set-env-vars ALLOWED_ORIGINS=https://YOUR-VERCEL-DOMAIN.vercel.app,GEMINI_MODEL=gemini-2.5-flash-lite \
  --set-secrets GEMINI_API_KEY=aura-gemini-key:latest
```

Your build project/service account needs the permissions required for a Cloud Run source deployment. Once deployed, verify `https://YOUR-CLOUD-RUN-URL/health` and a small authenticated-configuration smoke test via `/docs`.

**Security:** `--allow-unauthenticated` makes the backend public. Before sharing a live demo widely, add real auth/API gateway protection, robust persistent rate limiting and budget monitoring. Cloud Run instance count and in-memory limits **do not** guarantee a hard billing cap.

## 4. Connect the frontend

Edit `AURA_demo_UI/config.js`:

```js
window.AURA_BACKEND_URL = "https://YOUR-CLOUD-RUN-URL";
```

Use the origin only (no trailing `/research`) and **do not put the Gemini key in browser code**. Commit to GitHub. Vercel automatically redeploys when the tracked branch updates. Check the browser console and backend logs if cross-origin requests fail; `ALLOWED_ORIGINS` must match the exact Vercel site origin.

## What to publish on LinkedIn

A screenshot of the Atlas dashboard, your GitHub repository link and Vercel URL. Describe the current mode precisely, for example **“AURA Atlas: multi-agent AI research prototype with a responsive demo and an optional cloud-hosted API.”** Only say “live agent demo” after successfully configuring and testing the backend.
