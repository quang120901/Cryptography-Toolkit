
def sym_encrypt(page):
    """
    Đọc input từ GUI → xử lý → trả kết quả lên GUI.
    
    Lấy dữ liệu:
        algo     = page.algo_var.get()       # "AES" | "3DES" | "DES"
        mode     = page.mode_var.get()       # "CBC" | "ECB"
        key      = page.enc_key_entry.get()  # hex string
        text     = page.pt_input.get("1.0", "end").strip()
    
    Trả kết quả:
        page.enc_result.set("kết quả ở đây", color=SUCCESS)  # thành công
        page.enc_result.set("lỗi...",         color=DANGER)   # thất bại
    """
    pass  # ← implement tại đây


def sym_decrypt(page):
    """
    Lấy dữ liệu:
        algo = page.algo_var.get()
        mode = page.mode_var.get()
        key  = page.dec_key_entry.get()
        ct   = page.ct_input.get("1.0", "end").strip()
    
    Trả kết quả:
        page.dec_result.set(...)
    """
    pass


def gen_sym_key(page):
    """Tạo key ngẫu nhiên rồi điền vào ô key."""
    pass


def rsa_gen_keys(page):
    """
    Lấy dữ liệu:
        bits = int(page.bits_var.get())
    
    Trả kết quả:
        page.pub_box.set(public_key_pem)
        page.priv_box.set(private_key_pem)
    """
    pass


def rsa_encrypt(page):
    """..."""
    pass


def rsa_decrypt(page):
    """..."""
    pass


def hash_now(page):
    """
    Lấy dữ liệu:
        text = page.txt_input.get("1.0", "end").strip()
        algo = page.hash_algo_var.get()   # "MD5" | "SHA-256"
    
    Trả kết quả:
        page.md5_result.set(...)
        page.sha_result.set(...)
    """
    pass


def hash_both(page):
    """Tính cả MD5 lẫn SHA-256 cùng lúc."""
    pass