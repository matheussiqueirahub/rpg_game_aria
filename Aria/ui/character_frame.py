import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
import random

from .. import database
from .toast import show_toast
from .tooltip import bind_tooltip


HAIR_COLORS = ["Preto", "Castanho", "Loiro", "Ruivo", "Branco"]
HAIR_STYLES = ["Curto", "Médio", "Longo", "Raspado", "Coque"]
SKIN_TONES = ["Muito clara", "Clara", "Morena", "Escura"]
EYE_COLORS = ["Castanho", "Preto", "Azul", "Verde", "Cinza"]


def _color_map_skin(name: str) -> str:
    return {
        "Muito clara": "#ffdbac",
        "Clara": "#f1c27d",
        "Morena": "#c68642",
        "Escura": "#8d5524",
    }.get(name, "#f1c27d")


def _color_map_hair(name: str) -> str:
    return {
        "Preto": "#1f1f1f",
        "Castanho": "#6f4e37",
        "Loiro": "#d1b280",
        "Ruivo": "#a0522d",
        "Branco": "#e6e6e6",
    }.get(name, "#6f4e37")


def _color_map_eye(name: str) -> str:
    return {
        "Castanho": "#5a3e2b",
        "Preto": "#000000",
        "Azul": "#1e90ff",
        "Verde": "#228b22",
        "Cinza": "#708090",
    }.get(name, "#5a3e2b")


