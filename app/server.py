from flask import current_app
from main import server
from controllers.data import bp

with server.app_context():
    current_app.register_blueprint(bp)

if __name__ == "__main__":
    server.run(host="0.0.0.0")
