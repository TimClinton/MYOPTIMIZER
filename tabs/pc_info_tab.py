import customtkinter as ctk
import platform
import psutil

try:
    import wmi
except ImportError:
    wmi = None

class PCInfoTab(ctk.CTkFrame):
    def __init__(self, parent):
        """
        :param parent: container-ul părinte (de regulă un ctk.CTkTabview sau alt ctk.CTkFrame)
        """
        super().__init__(parent)
        
        # Titlu mare, cu font mai vizibil (opțional, poți personaliza culori etc.)
        title_label = ctk.CTkLabel(
            self,
            text="Informații detaliate despre PC",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Creăm un frame scrollabil (CTkScrollableFrame) pentru a afișa informațiile pe mai multe coloane
        self.scrolled_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )
        self.scrolled_frame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

        # Obținem informațiile de sistem
        info = self.get_system_info()
        info_items = list(info.items())

        # Vom afișa categoriile în 3 coloane
        cols = 3

        # Facem setări de "grid" pentru scrolled_frame (pe lățime)
        for col in range(cols):
            self.scrolled_frame.grid_columnconfigure(col, weight=1)

        # Afișăm fiecare categorie (Sistem de Operare, CPU, Memorie, etc.)
        for i, (category, details) in enumerate(info_items):
            row = i // cols
            col = i % cols

            # Un ctk.CTkFrame pentru fiecare categorie
            category_frame = ctk.CTkFrame(
                self.scrolled_frame,
                corner_radius=8
            )
            category_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            # Eticheta (titlul categoriei)
            cat_label = ctk.CTkLabel(
                category_frame,
                text=category,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            cat_label.pack(anchor="w", padx=5, pady=(5, 2))

            # Afișăm detaliile: pot fi un dict sau o listă de dict-uri
            if isinstance(details, dict):
                # Creăm direct un "tabel" cu cheie-valoare
                self.create_table(category_frame, details)
            elif isinstance(details, list):
                # Fiecare element din listă poate fi sub-categorie (ex: Discuri, Rețea, GPU)
                for item in details:
                    # Extrag un titlu din date (ex "Discul", "Interfață", "Nume GPU")
                    sub_title = item.get("Discul") or item.get("Interfață") or item.get("Nume GPU") or ""
                    if sub_title:
                        sub_frame = ctk.CTkFrame(category_frame, corner_radius=6)
                        sub_frame.pack(fill="x", padx=5, pady=5)

                        sub_label = ctk.CTkLabel(
                            sub_frame,
                            text=sub_title,
                            font=ctk.CTkFont(size=13, weight="bold")
                        )
                        sub_label.pack(anchor="w", padx=5, pady=(5, 2))

                        self.create_table(sub_frame, item)
                    else:
                        # Dacă nu avem un titlu, punem direct datele
                        self.create_table(category_frame, item)

    def create_table(self, parent, data: dict):
        """
        Afișează un "mini-tabel" cu cheie-valoare, stivuite vertical.
        """
        for key, value in data.items():
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=5, pady=2)

            key_label = ctk.CTkLabel(
                row_frame,
                text=f"{key}:",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            key_label.pack(side="left")

            val_label = ctk.CTkLabel(
                row_frame,
                text=str(value),
                font=ctk.CTkFont(size=12)
            )
            val_label.pack(side="left", padx=(5, 0))

    def get_system_info(self):
        """
        Colectează informații despre:
         - Sistem de Operare
         - CPU
         - Memorie RAM
         - Discuri
         - Rețea
         - GPU (opțional, prin WMI)
        """
        info = {}

        # Sistem de Operare
        info["Sistem de Operare"] = {
            "Sistem": platform.system(),
            "Versiune": platform.version(),
            "Platform": platform.platform(),
            "Machine": platform.machine(),
        }

        # CPU
        physical_cores = psutil.cpu_count(logical=False)
        total_cores = psutil.cpu_count(logical=True)
        cpu_usage = psutil.cpu_percent(interval=0.5)

        cpu_info = {
            "Nuclee fizice": physical_cores,
            "Nuclee logice": total_cores,
            "Utilizare CPU": f"{cpu_usage}%"
        }
        try:
            cpufreq = psutil.cpu_freq()
            if cpufreq:
                cpu_info["Frecvență curentă"] = f"{cpufreq.current:.2f} MHz"
                cpu_info["Frecvență maximă"] = f"{cpufreq.max:.2f} MHz"
        except:
            pass
        info["Informații CPU"] = cpu_info

        # Memorie RAM
        svmem = psutil.virtual_memory()
        info["Memorie RAM"] = {
            "Total": self.get_size(svmem.total),
            "Disponibil": self.get_size(svmem.available),
            "Utilizată": self.get_size(svmem.used),
            "Procent": f"{svmem.percent}%"
        }

        # Discuri
        partitions = psutil.disk_partitions()
        disk_list = []
        for partition in partitions:
            partition_info = {"Discul": partition.device, "FS": partition.fstype}
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info["Total"] = self.get_size(usage.total)
                partition_info["Utilizat"] = self.get_size(usage.used)
                partition_info["Disponibil"] = self.get_size(usage.free)
                partition_info["Procent"] = f"{usage.percent}%"
            except:
                partition_info["Info"] = "Nu se pot obține detalii"
            disk_list.append(partition_info)
        info["Discuri"] = disk_list

        # Rețea
        net_if_addrs = psutil.net_if_addrs()
        net_list = []
        for if_name, if_add in net_if_addrs.items():
            net_item = {"Interfață": if_name}
            ip_list = []
            mac_list = []
            for addr in if_add:
                if addr.family.name == 'AF_INET':
                    ip_list.append(addr.address)
                elif addr.family.name == 'AF_PACKET':
                    mac_list.append(addr.address)
            if ip_list:
                net_item["IP"] = ", ".join(ip_list)
            if mac_list:
                net_item["MAC"] = ", ".join(mac_list)
            net_list.append(net_item)
        info["Rețea"] = net_list

        # GPU (folosind WMI, dacă e disponibil)
        gpu_list = []
        if wmi is not None:
            try:
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    gpu_info = {
                        "Nume GPU": getattr(gpu, "Name", "N/A"),
                        "Driver": getattr(gpu, "DriverVersion", "N/A")
                    }
                    gpu_list.append(gpu_info)
            except:
                pass
        if gpu_list:
            info["GPU"] = gpu_list

        return info

    @staticmethod
    def get_size(bytes_val, suffix="B"):
        """
        Conversie bytes -> KB, MB, GB etc.
        """
        if not bytes_val:
            return "0B"
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes_val < factor:
                return f"{bytes_val:.2f}{unit}{suffix}"
            bytes_val /= factor
        return f"{bytes_val:.2f}Y{suffix}"
