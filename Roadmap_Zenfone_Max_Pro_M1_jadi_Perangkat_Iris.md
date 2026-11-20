# Roadmap + Tutorial: Zenfone Max Pro M1 jadi Perangkat Iris

Nov 20, 2026 · @Jiho · versi jalur cepat dengan tutorial langkah demi langkah

by: KangJiho · terakhir diupdate: 20 Nov 2026 (Fase 0 dan Fase 1 lulus, siap Fase 2)

> Kode di dokumen ini belum diuji di HP-mu. Anggap sebagai titik awal, dan sesuaikan kalau ada yang error.

## Tujuan dan prinsip

Zenfone Max Pro M1 jadi perangkat khusus Iris: begitu dinyalakan langsung menampilkan avatar dan kotak chat, tanpa aplikasi lain.

- **HP hanya layar, suara, dan input.** Otak (LLM) berjalan di luar HP, lewat WiFi. Snapdragon 636 dengan RAM 3 GB tidak cocok menjalankan model AI lokal.
- **Mulai dari yang paling murah dicoba.** Halaman web dulu, aplikasi kiosk sesudahnya, custom ROM hanya bila perlu.
- **Halaman dimuat dari server.** Mengubah avatar atau persona cukup edit file di PC, tanpa build ulang APK.
- **Jalur cepat:** input awal cukup teks, suara keluar pakai suara bawaan Android. Mikrofon dan suara bagus menyusul.
- Repo iris-desktop-companion milikmu sendiri, jadi logika chat, bubble, dan persona boleh diadaptasi. Bagian Electron dan WSL2 tidak ikut.

## Status saat ini

- [x] Spesifikasi tercatat: ASUS\_X00TD (ZB601KL), RAM 3 GB, Android 9, patch keamanan 5 September 2020 (sudah versi terakhir dari Asus)
- [x] Penyimpanan dikosongkan: 7,96 GB terpakai dari 22,07 GB
- [x] Backup selesai
- [x] Reset pabrik **dilewati** (penyimpanan sudah dikosongkan, aplikasi tak perlu dinonaktifkan manual)
- [x] Aplikasi tak perlu dinonaktifkan (WebView, Chrome, Speech Services, Play Store, keyboard, launcher tidak disentuh)
- [x] Versi tercatat: Chrome 138.0.7204.179 (Android 9, 32 bit). WebView aktif = Chrome 138.0.7204.179; Android System WebView 79.0.3945.116 bawaan pabrik dinonaktifkan dan dibiarkan
- [x] Baterai fisik dicek: layar tidak terangkat, bodi tidak menggembung
- [x] Dudukan dan charger tercolok terus siap
- [x] Fase 1 langkah 1-5: `index.html` di `iris\web`, server `python -m http.server 8000`, halaman terbuka di Chrome HP (`http://192.168.15.18:8000`), avatar dan chat palsu tampil dan membalas
- [x] Fase 1 uji suhu (CPU-Z, tab Thermal, 20 Nov 2026 21.27, baterai 95% saat tercolok charger): battery 33,0 °C, sensor SoC tertinggi 39,5 °C (tsens_tz_sensor7), lainnya 36,9-38,8 °C. Lolos batas sekitar 40 °C, tapi sensor tertinggi sudah dekat batas
- [x] Fase 1 kelancaran: tampilan avatar dinilai jelek (placeholder), tapi gerak mulus tanpa patah-patah
- [x] **Fase 1 LULUS** (20 Nov 2026)
- [ ] Keputusan: otak di cloud atau di PC rumah (default tutorial ini: cloud lewat server di PC)

## Jalur cepat (target 9-10 hari, santai 1-2 jam per hari)

| Hari | Kerjaan | Gerbang |
| --- | --- | --- |
| 1 | Fase 0: backup, reset, update, catat versi | HP bersih, versi tercatat |
| 2-3 | Fase 1: halaman avatar dan chat palsu | Lancar 10 menit di HP |
| 4-6 | Fase 2: server, LLM, suara bawaan | Ketik di HP, Iris balas dengan suara |
| 7-9 | Fase 3: aplikasi kiosk dan launcher | Restart, Iris langsung terbuka |
| Nanti | Fase 5: mode selalu menyala, mikrofon | Dipakai seharian |

