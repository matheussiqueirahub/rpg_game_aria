import tkinter as tk
from tkinter import messagebox
from typing import Callable

from .. import database
from .. import security
from .tooltip import bind_tooltip


class RegisterFrame(tk.Frame):
    def __init__(self, master, on_account_created: Callable[[str], None], on_go_login: Callable[[], None]):
        super().__init__(master)
        self.on_account_created = on_account_created
        self.on_go_login = on_go_login
        # Política de senha
        self.MIN_LEN = 8

        self.columnconfigure(0, weight=1)

        self.title = tk.Label(self, text="Aria — Criar Conta", font=("Segoe UI", 18, "bold"))
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

        self.lbl_conf = tk.Label(form, text="Confirmar senha:")
        self.lbl_conf.grid(row=2, column=0, sticky="e", padx=(0, 8), pady=5)
        self.entry_conf = tk.Entry(form, show="•")
        self.entry_conf.grid(row=2, column=1, sticky="ew", pady=5)

        actions = tk.Frame(self)
        actions.grid(row=2, column=0, pady=10)

        self.btn_create = tk.Button(actions, text="Criar", width=12, command=self._create_account)
        self.btn_create.grid(row=0, column=0, padx=6)

        self.btn_back = tk.Button(actions, text="Voltar", width=12, command=self.on_go_login)
        self.btn_back.grid(row=0, column=1, padx=6)

        self.entry_user.focus_set()
        # Atalhos
        self.entry_user.bind("<Return>", lambda e: self._create_account())
        self.entry_pass.bind("<Return>", lambda e: self._create_account())
        self.entry_conf.bind("<Return>", lambda e: self._create_account())
        self.bind_all("<Escape>", lambda e: self.on_go_login())
        # Tooltips
        bind_tooltip(self.btn_create, "Criar conta com senha forte: 8+ caracteres, maiúscula, minúscula e número")
        bind_tooltip(self.btn_back, "Voltar ao login")

    def _create_account(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()
        confirm = self.entry_conf.get()

        if not username or not password:
            messagebox.showwarning("Campos obrigatórios", "Informe usuário e senha.")
            return

        if len(username) < 3:
            messagebox.showwarning("Validação", "Usuário deve ter pelo menos 3 caracteres.")
            return

        # Política de senha forte
        import re
        if len(password) < self.MIN_LEN or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password):
            messagebox.showwarning(
                "Senha fraca",
                f"A senha deve ter no mínimo {self.MIN_LEN} caracteres, incluindo maiúscula, minúscula e número.",
            )
            return

        if password != confirm:
            messagebox.showwarning("Validação", "As senhas não coincidem.")
            return

        if database.get_user_by_username(username):
            messagebox.showerror("Usuário existente", "Escolha outro nome de usuário.")
            return

        ph = security.hash_password(password)
        database.create_user(username, ph)
        messagebox.showinfo("Conta criada", "Cadastro efetuado com sucesso! Faça login.")
        self.on_account_created(username)

    def clear(self):
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)
        self.entry_conf.delete(0, tk.END)

    def apply_theme(self, c):
        self.configure(bg=c["BG"]) 
        for child in self.grid_slaves():
            if isinstance(child, tk.Frame):
                child.configure(bg=c["BG"]) 
        # titles/labels
        self.title.configure(bg=c["BG"], fg=c["TEXT"]) 
        self.lbl_user.configure(bg=c["BG"], fg=c["TEXT"]) 
        self.lbl_pass.configure(bg=c["BG"], fg=c["TEXT"]) 
        self.lbl_conf.configure(bg=c["BG"], fg=c["TEXT"]) 
        # entries
        for e in (self.entry_user, self.entry_pass, self.entry_conf):
            e.configure(bg=c["SURFACE"], fg=c["TEXT"], insertbackground=c["TEXT"]) 
        # buttons
        from .theme import style_primary_button, style_ghost_button
        style_primary_button(self.btn_create, c)
        style_ghost_button(self.btn_back, c)
