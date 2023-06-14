import pandas as pd
import numpy as np
import fonctions as fc
import classes

# ---------- YAML ---------- #

# Création de l'objet YAML qui lit le fichier "deck.yamL"
parser = classes.LecteurYAML('deck.yaml')
# Lecture du fichier avec la fonction read_yaml()
parametres_init = parser.read_yaml()

# ---------- INFORMATIONS AEROPORT.CSV ---------- #

df = pd.read_csv("C:\\Users\\natha\\PycharmProjects\\test_cartopy\\Aeroport.csv")
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

vecteur_creer_aerodrome = np.vectorize(classes.creer_aerodrome)

aerodromes = vecteur_creer_aerodrome(objectid_array, nomcarto_array, codeindic_array,
                                     typeinfras_array, nbrpiste_array, longpiste2_array,
                                     surface_array, latitude_array, longitude_array, acces_array)

# ---------- CALCUL RANGE THEORIQUE ---------- #

range_theorique_avion = 400

# ---------- CREATION DE L'AVION ---------- #

coordonnees_avion = (parametres_init["latitude"],parametres_init["longitude"])
avion = classes.Avion(coordonnees_avion,range_theorique_avion)

coordonnes_sur_cercle,lons,lats = fc.cercle_range(range_theorique_avion,avion)

list_coordonnes_sur_cercle = list(coordonnes_sur_cercle)

#print(list_coordonnes_sur_cercle)

# ---------- CREATION DES VENTS DES POINTS DU CERCLE ---------- #

list_vents = []

for point in list_coordonnes_sur_cercle:
    list_vents.append(fc.calcul_vent(point[0],point[1],parametres_init["altitude"]))

#print(f'Vents : {list_vents}')

# ---------- CALCUL RANGE AVEC VENT ---------- #

# ---------- CREATION DES AERODROMES DANS LA RANGE AVEC VENT ---------- #

aerodromes_in_range = []

for aerodrome in aerodromes:
    wn = fc.winding_number((aerodrome.latitude,aerodrome.longitude), list_coordonnes_sur_cercle)
    if wn != 0:
        aerodromes_in_range.append(aerodrome)

lons_in_range = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range])
lats_in_range = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range])

aerodromes_in_range_right_size = []

for aerodrome in aerodromes_in_range:
    resultat,numero_pistes = fc.cherche_longueur_piste(aerodrome,parametres_init["dist_roulage_mini"])
    if resultat == True:
        aerodromes_in_range_right_size.append(aerodrome)

lons_in_range_in_size = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range_right_size])
lats_in_range_in_size = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range_right_size])

# ---------- AERODROME LE PLUS PROCHE ---------- #

distance = np.array(fc.calcul_entre_deux_coordonnees(coordonnees_avion,lats_in_range_in_size,lons_in_range_in_size))
print(distance)
print(len(aerodromes_in_range_right_size))

min_value = np.min(distance)
min_index = np.argmin(distance)

print("Valeur minimale :", min_value)
print("Indice correspondant :", min_index)

lat_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].latitude

lon_aerodrome_plus_proche = aerodromes_in_range_right_size[min_index].longitude

# ---------- CAP AEROPORT LE PLUS PROCHE ---------- #

new_cap = fc.calcul_new_cap(avion.latitude,avion.longitude,lat_aerodrome_plus_proche,lon_aerodrome_plus_proche)

print(new_cap)

# ---------- AFFICHAGE DE LA CARTE FINALE ---------- #

fc.affichage_carte(aerodromes,avion,lons,lats,lons_in_range,lats_in_range,lons_in_range_in_size,lats_in_range_in_size)