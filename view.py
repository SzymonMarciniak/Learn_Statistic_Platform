import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


from controller import DataController

class Colors:
    BACKGROUND = "#333333"
    PANEL_BG = "#333333"
    BUTTON_BG = "#555555"
    BUTTON_FG = "white"
    TEXT_FG = "white"
    COMBOBOX_BG = "#555555"
    COMBOBOX_FG = "white"
    PLOT_BG = "#333333"
    PLOT_LINE_COLOR = "cyan"
    AXES_COLOR = "white"

class DataView:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiza danych - Statystyki opisowe")
        self.root.configure(bg=Colors.BACKGROUND)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state('zoomed')
        self.root.resizable(True, True)

        self.controller = DataController()

        self.descriptions = self.controller.model.load_descriptions()

        self.configure_styles()
        self.create_header()
        self.create_body_frame()
        self.create_footer()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=Colors.PANEL_BG)
        style.configure("TButton", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG, padding=5)
        style.configure("TLabel", background=Colors.PANEL_BG, foreground=Colors.TEXT_FG, font=("Helvetica", 12, "bold"))
        style.configure("TCombobox", fieldbackground=Colors.COMBOBOX_BG, foreground=Colors.COMBOBOX_FG, borderwidth=0)
        style.map("TCombobox", fieldbackground=[("readonly", Colors.COMBOBOX_BG)], selectbackground=[("readonly", Colors.COMBOBOX_BG)])
        style.configure("Treeview", background=Colors.PLOT_BG, foreground=Colors.TEXT_FG, fieldbackground=Colors.PLOT_BG)
        style.configure("Treeview.Heading", background=Colors.BUTTON_BG, foreground=Colors.BUTTON_FG, font=("Helvetica", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#4d4d4d"), ("selected", Colors.BUTTON_BG)], foreground=[("active", Colors.BUTTON_FG), ("selected", Colors.BUTTON_FG)])

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
        

    def create_header(self):
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)

        self.data_frame_selector = ttk.Combobox(self.header_frame, values=self.controller.get_csv_files(), state="readonly")
        self.combo2 = ttk.Combobox(self.header_frame, values=["Opcja A", "Opcja B", "Opcja C"], state="readonly")
        self.combo3 = ttk.Combobox(self.header_frame, values=["Parametr X", "Parametr Y", "Parametr Z"], state="readonly")

        self.data_frame_selector.set("titanic.csv")
        self.combo2.set("Wybierz opcję 2")
        self.combo3.set("Wybierz parametr")

        self.data_frame_selector.pack(side=tk.LEFT, padx=5)
        self.combo2.pack(side=tk.LEFT, padx=5)
        self.combo3.pack(side=tk.LEFT, padx=5)

        self.data_frame_selector.bind("<<ComboboxSelected>>", self.on_data_frame_selector_select)
        self.combo2.bind("<<ComboboxSelected>>", self.on_combo2_select)
        self.combo3.bind("<<ComboboxSelected>>", self.on_combo3_select)

    def on_data_frame_selector_select(self, event):
        self.table.destroy()
        self.table = ttk.Treeview(self.footer_content_frame, show="headings")
        self.table.grid(row=0, column=1, padx=10, pady=5) 

        self.controller.on_data_frame_selector_select(self.table, self.data_frame_selector.get())

    def on_combo2_select(self, event):
        self.controller.on_combo2_select(self.combo2.get())

    def on_combo3_select(self, event):
        self.controller.on_combo3_select(self.combo3.get())

    def create_body_frame(self):
        self.body_frame = ttk.Frame(self.root)
        self.body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.body_frame.grid_columnconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(1, weight=5)
        self.body_frame.grid_columnconfigure(2, weight=1)

        self.body_frame.grid_rowconfigure(0, weight=3)
        self.body_frame.grid_rowconfigure(1, weight=1)

        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.left_panel = ttk.Frame(self.body_frame, width=150)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(self.left_panel, text=" ", background=Colors.PANEL_BG).pack(pady=45)

        for name in self.descriptions.keys():
            self.add_measure_button(name)
    
    def add_measure_button(self, name):
        description = self.descriptions.get(name, "Brak opisu dla tej miary.")
        button = ttk.Button(self.left_panel, text=name, command=lambda: [self.update_description(name, description), self.update_chart()])
        button.pack(pady=5, fill=tk.X)  # Ustawienie przycisku na pełną szerokość panelu

    def create_center_panel(self):
        self.center_panel = ttk.Frame(self.body_frame)
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(self.center_panel, text=" ", background=Colors.PANEL_BG).pack(pady=20)

        self.fig, self.ax = plt.subplots(facecolor=Colors.PLOT_BG)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.center_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.configure_plot()

    def create_right_panel(self):
        self.right_panel = ttk.Frame(self.body_frame, width=200)  # Stała szerokość panelu
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.right_panel.grid_propagate(False)  # Wyłączenie automatycznego dostosowania

        ttk.Label(self.right_panel, text=" ", background=Colors.PANEL_BG).grid(row=0, sticky="n")

        self.description_label = ttk.Label(self.right_panel, text="Wybierz miarę, aby zobaczyć opis.", wraplength=180, justify=tk.LEFT)
        self.description_label.grid(row=1, sticky="nsew", padx=10, pady=10)
        self.right_panel.grid_rowconfigure(1, weight=2)  # Rozciąganie wiersza dla opisu

    def create_footer(self):
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(5, 20))

        self.footer_content_frame = ttk.Frame(self.footer_frame)
        self.footer_content_frame.pack(fill=tk.BOTH, expand=True)
        self.footer_content_frame.pack_propagate(False)  

        self.footer_content_frame.grid_columnconfigure(0, weight=1)  # Lewa pusta kolumna
        self.footer_content_frame.grid_columnconfigure(2, weight=1)  # Prawa pusta kolumna
        
        self.table = ttk.Treeview(self.footer_content_frame, show="headings")
        self.table.grid(row=0, column=1, padx=10, pady=5)  # Umieszczenie tabeli w środkowej kolumnie

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

        self.controller.update_table(self.table, "csvs/titanic.csv")  # Ścieżka do pliku .csv
    
    def update_description(self, option_name, new_text):
        label_width = self.description_label.winfo_width()
        label_height = self.description_label.winfo_height()
    
        self.description_label.config(text=new_text)

        self.description_label.update_idletasks()

    def configure_plot(self, title="Przykładowy wykres", xlabel="Oś X", ylabel="Oś Y"):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(Colors.PLOT_BG)
        self.ax.spines['bottom'].set_color(Colors.AXES_COLOR)
        self.ax.spines['left'].set_color(Colors.AXES_COLOR)
        self.ax.tick_params(axis='x', colors=Colors.AXES_COLOR)
        self.ax.tick_params(axis='y', colors=Colors.AXES_COLOR)
        self.ax.grid(color="gray", linestyle="--", linewidth=0.5)
        self.ax.set_title(title, color=Colors.TEXT_FG)
        self.ax.set_xlabel(xlabel, color=Colors.TEXT_FG)
        self.ax.set_ylabel(ylabel, color=Colors.TEXT_FG)

    def update_chart(self):
        self.configure_plot(title="Zaktualizowany wykres", xlabel="Nowa Oś X", ylabel="Nowa Oś Y")
        self.ax.plot([1, 2, 3], [4, 5, 6], color=Colors.PLOT_LINE_COLOR, label="Wykres")
        self.ax.legend(facecolor=Colors.PLOT_BG, labelcolor=Colors.TEXT_FG)
        self.canvas.draw()