# S.A.S.S.I

A lightweight Python code security gatekeeper that scans user input for syntax issues and banned tokens before allowing execution.

## Live Web Service
This repository now includes a public-facing Streamlit application.

### Run locally
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```
3. Open the generated URL in your browser.

### Deploy publicly
#### Streamlit Cloud
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select this repository and branch
4. Deploy

The repository already includes:
- `.streamlit/config.toml` for Streamlit defaults
- `Procfile` for compatible deployments

#### Other hosts
This app also works on Render, Railway, Fly.io, or any host that supports Python.
Use the same command:
```bash
streamlit run app.py
```

## Files
- `sassi_engine.py`: core parsing and scan logic
- `app.py`: Streamlit web interface
- `requirements.txt`: required Python packages
- `.streamlit/config.toml`: Streamlit app configuration
- `Procfile`: deploy command for hosted services
