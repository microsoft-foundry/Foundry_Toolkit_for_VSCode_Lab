# Cara menyampaikan sesi ini

Terima kasih telah menyampaikan sesi ini!

Sebelum menyampaikan workshop, harap:

1. Baca dokumen ini dan semua sumber daya yang disertakan secara keseluruhan.
2. Tonton rekaman penyampaian sesi dan walkthrough workshop dari awal hingga akhir.
3. Lakukan kedua lab praktikum secara menyeluruh di mesin Anda sendiri **setidaknya sekali** sebelum acara.
4. Validasi proyek Microsoft Foundry Anda, penyebaran model, dan kuota.
5. Hubungi pemelihara jika ada yang tidak jelas.

---

## Ringkasan file

| Sumber Daya                 | Tautan                                                                           | Deskripsi                                                                                     |
|-----------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Dek slide Workshop          | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                   | Slide presentasi untuk workshop ini dengan catatan presenter dan video demo tersemat           |
| Rekaman penyampaian sesi    | _Akan disediakan oleh pemelihara_                                              | Rekaman pengantar workshop dan walkthrough slide                                              |
| Rekaman workshop end-to-end | _Akan disediakan oleh pemelihara_                                              | Rekaman menyeluruh kedua lab dari perspektif peserta                                         |
| Dokumentasi workshop        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Repositori sumber, README lab, modul langkah demi langkah                                    |
| Lab 01 - agen tunggal       | [Lab 01](../workshop/lab01-single-agent/README.md)                             | Lab praktikum: membangun, menguji, dan menyebarkan agen *Explain Like I'm an Executive* yang dihosting |
| Lab 02 - alur kerja multi-agen | [Lab 02](../workshop/lab02-multi-agent/README.md)                              | Lab praktikum: membangun alur kerja 4 agen *Resume to Job Fit Evaluator*                      |
| Demo 1: Agen Eksekutif       | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                           | Demo Lab 01: menerjemahkan jargon teknis ke dalam ringkasan eksekutif                        |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Demo Lab 02: alur kerja 4 agen yang menilai kecocokan resume-pekerjaan dan menghasilkan rekomendasi |

