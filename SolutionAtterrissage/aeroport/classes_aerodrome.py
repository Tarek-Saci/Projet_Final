class Piste:
    """
    Cette classe permet de stocker les informations des pistes d'atterrissages.

    Args:
        longueur (string): La longueur de la piste

    Returns:
        0
    """
    def __init__(self,longueur):
        self.longeur = longueur

class Aerodrome:
    """
    Cette classe permet de créer un objet Aerodrome.

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
        0
    """
    def __init__(self,objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface, latitude, longitude, acces):
        self.id = objectid
        self.nom = nomcarto
        self.code = codeindic
        self.type = typeinfras
        self.nombre_piste = nbrpiste
        self.pistes = []

        longeur = []
        resultat_longeur = longpiste2.split("/")
        if len(resultat_longeur) < nbrpiste:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[0])
        elif len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                longeur.append(resultat_longeur[i])
        else:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[i])

        if len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                self.pistes.append(Piste(longeur[i]))
        else:
            for i in range(0,int(nbrpiste)):
                self.pistes.append(Piste(longeur[i]))

        self.latitude = latitude
        self.longitude = longitude
        self.acces = acces
