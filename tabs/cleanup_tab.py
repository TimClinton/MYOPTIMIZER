import customtkinter as ctk
import subprocess
import os
import shutil
from tkinter import messagebox

class CleanupTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Titlu mare
        title_label = ctk.CTkLabel(
            self,
            text="Advanced Clean - Curățare rapidă",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Descriere scurtă
        desc_label = ctk.CTkLabel(
            self,
            text=(
                "Elimină fișiere temporare, cache și alte date inutile pentru a elibera spațiu și "
                "a îmbunătăți performanța. Alege din opțiunile de mai jos sau apasă pe "
                "'Curăță tot' pentru a face totul dintr-un singur pas."
            ),
            wraplength=500  # opțional, pentru text mai lung
        )
        desc_label.pack(padx=10, pady=5)

        # Cadru pentru butoanele de curățare
        adv_frame = ctk.CTkFrame(self, corner_radius=10)
        adv_frame.pack(fill="x", padx=10, pady=10)

        # Etichetă de titlu pentru frame
        frame_title = ctk.CTkLabel(
            adv_frame,
            text="⚙️ Advanced Clean",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        frame_title.pack(anchor="w", padx=5, pady=(5, 5))

        # Buton "Curăță tot"
        clean_all_btn = ctk.CTkButton(
            adv_frame,
            text="Curăță tot",
            command=self.cleanup_all
        )
        clean_all_btn.pack(fill="x", padx=5, pady=(0, 10))

        # Butoanele individuale pentru curățarea avansată
        btn_sys_temp = ctk.CTkButton(
            adv_frame,
            text="Fișiere temporare de sistem",
            command=self.cleanup_windows_temp
        )
        btn_sys_temp.pack(fill="x", padx=5, pady=2)

        btn_user_temp = ctk.CTkButton(
            adv_frame,
            text="Fișiere temporare utilizator",
            command=self.cleanup_temp
        )
        btn_user_temp.pack(fill="x", padx=5, pady=2)

        btn_prefetch = ctk.CTkButton(
            adv_frame,
            text="Fișiere Prefetch",
            command=self.cleanup_prefetch
        )
        btn_prefetch.pack(fill="x", padx=5, pady=2)

        btn_dns_cache = ctk.CTkButton(
            adv_frame,
            text="Cache DNS",
            command=self.cleanup_dns_cache
        )
        btn_dns_cache.pack(fill="x", padx=5, pady=2)

        btn_thumb_cache = ctk.CTkButton(
            adv_frame,
            text="Cache thumbnail-uri",
            command=self.cleanup_thumbnail_cache
        )
        btn_thumb_cache.pack(fill="x", padx=5, pady=2)

        btn_error_logs = ctk.CTkButton(
            adv_frame,
            text="Fișiere log Windows",
            command=self.cleanup_error_logs
        )
        btn_error_logs.pack(fill="x", padx=5, pady=2)

        btn_old_updates = ctk.CTkButton(
            adv_frame,
            text="Update Windows vechi",
            command=self.cleanup_windows_update_old
        )
        btn_old_updates.pack(fill="x", padx=5, pady=2)

        btn_recycle_bin = ctk.CTkButton(
            adv_frame,
            text="Coș de gunoi",
            command=self.cleanup_recycle_bin
        )
        btn_recycle_bin.pack(fill="x", padx=5, pady=2)

        btn_clipboard = ctk.CTkButton(
            adv_frame,
            text="Clipboard",
            command=self.cleanup_clipboard
        )
        btn_clipboard.pack(fill="x", padx=5, pady=2)

        # Buton suplimentar - deschide Disk Cleanup
        diskcleanup_btn = ctk.CTkButton(
            adv_frame,
            text="Deschide Disk Cleanup (cleanmgr)",
            command=self.open_disk_cleanup
        )
        diskcleanup_btn.pack(fill="x", padx=5, pady=(10, 2))

    def cleanup_all(self):
        """
        Apelează, pe rând, metodele de curățare considerate importante.
        """
        self.cleanup_windows_temp()
        self.cleanup_temp()
        self.cleanup_prefetch()
        self.cleanup_recycle_bin()
        # Adaugă și alte funcții de curățare dacă dorești
        messagebox.showinfo("Curăță tot", "Operațiile de curățare s-au finalizat.")

    def open_disk_cleanup(self):
        """
        Deschide utilitarul Disk Cleanup, pentru curățare avansată la nivel de sistem.
        """
        try:
            subprocess.run(["cleanmgr"], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la deschiderea Disk Cleanup:\n{e}")

    def remove_files_in_folder(self, folder):
        errs = []
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    errs.append(f"Eroare la ștergerea {file_path}: {e}")
        else:
            errs.append(f"Folderul {folder} nu există.")
        return errs

    def cleanup_windows_temp(self):
        folder = r"C:\Windows\Temp"
        errs = self.remove_files_in_folder(folder)
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Fișierele temporare de sistem au fost șterse.")

    def cleanup_temp(self):
        folder = os.environ.get("TEMP", "")
        errs = self.remove_files_in_folder(folder)
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Fișierele temporare utilizator au fost șterse.")

    def cleanup_prefetch(self):
        folder = r"C:\Windows\Prefetch"
        errs = self.remove_files_in_folder(folder)
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Fișierele Prefetch au fost șterse.")

    def cleanup_dns_cache(self):
        try:
            subprocess.run(["ipconfig", "/flushdns"], shell=True, check=True)
            messagebox.showinfo("Succes", "Cache DNS a fost curățat.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la curățarea DNS cache:\n{e}")

    def cleanup_thumbnail_cache(self):
        folder = os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Microsoft\Windows\Explorer")
        errs = []
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if filename.lower().startswith("thumbcache"):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        errs.append(f"Eroare la ștergerea {file_path}: {e}")
        else:
            errs.append(f"Folderul {folder} nu există.")
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Cache thumbnail-uri a fost curățat.")

    def cleanup_error_logs(self):
        folder = r"C:\Windows\Temp\WER"
        errs = self.remove_files_in_folder(folder)
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Fișierele log Windows au fost șterse.")

    def cleanup_windows_update_old(self):
        folder = r"C:\Windows\SoftwareDistribution\Download"
        errs = self.remove_files_in_folder(folder)
        if errs:
            messagebox.showerror("Eroare", "\n".join(errs))
        else:
            messagebox.showinfo("Succes", "Fișierele de update Windows vechi au fost șterse.")

    def cleanup_recycle_bin(self):
        try:
            subprocess.run(["powershell.exe", "-Command", "Clear-RecycleBin -Force"], shell=True, check=True)
            messagebox.showinfo("Succes", "Coșul de gunoi a fost golit.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la golirea coșului de gunoi:\n{e}")

    def cleanup_clipboard(self):
        try:
            subprocess.run(["cmd", "/c", "echo off|clip"], shell=True, check=True)
            messagebox.showinfo("Succes", "Clipboard-ul a fost curățat.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Eroare", f"Eroare la curățarea clipboard-ului:\n{e}")
