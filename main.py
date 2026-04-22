# main.py — Entry point của Cryptography Toolkit
# Chỉ khởi tạo cửa sổ, ghép sidebar + các trang lại với nhau.
# Logic crypto sẽ được gán vào các nút tại đây (controller layer).

import tkinter as tk
from gui.theme import BG, PANEL
from gui.sidebar import Sidebar
from gui.page_symmetric import SymmetricPage
from gui.page_asymmetric import AsymmetricPage
from gui.page_hash import HashPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cryptography Toolkit")
        self.geometry("920x700")
        self.minsize(780, 580)
        self.configure(bg=BG)
        self._build()

    def _build(self):
        # ── Sidebar ───────────────────────────────────────────
        self._sidebar = Sidebar(self, on_navigate=self._show_page)
        self._sidebar.pack(side="left", fill="y")

        # ── Content area ──────────────────────────────────────
        self._content = tk.Frame(self, bg=PANEL)
        self._content.pack(side="right", fill="both", expand=True)

        # ── Pages ─────────────────────────────────────────────
        self._pages = {
            "sym":  SymmetricPage(self._content),
            "asym": AsymmetricPage(self._content),
            "hash": HashPage(self._content),
        }

        # ── Wire up buttons (controller) ──────────────────────
        # TODO: Gán các hàm crypto vào đây sau khi implement logic
        # Ví dụ:
        #   sym = self._pages["sym"]
        #   sym.btn_encrypt.config(command=lambda: controller.sym_encrypt(sym))
        #   sym.btn_gen_key.config(command=lambda: controller.gen_key(sym))

        # ── Show trang đầu ────────────────────────────────────
        self._sidebar.activate("sym")

    def _show_page(self, key):
        for page in self._pages.values():
            page.pack_forget()
        self._pages[key].pack(fill="both", expand=True)


if __name__ == "__main__":
    App().mainloop()
