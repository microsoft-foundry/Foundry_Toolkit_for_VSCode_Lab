# Lab 02 - Alur Kerja Multi-Agen: Resume → Evaluator Kesesuaian Pekerjaan

## Jalur Pembelajaran Lengkap

Dokumentasi ini memandu Anda membangun, menguji, dan menerapkan **alur kerja multi-agen** yang menilai kesesuaian resume dengan pekerjaan menggunakan empat agen khusus yang diorkestrasi melalui **WorkflowBuilder**.

> **Prasyarat:** Selesaikan [Lab 01 - Agen Tunggal](../../lab01-single-agent/README.md) sebelum memulai Lab 02.

---

## Modul

| # | Modul | Apa yang akan Anda lakukan |
|---|--------|--------------------------|
| 0 | [Pendahuluan](00-prerequisites.md) | Apa yang akan Anda bangun, verifikasi Lab 01, perbandingan Lab 02 vs Lab 01 |
| 1 | [Memahami Arsitektur Multi-Agen](01-understand-multi-agent.md) | Pelajari WorkflowBuilder, peran agen, grafik orkestrasi |
| 2 | [Membuat Proyek Multi-Agen](02-scaffold-multi-agent.md) | Gunakan wizard ekstensi Foundry untuk membuat proyek dasar |
| 3 | [Konfigurasi Agen & Lingkungan](03-configure-agents.md) | Menulis instruksi untuk 4 agen, konfigurasi alat MCP, atur variabel lingkungan |
| 4 | [Pola Orkestrasi](04-orchestration-patterns.md) | Rangkaian berurutan, relay konten, dan semantik OR WorkflowBuilder |
| 5 | [Uji Secara Lokal](05-test-locally.md) | Debug F5 dengan Agent Inspector, jalankan tes dasar dengan resume + JD |
| 6 | [Terapkan ke Foundry](06-deploy-to-foundry.md) | Bangun container, dorong ke ACR, daftarkan agen yang dihosting |
| 7 | [Verifikasi di Playground](07-verify-in-playground.md) | Uji agen yang diterapkan di playground VS Code dan Foundry Portal |
| 8 | [Pemecahan Masalah](08-troubleshooting.md) | Perbaiki masalah umum multi-agen (kesalahan MCP, output terpotong, versi paket) |
| 9 | [Ringkasan & Langkah Selanjutnya](09-summary.md) | Apa yang telah Anda bangun, konsep kunci yang dipelajari, pembersihan, dan arahan selanjutnya |

---

**Kembali ke:** [Lab 02 README](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->