from flask import Flask
from flask_cors import CORS
from .config.config import DevelopmentConfig
from .extensions import db
from .models import *

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    CORS(app)
    
    # Register Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.challenge_routes import challenge_bp
    from .routes.trade_routes import trade_bp
    from .routes.market_routes import market_bp
    from .routes.news_routes import news_bp
    from .routes.leaderboard_routes import leaderboard_bp
    from .routes.admin_routes import admin_bp
    from .routes.analysis_routes import market_bp_analysis
    from .routes.ai_analysis_routes import ai_analysis_bp
    from .routes.ai_routes import ai_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/<tenant>/auth')
    app.register_blueprint(challenge_bp, url_prefix='/api/v1/<tenant>/challenges')
    app.register_blueprint(trade_bp, url_prefix='/api/v1/<tenant>/trades')
    app.register_blueprint(market_bp, url_prefix='/api/v1/<tenant>/market-data')
    app.register_blueprint(news_bp, url_prefix='/api/v1/<tenant>/news')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/v1/<tenant>/leaderboard')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/<tenant>/admin')
    app.register_blueprint(market_bp_analysis, url_prefix='/api/v1/<tenant>/analysis')
    app.register_blueprint(ai_analysis_bp, url_prefix='/api/v1/<tenant>/ai-analysis')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/<tenant>/ai')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
