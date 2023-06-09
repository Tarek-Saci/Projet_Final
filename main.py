from fonctions import *
from deck import *

#moteur_avion = False
if moteur_avion:
    range_theorique = range_moteur(vitesse_avion,carburant_restant)
    print(f'range avec moteurs : {range_theorique} [nm]')
    range_corrige = correction_range(range_theorique,vitesse_avion,vitesse_vent,direction_vent)
    print(f'range corrigé : {range_corrige} [nm]')
else:
    range_theorique = range_plane(finesse,altitude_avion,hauteur_aerodrome)
    print(f'range sans moteurs : {range_theorique} [nm]')
    range_corrige = correction_range(range_theorique,vitesse_avion,vitesse_vent,direction_vent)
    print(f'range corrigé : {range_corrige} [nm]')
