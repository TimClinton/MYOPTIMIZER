import customtkinter as ctk
import subprocess
import ctypes
from tkinter import messagebox

class RestoreTab(ctk.CTkFrame):
    def __init__(self, parent):
        """
        :param parent: containerul părinte, de obicei un ctk.CTkTabview sau alt CTkFrame
        """
        super().__init__(parent)

        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Punct de Restaurare Windows",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Creează rapid un punct de restaurare pentru a putea reveni la "
                "setările actuale ale sistemului."
            ),
            wraplength=500  # optional, pentru text mai lung
        )
        desc_label.pack(pady=5, padx=10)

        # Un cadru (CTkFrame) în care să așezăm butoanele
        buttons_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )
        buttons_frame.pack(pady=10)

        # Butonul principal de creare Restore Point
        create_btn = ctk.CTkButton(
            buttons_frame,
            text="Creează Restore Point",
            command=self.create_restore_point
        )
        create_btn.pack(padx=10, pady=5)

        # Buton suplimentar - deschide fereastra de configurare System Restore
        config_btn = ctk.CTkButton(
            buttons_frame,
            text="Deschide setări System Restore",
            command=self.open_system_restore_settings
        )
        config_btn.pack(padx=10, pady=5)

    def is_admin(self):
        """
        Verifică dacă aplicația rulează cu drepturi de administrator.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def open_system_restore_settings(self):
        """
        Deschide direct pagina de System Restore, de unde se pot configura
        setările de restaurare și se pot vedea punctele existente.
        """
        try:
            # Comanda echivalentă pentru Windows 10/11 să deschidă direct System Protection
            # Va lansa fereastra 'SystemPropertiesProtection'
            subprocess.run(["cmd.exe", "/c", "start SystemPropertiesProtection"], check=True)
        except Exception as e:
            messagebox.showerror("Eroare", f"Nu s-au putut deschide setările de restaurare: {e}")

    def create_restore_point(self):
        """
        Creează un punct de restaurare nou, folosind PowerShell (Checkpoint-Computer).
        Necesită drepturi de administrator.
        """
        if not self.is_admin():
            messagebox.showerror(
                "Eroare",
                "Pentru a crea un punct de restaurare, aplicația trebuie să ruleze ca administrator!"
            )
            return

        try:
            command = "Checkpoint-Computer -Description 'MyRestore' -RestorePointType 'MODIFY_SETTINGS'"
            subprocess.run(["powershell.exe", "-Command", command], shell=True)
            messagebox.showinfo("Succes", "Restore point creat cu succes!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la crearea restore point: {e}")
