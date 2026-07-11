# Modul 9 - Ringkasan & Langkah Selanjutnya

⏱️ ~5 menit

**Selamat!** Anda telah membangun, menguji, dan (jika di Jalur A) menerapkan alur kerja multi-agen menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang Anda bangun

**Resume → Evaluator Kecocokan Pekerjaan** - sebuah alur kerja multi-agen yang dihosting yang:
- Menerima resume + deskripsi pekerjaan melalui HTTP (`POST /responses`)
- Menjalankan empat agen khusus dalam pipeline berurutan - setiap agen meneruskan data yang diperlukan oleh agen penggantinya
- Mengembalikan skor kecocokan (0–100 dengan rincian), daftar kekurangan keterampilan dan sertifikasi, dan roadmap pembelajaran yang dipersonalisasi dengan tautan Microsoft Learn nyata untuk setiap kekurangan
- Memanggil server MCP Microsoft Learn (`https://learn.microsoft.com/api/mcp`) untuk mengambil sumber belajar resmi untuk setiap kekurangan keterampilan yang diidentifikasi
- Berjalan sebagai satu agen containerized yang dihosting di Microsoft Foundry Agent Service

---

## Konsep utama yang dipelajari

| Konsep | Apa yang Anda praktikkan |
|---------|-------------------|
| **Orkestrasi multi-agen** | pipeline berurutan `WorkflowBuilder` dengan `add_edge()` |
| **Spesialisasi agen** | Empat agen fokus mengungguli satu agen serba guna |
| **Pola Router Konten** | ResumeParser juga berfungsi sebagai router - ia mempertahankan teks JD dalam bagian `[JOB DESCRIPTION PASS-THROUGH]` sehingga agen berikutnya dapat mengaksesnya (diperlukan karena `context_mode="last_agent"` berarti hanya `start_executor` yang melihat pesan pengguna mentah) |
| **Pola Relay Konten** | Agen JD meneruskan `[PARSED RESUME PASS-THROUGH]` ke depan sehingga MatchingAgent mendapatkan kedua profil; menghindari pemicu ganda OR-semantik yang disebabkan oleh grafik fan-in |
| **Integrasi alat MCP** | `@tool` + `streamable_http_client` memanggil server MCP eksternal |
| **Siklus hidup Agen yang dihosting** | Scaffold → Konfigurasi → Uji lokal → Deploy → Verifikasi di cloud |
| **`context_mode="last_agent"`** | Setiap executor hanya melihat output dari pendahulu langsungnya |
| **Alur kerja Foundry Toolkit** | Scaffold wizard, Agent Inspector, Workflow Visualizer, deploy sekali klik |

---

## Apa yang Anda selesaikan

<details open>
<summary><strong>🅰️ Jalur A - Langganan Foundry</strong></summary>

- [x] Memverifikasi pengaturan Lab 01: proyek, model, dan RBAC masih aktif
- [x] Membuat scaffold proyek multi-agen menggunakan templat Workflows
- [x] Menulis empat set instruksi agen (ResumeParser, Agen JD, MatchingAgent, GapAnalyzer)
- [x] Mengintegrasikan alat Microsoft Learn MCP dengan `streamable_http_client`
- [x] Menghubungkan grafik alur kerja dengan `WorkflowBuilder` (pipeline berurutan dengan relay konten)
- [x] Menguji secara lokal dengan 3 tes asap (Agent Inspector) - skor kecocokan, kartu kekurangan, dan URL MCP
- [x] Menerapkan ke Foundry Agent Service (containerized, identity terkelola)
- [x] Memverifikasi di playground cloud - konsistensi struktural dengan hasil lokal

</details>

<details open>
<summary><strong>🅱️ Jalur B - Foundry Lokal</strong></summary>

- [x] Memverifikasi pengaturan Lab 01: Foundry Lokal berjalan dengan model lokal
- [x] Membuat scaffold proyek multi-agen menggunakan templat Workflows
- [x] Menulis empat set instruksi agen dan menghubungkan grafik alur kerja
- [x] Mengintegrasikan alat Microsoft Learn MCP
- [x] Menguji secara lokal dengan 3 tes asap
- [x] Memvalidasi perilaku multi-agen tanpa memerlukan sumber daya cloud

</details>

---

## Langkah selanjutnya

### Lanjutkan belajar

| Sumber Daya | Deskripsi |
|----------|-------------|
| **[Referensi Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Dokumentasi API untuk `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog alat MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Menghubungkan agen ke server MCP lain (Bing, GitHub, kustom) |
| **[Tambah pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Memberi dasar kepada agen dengan dokumen, penyimpanan vektor, atau pencarian Bing |
| **[Evaluasi Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Mengukur kualitas agen secara skala besar dengan evaluator otomatis |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referensi platform lengkap |
| **[Foundry Toolkit - Apa yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Catatan rilis ekstensi dan changelog |

### Ide untuk memperluas alur kerja ini

- **Tambahkan agen ke-5** - Pelatih wawancara yang menghasilkan kemungkinan pertanyaan wawancara berdasarkan laporan kekurangan
- **Tambahkan alat grounding Bing** - Biarkan Agen JD mencari lowongan kerja serupa untuk memperkaya persyaratan
- **Hubungkan ke basis data resume** - Ambil profil kandidat dari database melalui `@tool` kustom
- **Coba model berbeda** - Bandingkan kualitas output dan latensi `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluasi dengan Foundry** - Gunakan fitur Evaluasi untuk menilai laporan kecocokan terhadap dataset emas

### Untuk pengguna Jalur B: Tingkatkan ke penerapan cloud

Saat Anda siap untuk menerapkan ke cloud:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Selesaikan [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (buat proyek, terapkan model, tetapkan RBAC)
3. Perbarui `.env` Anda dengan endpoint proyek Foundry dan nama penerapan model
4. Lanjutkan dari [Modul 06 - Deploy ke Foundry](06-deploy-to-foundry.md)

---

## Bersihkan sumber daya (opsional)

Jika Anda ingin menghapus sumber daya Azure yang dibuat selama lokakarya ini:

### Pilihan 1: Hapus grup sumber daya (menghapus semuanya)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Pilihan 2: Hapus hanya agen yang dihosting

1. Buka [ai.azure.com](https://ai.azure.com) → proyek Anda → **Build** → **Agents**.
2. Temukan **PersonalCareerCopilot** → klik **Delete**.

### Pilihan 3: Hapus penerapan model

1. Di sidebar Foundry, perluas proyek Anda → **Models**.
2. Klik kanan penerapan model → **Delete**.


> **Catatan biaya:** Agen yang dihosting hanya menimbulkan biaya saat berjalan. Jika Anda menghentikan atau menghapus agen, tidak ada biaya berkelanjutan. Penyebaran model mungkin menimbulkan biaya kecil untuk kapasitas yang dipesan - hapus jika sudah selesai.

---

**Sebelumnya:** [08 - Troubleshooting](08-troubleshooting.md) · **Beranda:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->