import pandas as pd
import yaml

class DataModel:
    def __init__(self):
        self.df = None
        self.descriptions = self.load_descriptions()

    def load_data_from_csv(self, file_path):
        """Ładuje dane z pliku CSV przy użyciu Pandas i tworzy tabelę."""
        # Ładowanie danych z CSV do DataFrame
        return pd.read_csv(file_path)

    def load_descriptions(self):
        """Wczytuje opisy miar z pliku YAML."""
        with open("data/descriptions.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)