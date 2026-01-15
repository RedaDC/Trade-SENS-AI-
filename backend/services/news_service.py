import requests
from backend.models import NewsEvent
from backend.extensions import db
from datetime import datetime

class NewsService:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key

    def fetch_daily_calendar(self, currencies: list, tenant_id: int):
        # Mock implementation of fetching from HorizonFX or JBlanked
        # url = f"{self.api_base_url}/calendar"
        # params = {'currencies': ','.join(currencies), 'token': self.api_key}
        # resp = requests.get(url, params=params)
        
        # Mock Data
        mock_events = [
            {
                'id': 'evt_1',
                'currency': 'USD',
                'name': 'Non-Farm Payrolls',
                'impact': 'HIGH',
                'actual': '200K',
                'forecast': '180K',
                'time': datetime.utcnow()
            }
        ]
        
        for evt in mock_events:
            event = NewsEvent(
                tenant_id=tenant_id,
                external_id=evt['id'],
                source='CALENDAR_API',
                currency=evt['currency'],
                event_name=evt['name'],
                impact=evt['impact'],
                actual=evt['actual'],
                forecast=evt['forecast'],
                event_time=evt['time']
            )
            db.session.add(event)
        
        db.session.commit()
