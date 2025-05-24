import customtkinter as ctk
import subprocess
import os
from tkinter import messagebox

class GPUTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Setări GPU (NVIDIA Inspector)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Importă profilul NVIDIA Inspector pentru a personaliza driverele "
                "și a obține performanțe mai bune în jocuri.\n"
                "De asemenea, poți deschide panoul NVIDIA pentru setări suplimentare."
            ),
            wraplength=500  # opțional, pentru text mai lung
        )
        desc_label.pack(padx=10, pady=5)

        # Cadru pentru butoane
        buttons_frame = ctk.CTkFrame(self, corner_radius=10)
        buttons_frame.pack(pady=10)

        # Buton principal – importă fișierul .nip
        import_btn = ctk.CTkButton(
            buttons_frame,
            text="Importă nvidiaset.nip",
            command=self.import_nip
        )
        import_btn.pack(pady=5)

        # Buton suplimentar – deschide NVIDIA Control Panel
        nvcp_btn = ctk.CTkButton(
            buttons_frame,
            text="Deschide NVIDIA Control Panel",
            command=self.open_nvidia_control_panel
        )
        nvcp_btn.pack(pady=5)

    def import_nip(self):
        """
        Importă profilul NVIDIA Inspector (nvidiaset.nip) folosind nvidiaProfileInspector.exe.
        """
        nip_path = os.path.abspath("resources/nvidiaset.nip")
        inspector_path = os.path.abspath("resources/nvidiaProfileInspector.exe")

        if not os.path.exists(inspector_path):
            messagebox.showerror("Eroare", "nvidiaProfileInspector.exe nu a fost găsit!")
            return

        if not os.path.exists(nip_path):
            messagebox.showerror("Eroare", "Fișierul nvidiaset.nip nu a fost găsit!")
            return

        try:
            # Comandă: nvidiaProfileInspector.exe -import nvidiaset.nip
            subprocess.run([inspector_path, "-import", nip_path], shell=True, check=True)
            messagebox.showinfo("Succes", "Profilul NVIDIA a fost importat cu succes!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la importul profilului:\n{e}")

    def open_nvidia_control_panel(self):
        """
        Deschide NVIDIA Control Panel (dacă este instalat).
        Metode posibile: rundll32.exe shell32.dll,Control_RunDLL nvcpl.cpl
        """
        try:
            subprocess.run(
                ["rundll32.exe", "shell32.dll,Control_RunDLL", "nvcpl.cpl"],
                shell=True,
                check=True
            )
            messagebox.showinfo("NVIDIA Control Panel", "NVIDIA Control Panel a fost deschis.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Nu s-a putut deschide NVIDIA Control Panel:\n{e}")