Ini target ambisius. Kalau meleset, tidak apa-apa; urutan dan gerbangnya yang penting.

## Fase 0: Persiapan HP (hari 1)

**Tutorial**

1. **Backup.** Colok HP ke PC lewat USB, pilih mode "Transfer file", lalu salin folder `backups` dan `cc` (dan foto, kontak, chat bila perlu) ke PC. Pastikan akun Google tersinkron di Pengaturan > Akun, dan kamu ingat kata sandinya (HP akan meminta login yang sama setelah reset).
2. **Cek baterai fisik.** Lihat apakah layar terangkat atau bodi menggembung. Cas dari rendah dan lihat apakah persentase turun tidak wajar.
3. **Reset pabrik.** Pengaturan > Sistem > Reset > Hapus semua data. Ini sekaligus menghapus sisa folder aplikasi lama.
4. **Setelah menyala:** login Google, lewati semua aplikasi yang tidak perlu, nonaktifkan aplikasi bawaan lewat Pengaturan > Aplikasi > Nonaktifkan.
5. **Update lewat Play Store:** Chrome dan Android System WebView. Buka Play Store, cari masing-masing, tekan Update kalau ada.
6. **Catat versi:** Pengaturan > Aplikasi > Android System WebView > gulir ke bawah > Versi. Untuk Chrome, buka `chrome://version`. Tulis kedua nomor di bawah:
   - Chrome: 138.0.7204.179
   - WebView: memakai Chrome 138.0.7204.179 (Pengaturan > Opsi pengembang > Penerapan WebView); Android System WebView 79 dinonaktifkan, jangan dipilih
7. **Siapkan fisik:** dudukan HP dan charger yang bisa tercolok terus.

**Gerbang:** HP bersih, baterai tidak menggembung, nomor versi Chrome dan WebView tercatat.

**Status: SELESAI (20 Nov 2026).** Catatan: reset pabrik dilewati; WebView ternyata memakai Chrome 138, jadi rencana mundur WebView lama di Fase 3 kemungkinan tidak diperlukan.

**Catatan keamanan:** patch keamanan sudah sekitar 6 tahun. Pakai hanya di WiFi rumah, jangan login akun penting, dan jangan buka situs sembarangan.

## Fase 1: Halaman avatar dan chat (hari 2-3)

**Tutorial**

1. Di PC, buat struktur folder:

   ```
   iris/
     web/
       index.html
     server/        (dipakai di Fase 2)
   ```

