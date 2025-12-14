# 🚀 Quick GitHub Setup

## ✅ Files are now committed!

Your files are ready to push to GitHub. Follow these steps:

## Step 1: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `face-recognition-attendance-system` (or any name you want)
3. **Important:** Leave all checkboxes UNCHECKED (don't add README, .gitignore, or license)
4. Click **"Create repository"**

## Step 2: Copy Your Repository URL

After creating, GitHub will show you a URL like:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Copy this URL!

## Step 3: Connect and Push

Run these commands in your terminal (replace with your actual URL):

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

## Common Errors

### ❌ Error: "remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### ❌ Error: "authentication failed" or "fatal: could not read Username"
**Solution:** Use a Personal Access Token instead of password:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scope: `repo` (check all repo permissions)
4. Generate and **copy the token** (you won't see it again!)
5. When Git asks for password, paste the token (not your GitHub password)

### ❌ Error: "fatal: refusing to merge unrelated histories"
**Solution:**
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### ❌ Error: "fatal: The current branch main has no upstream branch"
**Solution:**
```bash
git push -u origin main
```

## ✅ Success!

Once pushed successfully, you'll see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

Your repository will be live at: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

