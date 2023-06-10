
class Avion:
    def __init__(self,coordonnees_avion,range_avion):
        self.latitude = coordonnees_avion[0]
        self.longitude = coordonnees_avion[1]
        self.range_avion = range_avion
class Piste:
    def __init__(self,longeur,surface):
        self.longeur = longeur
        self.surface = surface
class Aerodrome:
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
        if len(resultat_longeur) != nbrpiste:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur)
        else:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[i])
        surface_liste = []
        resultat_surface = surface.split(",")
        if len(resultat_surface) != nbrpiste:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface)
        else:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface[i])
        for i in range(0,int(nbrpiste)):
            self.pistes.append(Piste(longeur[i],surface_liste[i]))

        self.latitude = latitude
        self.longitude = longitude
        self.acces = acces

def creer_aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface,latitude, longitude, acces):
    return Aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                     surface,latitude, longitude, acces)