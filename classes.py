import yaml
from fonctions import get_windy_data, flatten_json, calcul_altitude_pression
import datetime
import pandas as pd
class LecteurYAML:

    def __init__(self, file_path):
        self.file_path = file_path
    def read_yaml(self):
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")
class Avion:
    def __init__(self,coordonnees_avion,range_avion, altitude):
        self.latitude = coordonnees_avion[0]
        self.longitude = coordonnees_avion[1]
        self.range_theorique_avion = range_avion
        self.altitude = altitude

    def temperature(self):

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
        altitude_pression_avion = calcul_altitude_pression(self.altitude)

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
            temperature = df[f'temp-{altitude_database}h_{i}']
        else:
            temperature = df[f'temp-surface_{i}']

        return temperature
class Piste:
    def __init__(self,longeur):
        self.longeur = longeur
        #self.surface = surface
class Aerodrome:
    def __init__(self,objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface, latitude, longitude, acces):
        self.id = objectid
        self.nom = nomcarto
        self.code = codeindic
        self.type = typeinfras
        self.nombre_piste = nbrpiste
        self.pistes = []

        longeur = []
        resultat_longeur = longpiste2.split("/")
        if len(resultat_longeur) < nbrpiste:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[0])
        elif len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                longeur.append(resultat_longeur[i])
        else:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[i])
        """surface_liste = []
        resultat_surface = surface.split(",")
        if len(resultat_surface) != nbrpiste:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface)
        else:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface[i])"""

        if len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                self.pistes.append(Piste(longeur[i]))
        else:
            for i in range(0,int(nbrpiste)):
                self.pistes.append(Piste(longeur[i]))

        self.latitude = latitude
        self.longitude = longitude
        self.acces = acces
def creer_aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface,latitude, longitude, acces):
    return Aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                     surface,latitude, longitude, acces)