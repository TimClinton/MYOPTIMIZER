import customtkinter as ctk
import subprocess
import os
from tkinter import messagebox

class RegTweaksTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Registry Tweaks",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Salvează mai întâi o copie a registrului Windows, apoi aplică tweak-uri.\n"
                "Este recomandat să ai un backup înainte de orice modificare de registry."
            ),
            wraplength=500  # opțional, pentru text mai lung
        )
        desc_label.pack(padx=10, pady=5)

        # Cadru pentru butoane
        buttons_frame = ctk.CTkFrame(self, corner_radius=10)
        buttons_frame.pack(padx=10, pady=10, fill="x")

        # Variabilă ce indică dacă s-a făcut backup
        self.has_backup = False

        # Buton pentru crearea backup-ului
        backup_btn = ctk.CTkButton(
            buttons_frame,
            text="Creează Backup la Registry",
            command=self.backup_registry
        )
        backup_btn.pack(anchor="w", pady=5, fill="x")

        # Un singur tweak definit (fără ON/OFF). Va fi dezactivat până se face backup.
        self.reg_tweak = {
            "name": "Reg Tweak 1",
            "file": "reg_tweak1.reg"
        }

        # Butonul pentru aplicarea Tweak-ului
        self.btn_apply_tweak = ctk.CTkButton(
            buttons_frame,
            text=f"Aplică {self.reg_tweak['name']}",
            command=self.apply_tweak
        )
        self.btn_apply_tweak.pack(anchor="w", pady=5, fill="x")

        # Inițial, îl dezactivăm, până facem backup
        self.btn_apply_tweak.configure(state="disabled")

    def backup_registry(self):
        """
        Creăm un backup al Registry-ului.
        Metodă simplă: exportăm Hive-urile principale HKLM și HKCU în fișiere .reg
        sau orice metodă preferată.
        """
        backup_dir = os.path.abspath("backup_registry")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_hklm_path = os.path.join(backup_dir, "backup_hklm.reg")
        backup_hkcu_path = os.path.join(backup_dir, "backup_hkcu.reg")

        try:
            # Exportăm HKLM
            subprocess.run(["reg", "export", "HKLM", backup_hklm_path, "/y"], shell=True, check=True)
            # Exportăm HKCU
            subprocess.run(["reg", "export", "HKCU", backup_hkcu_path, "/y"], shell=True, check=True)

            messagebox.showinfo(
                "Backup Registry",
                f"Backup creat cu succes în folderul:\n{backup_dir}"
            )

            # Marcam că avem backup
            self.has_backup = True
            # Activăm butonul de Tweak
            self.btn_apply_tweak.configure(state="normal")

        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Eroare Backup Registry",
                f"A apărut o eroare la crearea backup-ului:\n{e}"
            )

    def apply_tweak(self):
        """
        Aplică fișierul .reg (Reg Tweak 1), numai dacă avem deja backup făcut.
        """
        if not self.has_backup:
            messagebox.showerror(
                "Eroare",
                "Trebuie să faci întâi backup la Registry!"
            )
            return

        reg_file = os.path.abspath(os.path.join("resources", self.reg_tweak["file"]))
        if not os.path.exists(reg_file):
            messagebox.showerror(
                "Eroare",
                f"Fișierul de tweak nu există:\n{reg_file}"
            )
            return

        try:
            subprocess.run(["reg", "import", reg_file], shell=True, check=True)
            messagebox.showinfo(
                "Reg Tweak",
                f"{self.reg_tweak['name']} a fost aplicat cu succes!"
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror(
                "Eroare Tweak",
                f"Eroare la aplicarea {self.reg_tweak['name']}:\n{e}"
            )
