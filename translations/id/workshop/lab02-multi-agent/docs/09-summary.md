# Modul 9 - Ringkasan & Langkah Selanjutnya

⏱️ ~5 menit

**Selamat!** Anda telah membangun, menguji, dan (jika di Jalur A) menerapkan alur kerja multi-agen menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang Anda bangun

**Resume → Job Fit Evaluator** - alur kerja multi-agen yang dihosting yang:
- Menerima resume + deskripsi pekerjaan melalui HTTP (`POST /responses`)
- Menjalankan empat agen khusus dalam pipeline berurutan - setiap agen meneruskan data yang dibutuhkan penerusnya
- Mengembalikan skor kecocokan (0–100 dengan rincian), daftar kesenjangan keterampilan dan sertifikasi, dan peta pembelajaran pribadi dengan tautan Microsoft Learn asli untuk setiap kesenjangan
- Memanggil server Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) untuk mengambil sumber belajar resmi untuk setiap kesenjangan keterampilan yang diidentifikasi
- Berjalan sebagai satu agen containerized yang dihosting di Microsoft Foundry Agent Service

---

## Konsep kunci yang dipelajari

| Konsep | Apa yang Anda latih |
|---------|-------------------|
| **Orkestrasi multi-agen** | `WorkflowBuilder` pipeline berurutan dengan `add_edge()` |
| **Spesialisasi agen** | Empat agen fokus mengungguli satu agen serbaguna |
| **Polanya Content Router** | ResumeParser juga berfungsi sebagai router - menjaga teks JD dalam bagian `[JOB DESCRIPTION PASS-THROUGH]` agar agen-agennya bisa mengaksesnya (diperlukan karena `context_mode="last_agent"` membuat hanya `start_executor` yang melihat pesan mentah pengguna) |
| **Polanya Content Relay** | Agen JD meneruskan `[PARSED RESUME PASS-THROUGH]` ke depan sehingga MatchingAgent mendapatkan keduanya; menghindari double-trigger semantik OR yang terjadi di grafik fan-in |
| **Integrasi alat MCP** | `@tool` + `streamable_http_client` memanggil server MCP eksternal |
| **Siklus Hidup Agen Hosted** | Scaffold → Konfigurasi → Uji lokal → Deploy → Verifikasi di cloud |
| **`context_mode="last_agent"`** | Setiap eksekutor hanya melihat output dari pendahulu langsungnya |
| **Alur kerja Foundry Toolkit** | Wizard scaffold, Agent Inspector, Workflow Visualizer, deploy sekali klik |

---

## Apa yang Anda selesaikan

<details open>
<summary><strong>🅰️ Jalur A - Langganan Foundry</strong></summary>

- [x] Memverifikasi pengaturan Lab 01: proyek, model, dan RBAC masih aktif
- [x] Membuat proyek multi-agen menggunakan template Workflows
- [x] Menulis empat set instruksi agen (ResumeParser, Agen JD, MatchingAgent, GapAnalyzer)
- [x] Mengintegrasikan alat Microsoft Learn MCP dengan `streamable_http_client`
- [x] Menghubungkan graf workflow dengan `WorkflowBuilder` (pipeline berurutan dengan content relay)
- [x] Menguji secara lokal dengan 2 tes awal (Agent Inspector) - skor kecocokan, kartu kesenjangan, dan URL MCP
- [x] Menerapkan ke Foundry Agent Service (containerized, managed identity)
- [x] Memverifikasi di playground cloud - konsistensi struktural dengan hasil lokal

</details>

<details open>
<summary><strong>🅱️ Jalur B - Foundry Lokal</strong></summary>

- [x] Memverifikasi pengaturan Lab 01: Foundry Lokal berjalan dengan model lokal
- [x] Membuat proyek multi-agen menggunakan template Workflows
- [x] Menulis empat set instruksi agen dan menghubungkan graf workflow
- [x] Mengintegrasikan alat Microsoft Learn MCP
- [x] Menguji secara lokal dengan 2 tes awal
- [x] Memvalidasi perilaku multi-agen tanpa membutuhkan sumber daya cloud

</details>

---

## Langkah selanjutnya

### Lanjutkan belajar

| Sumber Daya | Deskripsi |
|----------|-------------|
| **[Referensi Agent Framework SDK](https://learn.microsoft.com/agent-framework/)** | Dokumentasi API untuk `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog alat MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Hubungkan agen ke server MCP lain (Bing, GitHub, khusus) |
| **[Tambah pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Membumikan agen dengan dokumen, penyimpanan vektor, atau pencarian Bing |
| **[Evaluasi Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Mengukur kualitas agen secara skala dengan evaluator otomatis |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Referensi lengkap platform |
| **[Foundry Toolkit - Apa Yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Catatan rilis ekstensi dan log perubahan |

### Ide untuk memperluas alur kerja ini

- **Tambah agen ke-5** - Pelatih wawancara yang menghasilkan pertanyaan wawancara yang mungkin berdasarkan laporan kesenjangan
- **Tambah alat pembumian Bing** - Biarkan Agen JD mencari lowongan kerja serupa untuk memperkaya persyaratan
- **Hubungkan ke database resume** - Tarik profil kandidat dari database lewat `@tool` khusus
- **Coba model berbeda** - Bandingkan kualitas keluaran dan latensi `gpt-4.1` vs. `gpt-4.1-mini`
- **Evaluasi dengan Foundry** - Gunakan fitur Evaluasi untuk memberi skor laporan kecocokan terhadap dataset emas

### Untuk pengguna Jalur B: Upgrade ke penerapan cloud

Saat Anda siap menerapkan ke cloud:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Selesaikan [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (buat proyek, deploy model, tetapkan RBAC)
3. Perbarui `.env` Anda dengan endpoint proyek Foundry dan nama deploy model
4. Lanjutkan dari [Modul 06 - Deploy ke Foundry](06-deploy-to-foundry.md)

---

## Bersihkan sumber daya (opsional)

Jika Anda ingin menghapus sumber daya Azure yang dibuat selama workshop ini:

### Opsi 1: Hapus grup sumber daya (menghapus semua)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Opsi 2: Hapus hanya agen yang dihosting

1. Buka [ai.azure.com](https://ai.azure.com) → proyek Anda → **Build** → **Agents**.
2. Temukan **PersonalCareerCopilot** → klik **Delete**.

### Opsi 3: Hapus deploy model

1. Di sidebar Foundry, perluas proyek Anda → **Models**.
2. Klik kanan deploy model → **Delete**.

> **Catatan biaya:** Agen yang dihosting hanya dikenakan biaya saat berjalan. Jika Anda menghentikan atau menghapus agen, tidak ada biaya berkelanjutan. Deploy model mungkin dikenakan biaya kecil untuk kapasitas cadangan - hapus jika sudah selesai.

---

**Sebelumnya:** [08 - Troubleshooting](08-troubleshooting.md) · **Beranda:** [Lab 02 README](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->