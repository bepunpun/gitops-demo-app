import os

from flask import Flask, jsonify, render_template_string

COLORS = {"production": "#1f8a4c", "staging": "#c9740a"}
DEFAULT_COLOR = "#2f5fb3"

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GitOps demo</title>
  <style>
    body { margin: 0; min-height: 100vh; display: grid; place-items: center;
           font-family: system-ui, sans-serif; background: {{ color }}; color: #fff; }
    main { text-align: center; padding: 2rem; }
    h1 { font-size: 2.4rem; margin: 0 0 .5rem; }
    code { background: rgba(0,0,0,.25); padding: .2rem .5rem; border-radius: 4px; }
  </style>
</head>
<body>
  <main>
    <h1>{{ message }}</h1>
    <p>environment <code>{{ environment }}</code> &middot; commit <code>{{ commit }}</code></p>
  </main>
</body>
</html>
"""


def build_info():
    return {
        "environment": os.getenv("APP_ENV", "local"),
        "commit": os.getenv("GIT_SHA", "unknown"),
        "message": os.getenv("APP_MESSAGE", "Hello from the GitOps demo"),
    }


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
        info = build_info()
        color = COLORS.get(info["environment"], DEFAULT_COLOR)
        return render_template_string(PAGE, color=color, **info)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/version")
    def version():
        return jsonify(build_info())

    return app


app = create_app()
