from .vent_windy import get_windy_data
from .transforme_data import flatten_json
import math
import datetime
import pandas as pd

class Air:
    def __init__(self,latitude,longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    # L'argument doit être entré en mètres
    def calcul_altitude_pression(self):
        # d'après l'ISA
        if self.altitude < 11000:
            pression = 1013.25 * (1 - 0.0065 * self.altitude / 288.15) ** (9.81 / (0.0065 * 287.04))
        else:
            pression = 226.32 * math.exp(-9.81 * (self.altitude - 11000) / (287.04 * 216.65))
        return pression

    # Fonction permettant de déterminer le vecteur vitesse du vent à une position et une altitude donnée
    # L'altitude doit être entrée en mètres
    # La position géographique doit être repérée par des coordonnées GPS (latitude, longitude).
    # La latitude doit être un flottant compris entre -89.99° et 90° tandis que la longitude peut être un flottant quelconque

    def calcul_vent(self):

        # Récupération des données dans la base de données de Windy
        meteo = get_windy_data(self.latitude, self.longitude)

        # Détermination de l'heure de la requête
        # En format POSIX
        posix_time = datetime.datetime.now().timestamp()
        # print(posix_time)
        # En format classique
        classical_time = datetime.datetime.fromtimestamp(posix_time)
        # print(classical_time)

        # Transformation du JSON en dataframe
        # flatten the JSON
        flattened = flatten_json(meteo)
        df = pd.DataFrame([flattened])

        # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
        data_hours = df.filter(like="data_hours")

        i = 0
        # print(data_hours.iloc[0, i] / 1000)
        while posix_time > data_hours.iloc[0, i] / 1000:
            i += 1
        # print(i)
        if abs(posix_time - data_hours.iloc[0, i]) > abs(posix_time - data_hours.iloc[0, i - 1]):
            i -= 1

        # Liste des altitudes pour lesquelles les données sont recensées
        liste_altitude_pression = [150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000, 1013.25]

        # Calcul de l'altitude pression de l'avion
        altitude_pression_avion = self.calcul_altitude_pression()

        # Détermination de l'altitude recensée la plus proche de l'altitude de l'avion
        j = 0
        while altitude_pression_avion > liste_altitude_pression[j]:
            j += 1
        # print(j)
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
        vecteur_vent = [vecteur_vent_u.iloc[0], vecteur_vent_v.iloc[0]]

        return vecteur_vent

    def calcul_temperature(self):

        # Récupération des données dans la base de données de Windy
        meteo = get_windy_data(self.latitude, self.longitude)

        # Détermination de l'heure de la requête
        # En format POSIX
        posix_time = datetime.datetime.now().timestamp()
        # print(posix_time)
        # En format classique
        classical_time = datetime.datetime.fromtimestamp(posix_time)
        # print(classical_time)

        # Transformation du JSON en dataframe
        # flatten the JSON
        flattened = flatten_json(meteo)
        df = pd.DataFrame([flattened])
        #print(df)

        # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
        data_hours = df.filter(like="data_hours")

        i = 0
        # print(data_hours.iloc[0, i] / 1000)
        while posix_time > data_hours.iloc[0, i] / 1000:
            i += 1
        # print(i)
        if abs(posix_time - data_hours.iloc[0, i]) > abs(posix_time - data_hours.iloc[0, i - 1]):
            i -= 1

        # Liste des altitudes pour lesquelles les données sont recensées
        liste_altitude_pression = [150, 200, 250, 300, 400, 500, 600, 700, 800, 850, 900, 925, 950, 1000, 1013.25]

        # Calcul de l'altitude pression de l'avion
        altitude_pression_avion = self.calcul_altitude_pression()

        # Détermination de l'altitude recensée la plus proche de l'altitude de l'avion
        j = 0
        while altitude_pression_avion > liste_altitude_pression[j]:
            j += 1
        # print(j)
        if abs(altitude_pression_avion - liste_altitude_pression[j]) > abs(
                altitude_pression_avion - liste_altitude_pression[j - 1]):
            altitude_database = liste_altitude_pression[j - 1]
        else:
            altitude_database = liste_altitude_pression[j]
        #print(altitude_database)

        # Récupération des données recherchées dans la database
        if altitude_database != 1013.25:
            temperature = df[f'data_temp-{altitude_database}h_{i}']
        else:
            temperature = df[f'data_temp-surface_{i}']

        temperature_vraie = temperature.iloc[0]
        return temperature_vraie




