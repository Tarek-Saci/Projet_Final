# Importation des fichiers
import Donnees
from LectureYAML import LecteurYAML
from fonction_range import Performance
import numpy as np

#-----------lecture du fichier des paramètres d'entrée-----------#

# Création de l'objet YAML qui lit le fichier "deck.yamL"
parser = LecteurYAML('deck.yaml')
# Lecture du fichier avec la fonction read_yaml()
params = parser.read_yaml()
# On imprime le contenu qui a été lu
print("Données brutes\n:" + str(params) + "\n")
print("Types des données lues:\n" + str(type(params)) + "\n")
print(params["latitude"])

#-----------test de fonctions------------#

performence = Performance(params["finesse"],params["vitesse"],params["altitude"],params["dist_roulage_mini"],params["carburant_restant"],params["moteur_avion"])




if params["moteur_avion"]:
    range_theorique = performence.range_moteur()
    print(f'range avec moteurs : {range_theorique} [nm]')
    range_corrige = performence.correction_range(range_theorique,Donnees.vents)
    print(f'range corrigé : {range_corrige} [nm]')
else:
    range_theorique = performence.range_plane()
    print(f'range sans moteurs : {range_theorique} [nm]')
    range_corrige = performence.correction_range(range_theorique,Donnees.vents)
    print(f'range corrigé : {range_corrige} [nm]')




