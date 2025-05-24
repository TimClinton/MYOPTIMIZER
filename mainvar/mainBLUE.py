import tkinter as tk
from tkinter import ttk

# Importăm toate tab-urile existente
from tabs.pc_info_tab import PCInfoTab
from tabs.restore_tab import RestoreTab
from tabs.reduce_services_tab import ReduceServicesTab
from tabs.windows_settings_tab import WindowsSettingsTab
from tabs.gpu_tab import GPUTab
from tabs.reg_tweaks_tab import RegTweaksTab
from tabs.cleanup_tab import CleanupTab

class WindowsOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🛠️ Windows Optimizer")
        self.geometry("1000x650")

        # Stabilim tema curentă (dark vs light)
        self.current_theme = "dark"
        
        # Inițializăm Style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Bază pentru stil
       
        # Culoarea de fundal reținută (o transmitem tab-urilor care folosesc Canvas)
        self.bg_color = "#3E3F5B"

        # Apelăm setup_styles pentru a configura culorile, fonturile etc.
        self.setup_styles(self.current_theme)

        # HEADER (cadru cu titlul aplicației și butonul de schimbare a temei)
        header = ttk.Frame(self, style="Custom.TFrame")
        header.pack(fill="x")

        title_label = ttk.Label(
            header,
            text="🛠️ Windows Optimizer",
            style="Custom.TLabel",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(side="left", padx=10, pady=10)

        theme_btn = ttk.Button(
            header,
            text="🌓 Schimbă tema",
            command=self.toggle_theme,
            style="Custom.TButton"
        )
        theme_btn.pack(side="right", padx=10, pady=10)

        # MAIN FRAME
        main_frame = ttk.Frame(self, style="Custom.TFrame")
        main_frame.pack(expand=True, fill="both")

        # NOTEBOOK (tab-uri)
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Instanțiem tab-urile noastre
        self.tabs = {
            "PC Info": PCInfoTab(self.notebook, style="Custom.TFrame", canvas_bg=self.bg_color),
            "Restore Point": RestoreTab(self.notebook, style="Custom.TFrame"),
            "Reduce Services": ReduceServicesTab(self.notebook, style="Custom.TFrame"),
            "Windows Settings": WindowsSettingsTab(self.notebook, style="Custom.TFrame"),
            "GPU": GPUTab(self.notebook, style="Custom.TFrame"),
            "Reg Tweaks": RegTweaksTab(self.notebook, style="Custom.TFrame"),
            "Cleanup": CleanupTab(self.notebook, style="Custom.TFrame")
        }

        # Adăugăm fiecare tab în notebook
        for name, tab in self.tabs.items():
            self.notebook.add(tab, text=name)

    def toggle_theme(self):
        # Alternează între 'light' și 'dark'
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.setup_styles(self.current_theme)

        # Actualizăm și fundalul tab-ului PC Info (dacă folosește canvas_bg).
        self.tabs["PC Info"].update_canvas_bg(self.bg_color)

    def setup_styles(self, theme):
        """Configurează stilurile pentru 'dark' și 'light', bazate pe paleta de culori din imagine."""
        
        # Paletă din imagine:
        #   #F6F1DE (un crem foarte deschis)
        #   #3E3F5B (un navy/gri închis)
        #   #8AB2A6 (verde-gri deschis)
        #   #ACD3A8 (verde pal)
        
        if theme == "light":
            # ------- LIGHT THEME -------
            bg       = "#F6F1DE"  # fundal foarte deschis
            fg       = "#3E3F5B"  # text închis
            tab_bg   = "#ACD3A8"  # fundal normal al tab-urilor
            tab_sel  = "#8AB2A6"  # fundal tab selectat
            btn_bg   = "#8AB2A6"  # buton normal
            btn_hover= "#ACD3A8"  # hover
            on_bg    = "#8AB2A6"  # ON
            off_bg   = "#3E3F5B"  # OFF (contrast mai mare)
        else:
            # ------- DARK THEME -------
            bg       = "#3E3F5B"  # fundal închis (navy/gri)
            fg       = "#F6F1DE"  # text deschis
            tab_bg   = "#8AB2A6"  # tab normal
            tab_sel  = "#ACD3A8"  # tab selectat
            btn_bg   = "#8AB2A6"  # buton
            btn_hover= "#ACD3A8"  # hover
            on_bg    = "#8AB2A6"  # ON
            off_bg   = "#F6F1DE"  # OFF (pentru contrast)
        
        # Salvăm culoarea de fundal în self.bg_color, pentru a o folosi la tab-ul PC Info
        self.bg_color = bg

        # Setăm fundalul principal al ferestrei
        self.configure(bg=bg)
        
        # ===================================
        # Notebook & Tabs
        # ===================================
        self.style.configure("Custom.TNotebook", background=bg, borderwidth=0)
        self.style.configure("Custom.TNotebook.Tab",
                             background=tab_bg,
                             foreground=fg,
                             padding=[12, 8],
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Custom.TNotebook.Tab",
                       background=[("selected", tab_sel)],
                       foreground=[("selected", bg)])  # la selectare, textul devine în culoarea de fundal principal (sau #F6F1DE) – poți ajusta

        # ===================================
        # Frame, Label, Labelframe
        # ===================================
        # "Custom.*"
        self.style.configure("Custom.TFrame", background=bg)
        self.style.configure("Custom.TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Custom.TLabelframe", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        self.style.configure("Custom.TLabelframe.Label", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        
        # "Green.*" – unele tab-uri folosesc "Green.TLabel", "Green.TButton", etc.
        self.style.configure("Green.TFrame", background=bg)
        self.style.configure("Green.TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Green.TLabelframe", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        self.style.configure("Green.TLabelframe.Label", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))

        # ===================================
        # Butoane
        # ===================================
        self.style.configure("Custom.TButton",
                             background=btn_bg,
                             foreground=fg if theme == "light" else "#F6F1DE",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("Custom.TButton",
                       background=[("active", btn_hover)])

        # "Green.TButton" – unii itemi folosesc explicit acest stil
        self.style.configure("Green.TButton",
                             background=btn_bg,
                             foreground=fg if theme == "light" else "#F6F1DE",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("Green.TButton",
                       background=[("active", btn_hover)])

        # ===================================
        # Butoane ON / OFF (folosite la toggle)
        # ===================================
        # On.TButton
        self.style.configure("On.TButton",
                             background=on_bg,
                             foreground="#F6F1DE" if theme == "dark" else "#3E3F5B",
                             font=("Arial", 10, "bold"),
                             padding=6)
        self.style.map("On.TButton",
                       background=[("active", btn_hover)])
        
        # Off.TButton
        self.style.configure("Off.TButton",
                             background=off_bg,
                             foreground="#F6F1DE" if theme == "dark" else "#3E3F5B",
                             font=("Arial", 10, "bold"),
                             padding=6)
        self.style.map("Off.TButton",
                       background=[("active", btn_hover)])


if __name__ == "__main__":
    app = WindowsOptimizerApp()
    app.mainloop()
