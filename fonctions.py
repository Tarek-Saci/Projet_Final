from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import math

def affichage_carte(aerodromes,avion,lons,lats,lons_in_range,lats_in_range):

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

    x_avion, y_avion = m(avion.longitude, avion.latitude)
    m.plot(x_avion, y_avion, 'go', markersize=3)

    # Conversion des coordonnées en coordonnées de la carte
    x, y = m(lons,lats)

    # Tracé du cercle sur la carte
    m.plot(x, y, 'b-', linewidth=1)

    plt.show()

def calcul_entre_deux_coordonnees(point1,point2):

    lat1 = math.radians(point1[0])
    lat2 = math.radians(point2[0])
    lon1 = math.radians(point1[1])
    lon2 = math.radians(point2[1])

    # rayon de la Terre
    r = 6371
    #distance = 2*r*math.asin(math.sqrt((math.sin((lat2-lat1)/2)**2)+(math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2)))
    distance = r*(math.acos(math.sin(lat1)*math.sin(lat2)+(math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1))))

    return distance

def cercle_range(range_avion,avion):
    # Conversion du rayon en degrés approximatifs (à une latitude moyenne)
    conversion_kilometre_degre = 111  # Approximation pour une latitude moyenne

    rayon_deg = range_avion / conversion_kilometre_degre

    nombre_points_cercle = 100
    # Génération des points le long du cercle
    angles = np.linspace(0, 2 * np.pi, nombre_points_cercle)
    lons = avion.longitude + rayon_deg * np.cos(angles)
    lats = avion.latitude + rayon_deg * np.sin(angles)

    coordonnes_sur_cercle = zip(lats, lons)

    return coordonnes_sur_cercle,lons,lats

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

