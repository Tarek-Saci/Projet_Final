import pandas as pd
import numpy as np
from SolutionAtterrissage import aeroport
from SolutionAtterrissage import affichage
from SolutionAtterrissage import atmosphere
from SolutionAtterrissage import avion
from SolutionAtterrissage import donnees

# ---------- YAML ---------- #

parser = donnees.LecteurYAML('SolutionAtterrissage/donnees/deck.yaml')
parametres_init = parser.read_yaml()

# ---------- INFORMATIONS AEROPORT.CSV ---------- #

df = pd.read_csv("SolutionAtterrissage/donnees/Aeroport.csv")
colonnes_souhaitees = ['objectid', 'nomcarto', 'codeindic', 'typeinfras', 'nbrpiste', 'longpiste2',
                       'surface', 'latitude', 'longitude', 'acces']
df_colonnes = df[colonnes_souhaitees]
aerodromes = []
df_final = df_colonnes[(df_colonnes['typeinfras'] == 'Aéroport') | (df_colonnes['typeinfras'] == 'Aérodrome')].reset_index()
objectid_array = df_final['objectid'].to_numpy()
nomcarto_array = df_final['nomcarto'].to_numpy()
codeindic_array = df_final['codeindic'].to_numpy()
typeinfras_array = df_final['typeinfras'].to_numpy()
nbrpiste_array = df_final['nbrpiste'].to_numpy()
longpiste2_array = df_final['longpiste2'].to_numpy()
surface_array = df_final['surface'].to_numpy()
latitude_array = df_final['latitude'].to_numpy()
longitude_array = df_final['longitude'].to_numpy()
acces_array = df_final['acces'].to_numpy()

# ---------- CREATION DES AERODROMES ---------- #

vecteur_creer_aerodrome = np.vectorize(aeroport.creer_aerodrome)

aerodromes = vecteur_creer_aerodrome(objectid_array, nomcarto_array, codeindic_array,
                                     typeinfras_array, nbrpiste_array, longpiste2_array,
                                     surface_array, latitude_array, longitude_array, acces_array)

# ---------- CALCUL PERFORMANCE DE L'AVION ---------- #

mon_air = atmosphere.Air(parametres_init["latitude"],parametres_init["longitude"],parametres_init["altitude"])

performance = avion.Performance(parametres_init["finesse"],parametres_init["vitesse"],
                          parametres_init["vitesse_plane"],parametres_init["altitude"],
                          parametres_init["dist_roulage_mini"],parametres_init["carburant_restant"],
                          parametres_init["moteur_avion"],mon_air)

# ---------- CALCUL RANGE THEORIQUE ---------- #

if parametres_init["moteur_avion"]:
    range_theorique = performance.range_moteur_theorique()
else:
    range_theorique = performance.range_plane_theorique()

# ---------- CREATION DE L'AVION ---------- #

coordonnees_avion = (parametres_init["latitude"],parametres_init["longitude"])

avion_1 = avion.Avion(coordonnees_avion, range_theorique, parametres_init["altitude"])
lons,lats = affichage.cercle_range(range_theorique,avion_1)
list_coordonnes_sur_cercle = np.column_stack((lats, lons))

# ---------- CREATION DES VENTS DES POINTS DU CERCLE ---------- #

vents = np.zeros((affichage.nombre_points,affichage.discretisation+1,2))
coordonnees = np.zeros((affichage.nombre_points,affichage.discretisation+1,2))

for i in range(0,affichage.nombre_points):
    coordonnees_points_interieurs = atmosphere.calcul_coordonnees_vents_trajet(affichage.discretisation,coordonnees_avion,list_coordonnes_sur_cercle[i][0],list_coordonnes_sur_cercle[i][1])
    for y in range(0,affichage.discretisation):
        coordonnees[i,y] = coordonnees_points_interieurs[y]
    coordonnees[i,affichage.discretisation] = (list_coordonnes_sur_cercle[i,0],list_coordonnes_sur_cercle[i,1])

for i in range(0,affichage.nombre_points):
    for y in range(0,affichage.discretisation):
        vents[i][y] = mon_air.calcul_vent()
    vents[i,affichage.discretisation] = mon_air.calcul_vent()

list_vents = []

for i in range(0,affichage.nombre_points):
    vent1 = atmosphere.calcul_moyenne_vents_trajet(vents[i,:])
    list_vents.append(vent1)

list_vents_array = np.array(list_vents)

# ---------- CALCUL RANGE AVEC VENT ---------- #

if parametres_init["moteur_avion"]:
    range_corrige = performance.range_moteur_reel(list_vents_array,affichage.vecteur_angle)
else:
    range_corrige = performance.range_plane_reel(list_vents_array,affichage.vecteur_angle)

lons_reel,lats_reel = affichage.cercle_range_reel(range_corrige,avion_1)

list_coordonnes_sur_cercle_reel = np.column_stack((lats_reel, lons_reel))
list_coordonnes_sur_cercle_reel = np.concatenate((list_coordonnes_sur_cercle_reel, np.column_stack((lats_reel[0], lons_reel[0]))))

# ---------- CREATION DES AERODROMES DANS LA RANGE AVEC VENT ---------- #

aerodromes_in_range = []
for aerodrome in aerodromes:
    wn = affichage.winding_number((aerodrome.latitude,aerodrome.longitude), list_coordonnes_sur_cercle_reel)
    if wn != 0:
        aerodromes_in_range.append(aerodrome)

lons_in_range = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range])
lats_in_range = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range])
aerodromes_in_range_right_size = []

for aerodrome in aerodromes_in_range:
    resultat,numero_pistes = aeroport.cherche_longueur_piste(aerodrome,parametres_init["dist_roulage_mini"])
    if resultat == True:
        aerodromes_in_range_right_size.append(aerodrome)

lons_in_range_in_size = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range_right_size])
lats_in_range_in_size = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range_right_size])

# ---------- AERODROME LE PLUS PROCHE ---------- #

distance = np.array(affichage.calcul_entre_deux_coordonnees(coordonnees_avion,lats_in_range_in_size,lons_in_range_in_size))
if len(distance) != 0:
    min_value = np.min(distance)
    min_index = np.argmin(distance)
    lat_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].latitude
    lon_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].longitude
    new_cap = avion.calcul_new_cap(avion_1.latitude,avion_1.longitude,lat_aerodrome_plus_proche,lon_aerodrome_plus_proche)
else:
    lat_aerodrome_plus_proche = avion_1.latitude
    lon_aerodrome_plus_proche = avion_1.longitude
    new_cap = 0

# ---------- AFFICHAGE DE LA CARTE FINALE ---------- #


if parametres_init["moteur_avion"] == True :
    distance_reelle, angle_cap_aero = avion.distance_avec_virage(parametres_init["vitesse"], avion_1.longitude, avion_1.latitude, -68.79560969, 53.17322831, parametres_init["cap"])
else:
    distance_reelle, angle_cap_aero = avion.distance_avec_virage(parametres_init["vitesse_plane"], avion_1.longitude, avion_1.latitude, -68.79560969, 53.17322831, parametres_init["cap"])

affichage.affichage_carte(aerodromes,avion_1,
                   lons,lats,
                   lons_in_range,lats_in_range,
                   lons_in_range_in_size,lats_in_range_in_size,
                   lons_reel,lats_reel,
                   lon_aerodrome_plus_proche,lat_aerodrome_plus_proche,new_cap,distance_reelle)