import customtkinter as ctk
from tabs.pc_info_tab import PCInfoTab
from tabs.restore_tab import RestoreTab
from tabs.reduce_services_tab import ReduceServicesTab
from tabs.windows_settings_tab import WindowsSettingsTab
from tabs.gpu_tab import GPUTab
from tabs.reg_tweaks_tab import RegTweaksTab
from tabs.cleanup_tab import CleanupTab

# Constants for styling
FONT_TITLE = ("Roboto", 24, "bold")
FONT_BUTTON = ("Roboto", 16)
FONT_BUTTON_ACTIVE = ("Roboto", 16, "bold")
CORNER_RADIUS = 15
PADDING = 20
SIDEBAR_WIDTH = 250

class ThemeConfig:
    """Class to manage theme settings."""
    DARK = {
        "bg_color": "#1A3C34",
        "dark_green": "#0A2F2A",
        "medium_green": "#2A5C52",
        "light_green": "#3A7A6E",
        "accent_green": "#4CAF50",
        "text_color": "#E0F2E9",
        "gradient_start": "#2A5C52",
        "gradient_end": "#1A3C34"
    }
    LIGHT = {
        "bg_color": "#E6F3E6",
        "dark_green": "#A8D5A8",
        "medium_green": "#C2E2C2",
        "light_green": "#D9EAD9",
        "accent_green": "#4CAF50",
        "text_color": "#1A3C34",
        "gradient_start": "#C2E2C2",
        "gradient_end": "#A8D5A8"
    }

class ModernOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WinOptim")
        self.geometry("1200x800")
        self.minsize(800, 600)  # Ensure minimum window size for responsiveness

        # Set initial theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.theme = ThemeConfig.DARK
        self.is_dark_mode = True

        # Instance attributes
        self.header_frame = None
        self.title_label = None
        self.toggle_theme_btn = None
        self.main_frame = None
        self.sidebar_frame = None
        self.content_frame = None
        self.sidebar_buttons = []
        self.frames_dict = {}
        self.current_frame_key = None

        self.build_ui()
        self.show_frame("PC Info")  # Load default tab

    def build_ui(self):
        """Build the main UI components."""
        self.configure(fg_color=self.theme["bg_color"])

        # Header
        self.header_frame = ctk.CTkFrame(
            self, corner_radius=CORNER_RADIUS, fg_color=self.theme["light_green"], height=60
        )
        self.header_frame.pack(fill="x", padx=PADDING, pady=(PADDING, 10))
        self.header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="WinOptim",
            font=FONT_TITLE,
            text_color=self.theme["text_color"]
        )
        self.title_label.pack(side="left", padx=PADDING, pady=10)

        self.toggle_theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌓",
            width=50,
            height=40,
            corner_radius=25,
            fg_color=self.theme["accent_green"],
            hover_color=self.theme["dark_green"],
            text_color=self.theme["text_color"],
            font=ctk.CTkFont(size=20),
            command=self.toggle_theme
        )
        self.toggle_theme_btn.pack(side="right", padx=PADDING, pady=10)

        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=PADDING, pady=10)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(
            self.main_frame,
            width=SIDEBAR_WIDTH,
            corner_radius=CORNER_RADIUS,
            fg_color=self.theme["light_green"]
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, PADDING), pady=10)
        self.sidebar_frame.pack_propagate(False)

        # Sidebar buttons
        button_configs = [
            ("PC Info", "🖥️", PCInfoTab),
            ("Restore Point", "🔄", RestoreTab),
            ("Reduce Services", "⚙️", ReduceServicesTab),
            ("Windows Settings", "⚙️", WindowsSettingsTab),
            ("GPU", "🎮", GPUTab),
            ("Reg Tweaks", "🔧", RegTweaksTab),
            ("Cleanup", "🧹", CleanupTab)
        ]

        for text, icon, _ in button_configs:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=f"{icon}  {text}",
                corner_radius=CORNER_RADIUS,
                fg_color="transparent",
                hover_color=self.theme["accent_green"],
                text_color=self.theme["text_color"],
                font=FONT_BUTTON,
                height=50,
                anchor="w",
                command=lambda t=text: self.show_frame(t)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.sidebar_buttons.append(btn)

        # Content frame
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=CORNER_RADIUS,
            fg_color=self.theme["medium_green"]
        )
        self.content_frame.pack(side="left", expand=True, fill="both", pady=10)

        # Initialize only the default tab
        self.frames_dict["PC Info"] = PCInfoTab(self.content_frame)
        self.frames_dict["PC Info"].pack(fill="both", expand=True)

        # Store tab classes for lazy loading
        self.tab_classes = {name: cls for name, _, cls in button_configs}

    def show_frame(self, frame_key):
        """Show the selected frame, lazily loading it if necessary."""
        if frame_key == self.current_frame_key:
            return

        # Hide current frame
        if self.current_frame_key:
            current_frame = self.frames_dict.get(self.current_frame_key)
            if current_frame:
                current_frame.pack_forget()

        # Load frame if not already initialized
        if frame_key not in self.frames_dict:
            tab_class = self.tab_classes.get(frame_key)
            if tab_class:
                self.frames_dict[frame_key] = tab_class(self.content_frame)
            else:
                print(f"Error: No tab class found for {frame_key}")
                return

        # Show new frame
        frame_to_show = self.frames_dict[frame_key]
        frame_to_show.pack(fill="both", expand=True)
        self.current_frame_key = frame_key

        # Update button states
        for btn in self.sidebar_buttons:
            btn_text = btn.cget("text").split("  ")[1]
            btn.configure(
                fg_color=self.theme["accent_green"] if btn_text == frame_key else "transparent",
                font=FONT_BUTTON_ACTIVE if btn_text == frame_key else FONT_BUTTON
            )

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = ThemeConfig.LIGHT if not self.is_dark_mode else ThemeConfig.DARK
        ctk.set_appearance_mode("light" if not self.is_dark_mode else "dark")
        self.apply_theme_colors()

    def apply_theme_colors(self):
        """Apply the current theme colors to all widgets."""
        self.configure(fg_color=self.theme["bg_color"])
        self.header_frame.configure(fg_color=self.theme["light_green"])
        self.title_label.configure(text_color=self.theme["text_color"])
        self.toggle_theme_btn.configure(
            fg_color=self.theme["accent_green"],
            hover_color=self.theme["dark_green"],
            text_color=self.theme["text_color"]
        )
        self.main_frame.configure(fg_color="transparent")
        self.sidebar_frame.configure(fg_color=self.theme["light_green"])
        self.content_frame.configure(fg_color=self.theme["medium_green"])

        for btn in self.sidebar_buttons:
            btn.configure(
                text_color=self.theme["text_color"],
                hover_color=self.theme["accent_green"]
            )

        # Refresh active frame to ensure theme consistency
        if self.current_frame_key:
            self.show_frame(self.current_frame_key)

if __name__ == "__main__":
    app = ModernOptimizerApp()
    app.mainloop()