import numpy as np 

# --------------------------------------valeurs de test windy------------------------------------------

# test avec 8 points donc faire des liste de taille = nombre de cercle 
nombre_point_cercle = 8
vitesse_vent = np.random.uniform(0,100,nombre_point_cercle)  # homogène au reste de preference en [Kts]
direction_vent = np.random.uniform(0,360,nombre_point_cercle)  # Direction du vent en degrés

vents = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16]])