2. Isi `iris/web/index.html` dengan kode ini (avatar SVG sederhana; nanti ganti dengan gambar berlapis milikmu):

   ```html
   <!DOCTYPE html>
   <html lang="id">
   <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
   <title>Iris</title>
   <style>
     html, body { margin:0; height:100%; background:#14141c; color:#eee;
       font-family:system-ui, sans-serif; overflow:hidden; }
     #app { display:flex; flex-direction:column; height:100%; }
     #stage { flex:0 0 42%; display:flex; align-items:center; justify-content:center; }
     #avatar { height:100%; max-height:300px; animation:breathe 4s ease-in-out infinite;
       transform-origin:50% 100%; }
     @keyframes breathe { 0%,100%{transform:scaleY(1)} 50%{transform:scaleY(1.015)} }
     .eye { transform-box:fill-box; transform-origin:center; animation:blink 5s infinite; }
     @keyframes blink { 0%,94%,100%{transform:scaleY(1)} 97%{transform:scaleY(0.1)} }
     #mouth { transform-box:fill-box; transform-origin:center; }
     .talking #mouth { animation:talk .25s infinite alternate; }
     @keyframes talk { from{transform:scaleY(.4)} to{transform:scaleY(2.2)} }
     #chat { flex:1; overflow-y:auto; padding:8px 12px; }
     .msg { max-width:80%; margin:6px 0; padding:8px 12px; border-radius:14px; line-height:1.35; }
     .iris { background:#2b2b44; }
     .me { background:#3d5afe; margin-left:auto; }
     #bar { display:flex; gap:8px; padding:8px 12px calc(8px + env(safe-area-inset-bottom,0px)); }
     #text { flex:1; padding:10px; border-radius:10px; border:0; font-size:16px; }
     button { padding:10px 16px; border:0; border-radius:10px; font-size:16px;
       background:#3d5afe; color:#fff; }
     #status { font-size:12px; text-align:center; color:#8a8aa5; height:16px; }
   </style>
   </head>
   <body>
   <div id="app">
     <div id="stage">
       <svg id="avatar" viewBox="0 0 200 260" xmlns="http://www.w3.org/2000/svg">
         <rect x="55" y="150" width="90" height="110" rx="32" fill="#6c7bd9"/>
         <circle cx="100" cy="100" r="62" fill="#ffe0cc"/>
         <path d="M38 95 Q100 10 162 95 Q150 55 100 48 Q50 55 38 95Z" fill="#3a2a5c"/>
         <g id="eyes">
           <ellipse class="eye" cx="78" cy="102" rx="9" ry="12" fill="#222"/>
           <ellipse class="eye" cx="122" cy="102" rx="9" ry="12" fill="#222"/>
         </g>
         <ellipse id="mouth" cx="100" cy="135" rx="12" ry="4" fill="#a33"/>
       </svg>
     </div>
     <div id="status"></div>
     <div id="chat"></div>
     <div id="bar">
       <input id="text" placeholder="Ketik pesan..." autocomplete="off">
       <button id="send">Kirim</button>
     </div>
   </div>
   <script>
   const chat = document.getElementById('chat');
   const input = document.getElementById('text');
   const avatar = document.getElementById('avatar');
   const eyes = document.getElementById('eyes');
   const statusEl = document.getElementById('status');

   function add(role, text) {
     const d = document.createElement('div');
     d.className = 'msg ' + role;
     d.textContent = text;
     chat.appendChild(d);
     chat.scrollTop = chat.scrollHeight;
   }

   // Mata mengikuti titik sentuhan
   function look(e) {
     const p = e.touches ? e.touches[0] : e;
     const r = avatar.getBoundingClientRect();
     const dx = Math.max(-1, Math.min(1, (p.clientX - (r.left + r.width/2)) / r.width));
     const dy = Math.max(-1, Math.min(1, (p.clientY - (r.top + r.height/3)) / r.height));
     eyes.style.transform = `translate(${dx*5}px, ${dy*4}px)`;
   }
   window.addEventListener('touchstart', look, {passive:true});
   window.addEventListener('mousemove', look);

   // FASE 1: balasan palsu. Di Fase 2 fungsi ini diganti.
   async function getReply(text) {
     return 'Halo, aku Iris. Kamu bilang: ' + text;
   }

   async function send() {
     const t = input.value.trim();
     if (!t) return;
     input.value = '';
     add('me', t);
     try {
       const reply = await getReply(t);
       add('iris', reply);
     } catch (e) {
       statusEl.textContent = 'Gagal terhubung';
     }
   }
   document.getElementById('send').onclick = send;
   input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
   add('iris', 'Halo! Aku Iris.');
   </script>
   </body>
   </html>
   ```

3. Jalankan server statis dari folder `iris/web`:

   ```
   cd iris/web
   python -m http.server 8000
   ```

4. Cari IP PC: di Windows jalankan `ipconfig` dan cari "IPv4 Address" (contoh `192.168.1.10`). Izinkan Python lewat firewall kalau diminta.
5. Di Chrome HP (satu WiFi dengan PC), buka `http://192.168.1.10:8000`. Chat dan avatar harus tampil.
6. **Uji 10 menit:** biarkan halaman terbuka dan perhatikan patah-patah dan suhu (CPU-Z). Kalau berat: perkecil gambar, kurangi animasi, atau matikan animasi bernapas.
7. Ganti SVG dengan gambar berlapis milikmu (PNG kecil, lebar maksimal sekitar 800 px) kalau sudah puas dengan dasarnya.

