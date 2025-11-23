# 📤 Upload File Sharing Project to GitHub

## **Step-by-Step Guide**

### **Prerequisites**

1. **GitHub Account** - Create one at https://github.com if you don't have one
2. **Git Installed** - Download from https://git-scm.com/download/win
3. **GitHub Desktop (Optional)** - Easier alternative at https://desktop.github.com

---

## **OPTION 1: Using Git Command Line (Recommended)**

### **Step 1: Install Git**

1. Go to https://git-scm.com/download/win
2. Download and install (use default settings)
3. Restart PowerShell/Terminal

### **Step 2: Configure Git**

Open PowerShell and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"
```

Example:
```bash
git config --global user.name "Pawan Poojari"
git config --global user.email "pawanpoojari026@gmail.com"
```

### **Step 3: Create .gitignore File**

Create a `.gitignore` file in `c:\file_sharing\sharing\`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
db.sqlite3
/media/
/staticfiles/
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
```

### **Step 4: Initialize Git Repository Locally**

```bash
cd c:\file_sharing\sharing
git init
git add .
git commit -m "Initial commit: File Sharing Application"
```

### **Step 5: Create GitHub Repository**

1. Go to https://github.com/new
2. Repository name: `file-sharing`
3. Description: `WiFi Network File Sharing Application - Django`
4. Make it **Public** (so others can see it)
5. **DO NOT** initialize with README (we already have one)
6. Click **"Create repository"**

### **Step 6: Add Remote and Push**

GitHub will show you commands. Run these in PowerShell:

```bash
cd c:\file_sharing\sharing
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/file-sharing.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username!

### **Step 7: Enter GitHub Credentials**

When prompted:
```
Username: your_github_username
Password: your_personal_access_token
```

**To create Personal Access Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select `repo` scope
4. Copy the token and paste it as password

---

## **OPTION 2: Using GitHub Desktop (Easier)**

### **Step 1: Install GitHub Desktop**

1. Download from https://desktop.github.com
2. Install and sign in with your GitHub account

### **Step 2: Create Repository**

1. Click "Create a New Repository"
2. Name: `file-sharing`
3. Description: `WiFi Network File Sharing Application`
4. Local Path: `C:\file_sharing\sharing`
5. Click "Create"

### **Step 3: Commit Files**

1. In GitHub Desktop, all your files appear
2. Write commit message: "Initial commit: File Sharing Application"
3. Click "Commit to main"

### **Step 4: Publish to GitHub**

1. Click "Publish repository"
2. Uncheck "Keep this code private" (to make it public)
3. Click "Publish Repository"

**Done!** Your project is now on GitHub! 🎉

---

## **OPTION 3: Upload Directly (No Git Needed)**

### **Step 1: Create Repository on GitHub**

1. Go to https://github.com/new
2. Repository name: `file-sharing`
3. Description: `WiFi Network File Sharing Application`
4. Click "Create repository"

### **Step 2: Upload Files Manually**

On the repository page:
1. Click "Add file" → "Upload files"
2. Drag and drop your project folder
3. Write commit message
4. Click "Commit changes"

**Note:** This uploads only once. For updates, use Git method.

---

## **After Upload - Repository Structure**

Your GitHub repo should look like:

```
file-sharing/
├── README.md
├── requirements.txt
├── QUICK_START.md
├── SMARTPHONE_LAPTOP_GUIDE.md
├── manage.py
├── db.sqlite3
├── sharing/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── filesharing/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
├── templates/
│   ├── home.html
│   ├── base.html
│   └── ...
└── media/
```

---

## **Push Updates After Changes**

After making changes:

```bash
cd c:\file_sharing\sharing
git add .
git commit -m "Your commit message here"
git push
```

---

## **GitHub Repository URL**

After uploading, your project will be at:

```
https://github.com/YOUR_USERNAME/file-sharing
```

Share this link with others to show them your project!

---

## **Troubleshooting**

### ❌ "Git not found"
- Download from https://git-scm.com/download/win
- Install and restart PowerShell

### ❌ "Authentication failed"
- Use Personal Access Token (not password)
- Get it from https://github.com/settings/tokens

### ❌ "Repository already exists"
- The repo was created. Just push code:
  ```bash
  git push -u origin main
  ```

### ❌ "Permission denied"
- Check GitHub username and token
- Make sure token has `repo` scope selected

---

## **What to Include/Exclude**

### **Include:**
- ✅ Source code (views.py, models.py, etc.)
- ✅ Templates (HTML files)
- ✅ Static files (CSS, JS)
- ✅ Documentation (README.md, guides)
- ✅ requirements.txt
- ✅ manage.py

### **Exclude (via .gitignore):**
- ❌ db.sqlite3 (database)
- ❌ __pycache__/ (compiled Python)
- ❌ .env (secrets)
- ❌ venv/ (virtual environment)
- ❌ media/ (uploaded files)

---

## **Next Steps**

1. **Add README.md** - Describe your project
2. **Add LICENSE** - Choose MIT, Apache 2.0, etc.
3. **Add CONTRIBUTING.md** - For contributors
4. **GitHub Pages** - Host your docs
5. **GitHub Actions** - Auto-test on push

---

## **Share Your Project**

Once on GitHub, you can:
- 🌟 Let others star your project
- 🔀 Get contributions from others
- 📝 Show it in your portfolio
- 🚀 Deploy from GitHub to servers

---

## **Example: Complete Git Workflow**

```bash
# Initial setup
cd c:\file_sharing\sharing
git config --global user.name "Pawan Poojari"
git config --global user.email "pawanpoojari026@gmail.com"

# Initialize and commit
git init
git add .
git commit -m "Initial commit: File Sharing Application"

# Create repo on GitHub at https://github.com/new
# (Name it: file-sharing)

# Connect and push
git branch -M main
git remote add origin https://github.com/pawanpoojari/file-sharing.git
git push -u origin main

# For future changes
git add .
git commit -m "Add real-time updates feature"
git push
```

---

## **Quick Reference**

| Command | What it does |
|---------|------------|
| `git init` | Initialize repository |
| `git add .` | Add all files |
| `git commit -m "message"` | Save changes |
| `git remote add origin <url>` | Connect to GitHub |
| `git push` | Upload to GitHub |
| `git pull` | Download from GitHub |
| `git status` | See changed files |
| `git log` | View commit history |

---

**Ready to upload?** Follow the steps above and let me know if you need help! 🚀
