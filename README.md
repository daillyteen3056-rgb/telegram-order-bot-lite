# Telegram Order Bot — single-file aiogram 3 shop template (Python, MIT)

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue.svg)](https://docs.aiogram.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/daillyteen3056-rgb/telegram-order-bot-lite?style=social)](https://github.com/daillyteen3056-rgb/telegram-order-bot-lite/stargazers)

A tiny, readable **Telegram shop bot** in modern Python (`aiogram 3`): product catalog → cart → FSM checkout, in one file. Built for small shops, Fiverr builds, and anyone who wants a clean starting point for a production order bot — not a 3000-LOC framework.

> ⭐ **If this saves you an afternoon, star it** — it helps other devs find the repo on `topic:aiogram-3`.

**Live demo bot:** [@quickorder_myshop_bot](https://t.me/quickorder_myshop_bot) — send `/start`
**Landing page:** [telegramorder-bot.pages.dev](https://telegramorder-bot.pages.dev/?utm_source=github&utm_medium=readme&utm_campaign=lite_homepage)
**Architecture write-up:** [Hashnode article](https://shippingpython.hashnode.dev/how-i-packaged-6-fiverr-telegram-bot-gigs-into-one-aiogram-3-template)

---

## What it does

- Browse products grouped by category (edit `products.json`, that's the catalog)
- Add to cart with quantity
- FSM-based checkout: name → phone → address → confirm
- Prints a fake order ID when done

That's the whole thing. One file, ~250 lines, readable in 10 minutes.

## Run it

```bash
git clone https://github.com/daillyteen3056-rgb/telegram-order-bot-lite
cd telegram-order-bot-lite
cp .env.example .env     # add your BOT_TOKEN
pip install -r requirements.txt
python bot.py
```

Get a `BOT_TOKEN` from [@BotFather](https://t.me/BotFather) in Telegram.

## Try it live

Message [@quickorder_myshop_bot](https://t.me/quickorder_myshop_bot) on Telegram → `/start`. It runs this exact flow (on the full version — same UX).

## Editing the catalog

Open `products.json`. Each item needs `id`, `name`, `description`, `price`, `category`, `in_stock`. Save, restart. Done.

```json
{
  "id": "coffee-espresso",
  "name": "Espresso",
  "description": "Double shot.",
  "price": 3.50,
  "in_stock": true,
  "category": "coffee"
}
```

---

## What's missing (on purpose)

This LITE version is deliberately minimal. If you need any of these, the full version has them:

| Feature | Lite | Full |
|---|---|---|
| Catalog, cart, checkout FSM | ✅ | ✅ |
| **Admin notifications** on every order | ❌ | ✅ |
| **Google Sheets** order log | ❌ | ✅ |
| **Railway / Render** deploy configs | ❌ | ✅ |
| Order history for customers | ❌ | ✅ |
| Modular handler files (easier to extend) | ❌ | ✅ |
| Webhook mode + long-polling | ❌ (polling only) | ✅ |
| Written setup guide + 12-min video | ❌ | ✅ |
| Developer license (resell client bots) | ❌ | ✅ (Developer tier) |
| Email support | ❌ | ✅ |

**Full version:** $9 launch (going to $29 on Dec 1) → [daillyteen.gumroad.com/l/telegram-order-bot](https://daillyteen.gumroad.com/l/telegram-order-bot?utm_source=github&utm_medium=readme&utm_campaign=lite_readme)

If LITE is enough for you, use it. No guilt. If you're deploying for a real shop or reselling on Fiverr, the full version saves hours and gives you a license to use it in client work.

---

## License

MIT. Fork it, ship it, charge money with it, whatever. Credit appreciated but not required.

## Contributing

Issues + PRs welcome. Scope rule: PRs must stay within what LITE does (catalog/cart/checkout). Admin notifications, Sheets, deploy configs — those live in the full version. Keeps both codebases simple.

---

## FAQ

**Is this a Telegram shop bot I can use for my own store?**
Yes. Edit `products.json`, add your `BOT_TOKEN`, run `python bot.py`. You own the code.

**Can I deploy this to Railway / Render / Fly?**
LITE runs on long-polling only — works on any host that keeps a Python process alive. For a one-click Railway config + Volume mounting + webhook mode, see the full version. There's also a [write-up on the 3 Railway traps](https://shippingpython.hashnode.dev/deploying-a-telegram-bot-to-railway-in-2026-the-3-traps-nobody-mentions) that will save you half a day.

**Does it handle payments?**
Not in LITE. The checkout collects name/phone/address and prints a fake order ID. For order collection + admin alerts + Google Sheets logging, grab the [full version on Gumroad](https://daillyteen.gumroad.com/l/telegram-order-bot?utm_source=github&utm_medium=readme&utm_campaign=lite_readme_faq). Stripe + Telegram native Payments ship in v1.1 (Q1 2027), free for buyers.

**Why aiogram 3 instead of `python-telegram-bot` / `pyTelegramBotAPI`?**
Tried all three. aiogram 3's router pattern + native FSM felt the cleanest for multi-handler apps. If you're already on `python-telegram-bot v20+`, no reason to switch — both are production-ready.

**Can I resell bots I build from this?**
LITE is MIT. Fork, extend, ship it — including client work. Full version has a Developer tier if you prefer a license for commercial resale with a formal grant.

**What Python version?**
3.10+. Pin 3.12 if you want to avoid [the Python 3.13 pydantic-core trap on Railway](https://shippingpython.hashnode.dev/deploying-a-telegram-bot-to-railway-in-2026-the-3-traps-nobody-mentions).

**How does this compare to no-code bot builders (BotFather alone, ManyBot, Chatfuel)?**
Those are faster for toy flows. This is faster the moment you want custom logic — real order parsing, per-user state, integration with an API or a database. If you'd write Python anyway, this skips the boilerplate.

---

## Keywords (SEO, you can ignore)

telegram order bot · python telegram bot template · aiogram 3 example · telegram ecommerce bot · telegram shop bot · aiogram checkout FSM · telegram bot python open source · MIT telegram bot template
