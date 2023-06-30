from mpl_toolkits.basemap import Basemap
from .donnees_fixees import *
import matplotlib.pyplot as plt
import math


def affichage_carte(aerodromes,avion,parametres_init,lons,lats,
                    lons_in_range,lats_in_range,
                    lons_in_range_in_size,lats_in_range_in_size,
                    lons_reel,lats_reel,
                    lon_aerodrome_plus_proche,lat_aerodrome_plus_proche,new_cap):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    if avion.longitude != lon_aerodrome_plus_proche :
        ax1.text(0, 1.0, f'Légendes et informations utiles ', fontsize=13, color='black')
        ax1.text(0, 0.9, f'Latitude avion :  {avion.latitude}°N ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.85, f'Longitude avion : {avion.longitude}°W ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.75, 'Aérodromes hors de portée', fontsize=11, color='red')
        ax1.text(0, 0.65, 'Aérodromes atteignables', fontsize=11, color='blue')
        ax1.text(0, 0.55, 'Aérodromes atteignables et avec une piste ', fontsize=11, color='green')
        ax1.text(0, 0.50, "d'atterrissage suffisamment longue", fontsize=11, color='green')
        ax1.text(0, 0.40, f'Latitude aéroport le plus proche : {lat_aerodrome_plus_proche}°N ', fontsize=11, color='darkmagenta')
        ax1.text(0, 0.35, f'Longitude aéroport le plus proche : {lon_aerodrome_plus_proche}°W ', fontsize=11, color='darkmagenta')
        ax1.text(0, 0.25, f'Nouveau cap à suivre : {new_cap}° ', fontsize=11, color='darkmagenta')
    else:
        ax1.text(0, 1.0, f'Légendes et informations utiles ', fontsize=13, color='black')
        ax1.text(0, 0.9, f'Latitude avion :  {avion.latitude}°N ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.85, f'Longitude avion : {avion.longitude}°W ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.75, 'Aérodromes hors de portée', fontsize=11, color='red')
        ax1.text(0, 0.65,"Il n'y a pas d'aérodrome à votre portée où", fontsize=11, color='black')
        ax1.text(0, 0.60,"vous pouvez atterrir en toute sécurité.", fontsize=11, color='black')
    ax1.axis('off')  # Désactiver les axes

    # Création de la carte
    m = Basemap(ax = ax2, projection='merc', llcrnrlat=44, urcrnrlat=63, llcrnrlon=-82, urcrnrlon=-54, resolution='i')
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

    if avion.longitude != lon_aerodrome_plus_proche :
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

    conversion_kilometre_degre = 78.567  # Approximation pour une latitude moyenne
    rayon_kilometre = range_avion * 1.852
    rayon_deg = rayon_kilometre / conversion_kilometre_degre
    angles_degrees = []

    # Génération des points le long du cercle
    for i in range (0,len(angles)):
        angles_degrees.append(math.degrees(angles[i]))

    lons = avion.longitude + rayon_deg * np.cos(angles)
    lats = avion.latitude + rayon_deg * np.sin(angles)

    return lons,lats

def cercle_range_reel(range_avion_reel,avion):
    # Conversion du rayon en degrés approximatifs (à une latitude moyenne)

    conversion_kilometre_degre = 78.567  # Approximation pour une latitude moyenne
    rayon_kilometre = range_avion_reel * 1.852
    rayon_deg = rayon_kilometre / conversion_kilometre_degre
    print(f'Range en kilomètre : {rayon_kilometre}')
    angles_degrees = []

    # Génération des points le long du cercle
    for i in range (0,len(angles)):
        angles_degrees.append(math.degrees(angles[i]))

    lons_reel = avion.longitude + rayon_deg * np.cos(angles_points)
    lats_reel = avion.latitude + rayon_deg * np.sin(angles_points)

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
