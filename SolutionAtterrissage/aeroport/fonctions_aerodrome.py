import re
from .classes_aerodrome import Aerodrome

def creer_aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface,latitude, longitude, acces):
    return Aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                     surface,latitude, longitude, acces)
def cherche_longueur_piste(aerodrome,dist_roulage_mini):

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
