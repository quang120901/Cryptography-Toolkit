# 🔐 Cryptography Toolkit — Nhóm 14

## 📌 Tổng quan

Dự án xây dựng ứng dụng **Cryptography Toolkit** dưới dạng GUI Desktop App bằng Python + Tkinter, cho phép người dùng thực hành các kỹ thuật mã hoá cơ bản gồm: mã hoá đối xứng, mã hoá bất đối xứng và hàm băm.

---

## 📁 Cấu trúc dự án

```
CryptographyToolkit/
├── main.py              ← Entry point, khởi động app & gán controller
├── functions.py         ← Toàn bộ logic crypto (symmetric, RSA, hash)
├── requirements.txt     ← Danh sách thư viện cần cài
├── README.md
└── gui/
    ├── theme.py         ← Màu sắc, font, hằng số giao diện
    ├── widgets.py       ← Các widget tái sử dụng (Button, Entry, ResultBox...)
    ├── sidebar.py       ← Sidebar điều hướng
    ├── page_symmetric.py   ← Giao diện trang Symmetric (DES / 3DES / AES)
    ├── page_asymmetric.py  ← Giao diện trang Asymmetric (RSA)
    └── page_hash.py        ← Giao diện trang Hash (MD5 / SHA-256)
```

---

## ⚙️ Cài đặt

**Yêu cầu:** Python 3.8+

```bash
# 1. Clone repo
git clone https://github.com/quang120901/Cryptography-Toolkit.git
cd CryptographyToolkit

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy ứng dụng
python main.py
```

---

## 🚀 Hướng dẫn sử dụng

Sau khi chạy `main.py`, giao diện hiện ra với sidebar điều hướng gồm 3 trang:

### 🔑 1. Symmetric Encryption

| Trường | Mô tả |
|--------|-------|
| Thuật toán | Chọn DES / 3DES / AES |
| Mode | Chọn CBC hoặc ECB |
| Plaintext | Nhập văn bản cần mã hoá |
| Secret Key | Nhập key dạng Hex hoặc nhấn **⚡ Random Key** |

- Tab **Mã hoá**: Nhập Plaintext + Key → nhận Ciphertext (hex)
- Tab **Giải mã**: Nhập Ciphertext + Key → nhận Plaintext gốc

> **Độ dài Key theo thuật toán:**
> - DES: 16 hex chars (8 bytes)
> - 3DES: 32 hoặc 48 hex chars (16/24 bytes)
> - AES: 32 / 48 / 64 hex chars (16/24/32 bytes)

---

### 🗝 2. Asymmetric Encryption (RSA)

1. Nhấn **⚡ Tạo Key Pair Ngẫu Nhiên** → Public Key và Private Key (PEM) hiện ra
2. Tab **Mã hoá**: Nhập Plaintext + Public Key → nhận Ciphertext (Base64)
3. Tab **Giải mã**: Nhập Ciphertext + Private Key → nhận Plaintext gốc

---

### # 3. Hash Functions

1. Nhập văn bản bất kỳ
2. Chọn thuật toán: **MD5** hoặc **SHA-256**
3. Nhấn **# Hash** → nhận Hash Value (Digest)

---

## 📚 Thư viện sử dụng

| Thư viện | Mục đích |
|----------|----------|
| `tkinter` | Xây dựng giao diện GUI (có sẵn trong Python) |
| `pycryptodome` | Mã hoá DES, 3DES, AES, RSA |
| `hashlib` | Tính hash MD5, SHA-256 (có sẵn trong Python) |

---

## 👥 Nhóm 14

| Thành viên | Phụ trách | Trạng thái |
|------------|-----------|-----------|
| Quang | GUI Layout (`gui/`) | ✅ Hoàn thành |
| Hoài Tâm | Symmetric Encryption — DES / 3DES / AES (`functions.py`) | ✅ Hoàn thành |
| Quân | Symmetric Encryption — DES / 3DES / AES (`functions.py`) | ✅ Hoàn thành |
| Minh Tâm | Asymmetric Encryption — RSA (`functions.py`) | ✅ Hoàn thành |
| Quỳnh | Hash Functions — MD5 / SHA-256 (`functions.py`) | ✅ Hoàn thành |

---

## 📝 Ghi chú

> MD5 và DES được đưa vào dự án với **mục đích học thuật** — so sánh độ dài output và cấu trúc với các thuật toán hiện đại hơn như AES và SHA-256. Hai thuật toán này **không được khuyến nghị** dùng trong môi trường thực tế.