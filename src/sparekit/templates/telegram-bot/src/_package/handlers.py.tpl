"""Telegram command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start."""

    if update.message is not None:
        await update.message.reply_text("Hello from {{ project_name }}!")
