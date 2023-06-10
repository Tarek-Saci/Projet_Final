# Importation des fichiers
import Donnees as data
from LectureYAML import LecteurYAML
from fonction_range import GPS as gps
from fonction_range import Performance as pf


#-----------lecture du fichier des paramètres d'entrée-----------#

# Création de l'objet YAML qui lit le fichier "deck.yamL"
parser = LecteurYAML('deck.yaml')
# Lecture du fichier avec la fonction read_yaml()
parametres_init = parser.read_yaml()
# On imprime le contenu qui a été lu
print("Données brutes\n:" + str(parametres_init) + "\n")
print("Types des données lues:\n" + str(type(parametres_init)) + "\n")
print(parametres_init["position"]["latitude"])

#----------test des fonctions avec les donnees du YAML---------#
gps = gps(parametres_init["position"]["latitude"],parametres_init["position"]["longitude"], parametres_init["position"]["altitude"], parametres_init["cap"])
distance_aero = gps.distance_entre_2_points(50.6,60.84)
print(distance_aero)

perf_avion = pf(parametres_init["finesse"],parametres_init["vitesse"],parametres_init["dist_roulage_mini"],parametres_init["carburant_restant"],parametres_init["probleme_moteur"])
range = perf_avion.range_plane(parametres_init["position"]["altitude"],data.hauteur_aerodrome)
print(range)
