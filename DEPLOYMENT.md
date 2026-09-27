# Streamlit Community Cloud Deployment

Use these exact settings when creating the app in Streamlit Community Cloud.

## GitHub coordinates
- Repository: `Nabilvisi/subsurface-30day-autonomous`
- Branch: `main`
- Entrypoint file: `app.py`

## Advanced settings
- Python version: **3.11**
- Secrets: **none required**
- App URL: choose any available custom subdomain, for example `nabilvisi-subsurface-30day`

## Repository status
- `requirements.txt` is in the repository root.
- `.streamlit/config.toml` is in the repository root.
- Streamlit is pinned to `1.64.0` for reproducibility.
- The app derives the live day from `project_config.json`.
- Daily release automation is defined in `.github/workflows/daily_release.yml`.
- The release schedule is **00:05 Asia/Jakarta**, Day 01 starting **2026-09-28**.

## Private repository note
This repository is private. Streamlit Community Cloud therefore needs permission to access private GitHub repositories for the connected GitHub account. With private-repository deployment, the app is private by default; app access can be changed later in Streamlit app settings.

## Deployment form
1. Open `https://share.streamlit.io`.
2. Select **Create app**.
3. Choose **Yup, I have an app**.
4. Enter the GitHub coordinates above.
5. Open **Advanced settings** and choose Python **3.11**.
6. Leave Secrets empty.
7. Click **Deploy**.
