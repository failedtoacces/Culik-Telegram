# Telegram Group Member Management Bot

## Deskripsi

Bot ini dirancang untuk membantu dalam mengelola anggota grup Telegram. Dengan bot ini, Anda dapat melakukan beberapa fungsi seperti mengumpulkan anggota dari grup tertentu dan menambahkannya ke grup lain secara otomatis.

## Fitur

- **Setup Konfigurasi:** Mengatur API ID, API Hash, dan nomor telepon untuk menghubungkan bot dengan Telegram.
- **Scrape Anggota Grup:** Mengambil anggota dari grup Telegram yang dipilih dan menyimpannya ke dalam file CSV.
- **Tambah Anggota ke Grup:** Menambahkan anggota dari file CSV ke grup Telegram yang ditentukan.
- **Pengecualian Flood:** Menangani pengecualian yang terkait dengan batasan Telegram dan menjaga agar bot tetap berfungsi.

## Prasyarat

1. Python 3.6 atau lebih baru
2. Pustaka `telethon` untuk interaksi dengan API Telegram

## Instalasi

1. Clone repositori ini:
    ```sh
    [git clone https://github.com/username/repository.git](https://github.com/failedtoacces/culiktele.git)
    cd culiktele
    ```
2. Jalankan setup:
    ```sh
    python3 main.py
    ```

4. Tinggal ikuti langkah satu sampai 4

## Penggunaan

1. **Setup Konfigurasi:** Jalankan bot dan pilih opsi `1` untuk mengatur konfigurasi API.
2. **Setup API:** Pilih opsi `2` untuk menghubungkan bot dengan Telegram menggunakan konfigurasi yang telah disiapkan.
3. **Scrape Anggota Grup:** Pilih opsi `3` untuk mengumpulkan anggota dari grup dan menyimpannya dalam file CSV.
4. **Tambah Anggota ke Grup:** Pilih opsi `4` untuk menambahkan anggota dari file CSV ke grup yang dipilih.

## Struktur Kode

- `bot.py`: Script utama untuk menjalankan bot.
- `config.data`: File konfigurasi yang berisi API ID, API Hash, dan nomor telepon.
- `members.csv`: File output yang berisi data anggota grup.

## Penanganan Pengecualian

Bot ini menangani beberapa pengecualian termasuk:
- `FloodWaitError`: Penanganan batasan waktu dari Telegram.
- `PeerFloodError`: Menghentikan bot jika terkena pembatasan dari Telegram.
- `UserPrivacyRestrictedError`: Menangani pengaturan privasi pengguna.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan buat pull request dengan perubahan Anda. Pastikan untuk memeriksa masalah yang ada atau membuka issue baru untuk diskusi sebelum membuat perubahan besar.

## Lisensi

Distribusi proyek ini diatur di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

