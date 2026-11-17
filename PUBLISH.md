# Publishing the lite to GitHub

5 min. This becomes the free tier of the freemium funnel: free lite on GitHub → README links to paid full on Gumroad.

## 1. Create repo

github.com → **New repository**
- Name: `telegram-order-bot-lite` (any name — `telegram-order-bot` works too, but keeping "lite" in the name signals that there's a fuller version)
- **Public** (this one must be public — social proof + SEO + Reddit allows GitHub links)
- Don't init with README / license / gitignore (we have them)

## 2. Edit placeholders before you push

**`README.md`** — replace `[FULL_VERSION_URL]` with your Gumroad URL.

**`LICENSE`** — replace `[YOUR NAME]` with your name.

## 3. Push

```powershell
cd C:\Users\admin\Desktop\claudfake\trump\bots\order-bot-lite
git init
git add .
git commit -m "Initial: single-file Telegram order bot"
git branch -M main
git remote add origin https://github.com/YOUR_USER/telegram-order-bot-lite.git
git push -u origin main
```

**Confirm `.env` is NOT in the repo.** On GitHub, open the file list — you should see `.env.example` only. If `.env` appears, delete it on GitHub immediately and rotate your BotFather token.

## 4. Polish the repo page

- Add a **description** (top-right): `Single-file Telegram order bot — catalog, cart, FSM checkout. aiogram 3.`
- Add **topics**: `telegram-bot`, `aiogram`, `python`, `ecommerce`, `order-bot`, `template`
- Add a **link** (top-right): your landing page URL
- Pin it to your profile (profile → customize pins)

## 5. Use the repo in Reddit launches

Post `trump/reddit-outreach/launch-posts.md` references `[GITHUB_LITE_URL]` — now that the repo is live, that URL exists. Paste it in.

## Maintenance

Only merge PRs that stay within the lite scope (catalog/cart/checkout). Admin alerts, Sheets, deploy configs — those are the full version's job. Redirect contributors who want those to the full version.
