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
       
        # Culoarea de fundal reținută (o transmitem la tab-ul PC Info ce folosește Canvas)
        self.bg_color = "#690B22"

        # Configurăm stilurile inițial
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
        """Configurează stilurile pentru 'dark' și 'light', cu paleta #690B22, #E07A5F, #F1E3D3, #1B4D3E."""

        # CULORI DE BAZĂ DIN IMAGINE:
        #  #690B22 (roșu închis)
        #  #E07A5F (portocaliu-somon)
        #  #F1E3D3 (crem deschis)
        #  #1B4D3E (verde închis)

        if theme == "light":
            # ------- LIGHT THEME -------
            bg       = "#F1E3D3"  # fundal crem deschis
            fg       = "#690B22"  # text roșu închis
            tab_bg   = "#E07A5F"  # tab normal
            tab_sel  = "#1B4D3E"  # tab selectat (verde închis)
            btn_bg   = "#1B4D3E"  # buton normal
            btn_hover= "#E07A5F"  # hover buton
            on_bg    = "#1B4D3E"  # ON (verde închis)
            off_bg   = "#E07A5F"  # OFF (portocaliu-somon)
        else:
            # ------- DARK THEME -------
            bg       = "#690B22"  # roșu închis
            fg       = "#F1E3D3"  # text crem deschis
            tab_bg   = "#1B4D3E"  # tab normal
            tab_sel  = "#E07A5F"  # tab selectat (portocaliu-somon)
            btn_bg   = "#E07A5F"  # buton normal
            btn_hover= "#F1E3D3"  # hover buton (crem)
            on_bg    = "#1B4D3E"  # ON (verde închis)
            off_bg   = "#F1E3D3"  # OFF (crem)

        # Salvăm culoarea de fundal în self.bg_color, pentru a o folosi la PC Info
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
                       foreground=[("selected", "#F1E3D3" if theme == "dark" else "#690B22")])

        # ===================================
        # Frame, Label, Labelframe
        # ===================================
        # "Custom.*"
        self.style.configure("Custom.TFrame", background=bg)
        self.style.configure("Custom.TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Custom.TLabelframe", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        self.style.configure("Custom.TLabelframe.Label", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        
        # "Green.*" – folosit de unele tab-uri (Green.TLabel, Green.TButton etc.)
        self.style.configure("Green.TFrame", background=bg)
        self.style.configure("Green.TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("Green.TLabelframe", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        self.style.configure("Green.TLabelframe.Label", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))

        # ===================================
        # Butoane
        # ===================================
        self.style.configure("Custom.TButton",
                             background=btn_bg,
                             foreground=fg if theme == "light" else "#F1E3D3",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("Custom.TButton",
                       background=[("active", btn_hover)])

        # "Green.TButton"
        self.style.configure("Green.TButton",
                             background=btn_bg,
                             foreground=fg if theme == "light" else "#F1E3D3",
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
                             foreground="#F1E3D3" if theme == "dark" else "#690B22",
                             font=("Arial", 10, "bold"),
                             padding=6)
        self.style.map("On.TButton",
                       background=[("active", btn_hover)])
        
        # Off.TButton
        self.style.configure("Off.TButton",
                             background=off_bg,
                             foreground="#690B22" if theme == "light" else "#690B22",
                             font=("Arial", 10, "bold"),
                             padding=6)
        self.style.map("Off.TButton",
                       background=[("active", btn_hover)])


if __name__ == "__main__":
    app = WindowsOptimizerApp()
    app.mainloop()
