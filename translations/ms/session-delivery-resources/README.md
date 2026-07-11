# Cara menyampaikan sesi ini

Terima kasih kerana menyampaikan sesi ini!

Sebelum menyampaikan bengkel, sila:

1. Baca dokumen ini dan semua sumber yang disertakan sepenuhnya.
2. Tonton rakaman penyampaian sesi dan perbincangan bengkel secara menyeluruh.
3. Lalui kedua-dua makmal latihan secara menyeluruh pada mesin anda sendiri **sekurang-kurangnya sekali** sebelum acara.
4. Sahihkan projek Microsoft Foundry, penyebaran model, dan kuota anda.
5. Hubungi penyelenggara jika ada apa-apa yang tidak jelas.

---

## Ringkasan fail

| Sumber                       | Pautan                                                                            | Penerangan                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Slide dek bengkel             | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Slaid pembentangan untuk bengkel ini dengan nota penyampai dan video demo terbenam           |
| Rakaman penyampaian sesi      | _Akan disediakan oleh penyelenggara_                                               | Rakaman pengenalan bengkel dan perbincangan slaid                                          |
| Rakaman bengkel secara menyeluruh | _Akan disediakan oleh penyelenggara_                                               | Rakaman dari awal hingga akhir bagi kedua-dua makmal latihan dari perspektif pelajar         |
| Dokumentasi bengkel           | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repositori sumber, README makmal, modul langkah demi langkah                               |
| Makmal 01 - ejen tunggal      | [Lab 01](../workshop/lab01-single-agent/README.md)                               | Makmal latihan: bina, uji, dan sebarkan ejen *Explain Like I'm an Executive*                  |
| Makmal 02 - aliran kerja berbilang ejen | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | Makmal latihan: bina aliran kerja 4 ejen *Resume to Job Fit Evaluator*                       |
| Demo 1: Ejen Eksekutif             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | Demo Makmal 01: terjemahkan jargon teknikal ke dalam ringkasan eksekutif                     |
| Demo 2: Penilai Kesesuaian Kerja Resume | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Demo Makmal 02: aliran kerja 4 ejen yang menilai kesesuaian resume-kerja dan menjana cadangan |

