from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.extensions import db
from app.routes.destination_routes import destination_bp

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_board.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Swagger basic confiuration
    app.config["SWAGGER"] = {
        "title": "Travel Board API",
        "uiversion": 3
    }
    
    # CORS configuration
    app.config["CORS_HEADERS"] = "Content-Type"

    
    db.init_app(app)
    Swagger(app)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    
    # Realizar o registro das rotas com blueprint
    # O Conceito dos Blueprints
    #       The basic concept of blueprints is that they record operations to execute when registered on an application. 
    #       Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another.
    app.register_blueprint(destination_bp)
    
    return app