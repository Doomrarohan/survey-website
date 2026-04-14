# Gaming Report 2025 — Streamlit Survey

Interactive gaming survey dashboard built with Streamlit + Plotly.  
Shareable via a public URL on Streamlit Community Cloud (free).


## Quick Start (run locally)

```bash
cd gaming-survey-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**


## Deploy to Streamlit Cloud (get a shareable link)

### Step 1 — Push to GitHub

Open PowerShell and navigate to this folder:

```bash
cd C:\Users\YOUR_NAME\Desktop\gaming-survey-streamlit

git init
git add .
git commit -m "Initial commit - Gaming Report 2025"
```

Then create a new repo on GitHub:
1. Go to **github.com/new**
2. Name it `gaming-survey` (or anything you like)
3. Do NOT check "Add a README" (we already have one)
4. Click **Create repository**
5. Copy the two commands GitHub shows under "push an existing repository":

```bash
git remote add origin https://github.com/YOUR_USERNAME/gaming-survey.git
git branch -M main
git push -u origin main
```

### Step 2 — Connect to Streamlit Cloud

1. Go to **share.streamlit.io**
2. Sign in with your GitHub account
3. Click **New app**
4. Select your `gaming-survey` repository
5. Set **Main file path** to: `app.py`
6. Click **Deploy**

In ~2 minutes you'll get a live URL like:
```
https://gaming-survey-YOURNAME.streamlit.app
```

Share this link with anyone — they can view the survey without installing anything.


## How to Update Content

### Edit the data
Open `survey_data.json` in VS Code (or any text editor).  
Each agenda has a `charts` array. Each chart has:

- `title` — chart heading
- `labels` — x-axis or y-axis labels
- `datasets` — the actual numbers (each dataset = one bar color)
- `note` — footnote text below the chart

### Push changes
After editing, push to GitHub:

```bash
git add survey_data.json
git commit -m "Updated survey data"
git push
```

Streamlit Cloud auto-detects the push and **redeploys in ~30 seconds**.  
Everyone with the link sees the updated version.


## Adding a New Question/Agenda

Add a new object to the `agendas` array in `survey_data.json`:

```json
{
  "id": "q99",
  "name": "Q99: Your New Question",
  "icon": "🆕",
  "color": "#CC2936",
  "summary": "Description of this section.",
  "charts": [
    {
      "id": "q99_chart1",
      "title": "Chart title here",
      "type": "stacked_bar",
      "labels": ["A", "B", "C"],
      "datasets": [
        { "label": "Group 1", "data": [40, 30, 20], "color": "#CC2936" },
        { "label": "Group 2", "data": [25, 35, 40], "color": "#1B4965" }
      ],
      "note": "Explanatory note."
    }
  ]
}
```

Chart types:
- `stacked_bar` — vertical stacked bars
- `horizontal_stacked` — horizontal stacked bars (good for rankings/long labels)


## Project Structure

```
gaming-survey-streamlit/
├── app.py                 ← Streamlit app (the website)
├── survey_data.json       ← YOUR DATA — edit this to update everything
├── requirements.txt       ← Python dependencies
├── .streamlit/
│   └── config.toml        ← Theme colors and settings
├── .gitignore
└── README.md
```


## Troubleshooting

**"streamlit: not found"** → Run `pip install streamlit` first.

**Charts not showing** → Check `survey_data.json` is valid JSON (no trailing commas). Use jsonlint.com to validate.

**Streamlit Cloud deploy fails** → Check the deploy logs. Most common issue is a missing package in `requirements.txt`.

**Want to password-protect it?** → Add to the top of `app.py`:
```python
password = st.text_input("Password", type="password")
if password != "your_secret":
    st.stop()
```
