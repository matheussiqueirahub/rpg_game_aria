import tkinter as tk
from tkinter import messagebox
from typing import Callable

from .. import database
from .. import security
from .tooltip import bind_tooltip


class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success: Callable[[int, str], None], on_go_register: Callable[[], None]):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.on_go_register = on_go_register
        # Políticas
        self.MAX_ATTEMPTS = 5
        self.LOCK_MINUTES = 15

        self.columnconfigure(0, weight=1)

        self.title = tk.Label(self, text="Aria — Login", font=("Segoe UI", 18, "bold"))
        self.title.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="n")

        form = tk.Frame(self)
        form.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form.columnconfigure(1, weight=1)

        self.lbl_user = tk.Label(form, text="Usuário:")
        self.lbl_user.grid(row=0, column=0, sticky="e", padx=(0, 8), pady=5)
        self.entry_user = tk.Entry(form)
        self.entry_user.grid(row=0, column=1, sticky="ew", pady=5)

        self.lbl_pass = tk.Label(form, text="Senha:")
        self.lbl_pass.grid(row=1, column=0, sticky="e", padx=(0, 8), pady=5)
        self.entry_pass = tk.Entry(form, show="•")
        self.entry_pass.grid(row=1, column=1, sticky="ew", pady=5)

        actions = tk.Frame(self)
        actions.grid(row=2, column=0, pady=10)

        self.btn_login = tk.Button(actions, text="Entrar", width=12, command=self._attempt_login)
        self.btn_login.grid(row=0, column=0, padx=6)

        self.btn_register = tk.Button(actions, text="Criar conta", width=12, command=self.on_go_register)
        self.btn_register.grid(row=0, column=1, padx=6)

        self.entry_user.focus_set()
        # Atalhos
        self.entry_user.bind("<Return>", lambda e: self._attempt_login())
        self.entry_pass.bind("<Return>", lambda e: self._attempt_login())
        self.bind_all("<Escape>", lambda e: self._clear_fields())
        # Tooltips
        bind_tooltip(self.btn_login, "Entrar no Aria")
        bind_tooltip(self.btn_register, "Criar uma nova conta")

    def _attempt_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()
        if not username or not password:
            messagebox.showwarning("Campos obrigatórios", "Informe usuário e senha.")
            return

        user = database.get_user_by_username(username)
        if not user:
            messagebox.showerror("Falha no login", "Usuário ou senha inválidos.")
            return

        # Verifica bloqueio
        remaining = database.get_lock_remaining_minutes(int(user["id"]))
        if remaining > 0:
            messagebox.showerror("Conta bloqueada", f"Tente novamente em aproximadamente {remaining} min.")
            return

        if security.verify_password(user["password_hash"], password):
            database.reset_failed_login(int(user["id"]))
            self.on_login_success(int(user["id"]), username)
        else:
            database.register_failed_login(int(user["id"]), self.MAX_ATTEMPTS, self.LOCK_MINUTES)
            remaining = database.get_lock_remaining_minutes(int(user["id"]))
            if remaining > 0:
                messagebox.showerror("Conta bloqueada", f"Muitas tentativas. Tente em {remaining} min.")
            else:
                messagebox.showerror("Falha no login", "Usuário ou senha inválidos.")

    def prefill(self, username: str):
        self.entry_user.delete(0, tk.END)
        self.entry_user.insert(0, username)
        self.entry_pass.delete(0, tk.END)

    def _clear_fields(self):
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)

    def apply_theme(self, c):
        # Backgrounds
        self.configure(bg=c["BG"]) 
        for child in self.grid_slaves():
            if isinstance(child, tk.Frame):
                child.configure(bg=c["BG"]) 
        # Titles / labels
        self.title.configure(bg=c["BG"], fg=c["TEXT"]) 
        self.lbl_user.configure(bg=c["BG"], fg=c["TEXT"]) 
        self.lbl_pass.configure(bg=c["BG"], fg=c["TEXT"]) 
        # Entries
        self.entry_user.configure(bg=c["SURFACE"], fg=c["TEXT"], insertbackground=c["TEXT"])
        self.entry_pass.configure(bg=c["SURFACE"], fg=c["TEXT"], insertbackground=c["TEXT"])
        # Buttons
        from .theme import style_primary_button, style_secondary_button
        style_primary_button(self.btn_login, c)
        style_secondary_button(self.btn_register, c)
