from extensions import db
from datetime import datetime

class Tenant(db.Model):
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subdomain = db.Column(db.String(50), unique=True, nullable=False)
    plan = db.Column(db.String(50), default='FREE') # e.g., BASIC, PRO
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    settings = db.relationship('TenantSettings', backref='tenant', uselist=False, cascade="all, delete-orphan")
    users = db.relationship('User', backref='tenant', lazy=True)
    challenges = db.relationship('UserChallenge', backref='tenant', lazy=True)
    trades = db.relationship('Trade', backref='tenant', lazy=True)

class TenantSettings(db.Model):
    __tablename__ = 'tenant_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    
    # Branding & Localization
    default_language = db.Column(db.String(10), default='en')
    base_currency = db.Column(db.String(10), default='USD')
    
    # Provider Configs
    market_data_provider = db.Column(db.String(50), default='YFINANCE') # YFINANCE, PREMIUM_US, DEFEATBETA
    data_quality_level = db.Column(db.String(50), default='DELAYED') # DELAYED, REALTIME, INSTITUTIONAL
    ai_service_level = db.Column(db.String(50), default='BASIC') # BASIC, ADVANCED, PREMIUM
    news_api_base_url = db.Column(db.String(200))
    news_api_key = db.Column(db.String(200))
    
    # Payment Configs
    paypal_client_id = db.Column(db.String(200))
    paypal_secret = db.Column(db.String(200))
    
    # Pricing
    price_starter = db.Column(db.Float, default=49.0)
    price_pro = db.Column(db.Float, default=199.0)
    price_elite = db.Column(db.Float, default=349.0)
