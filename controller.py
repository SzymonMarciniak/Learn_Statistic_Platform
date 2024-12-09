import os
from model import DataModel

class DataController:
    def __init__(self):
        self.model = DataModel()

        self.csvs_folder = "csvs/"

    def update_table(self, table, file_path):
        df = self.model.load_data_from_csv(file_path)
        self.create_df(table, df)
        self.adjust_columns_width(table, df)

    def create_df(self, table, df):
    
        table["columns"] = list(df.columns)

        for col in df.columns:
            table.heading(col, text=col)
    
        # Usuwanie poprzednich danych wierszy
        for row in table.get_children():
            table.delete(row)
    
        # Dodawanie wierszy z pliku CSV do tabeli
        for _, row in df.iterrows():
            table.insert("", "end", values=list(row))
    
    def adjust_columns_width(self, table, df):
        for col in table["columns"]:
            max_width = max(len(str(value)) for value in df[col].astype(str))  # Najdłuższa wartość w kolumnie
            max_width = max(int(max_width*1.5), int(len(col)*1.25))  # Uwzględnienie długości nagłówka
            pixel_width = max_width * 8  # Przeliczanie na szerokość w pikselach (zakładając średnią szerokość 8 px na znak)
            pixel_width = pixel_width if pixel_width <= 240 else 240
            pixel_width = pixel_width if pixel_width >= 50 else 50
            table.column(col, width=pixel_width, anchor="center", stretch=False)  

    def on_data_frame_selector_select(self, table, data):
        print(f"Choosed: {data}")
        file_path = os.path.join(self.csvs_folder, data)
        self.update_table(table, file_path)

    def on_combo2_select(self, data):
        print(f"Wybrano: {data}")

    def on_combo3_select(self, data):
        print(f"Wybrano: {data}")

    def get_csv_files(self):
        return [f for f in os.listdir(self.csvs_folder) if f.endswith('.csv')]