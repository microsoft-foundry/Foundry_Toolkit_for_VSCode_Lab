# Workshop Foundry Toolkit + Agen Hosted Foundry

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/agent-framework/)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Bangun, uji, dan deploy agen AI ke **Microsoft Foundry Agent Service** sebagai **Hosted Agents** - sepenuhnya dari VS Code menggunakan **ekstensi Microsoft Foundry** dan **Foundry Toolkit**.

> **Hosted Agents saat ini dalam pratinjau.** Wilayah yang didukung terbatas - lihat [ketersediaan wilayah](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Folder `agent/` di dalam setiap lab **secara otomatis dibuat** oleh ekstensi Foundry - Anda kemudian menyesuaikan kode, menguji secara lokal, dan melakukan deploy.

### 🌐 Dukungan Multi-Bahasa

#### Didukung melalui GitHub Action (Otomatis & Selalu Terbaru)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](./README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Lebih suka clone secara lokal?**
>
> Repositori ini mencakup lebih dari 50 terjemahan bahasa yang secara signifikan meningkatkan ukuran unduhan. Untuk clone tanpa terjemahan, gunakan sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Ini memberikan Anda semua yang dibutuhkan untuk menyelesaikan kursus dengan unduhan yang jauh lebih cepat.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Arsitektur

```mermaid
flowchart TB
    subgraph Local["Local Development (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "F5 Debug" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "Test prompts" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Alur:** Ekstensi Foundry membuat kerangka agen → Anda menyesuaikan kode & instruksi → uji secara lokal dengan Agent Inspector → deploy ke Foundry (gambar Docker didorong ke ACR) → verifikasi di Playground.

---

## Apa yang akan Anda bangun

| Lab | Deskripsi | Status |
|-----|-------------|--------|
| **Lab 01 - Agen Tunggal** | Bangun **"Jelaskan Seperti Saya Eksekutif" Agent**, uji secara lokal, dan deploy ke Foundry | ✅ Tersedia |
| **Lab 02 - Alur Kerja Multi-Agen** | Bangun **"Resume → Evaluator Kecocokan Pekerjaan"** - 4 agen berkolaborasi untuk menilai kecocokan resume dan membuat peta belajar | ✅ Tersedia |

---

## Kenali Agen Eksekutif

Di workshop ini Anda akan membangun **"Jelaskan Seperti Saya Eksekutif" Agent** - agen AI yang mengubah jargon teknis rumit menjadi ringkasan yang santai dan siap untuk rapat dewan. Jujur saja, tidak ada yang di jajaran eksekutif mau mendengar tentang "kehabisan thread pool yang disebabkan oleh panggilan sinkron yang diperkenalkan di v3.2."

Saya membangun agen ini setelah beberapa insiden di mana post-mortem saya yang sempurna mendapat respons: *"Jadi... apakah situs webnya down atau tidak?"*

### Cara kerjanya

Anda memberikan pembaruan teknis. Ia mengeluarkan ringkasan eksekutif - tiga poin peluru, tanpa jargon, tanpa jejak stack, tanpa ketakutan eksistensial. Hanya **apa yang terjadi**, **dampak bisnis**, dan **langkah selanjutnya**.

### Lihat dalam aksi

**Anda mengatakan:**
> "Latency API meningkat karena kehabisan thread pool yang disebabkan oleh panggilan sinkron yang diperkenalkan di v3.2."

**Agen menjawab:**

> **Ringkasan Eksekutif:**
> - **Apa yang terjadi:** Setelah rilis terbaru, sistem melambat.
> - **Dampak bisnis:** Beberapa pengguna mengalami keterlambatan saat menggunakan layanan.
> - **Langkah selanjutnya:** Perubahan telah dibatalkan dan perbaikan sedang dipersiapkan sebelum dilakukan deploy ulang.

### Mengapa agen ini?

Ini adalah agen yang sangat sederhana dan dengan tujuan tunggal - cocok untuk mempelajari alur kerja agen hosted dari awal hingga akhir tanpa terjebak dalam rantai alat yang kompleks. Dan jujur? Setiap tim teknik bisa menggunakan salah satu dari ini.

---

## Struktur workshop

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   ├── 08-troubleshooting.md
        │   └── 09-summary.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Catatan:** Folder `agent/` di dalam setiap lab adalah yang dihasilkan oleh **ekstensi Microsoft Foundry** saat Anda menjalankan `Microsoft Foundry: Create a New Hosted Agent` dari Command Palette. File-file tersebut kemudian disesuaikan dengan instruksi, alat, dan konfigurasi agen Anda. Lab 01 memandu Anda membuat ini dari awal.

---

## Memulai

### 1. Clone repositori

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Siapkan virtual environment Python

```bash
python -m venv venv
```

Aktifkan:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instal dependensi

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Konfigurasi variabel lingkungan

Salin file contoh `.env` di dalam folder agen dan isi dengan nilai Anda:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

Edit `workshop/lab01-single-agent/agent/.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Ikuti lab workshop

Setiap lab berdiri sendiri dengan modulnya masing-masing. Mulailah dengan **Lab 01** untuk mempelajari dasar-dasar, kemudian lanjutkan ke **Lab 02** untuk alur kerja multi-agen.

#### Lab 01 - Agen Tunggal ([instruksi lengkap](workshop/lab01-single-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Baca prasyarat | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Instal Foundry Toolkit & ekstensi Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Buat proyek Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Buat agen hosted | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Konfigurasikan instruksi & lingkungan | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Uji secara lokal | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Deploy ke Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Verifikasi di playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Ringkasan & langkah selanjutnya | [07-summary.md](workshop/lab01-single-agent/docs/07-summary.md) |
| 10 | Pemecahan masalah | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Lab 02 - Alur Kerja Multi-Agen ([instruksi lengkap](workshop/lab02-multi-agent/README.md))

| # | Modul | Link |
|---|--------|------|
| 1 | Prasyarat (Lab 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Pahami arsitektur multi-agen | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Buat kerangka proyek multi-agen | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Konfigurasikan agen & lingkungan | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Pola orkestrasi | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Uji secara lokal (multi-agen) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Deploy ke Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Verifikasi di playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Pemecahan masalah (multi-agen) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |
| 10 | Ringkasan & langkah selanjutnya | [09-summary.md](workshop/lab02-multi-agent/docs/09-summary.md) |

---

## Pemelihara

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Izin yang diperlukan (referensi cepat)

| Skenario | Peran yang diperlukan |
|----------|---------------|
| Buat proyek Foundry baru | **Azure AI Owner** pada sumber daya Foundry |
| Deploy ke proyek yang sudah ada (sumber daya baru) | **Azure AI Owner** + **Contributor** pada langganan |
| Deploy ke proyek dengan konfigurasi lengkap | **Reader** pada akun + **Azure AI User** pada proyek |

> **Penting:** Peran Azure `Owner` dan `Contributor` hanya mencakup izin *manajemen*, bukan izin *pengembangan* (aksi data). Anda memerlukan **Azure AI User** atau **Azure AI Owner** untuk membangun dan menerapkan agen.

---

## Referensi

- [Memulai dengan cepat: Terapkan agen host pertama Anda (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Apa itu agen host?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Buat alur kerja agen host di VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Terapkan agen host](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Contoh Agen Tinjauan Arsitektur](https://github.com/Azure-Samples/agent-architecture-review-sample) - Agen host dunia nyata dengan alat MCP, diagram Excalidraw, dan penerapan ganda

---


## Lisensi

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->