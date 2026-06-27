from {{ package_name }}.settings import Settings


def test_settings_accepts_token() -> None:
    settings = Settings(telegram_bot_token="token")
    assert settings.telegram_bot_token == "token"
