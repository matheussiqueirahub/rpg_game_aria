import os
import tkinter as tk

from Aria import database
from Aria.ui.login_frame import LoginFrame
from Aria.ui.register_frame import RegisterFrame
from Aria.ui.character_frame import CharacterFrame
from Aria.ui.theme import ThemeManager


class AriaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aria — CB Games")
        self.minsize(840, 560)
        self._try_set_icon()

        # Estado de sessão
        self.current_user_id = None
        self.current_username = None

        # Tema
        self.theme = ThemeManager(mode="light")
        self.configure(bg=self.theme.colors()["BG"])

        # Topbar
        self.topbar = tk.Frame(self, height=48)
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        self.topbar_title = tk.Label(self.topbar, text="Aria — CB Games", font=("Segoe UI", 14, "bold"))
        self.topbar_title.pack(side=tk.LEFT, padx=16, pady=8)
        self.btn_theme = tk.Button(self.topbar, text="Modo Escuro", command=self._toggle_theme)
        self.btn_theme.pack(side=tk.RIGHT, padx=12, pady=8)

        # Container principal que troca as telas
        container = tk.Frame(self, bd=0)
        container.pack(fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Instancia telas
        self.frames["login"] = LoginFrame(
            container,
            on_login_success=self._on_login_success,
            on_go_register=lambda: self.show_frame("register"),
        )
        self.frames["register"] = RegisterFrame(
            container,
            on_account_created=self._on_account_created,
            on_go_login=lambda: self.show_frame("login"),
        )
        self.frames["character"] = CharacterFrame(
            container,
            get_current_user_id=lambda: self.current_user_id,
            on_logout=self._logout,
        )

        # Empacota frames no grid e esconde todos inicialmente
        for name, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("login")
        self._apply_theme()
        self.after(50, self._center_on_screen)

    def _try_set_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "aria.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            # Ignora em plataformas sem suporte
            pass

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception:
                pass

    def _on_login_success(self, user_id: int, username: str):
        self.current_user_id = user_id
        self.current_username = username
        self.show_frame("character")

    def _on_account_created(self, username: str):
        # Volta ao login com usuário preenchido
        login: LoginFrame = self.frames["login"]
        login.prefill(username)
        self.show_frame("login")

    def _logout(self):
        self.current_user_id = None
        self.current_username = None
        self.show_frame("login")

    def _toggle_theme(self):
        self.theme.toggle()
        self._apply_theme()

    def _apply_theme(self):
        c = self.theme.colors()
        # App bg
        self.configure(bg=c["BG"])
        # Topbar
        self.topbar.configure(bg=c["PRIMARY"])
        self.topbar_title.configure(bg=c["PRIMARY"], fg="#FFFFFF")
        self.btn_theme.configure(
            bg=c["PRIMARY_700"], fg="#FFFFFF",
            activebackground=c["PRIMARY_700"], activeforeground="#FFFFFF",
            relief="flat", bd=0, highlightthickness=0, cursor="hand2",
            text=("Modo Claro" if self.theme.mode == "dark" else "Modo Escuro"),
        )

        # Frames
        for frame in self.frames.values():
            if hasattr(frame, "apply_theme"):
                try:
                    frame.apply_theme(c)
                except Exception:
                    pass

    def _center_on_screen(self):
        try:
            self.update_idletasks()
            w = self.winfo_width()
            h = self.winfo_height()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = (sw // 2) - (w // 2)
            y = (sh // 2) - (h // 2)
            self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass


def main():
    # Prepara banco de dados
    database.init_db()

    # Inicia aplicação
    app = AriaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
