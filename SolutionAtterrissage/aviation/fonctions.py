from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import datetime
import re
from .Donnees import *

#Ce programme permet d'obtenir en temps réel les données météorologiques en un point donné
#Ce point doit être repéré par ses coordonnées GPS (latitude, longitude). La latitude doit être un flottant
# compris entre -89.99° et 90° tandis que la longitude peut être un flottant quelconque
def get_windy_data(lat, lon):
    url_base = "https://node.windy.com/forecast/meteogram/ecmwf/"
    url_request = url_base + str(lat) + "/" + str(lon)
    import urllib.request, json
    with urllib.request.urlopen(url_request) as url:
        data = json.load(url)
        # data = pd.read_json(url)
    return data

# recursive function to flatten nested fields
def flatten_json(data, prefix=''):
    if isinstance(data, dict):
        flattened = {}
        for key, value in data.items():
            flattened.update(flatten_json(value, prefix + key + '_'))
        return flattened
    elif isinstance(data, list):
        flattened = {}
        for i, item in enumerate(data):
            flattened.update(flatten_json(item, prefix + str(i) + '_'))
        return flattened
    else:
        return {prefix[:-1]: data}

# L'argument doit être entré en mètres
def calcul_altitude_pression(altitude):
    #d'après l'ISA
    if altitude<11000:
        pression = 1013.25*(1-0.0065*altitude/288.15)**(9.81/(0.0065*287.04))
    else:
        pression = 226.32*math.exp(-9.81*(altitude-11000)/(287.04*216.65))
    return pression

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

def affichage_carte(aerodromes,avion,parametres_init,lons,lats,
                    lons_in_range,lats_in_range,
                    lons_in_range_in_size,lats_in_range_in_size,
                    lons_reel,lats_reel,
                    lon_aerodrome_plus_proche,lat_aerodrome_plus_proche):

    # Création de la carte
    m = Basemap(projection='merc', llcrnrlat=44, urcrnrlat=65, llcrnrlon=-82, urcrnrlon=-54, resolution='i')
    m.drawcoastlines()
    m.fillcontinents(color='peachpuff',lake_color='skyblue')
    # Affichage de la carte
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    m.drawmapboundary(fill_color='skyblue')
    m.drawcountries()
    m.drawstates()

    lat = np.array([aerodrome.latitude for aerodrome in aerodromes])
    lon = np.array([aerodrome.longitude for aerodrome in aerodromes])

    x, y = m(lon, lat)
    m.plot(x, y, 'ro', markersize=3)

    x_in_range,y_in_range = m(lons_in_range,lats_in_range)
    m.plot(x_in_range,y_in_range, 'bo', markersize=3)

    x_in_range_in_size, y_in_range_in_size = m(lons_in_range_in_size,lats_in_range_in_size)
    m.plot(x_in_range_in_size, y_in_range_in_size, 'go', markersize=3)

    m.drawgreatcircle(avion.longitude, avion.latitude, lon_aerodrome_plus_proche, lat_aerodrome_plus_proche, linewidth=1, color='m')

    x_aerodrome_plus_proche, y_aerodrome_plus_proche = m(lon_aerodrome_plus_proche, lat_aerodrome_plus_proche)
    m.plot(x_aerodrome_plus_proche, y_aerodrome_plus_proche, 'mo', markersize=3)

    x_avion, y_avion = m(avion.longitude, avion.latitude)
    m.plot(x_avion, y_avion, 'yo', markersize=5)

    # Conversion des coordonnées en coordonnées de la carte
    x, y = m(lons,lats)

    lons_reel = np.concatenate((lons_reel, np.array([lons_reel[0]])))
    lats_reel = np.concatenate((lats_reel, np.array([lats_reel[0]])))

    x_reel,y_reel = m(lons_reel,lats_reel)

    # Tracé du cercle reel sur la carte
    m.plot(x_reel,y_reel, 'g-', linewidth=1)
    # Tracé du cercle sur la carte
    m.plot(x, y, 'b-', linewidth=1)


    """lon_depart, lat_depart = avion.longitude, avion.latitude
    norme = 0.0001
    angle_rad = np.radians(45)
    dx = norme * np.cos(angle_rad)
    dy = norme * np.sin(angle_rad)
    x_depart, y_depart = m(lon_depart, lat_depart)
    x_arrow = x_depart + dx
    y_arrow = y_depart + dy
    plt.arrow(x_depart, y_depart, x_arrow,y_arrow, color='red', width=1)"""

    plt.show()