**Gerbang:** avatar bergerak lancar 10 menit, suhu di bawah sekitar 40 °C, tidak ada patah-patah.

## Fase 2: Otak dan suara (hari 4-6)

**Tutorial**

1. **Keputusan otak.** Default: API LLM cloud lewat server di PC (paling cepat). Alternatif: model lokal di PC dengan Ollama (`LLM_BASE_URL=http://localhost:11434/v1`), tapi PC harus menyala terus.
2. Di PC, pasang dependensi (butuh Python 3.10 ke atas):

   ```
   pip install fastapi uvicorn httpx
   ```

3. Buat `iris/server/main.py`:

   ```python
   import os, json
   import httpx
   from fastapi import FastAPI, Header, HTTPException
   from fastapi.staticfiles import StaticFiles
   from pydantic import BaseModel

   BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
   API_KEY = os.getenv("LLM_API_KEY", "")
   MODEL = os.getenv("LLM_MODEL", "")          # isi nama model dari penyedia kamu
   TOKEN = os.getenv("IRIS_TOKEN", "")         # kata sandi bebas, wajib diisi
   HIST_FILE = "memory.json"
   PERSONA = (
       "Kamu Iris, teman virtual yang hangat dan singkat. "
       "Balas dalam bahasa Indonesia, maksimal 3 kalimat."
   )

   app = FastAPI()

   class Msg(BaseModel):
       text: str

   def load():
       try:
           with open(HIST_FILE, encoding="utf-8") as f:
               return json.load(f)
       except Exception:
           return []

   def save(h):
       with open(HIST_FILE, "w", encoding="utf-8") as f:
           json.dump(h[-200:], f, ensure_ascii=False)

   @app.get("/ping")
   def ping():
       return {"ok": True}

   @app.post("/chat")
   async def chat(m: Msg, x_token: str = Header(default="")):
       if not TOKEN or x_token != TOKEN:
           raise HTTPException(status_code=401)
       hist = load()
       hist.append({"role": "user", "content": m.text[:1000]})
       async with httpx.AsyncClient(timeout=60) as c:
           r = await c.post(
               f"{BASE_URL}/chat/completions",
               headers={"Authorization": f"Bearer {API_KEY}"},
               json={
                   "model": MODEL,
                   "max_tokens": 300,
                   "messages": [{"role": "system", "content": PERSONA}] + hist[-20:],
               },
           )
       r.raise_for_status()
       reply = r.json()["choices"][0]["message"]["content"]
       hist.append({"role": "assistant", "content": reply})
       save(hist)
       return {"reply": reply}

   # Harus paling bawah, setelah semua route
   app.mount("/", StaticFiles(directory="web", html=True), name="web")
   ```

4. Jalankan dari folder `iris/` (bukan dari `server/`), dengan variabel lingkungan. Windows PowerShell:

   ```
   $env:LLM_API_KEY="kunci-kamu"
   $env:LLM_MODEL="nama-model"
   $env:IRIS_TOKEN="kata-sandi-bebas"
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   ```

   Hentikan `python -m http.server` dari Fase 1 dulu supaya port 8000 kosong. Kalau Python tidak menemukan paket `server`, tambahkan file kosong `server/__init__.py`.
5. Di `index.html`, ganti fungsi `getReply` dan tambah `speak`:

   ```js
   function speak(t) {
     try {
       speechSynthesis.cancel();
       const u = new SpeechSynthesisUtterance(t);
       u.lang = 'id-ID';
       u.onstart = () => avatar.classList.add('talking');
       u.onend = () => avatar.classList.remove('talking');
       speechSynthesis.speak(u);
     } catch (e) {}
   }

   function token() {
     try {
       let t = localStorage.getItem('iris_token');
       if (!t) { t = prompt('Token Iris:') || ''; localStorage.setItem('iris_token', t); }
       return t;
     } catch (e) { return prompt('Token Iris:') || ''; }
   }

   async function getReply(text) {
     const r = await fetch('/chat', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json', 'X-Token': token() },
       body: JSON.stringify({ text })
     });
     if (r.status === 401) { try { localStorage.removeItem('iris_token'); } catch (e) {} throw new Error('token'); }
     if (!r.ok) throw new Error('server');
     const j = await r.json();
     speak(j.reply);
     return j.reply;
   }
   ```

