# Modul 2 - Menyusun Projek Multi-Ejen

⏱️ ~5 minit

Dalam modul ini, anda menggunakan [Foundry Toolkit for VS Code](https://aka.ms/foundrytk) untuk **menyusun projek multi-ejen**. Penyihir menjana `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`, dan konfigurasi debug VS Code - supaya anda boleh fokus memasangkan aliran kerja 4-ejen dalam Modul 3.

> **Konsep utama:** Scaffold adalah stub yang berfungsi dengan satu ejen. Anda menggantikan logik ruang letak dengan graf `WorkflowBuilder` dalam Modul 3. Anda tidak menulis boilerplate dari awal.

> **Pelaksanaan rujukan:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot) adalah contoh lengkap yang berfungsi. Gunakannya untuk membandingkan kerja anda semasa anda berjalan.

### Aliran penyihir scaffold

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## Langkah 1: Buka penyihir Create Hosted Agent

1. Tekan `Ctrl+Shift+P` untuk membuka **Command Palette**.
2. Taip: **Foundry Toolkit: Create new Hosted Agent** dan pilih.
3. Penyihir dibuka pada tab **Agent Details**.

> **Alternatif:** Klik ikon **Foundry Toolkit** di Bar Aktiviti → klik ikon **+** di sebelah **Hosted Agents** → **Create New Hosted Agent**.

---

## Langkah 2: Pilih tetapan

![Create Hosted Agent from Sample - Agent Details tab with Workflows template selected](../../../../../translated_images/ms/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. Pada bahagian navigasi/pilihan kiri pilih yang berikut:

| Menu | Pilihan | Nota |
|--------|-----------|-------|
| **Bahasa** | Python | C# (.NET) juga disokong |
| **Rangka Kerja** | Agent Framework | Menyediakan `Agent`, `AgentExecutor`, `WorkflowBuilder` |
| **Jenis API** | Response API | `POST /responses` - sejarah yang dikendalikan platform, sokongan streaming |
| **Templat** | **Workflows** | Memproses permintaan melalui pelbagai ejen secara berturutan |

2. Setelah dipilih, klik **Next**

![Create Hosted Agent from Sample - Create tab showing PersonalCareerCopilot as the folder name](../../../../../translated_images/ms/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. Dalam tetingkap seterusnya, pilih yang berikut:

| Menu | Pilihan | Nota |
|--------|-----------|-------|
| **Folder kerja** | Layari ke folder sasaran | contohnya, `workshop/lab02-multi-agent/` dalam repo ini |
| **Nama ejen** | `PersonalCareerCopilot` | Ini menjadi nama direktori projek |
| **Pengeluaran Model** | Pilih model yang telah dipasang | contohnya, `gpt-4.1-mini` dari Lab 01 |

4. Klik **Create** untuk menyusun projek. VS Code menjana fail dan membuka folder.

> **Petua:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series) mengimbangi kelajuan dan kualiti dengan baik untuk pembangunan multi-ejen.

---

## Langkah 3: Periksa projek yang dijana

Selepas scaffolding selesai, pastikan anda melihat fail ini dalam Explorer (`Ctrl+Shift+E`):

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **Penting:** Buka folder scaffolded ini terus dalam VS Code supaya `.vscode/launch.json` dan `tasks.json` berfungsi dengan betul untuk debug F5.

### Fail utama dijelaskan

| Fail | Tujuan |
|------|---------|
| `agent.yaml` | Mengisytiharkan `kind: hosted`, memetakan pembolehubah persekitaran, mentakrifkan protokol `/responses` |
| `main.py` | Stub: satu `FoundryChatClient` → `Agent` → `ResponsesHostServer`. Anda gantikan ini dengan 4 ejen + `WorkflowBuilder` dalam Modul 3 |
| `Dockerfile` | `python:3.12-slim`, memasang `requirements.txt`, mendedahkan port 8088, menjalankan `python main.py` |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **Rujukan:** Lihat [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) dan [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) untuk kandungan lengkap yang dijana.

---

### ✅ Titik semakan

- [ ] Penyihir scaffold selesai - folder projek baru kelihatan dalam Explorer
- [ ] Semua fail dijangka hadir: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml` menunjukkan `kind: hosted` dan `protocol: responses`
- [ ] `main.py` mengimport `Agent`, `FoundryChatClient`, `ResponsesHostServer`
- [ ] Folder scaffolded dibuka sebagai akar ruang kerja VS Code
- [ ] Anda faham `main.py` adalah stub - `WorkflowBuilder` ditambah dalam Modul 3

---

**Sebelum ini:** [01 - Memahami Seni Bina Multi-Ejen](01-understand-multi-agent.md) · **Seterusnya:** [03 - Konfigurasikan Ejen & Persekitaran →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->