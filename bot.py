"""
Telegram Order Bot — LITE (free, MIT).

Catalog → cart → checkout. That's it.

Intentionally missing (available in the full version):
- Admin notifications when an order comes in
- Google Sheets order log
- Railway / Render deploy configs
- Multi-admin, order history lookup
- Setup video, written setup guide, email support

Single file on purpose — easier to read, hack on, embed in another project.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("bot")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
SHOP_NAME = os.environ.get("SHOP_NAME", "Demo Shop")
CURRENCY = os.environ.get("CURRENCY_SYMBOL", "$")
PRODUCTS_FILE = os.environ.get("PRODUCTS_FILE", "products.json")

if not BOT_TOKEN:
    sys.exit("BOT_TOKEN is not set. Copy .env.example to .env and add your token.")


# --------------------------------------------------------------------------- #
#  Data
# --------------------------------------------------------------------------- #

@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    category: str
    in_stock: bool = True


def load_products(path: str) -> list[Product]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Product(**p) for p in raw if p.get("in_stock", True)]


PRODUCTS = load_products(PRODUCTS_FILE)
BY_ID: dict[str, Product] = {p.id: p for p in PRODUCTS}
CATEGORIES = sorted({p.category for p in PRODUCTS})

# { user_id: { product_id: qty } }
CARTS: dict[int, dict[str, int]] = {}


def cart_total(user_id: int) -> tuple[list[str], float]:
    cart = CARTS.get(user_id, {})
    lines: list[str] = []
    total = 0.0
    for pid, qty in cart.items():
        p = BY_ID.get(pid)
        if not p:
            continue
        sub = p.price * qty
        total += sub
        lines.append(f"• {p.name} × {qty} — {CURRENCY}{sub:.2f}")
    return lines, total


# --------------------------------------------------------------------------- #
#  Keyboards
# --------------------------------------------------------------------------- #

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛍 Catalog"), KeyboardButton(text="🛒 Cart")]],
        resize_keyboard=True,
    )


def categories_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{c.title()}", callback_data=f"cat:{c}")]
        for c in CATEGORIES
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def products_kb(category: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{p.name} — {CURRENCY}{p.price:.2f}", callback_data=f"prod:{p.id}")]
        for p in PRODUCTS if p.category == category
    ]
    rows.append([InlineKeyboardButton(text="← Back", callback_data="back:cats")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_kb(pid: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add to cart", callback_data=f"add:{pid}")],
        [InlineKeyboardButton(text="← Back", callback_data=f"back:cat:{BY_ID[pid].category}")],
    ])


def cart_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Checkout", callback_data="checkout")],
        [InlineKeyboardButton(text="🗑 Clear cart", callback_data="clear")],
    ])


# --------------------------------------------------------------------------- #
#  FSM
# --------------------------------------------------------------------------- #

class Checkout(StatesGroup):
    name = State()
    phone = State()
    address = State()
    confirm = State()


# --------------------------------------------------------------------------- #
#  Handlers
# --------------------------------------------------------------------------- #

router = Router()


async def safe_edit(cb: CallbackQuery, text: str, reply_markup=None) -> None:
    """edit_text that swallows 'message is not modified' when the user taps the same button twice."""
    try:
        await cb.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        f"Welcome to <b>{SHOP_NAME}</b> 👋\nTap <b>🛍 Catalog</b> to browse.",
        reply_markup=main_menu(),
    )


@router.message(F.text == "🛍 Catalog")
async def show_categories(msg: Message) -> None:
    await msg.answer("<b>Categories</b>", reply_markup=categories_kb())


@router.callback_query(F.data.startswith("cat:"))
async def show_category(cb: CallbackQuery) -> None:
    category = cb.data.split(":", 1)[1]
    await safe_edit(cb, f"<b>{category.title()}</b>", reply_markup=products_kb(category))
    await cb.answer()


@router.callback_query(F.data.startswith("prod:"))
async def show_product(cb: CallbackQuery) -> None:
    pid = cb.data.split(":", 1)[1]
    p = BY_ID.get(pid)
    if not p:
        await cb.answer("Not available.", show_alert=True)
        return
    await safe_edit(
        cb,
        f"<b>{p.name}</b>\n{p.description}\n\n<b>{CURRENCY}{p.price:.2f}</b>",
        reply_markup=product_kb(pid),
    )
    await cb.answer()


@router.callback_query(F.data == "back:cats")
async def back_to_cats(cb: CallbackQuery) -> None:
    await safe_edit(cb, "<b>Categories</b>", reply_markup=categories_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("back:cat:"))
async def back_to_category(cb: CallbackQuery) -> None:
    category = cb.data.split(":", 2)[2]
    await safe_edit(cb, f"<b>{category.title()}</b>", reply_markup=products_kb(category))
    await cb.answer()


@router.callback_query(F.data.startswith("add:"))
async def add_to_cart(cb: CallbackQuery) -> None:
    pid = cb.data.split(":", 1)[1]
    if pid not in BY_ID:
        await cb.answer("Not available.", show_alert=True)
        return
    cart = CARTS.setdefault(cb.from_user.id, {})
    cart[pid] = cart.get(pid, 0) + 1
    await cb.answer(f"Added — {cart[pid]} in cart.")


@router.message(F.text == "🛒 Cart")
async def show_cart(msg: Message) -> None:
    lines, total = cart_total(msg.from_user.id)
    if not lines:
        await msg.answer("Cart is empty. Tap <b>🛍 Catalog</b> to browse.")
        return
    body = "\n".join(lines) + f"\n\n<b>Total: {CURRENCY}{total:.2f}</b>"
    await msg.answer(body, reply_markup=cart_kb())


@router.callback_query(F.data == "clear")
async def clear_cart(cb: CallbackQuery) -> None:
    CARTS.pop(cb.from_user.id, None)
    await cb.message.edit_text("Cart cleared.")
    await cb.answer()


@router.callback_query(F.data == "checkout")
async def start_checkout(cb: CallbackQuery, state: FSMContext) -> None:
    lines, total = cart_total(cb.from_user.id)
    if not lines:
        await cb.answer("Cart is empty.", show_alert=True)
        return
    await state.set_state(Checkout.name)
    await cb.message.answer("What's your full name?")
    await cb.answer()


@router.message(Checkout.name)
async def checkout_name(msg: Message, state: FSMContext) -> None:
    await state.update_data(name=msg.text.strip())
    await state.set_state(Checkout.phone)
    await msg.answer("Phone number?")


@router.message(Checkout.phone)
async def checkout_phone(msg: Message, state: FSMContext) -> None:
    await state.update_data(phone=msg.text.strip())
    await state.set_state(Checkout.address)
    await msg.answer("Delivery address?")


@router.message(Checkout.address)
async def checkout_address(msg: Message, state: FSMContext) -> None:
    await state.update_data(address=msg.text.strip())
    data = await state.get_data()
    lines, total = cart_total(msg.from_user.id)
    summary = (
        "<b>Confirm order</b>\n\n"
        + "\n".join(lines)
        + f"\n\n<b>Total: {CURRENCY}{total:.2f}</b>\n\n"
        + f"Name: {data['name']}\nPhone: {data['phone']}\nAddress: {data['address']}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm", callback_data="confirm")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")],
    ])
    await state.set_state(Checkout.confirm)
    await msg.answer(summary, reply_markup=kb)


@router.callback_query(Checkout.confirm, F.data == "confirm")
async def confirm_order(cb: CallbackQuery, state: FSMContext) -> None:
    order_id = f"ORD-{int(time.time()) % 100000:05d}"
    CARTS.pop(cb.from_user.id, None)
    await state.clear()
    await cb.message.edit_text(
        f"✅ Order <b>{order_id}</b> placed.\n"
        "The shop will contact you shortly.\n\n"
        "<i>Note: this LITE version does not notify an admin automatically.\n"
        "The full version sends every order straight to the shop owner's Telegram.</i>"
    )
    await cb.answer("Thanks!")


@router.callback_query(Checkout.confirm, F.data == "cancel")
async def cancel_order(cb: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await cb.message.edit_text("Order cancelled. Your cart is kept.")
    await cb.answer()


# --------------------------------------------------------------------------- #
#  Entrypoint
# --------------------------------------------------------------------------- #

async def main() -> None:
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    me = await bot.get_me()
    log.info(
        "Bot @%s online (LITE). Shop=%s products=%d categories=%d",
        me.username, SHOP_NAME, len(PRODUCTS), len(CATEGORIES),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Shutting down.")
