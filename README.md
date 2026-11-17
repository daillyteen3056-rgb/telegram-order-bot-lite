# Telegram Order Bot — LITE

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue.svg)](https://docs.aiogram.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A single-file Telegram bot that walks a customer from catalog → cart → checkout, in modern Python (`aiogram 3`).

Free, MIT, hack away.

---

## What it does

- Browse products grouped by category (edit `products.json`, that's the catalog)
- Add to cart with quantity
- FSM-based checkout: name → phone → address → confirm
- Prints a fake order ID when done

That's the whole thing. One file, ~250 lines, readable in 10 minutes.

## Run it

```bash
git clone https://github.com/YOUR_USER/telegram-order-bot-lite
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

**Full version:** $9 launch (going to $29 on Dec 1) → [FULL_VERSION_URL]

If LITE is enough for you, use it. No guilt. If you're deploying for a real shop or reselling on Fiverr, the full version saves hours and gives you a license to use it in client work.

---

## License

MIT. Fork it, ship it, charge money with it, whatever. Credit appreciated but not required.

## Contributing

Issues + PRs welcome. Scope rule: PRs must stay within what LITE does (catalog/cart/checkout). Admin notifications, Sheets, deploy configs — those live in the full version. Keeps both codebases simple.
