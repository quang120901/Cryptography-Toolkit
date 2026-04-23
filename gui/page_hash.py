# gui/page_hash.py — Giao diện trang Hash Functions (MD5 / SHA-256)

import tkinter as tk
from gui.theme import *
from gui.widgets import (
    make_label, make_textarea,
    make_btn, make_card,
    ResultBox,
)


class HashPage(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=PANEL, **kw)
        self._build()

    # ── Public references (controller sẽ dùng) ────────────────
    # Input       : self.txt_input, self.hash_algo_var
    # Buttons     : self.btn_hash
    # Result box  : self.hash_result

    def _build(self):
        # ── Input card ────────────────────────────────────────
        c = make_card(self)
        c.pack(fill="x", padx=24, pady=(20, 0))

        make_label(c, "Văn bản cần Hash", font=FONT_HEAD).pack(
            anchor="w", padx=10, pady=(10, 4))

        self.txt_input = make_textarea(c, height=5, mono=False)
        self.txt_input.pack(fill="x", padx=10, pady=(0, 10))

        # ── Algorithm selector ────────────────────────────────
        algo_row = tk.Frame(c, bg=CARD)
        algo_row.pack(fill="x", padx=10, pady=(0, 10))

        make_label(algo_row, "Thuật toán:", bg=CARD, fg=MUTED,
                   font=FONT_LABEL).pack(side="left")

        self.hash_algo_var = tk.StringVar(value="SHA-256")
        for algo in ["MD5", "SHA-256"]:
            tk.Radiobutton(
                algo_row, text=algo,
                variable=self.hash_algo_var, value=algo,
                bg=CARD, fg=TEXT,
                activebackground=CARD, activeforeground=ACCENT,
                selectcolor=BTN_BG,
                font=FONT_BODY
            ).pack(side="left", padx=10)

        # ── Action buttons ────────────────────────────────────
        btn_row = tk.Frame(self, bg=PANEL)
        btn_row.pack(pady=14)

        self.btn_hash = make_btn(btn_row, "# Hash",
                                 command=lambda: None,   # ← controller gán sau
                                 color=ACCENT, width=18)
        self.btn_hash.pack(side="left", padx=4)

        make_btn(btn_row, "✕  Xoá", command=self._clear,
                 color=DANGER, width=10).pack(side="left", padx=4)

        # ── Result box ────────────────────────────────────────
        res = tk.Frame(self, bg=PANEL)
        res.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.hash_result = ResultBox(res, self.winfo_toplevel(), "Hash Value (Digest)")
        self.hash_result.pack(fill="both", expand=True)

    # ── Clear helper ──────────────────────────────────────────
    def _clear(self):
        self.txt_input.delete("1.0", "end")
        self.hash_result.clear()