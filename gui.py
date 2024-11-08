import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=Colors.PANEL_BG)
        style.configure("TButton", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG, padding=5)
        style.configure("TLabel", background=Colors.PANEL_BG, foreground=Colors.TEXT_FG)
        style.configure("TCombobox", fieldbackground=Colors.COMBOBOX_BG, foreground=Colors.COMBOBOX_FG, borderwidth=0)
        style.map("TCombobox", fieldbackground=[("readonly", Colors.COMBOBOX_BG)], selectbackground=[("readonly", Colors.COMBOBOX_BG)])

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

        # Wywołanie funkcji tworzących panele
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()

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
        self.right_panel = ttk.Frame(self.body_frame, width=500)
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=0, pady=5)

        # Dodajemy pusty Label, aby przesunąć opis w dół
        ttk.Label(self.right_panel, text=" ", background=Colors.PANEL_BG).pack(pady=45)

        self.description_label = ttk.Label(self.right_panel, text="Wybierz miarę, aby zobaczyć opis.", wraplength=300, justify=tk.LEFT)
        self.description_label.pack(padx=0, pady=10)

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
