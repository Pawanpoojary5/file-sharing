# 🚀 Quick GitHub Upload Steps

## **SUPER QUICK VERSION (5 minutes)**

### **Step 1: Install Git**
Download and install from: https://git-scm.com/download/win

### **Step 2: Configure Git**
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### **Step 3: Initialize Repository**
```bash
cd c:\file_sharing\sharing
git init
git add .
git commit -m "Initial commit: File Sharing App"
```

### **Step 4: Create GitHub Repository**
1. Go to https://github.com/new
2. Name: `file-sharing`
3. Make it Public
4. Click "Create repository"

### **Step 5: Push to GitHub**
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/file-sharing.git
git push -u origin main
```

When asked for password, use **Personal Access Token** from:
https://github.com/settings/tokens (create new with `repo` scope)

### **Done!** 🎉
Your project is on GitHub at: `https://github.com/YOUR_USERNAME/file-sharing`

---

## **EVEN EASIER: GitHub Desktop**

1. Download: https://desktop.github.com
2. Sign in with GitHub
3. Click "Create New Repository"
4. Name: `file-sharing`
5. Local Path: `C:\file_sharing\sharing`
6. Click "Create"
7. Add commit message
8. Click "Publish repository"

**Done!** 🎉

---

## **After Upload**

Share your repository:
```
https://github.com/YOUR_USERNAME/file-sharing
```

To make changes later:
```bash
cd c:\file_sharing\sharing
git add .
git commit -m "Your change description"
git push
```

That's it! 🚀
