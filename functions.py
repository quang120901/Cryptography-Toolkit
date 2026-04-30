import hashlib
import os

from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad

# ── Bảng ánh xạ thuật toán → module + kích thước key/block ──────────────
_ALGO_MAP = {
    "DES":  {"mod": DES,  "key_sizes": [8],          "block": 8},
    "3DES": {"mod": DES3, "key_sizes": [16, 24],     "block": 8},
    "AES":  {"mod": AES,  "key_sizes": [16, 24, 32], "block": 16},
}


def gen_sym_key(page):
    """Tạo key ngẫu nhiên phù hợp với thuật toán đang chọn,
    rồi điền vào ô key (cả tab Encrypt và Decrypt)."""
    algo = page.algo_var.get()
    info = _ALGO_MAP[algo]

    # Chọn key size lớn nhất mặc định (bảo mật cao nhất)
    key_len = info["key_sizes"][-1]
    key_hex = os.urandom(key_len).hex()

    # Điền vào ô key encrypt
    page.enc_key_entry.delete(0, "end")
    page.enc_key_entry.insert(0, key_hex)

    # Điền vào ô key decrypt (tiện cho test)
    page.dec_key_entry.delete(0, "end")
    page.dec_key_entry.insert(0, key_hex)

    # Cập nhật hint
    _update_key_hint(page, algo)


def sym_encrypt(page):
    """
    Đọc Plaintext + Key từ GUI → mã hoá → trả Ciphertext (hex) lên GUI.

    - Mode CBC: tự sinh IV ngẫu nhiên, prepend IV vào đầu ciphertext.
    - Mode ECB: không cần IV.
    - Plaintext được pad theo PKCS#7 trước khi mã hoá.
    """
    algo = page.algo_var.get()
    mode = page.mode_var.get()
    key_hex = page.enc_key_entry.get().strip()
    plaintext = page.pt_input.get("1.0", "end").strip()

    #- Validate
    if not plaintext:
        page.enc_result.set("Plaintext không được để trống!", color="#ef4444")
        return

    if not key_hex:
        page.enc_result.set("Key không được để trống!", color="#ef4444")
        return

    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        page.enc_result.set("Key phải là chuỗi Hex hợp lệ!", color="#ef4444")
        return

    info = _ALGO_MAP[algo]

    if len(key) not in info["key_sizes"]:
        sizes = ", ".join(str(s * 2) for s in info["key_sizes"])
        page.enc_result.set(
            f"⚠ {algo} yêu cầu key dài {sizes} ký tự hex "
            f"(hiện tại: {len(key_hex)})",
            color="#ef4444"
        )
        return

    #- Encrypt 
    try:
        block_size = info["block"]
        data = pad(plaintext.encode("utf-8"), block_size)

        if mode == "CBC":
            iv = os.urandom(block_size)
            cipher = info["mod"].new(key, info["mod"].MODE_CBC, iv)
            ct = iv + cipher.encrypt(data)          # IV ∥ Ciphertext
        else:  # ECB
            cipher = info["mod"].new(key, info["mod"].MODE_ECB)
            ct = cipher.encrypt(data)

        page.enc_result.set(ct.hex(), color="#10b981")

    except Exception as e:
        page.enc_result.set(f"Lỗi mã hoá: {e}", color="#ef4444")


def sym_decrypt(page):
    """
    Đọc Ciphertext (hex) + Key từ GUI → giải mã → trả Plaintext gốc.

    - Mode CBC: tách IV từ đầu ciphertext.
    - Mode ECB: giải mã trực tiếp.
    - Sau giải mã, unpad PKCS#7.
    """
    algo = page.algo_var.get()
    mode = page.mode_var.get()
    key_hex = page.dec_key_entry.get().strip()
    ct_hex = page.ct_input.get("1.0", "end").strip()

    #- Validate 
    if not ct_hex:
        page.dec_result.set("Ciphertext không được để trống!", color="#ef4444")
        return

    if not key_hex:
        page.dec_result.set("Key không được để trống!", color="#ef4444")
        return

    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        page.dec_result.set("Key phải là chuỗi Hex hợp lệ!", color="#ef4444")
        return

    try:
        ct = bytes.fromhex(ct_hex)
    except ValueError:
        page.dec_result.set("Ciphertext phải là chuỗi Hex hợp lệ!", color="#ef4444")
        return

    info = _ALGO_MAP[algo]

    if len(key) not in info["key_sizes"]:
        sizes = ", ".join(str(s * 2) for s in info["key_sizes"])
        page.dec_result.set(
            f"{algo} yêu cầu key dài {sizes} ký tự hex "
            f"(hiện tại: {len(key_hex)})",
            color="#ef4444"
        )
        return

    #- Decrypt 
    try:
        block_size = info["block"]

        if mode == "CBC":
            if len(ct) < block_size:
                page.dec_result.set(
                    "Ciphertext quá ngắn (thiếu IV)!", color="#ef4444"
                )
                return
            iv = ct[:block_size]
            ct_body = ct[block_size:]
            cipher = info["mod"].new(key, info["mod"].MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ct_body), block_size)
        else:  # ECB
            cipher = info["mod"].new(key, info["mod"].MODE_ECB)
            plaintext = unpad(cipher.decrypt(ct), block_size)

        page.dec_result.set(plaintext.decode("utf-8"), color="#10b981")

    except ValueError as e:
        page.dec_result.set(
            f"Giải mã thất bại — sai key hoặc dữ liệu bị hỏng.\n({e})",
            color="#ef4444"
        )
    except Exception as e:
        page.dec_result.set(f"Lỗi giải mã: {e}", color="#ef4444")


#- Tiện ích nội bộ
def _update_key_hint(page, algo):
    """Cập nhật text gợi ý key length trên GUI."""
    mapping = {
        "DES":  "DES: 16 hex chars  (8 bytes)",
        "3DES": "3DES: 32 hoặc 48 hex chars  (16/24 bytes)",
        "AES":  "AES: 32 / 48 / 64 hex chars  (16/24/32 bytes)",
    }
    try:
        page.key_hint_lbl.config(text=mapping.get(algo, ""))
    except AttributeError:
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
    text = page.txt_input.get("1.0", "end").strip()
    algo = page.hash_algo_var.get()

    if not text:
        page.hash_result.set("Input rỗng")
        return

    if algo == "MD5":
        result = hashlib.md5(text.encode()).hexdigest()
    else:
        result = hashlib.sha256(text.encode()).hexdigest()

    page.hash_result.set(result)
