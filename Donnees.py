import numpy as np 

# --------------------------------------valeurs de test windy------------------------------------------

# test avec 8 points donc faire des liste de taille = nombre de cercle 
nombre_points = 8
vitesse_vent = np.random.uniform(0,100,nombre_points)  # homogène au reste de preference en [Kts]
direction_vent = np.random.uniform(0,360,nombre_points)  # Direction du vent en degrés

vents = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16]])



theta = np.array([[1,0], [2*(2)**(0.5), 2*(2)**(0.5)], [0, 1], [-2*(2)**(0.5), 2*(2)**(0.5)], [-1, 0], [-2*(2)**(0.5),-2*(2)**(0.5)], [0, -1], [2*(2)**(0.5), -2*(2)**(0.5)]])
#il faut creer une fonction pour creer un nd.array a partir du nombre de points

