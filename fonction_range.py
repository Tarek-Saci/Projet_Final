import Requete_api
import math
from Donnees import *

'''
def get_windy_data(lat , lon):
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.requete_api.urlopen(url_request) as url:
        data = json.load(url)
    print(data)

get_windy_data(45.00 ,45.00)
'''
class GPS:
    def __init__(self, latitude,longitude,altitude,cap):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.cap = math.radians(cap)
        # Rayon de la Terre en mètres
        self.rayon_terre = 6371 * 1000  # En mètres

    def distance_entre_2_points(self, lat2, lon2):
        # Convertir les coordonnées degrés en radians
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Calcul des différences de latitude et de longitude
        diff_lat = lat2 - lat1
        diff_lon = lon2 - lon1

        # Calcul de la distance
        a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.rayon_terre * c * 0.001 # *1000 pour avoir des kilomètres

        return round(distance,3)

class Performance:
    def __init__(self, finesse, vitesse, dist_roulage_mini,carburant_restant, probleme_moteur):
        self.finesse = finesse
        self.vitesse = vitesse
        self.dist_roulage_mini = dist_roulage_mini
        self.carburant = carburant_restant
        self.probleme_moteur = probleme_moteur

    def range_plane(self, altitude, hauteur_aerodrome):  # calcul du range
        range_theorique_plane = (altitude - hauteur_aerodrome) * self.finesse / 6076.12 # on ne sait pas encore si on aura les altitudes des aerodromes

        return round(range_theorique_plane,3) # en [nm]
    def conso_vitesse(self):
        # --------de 0ft à 4000ft--------
        gph = 0.00160782 * self.vitesse **(2) - 0.205136 * self.vitesse + 9.88425 #exemple pour un cessna-152 entre 6000ft et 8000ft
        0.00321894 * x ** (2) - 0.470747 * x + 20.9657
        # --------de 4000ft à 6000ft--------
        0.00153755 * x ** (2) - 0.182342 * x + 8.56135
        # --------de 6000ft à 8000ft--------

        # --------de 8000ft à 10000ft--------

        # --------de 10000ft à 12000ft--------
        return round(gph,3)


    def range_moteur(self): # range = (gph / carburant restsant) * vitesse
        gph = self.conso_vitesse(self.vitesse)
        range_theorique = (self.carburant / gph) * self.vitesse # il vaut mieux utiliser les unités en Kts nm pck generalement les données sont dans ces unitées
        return round(range_theorique,3)

    def correction_range(self, range_theorique, vitesse_vent, direction_vent):
        vent_x = vitesse_vent * math.cos(math.radians(direction_vent))
        vent_y = vitesse_vent * math.sin(math.radians(direction_vent))

        vitesse_relative = math.sqrt((self.vitesse - vent_x)**2 + vent_y**2)
        range_corrige = (range_theorique / self.vitesse) * vitesse_relative
        return round(range_corrige,3)



