import requests
import math
from deck import *

'''
def get_windy_data(lat , lon):
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)
    print(data)

get_windy_data(45.00 ,45.00)
'''


# -----peut etre definir une class pour le calcul GPS---------

def range_plane(finesse, altitude, hauteur_aerodrome):  # calcul du range
    range_theorique_plane = (altitude - hauteur_aerodrome) * finesse # on ne sait pas encore si on aura les altitudes des aerodromes
    return range_theorique_plane

def conso_vitesse(vitesse_avion):
    gph = 0.00160782 * vitesse_avion **(2) - 0.205136 * vitesse_avion + 9.88425
    return gph

def range_moteur(vitesse_avion , carburant_restant): # range = (gph / carburant restsant) * vitesse
    gph = conso_vitesse(vitesse_avion)
    range_theorique = (gph / carburant_restant) * vitesse_avion # il vaut mieux utiliser les unités en Kts nm pck generalement les données sont dans ses unitées
    return range_theorique

def corriger_distance_franchissable(range_theorique, vitesse_avion, vitesse_vent, direction_vent):
    vent_x = vitesse_vent * math.cos(math.radians(direction_vent))
    vent_y = vitesse_vent * math.sin(math.radians(direction_vent))

    vitesse_relative = math.sqrt((vitesse_avion - vent_x)**2 + vent_y**2)
    range_corrige = (range_theorique / vitesse_avion) * vitesse_relative
    return range_corrige


def distance_entre_2_points(lat1, lon1, lat2, lon2):
    # Convertir les coordonnées degrés en radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Rayon de la Terre en mètres
    rayon_terre = 6371 * 1000  # En mètres

    # Calcul des différences de latitude et de longitude
    diff_lat = lat2 - lat1
    diff_lon = lon2 - lon1

    # Calcul de la distance
    a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = rayon_terre * c

    return distance