6. Buka `http://IP-PC:8000` di HP, ketik pesan, masukkan token saat diminta. Iris harus membalas dengan teks dan suara.
7. **Suara Indonesia:** kalau suara tidak keluar atau bahasanya salah, buka Pengaturan > Sistem > Bahasa & input > Output text-to-speech, lalu unduh data suara Bahasa Indonesia untuk mesin Google.
8. **Batas biaya:** `max_tokens` sudah 300 dan riwayat dibatasi 20 pesan terakhir. Atur juga batas pengeluaran di dashboard penyedia API.
9. **Keamanan:** kunci API hanya ada di PC. Token dikirim lewat WiFi rumah tanpa enkripsi (HTTP), jadi cukup untuk jaringan rumah, jangan diekspos ke internet.
10. **Backup:** salin `memory.json` dan `main.py` (persona) secara berkala ke tempat lain.

**Gerbang:** kamu mengetik di HP, dan Iris membalas dengan teks dan suara dalam sekitar 5 detik.

**Menyusul (tidak di jalur cepat):**
- **Input suara.** `SpeechRecognition` umumnya tidak jalan di WebView, dan mikrofon butuh HTTPS. Opsi: rekam audio lalu kirim ke server untuk Whisper (butuh sertifikat lokal atau origin `localhost`), atau jembatan native ke `SpeechRecognizer` Android.
- **Suara lebih bagus.** Server menghasilkan audio (misalnya VOICEVOX atau TTS cloud), HP memutarnya.

## Fase 3: Aplikasi kiosk dan launcher (hari 7-9)

Pendekatan: aplikasi Capacitor yang memuat halaman langsung dari server di PC (`server.url`). Keuntungannya, halaman bisa diubah tanpa build ulang. Kekurangannya, PC harus menyala dan satu WiFi.

**Tutorial**

1. **Pasang di PC:** Node.js (versi yang diminta dokumentasi Capacitor terbaru) dan Android Studio (termasuk Android SDK).
2. **Buat proyek:**

   ```
   mkdir iris-app && cd iris-app
   npm init -y
   npm i @capacitor/core @capacitor/cli @capacitor/android
   npx cap init Iris com.jiho.iris --web-dir=www
   mkdir www
   echo "<html></html>" > www/index.html
   npx cap add android
   ```

3. **Arahkan ke server.** Buka `capacitor.config.json` (atau `.ts`) dan tambahkan:

   ```json
   {
     "appId": "com.jiho.iris",
     "appName": "Iris",
     "webDir": "www",
     "server": {
       "url": "http://192.168.1.10:8000",
       "cleartext": true
     }
   }
   ```

   Ganti IP dengan IP PC-mu, lalu jalankan `npx cap sync android`. Supaya IP tidak berubah-ubah, set IP tetap (DHCP reservation) di router untuk PC.
4. **Jadikan launcher.** Buka `android/app/src/main/AndroidManifest.xml`, di dalam `<activity ... MainActivity>` tambahkan filter kedua (biarkan filter LAUNCHER yang sudah ada):

   ```xml
   <intent-filter>
       <action android:name="android.intent.action.MAIN" />
       <category android:name="android.intent.category.HOME" />
       <category android:name="android.intent.category.DEFAULT" />
   </intent-filter>
   ```

   Tambahkan juga atribut `android:launchMode="singleTask"` pada `<activity>` tersebut.
