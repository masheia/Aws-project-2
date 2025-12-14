# 📤 Publishing to GitHub - Step by Step Guide

## Step 1: Create a GitHub Repository

1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Enter repository name (e.g., `face-recognition-attendance-system`)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

### Option A: If you haven't pushed anything yet (use this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Option B: If you already have commits:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name!**

## Step 3: Authentication

### If you get authentication errors:

**Option 1: Use Personal Access Token (Recommended)**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name, select scopes: `repo` (all)
4. Generate and copy the token
5. When prompted for password, paste the token (not your GitHub password)

**Option 2: Use GitHub CLI**
```bash
gh auth login
```

**Option 3: Use SSH (Advanced)**
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Common Errors and Solutions

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Error: "fatal: refusing to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
```

### Error: "authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH keys

### Error: "large files" or "file too large"
- Make sure `.gitignore` is properly set up
- Remove large files: `git rm --cached LARGE_FILE`
- Commit the change

## Quick Command Reference

```bash
# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Your commit message"

# Add remote (first time only)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

