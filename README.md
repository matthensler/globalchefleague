# Global Chef League website (Phase 1, static HTML)

## Current mode: recruitment landing page

Right now the site is in **landing mode**. The home page is a single member-recruitment page, and every Join button goes to the live Stripe Payment Link. The only other pages published are the ones the join flow needs: `welcome/`, `submit-profile/`, the legal pages and `404.html`.

When the full build is ready, open `_build/build.py`, set `LANDING_MODE = False`, and run `python3 _build/build.py`. That regenerates all 9 pages of the full site (directory, chef profiles, competitions and the rest).


This is a plain HTML/CSS site with no WordPress and no build step. Upload the folder to GitHub and it runs on GitHub Pages as it is.

## What's in here

| Path | Page |
|---|---|
| `index.html` | Home |
| `chefs/` | Find a Chef directory, with search and filters |
| `chefs/<name>/` | Chef profiles (6 sample chefs) |
| `competitions/` | Chef Battle, World Chef Cup and upcoming events |
| `membership/` | $25/year membership, at-a-glance table and FAQ |
| `about/`, `contact/` | About and Contact (contact form) |
| `welcome/` | Stripe success page (hidden from search engines) |
| `submit-profile/` | Profile submission form (hidden from search engines) |
| `membership-terms/`, `privacy/`, `terms/`, `directory-disclaimer/` | Legal pages |
| `404.html`, `sitemap.xml`, `robots.txt` | Housekeeping |
| `assets/` | CSS, JS, fonts, logos |
| `_build/build.py` | Optional generator (see "Editing" below) |

## 1. Put it on GitHub Pages

1. Create a new repository on GitHub, e.g. `globalchefleague-site`.
2. Upload **the contents** of this folder to the root of the repo, so `index.html` sits at the top level. Use **Add file → Upload files** and drag everything in.
3. Go to **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, then branch `main` and folder `/ (root)`. Save.
4. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`.

**Custom domain (globalchefleague.com):** in Settings → Pages, enter the domain under **Custom domain** and turn on **Enforce HTTPS**. At your domain registrar, add the DNS records GitHub shows you. GitHub creates a `CNAME` file in the repo for you.

> If you stay on the `github.io/<repo-name>/` address and don't use a custom domain, the 404 page needs one change: in `404.html`, replace `href="/` and `src="/` with `href="/<repo-name>/` and `src="/<repo-name>/`. Every other page uses relative links and works at either address.

## 2. Connect the forms (the Stripe link is already set)

Use find-and-replace across all files (in VS Code, **Edit → Replace in Files**):

| Find | Replace with |
|---|---|
| `https://formspree.io/f/REPLACE_CONTACT_FORM_ID` | Your Formspree endpoint for the contact form |
| `https://formspree.io/f/REPLACE_PROFILE_FORM_ID` | Your Formspree endpoint for profile submissions |

Until you replace them, the forms show a "not connected yet" message and the join buttons go to a dead Stripe URL.

**Stripe:** Product "Global Chef League Annual Membership", public name "League Chef Membership", $25 USD, recurring yearly. Create a Payment Link. Under **After payment**, set the redirect to `https://globalchefleague.com/welcome/`. Turn on the Customer Portal so members can cancel.

**Forms (Formspree):** sign up at formspree.io and create two forms, Contact and Profile. Each one gives you an endpoint like `https://formspree.io/f/abcd1234`. Submissions arrive by email. Note: **the profile photo upload needs a paid Formspree plan**, because file uploads aren't free. If you'd rather stay on the free plan, change the photo field on `submit-profile/` to a "link to your photo" text field.

## 3. Before launch

- **Real chefs and events.** Everyone on the site now is a sample: 6 chefs and 4 events, all labeled "illustrative". Replace them (see Editing).
- **Photography.** The sample profile on the landing page uses free Unsplash stock photos as placeholders (set in `PHOTOS` near the top of `_build/build.py`). Replace them with real chef photos before launch. Everywhere else, every photo is a striped placeholder box labeled with the shot it needs. To add a photo, put the image file inside the placeholder div:
  `<div class="ph">Profile photo<img src="../../assets/img/maria.jpg" alt="Chef Maria Santos"></div>`
  The image fills the box automatically.
- **Legal text.** The Membership Terms, Privacy and Website Terms pages are placeholders. The Directory Disclaimer has draft wording. Have your attorney supply or approve all four.
- **Fonts.** Montserrat, Barlow, Barlow Condensed and Big Shoulders Display are free stand-ins and are self-hosted in `assets/fonts/`. When you license the final fonts, drop in the files and update the `@font-face` lines at the top of `assets/css/styles.css`.
- **Logo.** The logos in `assets/img/` were traced from the brand guidelines PDF as vectors. Swap in the master artwork files when you have them, keeping the same file names.
- **Contact email.** `chefbattle@hoptoit.events` appears on the Contact page. Change it if needed.

## Editing

You can edit in either of two ways. Pick one:

**A. Edit the HTML directly.** This is simplest for small text changes. Note that the header and footer are repeated in every page, so a nav change means editing every file.

**B. Edit `_build/build.py` and regenerate.** All settings (Stripe link, form IDs, domain), chefs, events, FAQs and page copy live at the top of that one file. Change them there, then run:

```
python3 _build/build.py
```

This rewrites every page, including the nav, footer, sitemap and chef profiles. To add a chef, copy one of the entries in `CHEFS` and edit it, and the profile page and directory row are created for you. Any changes you made directly in the HTML files get overwritten, which is why you should stick to one method. The `_build` folder is not published by GitHub Pages.

## Adding a new member (Phase 1 manual flow)

1. The chef pays through Stripe, lands on `/welcome/`, then submits `/submit-profile/`.
2. You get the submission by email from Formspree.
3. Check Stripe to confirm the payment is active.
4. Add the chef to `CHEFS` in `build.py`, add their photos to `assets/img/`, and rebuild. Then upload the changed files to GitHub.
5. Publish only if they gave at least one public contact method: email, phone or booking link.
