"""Flask application factory."""

from __future__ import annotations

from flask import Flask

from {{ package_name }}.config import Settings
from {{ package_name }}.routes import api


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings()
    app = Flask(__name__)
    app.config["APP_NAME"] = settings.app_name
    app.config["ENVIRONMENT"] = settings.environment
    app.register_blueprint(api)
    return app
