# Modul 7 - Rumusan & Langkah Seterusnya

⏱️ ~5 minit

**Tahniah!** Anda telah membina, menguji, dan (jika pada Laluan A) melancarkan ejen AI yang dihoskan menggunakan Microsoft Foundry dan Foundry Toolkit untuk VS Code.

---

## Apa yang anda bina

Ejen **"Terangkan Seolah-olah Saya Eksekutif"** yang:
- Menerima laporan insiden teknikal atau kemas kini operasi melalui HTTP (`POST /responses`)
- Menterjemahkannya ke dalam rumusan eksekutif bahasa mudah
- Mengikuti format output yang berstruktur (Apa yang berlaku / Impak perniagaan / Langkah seterusnya)
- Menolak permintaan di luar topik dan percubaan suntikan arahan
- Beroperasi sebagai ejen yang dihoskan dalam kontena di Microsoft Foundry Agent Service

---

## Konsep penting yang dipelajari

| Konsep | Apa yang anda amalkan |
|---------|-------------------|
| **Arkitek Rangka Kerja Ejen** | Saluran `FoundryChatClient` → `Agent` → `ResponsesHostServer` |
| **Kitaran hidup Ejen Di hoskan** | Rangka → Konfigurasi → Uji secara tempatan → Lancar → Sahkan di awan |
| **Kejuruteraan arahan sistem** | Peranan, audiens, format output, peraturan, batasan keselamatan, dan contoh |
| **Perbezaan tempatan vs. dihoskan** | Identiti (kredensial peribadi vs. identiti terurus), titik akhir, laluan rangkaian |
| **Sempadan keselamatan** | Pertahanan suntikan arahan, pematuhan peranan, pengendalian rapi kes tepi |
| **Aliran kerja Foundry Toolkit** | Penciptaan projek, pelancaran model, rangka ejen, Pemeriksa Ejen, lancar satu klik |

---

## Apa yang anda selesaikan

### Laluan A (Langganan Foundry)

- [x] Menyediakan Foundry Toolkit dan mencipta projek Foundry dengan model yang dilancarkan
- [x] Merangka ejen yang dihoskan dengan struktur projek auto-dihasilkan
- [x] Menulis arahan ejen berstruktur dengan peraturan keselamatan
- [x] Menguji secara tempatan dengan 3 senario fungsian (Pemeriksa Ejen)
- [x] Melancarkan ke Foundry Agent Service (dalam kontena)
- [x] Mengesahkan di taman permainan awan dengan 4 ujian kes tepi/keselamatan

### Laluan B (Foundry Tempatan)

- [x] Menyediakan Foundry Toolkit dengan titik akhir model tempatan
- [x] Merangka projek ejen yang dihoskan
- [x] Menulis arahan ejen berstruktur dengan peraturan keselamatan
- [x] Menguji secara tempatan dengan 3 senario fungsian
- [x] Mengesahkan tingkah laku ejen tanpa memerlukan sumber awan

---

## Langkah seterusnya

### Teruskan pembelajaran

| Sumber | Penerangan |
|----------|-------------|
| **[Lab 02 - Orkestrasi Multi-Ejen](../../lab02-multi-agent/docs/README.md)** | Membina aliran kerja 4-ejen (Resume → Penilai Kesesuaian Kerja) dengan corak orkestrasi |
| **[Tambah alat ke ejen anda](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Sambungkan API, pangkalan data, atau fungsi tersuai melalui Katalog Alat |
| **[Tambah pengetahuan (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Mentapkan ejen anda dengan dokumen, stor vektor, atau carian Bing |
| **[Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/foundry/)** | Rujukan platform lengkap |
| **[Rujukan SDK Rangka Kerja Ejen](https://learn.microsoft.com/agent-framework/)** | Dokumen API untuk pakej `agent-framework` |
| **[Foundry Toolkit - Apa Yang Baru](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Nota pelepasan sambungan dan log perubahan |

### Idea untuk mengembangkan ejen anda

- **Tambah alat tarikh** - Benarkan ejen memasukkan konteks "sehingga hari ini" dalam rumusan
- **Sambungkan ke pangkalan data insiden** - Tarik butiran insiden sebenar melalui fungsi alat
- **Tambah alat mentapkan Bing** - Benarkan ejen mencari berita terkini untuk konteks tambahan
- **Cuba model berbeza** - Bandingkan kualiti output `gpt-4.1` vs. `gpt-4.1-mini`
- **Nilai dengan Foundry** - Gunakan ciri Penilaian untuk mengukur kualiti ejen secara skala

### Untuk pengguna Laluan B: Tingkatkan ke pelancaran awan

Apabila anda bersedia untuk melancarkan ke awan:
1. Dapatkan langganan Azure ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. Lengkapkan [Modul 01, Persediaan](01-setup.md#step-2-set-up-based-on-your-access) (cipta projek, lancar model, tugaskan RBAC)
3. Kemas kini `.env` anda dengan titik akhir projek Foundry dan nama pelancaran model
4. Teruskan dari [Modul 05 - Lancar ke Foundry](05-deploy-to-foundry.md)

---

## Bersihkan sumber (pilihan)

Jika anda ingin mengalih keluar sumber Azure yang dicipta semasa bengkel ini:

### Pilihan 1: Padam kumpulan sumber (membuang semuanya)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Pilihan 2: Padam hanya ejen yang dihoskan

1. Buka [ai.azure.com](https://ai.azure.com) → projek anda → **Build** → **Agents**.
2. Klik ejen anda → klik **Delete**.

### Pilihan 3: Padam pelancaran model

1. Dalam bar sisi Foundry, kembangkan projek anda → **Models**.
2. Klik kanan pelancaran model → **Delete**.

> **Nota kos:** Ejen yang dihoskan hanya mengenakan kos apabila beroperasi. Jika anda berhenti atau memadam ejen, tiada caj berterusan. Pelancaran model mungkin mengenakan caj kecil untuk kapasiti berreser; padam jika anda selesai.

---

**Sebelumnya:** [06 - Sahkan di Playground](06-verify-in-playground.md) · **Seterusnya:** [08 - Penyelesaian Masalah (Rujukan) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->