> **Nota untuk jurulatih:** Dek slaid dan pautan video akan ditambah setelah rakaman diterbitkan. Sehingga itu, hubungi penyelenggara (lihat [Contacts](#kontak)) untuk aset terkini.

---

## Mulakan

Bengkel ini mengajar pembangun cara membina, menguji, dan menyebarkan ejen AI ke **Microsoft Foundry Agent Service** sebagai **Ejen Dihoskan** sepenuhnya dari VS Code, menggunakan sambungan **Microsoft Foundry Toolkit**.

Bengkel dibahagikan kepada beberapa bahagian termasuk slaid, **2 demo langsung**, dan **2 makmal latihan**.

### Masa

#### Penyampaian penuh (kira-kira 2 jam)

| Masa            | Penerangan                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Pengenalan: ejen dihoskan, Foundry Agent Service, dan toolkit         |
| 10:00 - 20:00   | Demo: Ejen Eksekutif dari awal hingga akhir                          |
| 20:00 - 60:00   | Makmal 01 - ejen tunggal (bina, uji secara lokal, sebarkan, tempat latihan)     |
| 60:00 - 110:00  | Makmal 02 - aliran kerja berbilang ejen (Penilai Kesesuaian Kerja Resume)         |
| 110:00 - 120:00 | Penutup, soal jawab, dan sumber pembelajaran lanjut                  |

#### Penyampaian singkat (kira-kira 75 minit)

| Masa          | Penerangan                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Pengenalan dan gambaran umum                                |
| 10:00 - 20:00 | Demo: Ejen Eksekutif                                        |
| 20:00 - 70:00 | Hanya Makmal 01 (arahkan peserta ke Makmal 02 sebagai belajar kendiri)        |
| 70:00 - 75:00 | Penutup dan soal jawab                                      |

### Persediaan

| Sumber                        | Pautan                                                                                          | Penerangan                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Dokumentasi bengkel          | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Dokumentasi bengkel dan sumber                   |
| Arahan Makmal 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Makmal latihan: ejen dihoskan tunggal            |
| Arahan Makmal 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Makmal latihan: aliran kerja berbilang ejen     |
| Senarai semak prasyarat       | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Alat, akaun, dan akses Azure yang diperlukan      |
| Mula cepat ejen dihoskan (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Mula cepat rasmi untuk menyebarkan ejen dihoskan dengan `azd` |
| Ketersediaan rantau ejen dihoskan | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Rantau yang disokong untuk ejen dihoskan (pratonton) |

### Prasyarat untuk jurulatih

Sebelum menyampaikan, pastikan anda mempunyai:

- **Langganan Azure** dengan kebenaran untuk mencipta sumber (Pemilik atau Penyumbang pada kumpulan sumber).
- Akses ke **projek Microsoft Foundry** dalam [rantau yang menyokong ejen dihoskan](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kuota untuk **gpt-4.1** (atau **gpt-4.1-mini**) dalam projek Foundry anda.
- Alat berikut dipasang:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Sambungan Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Pilihan)
  - Python 3.10 atau versi lebih baru

Jalankan [mula cepat ejen dihoskan dengan `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) sekurang-kurangnya sekali sebelum penyampaian supaya anda mempunyai projek Foundry, penyebaran model, dan Azure Container Registry yang diketahui berfungsi jika pelajar mengalami masalah.

---

## Perjalanan slaid

Dek ini mengikuti aliran yang sama seperti makmal. Titik perbincangan yang disarankan untuk setiap bahagian:

| Bahagian                    | Mesej utama                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Tajuk dan agenda            | Bingkai bengkel sebagai *VS Code ke Foundry* tanpa perlu bertukar portal.                                  |
| Kenapa ejen dihoskan?       | Runtime diurus, penyebaran berasaskan ACR, API `/responses` yang serasi OpenAI, berfokus pada projek Foundry.        |
| Rajah seni bina             | Lalui [seni bina README](../README.md#architecture): kerangka, Inspector, ACR, Perkhidmatan Ejen.           |
| Anatomi ejen dihoskan       | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - fungsi setiap fail.                             |
| Demo langsung: Ejen Eksekutif | Tukar ke VS Code dan jalankan demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) dari awal hingga akhir (lihat [Demo 1](#demo-1-ejen-eksekutif)). |
| Demo langsung: Penilai Kesesuaian Kerja Resume | Tukar ke VS Code dan jalankan demo 4-ejen [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (lihat [Demo 2](#demo-2-penilai-kesesuaian-kerja-resume)). |
| Ringkasan Makmal 01         | Serahkan kepada pelajar. Arahkan ke [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Corak berbilang ejen        | Sejajar vs serentak vs penyerahan - pratonton sebelum Makmal 02 bermula.                                   |
| Ringkasan Makmal 02         | Serahkan kepada pelajar. Arahkan ke [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Penutup dan sumber          | Pautan pembelajaran lanjutan dari bahagian [Sumber tambahan](#sumber-tambahan).                        |

---

## Demo

Dua demo langsung disertakan dalam penyampaian. Sediakan masa 10 minit untuk setiap satu.

| Demo | Makmal | Fail | Apa yang hendak ditunjukkan |
|------|-----|-------|--------------|
| Ejen Eksekutif | Makmal 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Ejen dihoskan tunggal; terjemah jargon teknikal ke dalam ringkasan eksekutif |
| Penilai Kesesuaian Kerja Resume | Makmal 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orkestrasi 4-ejen; nilai kesesuaian resume-kerja dan hasilkan cadangan |

### Demo 1: Ejen Eksekutif

Ejen berdiri sendiri dalam [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Gunakan ini sebagai demo 10 minit sebelum Makmal 01.

1. Buka [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) dan lalui definisi ejen (prompt sistem, model, kerangka).
2. Tekan `F5` untuk melancarkan **Agent Inspector** secara lokal.
3. Tampal contoh prompt dari [README](../README.md#see-it-in-action) dan tunjukkan balasan ringkasan eksekutif.
4. Tunjukkan [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) dan [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) untuk terangkan artifak penyebaran.
5. Tunjukkan aliran penyebaran (pembinaan Docker, tolak ACR, cipta ejen dihoskan) tanpa menunggu selesai.

### Demo 2: Penilai Kesesuaian Kerja Resume

Aliran kerja 4-ejen dalam [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Gunakan ini sebagai demo 10 minit sebelum Makmal 02.

1. Buka [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) dan tunjukkan bagaimana keempat-empat ejen sambung secara berurutan.
2. Tekan `F5` untuk melancarkan **Agent Inspector** bagi aliran kerja berbilang ejen.
3. Tampal ringkasan kerja dan resume contoh dalam sembang Inspector.
4. Lalui saluran empat ejen: pengekstrak resume, pengekstrak keperluan kerja, penilai kesesuaian, dan penulis cadangan.
5. Terangkan bagaimana keluaran setiap sub-ejen menjadi konteks ejen seterusnya, menonjolkan corak penyerahan.
6. Tunjukkan [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) untuk bandingkan dengan yang setara ejen tunggal dari Demo 1.

---

## Petua penyampaian

- **Tetapkan jangkaan awal.** Ejen dihoskan masih dalam pratonton - nyatakan had rantau dan kuota pada awal supaya peserta tidak terkejut di tengah makmal.
- **Jalankan tugas prasyarat dahulu.** Kedua-dua makmal menyediakan tugas `Validate prerequisites` di VS Code - minta peserta jalankan sebelum mula menulis kod.
- **Pastikan Agent Inspector sentiasa kelihatan.** Kebanyakan momen "aha" berlaku apabila pelajar melihat cahaya putaran balik `/responses` secara lokal.
- **Sediakan projek sandaran.** Jika projek Foundry pelajar had kuota, kongsikan projek yang telah sedia ada untuk langkah penyebaran supaya tidak menghalang suasana bilik.
- **Paskan peserta berpasangan.** Makmal 02 (berbilang ejen) lebih mudah apabila pelajar boleh berbincang tentang orkestrasi bersama rakan.
- **Gunakan modul dokumen sebagai titik hentian.** Folder `docs/` setiap makmal dibahagikan kepada 8 modul bernombor - gunakan sebagai titik berhenti semula jadi.
- **Tarik imej Docker asas terlebih dahulu** pada mesin makmal kongsi untuk elak had kadar daftar masuk.

---

## Penyelesaian masalah semasa penyampaian

| Simptom                                      | Perkara pertama untuk cuba                                                                                |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector tidak dapat sambung          | Sahkan port `8088` bebas dan tugas `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` sedang berjalan.     |
| Debugger gagal untuk sambung                  | Periksa port `5679` bebas; mulakan semula VS Code jika `debugpy` sudah digunakan.                         |
| `azd up` gagal dengan kesilapan pengesahan   | Jalankan `az login` dan `azd auth login`, pastikan tenant yang betul dipilih.                            |
| Penyebaran tergantung pada tolak ACR          | Periksa Docker Desktop berjalan dan pengguna ada kebenaran `AcrPush` pada pendaftar.                      |
| Model pulang 404 / deployment-not-found       | Nama penyebaran model dalam `agent.yaml` mesti sepadan dengan penyebaran dalam projek Foundry.          |

| Ejen hos terperangkap dalam `Provisioning`         | Sahkan rantau projek [menyokong ejen hos](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) dan kuota tersedia. |
| Playground memulangkan 401                       | Sahkan semula peluasan Foundry dari bar aktiviti VS Code.                                     |

Untuk panduan lebih mendalam, setiap makmal dilengkapi dokumen `08-troubleshooting.md` sendiri - pautkan pelajar ke sana:

- Makmal 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Makmal 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Menyesuaikan sesi ini

Anda dialu-alukan untuk menyesuaikan bengkel untuk penonton anda. Variasi biasa:

- **Penonton backend:** luangkan lebih masa pada `agent.yaml`, Docker, dan ACR; pendekkan demo playground.
- **Penonton pembangun warganegara:** kekal di UI peluasan Foundry untuk scaffolding; kurangkan langkah CLI.
- **Slot trek tunggal 60 minit:** sampaikan pengenalan, demo, dan Makmal 01 sahaja.
- **Format hanya bengkel (tanpa slaid):** buka kedua-dua README makmal dan gunakan sebagai skrip utama.

Jika anda melanjutkan makmal, sila sumbangkan perubahan melalui PR supaya jurulatih lain mendapat manfaat.

---

## Sumber tambahan

- [Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Gambaran keseluruhan ejen hos](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Mula cepat: lancarkan ejen hos pertama anda (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Pasang ejen hos (cara-caranya)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Kerangka Ejen Microsoft](https://github.com/microsoft/agents)
- [Toolkit Microsoft Foundry untuk VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontak

Jika anda mempunyai soalan tentang penyampaian sesi ini, sila buka isu di [repositori bengkel](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) dan tandakan penyelenggara.

| Peranan             | Nama           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Penyelenggara / kontak| Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->