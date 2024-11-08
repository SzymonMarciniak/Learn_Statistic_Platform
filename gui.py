import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import yaml

# Klasa przechowująca kolory aplikacji
class Colors:
    BACKGROUND = "#333333"       # Kolor tła głównego
    PANEL_BG = "#333333"         # Kolor tła paneli
    BUTTON_BG = "#555555"        # Kolor tła przycisków
    BUTTON_FG = "white"          # Kolor tekstu na przyciskach
    TEXT_FG = "white"            # Kolor tekstu
    COMBOBOX_BG = "#555555"      # Kolor tła comboboxów
    COMBOBOX_FG = "white"        # Kolor tekstu comboboxów
    PLOT_BG = "#333333"          # Kolor tła wykresu
    PLOT_LINE_COLOR = "cyan"     # Kolor linii wykresów
    AXES_COLOR = "white"         # Kolor osi wykresu

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiza danych - Statystyki opisowe")
        self.root.configure(bg=Colors.BACKGROUND)

        # Ustawienia stylu (ciemny motyw)
        self.configure_styles()

        # Ładowanie opisów z pliku YAML
        self.load_descriptions()

        # Tworzenie nagłówka
        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)

        # Tworzenie list rozwijanych w nagłówku
        self.combo1 = ttk.Combobox(self.header_frame, values=["Opcja 1", "Opcja 2", "Opcja 3"], state="readonly")
        self.combo2 = ttk.Combobox(self.header_frame, values=["Opcja A", "Opcja B", "Opcja C"], state="readonly")
        self.combo3 = ttk.Combobox(self.header_frame, values=["Parametr X", "Parametr Y", "Parametr Z"], state="readonly")

        self.combo1.set("Wybierz opcję 1")
        self.combo2.set("Wybierz opcję 2")
        self.combo3.set("Wybierz parametr")

        self.combo1.pack(side=tk.LEFT, padx=5)
        self.combo2.pack(side=tk.LEFT, padx=5)
        self.combo3.pack(side=tk.LEFT, padx=5)

        # Tworzenie ciała aplikacji
        self.create_body_frame()

         # Tworzenie separatora między body a footerem
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=10)

        # Tworzenie stopki (footer)
        self.create_footer()

    def configure_styles(self):
        # Ustawienie stylu dla aplikacji
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=Colors.PANEL_BG)
        style.configure("TButton", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG, padding=5)
        style.configure("TLabel", background=Colors.PANEL_BG, foreground=Colors.TEXT_FG)
        style.configure("TCombobox", fieldbackground=Colors.COMBOBOX_BG, foreground=Colors.COMBOBOX_FG, borderwidth=0)
        style.map("TCombobox", fieldbackground=[("readonly", Colors.COMBOBOX_BG)], selectbackground=[("readonly", Colors.COMBOBOX_BG)])

        # Styl dla przycisków
        style.configure("TButton", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG)
        style.map("TButton",
                background=[("active", "#666666"), ("pressed", Colors.BUTTON_BG)],  # Subtelne podświetlenie
                foreground=[("active", Colors.BUTTON_FG), ("pressed", Colors.BUTTON_FG)])

        # Styl dla tabeli i nagłówków kolumn
        style.configure("Treeview", background=Colors.PLOT_BG, foreground=Colors.TEXT_FG, fieldbackground=Colors.PLOT_BG)
        style.configure("Treeview.Heading", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG, font=("Helvetica", 10, "bold"))
        style.map("Treeview.Heading",
                background=[("active", "#4d4d4d"), ("selected", Colors.BUTTON_BG)],  # Subtelne podświetlenie
                foreground=[("active", Colors.BUTTON_FG), ("selected", Colors.BUTTON_FG)])



    def load_descriptions(self):
        """Wczytuje opisy miar z pliku YAML."""
        with open("descriptions.yaml", "r", encoding="utf-8") as file:
            self.descriptions = yaml.safe_load(file)

    def add_measure_button(self, name):
        """Dodaje przycisk miary i przypisuje do niego opis z pliku YAML."""
        description = self.descriptions.get(name, "Brak opisu dla tej miary.")
        button = ttk.Button(self.left_panel, text=name, command=lambda: [self.update_description(description), self.update_chart()])
        button.pack(pady=5, fill=tk.X)  # Ustawienie przycisku na pełną szerokość panelu


    def create_body_frame(self):
        self.body_frame = ttk.Frame(self.root)
        self.body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Ustawienie proporcji dla kolumn
        self.body_frame.grid_columnconfigure(0, weight=1)  # Lewy panel (20%)
        self.body_frame.grid_columnconfigure(1, weight=5)  # Środkowy panel (60%)
        self.body_frame.grid_columnconfigure(2, weight=1)  # Prawy panel (20%)

        self.body_frame.grid_rowconfigure(0, weight=3)  # Główny wiersz z wykresem
        self.body_frame.grid_rowconfigure(1, weight=1)  # Footer

        # Wywołanie funkcji tworzących panele
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()

    def load_data_from_csv(self, file_path):
        """Ładuje dane z pliku CSV przy użyciu Pandas i tworzy tabelę."""
        # Ładowanie danych z CSV do DataFrame
        self.df = pd.read_csv(file_path)

        # Usuwanie poprzednich danych z tabeli
        for col in self.table["columns"]:
            self.table.heading(col, text="")

        # Ustawianie nowych kolumn
        self.table["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.table.heading(col, text=col)

        # Usuwanie poprzednich danych wierszy
        for row in self.table.get_children():
            self.table.delete(row)

        # Dodawanie wierszy z pliku CSV do tabeli
        for _, row in self.df.iterrows():
            self.table.insert("", "end", values=list(row))


    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.body_frame, width=150)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Dodajemy pusty Label, aby przesunąć przyciski w dół
        ttk.Label(self.left_panel, text=" ", background=Colors.PANEL_BG).pack(pady=45)

        # Tworzenie przycisków na podstawie kluczy z pliku YAML
        for name in self.descriptions.keys():
            self.add_measure_button(name)

    def create_center_panel(self):
        self.center_panel = ttk.Frame(self.body_frame)
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(self.center_panel, text=" ", background=Colors.PANEL_BG).pack(pady=20)

        # Konfiguracja wykresu
        self.fig, self.ax = plt.subplots(facecolor=Colors.PLOT_BG)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.center_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.configure_plot()

    def create_right_panel(self):
        # Tworzenie prawego panelu o stałej szerokości
        self.right_panel = ttk.Frame(self.body_frame, width=200)  # Stała szerokość panelu
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.right_panel.grid_propagate(False)  # Wyłączenie automatycznego dostosowania

        # Dodajemy pusty Label, aby przesunąć opis w dół
        ttk.Label(self.right_panel, text=" ", background=Colors.PANEL_BG).grid(row=0, sticky="n")

        # Etykieta dla opisu z wraplength, aby zapobiec zmianom szerokości
        self.description_label = ttk.Label(self.right_panel, text="Wybierz miarę, aby zobaczyć opis.", wraplength=180, justify=tk.LEFT)
        self.description_label.grid(row=1, sticky="nsew", padx=10, pady=10)
        self.right_panel.grid_rowconfigure(1, weight=1)  # Rozciąganie wiersza dla opisu


    def create_footer(self):
        # Tworzenie kontenera dla stopki
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(5, 20))

        footer_content_frame = ttk.Frame(self.footer_frame)
        footer_content_frame.pack(fill=tk.BOTH, expand=True)

        # Konfiguracja kolumn siatki w `footer_content_frame`, aby tabela była wyśrodkowana
        footer_content_frame.grid_columnconfigure(0, weight=1)  # Lewa pusta kolumna
        footer_content_frame.grid_columnconfigure(2, weight=1)  # Prawa pusta kolumna

        # Tworzenie dynamicznej tabeli Treeview dla danych CSV
        self.table = ttk.Treeview(footer_content_frame, show="headings")
        self.table.grid(row=0, column=1, padx=10, pady=5)  # Umieszczenie tabeli w środkowej kolumnie

        # Stylizacja tabeli, aby pasowała do ciemnego motywu
        style = ttk.Style()
        style.configure("Treeview", 
                        background=Colors.PLOT_BG, 
                        foreground=Colors.TEXT_FG, 
                        fieldbackground=Colors.PLOT_BG)
        style.configure("Treeview.Heading", 
                        background=Colors.BUTTON_BG, 
                        foreground=Colors.BUTTON_FG, 
                        font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", "gray")])  # Kolor zaznaczenia wiersza

        # Przykładowe wywołanie załadowania danych z CSV
        self.load_data_from_csv("data.csv")  # Ścieżka do pliku .csv


    def update_description(self, text):
        self.description_label.config(text=text)

    def configure_plot(self, title="Przykładowy wykres", xlabel="Oś X", ylabel="Oś Y"):
        """Konfiguruje wykres z odpowiednimi ustawieniami kolorów i stylów."""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(Colors.PLOT_BG)  # Tło wykresu
        self.ax.spines['bottom'].set_color(Colors.AXES_COLOR)
        self.ax.spines['left'].set_color(Colors.AXES_COLOR)
        self.ax.tick_params(axis='x', colors=Colors.AXES_COLOR)
        self.ax.tick_params(axis='y', colors=Colors.AXES_COLOR)
        self.ax.grid(color="gray", linestyle="--", linewidth=0.5)  # Siatka w kolorze szarym

        # Ustawienia tytułu i etykiet z odpowiednimi kolorami
        self.ax.set_title(title, color=Colors.TEXT_FG)
        self.ax.set_xlabel(xlabel, color=Colors.TEXT_FG)
        self.ax.set_ylabel(ylabel, color=Colors.TEXT_FG)

    def update_chart(self):
        self.configure_plot(title="Zaktualizowany wykres", xlabel="Nowa Oś X", ylabel="Nowa Oś Y")
        # Ustalony kolor linii wykresu
        self.ax.plot([1, 2, 3], [4, 5, 6], color=Colors.PLOT_LINE_COLOR, label="Wykres")

        self.ax.legend(facecolor=Colors.PLOT_BG, labelcolor=Colors.TEXT_FG)
        self.canvas.draw()


# Uruchomienie aplikacji
root = tk.Tk()
app = DataAnalysisApp(root)
root.mainloop()
