# gui/widgets.py — Các widget tái sử dụng

import tkinter as tk
from tkinter import ttk
from gui.theme import *


def make_label(parent, text, fg=TEXT, font=FONT_BODY, bg=CARD, **kw):
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=font, **kw)


def make_entry(parent, textvariable=None, mono=False, **kw):
    return tk.Entry(
        parent,
        textvariable=textvariable,
        bg=BTN_BG, fg=TEXT,
        insertbackground=ACCENT,
        relief="flat", bd=0,
        font=FONT_MONO if mono else FONT_BODY,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        **kw
    )


def make_textarea(parent, height=4, mono=True, **kw):
    return tk.Text(
        parent,
        height=height,
        bg=BTN_BG, fg=TEXT,
        insertbackground=ACCENT,
        relief="flat", bd=0,
        font=FONT_MONO if mono else FONT_BODY,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        wrap="word",
        **kw
    )


def make_btn(parent, text, command, color=ACCENT, width=None, padx=12, pady=6, **kw):
    b = tk.Button(
        parent, text=text, command=command,
        bg=BTN_BG, fg=color,
        activebackground=BORDER, activeforeground=color,
        relief="flat", bd=0, cursor="hand2",
        font=FONT_BTN, padx=padx, pady=pady,
        highlightthickness=1,
        highlightbackground=color,
        **kw
    )
    if width:
        b.configure(width=width)
    b.bind("<Enter>", lambda e: b.config(bg=color, fg=BG))
    b.bind("<Leave>", lambda e: b.config(bg=BTN_BG, fg=color))
    return b


def make_combo(parent, values, textvariable=None, **kw):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.TCombobox",
                    fieldbackground=BTN_BG, background=BTN_BG,
                    foreground=TEXT, selectforeground=TEXT,
                    selectbackground=BTN_BG, arrowcolor=ACCENT)
    return ttk.Combobox(
        parent, values=values,
        textvariable=textvariable,
        style="Dark.TCombobox",
        state="readonly",
        font=FONT_BODY,
        **kw
    )


def make_divider(parent):
    return tk.Frame(parent, bg=BORDER, height=1)


def make_card(parent, **kw):
    return tk.Frame(parent, bg=CARD, **kw)


class ResultBox(tk.Frame):
    """Ô hiển thị kết quả chỉ đọc kèm nút Copy."""

    def __init__(self, parent, root_ref, label_text="Kết quả", **kw):
        super().__init__(parent, bg=CARD, **kw)
        self._root = root_ref

        hdr = tk.Frame(self, bg=CARD)
        hdr.pack(fill="x", pady=(0, 4))

        if label_text:
            tk.Label(hdr, text=label_text, bg=CARD, fg=MUTED,
                     font=FONT_LABEL).pack(side="left")

        make_btn(hdr, "⎘ Copy", self._copy,
                 color=SUCCESS, padx=6, pady=2).pack(side="right")

        self._txt = make_textarea(self, height=3)
        self._txt.pack(fill="both", expand=True)
        self._txt.config(state="disabled")

    def set(self, value, color=TEXT):
        self._txt.config(state="normal", fg=color)
        self._txt.delete("1.0", "end")
        self._txt.insert("end", value)
        self._txt.config(state="disabled")

    def clear(self):
        self._txt.config(state="normal")
        self._txt.delete("1.0", "end")
        self._txt.config(state="disabled")

    def get(self):
        return self._txt.get("1.0", "end").strip()

    def _copy(self):
        text = self.get()
        self._root.clipboard_clear()
        self._root.clipboard_append(text)
        self._root.update()


class TabBar(tk.Frame):
    """Thanh tab đơn giản với 2 nút Mã hoá / Giải mã."""

    def __init__(self, parent, on_switch, **kw):
        super().__init__(parent, bg=PANEL, **kw)
        self._on_switch = on_switch

        self.enc_btn = make_btn(self, "🔒  Mã hoá",
                                lambda: self._switch("enc"),
                                color=ACCENT, width=14)
        self.enc_btn.pack(side="left", padx=(0, 4))

        self.dec_btn = make_btn(self, "🔓  Giải mã",
                                lambda: self._switch("dec"),
                                color=MUTED, width=14)
        self.dec_btn.pack(side="left")

        self._active = None

    def _switch(self, tab):
        if tab == "enc":
            self.enc_btn.config(fg=ACCENT, highlightbackground=ACCENT)
            self.dec_btn.config(fg=MUTED,  highlightbackground=BORDER)
        else:
            self.dec_btn.config(fg=SUCCESS, highlightbackground=SUCCESS)
            self.enc_btn.config(fg=MUTED,   highlightbackground=BORDER)
        self._active = tab
        self._on_switch(tab)

    def activate(self, tab):
        self._switch(tab)