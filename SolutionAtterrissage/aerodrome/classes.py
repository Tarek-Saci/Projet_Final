import yaml
class LecteurYAML:

    def __init__(self, file_path):
        self.file_path = file_path
    def read_yaml(self):
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")
class Avion:
    def __init__(self,coordonnees_avion,range_avion):
        self.latitude = coordonnees_avion[0]
        self.longitude = coordonnees_avion[1]
        self.range_theorique_avion = range_avion
class Piste:
    def __init__(self,longeur):
        self.longeur = longeur
        #self.surface = surface
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
        if len(resultat_longeur) < nbrpiste:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[0])
        elif len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                print(i)
                longeur.append(resultat_longeur[i])
        else:
            for i in range(0, int(nbrpiste)):
                longeur.append(resultat_longeur[i])
        """surface_liste = []
        resultat_surface = surface.split(",")
        if len(resultat_surface) != nbrpiste:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface)
        else:
            for i in range(0, int(nbrpiste)):
                surface_liste.append(resultat_surface[i])"""

        if len(resultat_longeur) > nbrpiste:
            for i in range(0, len(resultat_longeur)):
                self.pistes.append(Piste(longeur[i]))
        else:
            for i in range(0,int(nbrpiste)):
                self.pistes.append(Piste(longeur[i]))

        self.latitude = latitude
        self.longitude = longitude
        self.acces = acces
def creer_aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                    surface,latitude, longitude, acces):
    return Aerodrome(objectid, nomcarto, codeindic, typeinfras, nbrpiste,longpiste2,
                     surface,latitude, longitude, acces)