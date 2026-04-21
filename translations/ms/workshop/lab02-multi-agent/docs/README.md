# Makmal 02 - Aliran Kerja Berbilang Ejen: Penilai Kesesuaian Resume → Kerja

## Laluan Pembelajaran Penuh

Dokumentasi ini membimbing anda membina, menguji, dan melancarkan **aliran kerja berbilang ejen** yang menilai kesesuaian resume-ke-kerja menggunakan empat ejen khusus yang diorkestrakan melalui **WorkflowBuilder**.

> **Prasyarat:** Lengkapkan [Makmal 01 - Ejen Tunggal](../../lab01-single-agent/README.md) sebelum memulakan Makmal 02.

---

## Modul

| # | Modul | Apa yang akan anda lakukan |
|---|--------|----------------------------|
| 0 | [Prasyarat](00-prerequisites.md) | Sahkan penyelesaian Makmal 01, fahami konsep berbilang ejen |
| 1 | [Fahami Seni Bina Berbilang Ejen](01-understand-multi-agent.md) | Pelajari WorkflowBuilder, peranan ejen, graf orkestrasi |
| 2 | [Bina Projek Berbilang Ejen](02-scaffold-multi-agent.md) | Gunakan sambungan Foundry untuk membina aliran kerja berbilang ejen |
| 3 | [Konfigurasikan Ejen & Persekitaran](03-configure-agents.md) | Tulis arahan untuk 4 ejen, konfigurasikan alat MCP, tetapkan pembolehubah persekitaran |
| 4 | [Corak Orkestrasi](04-orchestration-patterns.md) | Teroka pengeluaran kipas selari, penggabungan bersiri, dan corak alternatif |
| 5 | [Uji Secara Tempatan](05-test-locally.md) | Debug F5 dengan Pemeriksa Ejen, jalankan ujian asap dengan resume + JD |
| 6 | [Lancarkan ke Foundry](06-deploy-to-foundry.md) | Bina bekas, tolak ke ACR, daftar ejen yang dihoskan |
| 7 | [Sahkan di Playground](07-verify-in-playground.md) | Uji ejen yang dilancarkan dalam VS Code dan portal Foundry playground |
| 8 | [Penyelesaian Masalah](08-troubleshooting.md) | Betulkan isu berbilang ejen biasa (ralat MCP, output terpotong, versi pakej) |

---

## Anggaran masa

| Tahap pengalaman | Masa |
|------------------|------|
| Baru sahaja menamatkan Makmal 01 | 45-60 minit |
| Ada pengalaman Azure AI | 60-90 minit |
| Kali pertama dengan berbilang ejen | 90-120 minit |

---

## Seni Bina sekilas

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

**Kembali ke:** [Makmal 02 README](../README.md) · [Laman Utama Bengkel](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->