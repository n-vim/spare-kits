"""Telegram bot entrypoint."""

from __future__ import annotations

from telegram.ext import Application, CommandHandler

from {{ package_name }}.handlers import start
from {{ package_name }}.settings import Settings


def build_application(settings: Settings) -> Application:
    """Build the Telegram application."""

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    return application


def main() -> None:
    """Run the bot."""

    build_application(Settings()).run_polling()


if __name__ == "__main__":
    main()