5. **Layar penuh dan layar menyala.** Di `android/app/src/main/java/com/jiho/iris/MainActivity.java`:

   ```java
   package com.jiho.iris;

   import android.os.Bundle;
   import android.view.View;
   import android.view.WindowManager;
   import com.getcapacitor.BridgeActivity;

   public class MainActivity extends BridgeActivity {
     @Override
     public void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
     }

     @Override
     public void onWindowFocusChanged(boolean hasFocus) {
       super.onWindowFocusChanged(hasFocus);
       if (hasFocus) {
         getWindow().getDecorView().setSystemUiVisibility(
           View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
           | View.SYSTEM_UI_FLAG_FULLSCREEN
           | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
           | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
           | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
           | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
       }
     }
   }
   ```

   Kalau file Java sudah ada isinya, pertahankan `package` dan tambahkan metode di atas.
6. **Siapkan HP untuk instalasi:** Pengaturan > Tentang ponsel > ketuk Nomor build 7 kali > kembali ke Sistem > Opsi pengembang > aktifkan Debugging USB. Colok ke PC dan setujui prompt di HP.
7. **Pasang aplikasi:**

   ```
   npx cap run android
   ```

   Atau buka `npx cap open android` dan tekan tombol Run di Android Studio.
8. **Jadikan layar utama:** tekan tombol Home di HP, pilih "Iris" dan "Selalu".
9. **Atur HP agar tidak mengganggu:**
   - Pengaturan > Keamanan > Kunci layar > **Tidak ada**.
   - Pengaturan > Aplikasi > Iris > Baterai > Optimasi baterai > Jangan optimalkan.
   - Play Store > Pengaturan > Update otomatis aplikasi > **Jangan** update otomatis.
   - Pengaturan > Tampilan > Tidur > nilai terpanjang (atau andalkan flag layar menyala).
10. **Suara tanpa sentuhan.** Uji dulu: restart, biarkan, lalu kirim pesan dari PC atau tunggu respons. Kalau suara bisa diblokir sampai ada sentuhan, tambahkan tombol atau layar "Ketuk untuk mulai" sekali setelah boot, atau pindahkan TTS ke audio dari server. Di aplikasi sendiri, pengaturan `setMediaPlaybackRequiresUserGesture(false)` pada WebView juga bisa dipakai.
11. **Pulih otomatis saat server putus.** Tambahkan di `index.html`:

    ```js
    let down = false;
    setInterval(async () => {
      try {
        const r = await fetch('/ping', { cache: 'no-store' });
        if (r.ok && down) location.reload();
        down = !r.ok;
      } catch (e) { down = true; }
      statusEl.textContent = down ? 'Server tidak terjangkau, mencoba lagi...' : '';
    }, 5000);
    ```

    Catatan: kalau server mati saat aplikasi pertama dibuka, WebView menampilkan halaman error bawaan. Solusi sederhana: jalankan server PC otomatis saat PC menyala (Task Scheduler di Windows).
12. **Uji restart:** matikan HP, nyalakan, jangan sentuh. Iris harus muncul sendiri.

**Gerbang:** setelah HP direstart, Iris langsung terbuka tanpa disentuh, tidak ada kunci layar, layar tetap menyala, dan suara keluar sesuai kemampuan hasil uji langkah 10.

**Rencana mundur kalau WebView Android 9 terlalu tua** (animasi error, fitur JS tidak jalan): turunkan fitur web yang dipakai (hindari sintaks JS terbaru, uji dengan Chrome remote debugging), atau pertimbangkan Fase 4 untuk mendapat WebView lebih baru.

## Fase 4 (dilewati untuk sekarang): LineageOS

Dikerjakan hanya kalau ROM stok mengganggu (bloatware, lambat), WebView Android 9 terlalu tua, atau kamu ingin Android lebih baru. Putuskan setelah Fase 1 diuji di HP.

