import pandas as pd
import numpy as np
import SolutionAtterrissage

# ---------- YAML ---------- #

# Création de l'objet YAML qui lit le fichier "deck.yamL"
parser = SolutionAtterrissage.LecteurYAML('SolutionAtterrissage/aviation/deck.yaml')
# Lecture du fichier avec la fonction read_yaml()
parametres_init = parser.read_yaml()

# ---------- INFORMATIONS AEROPORT.CSV ---------- #

df = pd.read_csv("SolutionAtterrissage/aerodrome/Aeroport.csv")
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

vecteur_creer_aerodrome = np.vectorize(SolutionAtterrissage.creer_aerodrome)

aerodromes = vecteur_creer_aerodrome(objectid_array, nomcarto_array, codeindic_array,
                                     typeinfras_array, nbrpiste_array, longpiste2_array,
                                     surface_array, latitude_array, longitude_array, acces_array)

# ---------- CALCUL PERFORMANCE DE L'AVION ---------- #

performence = SolutionAtterrissage.Performance(parametres_init["finesse"],parametres_init["vitesse"],
                          parametres_init["vitesse_plane"],parametres_init["altitude"],
                          parametres_init["dist_roulage_mini"],parametres_init["carburant_restant"],
                          parametres_init["moteur_avion"])

# ---------- CALCUL RANGE THEORIQUE ---------- #

if parametres_init["moteur_avion"]:
    range_theorique = performence.range_moteur_theorique()
    print(f'range avec moteurs : {range_theorique} [nm]')
else:
    range_theorique = performence.range_plane_theorique()
    print(f'range sans moteurs : {range_theorique} [nm]')

# ---------- CREATION DE L'AVION ---------- #

coordonnees_avion = (parametres_init["latitude"],parametres_init["longitude"])
avion = SolutionAtterrissage.Avion(coordonnees_avion, range_theorique)

lons,lats = SolutionAtterrissage.cercle_range(range_theorique,avion)

list_coordonnes_sur_cercle = np.column_stack((lats, lons))

# ---------- CREATION DES VENTS DES POINTS DU CERCLE ---------- #
list_vents = []
for i in range(0,len(lons)-1):
    list_vents.append(SolutionAtterrissage.calcul_vent(list_coordonnes_sur_cercle[i][0],list_coordonnes_sur_cercle[i][1],parametres_init["altitude"]))
print(f' LISTE VENT : {list_vents}')
list_vents_array = np.array(list_vents)

# ---------- CALCUL RANGE REEL ---------- #

if parametres_init["moteur_avion"]:
    range_corrige = performence.range_moteur_reel(list_vents_array,SolutionAtterrissage.vecteur_angle)
    print(f'range corrigé : {range_corrige} [nm]')
else:
    range_corrige = performence.range_plane_reel(list_vents_array,SolutionAtterrissage.vecteur_angle)
    print(f'range corrigé : {range_corrige} [nm]')

# ---------- CALCUL RANGE AVEC VENT ---------- #

lons_reel,lats_reel = SolutionAtterrissage.cercle_range_reel(range_corrige,avion)

list_coordonnes_sur_cercle_reel = np.column_stack((lats_reel, lons_reel))
list_coordonnes_sur_cercle_reel = np.concatenate((list_coordonnes_sur_cercle_reel, np.column_stack((lats_reel[0], lons_reel[0]))))
print(f'list_coordonnes_sur_cercle_reel : {list_coordonnes_sur_cercle_reel}')

# ---------- CREATION DES AERODROMES DANS LA RANGE AVEC VENT ---------- #

aerodromes_in_range = []
for aerodrome in aerodromes:
    wn = SolutionAtterrissage.winding_number((aerodrome.latitude,aerodrome.longitude), list_coordonnes_sur_cercle_reel)
    if wn != 0:
        aerodromes_in_range.append(aerodrome)

lons_in_range = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range])
lats_in_range = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range])

aerodromes_in_range_right_size = []

for aerodrome in aerodromes_in_range:
    resultat,numero_pistes = SolutionAtterrissage.cherche_longueur_piste(aerodrome,parametres_init["dist_roulage_mini"])
    if resultat == True:
        aerodromes_in_range_right_size.append(aerodrome)

lons_in_range_in_size = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range_right_size])
lats_in_range_in_size = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range_right_size])

# ---------- AERODROME LE PLUS PROCHE ---------- #

distance = np.array(SolutionAtterrissage.calcul_entre_deux_coordonnees(coordonnees_avion,lats_in_range_in_size,lons_in_range_in_size))
if len(distance) != 0:
    min_value = np.min(distance)
    min_index = np.argmin(distance)
    lat_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].latitude
    lon_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].longitude
    new_cap = SolutionAtterrissage.calcul_new_cap(avion.latitude,avion.longitude,lat_aerodrome_plus_proche,lon_aerodrome_plus_proche)
    print(new_cap)
else:
    print("VOUS ETES DANS UNE SITUATION DELICATE ! :'(")

# ---------- AFFICHAGE DE LA CARTE FINALE ---------- #

SolutionAtterrissage.affichage_carte(aerodromes,avion,parametres_init,
                   lons,lats,
                   lons_in_range,lats_in_range,
                   lons_in_range_in_size,lats_in_range_in_size,
                   lons_reel,lats_reel,
                   lon_aerodrome_plus_proche,lat_aerodrome_plus_proche)