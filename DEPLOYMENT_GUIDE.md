# 🚀 Streamlit Cloud Deployment Guide for DocFusion

## 📁 Files to Push to GitHub

You need to push **only these 4 files** to your GitHub repository:

```
DocFusion/
├── docfusion_streamlit.py    ✅ Main application file
├── requirements.txt          ✅ Python dependencies (updated)
├── README.md                 ✅ Project documentation
└── .gitignore               ✅ Files to exclude from Git
```

### ❌ DO NOT Upload These:
- `myenv/` folder (virtual environment)
- `__pycache__/` folder (Python cache)
- `iso27001.pdf` or any PDF files (large files)
- `RAG_GroqChat.py` (old file, not used)
- Any `.env` files

---

## 📋 Step-by-Step Deployment Instructions

### **Step 1: Prepare Your GitHub Repository**

1. Go to [GitHub.com](https://github.com) and log in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `DocFusion` (or your preferred name)
   - **Description**: `AI-powered Document Q&A using RAG with free embeddings`
   - **Visibility**: Choose Public or Private (both work with Streamlit Cloud)
   - ✅ **DO NOT** initialize with README (you already have one)
4. Click **"Create repository"**

---

### **Step 2: Push Your Code to GitHub**

Open **PowerShell** and run these commands:

```powershell
# Navigate to your project directory
cd "C:\Users\Prian\OneDrive\Desktop\DocFusion"

# Initialize Git repository (if not already done)
git init

# Add only the required files
git add docfusion_streamlit.py
git add requirements.txt
git add README.md
git add .gitignore

# Create your first commit
git commit -m "Initial commit: DocFusion RAG application for Streamlit Cloud"

# Rename branch to main
git branch -M main

# Add your GitHub remote (REPLACE with your actual username and repo name)
git remote add origin https://github.com/YOUR_USERNAME/DocFusion.git

# Push to GitHub
git push -u origin main
```

**⚠️ Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

**Example:**
```powershell
git remote add origin https://github.com/prian123/DocFusion.git
```

---

### **Step 3: Deploy to Streamlit Cloud**

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** (or sign up if you don't have an account)
3. Log in with your **GitHub account**
4. Fill in the deployment form:
   - **Repository**: Select your `DocFusion` repository from the dropdown
   - **Branch**: `main`
   - **Main file path**: `docfusion_streamlit.py`
   - **App URL**: Choose a custom subdomain (e.g., `docfusion-yourname`)
   
5. Click **"Deploy!"** 🚀

---

### **Step 4: Wait for Deployment**

- Deployment takes **2-5 minutes**
- You'll see a live log of the build process
- Streamlit Cloud will:
  1. Install dependencies from `requirements.txt`
  2. Launch your application
  3. Provide you with a live URL

---

### **Step 5: Share Your App!**

Once deployed, your app will be available at:
```
https://docfusion-yourname.streamlit.app
```

**Share this URL with your network!** 🎉

---

## 🔧 Troubleshooting

### **Issue: App won't deploy**
**Solution:**
- Check the deployment logs for error messages
- Ensure `requirements.txt` has all dependencies
- Verify `docfusion_streamlit.py` has no syntax errors

### **Issue: "Module not found" errors**
**Solution:**
- Make sure all required packages are in `requirements.txt`
- Current requirements are already updated and correct

### **Issue: API key not working**
**Solution:**
1. Get a free API key from [https://console.groq.com/keys](https://console.groq.com/keys)
2. Update line 16 in `docfusion_streamlit.py` with your key
3. Commit and push the changes:
   ```powershell
   git add docfusion_streamlit.py
   git commit -m "Update Groq API key"
   git push
   ```
4. Streamlit Cloud will auto-redeploy!

### **Issue: App is slow or crashing**
**Solution:**
- Streamlit Cloud free tier has limited resources
- Consider upgrading to a paid plan for production use
- Optimize chunk size in the sidebar settings

---

## 🔄 How to Update Your App Later

Whenever you make changes to your code:

```powershell
# Check what changed
git status

# Add modified files
git add docfusion_streamlit.py
# (or git add . to add all changes)

# Commit with a descriptive message
git commit -m "Describe what you changed"

# Push to GitHub
git push
```

**Streamlit Cloud automatically redeploys** when it detects new commits! 🎯

---

## 📊 Your Current Configuration

### Files Ready for Upload:
✅ `docfusion_streamlit.py` - Main application (8.4 KB)
✅ `requirements.txt` - Dependencies (updated)
✅ `README.md` - Documentation (3.2 KB)
✅ `.gitignore` - Git exclusions (newly created)

### Dependencies to be Installed:
- streamlit
- langchain
- langchain-community
- langchain-classic
- langchain-groq
- langchain-core
- faiss-cpu
- pypdf
- numpy

---

## 🎯 Quick Checklist

Before deploying, verify:
- [ ] GitHub repository created
- [ ] All 4 files added to Git
- [ ] Code pushed to GitHub successfully
- [ ] Streamlit Cloud account created
- [ ] App configured with correct file path (`docfusion_streamlit.py`)
- [ ] Groq API key is set in line 16 of the code
- [ ] Deployment completed successfully

---

## 💡 Pro Tips

### **1. Use Streamlit Secrets for API Keys (More Secure)**

Instead of hardcoding your API key in the code, use Streamlit's built-in secrets management:

#### **Step 1: Add Secret in Streamlit Cloud Dashboard**
1. Go to your app in Streamlit Cloud: [https://share.streamlit.io](https://share.streamlit.io)
2. Click on your deployed app
3. Click **"Settings"** (gear icon) in the top right
4. Scroll down to **"Secrets"** section
5. Add your secret in TOML format:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
6. Click **"Save"**

#### **Step 2: Update Your Code**
Modify line 16 in `docfusion_streamlit.py` to read from secrets:

**Replace this:**
```python
GROQ_API_KEY = ""
```

**With this:**
```python
# Try to get API key from Streamlit secrets, fallback to hardcoded value for local development
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
```

#### **Step 3: Commit and Push**
```powershell
git add docfusion_streamlit.py
git commit -m "Use Streamlit secrets for API key"
git push
```

**Benefits:**
- ✅ API key not exposed in GitHub repository
- ✅ Easy to rotate/update keys without code changes
- ✅ Works for both local development and production
- ✅ More secure for public repositories

---

### **2. Other Pro Tips**

- **Keep your repository public** if you want to share with others easily
- **Monitor your app** from the Streamlit Cloud dashboard
- **Custom domain** available on paid Streamlit Cloud plans
- **View analytics** to see how many people are using your app
- **Set up email notifications** for deployment failures

---

## 🆘 Need Help?

- **Streamlit Docs**: [https://docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Community**: [https://discuss.streamlit.io](https://discuss.streamlit.io)
- **Groq API**: [https://console.groq.com](https://console.groq.com)

---

**Good luck with your deployment! 🚀**
