from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """
    App factory. Loads env, configures app and registers blueprints.
    Gunicorn/uvicorn can import `app` from src.app.main.
    """
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret"),
        ENV=os.getenv("FLASK_ENV", "production"),
        RATELIMIT_DEFAULT=os.getenv("RATELIMIT_DEFAULT", "100/hour"),
    )

    # secure cookie defaults (can be overridden by env)
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SECURE", os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true")
    app.config.setdefault("SESSION_COOKIE_SAMESITE", os.getenv("SESSION_COOKIE_SAMESITE", "Lax"))

    # register routes blueprint if present
    try:
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
    except Exception:
        pass

    # WhiteNoise for simple static serving in Gunicorn
    try:
        from whitenoise import WhiteNoise
        static_root = os.path.join(app.root_path, "static")
        app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_root, prefix="static/")
    except Exception:
        pass

    return app