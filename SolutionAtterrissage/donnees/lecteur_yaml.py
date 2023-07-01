import yaml
class LecteurYAML:
    """Défini un objet lecteur Yaml qui vient lire n'importe quel fichier yaml."""
    def __init__(self, file_path):
        """Initialise la classe en prenant en entrée un nom de fichier au format yaml"""
        self.file_path = file_path
    def read_yaml(self):
        """Méthode de la classe LecteurYAML.
        Argument en entrée:
        file path -- le nom (et chemin si nécessaire) du fichier à lire

        Return une variable de type dictionnaire qui contient les éléments du fichier yaml
        """
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")