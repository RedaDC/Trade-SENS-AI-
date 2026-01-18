from app import create_app
from extensions import db
from models import Tenant, TenantSettings

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
                data_quality_level='INSTITUTIONAL', 
                ai_service_level='PREMIUM',
                price_starter=49.0,
                price_pro=199.0,
                price_elite=349.0 
            )
            db.session.add(settings)
            db.session.commit()
            print("Initialized TradeSense tenant.")
        else:
            tenant = Tenant.query.filter_by(subdomain='tradesense').first()
            if tenant and tenant.settings:
                tenant.settings.price_starter = 49.0
                tenant.settings.price_pro = 199.0
                tenant.settings.price_elite = 349.0
                tenant.settings.data_quality_level = 'INSTITUTIONAL'
                tenant.settings.ai_service_level = 'PREMIUM'
                db.session.commit()
                print("Updated existing TradeSense tenant prices.")
            else:
                print("Tenant exists but settings missing.")

if __name__ == '__main__':
    init_db()