> **Catatan untuk pelatih:** Dek slide dan tautan video akan ditambahkan setelah rekaman diterbitkan. Sampai saat itu, hubungi pemelihara (lihat [Kontak](#kontak)) untuk aset terbaru.

---

## Mulai

Workshop ini mengajarkan pengembang cara membangun, menguji, dan menyebarkan agen AI ke **Microsoft Foundry Agent Service** sebagai **Hosted Agents** sepenuhnya dari VS Code, menggunakan ekstensi **Microsoft Foundry Toolkit**.

Workshop ini dibagi menjadi beberapa bagian termasuk slide, **2 demo langsung**, dan **2 lab praktikum**.

### Waktu

#### Penyampaian lengkap (sekitar 2 jam)

| Waktu           | Deskripsi                                                           |
|-----------------|---------------------------------------------------------------------|
| 0:00 - 10:00    | Pembukaan: hosted agents, Foundry Agent Service, dan toolkit        |
| 10:00 - 20:00   | Demo: Executive Agent dari awal hingga akhir                        |
| 20:00 - 60:00   | Lab 01 - agen tunggal (bangun, uji lokal, sebar, playground)        |
| 60:00 - 110:00  | Lab 02 - alur kerja multi-agen (Resume to Job Fit Evaluator)        |
| 110:00 - 120:00 | Penutupan, sesi tanya jawab, dan sumber belajar lanjutan            |

#### Penyampaian singkat (sekitar 75 menit)

| Waktu          | Deskripsi                                                     |
|---------------|---------------------------------------------------------------|
| 0:00 - 10:00  | Pembukaan dan overview                                        |
| 10:00 - 20:00 | Demo: Executive Agent                                       |
| 20:00 - 70:00 | Hanya Lab 01 (arahkan peserta ke Lab 02 sebagai belajar mandiri) |
| 70:00 - 75:00 | Penutupan dan sesi tanya jawab                               |

### Persiapan

| Sumber Daya                  | Tautan                                                                                   | Deskripsi                                      |
|------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------|
| Dokumentasi workshop         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)        | Dokumentasi dan sumber workshop                |
| Instruksi Lab 01             | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                           | Lab praktikum: agen hosted tunggal             |
| Instruksi Lab 02             | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                             | Lab praktikum: alur kerja multi-agen           |
| Daftar periksa prasyarat     | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)           | Alat, akun, dan akses Azure yang diperlukan    |
| Quickstart hosted agents (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | Quickstart resmi untuk menyebarkan hosted agent dengan `azd` |
| Ketersediaan region hosted agents | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Region yang didukung untuk hosted agents (pratinjau) |

### Prasyarat pelatih

Sebelum menyampaikan, pastikan Anda memiliki:

- **Langganan Azure** dengan izin membuat sumber daya (Owner atau Contributor pada grup sumber daya).
- Akses ke **proyek Microsoft Foundry** di [region yang mendukung hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).
- Kuota untuk **gpt-4.1** (atau **gpt-4.1-mini**) dalam proyek Foundry Anda.
- Alat berikut terpasang:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Ekstensi Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (Opsional)
  - Python 3.10 atau lebih baru

Jalankan [Hosted agents quickstart dengan `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) setidaknya sekali sebelum penyampaian supaya Anda memiliki proyek Foundry, penyebaran model, dan Azure Container Registry yang sudah teruji untuk referensi jika peserta mengalami kesulitan.

---

## Walkthrough slide

Dek mengikuti alur yang sama dengan lab. Titik bicara yang disarankan untuk setiap bagian:

| Bagian                      | Pesan utama                                                                                                  |
|----------------------------|--------------------------------------------------------------------------------------------------------------|
| Judul dan agenda            | Bingkai workshop sebagai *VS Code ke Foundry* tanpa perlu berganti portal.                                   |
| Kenapa hosted agents?       | Runtime terkelola, penyebaran berbasis ACR, API `/responses` kompatibel OpenAI, terikat ke proyek Foundry.     |
| Diagram arsitektur          | Jelaskan [arsitektur di README](../README.md#architecture): kerangka, Inspector, ACR, Agent Service.          |
| Anatomi hosted agent        | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - fungsi masing-masing file.                        |
| Demo langsung: Executive Agent  | Beralih ke VS Code dan jalankan demo [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) dari awal hingga akhir (lihat [Demo 1](#demo-1-executive-agent)). |
| Demo langsung: Resume to Job Fit Evaluator | Beralih ke VS Code dan jalankan demo 4-agen [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (lihat [Demo 2](#demo-2-resume-to-job-fit-evaluator)). |
| Ringkasan Lab 01            | Berikan kepada peserta. Arahkan ke [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md). |
| Pola multi-agen             | Berurutan vs konkuren vs handoff - preview sebelum Lab 02 dimulai.                                           |
| Ringkasan Lab 02            | Berikan kepada peserta. Arahkan ke [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md). |
| Penutupan dan sumber daya   | Tautan belajar lanjutan dari bagian [Sumber tambahan](#sumber-daya-tambahan).                               |

---

## Demo

Dua demo langsung disertakan dalam penyampaian. Alokasikan 10 menit untuk masing-masing.

| Demo                   | Lab   | File                                                       | Apa yang ditampilkan                              |
|------------------------|-------|------------------------------------------------------------|--------------------------------------------------|
| Executive Agent         | Lab 01| [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Agen tunggal yang dihosting; terjemahkan jargon teknis ke ringkasan eksekutif |
| Resume to Job Fit Evaluator | Lab 02| [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | Orkestrasi 4 agen; nilai kecocokan resume-pekerjaan dan buat rekomendasi   |

### Demo 1: Executive Agent

Agen mandiri di [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent). Gunakan ini sebagai demo 10 menit sebelum Lab 01.

1. Buka [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) dan jelaskan definisi agen (prompt sistem, model, kerangka kerja).
2. Tekan `F5` untuk meluncurkan **Agent Inspector** secara lokal.
3. Tempel prompt contoh dari [README](../README.md#see-it-in-action) dan tunjukkan respon ringkasan eksekutif.
4. Tunjukkan [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) dan [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) untuk menjelaskan artefak penyebaran.
5. Demonstrasikan alur penyebaran (Docker build, ACR push, hosted agent create) tanpa menunggu selesai.

### Demo 2: Resume to Job Fit Evaluator

Alur kerja 4 agen di [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot). Gunakan ini sebagai demo 10 menit sebelum Lab 02.

1. Buka [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) dan tunjukkan bagaimana keempat agen dirangkai dalam orkestrasi berurutan.
2. Tekan `F5` untuk meluncurkan **Agent Inspector** untuk alur kerja multi-agen.
3. Tempelkan deskripsi pekerjaan singkat dan contoh resume di chat Inspector.
4. Jelaskan pipeline empat agen: parser resume, ekstraktor persyaratan pekerjaan, penilai kecocokan, dan penulis rekomendasi.
5. Tunjukkan bagaimana output setiap sub-agen menjadi konteks agen berikutnya, menyoroti pola handoff.
6. Tunjukkan [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) untuk dibandingkan dengan agen tunggal di Demo 1.

---

## Tips penyampaian

- **Tetapkan ekspektasi sejak awal.** Hosted agents masih pratinjau - sebutkan batasan region dan kuota di awal agar peserta tidak kaget saat lab berlangsung.
- **Jalankan tugas prasyarat terlebih dahulu.** Kedua lab menyediakan tugas `Validate prerequisites` di VS Code - minta peserta menjalankannya sebelum menulis kode apa pun.
- **Jaga agar Agent Inspector tetap terlihat.** Kebanyakan momen "aha" terjadi saat peserta melihat lampu bolak-balik `/responses` pada lokal menyala.
- **Siapkan proyek cadangan.** Jika proyek Foundry peserta menemui batas kuota, bagikan proyek yang sudah disiapkan untuk tahap penyebaran supaya tidak menghambat ruangan.
- **Pasangkan peserta.** Lab 02 (multi-agen) jauh lebih mudah jika peserta bisa diskusi orkestrasi dengan pasangan.
- **Gunakan modul dokumen sebagai titik cek.** Folder `docs/` tiap lab dibagi menjadi 8 modul bernomor - gunakan itu sebagai titik berhenti alami.
- **Tarik dulu base Docker image** di mesin lab bersama untuk menghindari batasan registri.

---

## Pemecahan masalah saat penyampaian

| Gejala                                    | Hal pertama yang dicoba                                                                      |
|------------------------------------------|---------------------------------------------------------------------------------------------|
| Agent Inspector tidak bisa terkoneksi     | Pastikan port `8088` bebas dan tugas `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` berjalan. |
| Debugger gagal melampirkan                 | Periksa port `5679` bebas; restart VS Code jika `debugpy` sudah terikat.                     |
| `azd up` gagal dengan error otentikasi    | Jalankan `az login` dan `azd auth login`, pastikan tenant yang dipilih benar.               |
| Penyebaran berhenti di ACR push            | Periksa Docker Desktop berjalan dan pengguna memiliki `AcrPush` di registry.                |
| Model mengembalikan 404 / deployment-not-found | Nama penyebaran model di `agent.yaml` harus sama dengan penyebaran di proyek Foundry.        |

| Agen hosted tersangkut di `Provisioning`         | Verifikasi wilayah proyek [mendukung agen hosted](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) dan bahwa kuota tersedia. |
| Playground mengembalikan 401                       | Autentikasi ulang ekstensi Foundry dari bilah aktivitas VS Code.                                     |

Untuk panduan mendalam, setiap lab menyediakan dokumen `08-troubleshooting.md` sendiri - arahkan pelajar ke sana:

- Lab 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Lab 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Menyesuaikan sesi ini

Anda dipersilakan untuk menyesuaikan workshop bagi audiens Anda. Variasi umum:

- **Audiens backend:** habiskan lebih banyak waktu pada `agent.yaml`, Docker, dan ACR; potong demo playground.
- **Audiens developer warga:** tetap di antarmuka ekstensi Foundry untuk scaffolding; kurangi langkah CLI.
- **Slot 60 menit satu track:** berikan intro, demo, dan hanya Lab 01.
- **Format hanya workshop (tanpa slide):** buka kedua README lab dan gunakan sebagai skrip utama.

Jika Anda memperluas lab, harap kontribusikan perubahan kembali melalui PR agar pelatih lain mendapat manfaat.

---

## Sumber daya tambahan

- [Dokumentasi Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [Ikhtisar agen hosted](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Panduan cepat: deploy agen hosted pertama Anda (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Deploy agen hosted (cara-cara)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit untuk VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## Kontak

Jika Anda memiliki pertanyaan tentang penyampaian sesi ini, silakan buka isu di [repositori workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) dan tag pemelihara.

| Peran                | Nama           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| Pemelihara / kontak  | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->