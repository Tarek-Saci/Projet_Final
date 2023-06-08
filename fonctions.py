import requests
from deck import *
import math

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

def range(finesse, altitude, hauteur_aerodrome):  # calcul du range
    range = (altitude - hauteur_aerodrome) * finesse # on ne sait pas encore si on aura les altitudes des aerodromes
    return range


def distance(lat1, lon1, lat2, lon2):
    # Convertir les coordonnées degrés en radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Rayon de la Terre en mètres
    rayon_terre = 6371 * 1000  # En mètres

    # Calcul des différences de latitude et de longitude
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    # Calcul de la distance
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = rayon_terre * c

    return distance
