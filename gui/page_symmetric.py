# gui/page_symmetric.py — Giao diện trang Symmetric Encryption (DES / 3DES / AES)

import tkinter as tk
from gui.theme import *
from gui.widgets import (
    make_label, make_entry, make_textarea,
    make_btn, make_combo, make_card, make_divider,
    ResultBox, TabBar,
)


class SymmetricPage(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=PANEL, **kw)
        self._build()

    # ── Public references (controller sẽ dùng) ────────────────
    # Encrypt tab  : self.pt_input, self.enc_key_entry, self.algo_var, self.mode_var
    # Decrypt tab  : self.ct_input, self.dec_key_entry
    # Buttons      : self.btn_encrypt, self.btn_dec_decrypt, self.btn_gen_key
    # Result boxes : self.enc_result, self.dec_result

    def _build(self):
        # ── Top controls row ──────────────────────────────────
        ctrl = tk.Frame(self, bg=PANEL)
        ctrl.pack(fill="x", padx=24, pady=(20, 8))

        make_label(ctrl, "Thuật toán:", bg=PANEL, fg=MUTED,
                   font=FONT_LABEL).pack(side="left")
        self.algo_var = tk.StringVar(value="AES")
        make_combo(ctrl, ["AES", "3DES", "DES"],
                   textvariable=self.algo_var, width=8).pack(side="left", padx=(6, 20))

        make_label(ctrl, "Mode:", bg=PANEL, fg=MUTED,
                   font=FONT_LABEL).pack(side="left")
        self.mode_var = tk.StringVar(value="CBC")
        make_combo(ctrl, ["CBC", "ECB"],
                   textvariable=self.mode_var, width=6).pack(side="left", padx=6)

        # ── Tab bar ───────────────────────────────────────────
        self._tabbar = TabBar(self, on_switch=self._switch_tab)
        self._tabbar.pack(fill="x", padx=24, pady=(0, 4))

        # ── Panels ────────────────────────────────────────────
        self._enc_panel = self._build_enc_panel()
        self._dec_panel = self._build_dec_panel()

        self._tabbar.activate("enc")

    # ── Encrypt Panel ─────────────────────────────────────────
    def _build_enc_panel(self):
        panel = tk.Frame(self, bg=PANEL)

        # Plaintext card
        c1 = make_card(panel)
        c1.pack(fill="x", padx=24, pady=(8, 0))
        make_label(c1, "Plaintext").pack(anchor="w", padx=10, pady=(8, 2))
        self.pt_input = make_textarea(c1, height=3, mono=False)
        self.pt_input.pack(fill="x", padx=10, pady=(0, 10))

        # Key card
        c2 = make_card(panel)
        c2.pack(fill="x", padx=24, pady=(8, 0))

        key_hdr = tk.Frame(c2, bg=CARD)
        key_hdr.pack(fill="x", padx=10, pady=(8, 2))
        make_label(c2, "Secret Key (Hex)").pack(in_=key_hdr, side="left")
        self.btn_gen_key = make_btn(key_hdr, "⚡ Random Key",
                                    command=lambda: None,   # ← controller gán sau
                                    color=WARNING, padx=8, pady=3)
        self.btn_gen_key.pack(side="right")

        self.enc_key_entry = make_entry(c2, mono=True)
        self.enc_key_entry.pack(fill="x", padx=10, pady=(0, 4))

        self.key_hint_lbl = make_label(c2, "AES: 32/48/64 hex chars",
                                       fg=MUTED, font=FONT_LABEL)
        self.key_hint_lbl.pack(anchor="w", padx=10, pady=(0, 8))

        # Action row
        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(pady=10)
        self.btn_encrypt = make_btn(btn_row, "🔒  Mã Hoá",
                                    command=lambda: None,   # ← controller gán sau
                                    color=ACCENT, width=18)
        self.btn_encrypt.pack(side="left", padx=4)
        make_btn(btn_row, "✕  Xoá", command=self._clear_enc,
                 color=DANGER, width=10).pack(side="left", padx=4)

        # Result
        rc = tk.Frame(panel, bg=PANEL)
        rc.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.enc_result = ResultBox(rc, self.winfo_toplevel(), "Ciphertext (Hex)")
        self.enc_result.pack(fill="both", expand=True)

        return panel

    # ── Decrypt Panel ─────────────────────────────────────────
    def _build_dec_panel(self):
        panel = tk.Frame(self, bg=PANEL)

        c1 = make_card(panel)
        c1.pack(fill="x", padx=24, pady=(8, 0))
        make_label(c1, "Ciphertext (Hex)").pack(anchor="w", padx=10, pady=(8, 2))
        self.ct_input = make_textarea(c1, height=3, mono=True)
        self.ct_input.pack(fill="x", padx=10, pady=(0, 10))

        c2 = make_card(panel)
        c2.pack(fill="x", padx=24, pady=(8, 0))
        make_label(c2, "Secret Key (Hex)").pack(anchor="w", padx=10, pady=(8, 2))
        self.dec_key_entry = make_entry(c2, mono=True)
        self.dec_key_entry.pack(fill="x", padx=10, pady=(0, 10))

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(pady=10)
        self.btn_dec_decrypt = make_btn(btn_row, "🔓  Giải Mã",
                                        command=lambda: None,   # ← controller gán sau
                                        color=SUCCESS, width=18)
        self.btn_dec_decrypt.pack(side="left", padx=4)
        make_btn(btn_row, "✕  Xoá", command=self._clear_dec,
                 color=DANGER, width=10).pack(side="left", padx=4)

        rc = tk.Frame(panel, bg=PANEL)
        rc.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.dec_result = ResultBox(rc, self.winfo_toplevel(), "Plaintext gốc")
        self.dec_result.pack(fill="both", expand=True)

        return panel

    # ── Tab switching ─────────────────────────────────────────
    def _switch_tab(self, tab):
        self._enc_panel.pack_forget()
        self._dec_panel.pack_forget()
        if tab == "enc":
            self._enc_panel.pack(fill="both", expand=True)
        else:
            self._dec_panel.pack(fill="both", expand=True)

    # ── Clear helpers ─────────────────────────────────────────
    def _clear_enc(self):
        self.pt_input.delete("1.0", "end")
        self.enc_key_entry.delete(0, "end")
        self.enc_result.clear()

    def _clear_dec(self):
        self.ct_input.delete("1.0", "end")
        self.dec_key_entry.delete(0, "end")
        self.dec_result.clear()
