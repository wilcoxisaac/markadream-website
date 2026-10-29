# Mark A Dream — Website

The public website for **Mark A Dream**, a private investment group. It is a static site: no server, no database, no build tools beyond one Python script. It runs on any static host, including GitHub Pages.

## What's in this repository

```
markadream-website/
├── index.html                 ← the live site (generated; GitHub Pages serves this)
├── 404.html                   ← sends unknown paths back to the site (generated)
├── .nojekyll                  ← tells GitHub Pages to serve files as-is
├── CNAME                      ← custom domain (markadream.com) — keep this file
├── src/
│   └── template.html          ← EDIT THIS: all pages, styles, scripts, and copy
├── assets/
│   ├── img/                   ← optimized images used by the site (logo, "M" mark)
│   └── brand/                 ← original full-resolution logo files
├── dist/
│   └── MarkADream-site.html   ← single self-contained file (images embedded) for email/offline sharing
└── build.py                   ← regenerates index.html, 404.html, and dist/ from src/template.html
```

## Making changes

1. Edit `src/template.html`.
2. Run `python3 build.py` (Python 3, no packages needed).
3. Commit and push. GitHub Pages republishes automatically within a minute or two.

Image placeholders in the template (`%%LOGO%%`, `%%MARK%%`, `%%MARKSM%%`) are filled in by `build.py`. Don't hand-edit `index.html` or `dist/`; your changes would be overwritten on the next build.

## Publishing

### Live site
**https://markadream.com** (GitHub Pages, branch `main`, folder `/ (root)`). The `CNAME` file in the repo root holds the custom domain; keep it.

DNS (GoDaddy): four `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` → `markadream.com` (or `wilcoxisaac.github.io`).

### Re-creating the custom domain setup
1. Settings → Pages → *Custom domain* → enter `markadream.com` and save (this adds a `CNAME` file).
2. At the domain registrar, point DNS to GitHub Pages:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` record for `www`: `<github-username>.github.io`
3. Back in Settings → Pages, tick **Enforce HTTPS** once the certificate is issued.

### Other hosts
Netlify, Cloudflare Pages, or any web host: upload the repository root (or connect the repo). No build step is required on the host because `index.html` is committed already built.

## Forms

All forms (founder submission, seller inquiry, investor list, referral partner, contact, quarterly letter) send each submission by email using [FormSubmit](https://formsubmit.co):

- **To:** adam.wilcox3@gmail.com
- **Copy (CC):** wilcoxisaac@gmail.com

Each email has a clear subject (for example, *Mark A Dream · Founder submission (Strong fit, 92/100)*), a table of the answers, and the submitter's email set as reply-to.

**One-time activation:** the first submission from the live site triggers an activation email from FormSubmit to adam.wilcox3@gmail.com. Click **Activate Form** in that email; submissions are delivered from then on. Send a test from the live site right after publishing.

**Recommended after activation:** FormSubmit's activation email includes a private alias (a random string). Replace the address in `FORM_TO` inside `src/template.html` with that alias, rebuild, and push, so the Gmail address no longer appears in the public page source.

Forms only deliver from a real web address (GitHub Pages, Netlify, etc.). Inside the Claude artifact preview, outside requests are blocked, so a submission there shows a "couldn't send" message.

Spam protection: each form includes a hidden honeypot field that FormSubmit uses to discard bot submissions.

## Content placeholders to replace before a public launch

Items marked with a dotted underline on the site need real information: managing partner name and bio, check-size range, investor minimums, and the public contact email. The internal **Site review** page (footer → *Site review (internal)*) lists these plus a launch checklist; remove it from `src/template.html` before launch.

## Compliance note

The investor pages are written for a relationship-first approach under Regulation D. Have securities counsel review the Disclosures, Terms, and Privacy pages before the site is promoted.
