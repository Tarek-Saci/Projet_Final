from shapely.geometry import LineString
import numpy as np

def calcul_coordonnees_vents_trajet(n,coordonnees_avion,latitude_point,longitude_point):
    """
    Cette fonction permet de trouver les coordonnées des points à l'intérieur du cercle "range".

    Args:
        n (int): nombre de points de discrétisation
        coordonnees_avion (tuple de float): coordonnées de l'avion (latitude et longitude)
        latitude_point (float): latitude du point étudié sur le cercle
        longitude_point (float): longitude du point étudié sur le cercle

    Returns:
        coordonnees_points_interieurs (liste de tuples de float): coordonnées des points de discrétisation
    """
    point1 = (coordonnees_avion[1], coordonnees_avion[0])
    point2 = (longitude_point, latitude_point)

    line = LineString([point1, point2])

    points_interieurs = [line.interpolate(i / (n + 1), normalized=True) for i in range(1, n + 1)]

    coordonnees_points_interieurs = [(point.y, point.x) for point in points_interieurs]

    return coordonnees_points_interieurs

def calcul_moyenne_vents_trajet(vents_a_moyenner):
    """
    Cette fonction permet de calculer la moyenne des vents sur le trajet potentiel

    Args:
        vents_a_moyenner (liste de tuples de float): liste des vents sur le trajet potentiel

    Returns:
        (moyenne_vent_x,moyenne_vent_y) (tuple de float) : vecteur vent moyen
    """
    moyenne_vent_x = np.mean(vents_a_moyenner[:,0])
    moyenne_vent_y = np.mean(vents_a_moyenner[:,1])

    return (moyenne_vent_x,moyenne_vent_y)


