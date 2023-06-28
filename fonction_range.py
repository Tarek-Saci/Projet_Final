
import numpy as np
import math
from Donnees import *

class GPS:
    def __init__(self, latitude, longitude, altitude, cap):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.cap = math.radians(cap)
        # Rayon de la Terre en mètres
        self.rayon_terre = 6371 * 1000  # En mètres

    def distance_entre_2_points(self, lat2, lon2):

        # Convertir les coordonnées degrés en radians
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Calcul des différences de latitude et de longitude
        diff_lat = lat2 - lat1
        diff_lon = lon2 - lon1

        # Calcul de la distance
        a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.rayon_terre * c * 0.001  # *1000 pour avoir des kilomètres

        return round(distance, 3)

class Performance:
    def __init__(self, finesse, vitesse, vitesse_plane, altitude, dist_roulage_mini, carburant_restant, moteur_avion):
        self.finesse = finesse
        self.vitesse = vitesse
        self.altitude = altitude
        self.dist_roulage_mini = dist_roulage_mini
        self.carburant = carburant_restant
        self.moteur_avion = moteur_avion
        self.vitesse_plane = vitesse_plane

    def range_plane_theorique(self):  # calcul du range
        range_theorique_plane = self.altitude * self.finesse / 6076.12  # on ne sait pas encore si on aura les altitudes des aerodromes
        return round(range_theorique_plane, 3)  # en [nm]

    def range_moteur_theorique(self):  # range = (gph / carburant restsant) * vitesse
        gph = self.conso_vitesse()
        range_theorique = (self.carburant / gph) * self.vitesse  # il vaut mieux utiliser les unités en Kts et nm pck generalement les données sont dans ces unitées
        return range_theorique

    def conso_vitesse(self):
        # --------de 0ft à 4000ft--------

        if self.altitude < 4000:
            gph = 0.00321894 * self.vitesse ** (2) - 0.470747 * self.vitesse + 20.9657

        # --------de 4000ft à 6000ft--------

        elif 4000 <= self.altitude < 6000:
            gph = 0.00153755 * self.vitesse ** (2) - 0.182342 * self.vitesse + 8.56135

        # --------de 6000ft à 8000ft--------

        elif 6000 <= self.altitude < 8000:
            gph = 0.00160782 * self.vitesse ** (2) - 0.205136 * self.vitesse + 9.88425

        # --------de 8000ft à 10000ft--------

        elif 8000 <= self.altitude < 10000:
            gph = 0.00168283 * self.vitesse ** (2) - 0.2278 * self.vitesse + 11.2253

        # --------de 10000ft à 12000ft--------

        elif 10000 <= self.altitude < 12000:
            gph = 0.00211899 * self.vitesse ** (2) - 0.320033 * self.vitesse + 15.9161

        # --------de 12000ft à 14000ft--------

        elif 12000 <= self.altitude:
            gph = 0.00101772 * self.vitesse ** (2) - 0.120151 * self.vitesse + 6.85233

        return round(gph, 3)  # en gallon par heure

    def angle_cap_vent(self, vecteur_vent, vecteur_theta):  # il faut essayer de vectoriser avec les tab numpy
        norme_vent = np.sqrt(vecteur_vent[:,0] ** 2 + vecteur_vent[:,1] ** 2)
        norme_theta = np.sqrt(vecteur_theta[:,0] ** 2 + vecteur_theta[:,1] ** 2)
        produit_scalaire = vecteur_vent[:,0] * vecteur_theta[:,0] + vecteur_vent[:,1] * vecteur_theta[:,1]
        angle_cap_vent_rad = np.arccos(produit_scalaire / (norme_vent * norme_theta))
        angle_cap_vent_deg = np.rad2deg(angle_cap_vent_rad)  # just au cas ou

        return angle_cap_vent_rad

    def range_plane_reel(self,vecteur_vent, vecteur_theta):  # apres vctorisation de angle_cap_vent il faut transformer angle_cap_vent_rad en self.
        vitesse_vent = np.sqrt(vecteur_vent[:,0] ** 2 + vecteur_vent[:,1] ** 2)
        angle_cap_vent_rad = self.angle_cap_vent(vecteur_vent, vecteur_theta)
        #print(f'angle cap vent rad : {angle_cap_vent_rad}')
        vitesse_sol = self.vitesse_plane + vitesse_vent * np.cos(angle_cap_vent_rad)  # il faut calculer le module du vecteur pour le remplacer dans vitese_vent
        #print('vitesse sol : ',vitesse_sol)
        temps_vol = self.range_plane_theorique() / self.vitesse_plane
        #print(f'temps vol : {temps_vol}')
        range_plane_reel = vitesse_sol * temps_vol
        return range_plane_reel

    def range_moteur_reel(self,vecteur_vent, vecteur_theta):  # apres vctorisation de angle_cap_vent il faut transformer angle_cap_vent_rad en self.
        angle_cap_vent_rad = self.angle_cap_vent(vecteur_vent , vecteur_theta)
        vitesse_vent = np.sqrt(vecteur_vent[:,0]**2 + vecteur_vent[:,1]**2 )
        vitesse_sol = self.vitesse + vitesse_vent * np.cos(angle_cap_vent_rad)  # il faut calculer le module du vecteur pour le remplacer dans vitese_vent
        temps_vol = self.carburant / self.conso_vitesse()

        range_moteur_reel = vitesse_sol * temps_vol
        return range_moteur_reel

