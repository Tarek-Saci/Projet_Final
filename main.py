# Importation des fichiers
import Donnees as data
from LectureYAML import LecteurYAML
from fonction_range import Performance

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

performence = Performance()


moteur_avion = False
if moteur_avion:
    range_theorique = performence.range_moteur()
    print(f'range avec moteurs : {range_theorique} [nm]')
    range_corrige = performence.correction_range()
    print(f'range corrigé : {range_corrige} [nm]')
else:
    range_theorique = performence.range_plane()
    print(f'range sans moteurs : {range_theorique} [nm]')
    range_corrige = performence.correction_range()
    print(f'range corrigé : {range_corrige} [nm]')




