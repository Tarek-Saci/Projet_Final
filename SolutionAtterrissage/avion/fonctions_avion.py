import math
import numpy as np

#Ce programme permet d'obtenir en temps réel les données météorologiques en un point donné
#Ce point doit être repéré par ses coordonnées GPS (latitude, longitude). La latitude doit être un flottant
# compris entre -89.99° et 90° tandis que la longitude peut être un flottant quelconque
"""def get_windy_data(lat, lon):
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
    altitude_m=altitude/3.28
    if altitude_m<11000:
        pression = 1013.25*(1-0.0065*altitude_m/288.15)**(9.81/(0.0065*287.04))
    else:
        pression = 226.32*math.exp(-9.81*(altitude_m-11000)/(287.04*216.65))
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
                    lon_aerodrome_plus_proche,lat_aerodrome_plus_proche,new_cap):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    if avion.longitude != lon_aerodrome_plus_proche :
        ax1.text(0, 0.9, f'Latitude avion =  {avion.latitude} ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.85, f'Longitude avion = {avion.longitude} ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.75, 'Aérodromes hors de portée', fontsize=11, color='red')
        ax1.text(0, 0.65, 'Aérodromes à portée', fontsize=11, color='blue')
        ax1.text(0, 0.55, 'Aérodromes à portée et avec une piste ', fontsize=11, color='green')
        ax1.text(0, 0.50, "d'atterrissage suffisamment longue", fontsize=11, color='green')
        ax1.text(0, 0.40, f'Latitude aéroport le plus proche = {lat_aerodrome_plus_proche} ', fontsize=11, color='darkmagenta')
        ax1.text(0, 0.35, f'Longitude aéroport le plus proche = {lon_aerodrome_plus_proche} ', fontsize=11, color='darkmagenta')
        ax1.text(0, 0.25, f'Nouveau cap à prendre = {new_cap} ', fontsize=11, color='darkmagenta')
    else:
        ax1.text(0, 0.9, f'Latitude avion =  {avion.latitude} ', fontsize=11, color='goldenrod')
        ax1.text(0, 0.85, f'Longitude avion = {avion.longitude} ', fontsize=11, color='goldenrod')
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

    lat = np.array([aeroport.latitude for aeroport in aerodromes])
    lon = np.array([aeroport.longitude for aeroport in aerodromes])

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

def cherche_longueur_piste(aeroport,dist_roulage_mini):

    numero_pistes = []
    resultat = False

    for i in range(0,len(aeroport.pistes)):
        chiffres = re.findall(r'\d+', aeroport.pistes[i].longeur)
        chiffres_concatenes = ''.join(chiffres)
        nombre = int(chiffres_concatenes)
        if nombre > dist_roulage_mini:
            resultat = True
            numero_pistes.append(i)

    return  resultat,numero_pistes"""

def calcul_new_cap (lat_avion, longi_avion, lat_aerodrome,longi_aerodrome) :
    """Défini la valeur du nouveau cap que doit suivre l'avion pour atteindre l'aéroport le plus proche.

    Paramètres d'entrée:
    lat_avion -- latitude de l'avion
    longi_avion -- longitude de l'avion
    lat_aerodrome -- latitude de l'aérodrome le plus proche
    longi_aerodrome -- longitude de l'aérodrome le plus proche

    Utilise la méthode de calcul de l'azimut afin de calculer un angle à suivre par rapport au nord géographique à partir de 2 positions géographiques
    Convertit au format de cap 0°-360° dans le cas d'un angle négatif

    Return la valeur du nouveau cap à suivre en degrés
    """
    lat_avion_rad = lat_avion * (np.pi / 180)
    lat_aerodrome_rad = lat_aerodrome * (np.pi / 180)
    longi_avion_rad = longi_avion * (np.pi / 180)
    longi_aerodrome_rad = longi_aerodrome * (np.pi / 180)

    diff_longi = longi_aerodrome_rad - longi_avion_rad

    azimut_rad = np.arctan2(math.sin(diff_longi) *np.cos(lat_aerodrome_rad), np.cos(lat_avion_rad) *np.sin(lat_aerodrome_rad) - np.sin(lat_avion_rad) *np.cos(lat_aerodrome_rad) *np.cos(diff_longi))
    azimut_deg = azimut_rad*(180/np.pi)
    if azimut_deg < 0 :
        azimut_deg += 360

    return azimut_deg

