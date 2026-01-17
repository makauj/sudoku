from flask import Flask
from .routes import bp as routes_bp
import os

def create_app():
    print("TEMPLATE FOLDER:", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/templates')))
    app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/templates')))
    app.register_blueprint(routes_bp)
    return app

# module-level `app` is the WSGI entrypoint used by gunicorn: `gunicorn src.app.main:app`
app = create_app()



if __name__ == "__main__":
    # dev runner (only for local dev)
    debug = app.config.get("ENV") != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug)
