# gui/page_asymmetric.py — Giao diện trang Asymmetric Encryption (RSA)

import tkinter as tk
from gui.theme import *
from gui.widgets import (
    make_label, make_textarea, make_btn,
    make_card, make_divider,
    ResultBox, TabBar,
)


class AsymmetricPage(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=PANEL, **kw)
        self._build()

    # ── Public references (controller sẽ dùng) ─────────────────
    # Key section  : self.btn_gen_keys, self.pub_box, self.priv_box
    # Encrypt tab  : self.rsa_pt_input, self.rsa_pubkey_input, self.btn_rsa_encrypt
    # Decrypt tab  : self.rsa_ct_input, self.rsa_privkey_input, self.btn_rsa_decrypt
    # Result boxes : self.rsa_enc_result, self.rsa_dec_result

    def _build(self):
        # ── Key generation section ────────────────────────────
        kf = make_card(self)
        kf.pack(fill="x", padx=24, pady=(20, 0))

        hdr = tk.Frame(kf, bg=CARD)
        hdr.pack(fill="x", padx=10, pady=(10, 6))

        make_label(kf, "RSA Key Pair", font=FONT_HEAD).pack(in_=hdr, side="left")

        self.btn_gen_keys = make_btn(kf, "⚡  Tạo Key Pair Ngẫu Nhiên",
                                     command=lambda: None,   # ← controller gán sau
                                     color=WARNING)
        self.btn_gen_keys.pack(padx=10, pady=(0, 8))

        # Key display (2 cột)
        keys_row = tk.Frame(kf, bg=CARD)
        keys_row.pack(fill="x", padx=10, pady=(0, 10))
        keys_row.columnconfigure(0, weight=1)
        keys_row.columnconfigure(1, weight=1)

        lf = tk.Frame(keys_row, bg=CARD)
        lf.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        make_label(lf, "Public Key (PEM)", fg=MUTED,
                   font=FONT_LABEL).pack(anchor="w")
        self.pub_box = ResultBox(lf, self.winfo_toplevel(), "")
        self.pub_box.pack(fill="both", expand=True)

        rf = tk.Frame(keys_row, bg=CARD)
        rf.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        make_label(rf, "Private Key (PEM)", fg=MUTED,
                   font=FONT_LABEL).pack(anchor="w")
        self.priv_box = ResultBox(rf, self.winfo_toplevel(), "")
        self.priv_box.pack(fill="both", expand=True)

        make_divider(self).pack(fill="x", padx=24, pady=14)

        # ── Tab bar ───────────────────────────────────────────
        self._tabbar = TabBar(self, on_switch=self._switch_tab)
        self._tabbar.pack(fill="x", padx=24, pady=(0, 4))

        self._enc_panel = self._build_enc_panel()
        self._dec_panel = self._build_dec_panel()

        self._tabbar.activate("enc")

    # ── Encrypt Panel ─────────────────────────────────────────
    def _build_enc_panel(self):
        panel = tk.Frame(self, bg=PANEL)

        c = make_card(panel)
        c.pack(fill="x", padx=24, pady=(8, 0))

        make_label(c, "Plaintext").pack(anchor="w", padx=10, pady=(8, 2))
        self.rsa_pt_input = make_textarea(c, height=3, mono=False)
        self.rsa_pt_input.pack(fill="x", padx=10, pady=(0, 6))

        make_label(c, "Public Key (PEM)").pack(anchor="w", padx=10, pady=(6, 2))
        self.rsa_pubkey_input = make_textarea(c, height=4, mono=True)
        self.rsa_pubkey_input.pack(fill="x", padx=10, pady=(0, 10))

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(pady=10)
        self.btn_rsa_encrypt = make_btn(btn_row, "🔒  Mã Hoá RSA",
                                        command=lambda: None,   # ← controller gán sau
                                        color=ACCENT, width=18)
        self.btn_rsa_encrypt.pack(side="left", padx=4)
        make_btn(btn_row, "✕  Xoá", command=self._clear_enc,
                 color=DANGER, width=10).pack(side="left", padx=4)

        rc = tk.Frame(panel, bg=PANEL)
        rc.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.rsa_enc_result = ResultBox(rc, self.winfo_toplevel(), "Ciphertext (Base64)")
        self.rsa_enc_result.pack(fill="both", expand=True)

        return panel

    # ── Decrypt Panel ─────────────────────────────────────────
    def _build_dec_panel(self):
        panel = tk.Frame(self, bg=PANEL)

        c = make_card(panel)
        c.pack(fill="x", padx=24, pady=(8, 0))

        make_label(c, "Ciphertext (Base64)").pack(anchor="w", padx=10, pady=(8, 2))
        self.rsa_ct_input = make_textarea(c, height=3, mono=True)
        self.rsa_ct_input.pack(fill="x", padx=10, pady=(0, 6))

        make_label(c, "Private Key (PEM)").pack(anchor="w", padx=10, pady=(6, 2))
        self.rsa_privkey_input = make_textarea(c, height=4, mono=True)
        self.rsa_privkey_input.pack(fill="x", padx=10, pady=(0, 10))

        btn_row = tk.Frame(panel, bg=PANEL)
        btn_row.pack(pady=10)
        self.btn_rsa_decrypt = make_btn(btn_row, "🔓  Giải Mã RSA",
                                        command=lambda: None,   # ← controller gán sau
                                        color=SUCCESS, width=18)
        self.btn_rsa_decrypt.pack(side="left", padx=4)
        make_btn(btn_row, "✕  Xoá", command=self._clear_dec,
                 color=DANGER, width=10).pack(side="left", padx=4)

        rc = tk.Frame(panel, bg=PANEL)
        rc.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        self.rsa_dec_result = ResultBox(rc, self.winfo_toplevel(), "Plaintext gốc")
        self.rsa_dec_result.pack(fill="both", expand=True)

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
        self.rsa_pt_input.delete("1.0", "end")
        self.rsa_pubkey_input.delete("1.0", "end")
        self.rsa_enc_result.clear()

    def _clear_dec(self):
        self.rsa_ct_input.delete("1.0", "end")
        self.rsa_privkey_input.delete("1.0", "end")
        self.rsa_dec_result.clear()