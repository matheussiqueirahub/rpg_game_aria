import tkinter as tk


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str, wait: int = 350):
        self.widget = widget
        self.text = text
        self.wait = wait
        self._after_id = None
        self._tip = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<ButtonPress>", self._hide)

    def _schedule(self, _=None):
        self._cancel()
        self._after_id = self.widget.after(self.wait, self._show)

    def _cancel(self):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        if self._tip:
            return
        try:
            x = self.widget.winfo_rootx() + 12
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        except Exception:
            x, y = 100, 100
        self._tip = tk.Toplevel(self.widget)
        self._tip.overrideredirect(True)
        self._tip.attributes("-topmost", True)
        self._tip.geometry(f"240x30+{x}+{y}")
        frame = tk.Frame(self._tip, bg="#333333")
        frame.pack(fill=tk.BOTH, expand=True)
        lbl = tk.Label(frame, text=self.text, bg="#333333", fg="#FFFFFF", font=("Segoe UI", 9), wraplength=220, justify="left")
        lbl.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

    def _hide(self, _=None):
        self._cancel()
        if self._tip:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None


def bind_tooltip(widget: tk.Widget, text: str):
    ToolTip(widget, text)

