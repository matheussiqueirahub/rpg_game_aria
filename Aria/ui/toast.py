import tkinter as tk


def show_toast(root: tk.Widget, text: str, duration: int = 1500):
    try:
        master = root.winfo_toplevel()
        x = master.winfo_rootx() + master.winfo_width() - 320
        y = master.winfo_rooty() + master.winfo_height() - 100
    except Exception:
        x = 100
        y = 100

    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)
    toast.geometry(f"300x40+{x}+{y}")

    frame = tk.Frame(toast, bg="#333333")
    frame.pack(fill=tk.BOTH, expand=True)
    lbl = tk.Label(frame, text=text, bg="#333333", fg="#FFFFFF", font=("Segoe UI", 9))
    lbl.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

    # Auto-destroy
    toast.after(duration, toast.destroy)

