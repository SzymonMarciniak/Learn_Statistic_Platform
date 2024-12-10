import pandas as pd
import yaml

class DataModel:
    def __init__(self):
        self.df = None
        self.descriptions = self.load_descriptions()

    def load_data_from_csv(self, file_path):
        return pd.read_csv(file_path)

    def load_descriptions(self) -> dict:
        with open("data/descriptions.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
        
    def load_formulas_paths(self) -> dict:
        with open("data/math_formulas.yaml", "r", encoding="utf-8") as file:
            return yaml.safe_load(file)