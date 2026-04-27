# pip install pandas requests beautifulsoup4 langdetect transformers torch

import pandas as pd
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from transformers import pipeline
import time
from datetime import datetime
import os

# --- OBJECTIF ---
# Collecter l'actualité marocaine (Médias24, L'Économiste, MAP) et calculer un score de sentiment IA.

def collect_news():
    """
    Simule la collecte RSS/NewsAPI pour le marché marocain.
    """
    print(f"[{datetime.now()}] Collecte des actualités (Mots-clés: OPCVM, BAM, Taux)...")
    
    # Mock des actualités réelles
    news = [
        {"title": "Bank Al-Maghrib maintient son taux directeur, la stabilité rassure les marchés.", "source": "Médias24", "classif": "Monétaire"},
        {"title": "Baisse surprise de la collecte nette sur les fonds obligataires ce mois-ci.", "source": "L'Économiste", "classif": "Obligataire"},
        {"title": "Le MASI termine en zone verte grâce au secteur bancaire.", "source": "MAP", "classif": "Actions"},
        {"title": "Les investisseurs s'attendent à un pivot de la politique monétaire en 2025.", "source": "Finance News", "classif": "Diversifié"}
    ]
    return news

def get_sentiment_pipeline(lang):
    if lang == 'ar':
        return pipeline("sentiment-analysis", model="CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment")
    else:
        # Multilingual BERT for French
        return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def process_sentiment():
    news_items = collect_news()
    results = []
    
    # Cache pour les pipelines (évite de recharger le modèle à chaque itération)
    pipelines = {}
    
    for item in news_items:
        try:
            text = item['title']
            lang = detect(text)
            
            if lang not in pipelines:
                pipelines[lang] = get_sentiment_pipeline(lang)
            
            pipe = pipelines[lang]
            sentiment_res = pipe(text)[0]
            
            # Normalisation du score entre -1 et +1
            # nlptown renvoie des étoiles (1-5) -> (star - 3) / 2
            if lang != 'ar':
                star = int(sentiment_res['label'].split()[0])
                score = (star - 3) / 2
            else:
                # CamelBERT renvoie 'positive', 'neutral', 'negative'
                mapping = {'positive': 0.8, 'neutral': 0.0, 'negative': -0.8}
                score = mapping.get(sentiment_res['label'], 0.0)
            
            results.append({
                'classification': item['classif'],
                'sentiment_score': score,
                'title': text,
                'source': item['source']
            })
            
            time.sleep(2) # Respect du délai BAM/MAP
            
        except Exception as e:
            print(f"Erreur sentiment pour '{text[:20]}...': {e}")

    df_sentiment = pd.DataFrame(results)
    
    # Agrégation par classification
    df_agg = df_sentiment.groupby('classification')['sentiment_score'].agg(['mean', 'count']).reset_index()
    df_agg.columns = ['classification', 'score_sentiment_moyen_jour', 'nb_actus_jour']
    
    return df_agg

def main():
    df_sent = process_sentiment()
    
    if os.path.exists("opcvm_data.csv"):
        df_data = pd.read_csv("opcvm_data.csv")
        # Fusion sur la colonne classification
        df_final = pd.merge(df_data, df_sent, on='classification', how='left').fillna(0)
        df_final.to_csv("opcvm_enriched.csv", index=False)
        print(f"[{datetime.now()}] opcvm_enriched.csv généré avec succès.")
    else:
        print("Erreur : opcvm_data.csv introuvable. Lancez asfim_ingestion.py d'abord.")

if __name__ == "__main__":
    main()

# --- EXPLICATION ---
# Ce pipeline utilise BERT pour comprendre le ton émotionnel des news financières.
# Il gère nativement le français et l'arabe.
# Le score agrégé permet de quantifier le "poids" de l'opinion sur chaque classe d'actif.

# --- PROCHAINE ÉTAPE ---
# Entraîner le modèle LSTM (Module 3) sur ces données enrichies.
