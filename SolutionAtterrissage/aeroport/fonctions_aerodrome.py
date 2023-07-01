import re
from .classes_aerodrome import Aerodrome

def creer_aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface,latitude, longitude, acces):
    """
    Cette fonction permet de créer un aérodrome de type Aerodrome.

    Args:
        objectid (string): Le numéro de l'aérodrome dans la liste
        nomcarto (string): Le nom de l'aérodrome
        codeindic (string): Le code de l'aérodrome
        typeinfras (string): Le type (aéroport ou aérodrome) d'infrastructure
        nbrpiste (string): Le nombre de piste que possède l'aérodrome
        longpiste2 (string): Les longueurs des pistes de l'aérodrome
        surface (string): Les surface des pistes
        latitude (string): La latitude de l'aérodrome
        longitude (string): La longitude de l'aérodrome
        acces (string): Le type d'accès

    Returns:
        Aerodrome (Aerodrome): L'aérodrome à créer par le constructeur de la classe
    """
    return Aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                     surface,latitude, longitude, acces)
def cherche_longueur_piste(aerodrome,dist_roulage_mini):
    """
    Cette fonction permet de savoir si un aérodrome dans la range possède une piste suffisamment longue.

    Args:
        aerodrome (Aerodrome): L'aérodrome dans la range à vérifier
        dist_roulage_mini (int): La distance minimum de la piste sur laquelle peut atterrir l'avion

    Returns:
        resultat (boolean): Le boolean qui vérifie si la piste de l'aérodrome est suffisamment longue
        numero_pistes (liste de piste): Les pistes qui sont suffisamment longues
    """
    numero_pistes = []
    resultat = False

    for i in range(0,len(aerodrome.pistes)):
        chiffres = re.findall(r'\d+', aerodrome.pistes[i].longeur)
        chiffres_concatenes = ''.join(chiffres)
        nombre = int(chiffres_concatenes)
        if nombre > dist_roulage_mini:
            resultat = True
            numero_pistes.append(i)

    return  resultat,numero_pistes
