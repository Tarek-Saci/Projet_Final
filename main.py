
import pandas as pd
import numpy as np
import fonctions as fc
import classes

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

vecteur_creer_aerodrome = np.vectorize(classes.creer_aerodrome)

aerodromes = vecteur_creer_aerodrome(objectid_array, nomcarto_array, codeindic_array,
                                     typeinfras_array, nbrpiste_array, longpiste2_array,
                                     surface_array, latitude_array, longitude_array, acces_array)

coordonnees_avion = (49.603934,-75.402508)

range_avion = 260

avion = classes.Avion(coordonnees_avion,range_avion)

coordonnes_sur_cercle,lons,lats = fc.cercle_range(range_avion,avion)

list_coordonnes_sur_cercle = list(coordonnes_sur_cercle)
distance = []

for coordonnee in list_coordonnes_sur_cercle:
    distance.append(fc.calcul_entre_deux_coordonnees(coordonnee, coordonnees_avion))

aerodromes_in_range = []

for aerodrome in aerodromes:
    wn = fc.winding_number((aerodrome.latitude,aerodrome.longitude), list_coordonnes_sur_cercle)
    if wn != 0:
        aerodromes_in_range.append(aerodrome)

lons_in_range = np.array([aerodrome.longitude for aerodrome in aerodromes_in_range])
lats_in_range = np.array([aerodrome.latitude for aerodrome in aerodromes_in_range])

fc.affichage_carte(aerodromes,avion,lons,lats,lons_in_range,lats_in_range)

