# Haus Bot Lark

Haus Bot Lark adalah sebuah bot yang menggunakan framework Flask untuk berinteraksi dengan API Lark.

## Daftar Isi

- [Pendahuluan](#pendahuluan)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)
- [Kontributor](#kontributor)

## Pendahuluan

Haus Bot Lark adalah proyek prototype untuk penelitian bot Lark yang dapat berinteraksi dengan API Lark. Proyek ini mungkin akan diupgrade di masa depan.

## Fitur

- Mengirim pesan melalui API Lark
- Mendapatkan data pengguna berdasarkan departemen

## Instalasi

Instruksi untuk menginstal proyek Anda.

1. Clone repository ini
   ```bash
   git clone https://github.com/username/repo-name.git
   cd repo-name
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Library yang diperlukan:

   - Flask
   - Flask-CORS
   - hmac
   - hashlib
   - os
   - threading
   - pyngrok
   - python-dotenv
   - LarkController
   - Middleware
   - json
   - requests

   Tambahkan library di atas ke file `requirements.txt` atau install langsung menggunakan pip:

   ```bash
   pip install Flask Flask-CORS hmac hashlib os threading pyngrok python-dotenv LarkController Middleware json requests
   ```

4. Setting environment variables

   Buat file `.env` di root directory proyek dan tambahkan variabel berikut:

   ```env
   VERIFY_TOKEN=...
   LARK_API_URL=https://open.larksuite.com/open-apis/im/v1/messages/
   AUTH_TOKEN=...
   LARK_API_URL_GET_USER_DEPARTMENT=https://open.larksuite.com/open-apis/contact/v3/users/find_by_department
   AUTH_TOKEN_DEPARTMEN=...
   ```

   - `VERIFY_TOKEN`: Dapatkan dari aplikasi bot yang dapat diambil di credential dan info di `haus_test_apps`.
   - `AUTH_TOKEN`: Dapat diambil pada API generator di Lark. Contoh link: [API Generator](https://open.larksuite.com/document/server-docs/im-v1/message/create?appId=cli_a55d512fc1b89009)
   - `AUTH_TOKEN_DEPARTMEN`: Dapat diambil pada API generator di Lark. Contoh link: [API Generator](https://open.larksuite.com/document/server-docs/contact-v3/user/find_by_department?appId=cli_a55d512fc1b89009)

5. Jika ingin menggunakan GitHub bot watcher, maka set up di webhooks repo GitHub yang ingin di monitoring dengan menggunakan API `/webhook`.

## Penggunaan

Cara menjalankan aplikasi:

```bash
python app.py
```
