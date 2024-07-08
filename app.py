# flask_app.py
from flask import Flask, jsonify, render_template, request
import pandas as pd
import pickle
import logging

app = Flask(__name__)

# Importer le dataframe
df = pd.read_csv('data.csv')

# Importer le modèle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtenir l'identifiant du client à analyser
        client_id = int(request.form['client_id'])

        # Vérifier si l'identifiant du client est présent dans le dataframe
        if client_id in df['SK_ID_CURR'].values:
            # Sélectionner les données client
            features_client = df.loc[df['SK_ID_CURR'] == client_id]
            # Suppression des colonnes SK_ID_CURR et TARGET
            features_client = features_client.drop(columns=['SK_ID_CURR', 'TARGET'])

            # Faire la prédiction
            prob = model.predict_proba(features_client)[:, 1]
            pred = (prob >= 0.52).astype(int)

            response = {
                'proba': prob.tolist(),
                'prediction': pred.tolist()
            }
        else:
            response = {'erreur': 'Identifiant du client incorrect'}

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=8000)