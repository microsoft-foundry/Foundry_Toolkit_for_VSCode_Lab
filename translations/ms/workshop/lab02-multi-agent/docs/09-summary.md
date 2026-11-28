# Modul 9 - Ringkasan & Langkah Seterusnya

⏱️ ~5 min

**Tahniah!** Anda telah membina, menguji, dan (jika dalam Laluan A) menggunakan aliran kerja berbilang ejen menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang anda bina

**Penilai Keserasian Resume → Kerja** - aliran kerja hos berbilang ejen yang:
- Menerima resume + deskripsi kerja melalui HTTP (`POST /responses`)
- Menjalankan empat ejen khusus dalam saluran berurutan - setiap ejen menyampaikan data yang diperlukan oleh ejen seterusnya
- Mengembalikan skor kesesuaian (0–100 dengan pecahan), senarai jurang kemahiran dan pensijilan, dan peta pembelajaran yang diperibadikan dengan pautan Microsoft Learn sebenar untuk setiap jurang
- Memanggil pelayan Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) untuk mendapatkan sumber pembelajaran rasmi bagi setiap jurang kemahiran yang dikenal pasti
- Berjalan sebagai ejen hos yang dipaketkan dalam satu bekas di Perkhidmatan Ejen Microsoft Foundry

---

## Konsep utama yang dipelajari

| Konsep | Apa yang anda amalkan |
|---------|-------------------|
| **Orkestrasi berbilang ejen** | saluran berurutan `WorkflowBuilder` dengan `add_edge()` |
| **Pengkhususan ejen** | Empat ejen fokus mengatasi satu ejen serba guna |
| **Corak Penghala Kandungan** | ResumeParser juga berfungsi sebagai penghala - ia mengekalkan teks JD dalam seksyen `[JOB DESCRIPTION PASS-THROUGH]` supaya ejen hiliran boleh mengaksesnya (diperlukan kerana `context_mode="last_agent"` bermakna hanya `start_executor` yang melihat mesej mentah pengguna) |
| **Corak Penyampaian Kandungan** | Ejen JD menyampaikan `[PARSED RESUME PASS-THROUGH]` ke hadapan supaya MatchingAgent mendapat kedua-dua profil; mengelakkan pencetus berganda semantik ATAU yang menyebabkan graf fan-in |
| **Integrasi alat MCP** | `@tool` + `streamable_http_client` memanggil pelayan MCP luar |
| **Kitar hidup Ejen Hos** | Buat Rangka → Konfigurasi → Uji secara tempatan → Lancarkan → Sahkan di awan |
| **`context_mode="last_agent"`** | Setiap pelaksana hanya melihat output daripada pendahulunya secara langsung |
| **Aliran kerja Foundry Toolkit** | Penyihir binaan, Pemeriksa Ejen, Visualisasi Aliran Kerja, lancar satu klik |

---

## Apa yang anda telah lengkapkan

<details open>
<summary><strong>🅰️ Laluan A - Langganan Foundry</strong></summary>

- [x] Sahkan persediaan Lab 01: projek, model, dan RBAC masih aktif
- [x] Membina projek berbilang ejen menggunakan templat Aliran Kerja
- [x] Menulis empat set arahan ejen (ResumeParser, Ejen JD, MatchingAgent, GapAnalyzer)
- [x] Mengintegrasikan alat Microsoft Learn MCP dengan `streamable_http_client`
- [x] Menghubungkan graf aliran kerja dengan `WorkflowBuilder` (saluran berurutan dengan penyampaian kandungan)
- [x] Uji secara tempatan dengan 2 ujian asap (Pemeriksa Ejen) - skor kesesuaian, kad jurang, dan URL MCP
- [x] Lancarkan ke Perkhidmatan Ejen Foundry (dipaketkan, identiti terurus)
- [x] Sahkan di kawasan awan permainan - konsistensi struktur dengan keputusan tempatan

</details>

<details open>
<summary><strong>🅱️ Laluan B - Foundry Tempatan</strong></summary>

- [x] Sahkan persediaan Lab 01: Foundry Tempatan berjalan dengan model tempatan
- [x] Membina projek berbilang ejen menggunakan templat Aliran Kerja
- [x] Menulis empat set arahan ejen dan menghubungkan graf aliran kerja
- [x] Mengintegrasikan alat Microsoft Learn MCP
- [x] Uji secara tempatan dengan 2 ujian asap
- [x] Sahkan tingkah laku berbilang ejen tanpa memerlukan sumber awan

</details>

---

## Langkah seterusnya

### Teruskan pembelajaran

| Sumber | Penerangan |
|----------|-------------|
| **[Rujukan SDK Rangka Kerja Ejen](https://learn.microsoft.com/agent-framework/)** | Dokumen API untuk `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog alat MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Sambungkan ejen ke pelayan MCP lain (Bing, GitHub, tersuai) |
| **[Tambah pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)** | Landas ejen dengan dokumen, stor vector, atau carian Bing |
| **[Penilaian Foundry](https://learn.microsoft.com/azure/foundry/concepts/evaluation-overview)** | Ukur kualiti ejen secara skala dengan penilai automatik |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Rujukan penuh platform |
| **[Foundry Toolkit - Apa Yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Nota keluaran sambungan dan log perubahan |

### Idea untuk mengembangkan aliran kerja ini

- **Tambah ejen ke-5** - Jurulatih temuduga yang menghasilkan soalan temuduga yang mungkin berdasarkan laporan jurang
- **Tambah alat grounding Bing** - Biarkan Ejen JD mencari iklan kerja serupa untuk memperkayakan keperluan
- **Sambungkan ke pangkalan data resume** - Tarik profil calon dari pangkalan data melalui `@tool` tersuai
- **Cuba model berbeza** - Bandingkan kualiti output dan kelewatan `gpt-4.1` vs. `gpt-4.1-mini`
- **Nilai dengan Foundry** - Gunakan ciri Penilaian untuk menilai laporan keserasian terhadap dataset emas

### Untuk pengguna Laluan B: Tingkatkan ke pelancaran awan

Apabila anda bersedia untuk melancarkan ke awan:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lengkapkan [Lab 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (bina projek, lancarkan model, tetapkan RBAC)
3. Kemas kini `.env` anda dengan titik hujung projek Foundry dan nama pelancaran model
4. Teruskan dari [Modul 06 - Lancarkan ke Foundry](06-deploy-to-foundry.md)

---

## Bersihkan sumber (pilihan)

Jika anda mahu mengalih keluar sumber Azure yang dibuat semasa bengkel ini:

### Pilihan 1: Padamkan kumpulan sumber (menghapuskan semua)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Pilihan 2: Padam hanya ejen yang dihoskan

1. Buka [ai.azure.com](https://ai.azure.com) → projek anda → **Bina** → **Ejen**.
2. Cari **PersonalCareerCopilot** → klik **Padam**.

### Pilihan 3: Padam pelancaran model

1. Dalam bar sisi Foundry, kembangkan projek anda → **Model**.
2. Klik kanan pelancaran model → **Padam**.

> **Nota kos:** Ejen yang dihoskan hanya dikenakan kos apabila berjalan. Jika anda berhenti atau memadam ejen, tiada caj berterusan. Pelancaran model mungkin dikenakan caj kecil untuk kapasiti yang ditempah - padam jika anda sudah selesai.

---

**Sebelumnya:** [08 - Penyelesaian Masalah](08-troubleshooting.md) · **Utama:** [Lab 02 README](../README.md) · [Laman Utama Bengkel](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->