- **Kandidat:** LineageOS 21 (Android 14) unofficial dari rajesh@xda untuk X00TD. Ada laporan nyangkut di boot animation setelah update tertentu (Mei 2024), jadi baca halaman terakhir thread-nya. Evolution-X berbasis Android 16 (unofficial, posting terakhir 17 Oktober 2026) terlalu baru untuk langsung dipercaya.
- **Belum diverifikasi:** detail build dan syarat unlock bootloader lewat aplikasi resmi Asus pada firmware Android 9. Cek ulang sebelum mencoba.
- **Urutan umum:** backup, unlock bootloader, pasang recovery, flash ROM sesuai syarat firmware di thread, lalu pasang aplikasi Iris sebagai launcher. Tutorial rincinya mengikuti thread XDA, bukan dokumen ini, karena langkah tiap build berbeda.
- **Tidak termasuk:** membangun OS dari nol.

**Gerbang:** HP boot stabil, dan WiFi, layar, mikrofon, serta speaker berfungsi normal.

## Fase 5: Mode selalu menyala dan polesan (setelah jalur cepat)

**Tutorial**

1. **Mode malam otomatis.** Tambahkan di `index.html`:

   ```js
   function applyNight() {
     const h = new Date().getHours();
     document.body.style.filter = (h >= 22 || h < 6) ? 'brightness(0.35)' : 'none';
   }
   applyNight();
   setInterval(applyNight, 60000);
   ```

   Ini meredupkan tampilan, bukan kecerahan panel. Untuk kecerahan panel, atur kecerahan HP secara manual atau lewat jadwal.
2. **Baterai.** Pasang smart plug berjadwal (misalnya cas hanya beberapa jam per hari) atau charger yang membatasi sekitar 80%. ROM stok tidak punya batas pengisian bawaan. Cek fisik tiap beberapa bulan; baterai yang menggembung harus diganti, jangan terus dicas.
3. **Jam dan avatar tidur.** Setelah 2 menit tanpa aktivitas, tampilkan jam dan ganti avatar ke mode tidur (mata tertutup), bangunkan saat disentuh.
4. **Debug jarak jauh.** Colok USB, buka `chrome://inspect` di Chrome PC untuk melihat konsol halaman di HP. Untuk tanpa kabel, gunakan `adb` over WiFi (`adb tcpip 5555` lalu `adb connect IP-HP:5555`).
5. **Pemantauan sederhana.** Tambahkan endpoint `/heartbeat` di server yang dicatat tiap menit dari HP, supaya tahu kapan HP terakhir terhubung.
6. **Fitur lain:** jam dan alarm, timer, pengingat istirahat, ekspresi yang mengikuti suasana percakapan.

**Gerbang:** HP dipakai seharian penuh tanpa perlu disentuh atau direstart.

## Kriteria ukur per fase

| Fase | Ukuran lolos |
| --- | --- |
| 1 | 10 menit tanpa patah-patah, suhu di bawah sekitar 40 °C |
| 2 | Balasan di bawah sekitar 5 detik, suara Indonesia keluar |
| 3 | Restart tanpa sentuhan: Iris terbuka dalam sekitar 1 menit |
| 5 | 24 jam tanpa restart, baterai tidak menggembung |

## Risiko dan keputusan terbuka

| Risiko | Dampak | Antisipasi |
| --- | --- | --- |
| Animasi terlalu berat | Patah-patah dan HP panas | Perkecil gambar, kurangi animasi |
| WebView Android 9 terlalu tua | Fitur web tidak jalan | Catat versi di Fase 0, uji lebih awal, rencana mundur di Fase 3 |
| Mikrofon tidak jalan di WebView atau butuh HTTPS | Input suara gagal | Mulai dengan teks; Whisper di server atau jembatan native nanti |
| Suara diblokir tanpa sentuhan | Iris diam setelah boot | Ketuk sekali untuk mulai, atau audio dari server |
| IP PC berubah | HP tidak menemukan server | DHCP reservation di router |
| PC mati | Iris tidak berfungsi | Server auto-start, atau pindah ke server murah |
| Baterai menggembung | Bahaya keselamatan | Smart plug, batas 80%, cek berkala |
| Patch keamanan usang | Celah keamanan | Hanya WiFi rumah, tanpa akun penting, token wajib |
| Biaya API membengkak | Tagihan besar | `max_tokens` 300, batas bulanan di dashboard |
| Privasi (mikrofon, percakapan tersimpan) | Data sensitif | Tentukan apa yang disimpan, indikator jelas saat mikrofon aktif |
| Motivasi hilang | Proyek berhenti | Kerjakan per fase kecil dengan gerbang jelas |

