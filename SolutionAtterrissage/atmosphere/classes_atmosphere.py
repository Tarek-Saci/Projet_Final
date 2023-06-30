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

    def calcul_altitude_pression(self):
        """
        Cette méthode de la classe Air permet de calculer la pression (en hPa) à l'altitude donnée selon
        le modèle de l'atmosphère standard. En effet, les données météorologiques sont classées
        en niveaux de pression

        Args:
            altitude (int): L'altitude en mètres (un réel positif)

        Returns:
            pression: La pression à l'altitude souhaitée (en hPa)
        """
        if self.altitude < 11000:
            #Modèle dans la troposphère
            pression = 1013.25 * (1 - 0.0065 * self.altitude / 288.15) ** (9.81 / (0.0065 * 287.04))
        else:
            #Modèle dans la stratosphère
            pression = 226.32 * math.exp(-9.81 * (self.altitude - 11000) / (287.04 * 216.65))
        return pression

    def calcul_vent(self):
        """Cette méthode de la classe Air permet de déterminer le vecteur vitesse du vent à la position GPS et l'altitude donnée

        Args:
            latitude (float): La latitude du point recherché compris entre -89.99° et 90°
            lon (float): La longitude du point recherché appartenant aux nombres réels
            altitude (int): L'altitude en mètres (un réel positif)

        Returns:
            vecteur_vent: Une liste de deux valeurs contenant la composante horizontale et la composante verticale du vent (en kts)
        """
        # Récupération des données dans la base de données de Windy
        meteo = get_windy_data(self.latitude, self.longitude)

        # Détermination de l'heure de la requête
        # En format POSIX
        posix_time = datetime.datetime.now().timestamp()
        # En format classique
        #classical_time = datetime.datetime.fromtimestamp(posix_time)

        # Transformation du JSON en dataframe pandas
        flattened = flatten_json(meteo)
        df = pd.DataFrame([flattened])

        # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
        data_hours = df.filter(like="data_hours")

        i = 0
        while posix_time > data_hours.iloc[0, i] / 1000:
            i += 1

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
        if abs(altitude_pression_avion - liste_altitude_pression[j]) > abs(
                altitude_pression_avion - liste_altitude_pression[j - 1]):
            altitude_database = liste_altitude_pression[j - 1]
        else:
            altitude_database = liste_altitude_pression[j]

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
        """
        Cette méthode de la classe Air permet de déterminer la température à la position GPS et l'altitude donnée

        Args:
            latitude (float): La latitude du point recherché compris entre -89.99° et 90°
            lon (float): La longitude du point recherché appartenant aux nombres réels
            altitude (int): L'altitude en mètres (un réel positif)

        Returns:
            température_vraie (float) : La valeur de la température recherchée exprimée (en K)
        """
        # Récupération des données dans la base de données de Windy
        meteo = get_windy_data(self.latitude, self.longitude)

        # Détermination de l'heure de la requête
        # En format POSIX
        posix_time = datetime.datetime.now().timestamp()
        # En format classique
        #classical_time = datetime.datetime.fromtimestamp(posix_time)

        # Transformation du JSON en dataframe pandas
        flattened = flatten_json(meteo)
        df = pd.DataFrame([flattened])

        # Détermination de l'heure répertoriée la plus proche de l'heure actuelle
        data_hours = df.filter(like="data_hours")

        i = 0
        while posix_time > data_hours.iloc[0, i] / 1000:
            i += 1
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

        if abs(altitude_pression_avion - liste_altitude_pression[j]) > abs(
                altitude_pression_avion - liste_altitude_pression[j - 1]):
            altitude_database = liste_altitude_pression[j - 1]
        else:
            altitude_database = liste_altitude_pression[j]

        # Récupération des données recherchées dans la database
        if altitude_database != 1013.25:
            temperature = df[f'data_temp-{altitude_database}h_{i}']
        else:
            temperature = df[f'data_temp-surface_{i}']

        temperature_vraie = temperature.iloc[0]
        return temperature_vraie




