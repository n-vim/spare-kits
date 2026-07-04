"""HTTP routes."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)


@api.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@api.get("/api/v1/hello")
def hello() -> tuple[dict[str, str], int]:
    name = request.args.get("name", "world")
    return {"message": f"Hello, {name}!"}, 200
