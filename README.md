# Iris di Zenfone Max Pro M1

Mengubah ASUS Zenfone Max Pro M1 (X00TD) lama menjadi perangkat khusus **Iris**, teman virtual 2D: begitu HP dinyalakan, langsung muncul avatar dan kotak chat, tanpa aplikasi lain.

> **Status:** Fase 0 dan Fase 1 lulus (20 Nov 2026). Fase 2 (otak LLM dan suara) berikutnya.
> Kode di repo ini belum diuji penuh di HP, jadi anggap sebagai titik awal.

## Cara kerja

```
┌──────────────┐   WiFi rumah   ┌─────────────────────┐        ┌───────────┐
│ Zenfone (UI) │ ─────────────▶ │ Server di PC        │ ─────▶ │ LLM       │
│ avatar+chat  │ ◀───────────── │ FastAPI, port 8000  │ ◀───── │ cloud/lokal│
└──────────────┘                └─────────────────────┘        └───────────┘
```

- **HP hanya layar, suara, dan input.** Snapdragon 636 dengan RAM 3 GB tidak cocok menjalankan model AI lokal.
- **Halaman dimuat dari server.** Mengubah avatar atau persona cukup edit file di PC, tanpa build ulang APK.
- **Jalur cepat:** input teks dulu, suara keluar memakai text-to-speech bawaan Android. Mikrofon dan suara yang lebih bagus menyusul.
- **Avatar 2D** (SVG, animasi CSS): napas, kedip, mata mengikuti sentuhan, mulut bergerak saat Iris bicara.

## Struktur repo

```
.
├── README.md
├── Roadmap_Zenfone_Max_Pro_M1_jadi_Perangkat_Iris.md   # roadmap + tutorial per fase, log progres
└── iris/
    ├── web/
    │   └── index.html      # avatar dan chat (Fase 1)
    └── server/             # backend FastAPI (Fase 2)
```

## Roadmap singkat

| Fase | Isi | Status |
| --- | --- | --- |
| 0 | Persiapan HP: backup, catat versi Chrome/WebView | Selesai |
| 1 | Halaman avatar dan chat palsu, uji kelancaran dan suhu | Lulus |
| 2 | Server, LLM, suara bawaan Android | Berikutnya |
| 3 | Aplikasi kiosk (Capacitor) dan launcher | Belum |
| 4 | LineageOS | Dilewati untuk sekarang |
| 5 | Mode selalu menyala, mode malam, mikrofon | Belum |

Detail langkah, gerbang lolos tiap fase, risiko, dan log progres ada di [roadmap](Roadmap_Zenfone_Max_Pro_M1_jadi_Perangkat_Iris.md).

## Menjalankan Fase 1 (halaman statis)

Butuh Python 3 di PC, dan HP satu WiFi dengan PC.

```powershell
cd iris/web
python -m http.server 8000
```

1. Cari IP PC dengan `ipconfig` (IPv4 Address).
2. Di Chrome HP, buka `http://IP-PC:8000`.
3. Kalau HP timeout, cek profil jaringan WiFi PC. Profil **Public** memblokir koneksi masuk; ubah ke **Private** dan izinkan port 8000 di firewall.

## Menjalankan Fase 2 (server dan LLM)

Butuh Python 3.10 ke atas.

```powershell
pip install fastapi uvicorn httpx

# jalankan dari folder iris/ (bukan dari server/)
$env:LLM_API_KEY="kunci-kamu"
$env:LLM_MODEL="nama-model"
$env:IRIS_TOKEN="kata-sandi-bebas"
# opsional: $env:LLM_BASE_URL="http://localhost:11434/v1"  (Ollama di PC)
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

| Variabel | Fungsi |
| --- | --- |
| `LLM_API_KEY` | Kunci API penyedia LLM (hanya ada di PC) |
| `LLM_MODEL` | Nama model |
| `LLM_BASE_URL` | Endpoint kompatibel OpenAI (default OpenAI, atau Ollama lokal) |
| `IRIS_TOKEN` | Token wajib yang dikirim HP lewat header `X-Token` |

**Jangan commit** kunci API, token, atau `memory.json` (riwayat percakapan). Semuanya sudah dikecualikan lewat `.gitignore`.

## Spesifikasi perangkat

- ASUS Zenfone Max Pro M1 (ASUS_X00TD / ZB601KL), RAM 3 GB, Android 9
- Patch keamanan terakhir 5 September 2020, jadi **pakai hanya di WiFi rumah**, jangan login akun penting
- Chrome / WebView aktif: 138.0.7204.179

## Catatan keamanan

- Server memakai HTTP biasa di jaringan rumah. Jangan diekspos ke internet.
- Token dan riwayat chat hanya untuk penggunaan pribadi; batasi `max_tokens` dan atur batas pengeluaran API di dashboard penyedia.
- Baterai yang selalu tercolok perlu dicek fisik berkala (menggembung = ganti).

## Proyek terkait

- [iris-desktop-companion](https://github.com/JihoStarting/iris-desktop-companion): versi overlay desktop (Electron); logika chat, bubble, dan persona diadaptasi dari sini.

## Penulis

KangJiho
