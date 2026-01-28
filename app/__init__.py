from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    # Explicitly set paths for Vercel production stability
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    app.config.from_object(config_class)

    from app.routes import main
    app.register_blueprint(main)

    return app
