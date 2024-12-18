import tkinter as tk
from tkinter import PhotoImage, ttk
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
        self.math_formulas_paths = self.controller.model.load_formulas_paths()

        self.configure_styles()
        self.create_menu()
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

        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        self.comboboxs_left_frame = ttk.Frame(self.header_frame)
        self.comboboxs_left_frame.grid(row=0, column=0, columnspan=1, sticky="w", pady=(5, 10)) 
        
        self.comboboxs_center_frame = ttk.Frame(self.header_frame)
        self.comboboxs_center_frame.grid(row=0, column=1, columnspan=1, sticky="w", pady=(5, 10)) 

        combobox_font = ("Helvetica", 10)
        label_font = ("Helvetica", 12, "bold")

        # Etykieta i lista dla wyboru pliku
        self.label_data_frame = ttk.Label(self.comboboxs_left_frame, text="Wybierz plik:", font=label_font)
        self.label_data_frame.grid(row=0, column=0, padx=15, pady=(0, 5), sticky="w") 
        self.data_frame_selector = ttk.Combobox(self.comboboxs_left_frame, values=self.controller.get_csv_files(), state="readonly", font=combobox_font)
        self.data_frame_selector.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")

        # Etykieta i lista dla opcji
        self.label_combo2 = ttk.Label(self.comboboxs_center_frame, text="Wybierz opcję:", font=label_font)
        self.label_combo2.grid(row=0, column=0, padx=15, pady=(0, 5), sticky="n")
        self.combo2 = ttk.Combobox(self.comboboxs_center_frame, values=["Opcja A", "Opcja B", "Opcja C"], state="readonly", font=combobox_font)
        self.combo2.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")

        # Etykieta i lista dla parametrów
        self.label_combo3 = ttk.Label(self.comboboxs_center_frame, text="Wybierz parametr:", font=label_font)
        self.label_combo3.grid(row=0, column=1, padx=15, pady=(0, 5), sticky="n")
        self.combo3 = ttk.Combobox(self.comboboxs_center_frame, values=["Parametr X", "Parametr Y", "Parametr Z"], state="readonly", font=combobox_font)
        self.combo3.grid(row=1, column=1, padx=15, pady=(0, 10), sticky="ew")

        self.data_frame_selector.set("titanic.csv")
        self.combo2.set("Wybierz opcję 2")
        self.combo3.set("Wybierz parametr")

        self.data_frame_selector.bind("<<ComboboxSelected>>", self.on_data_frame_selector_select)
        self.combo2.bind("<<ComboboxSelected>>", self.on_combo2_select)
        self.combo3.bind("<<ComboboxSelected>>", self.on_combo3_select)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        # file_menu.add_command(label="Nowy", command=self.new_file)
        # file_menu.add_command(label="Otwórz", command=self.open_file)
        # file_menu.add_command(label="Zapisz", command=self.save_file)
        # file_menu.add_separator()
        file_menu.add_command(label="Wyjdź", command=self.exit_app)
        menu_bar.add_cascade(label=" Plik   ", menu=file_menu)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Brak   ", command=self.open_preferences)
        menu_bar.add_cascade(label="   Opcje   ", menu=options_menu)

        contact_menu = tk.Menu(menu_bar, tearoff=0)
        contact_menu.add_command(label="Kontakt", command=self.about_app)
        contact_menu.add_command(label="Pomoc", command=self.help)
        menu_bar.add_cascade(label="   Kontakt   ", menu=contact_menu)

    def new_file(self):
        print("Nowy plik został utworzony.")

    def open_file(self):
        print("Otwórz plik został wybrany.")

    def save_file(self):
        print("Zapisz plik został wybrany.")

    def exit_app(self):
        self.root.quit()

    def open_preferences(self):
        print("Preferencje zostały otwarte.")

    def about_app(self):
        print("Informacje o aplikacji.")

    def help(self):
        print("Pomoc została otwarta.")

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
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=(5,0), pady=5)
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

        self.description_label = ttk.Label(self.right_panel, text="Wybierz miarę, aby zobaczyć opis.", wraplength=300, justify=tk.LEFT, compound="bottom")
        self.description_label.grid(row=1, sticky="nswe", padx=(0,10), pady=10)
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
        self.remove_image()

        text_header = f"{option_name.upper()}\n\n"
        text_body = f"{new_text}\n"
        upper_text = f"{text_header}{text_body}"
        self.description_label.config(text=upper_text)

        formula_path = self.math_formulas_paths.get(option_name, None)
        if formula_path:
            self.formula_image = PhotoImage(file=formula_path)
            self.description_label.config(image=self.formula_image)




        self.description_label.update_idletasks()

    def remove_image(self):
        if hasattr(self, 'formula_image') and self.formula_image is not None:
            self.description_label.config(image="")  # Usunięcie obrazu
            self.formula_image = None  # Usunięcie referencji do obrazu

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