from flask import Flask
from routes import main_routes

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(main_routes)

    return app

# module-level `app` is the WSGI entrypoint used by gunicorn: `gunicorn src.app.main:app`
app = create_app()

if __name__ == "__main__":
    # dev runner (only for local dev)
    debug = app.config.get("ENV") != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug)