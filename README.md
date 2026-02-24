# 86 Agency - AI Outreach Generator

Complete web app for generating multi-channel outreach sequences.

## Features
- 🔥 4-email sequences (Day 1, 3, 7, 10)
- 💼 LinkedIn connection messages
- 📞 Call scripts with objections
- ⚡ Beautiful purple/pink gradient UI
- 🎯 Powered by Claude AI

## Quick Deploy to Streamlit Cloud

### Step 1: Create GitHub Account
1. Go to github.com
2. Sign up with your email
3. Verify email

### Step 2: Create New Repository
1. Click "+" in top right → "New repository"
2. Name: `86agency-outreach`
3. Description: `AI-powered outreach generator`
4. Public
5. Click "Create repository"

### Step 3: Upload Files
1. Click "uploading an existing file"
2. Drag and drop these 3 files:
   - streamlit_app.py
   - requirements.txt
   - README.md
3. Scroll down, click "Commit changes"

### Step 4: Deploy to Streamlit Cloud
1. Go to share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: Select `86agency-outreach`
5. Branch: `main`
6. Main file path: `streamlit_app.py`
7. Click "Deploy"
8. Wait 2-3 minutes

### Step 5: Your App is Live! 🎉
You'll get a URL like: `https://86agency-outreach.streamlit.app`

## How to Use the App

1. **Get Claude API Key**
   - Go to console.anthropic.com
   - Create account
   - Get API key

2. **Upload CSV**
   - Must have: Email, First Name, Company columns
   - Export from Apollo

3. **Generate**
   - Enter API key in sidebar
   - Upload CSV
   - Click "Generate Outreach"
   - Wait for completion

4. **Download**
   - Get complete CSV with all outreach content
   - Import to Apollo or your CRM

## Local Development

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Support

Built for 86 Agency • Powered by Claude AI