Keputusan yang sudah diambil:

- [x] Repo iris-desktop-companion milik sendiri, kodenya boleh diadaptasi
- [x] Avatar 2D
- [x] ROM stok, Fase 4 dilewati
- [x] Jalur cepat: input teks dulu, suara keluar bawaan Android

Keputusan yang masih terbuka:

- [ ] Otak: cloud (default) atau Ollama di PC rumah
- [ ] Cara memanggil Iris tanpa sentuhan nanti: tombol besar di layar (disarankan), atau wake word di server
- [ ] Anggaran bulanan API: ______

Keputusan tambahan (20 Nov 2026):

- [x] Reset pabrik dilewati
- [x] Roadmap ini diupdate tiap ada progress

## Langkah berikutnya

1. ~~Fase 0: backup, update, catat versi Chrome dan WebView.~~ Selesai 20 Nov 2026.
2. **Sekarang:** Fase 1. Buat `index.html`, jalankan `python -m http.server 8000`, buka `http://IP-PC:8000` di Chrome HP, uji 10 menit sambil pantau suhu di CPU-Z.
3. Kabari hasil gerbang tiap fase, nanti kita lanjut atau perbaiki.

## Log progres

- 20 Nov 2026: Fase 0 selesai (backup, tanpa reset pabrik, Chrome dan WebView 138.0.7204.179, baterai aman, dudukan siap). Fase 1 dimulai.
- 20 Nov 2026: file `index.html` Fase 1 disiapkan (avatar SVG + chat palsu), menunggu disimpan di `iris\web` dan diuji dari Chrome HP. Catatan: `index.html` overlay desktop AI Companion (5.656 baris, WebSocket ke localhost:8765) tidak dipakai di Fase 1.
- 20 Nov 2026: awalnya HP timeout (`ERR_CONNECTION_TIMED_OUT`) karena WiFi di PC berstatus Public. Perbaikan: aturan firewall port 8000 untuk profil Private (`New-NetFirewallRule`), lalu `Set-NetConnectionProfile -InterfaceAlias "Wi-Fi 2" -NetworkCategory Private`. Setelah itu halaman terbuka di Chrome HP: avatar tampil, chat palsu membalas "Halo, aku Iris. Kamu bilang: ...". Sisa Fase 1: uji 10 menit dan pantau suhu.
- 20 Nov 2026 (21.27): hasil CPU-Z Thermal: battery 33,0 °C, sensor SoC tertinggi 39,5 °C, rata-rata sensor sekitar 38 °C. Lolos batas suhu Fase 1 (di bawah sekitar 40 °C), dengan catatan sensor tertinggi sudah mendekati batas.
- 20 Nov 2026: Fase 1 LULUS. Animasi mulus tanpa patah-patah; tampilan avatar placeholder dinilai jelek, jadi avatar yang lebih bagus (gaya anime, mulut bergerak saat bicara) masuk daftar perbaikan. Berikutnya: Fase 2.
- 20 Nov 2026: `index.html` avatar v2 dibuat (rambut, mata besar mengikuti sentuhan dan melirik sendiri, kedip, kepala bergoyang pelan, mulut bergerak saat Iris membalas). Menimpa file lama di `iris\web`; menunggu dicoba di HP.

**Sumber** (dibuka November 2026):

- [Forum XDA Asus ZenFone Max Pro M1](https://xdaforums.com/c/asus-zenfone-max-pro-m1.7656/)
- [Thread Lineage-21.0 X00TD di XDA](https://xdaforums.com/t/rom-14-signed-lineage-21-0-x00td-asus-zenfone-max-pro-m1.4669119/)
- [Repo iris-desktop-companion](https://github.com/JihoStarting/iris-desktop-companion)
