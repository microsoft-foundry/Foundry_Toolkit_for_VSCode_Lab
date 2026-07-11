# Modul 9 - Ringkasan & Langkah Seterusnya

⏱️ ~5 min

**Tahniah!** Anda telah membina, menguji, dan (jika di Laluan A) melancarkan aliran kerja berbilang ejen menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang anda bina

**Penilai Keserasian Resume → Kerja** - aliran kerja berbilang ejen yang dihoskan yang:
- Menerima resume + penerangan kerja melalui HTTP (`POST /responses`)
- Menjalankan empat ejen khusus dalam saluran berurutan - setiap ejen menyampaikan data yang diperlukan oleh ejen penggantiannya
- Mengembalikan skor kesesuaian (0–100 dengan pecahan), senarai jurang kemahiran dan sijil, serta peta pembelajaran peribadi dengan pautan Microsoft Learn sebenar untuk setiap jurang
- Memanggil pelayan Microsoft Learn MCP (`https://learn.microsoft.com/api/mcp`) untuk mendapatkan sumber pembelajaran rasmi bagi setiap jurang kemahiran yang dikenal pasti
- Berjalan sebagai ejen dihoskan berkontena tunggal dalam Perkhidmatan Ejen Microsoft Foundry

---

## Konsep utama yang dipelajari

| Konsep | Apa yang anda amalkan |
|---------|-------------------|
| **Orkestrasi berbilang ejen** | Saluran berurutan `WorkflowBuilder` dengan `add_edge()` |
| **Pengkhususan ejen** | Empat ejen khusus mengatasi satu ejen tujuan umum |
| **Corak Penghala Kandungan** | ResumeParser berfungsi juga sebagai penghala - ia mengekalkan teks JD dalam seksyen `[JOB DESCRIPTION PASS-THROUGH]` supaya ejen hiliran boleh mengaksesnya (diperlukan kerana `context_mode="last_agent"` bermakna hanya `start_executor` melihat mesej pengguna mentah) |
| **Corak Penyampaian Kandungan** | Ejen JD menyampaikan `[PARSED RESUME PASS-THROUGH]` ke hadapan supaya MatchingAgent mendapat kedua-dua profil; mengelakkan pencetus berganda semantik OR yang disebabkan oleh graf penggabungan |
| **Integrasi alat MCP** | `@tool` + `streamable_http_client` memanggil pelayan MCP luaran |
| **Kitaran hayat Ejen dihoskan** | Kerangka → Konfigurasi → Uji secara tempatan → Lancar → Sahkan dalam awan |
| **`context_mode="last_agent"`** | Setiap pelaksana hanya melihat output daripada pendahulu langsungnya |
| **Aliran kerja Foundry Toolkit** | Wizad kerangka, Pemeriksa Ejen, Visualizer Aliran Kerja, lancar satu klik |

---

## Apa yang anda lengkapkan

<details open>
<summary><strong>🅰️ Laluan A - Langganan Foundry</strong></summary>

- [x] Mengesahkan persediaan Makmal 01: projek, model, dan RBAC masih aktif
- [x] Membina kerangka projek berbilang ejen menggunakan templat Aliran Kerja
- [x] Menulis empat set arahan ejen (ResumeParser, Ejen JD, MatchingAgent, GapAnalyzer)
- [x] Mengintegrasi alat Microsoft Learn MCP dengan `streamable_http_client`
- [x] Menghubungkan graf aliran kerja dengan `WorkflowBuilder` (saluran berurutan dengan penyampaian kandungan)
- [x] Menguji secara tempatan dengan 3 ujian asas (Pemeriksa Ejen) - skor kesesuaian, kad jurang, dan URL MCP
- [x] Melancarkan ke Perkhidmatan Ejen Foundry (berkontena, identiti terurus)
- [x] Mengesahkan di ruang awan - konsistensi struktur dengan keputusan tempatan

</details>

<details open>
<summary><strong>🅱️ Laluan B - Foundry Tempatan</strong></summary>

- [x] Mengesahkan persediaan Makmal 01: Foundry Tempatan berjalan dengan model tempatan
- [x] Membina kerangka projek berbilang ejen menggunakan templat Aliran Kerja
- [x] Menulis empat set arahan ejen dan menghubungkan graf aliran kerja
- [x] Mengintegrasi alat Microsoft Learn MCP
- [x] Menguji secara tempatan dengan 3 ujian asas
- [x] Mengesahkan tingkah laku berbilang ejen tanpa perlu sumber awan

</details>

---

## Langkah seterusnya

### Teruskan pembelajaran

| Sumber | Penerangan |
|----------|-------------|
| **[Rujukan SDK Rangka Kerja Ejen](https://learn.microsoft.com/agent-framework/)** | Dokumentasi API untuk `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` |
| **[Katalog alat MCP](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Sambungkan ejen ke pelayan MCP lain (Bing, GitHub, tersuai) |
| **[Tambah pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Dasarkan ejen dengan dokumen, stor vektor, atau carian Bing |
| **[Penilaian Foundry](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Ukur kualiti ejen pada skala besar dengan penilai automatik |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Rujukan platform penuh |
| **[Foundry Toolkit - Apa Yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Nota keluaran sambungan dan log perubahan |

### Idea untuk memperluaskan aliran kerja ini

- **Tambah ejen ke-5** - Jurulatih temuduga yang menghasilkan soalan temuduga yang mungkin berdasarkan laporan jurang
- **Tambah alat pembumian Bing** - Benarkan Ejen JD mencari tawaran kerja serupa untuk memperkayakan keperluan
- **Sambungkan ke pangkalan data resume** - Tarik profil calon dari pangkalan data melalui `@tool` tersuai
- **Cuba model berlainan** - Bandingkan kualiti output dan kelewatan `gpt-4.1` vs. `gpt-4.1-mini`
- **Nilai dengan Foundry** - Gunakan ciri Penilaian untuk skor laporan keserasian berbanding set data emas

### Untuk pengguna Laluan B: Naik taraf ke pelancaran awan

Apabila anda sudah bersedia untuk melancarkan ke awan:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lengkapkan [Makmal 01, Modul 01](../../lab01-single-agent/docs/01-setup.md) (cipta projek, lancar model, tugaskan RBAC)
3. Kemas kini `.env` anda dengan titik hujung projek Foundry dan nama pelancaran model
4. Teruskan dari [Modul 06 - Lancar ke Foundry](06-deploy-to-foundry.md)

---

## Bersihkan sumber (pilihan)

Jika anda ingin mengalih keluar sumber Azure yang dibuat semasa bengkel ini:

### Pilihan 1: Padam kumpulan sumber (mengalih keluar semuanya)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Pilihan 2: Padam hanya ejen dihoskan

1. Buka [ai.azure.com](https://ai.azure.com) → projek anda → **Bangunkan** → **Ejen**.
2. Cari **PersonalCareerCopilot** → klik **Padam**.

### Pilihan 3: Padam pelancaran model

1. Dalam bar sisi Foundry, kembangkan projek anda → **Model**.
2. Klik kanan pelancaran model → **Padam**.

> **Nota kos:** Ejen dihoskan hanya mengenakan kos semasa berjalan. Jika anda menghentikan atau memadam ejen, tiada caj berterusan. Pelancaran model mungkin mengenakan caj kecil untuk kapasiti yang diperuntukkan - padam jika anda sudah selesai.

---

**Sebelum ini:** [08 - Penyelesaian Masalah](08-troubleshooting.md) · **Utama:** [Lab 02 README](../README.md) · [Laman Utama Bengkel](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->