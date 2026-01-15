from backend.app import create_app
from backend.extensions import db
from backend.models import Tenant, TenantSettings

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Create Default Tenant
        if not Tenant.query.filter_by(subdomain='tradesense').first():
            tenant = Tenant(name='TradeSense', subdomain='tradesense', plan='ENTERPRISE')
            db.session.add(tenant)
            db.session.commit()
            
            settings = TenantSettings(
                tenant_id=tenant.id,
                market_data_provider='YFINANCE',
                price_starter=99.0,
                price_pro=199.0,
                price_elite=299.0 
            )
            db.session.add(settings)
            db.session.commit()
            print("Initialized TradeSense tenant.")
        else:
            print("Tenant already exists.")

if __name__ == '__main__':
    init_db()