class CharacterFrame(tk.Frame):
    def __init__(self, master, get_current_user_id: Callable[[], Optional[int]], on_logout: Callable[[], None]):
        super().__init__(master)
        self.get_current_user_id = get_current_user_id
        self.on_logout = on_logout

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.title = tk.Label(self, text="Aria — Personalização", font=("Segoe UI", 18, "bold"))
        self.title.grid(row=0, column=0, pady=(20, 10))

        container = tk.Frame(self)
        container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # Formulário à esquerda
        form = tk.Frame(container)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        for i in range(3):
            form.columnconfigure(i, weight=1)

        # Nome
        self.lbl_name = tk.Label(form, text="Nome:")
        self.lbl_name.grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(form)
        self.entry_name.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)
        self.entry_name.bind("<KeyRelease>", lambda e: self._update_name_preview())

        # Atributos
        def make_scale(label, row):
            l = tk.Label(form, text=label)
            l.grid(row=row, column=0, sticky="w")
            var = tk.IntVar(value=5)
            val_label = tk.Label(form, text=str(var.get()), width=3, anchor="e")
            val_label.grid(row=row, column=2, sticky="e", pady=2)
            def on_change(v):
                val_label.configure(text=str(int(float(v))))
            scale = tk.Scale(form, from_=1, to=10, orient=tk.HORIZONTAL, variable=var, command=on_change, showvalue=False)
            scale.grid(row=row, column=1, sticky="ew", pady=2)
            return var, scale, l, val_label

        self.var_strength, self.scale_strength, self.lbl_strength, self.lbl_strength_val = make_scale("Força", 1)
        self.var_intelligence, self.scale_intelligence, self.lbl_intelligence, self.lbl_intelligence_val = make_scale("Inteligência", 2)
        self.var_agility, self.scale_agility, self.lbl_agility, self.lbl_agility_val = make_scale("Agilidade", 3)

        # Opções de aparência
        def make_option(label, values, row):
            lab = tk.Label(form, text=label)
            lab.grid(row=row, column=0, sticky="w")
            var = tk.StringVar(value=values[0])
            opt = tk.OptionMenu(form, var, *values, command=lambda _: self._redraw_preview())
            opt.grid(row=row, column=1, columnspan=2, sticky="ew", pady=2)
            return var, opt, lab

        self.var_hair_color, self.opt_hair_color, self.lbl_hair_color = make_option("Cor do cabelo", HAIR_COLORS, 4)
        self.var_hair_style, self.opt_hair_style, self.lbl_hair_style = make_option("Estilo do cabelo", HAIR_STYLES, 5)
        self.var_skin_tone, self.opt_skin_tone, self.lbl_skin_tone = make_option("Tom de pele", SKIN_TONES, 6)
        self.var_eye_color, self.opt_eye_color, self.lbl_eye_color = make_option("Cor dos olhos", EYE_COLORS, 7)

        # Ações
        actions = tk.Frame(form)
        actions.grid(row=8, column=0, columnspan=3, pady=(12, 0))
        self.btn_save = tk.Button(actions, text="Salvar", width=12, command=self._save)
        self.btn_save.grid(row=0, column=0, padx=6)
        self.btn_reset = tk.Button(actions, text="Resetar", width=12, command=self._reset_defaults)
        self.btn_reset.grid(row=0, column=1, padx=6)
        self.btn_random = tk.Button(actions, text="Aleatorizar", width=12, command=self._randomize)
        self.btn_random.grid(row=0, column=2, padx=6)
        self.btn_logout = tk.Button(actions, text="Sair", width=12, command=self.on_logout)
        self.btn_logout.grid(row=0, column=3, padx=6)

        # Tooltips
        bind_tooltip(self.btn_save, "Salvar alterações do personagem (Ctrl+S)")
        bind_tooltip(self.btn_reset, "Voltar aos valores padrão")
        bind_tooltip(self.btn_random, "Gerar valores e aparência aleatórios")
        bind_tooltip(self.btn_logout, "Sair da conta")

        # Preview à direita
        preview = tk.Frame(container)
        preview.grid(row=0, column=1, sticky="nsew")
        preview.columnconfigure(0, weight=1)
        preview.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(preview, width=300, height=320, highlightthickness=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.preview_name = tk.Label(preview, text="Aventureiro", font=("Segoe UI", 12, "bold"))
        self.preview_name.grid(row=1, column=0, pady=(8,0))

        self._redraw_preview()

    def on_show(self):
        # Carrega dados do usuário atual
        uid = self.get_current_user_id()
        if not uid:
            return
        ch = database.get_character_by_user(uid)
        if ch:
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, ch["name"] or "")
            self.scale_strength.set(int(ch["strength"]))
            self.scale_intelligence.set(int(ch["intelligence"]))
            self.scale_agility.set(int(ch["agility"]))
            self.var_hair_color.set(ch["hair_color"])
            self.var_hair_style.set(ch["hair_style"])
            self.var_skin_tone.set(ch["skin_tone"])
            self.var_eye_color.set(ch["eye_color"])
        else:
            # Defaults
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, "Aventureiro")
            self.scale_strength.set(5)
            self.scale_intelligence.set(5)
            self.scale_agility.set(5)
            self.var_hair_color.set(HAIR_COLORS[1])
            self.var_hair_style.set(HAIR_STYLES[0])
            self.var_skin_tone.set(SKIN_TONES[1])
            self.var_eye_color.set(EYE_COLORS[0])
        self._update_name_preview()
        self._redraw_preview()
        # Atalhos
        try:
            self.bind_all("<Control-s>", lambda e: self._save())
            self.bind_all("<Escape>", lambda e: self.on_logout())
        except Exception:
            pass

    def _save(self):
        uid = self.get_current_user_id()
        if not uid:
            messagebox.showerror("Sessão expirada", "Faça login novamente.")
            return
        data = {
            "name": self.entry_name.get().strip() or "Aventureiro",
            "strength": int(self.scale_strength.get()),
            "intelligence": int(self.scale_intelligence.get()),
            "agility": int(self.scale_agility.get()),
            "hair_color": self.var_hair_color.get(),
            "hair_style": self.var_hair_style.get(),
            "skin_tone": self.var_skin_tone.get(),
            "eye_color": self.var_eye_color.get(),
        }
        try:
            database.upsert_character(uid, data)
            show_toast(self, "Personagem salvo!")
        except Exception as exc:
            messagebox.showerror("Erro ao salvar", str(exc))

    def _redraw_preview(self):
        self.canvas.delete("all")
        w = int(self.canvas["width"]) 
        h = int(self.canvas["height"]) 
        cx, cy = w // 2, h // 2

        skin = _color_map_skin(self.var_skin_tone.get())
        hair = _color_map_hair(self.var_hair_color.get())
        eye = _color_map_eye(self.var_eye_color.get())
        style = self.var_hair_style.get()

        # Cabeça
        self.canvas.create_oval(cx-60, cy-80, cx+60, cy+60, fill=skin, outline="#555555")

        # Cabelo (simples), baseado no estilo
        if style in ("Curto", "Médio"):
            self.canvas.create_arc(cx-70, cy-110, cx+70, cy+40, start=0, extent=180, fill=hair, outline=hair)
        elif style == "Longo":
            self.canvas.create_arc(cx-70, cy-110, cx+70, cy+40, start=0, extent=180, fill=hair, outline=hair)
            self.canvas.create_rectangle(cx-70, cy+10, cx+70, cy+60, fill=hair, outline=hair)
        elif style == "Raspado":
            self.canvas.create_arc(cx-65, cy-95, cx+65, cy+10, start=0, extent=180, fill=hair, outline=hair)
        elif style == "Coque":
            self.canvas.create_arc(cx-70, cy-110, cx+70, cy+40, start=0, extent=180, fill=hair, outline=hair)
            self.canvas.create_oval(cx-15, cy-110, cx+15, cy-85, fill=hair, outline=hair)

        # Olhos
        self.canvas.create_oval(cx-30, cy-20, cx-10, cy, fill="#ffffff", outline="#333333")
        self.canvas.create_oval(cx+10, cy-20, cx+30, cy, fill="#ffffff", outline="#333333")
        self.canvas.create_oval(cx-24, cy-14, cx-16, cy-6, fill=eye, outline=eye)
        self.canvas.create_oval(cx+16, cy-14, cx+24, cy-6, fill=eye, outline=eye)

        # Boca
        self.canvas.create_arc(cx-25, cy+10, cx+25, cy+35, start=200, extent=140, style=tk.ARC, outline="#aa3333", width=2)

    def _update_name_preview(self):
        name = self.entry_name.get().strip() or "Aventureiro"
        self.preview_name.configure(text=name)

    def _reset_defaults(self):
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, "Aventureiro")
        self.scale_strength.set(5)
        self.scale_intelligence.set(5)
        self.scale_agility.set(5)
        self.var_hair_color.set(HAIR_COLORS[1])
        self.var_hair_style.set(HAIR_STYLES[0])
        self.var_skin_tone.set(SKIN_TONES[1])
        self.var_eye_color.set(EYE_COLORS[0])
        self._update_name_preview()
        self._redraw_preview()

    def _randomize(self):
        if not self.entry_name.get().strip():
            self.entry_name.insert(0, "Aventureiro")
        self.scale_strength.set(random.randint(1, 10))
        self.scale_intelligence.set(random.randint(1, 10))
        self.scale_agility.set(random.randint(1, 10))
        self.var_hair_color.set(random.choice(HAIR_COLORS))
        self.var_hair_style.set(random.choice(HAIR_STYLES))
        self.var_skin_tone.set(random.choice(SKIN_TONES))
        self.var_eye_color.set(random.choice(EYE_COLORS))
        self._update_name_preview()
        self._redraw_preview()

    def apply_theme(self, c):
        # Containers
        self.configure(bg=c["BG"]) 
        for w in self.grid_slaves():
            if isinstance(w, tk.Frame):
                w.configure(bg=c["BG"]) 
        # Labels
        self.title.configure(bg=c["BG"], fg=c["TEXT"]) 
        for lbl in (self.lbl_name, self.lbl_strength, self.lbl_intelligence, self.lbl_agility,
                    self.lbl_hair_color, self.lbl_hair_style, self.lbl_skin_tone, self.lbl_eye_color,
                    self.lbl_strength_val, self.lbl_intelligence_val, self.lbl_agility_val):
            lbl.configure(bg=c["BG"], fg=c["TEXT"]) 
        # Entry
        self.entry_name.configure(bg=c["SURFACE"], fg=c["TEXT"], insertbackground=c["TEXT"]) 
        # OptionMenus
        for opt in (self.opt_hair_color, self.opt_hair_style, self.opt_skin_tone, self.opt_eye_color):
            opt.configure(bg=c["SURFACE"], fg=c["TEXT"], activebackground=c["BORDER"], activeforeground=c["TEXT"], highlightthickness=0)
            try:
                m = opt.nametowidget(opt["menu"])  # resolve o menu interno
                m.configure(bg=c["SURFACE"], fg=c["TEXT"]) 
            except Exception:
                pass
        # Canvas
        self.canvas.configure(bg=c["CANVAS_BG"], highlightbackground=c["BORDER"]) 
        self.preview_name.configure(bg=c["BG"], fg=c["TEXT"]) 
        # Buttons
        from .theme import style_primary_button, style_secondary_button, style_ghost_button
        style_primary_button(self.btn_save, c)
        style_ghost_button(self.btn_reset, c)
        style_secondary_button(self.btn_random, c)
        style_ghost_button(self.btn_logout, c)
