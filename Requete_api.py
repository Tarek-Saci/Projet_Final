import requests
import json

# URL de l'API
url = "https://api.windy.com/api/point-forecast/v2"

# Données de la requête
data = {
    "lat": 49.809,
    "lon": 16.787,
    "model": "GFS",
    "parameters": ["wind", "temperature"],
    "levels": ["200h"],
    "key": "gJuDVdIeZ2asmtlZb4xMH5atyimaJVUa"
}

# Envoi de la requête POST avec le corps de requête JSON
response = requests.post(url, json=data)

# Vérification du code de réponse
if response.status_code == 200:
    # Requête réussie
    result = response.json()
    # Traiter le résultat de la requête JSON
    print(result)
else:
    # La requête a échoué
    print("La requête a échoué avec le code de réponse :", response.status_code)
