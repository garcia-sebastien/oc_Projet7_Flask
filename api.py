# flask_app.py
from flask import Flask, jsonify, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Importer le dataframe
df = pd.read_csv('data.csv')

# Importer le modèle
with open('C:/Users/User/final_model/model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Obtenir l'identifiant du client à partir du formulaire
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
            'probabilité': prob.tolist(),
            'prediction': pred.tolist()
        }
    
    else:
        # Afficher un message d'erreur si l'identifiant du client n'est pas trouvé
        response = {
            'erreur': 'Identifiant du client incorrect'
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)