def calcul_entre_deux_coordonnees(point1,lat2,lon2):

    lat1 = np.radians(point1[0])
    lat2 = np.radians(lat2)
    lon1 = np.radians(point1[1])
    lon2 = np.radians(lon2)

    # rayon de la Terre
    r = 6371
    #distance = 2*r*math.asin(math.sqrt((math.sin((lat2-lat1)/2)**2)+(math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2)))
    distance = r*(np.arccos(np.sin(lat1)*np.sin(lat2)+(np.cos(lat1)*np.cos(lat2)*np.cos(lon2-lon1))))

    return distance

def cercle_range(range_avion,avion):
    # Conversion du rayon en degrés approximatifs (à une latitude moyenne)

    conversion_kilometre_degre = 111  # Approximation pour une latitude moyenne
    rayon_kilometre = range_avion * 1.852
    rayon_deg = rayon_kilometre / conversion_kilometre_degre
    print(f'Rayon : {rayon_kilometre}')
    angles_degrees = []

    # Génération des points le long du cercle
    for i in range (0,len(angles)):
        angles_degrees.append(math.degrees(angles[i]))

    lons = avion.longitude + rayon_deg * np.cos(angles)
    lats = avion.latitude + rayon_deg * np.sin(angles)
    print(f'Lats : {lats}')
    print(f'Lons : {lons}')

    return lons,lats

def cercle_range_reel(range_avion_reel,avion):
    # Conversion du rayon en degrés approximatifs (à une latitude moyenne)

    conversion_kilometre_degre = 111  # Approximation pour une latitude moyenne
    rayon_kilometre = range_avion_reel * 1.852
    rayon_deg = rayon_kilometre / conversion_kilometre_degre
    print(f'Rayon : {rayon_kilometre}')
    angles_degrees = []

    # Génération des points le long du cercle
    for i in range (0,len(angles)):
        angles_degrees.append(math.degrees(angles[i]))

    lons_reel = avion.longitude + rayon_deg * np.cos(angles_points)
    lats_reel = avion.latitude + rayon_deg * np.sin(angles_points)
    print(f'Lats : {lons_reel}')
    print(f'Lons : {lats_reel}')

    return lons_reel,lats_reel

def is_left(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])

def winding_number(point, sommets):

    wn = 0  # Initialisation du nombre de tours

    for i in range(len(sommets)):
        sommet1 = sommets[i]
        sommet2 = sommets[(i + 1) % len(sommets)]

        if sommet1[1] <= point[1]:
            if sommet2[1] > point[1] and is_left(sommet1, sommet2, point) > 0:
                wn += 1
        else:
            if sommet2[1] <= point[1] and is_left(sommet1, sommet2, point) < 0:
                wn -= 1

    return wn

def cherche_longueur_piste(aerodrome,dist_roulage_mini):

    numero_pistes = []
    resultat = False

    for i in range(0,len(aerodrome.pistes)):
        chiffres = re.findall(r'\d+', aerodrome.pistes[i].longeur)
        chiffres_concatenes = ''.join(chiffres)
        nombre = int(chiffres_concatenes)
        if nombre > dist_roulage_mini:
            resultat = True
            numero_pistes.append(i)

    return  resultat,numero_pistes

def calcul_new_cap (lat_avion, longi_avion, lat_aerodrome,longi_aerodrome) :
    lat_avion_rad = lat_avion * (np.pi / 180)
    lat_aerodrome_rad = lat_aerodrome * (np.pi / 180)
    longi_avion_rad = longi_avion * (np.pi / 180)
    longi_aerodrome_rad = longi_aerodrome * (np.pi / 180)

    diff_longi =  longi_aerodrome_rad - longi_avion_rad
    # l'azimut entre 2 point correspond à l'angle formé par la droite passant par ces 2 points et la ligne passant par le nord et sud géographique

    azimut_rad = np.arctan2(math.sin(diff_longi) *np.cos(lat_aerodrome_rad), np.cos(lat_avion_rad) *np.sin(lat_aerodrome_rad) - np.sin(lat_avion_rad) *np.cos(lat_aerodrome_rad) *np.cos(diff_longi))
    azimut_deg = azimut_rad*(180/np.pi)

    return azimut_deg