def distance_avec_virage(vitesse, x_avion, y_avion, x_aero, y_aero, cap):
    """
    Cette fonction permet de calculer la distance entre l'avion et l'aéroport le plus proche en prenant
    en compte le potentiel virage que l'avion devra réaliser pour rejoindre l'aéroport

    Args:
        vitesse (float) : La vitesse de l'avion (en kts)
        x_avion (float) : La longitude de l'avion (un réel)
        y_avion (float) : La latitude de l'avion (un réel compris entre -89.99° et 90°)
        x_aéroport (float) : La longitude de l'aéroport (un réel)
        y_aéroport (float) : La latitude de l'aéroport (un réel compris entre -89.99° et 90°)
        cap (float) : Le cap de l'avion (un réel compris entre 0° et 360°)

    Returns:
        distance_cercle_nm (float) : La distance ajoutée par la prise en compte du virage (en nm)
        angle_cap_aero (float) : L'angle entre le cap de l'avion et le vecteur avion-aéroport (en °)
    """
    #Angle du cap par rapport à l'horizontal en degré

    if 180>cap>90:
        angle_cap = 450-cap
    elif 0<=cap<=90:
        angle_cap=90-cap
    else:
        angle_cap = 90 + abs(cap)

    #Conversion des coordonnées GPS en km
    x_avion_km = x_avion * 78.567
    y_avion_km = y_avion * 111
    x_aero_km = x_aero * 78.567
    y_aero_km = y_aero * 111
    #Coordonnées du vecteur avion-aéroport avec les coordonnées convertis en km
    vect_av_aero = [x_aero_km-x_avion_km, y_aero_km-y_avion_km]

    #Calcul de l'angle entre le cap et l'aéroport
    angle_cap_aero = angle_cap - math.degrees(math.acos(vect_av_aero[0]/(vect_av_aero[0]**2+vect_av_aero[1]**2)**0.5))

    #Calcul du rayon minimal de virage (le facteur de charge maximale pour un avion civil est généralement n=1.19)
    vitesse_ms = vitesse * 0.5144
    rayon_virage_km = vitesse_ms**2/(9.81*(1.19**2-1)**0.5)/1000

    #Détermination des coordonnées du milieu du cercle
    #Si l'angle entre le cap et l'aéroport est inférieur à 180° le virage se fera vers la droite,
    #sinon il se fera vers la gauche

    if angle_cap_aero < 180:
        milieu_cercle = [rayon_virage_km * math.cos(math.radians(angle_cap) + math.pi/2) + x_avion_km,
                         rayon_virage_km * math.sin(math.radians(angle_cap) + math.pi/2) + y_avion_km]
    else:
        milieu_cercle = [rayon_virage_km * math.cos(math.radians(angle_cap) - math.pi/2) + x_avion,
                         rayon_virage_km * math.sin(math.radians(angle_cap) - math.pi/2) + y_avion]
        
    #Calcul de la distance parcourue en virage

    if angle_cap_aero < 45 or angle_cap_aero > 315:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.125
    elif angle_cap_aero < 90 or angle_cap_aero > 270:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.25
    elif angle_cap_aero < 135 or angle_cap_aero > 225:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.375
    else:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.5


    #Calcul de la distance en ligne droite restante après le virage distance_av
    distance_centrecercle_aero = ((x_aero_km-milieu_cercle[0])**2+(y_aero_km-milieu_cercle[1])**2)**0.5
    distance_av=(distance_centrecercle_aero**2-rayon_virage_km**2)**0.5

    #print('distance après virage', distance_av)

    #distance_reelle = distance_cercle + distance_av
    distance_cercle_nm = distance_cercle / 1.852


    return distance_cercle_nm, angle_cap_aero


