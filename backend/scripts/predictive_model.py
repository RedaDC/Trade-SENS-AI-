# pip install pandas numpy scikit-learn tensorflow matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os
from datetime import datetime

# --- OBJECTIF ---
# Construire un modèle LSTM pour prédire la VL de demain et générer des signaux d'achat/vente.

def prepare_data(df):
    """
    Prépare les séquences temporelles pour le LSTM.
    """
    # Features demandées
    features = ['vl_jour', 'variation_pct', 'aum', 'flux_net', 'score_sentiment_moyen_jour', 'taux_coupon', 'nb_actus_jour']
    
    # Pour la démonstration, on génère un historique fictif si le CSV est trop court
    if len(df) < 60:
        print("Données insuffisantes pour LSTM. Génération d'un historique simulé...")
        base_data = df.iloc[0]
        rows = []
        for i in range(100):
            row = base_data.copy()
            row['vl_jour'] = row['vl_jour'] * (1 + np.random.normal(0, 0.01))
            row['variation_pct'] = np.random.normal(0, 0.5)
            rows.append(row)
        df_history = pd.DataFrame(rows)
    else:
        df_history = df

    data = df_history[features].values
    
    # Cible : VL J+1
    target = df_history['vl_jour'].shift(-1).fillna(method='ffill').values
    
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    
    X_scaled = scaler_x.fit_transform(data)
    y_scaled = scaler_y.fit_transform(target.reshape(-1, 1))
    
    X_seq, y_seq = [], []
    win = 30 # Fenêtre glissante de 30 jours
    
    for i in range(win, len(X_scaled)):
        X_seq.append(X_scaled[i-win:i])
        y_seq.append(y_scaled[i])
        
    return np.array(X_seq), np.array(y_seq), scaler_x, scaler_y, features

def build_model(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mae')
    return model

def main():
    if not os.path.exists("opcvm_enriched.csv"):
        print("Erreur : opcvm_enriched.csv introuvable.")
        return

    df = pd.read_csv("opcvm_enriched.csv")
    X, y, scaler_x, scaler_y, feature_names = prepare_data(df)
    
    # Split chronologique (80/20)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    print(f"[{datetime.now()}] Entraînement du modèle LSTM...")
    model = build_model((X.shape[1], X.shape[2]))
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=16, verbose=0)
    
    # Prédiction et Signal
    latest_seq = X[-1].reshape(1, 30, len(feature_names))
    pred_scaled = model.predict(latest_seq)
    vl_predite = scaler_y.inverse_transform(pred_scaled)[0][0]
    vl_actuelle = df.iloc[-1]['vl_jour']
    
    perf_attendue = (vl_predite - vl_actuelle) / vl_actuelle
    
    if perf_attendue > 0.005: signal = "ACHETER"
    elif perf_attendue < -0.005: signal = "VENDRE"
    else: signal = "ATTENDRE"
    
    print(f"RESULTAT: VL Actuelle: {vl_actuelle:.2f} | Prédite: {vl_predite:.2f} | Signal: {signal}")
    
    # Sauvegarde
    model.save("model_opcvm.h5")
    
    # Export des signaux pour le bot Telegram
    df_signals = df.copy()
    df_signals['vl_predite'] = vl_predite # Simplifié pour la démo
    df_signals['signal'] = signal
    df_signals.to_csv("signals_today.csv", index=False)
    
    # Graphique (Optionnel)
    plt.figure(figsize=(12, 6))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Performance du modèle LSTM')
    plt.legend()
    plt.savefig('performance_model.png')
    print("Graphique sauvegardé sous performance_model.png")

if __name__ == "__main__":
    main()

# --- EXPLICATION ---
# Le LSTM capte les dépendances temporelles complexes. 
# En intégrant le sentiment, il peut anticiper des baisses de VL liées à des paniques de marché (rachats massifs).
# Le seuil de 0.5% évite les signaux parasites liés au bruit de marché.

# --- PROCHAINE ÉTAPE ---
# Déployer le bot Telegram (Module 4) pour diffuser ces signaux.
