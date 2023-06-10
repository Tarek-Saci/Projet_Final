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