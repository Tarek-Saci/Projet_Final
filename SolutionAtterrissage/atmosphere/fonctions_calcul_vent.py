from shapely.geometry import LineString
import numpy as np
"""import pandas as pd
import datetime
from vent import get_windy_data
from transforme_data import flatten_json
from altitude_pression import calcul_altitude_pression

# Fonction permettant de déterminer le vecteur vitesse du vent à une position et une altitude donnée
# L'altitude doit être entrée en mètres
# La position géographique doit être repérée par des coordonnées GPS (latitude, longitude).
# La latitude doit être un flottant compris entre -89.99° et 90° tandis que la longitude peut être un flottant quelconque

def calcul_vent(lat, lon, altitude):

    # Récupération des données dans la base de données de Windy
    meteo = get_windy_data(lat, lon)

    # Détermination de l'heure de la requête
    # En format POSIX
    posix_time = datetime.datetime.now().timestamp()
    #print(posix_time)
    # En format classique
    classical_time = datetime.datetime.fromtimestamp(posix_time)
    #print(classical_time)

    # Transformation du JSON en dataframe
    # flatten the JSON
    flattened = flatten_json(meteo)
    df = pd.DataFrame([flattened])

    # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
    data_hours = df.filter(like="data_hours")

    i = 0
    #print(data_hours.iloc[0, i] / 1000)
    while posix_time > data_hours.iloc[0, i] / 1000:
        i += 1
    #print(i)
    if abs(posix_time - data_hours.iloc[0,i]) > abs(posix_time - data_hours.iloc[0, i-1]):
        i-=1

    # Liste des altitudes pour lesquelles les données sont recensées
    liste_altitude_pression = [150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000, 1013.25]

    # Calcul de l'altitude pression de l'avion
    altitude_pression_avion = calcul_altitude_pression(altitude)

    # Détermination de l'altitude recensée la plus proche de l'altitude de l'avion
    j = 0
    while altitude_pression_avion > liste_altitude_pression[j]:
        j += 1
    #print(j)
    if abs(altitude_pression_avion - liste_altitude_pression[j]) > abs(
            altitude_pression_avion - liste_altitude_pression[j - 1]):
        altitude_database = liste_altitude_pression[j - 1]
    else:
        altitude_database = liste_altitude_pression[j]
    # print(altitude_database)

    # Récupération des données recherchées dans la database
    if altitude_database != 1013.25:
        vecteur_vent_v = df[f'data_wind_v-{altitude_database}h_{i}']
        vecteur_vent_u = df[f'data_wind_u-{altitude_database}h_{i}']
    else:
        vecteur_vent_v = df[f'data_wind_v-surface_{i}']
        vecteur_vent_u = df[f'data_wind_u-surface_{i}']
    vecteur_vent=[vecteur_vent_u.iloc[0],vecteur_vent_v.iloc[0]]

    return vecteur_vent


print('Vecteur vent : ', calcul_vent(-23,204,8000))"""

def calcul_coordonnees_vents_trajet(n,coordonnees_avion,latitude_point,longitude_point):

    point1 = (coordonnees_avion[1], coordonnees_avion[0])
    point2 = (longitude_point, latitude_point)

    line = LineString([point1, point2])

    points_interieurs = [line.interpolate(i / (n + 1), normalized=True) for i in range(1, n + 1)]

    coordonnees_points_interieurs = [(point.y, point.x) for point in points_interieurs]

    return coordonnees_points_interieurs

def calcul_moyenne_vents_trajet(vents_a_moyenner):

    moyenne_vent_x = np.mean(vents_a_moyenner[:,0])
    moyenne_vent_y = np.mean(vents_a_moyenner[:,1])

    return (moyenne_vent_x,moyenne_vent_y)


