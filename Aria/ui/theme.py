from dataclasses import dataclass


LIGHT = {
    "BG": "#F7FAFF",
    "SURFACE": "#FFFFFF",
    "TEXT": "#1F2A44",
    "TEXT_SECONDARY": "#5B6477",
    "BORDER": "#E2E8F0",
    "PRIMARY": "#3A7BD5",
    "PRIMARY_700": "#2C5FA8",
    "SECONDARY": "#2EC4B6",
    "SECONDARY_700": "#219E92",
    "ACCENT": "#FF6B6B",
    "CANVAS_BG": "#FFFFFF",
}

DARK = {
    "BG": "#0F172A",            # slate-900
    "SURFACE": "#111827",       # gray-900
    "TEXT": "#E5E7EB",          # gray-200
    "TEXT_SECONDARY": "#9CA3AF", # gray-400
    "BORDER": "#374151",        # gray-700
    "PRIMARY": "#60A5FA",       # blue-400
    "PRIMARY_700": "#3B82F6",   # blue-500
    "SECONDARY": "#5EEAD4",     # teal-300
    "SECONDARY_700": "#2DD4BF", # teal-400
    "ACCENT": "#FB7185",        # rose-400
    "CANVAS_BG": "#1F2937",     # gray-800
}


@dataclass
class ThemeManager:
    mode: str = "light"  # 'light' | 'dark'

    def colors(self):
        return LIGHT if self.mode == "light" else DARK

    def toggle(self):
        self.mode = "dark" if self.mode == "light" else "light"


def style_primary_button(btn, c):
    btn.configure(
        bg=c["PRIMARY"], fg="#FFFFFF",
        activebackground=c["PRIMARY_700"], activeforeground="#FFFFFF",
        relief="flat", bd=0, highlightthickness=0,
        cursor="hand2",
    )


def style_secondary_button(btn, c):
    btn.configure(
        bg=c["SURFACE"], fg=c["PRIMARY"],
        activebackground=c["BORDER"], activeforeground=c["PRIMARY"],
        relief="groove", bd=1, highlightthickness=0,
        cursor="hand2",
    )


def style_ghost_button(btn, c):
    btn.configure(
        bg=c["BG"], fg=c["TEXT"],
        activebackground=c["BORDER"], activeforeground=c["TEXT"],
        relief="flat", bd=0, highlightthickness=0,
        cursor="hand2",
    )


def style_danger_button(btn, c):
    btn.configure(
        bg=c["ACCENT"], fg="#FFFFFF",
        activebackground="#e85b5b", activeforeground="#FFFFFF",
        relief="flat", bd=0, highlightthickness=0,
        cursor="hand2",
    )

