import math

def distance_avec_virage(vitesse, x_avion, y_avion, x_aero, y_aero, cap):
    #Angle du cap par rapport à l'horizontal en degré
    if cap>90:
        angle_cap =450-cap
    elif cap<=90:
        angle_cap=90-cap
    else:
        angle_cap = 90 + abs(cap)

    print('anglecap', angle_cap)

    #Conversion des coordonnées GPS en km
    x_avion_km = x_avion * 78.567
    y_avion_km = y_avion * 111
    x_aero_km = x_aero * 78.567
    y_aero_km = y_aero * 111
    #Coordonnées du vecteur avion-aéroport avec les coordonnées convertis en km
    vect_av_aero = [x_aero_km-x_avion_km, y_aero_km-y_avion_km]
    print(vect_av_aero)

    #Calcul de l'angle entre le cap et l'aéroport
    angle_cap_aero = angle_cap - math.degrees(math.acos(vect_av_aero[0]/(vect_av_aero[0]**2+vect_av_aero[1]**2)**0.5))
    print('angle cap aero', angle_cap_aero)

    #Calcul du rayon minimal de virage (le facteur de charge maximale pour un avion civil est généralement n=1.19)
    vitesse_ms = vitesse * 0.5144
    print(vitesse_ms)
    rayon_virage_km = vitesse_ms**2/(9.81*(1.19**2-1)**0.5)/1000
    print('rayon', rayon_virage_km)

    #Détermination des coordonnées du milieu du cercle
    #Si l'angle entre le cap et l'aéroport est inférieur à 180° le virage se fera vers la droite,
    #sinon il se fera vers la gauche

    if angle_cap_aero < 180:
        milieu_cercle = [rayon_virage_km * math.cos(math.radians(angle_cap) + math.pi/2) + x_avion_km,
                         rayon_virage_km * math.sin(math.radians(angle_cap) + math.pi/2) + y_avion_km]
    else:
        milieu_cercle = [rayon_virage_km * math.cos(math.radians(angle_cap) - math.pi/2) + x_avion,
                         rayon_virage_km * math.sin(math.radians(angle_cap) - math.pi/2) + y_avion]

    print('milieu', milieu_cercle)

    #Calcul de la distance parcourue en virage

    if angle_cap_aero < 45 or angle_cap_aero > 315:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.125
    elif angle_cap_aero < 90 or angle_cap_aero > 270:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.25
    elif angle_cap_aero < 135 or angle_cap_aero > 225:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.375
    else:
        distance_cercle = 2 * math.pi * rayon_virage_km * 0.5
    print('distance sur cercle',distance_cercle)

    #Calcul de la distance en ligne droite restante après le virage distance_av
    distance_centrecercle_aero = ((x_aero_km-milieu_cercle[0])**2+(y_aero_km-milieu_cercle[1])**2)**0.5
    distance_av=(distance_centrecercle_aero**2-rayon_virage_km**2)**0.5

    print('distance après virage', distance_av)

    distance_reelle = distance_cercle + distance_av

    return distance_reelle

print(distance_avec_virage(100,-72.142587,49.826251,-68.28109779,49.826251,-90))