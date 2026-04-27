from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='TRADER') # TRADER, ADMIN, SUPERADMIN
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    challenges = db.relationship('UserChallenge', backref='user', lazy=True)
    
    __table_args__ = (db.UniqueConstraint('tenant_id', 'email', name='_tenant_user_uc'),)
