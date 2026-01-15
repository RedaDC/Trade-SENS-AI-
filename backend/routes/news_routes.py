from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta

news_bp = Blueprint('news', __name__)

# Realistic news templates by source
NEWS_TEMPLATES = {
    'Reuters': [
        {"headline": "Oil prices surge {percent}% on OPEC+ supply cut announcement", "category": "Commodities", "impact": "HIGH"},
        {"headline": "Federal Reserve signals potential rate pause amid inflation concerns", "category": "Markets", "impact": "HIGH"},
        {"headline": "Tech stocks rally as earnings beat expectations", "category": "Stocks", "impact": "MEDIUM"},
        {"headline": "Dollar strengthens against major currencies on strong jobs data", "category": "Forex", "impact": "MEDIUM"},
        {"headline": "Gold hits {price}-month high as safe-haven demand rises", "category": "Commodities", "impact": "MEDIUM"},
    ],
    'Bloomberg': [
        {"headline": "S&P 500 reaches new record high on tech sector strength", "category": "Markets", "impact": "HIGH"},
        {"headline": "European Central Bank maintains rates, cites economic uncertainty", "category": "Markets", "impact": "HIGH"},
        {"headline": "Emerging markets see capital inflows amid dollar weakness", "category": "Forex", "impact": "MEDIUM"},
        {"headline": "Cryptocurrency market cap surpasses ${trillion} trillion milestone", "category": "Markets", "impact": "LOW"},
        {"headline": "Treasury yields fall as investors seek safety", "category": "Markets", "impact": "MEDIUM"},
    ],
    'TheStreet': [
        {"headline": "Top analyst upgrades {stock} stock to 'Strong Buy'", "category": "Stocks", "impact": "LOW"},
        {"headline": "5 dividend stocks to watch this quarter", "category": "Stocks", "impact": "LOW"},
        {"headline": "Market volatility creates buying opportunity, strategists say", "category": "Markets", "impact": "MEDIUM"},
        {"headline": "Retail investors flock to {sector} sector amid recovery hopes", "category": "Stocks", "impact": "LOW"},
        {"headline": "Earnings season preview: What to expect from major banks", "category": "Stocks", "impact": "MEDIUM"},
    ],
    'Forex Factory': [
        {"headline": "EUR/USD breaks key resistance at {level}, targets {target}", "category": "Forex", "impact": "HIGH"},
        {"headline": "GBP/USD consolidates ahead of Bank of England decision", "category": "Forex", "impact": "MEDIUM"},
        {"headline": "USD/JPY retreats from highs on intervention concerns", "category": "Forex", "impact": "MEDIUM"},
        {"headline": "Australian dollar surges on strong employment data", "category": "Forex", "impact": "MEDIUM"},
        {"headline": "Swiss franc gains as geopolitical tensions escalate", "category": "Forex", "impact": "LOW"},
    ],
    'ADVFN': [
        {"headline": "{stock} shares jump {percent}% on merger speculation", "category": "Stocks", "impact": "MEDIUM"},
        {"headline": "Insider buying activity surges in {sector} sector", "category": "Stocks", "impact": "LOW"},
        {"headline": "Short interest declines in major tech stocks", "category": "Stocks", "impact": "LOW"},
        {"headline": "Options activity suggests bullish sentiment for {stock}", "category": "Stocks", "impact": "LOW"},
        {"headline": "Institutional investors increase positions in {sector} ETFs", "category": "Stocks", "impact": "MEDIUM"},
    ]
}

def generate_realistic_news(count=20):
    """Generate realistic financial news articles"""
    news_items = []
    sources = list(NEWS_TEMPLATES.keys())
    
    for i in range(count):
        source = random.choice(sources)
        template = random.choice(NEWS_TEMPLATES[source])
        
        # Fill in placeholders
        headline = template['headline']
        headline = headline.replace('{percent}', str(random.randint(2, 8)))
        headline = headline.replace('{price}', str(random.randint(3, 12)))
        headline = headline.replace('{trillion}', str(round(random.uniform(1.5, 3.5), 1)))
        headline = headline.replace('{level}', f"1.{random.randint(1000, 2000)}")
        headline = headline.replace('{target}', f"1.{random.randint(2000, 3000)}")
        headline = headline.replace('{stock}', random.choice(['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']))
        headline = headline.replace('{sector}', random.choice(['technology', 'healthcare', 'energy', 'financial']))
        
        # Generate timestamp (last 24 hours)
        hours_ago = random.randint(0, 24)
        timestamp = datetime.now() - timedelta(hours=hours_ago)
        
        # Generate summary
        summaries = [
            "Market analysts are closely monitoring the situation as volatility increases.",
            "Traders are positioning for potential breakout as key levels are tested.",
            "This development could have significant implications for global markets.",
            "Investors are advised to watch for further updates throughout the trading session.",
            "The move comes amid broader market uncertainty and shifting sentiment.",
        ]
        
        news_items.append({
            'id': i + 1,
            'source': source,
            'headline': headline,
            'summary': random.choice(summaries),
            'category': template['category'],
            'impact': template['impact'],
            'timestamp': timestamp.isoformat(),
            'time_ago': f"{hours_ago}h ago" if hours_ago > 0 else "Just now"
        })
    
    # Sort by timestamp (newest first)
    news_items.sort(key=lambda x: x['timestamp'], reverse=True)
    return news_items

@news_bp.route('/', methods=['GET'])
def get_news(tenant):
    """Get financial news with optional filtering"""
    source_filter = request.args.get('source')
    category_filter = request.args.get('category')
    
    news_items = generate_realistic_news(count=30)
    
    # Apply filters
    if source_filter:
        news_items = [n for n in news_items if n['source'] == source_filter]
    
    if category_filter:
        news_items = [n for n in news_items if n['category'] == category_filter]
    
    return jsonify(news_items)

@news_bp.route('/sources', methods=['GET'])
def get_sources(tenant):
    """Get available news sources"""
    return jsonify(list(NEWS_TEMPLATES.keys()))

@news_bp.route('/categories', methods=['GET'])
def get_categories(tenant):
    """Get available news categories"""
    return jsonify(['Markets', 'Forex', 'Stocks', 'Commodities'])
