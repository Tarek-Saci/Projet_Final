import numpy as np 

# --------------------------------------valeurs de test windy------------------------------------------

# test avec 8 points donc faire des liste de taille = nombre de cercle 
nombre_point_cercle = 8
vitesse_vent = np.random.uniform(0,100,nombre_point_cercle)  # homogène au reste de preference en [Kts]
direction_vent = np.random.uniform(0,360,nombre_point_cercle)  # Direction du vent en degrés
hauteur_aerodrome = 423
