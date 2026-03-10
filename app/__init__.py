from flask import Flask
from app.db.connection import init_app
from app.routes.destination_routes import destination_bp

def create_app():
    app = Flask(__name__)
    
    init_app(app)
    
    # Realizar o registro das rotas com blueprint
    # O Conceito dos Blueprints
    #       The basic concept of blueprints is that they record operations to execute when registered on an application. 
    #       Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another.
    app.register_blueprint(destination_bp)
    
    return app