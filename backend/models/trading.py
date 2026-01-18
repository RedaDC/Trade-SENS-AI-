from extensions import db
from datetime import datetime

class UserChallenge(db.Model):
    __tablename__ = 'user_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    challenge_type = db.Column(db.String(50), nullable=False) # STARTER, PRO, ELITE
    initial_balance = db.Column(db.Float, nullable=False)
    current_equity = db.Column(db.Float, nullable=False)
    
    # Rules
    daily_max_loss = db.Column(db.Float, nullable=False) # e.g. 5000.0 (absolute value or calculated from %)
    max_drawdown = db.Column(db.Float, nullable=False)
    profit_target = db.Column(db.Float, nullable=False)
    
    status = db.Column(db.String(20), default='ACTIVE') # ACTIVE, FAILED, PASSED
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    trades = db.relationship('Trade', backref='challenge', lazy=True)

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('user_challenges.id'), nullable=False)
    
    symbol = db.Column(db.String(20), nullable=False)
    side = db.Column(db.String(10), nullable=False) # BUY, SELL
    volume = db.Column(db.Float, nullable=False)
    
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    pnl = db.Column(db.Float, nullable=True)
    
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)

    stop_loss = db.Column(db.Float, nullable=True)
    take_profit = db.Column(db.Float, nullable=True)

class PriceData(db.Model):
    __tablename__ = 'price_data'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True) # Nullable if shared data? Spec says tenant_id present.
    symbol = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Float)
    
    source = db.Column(db.String(50)) # YFINANCE, CASABLANCA, etc.

class NewsEvent(db.Model):
    __tablename__ = 'news_events'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    external_id = db.Column(db.String(100))
    source = db.Column(db.String(50))
    
    currency = db.Column(db.String(10))
    event_name = db.Column(db.String(200))
    category = db.Column(db.String(100))
    
    event_time = db.Column(db.DateTime)
    impact = db.Column(db.String(20)) # HIGH, MEDIUM, LOW
    
    actual = db.Column(db.String(50))
    forecast = db.Column(db.String(50))
    previous = db.Column(db.String(50))

class LeaderboardSnapshot(db.Model):
    __tablename__ = 'leaderboard_snapshots'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    
    period = db.Column(db.String(20)) # YYYY-MM
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    profit_percent = db.Column(db.Float)
    rank = db.Column(db.Integer)
