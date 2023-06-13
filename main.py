# Importation des fichiers
import Donnees as data
from LectureYAML import LecteurYAML
from fonction_range import *

#-----------lecture du fichier des paramètres d'entrée-----------#

# Création de l'objet YAML qui lit le fichier "deck.yamL"
parser = LecteurYAML('deck.yaml')
# Lecture du fichier avec la fonction read_yaml()
parametres_init = parser.read_yaml()
# On imprime le contenu qui a été lu
print("Données brutes\n:" + str(parametres_init) + "\n")
print("Types des données lues:\n" + str(type(parametres_init)) + "\n")
print(parametres_init["position"]["latitude"])

#-----------test de fonctions------------#

moteur_avion = False
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




