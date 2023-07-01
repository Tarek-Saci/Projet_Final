import numpy as np 

nombre_points = 30
discretisation = 2
nombre_segments = nombre_points+1
vitesse_vent = np.random.uniform(0,100,nombre_points)  # homogène au reste de preference en [Kts]
direction_vent = np.random.uniform(0,360,nombre_points)  # Direction du vent en degrés

angles = np.linspace(0, 2 * np.pi, nombre_segments)
angles_points = angles[:-1]
x = np.cos(angles_points)
y = np.sin(angles_points)
vecteur_angle = np.column_stack((x, y))

