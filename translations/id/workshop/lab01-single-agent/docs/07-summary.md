# Modul 7 - Ringkasan & Langkah Selanjutnya

⏱️ ~5 menit

**Selamat!** Anda telah membangun, menguji, dan (jika di Jalur A) menerapkan agen AI yang dihosting menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang Anda bangun

Agen **"Jelaskan Seperti Saya Eksekutif"** yang:
- Menerima laporan insiden teknis atau pembaruan operasional melalui HTTP (`POST /responses`)
- Menerjemahkannya menjadi ringkasan eksekutif dengan bahasa sederhana
- Mengikuti format keluaran yang terstruktur (Apa yang terjadi / Dampak bisnis / Langkah selanjutnya)
- Menolak permintaan di luar topik dan upaya penyuntikan prompt
- Berjalan sebagai agen yang dihosting dalam container di Microsoft Foundry Agent Service

---

## Konsep kunci yang dipelajari

| Konsep | Apa yang Anda latih |
|---------|-------------------|
| **Arsitektur Agent Framework** | Alur `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Siklus hidup Hosted Agent** | Scaffold → Konfigurasi → Uji lokal → Deploy → Verifikasi di cloud |
| **Rekayasa prompt sistem** | Peran, audiens, format keluaran, aturan, batasan keamanan, dan contoh |
| **Perbedaan lokal vs. hosted** | Identitas (kredensial pribadi vs. identitas terkelola), endpoint, jalur jaringan |
| **Batasan keamanan** | Pertahanan penyuntikan prompt, kepatuhan peran, penanganan kasus tepi dengan baik |
| **Alur kerja Foundry Toolkit** | Pembuatan proyek, deployment model, scaffolding agen, Agent Inspector, deploy sekali klik |

---

## Apa yang telah Anda selesaikan

### Jalur A (Langganan Foundry)

- [x] Mengatur Foundry Toolkit dan membuat proyek Foundry dengan model yang di-deploy
- [x] Membuat scaffold agen yang dihosting dengan struktur proyek yang dihasilkan otomatis
- [x] Menulis instruksi agen terstruktur dengan aturan keamanan
- [x] Menguji secara lokal dengan 3 skenario fungsional (Agent Inspector)
- [x] Mendeploy ke Foundry Agent Service (containerized)
- [x] Memverifikasi di playground cloud dengan 4 pengujian edge-case/keamanan

### Jalur B (Foundry Lokal)

- [x] Mengatur Foundry Toolkit dengan endpoint model lokal
- [x] Membuat scaffold proyek agen yang dihosting
- [x] Menulis instruksi agen terstruktur dengan aturan keamanan
- [x] Menguji secara lokal dengan 3 skenario fungsional
- [x] Memvalidasi perilaku agen tanpa memerlukan sumber daya cloud

---

## Langkah selanjutnya

### Lanjutkan belajar

| Sumber daya | Deskripsi |
|----------|-------------|
| **[Lab 02 - Orkestrasi Multi-Agen](../../lab02-multi-agent/docs/README.md)** | Bangun alur kerja 4 agen (Resume → Job Fit Evaluator) dengan pola orkestrasi |
| **[Tambahkan alat ke agen Anda](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Hubungkan API, basis data, atau fungsi kustom melalui Tool Catalog |
| **[Tambahkan pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Dasarkan agen Anda dengan dokumen, penyimpanan vektor, atau pencarian Bing |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referensi lengkap platform |
| **[Referensi SDK Agent Framework](https://learn.microsoft.com/agent-framework/)** | Dokumentasi API untuk paket `agent-framework` |
| **[Foundry Toolkit - Apa yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Catatan rilis ekstensi dan changelog |

### Ide untuk mengembangkan agen Anda

- **Tambahkan alat tanggal** - Biarkan agen menyertakan konteks "per hari ini" dalam ringkasan
- **Hubungkan ke basis data insiden** - Tarik detail insiden nyata melalui fungsi alat
- **Tambahkan alat grounding Bing** - Biarkan agen mencari berita terkini untuk konteks tambahan
- **Coba model berbeda** - Bandingkan kualitas keluaran `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluasi dengan Foundry** - Gunakan fitur Evaluasi untuk mengukur kualitas agen secara luas

### Untuk pengguna Jalur B: Tingkatkan ke deployment cloud

Saat Anda siap mendeploy ke cloud:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Selesaikan [Modul 01, Setup](01-setup.md#step-2-set-up-based-on-your-access) (buat proyek, deploy model, tetapkan RBAC)
3. Perbarui `.env` dengan endpoint proyek Foundry dan nama deployment model
4. Lanjutkan dari [Modul 05 - Deploy ke Foundry](05-deploy-to-foundry.md)

---

## Bersihkan sumber daya (opsional)

Jika Anda ingin menghapus sumber daya Azure yang dibuat selama workshop ini:

### Opsi 1: Hapus grup sumber daya (menghapus semua)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsi 2: Hapus hanya agen yang dihosting

1. Buka [ai.azure.com](https://ai.azure.com) → proyek Anda → **Build** → **Agents**.
2. Klik agen Anda → klik **Delete**.

### Opsi 3: Hapus deployment model

1. Di sidebar Foundry, kembangkan proyek Anda → **Models**.
2. Klik kanan deployment model → **Delete**.

> **Catatan biaya:** Agen yang dihosting hanya dikenakan biaya saat berjalan. Jika Anda menghentikan atau menghapus agen, tidak ada biaya berkelanjutan. Deployment model mungkin menimbulkan biaya kecil untuk kapasitas yang dipesan - hapus jika sudah selesai.

---

**Sebelumnya:** [06 - Verifikasi di Playground](06-verify-in-playground.md) · **Selanjutnya:** [08 - Pemecahan Masalah (Referensi) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->