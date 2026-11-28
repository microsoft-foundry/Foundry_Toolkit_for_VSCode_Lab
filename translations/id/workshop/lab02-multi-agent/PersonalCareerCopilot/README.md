# PersonalCareerCopilot - Evaluator Kesesuaian CV → Pekerjaan

Sebuah aplikasi multi-agen berbasis workflow yang mengevaluasi seberapa baik sebuah CV cocok dengan deskripsi pekerjaan, kemudian menghasilkan roadmap pembelajaran yang dipersonalisasi untuk menutup kesenjangan.

---

## Agen

| Agen | Peran | Alat |
|-------|------|-------|
| **ResumeParser** | Mengekstrak keterampilan, pengalaman, sertifikasi yang terstruktur dari teks CV | - |
| **JobDescriptionAgent** | Mengekstrak keterampilan, pengalaman, sertifikasi yang dibutuhkan/dipilih dari JD | - |
| **MatchingAgent** | Membandingkan profil vs persyaratan → skor kecocokan (0-100) + keterampilan yang cocok/hilang | - |
| **GapAnalyzer** | Membangun roadmap pembelajaran yang dipersonalisasi dengan sumber daya Microsoft Learn | `search_microsoft_learn_for_plan` (MCP) |

## Alur Kerja

```mermaid
flowchart LR
    UserInput["User Input: Resume + Job Description"] --> ResumeParser
    ResumeParser -- "parsed resume + JD relay" --> JobDescriptionAgent
    JobDescriptionAgent -- "JD requirements + resume relay" --> MatchingAgent
    MatchingAgent -- "fit report + gaps" --> GapAnalyzerMCP["Gap Analyzer +\nMicrosoft Learn MCP"]
    GapAnalyzerMCP --> FinalOutput["Final Output:\nFit Score + Roadmap"]
```

---

## Memulai dengan cepat

### 1. Siapkan lingkungan

Folder ini adalah implementasi referensi untuk kerangka Lab 02 berbasis workflow. `main.py` menggunakan blok prompt yang ada plus `WorkflowBuilder` untuk menghubungkan keempat agen.

```powershell
cd workshop\lab02-multi-agent\PersonalCareerCopilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate            # macOS / Linux
pip install -r requirements.txt
```

### 2. Konfigurasikan kredensial

Buat file `.env` di folder ini:

```powershell
copy .env .env.bak 2>$null; echo $null > .env
```

Edit `.env`:

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

| Nilai | Tempat menemukannya |
|-------|------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Sidebar Foundry Toolkit → klik kanan proyek Anda → **Salin Titik Akhir Proyek** |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Sidebar Foundry → perluas proyek → **Model + titik akhir** → nama deployment |

### 3. Jalankan secara lokal

```powershell
python -m debugpy --listen 127.0.0.1:5679 main.py --port 8088
```

Atau gunakan tugas VS Code: `Ctrl+Shift+P` → **Tugas: Jalankan Tugas** → **Jalankan Server HTTP Agen**.

Untuk debugging F5, gunakan **Debug Server HTTP Agen Lokal**.

### 4. Uji dengan Agent Inspector

Buka Agent Inspector: `Ctrl+Shift+P` → **Foundry Toolkit: Buka Agent Inspector**.

Tempel prompt uji ini:

```
Resume:
Jane Doe
Senior Software Engineer with 5 years of experience in Python, Django, and AWS.
Built microservices handling 10K+ requests/second. Led a team of 4 developers.
Certifications: AWS Solutions Architect Associate.
Education: B.S. Computer Science, State University.

Job Description:
Senior Cloud Engineer at Contoso Ltd.
Required: Python, Azure, Kubernetes, Terraform, CI/CD pipelines.
Preferred: Go, monitoring (Prometheus/Grafana), cost optimization.
Experience: 5+ years in cloud infrastructure.
Certifications: Azure Solutions Architect Expert preferred.
```

**Yang diharapkan:** Skor kesesuaian (0-100), keterampilan yang cocok/hilang, dan roadmap pembelajaran yang dipersonalisasi dengan URL Microsoft Learn.

### 5. Deploy ke Foundry

`Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pilih proyek Anda → konfirmasi.

---

## Struktur proyek

```
PersonalCareerCopilot/
├── .env                ← Your credentials (git-ignored)
├── agent.yaml          ← Hosted agent definition (name, resources, env vars)
├── Dockerfile          ← Container image for Foundry deployment
├── main.py             ← 4-agent workflow (instructions, MCP tool, WorkflowBuilder)
└── requirements.txt    ← Python dependencies
```

## Berkas kunci

### `agent.yaml`

Mendefinisikan agen hosted untuk Foundry Agent Service:
- `kind: hosted` - dijalankan sebagai kontainer terkelola
- `protocols` - protokol `responses` dengan `version: 2.0.0`, mengekspose endpoint HTTP `/responses`
- `environment_variables` - `AZURE_AI_MODEL_DEPLOYMENT_NAME` dideklarasikan di sini; `FOUNDRY_PROJECT_ENDPOINT` disuntikkan otomatis saat deploy

### `main.py`

Berisi:
- **Instruksi agen** - empat konstanta `*_INSTRUCTIONS`, satu per agen
- **Alat MCP** - `search_microsoft_learn_for_plan()` memanggil `https://learn.microsoft.com/api/mcp` via Streamable HTTP
- **Pembuatan agen** - empat instance `Agent()` + `AgentExecutor()` yang berbagi satu `FoundryChatClient`
- **Grafik workflow** - `WorkflowBuilder` menghubungkan agen sebagai pipeline berurutan: ResumeParser → Agen JD → MatchingAgent → GapAnalyzer
- **Startup server** - `ResponsesHostServer` berjalan di port 8088

### `requirements.txt`

| Paket | Tujuan |
|---------|----------|
| `agent-framework-foundry` | Runtime inti: `Agent`, `AgentExecutor`, `WorkflowBuilder`, `@tool`, `FoundryChatClient` |
| `agent-framework-foundry-hosting` | Integrasi hosting Foundry + `ResponsesHostServer` |
| `mcp<2,>=1.24.0` | Klien MCP untuk GapAnalyzer (`streamable_http_client`) |
| `debugpy` | Debugging Python (F5 di VS Code) |

---

## Pemecahan Masalah

| Masalah | Solusi |
|-------|-----|
| `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` atau `KeyError: 'AZURE_AI_MODEL_DEPLOYMENT_NAME'` | Buat `.env` dengan kedua `FOUNDRY_PROJECT_ENDPOINT` dan `AZURE_AI_MODEL_DEPLOYMENT_NAME` disetel |
| `ModuleNotFoundError: No module named 'agent_framework'` | Aktifkan venv dan jalankan `pip install -r requirements.txt` |
| Tidak ada URL Microsoft Learn di output | Periksa koneksi internet ke `https://learn.microsoft.com/api/mcp` |
| Hanya 1 kartu gap (terpotong) | Pastikan `GAP_ANALYZER_INSTRUCTIONS` menyertakan blok `CRITICAL:` |
| Port 8088 sedang digunakan | Matikan server lain: `netstat -ano \| findstr :8088` |

Untuk pemecahan masalah mendetail, lihat [Modul 8 - Pemecahan Masalah](../docs/08-troubleshooting.md).

---

**Panduan lengkap:** [Dokumen Lab 02](../docs/README.md) · **Kembali ke:** [README Lab 02](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->