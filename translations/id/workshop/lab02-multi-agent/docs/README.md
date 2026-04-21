# Lab 02 - Alur Kerja Multi-Agen: Evaluator Kesesuaian Resume → Pekerjaan

## Jalur Pembelajaran Lengkap

Dokumentasi ini memandu Anda melalui pembuatan, pengujian, dan penerapan **alur kerja multi-agen** yang mengevaluasi kesesuaian resume terhadap pekerjaan menggunakan empat agen khusus yang diorkestrasi melalui **WorkflowBuilder**.

> **Prasyarat:** Selesaikan [Lab 01 - Agen Tunggal](../../lab01-single-agent/README.md) sebelum memulai Lab 02.

---

## Modul

| # | Modul | Apa yang akan Anda lakukan |
|---|--------|----------------------------|
| 0 | [Prasyarat](00-prerequisites.md) | Verifikasi penyelesaian Lab 01, pahami konsep multi-agen |
| 1 | [Pahami Arsitektur Multi-Agen](01-understand-multi-agent.md) | Pelajari WorkflowBuilder, peran agen, grafik orkestrasi |
| 2 | [Susun Proyek Multi-Agen](02-scaffold-multi-agent.md) | Gunakan ekstensi Foundry untuk membuat kerangka alur kerja multi-agen |
| 3 | [Konfigurasikan Agen & Lingkungan](03-configure-agents.md) | Tulis instruksi untuk 4 agen, konfigurasikan alat MCP, atur variabel lingkungan |
| 4 | [Pola Orkestrasi](04-orchestration-patterns.md) | Jelajahi fan-out paralel, agregasi berurutan, dan pola alternatif |
| 5 | [Uji Secara Lokal](05-test-locally.md) | Debug dengan F5 menggunakan Agent Inspector, jalankan tes awal dengan resume + JD |
| 6 | [Deploy ke Foundry](06-deploy-to-foundry.md) | Bangun container, dorong ke ACR, daftarkan agen yang di-hosting |
| 7 | [Verifikasi di Playground](07-verify-in-playground.md) | Uji agen yang sudah dideploy di VS Code dan playground Foundry Portal |
| 8 | [Pemecahan Masalah](08-troubleshooting.md) | Perbaiki masalah umum multi-agen (error MCP, output terpotong, versi paket) |

---

## Perkiraan waktu

| Tingkat pengalaman | Waktu |
|--------------------|-------|
| Baru saja menyelesaikan Lab 01 | 45-60 menit |
| Memiliki pengalaman Azure AI | 60-90 menit |
| Pertama kali dengan multi-agen | 90-120 menit |

---

## Arsitektur sekilas

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Kembali ke:** [Lab 02 README](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berusaha untuk akurasi, harap diingat bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang salah yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->