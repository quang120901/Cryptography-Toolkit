# gui/sidebar.py — Sidebar điều hướng

import tkinter as tk
from gui.theme import *
from gui.widgets import make_divider


class Sidebar(tk.Frame):
    def __init__(self, parent, on_navigate, **kw):
        super().__init__(parent, bg=PANEL, width=200, **kw)
        self.pack_propagate(False)
        self._on_navigate = on_navigate
        self._btns = {}
        self._build()

    def _build(self):
        # ── Logo ──────────────────────────────────────────────
        tk.Label(self, text="🔐", bg=PANEL,
                 font=("Segoe UI", 28)).pack(pady=(24, 2))
        tk.Label(self, text="Crypto", bg=PANEL, fg=ACCENT,
                 font=("Segoe UI", 16, "bold")).pack()
        tk.Label(self, text="Toolkit", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 11)).pack()

        make_divider(self).pack(fill="x", padx=16, pady=18)

        # ── Nav items ─────────────────────────────────────────
        nav_items = [
            ("sym",  "🔑", "Symmetric"),
            ("asym", "🗝", "Asymmetric\n(RSA)"),
            ("hash", "#",  "Hash\nFunctions"),
        ]
        for key, icon, label in nav_items:
            b = tk.Button(
                self,
                text=f" {icon}  {label}",
                command=lambda k=key: self._navigate(k),
                bg=PANEL, fg=MUTED,
                activebackground=BTN_BG, activeforeground=ACCENT,
                relief="flat", bd=0, cursor="hand2",
                font=("Segoe UI", 10),
                anchor="w", justify="left",
                padx=20, pady=10
            )
            b.pack(fill="x", padx=8, pady=2)
            self._btns[key] = b

        # ── Footer ────────────────────────────────────────────
        tk.Label(self, text="v1.0  •  pycryptodome",
                 bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="bottom", pady=12)

    def _navigate(self, key):
        for k, b in self._btns.items():
            b.config(bg=PANEL if k != key else BTN_BG,
                     fg=ACCENT if k == key else MUTED)
        self._on_navigate(key)

    def activate(self, key):
        self._navigate(key)
