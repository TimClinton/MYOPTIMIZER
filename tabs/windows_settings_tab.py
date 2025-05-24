import customtkinter as ctk
import subprocess
from tkinter import messagebox

class WindowsSettingsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Setări Windows",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Activează sau dezactivează rapid anumite funcții din Windows. "
                "Apasă pe butoanele de mai jos pentru a comuta între ON și OFF.\n"
                "Pentru setări suplimentare, folosește butoanele dedicate sau "
                "deschide manual opțiunile Windows."
            ),
            wraplength=500  # opțional, pentru text mai lung
        )
        desc_label.pack(padx=10, pady=5)

        # Cadru pentru toggles
        toggles_frame = ctk.CTkFrame(self, corner_radius=10)
        toggles_frame.pack(pady=10, padx=10, fill="x")

        # În loc de "On/Off.TButton" (ttk.Style), vom crea butoane personalizate
        # și vom actualiza "fg_color"/"hover_color" la ON/OFF, plus textul butonului.

        # Variabile pentru starea setărilor
        self.notifications_state = True
        self.storage_state = True
        self.bluetooth_state = True
        self.game_mode_state = True

        # Buton pentru Notificări
        self.btn_notifications = ctk.CTkButton(
            toggles_frame,
            text=self.get_toggle_text("Notificări", self.notifications_state),
            command=self.toggle_notifications
        )
        self.btn_notifications.pack(anchor="w", pady=4, fill="x")

        # Buton pentru Storage Sense
        self.btn_storage = ctk.CTkButton(
            toggles_frame,
            text=self.get_toggle_text("Storage Sense", self.storage_state),
            command=self.toggle_storage_sense
        )
        self.btn_storage.pack(anchor="w", pady=4, fill="x")

        # Buton pentru Bluetooth
        self.btn_bluetooth = ctk.CTkButton(
            toggles_frame,
            text=self.get_toggle_text("Bluetooth", self.bluetooth_state),
            command=self.toggle_bluetooth
        )
        self.btn_bluetooth.pack(anchor="w", pady=4, fill="x")

        # Buton pentru Game Mode
        self.btn_game_mode = ctk.CTkButton(
            toggles_frame,
            text=self.get_toggle_text("Game Mode", self.game_mode_state),
            command=self.toggle_game_mode
        )
        self.btn_game_mode.pack(anchor="w", pady=4, fill="x")

        # Cadru pentru butoane suplimentare (deschid Windows Settings)
        extra_frame = ctk.CTkFrame(self, corner_radius=10)
        extra_frame.pack(pady=10, padx=10, fill="x")

        # Buton pentru Startup Apps
        btn_startup = ctk.CTkButton(
            extra_frame,
            text="Deschide Startup Apps",
            command=lambda: self.open_setting("ms-settings:startupapps")
        )
        btn_startup.pack(anchor="w", pady=3, fill="x")

        # Buton pentru Privacy (exemplu) - deschide setările de confidențialitate
        btn_privacy = ctk.CTkButton(
            extra_frame,
            text="Deschide Privacy Settings",
            command=lambda: self.open_setting("ms-settings:privacy")
        )
        btn_privacy.pack(anchor="w", pady=3, fill="x")

        # Buton pentru Notifications & actions (setări avansate de notificări)
        btn_notif_settings = ctk.CTkButton(
            extra_frame,
            text="Deschide Notifications & actions",
            command=lambda: self.open_setting("ms-settings:notifications")
        )
        btn_notif_settings.pack(anchor="w", pady=3, fill="x")

        # Actualizăm culorile inițiale ON vs OFF
        self.update_button_style(self.btn_notifications, self.notifications_state)
        self.update_button_style(self.btn_storage, self.storage_state)
        self.update_button_style(self.btn_bluetooth, self.bluetooth_state)
        self.update_button_style(self.btn_game_mode, self.game_mode_state)

    def get_toggle_text(self, label, state):
        """Formează textul ce apare pe butoanele de tip toggle."""
        return f"{label}: {'ON' if state else 'OFF'}"

    def update_button_style(self, button, state):
        """
        În customtkinter, putem personaliza culorile în funcție de stare (ON/OFF).
        De ex. ON: verde, OFF: gri.
        """
        if state:
            # ON: un verde
            button.configure(
                fg_color="#66bb6a",
                hover_color="#55aa5a",
                text_color="white"
            )
        else:
            # OFF: un gri
            button.configure(
                fg_color="grey",
                hover_color="#999999",
                text_color="white"
            )

        # Actualizează și textul (dacă e un buton dedicat)
        # (În acest exemplu, textul se actualizează în toggle_*)

    # ---------------------------------------------------------------
    # FUNCȚII PENTRU TOGGLE (Notificări, Storage Sense, Bluetooth, Game Mode)
    # ---------------------------------------------------------------
    def toggle_notifications(self):
        self.notifications_state = not self.notifications_state
        value = 1 if self.notifications_state else 0
        cmd = (
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications' "
            f"-Name 'ToastEnabled' -Value {value}"
        )
        try:
            subprocess.run(["powershell.exe", "-Command", cmd], shell=True, check=True)
            # Schimbăm textul butonului + culorile
            self.btn_notifications.configure(
                text=self.get_toggle_text("Notificări", self.notifications_state)
            )
            self.update_button_style(self.btn_notifications, self.notifications_state)

            messagebox.showinfo(
                "Notificări",
                f"Notificările au fost {'activate' if self.notifications_state else 'dezactivate'}."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la modificarea notificărilor:\n{e}")
            self.notifications_state = not self.notifications_state

    def toggle_storage_sense(self):
        self.storage_state = not self.storage_state
        value = 1 if self.storage_state else 0
        cmd = (
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy' "
            f"-Name '01' -Value {value}"
        )
        try:
            subprocess.run(["powershell.exe", "-Command", cmd], shell=True, check=True)
            self.btn_storage.configure(
                text=self.get_toggle_text("Storage Sense", self.storage_state)
            )
            self.update_button_style(self.btn_storage, self.storage_state)

            messagebox.showinfo(
                "Storage Sense",
                f"Storage Sense a fost {'activat' if self.storage_state else 'dezactivat'}."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la modificarea Storage Sense:\n{e}")
            self.storage_state = not self.storage_state

    def toggle_bluetooth(self):
        self.bluetooth_state = not self.bluetooth_state
        cmd = (
            "Get-PnpDevice -Class Bluetooth | "
            f"{'Enable' if self.bluetooth_state else 'Disable'}-PnpDevice -Confirm:$false"
        )
        try:
            subprocess.run(["powershell.exe", "-Command", cmd], shell=True, check=True)
            self.btn_bluetooth.configure(
                text=self.get_toggle_text("Bluetooth", self.bluetooth_state)
            )
            self.update_button_style(self.btn_bluetooth, self.bluetooth_state)

            messagebox.showinfo(
                "Bluetooth",
                f"Bluetooth a fost {'activat' if self.bluetooth_state else 'dezactivat'}."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la modificarea Bluetooth:\n{e}")
            self.bluetooth_state = not self.bluetooth_state

    def toggle_game_mode(self):
        self.game_mode_state = not self.game_mode_state
        value = 1 if self.game_mode_state else 0
        cmd = (
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\GameBar' "
            f"-Name 'AutoGameModeEnabled' -Value {value}"
        )
        try:
            subprocess.run(["powershell.exe", "-Command", cmd], shell=True, check=True)
            self.btn_game_mode.configure(
                text=self.get_toggle_text("Game Mode", self.game_mode_state)
            )
            self.update_button_style(self.btn_game_mode, self.game_mode_state)

            messagebox.showinfo(
                "Game Mode",
                f"Game Mode a fost {'activat' if self.game_mode_state else 'dezactivat'}."
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la modificarea Game Mode:\n{e}")
            self.game_mode_state = not self.game_mode_state

    def open_setting(self, command):
        """Deschide direct o pagină din Windows Settings (ex: ms-settings:startupapps)."""
        try:
            subprocess.run(["start", command], shell=True)
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la deschiderea setării: {e}")
