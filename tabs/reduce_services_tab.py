import customtkinter as ctk
import subprocess
import os
from tkinter import messagebox

class ReduceServicesTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Optimizare servicii Windows",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Închide servicii inutile pentru a elibera resurse și a grăbi încărcarea "
                "sistemului de operare.\nApasă pe butonul de mai jos pentru a rula "
                "scriptul automat (reduce_services.bat)."
            ),
            wraplength=500  # optional, pentru text mai lung
        )
        desc_label.pack(padx=10, pady=5)

        # Cadru pentru butoane
        buttons_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        buttons_frame.pack(pady=10)

        # Butonul principal – rulează reduce_services.bat
        run_btn = ctk.CTkButton(
            buttons_frame,
            text="Rulează reduce_services.bat",
            command=self.run_bat_file
        )
        run_btn.pack(padx=10, pady=5)

        # Buton suplimentar – deschide services.msc
        services_btn = ctk.CTkButton(
            buttons_frame,
            text="Deschide managerul de servicii (services.msc)",
            command=self.open_services_console
        )
        services_btn.pack(padx=10, pady=5)

    def run_bat_file(self):
        """
        Execută fișierul reduce_services.bat,
        care oprește/optimizează servicii neesențiale Windows.
        """
        bat_path = os.path.abspath(r"resources//reduce_services.bat")
        if os.path.exists(bat_path):
            try:
                subprocess.run([bat_path], shell=True, check=True)
                messagebox.showinfo("Succes", "Serviciile au fost optimizate cu succes!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Eroare", f"Eroare la rularea scriptului:\n{e}")
        else:
            messagebox.showerror("Eroare", f"Fișierul .bat nu există:\n{bat_path}")

    def open_services_console(self):
        """
        Deschide consola Services (services.msc),
        unde pot fi văzute și modificate manual serviciile Windows.
        """
        try:
            subprocess.run(["cmd.exe", "/c", "start", "services.msc"], check=True)
        except Exception as e:
            messagebox.showerror(
                "Eroare",
                f"Nu s-a putut deschide managerul de servicii Windows:\n{e}"
            )
