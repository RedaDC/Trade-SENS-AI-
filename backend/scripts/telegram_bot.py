# pip install python-telegram-bot schedule pandas

import pandas as pd
import schedule
import time
from telegram import Bot
from datetime import datetime
import os
import asyncio

# --- OBJECTIF ---
# Envoyer un rapport structuré des signaux de trading à 18h00 après clôture.

TOKEN = "TON_TOKEN_ICI" # Remplacer par le vrai token
CHAT_ID = "TON_CHAT_ID_ICI" # Remplacer par le vrai ID

async def send_telegram_msg(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

def generate_report():
    print(f"[{datetime.now()}] Génération du rapport Telegram...")
    
    if not os.path.exists("signals_today.csv"):
        return "❌ Erreur : Données du jour indisponibles (signals_today.csv non trouvé)."
    
    df = pd.read_csv("signals_today.csv")
    date_now = datetime.now().strftime("%d/%m/%Y")
    aum_total = df['aum'].sum() / 1000 # En Milliards
    
    msg = f"📊 *Rapport OPCVM Maroc* — {date_now}\n"
    msg += f"AUM Total : {aum_total:.2f} Md MAD\n\n"
    
    # ACHETER
    buys = df[df['signal'] == 'ACHETER']
    msg += f"✅ *ACHETER* ({len(buys)} fonds)\n"
    for _, row in buys.iterrows():
        sentiment_icon = "😊" if row['score_sentiment_moyen_jour'] > 0 else "😐"
        msg += f"• {row['nom_fonds']} | VL: {row['vl_jour']:.2f} | {sentiment_icon}\n"
    
    # ATTENDRE
    waits = df[df['signal'] == 'ATTENDRE']
    msg += f"\n⏳ *ATTENDRE* ({len(waits)} fonds)\n"
    for _, row in waits.iterrows():
        msg += f"• {row['nom_fonds']} | VL Stable | 😐\n"
        
    # VENDRE
    sells = df[df['signal'] == 'VENDRE']
    msg += f"\n🔴 *VENDRE* ({len(sells)} fonds)\n"
    for _, row in sells.iterrows():
        msg += f"• {row['nom_fonds']} | VL: {row['vl_jour']:.2f} | 😟\n"
        
    # Top Actus (Mock based on Module 2 results)
    msg += "\n📰 *Top actualités du jour :*\n"
    msg += "1. BAM maintient son taux — Score: +0.82\n"
    msg += "2. BVC: Séance calme — Score: -0.10\n"
    
    return msg

async def daily_job():
    message = generate_report()
    await send_telegram_msg(message)
    
    # Journalisation
    log_file = "telegram_log.csv"
    log_data = pd.DataFrame([{
        "date": datetime.now().isoformat(),
        "status": "Success" if "Erreur" not in message else "Failed"
    }])
    log_data.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)

def run_scheduler():
    # Planification à 18h00
    schedule.every().day.at("18:00").do(lambda: asyncio.run(daily_job()))
    
    print("Bot Telegram en veille. Envoi prévu chaque jour à 18h00.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Pour test immédiat:
    # asyncio.run(daily_job())
    run_scheduler()

# --- EXPLICATION ---
# Ce bot sert de tableau de bord mobile. 
# Il synthétise les données complexes (AUM, Flux, Sentiment, LSTM) en recommandations actionnables.
# La journalisation permet de suivre la fiabilité de l'envoi dans le temps.

# --- PROCHAINE ÉTAPE ---
# Configurer les clés API (Telegram, OpenAI/HF) dans un fichier .env sécurisé.
