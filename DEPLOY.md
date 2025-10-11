# 🚀 Deploy to GitHub Pages

## Quick Deployment Guide

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New Repository" (green button)
3. Name it: `nadi-dosha-calculator` (or any name you like)
4. Set to **Public**
5. Click "Create repository"

### Step 2: Upload Your Files

**Method A: Using GitHub Web Interface (Easiest)**

1. On your repository page, click "uploading an existing file"
2. Drag and drop ALL files from this folder
3. Add commit message: "Initial commit"
4. Click "Commit changes"

**Method B: Using Git Command Line**

```bash
# In your project folder, run:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/nadi-dosha-calculator.git
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Pages" in the left sidebar
4. Under "Source", select:
   - Source: **Deploy from a branch**
   - Branch: **main** (or master)
   - Folder: **/ (root)**
5. Click "Save"

### Step 4: Wait for Deployment

- GitHub will build and deploy your site (takes 1-2 minutes)
- You'll see a blue banner saying "Your site is ready"
- Your URL will be: `https://YOUR-USERNAME.github.io/nadi-dosha-calculator/`

### Step 5: Access Your App

Visit: `https://YOUR-USERNAME.github.io/nadi-dosha-calculator/`

🎉 **Done!** Your app is now live on the internet!

---

## Automatic Deployment (Advanced)

The included `.github/workflows/deploy.yml` file enables automatic deployment:

**Every time you push changes to GitHub:**
1. GitHub Actions automatically builds
2. Deploys to GitHub Pages
3. Your site updates automatically

**To enable this:**
1. Go to Settings → Pages
2. Change Source to: **GitHub Actions**
3. Push any changes to trigger deployment

---

## Update Your App

**To update after deployment:**

```bash
# Make your changes to the files
git add .
git commit -m "Your update description"
git push
```

GitHub Pages will automatically update in 1-2 minutes!

---

## Custom Domain (Optional)

Want your own domain like `astrology.yourdomain.com`?

1. Buy a domain from any registrar (Namecheap, GoDaddy, etc.)
2. In your repository settings → Pages
3. Add your custom domain
4. Update your domain's DNS settings (GitHub provides instructions)

---

## Troubleshooting

### Site Not Showing Up?

1. **Wait**: First deployment takes 5-10 minutes
2. **Check Settings → Pages**: Look for green success message
3. **Check Branch**: Make sure you selected correct branch (main/master)
4. **Clear Browser Cache**: Ctrl+F5 to force refresh

### 404 Error?

- Make sure `index.html` is in the root folder
- Check that repository is Public (not Private)
- Verify the URL format: `https://username.github.io/repo-name/`

### APIs Still Not Working?

- Check browser console (F12) for specific error messages
- GitHub Pages uses HTTPS - all API calls should work
- Nominatim prefers requests from proper domains (GitHub Pages works great!)

---

## Benefits of GitHub Pages vs Local Server

| Feature | Local Server | GitHub Pages |
|---------|-------------|--------------|
| **Access** | Only on your computer | Anywhere in the world |
| **CORS** | Need to run server | No issues |
| **APIs** | May be blocked | Full access |
| **Sharing** | Can't share | Share URL with anyone |
| **Updates** | Manual restart | Automatic |
| **Cost** | Free | Free |
| **Setup Time** | Every use | Once only |

---

## Security & Privacy

- ✅ All calculations happen in the browser (client-side)
- ✅ No data is stored on servers
- ✅ No backend database
- ✅ Birth data never leaves the user's browser
- ✅ API calls go directly from user's browser to services

---

## Example Deployed Sites

Your URL will look like:
- `https://yourusername.github.io/nadi-dosha-calculator/`
- Or with custom domain: `https://nadi.yourdomain.com`

Share this URL with anyone - they can use the calculator without installing anything!

---

## Next Steps After Deployment

1. ✅ Test all functionality on the live site
2. ✅ Share the URL with users
3. ✅ Add the URL to your README.md
4. ✅ Consider adding Google Analytics (optional)
5. ✅ Set up a custom domain (optional)

---

## Need Help?

- **GitHub Pages Docs**: https://pages.github.com
- **GitHub Actions**: https://docs.github.com/en/actions
- **DNS Setup**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

🎉 **Enjoy your live Nadi Dosha Calculator!**

