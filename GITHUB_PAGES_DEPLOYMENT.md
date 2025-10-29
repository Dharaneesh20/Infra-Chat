# 🌐 GitHub Pages Deployment Guide

This guide explains how to deploy the Infra-Chat landing page to GitHub Pages.

## 📋 Prerequisites

- GitHub repository created and pushed
- GitHub account with repository access

## 🚀 Quick Deployment

### Method 1: GitHub Settings (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git push origin master
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click **Settings** → **Pages** (left sidebar)
   - Under "Source", select **Branch: master**
   - Under "Folder", select **/ (root)**
   - Click **Save**

3. **Access your site:**
   - Your site will be available at: `https://yourusername.github.io/infra-chat/`
   - It may take 2-3 minutes for the first deployment

### Method 2: GitHub Actions (Advanced)

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ master ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Pages
        uses: actions/configure-pages@v3
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

## 📝 Important Notes

### Update GitHub Repository Links

Before deploying, update the repository URL in these files:

**index.html** - Replace `yourusername` with your actual GitHub username:
```html
<!-- Line 35, 42, etc. -->
<a href="https://github.com/YOURUSERNAME/infra-chat">

<!-- Update all occurrences -->
```

**Quick find & replace:**
```bash
# In PowerShell
(Get-Content index.html) -replace 'yourusername', 'ACTUAL_USERNAME' | Set-Content index.html
```

### Files Deployed to GitHub Pages

The following files are served from the root directory:
- ✅ `index.html` - Main landing page
- ✅ `styles.css` - All styles and animations
- ✅ `script.js` - Interactive features
- ✅ `README.md` - Linked from footer
- ✅ `LICENSE` - Linked from footer

### Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file to the repository root:
   ```bash
   echo "yourdomain.com" > CNAME
   git add CNAME
   git commit -m "feat: add custom domain"
   git push
   ```

2. Configure DNS:
   - Add a CNAME record: `www.yourdomain.com` → `yourusername.github.io`
   - Add A records for apex domain pointing to GitHub IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153

3. Update in GitHub Settings → Pages → Custom domain

## 🎨 Customization

### Update Branding

1. **Replace Logo/Icon:**
   - Edit the SVG in `index.html` (search for `<svg width="32"`)
   - Or add an image: `<img src="logo.png" alt="Infra-Chat">`

2. **Change Colors:**
   - Edit CSS variables in `styles.css`:
   ```css
   :root {
       --primary: #6366f1;      /* Change to your color */
       --secondary: #8b5cf6;    /* Change to your color */
   }
   ```

3. **Update Content:**
   - All text is in `index.html`
   - Modify sections as needed
   - Update features, tech stack, roadmap, etc.

### Add Analytics

Add Google Analytics before `</head>` in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 🔧 Troubleshooting

### Site Not Loading

1. **Check GitHub Pages Settings:**
   - Ensure source is set to `master` branch
   - Wait 2-3 minutes after enabling

2. **404 Error:**
   - Verify `index.html` is in the repository root
   - Check file capitalization (case-sensitive)

3. **CSS Not Loading:**
   - Verify `styles.css` path is correct
   - Check browser console for errors
   - Clear browser cache (Ctrl+Shift+R)

### Broken Links

Update relative links if using a custom domain:
```html
<!-- Before -->
<a href="README.md">Documentation</a>

<!-- After (for subpath deployment) -->
<a href="/infra-chat/README.md">Documentation</a>
```

### Images Not Displaying

If you add images, use absolute paths:
```html
<!-- Relative path (might break) -->
<img src="images/screenshot.png">

<!-- Absolute path (recommended) -->
<img src="/infra-chat/images/screenshot.png">
```

## 📊 Performance Optimization

### Enable Caching

GitHub Pages automatically caches static files.

### Minify Assets (Optional)

For production, minify CSS and JS:

```bash
# Install terser and csso-cli
npm install -g terser csso-cli

# Minify JavaScript
terser script.js -o script.min.js -c -m

# Minify CSS
csso styles.css -o styles.min.css

# Update references in index.html
```

### Use CDN for Fonts

Already implemented - using Google Fonts CDN for faster loading.

## 🎯 SEO Optimization

The landing page includes:
- ✅ Meta tags for description and keywords
- ✅ Semantic HTML structure
- ✅ Proper heading hierarchy (h1, h2, h3)
- ✅ Alt text for images/icons
- ✅ Mobile-responsive design
- ✅ Fast loading animations

### Add Open Graph Tags

For better social media sharing, add to `<head>`:

```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://yourusername.github.io/infra-chat/">
<meta property="og:title" content="Infra-Chat - AI Cloud Infrastructure Assistant">
<meta property="og:description" content="Intelligent chatbot for cloud infrastructure management">
<meta property="og:image" content="https://yourusername.github.io/infra-chat/preview.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://yourusername.github.io/infra-chat/">
<meta property="twitter:title" content="Infra-Chat - AI Cloud Infrastructure Assistant">
<meta property="twitter:description" content="Intelligent chatbot for cloud infrastructure management">
<meta property="twitter:image" content="https://yourusername.github.io/infra-chat/preview.png">
```

## 🚦 Testing Locally

Before deploying, test locally:

```bash
# Simple HTTP server with Python
python -m http.server 8000

# Or with Node.js
npx http-server

# Open in browser
# http://localhost:8000
```

## 📱 Mobile Testing

Test responsive design:
- Chrome DevTools (F12) → Device toolbar
- Resize browser window
- Test on actual mobile devices

## ✅ Deployment Checklist

Before going live:

- [ ] Update GitHub repository URLs
- [ ] Replace `yourusername` with actual username
- [ ] Test all navigation links
- [ ] Verify code copy buttons work
- [ ] Check mobile responsiveness
- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Verify animations work smoothly
- [ ] Check all external links open correctly
- [ ] Review SEO meta tags
- [ ] Add analytics (optional)
- [ ] Test scroll behavior
- [ ] Verify footer links

## 🎉 Post-Deployment

After deployment:

1. **Share Your Site:**
   - Add link to repository README
   - Share on social media
   - Add to portfolio

2. **Monitor:**
   - Check GitHub Actions for deployment status
   - Monitor Google Analytics (if added)
   - Review user feedback

3. **Maintain:**
   - Update content regularly
   - Keep dependencies updated
   - Add new features to roadmap

## 📞 Support

If you encounter issues:

1. Check [GitHub Pages documentation](https://docs.github.com/en/pages)
2. Review the [troubleshooting section](#-troubleshooting)
3. Open an issue on the repository
4. Check browser console for errors

---

**Your landing page is now live!** 🎊

Visit: `https://yourusername.github.io/infra-chat/`

Don't forget to star the repo! ⭐
