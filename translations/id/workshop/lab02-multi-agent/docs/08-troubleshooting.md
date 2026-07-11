# Modul 8 - Pemecahan Masalah

Modul ini membahas kesalahan umum, perbaikan, dan strategi debug khusus untuk alur kerja multi-agen.

## Masalah keluaran Agen

### GapAnalyzer mengatakan “Saya masih belum memiliki laporan yang cocok”

**Gejala:** Respons GapAnalyzer meminta Anda untuk menempelkan laporan yang cocok dengan “Keterampilan yang Hilang” dan “Kesenjangan Sertifikasi.” Ini terjadi bahkan ketika Anda mengirimkan resume dan deskripsi pekerjaan.

**Penyebab:** Teks JD tidak diteruskan ke agen JD. Dengan `context_mode="last_agent"`, `resume_executor` adalah satu-satunya executor yang melihat pesan asli pengguna. Jika `RESUME_PARSER_INSTRUCTIONS` tidak menyertakan teks JD dalam outputnya, agen JD tidak memiliki JD untuk diparsing, MatchingAgent tidak dapat menghitung skor kecocokan, dan GapAnalyzer menerima input yang tidak bermakna.

**Diagnosis:**

Di log server, cari span MatchingAgent. Jika berisi:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
penyambungan lanjutan hilang atau rusak.

**Perbaikan:** Pastikan `RESUME_PARSER_INSTRUCTIONS` di `main.py` berisi bagian `[JOB DESCRIPTION PASS-THROUGH]` dan aturan:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Juga pastikan `JOB_DESCRIPTION_INSTRUCTIONS` berisi aturan relay `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jika salah satu blok instruksi adalah stub dari wizard scaffold, gantilah dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent mengeluarkan pesan “Tidak dapat menghitung skor kecocokan - tidak ada JD yang diberikan”

Ini adalah penyebab yang sama seperti di atas. MatchingAgent menerima output Agen JD tetapi bagian `[PARSED RESUME PASS-THROUGH]` hilang atau kosong, sehingga tidak dapat membandingkan kedua profil. Pastikan:
1. `JOB_DESCRIPTION_INSTRUCTIONS` mencakup aturan relay: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` memberitahu agen untuk mencari bagian `[JD REQUIREMENTS]` dan `[PARSED RESUME PASS-THROUGH]`.

Ganti kedua blok instruksi dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Respons muncul dua kali

**Gejala:** Keluaran GapAnalyzer (atau seluruh keluaran pipeline) muncul dua kali dalam respons Agent Inspector.

**Penyebab:** `WorkflowBuilder` menggunakan semantik OR untuk edge masuk - executor downstream dijalankan segera setelah **salah satu** pendahulu selesai. Jika `matching_executor` memiliki dua edge masuk (satu dari `resume_executor` dan satu dari `jd_executor`), ia dieksekusi dua kali: sekali saat ResumeParser selesai dan sekali lagi saat Agen JD selesai. GapAnalyzer kemudian juga berjalan dua kali.

**Perbaikan:** Pastikan grafik `WorkflowBuilder` adalah pipeline berurutan tanpa fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # BUKAN dari resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jika ada baris `.add_edge(resume_executor, matching_executor)` yang tidak perlu, hapus saja. Relay `[PARSED RESUME PASS-THROUGH]` pada output Agen JD sudah memberikan akses resume ke MatchingAgent.

---

## Masalah lingkungan dan konfigurasi

### Nilai `.env` hilang atau salah

File `.env` harus berada di direktori `PersonalCareerCopilot/` (tingkat yang sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Konten `.env` yang diharapkan:

**Jalur A - Foundry cloud:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Jalur B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Kedua jalur menggunakan `FOUNDRY_PROJECT_ENDPOINT`. Nilainya berbeda: cloud menggunakan endpoint Foundry `https://`; lokal menggunakan `http://localhost:5273/v1`. Jalankan `foundry model list` untuk memastikan alias model tepat untuk Jalur B.

> **Menemukan `FOUNDRY_PROJECT_ENDPOINT` Anda:**
- Buka sidebar **Foundry Toolkit** di VS Code → klik kanan proyek Anda → **Copy Project Endpoint**.
- Atau buka [Azure Portal](https://portal.azure.com) → proyek Foundry Anda → **Overview** → **Project endpoint**.

> **Menemukan `AZURE_AI_MODEL_DEPLOYMENT_NAME` Anda:** Di sidebar Foundry Toolkit, perluas proyek Anda → **Models** → cari nama model yang dideploy (misal, `gpt-4.1-mini`).

### Urutan prioritas variabel lingkungan

`main.py` menggunakan `load_dotenv(override=True)`, yang berarti:

| Prioritas | Sumber | Menang jika keduanya diatur? |
|----------|--------|---------------------------|
| 1 (tertinggi) | File `.env` | Ya |
| 2 | Variabel lingkungan shell / container | Digunakan jika kunci sama tidak ada di `.env` |

Dalam pengembangan lokal, ini menjadikan `.env` sebagai sumber kebenaran (mengedit `.env` langsung memengaruhi proses). Dalam deployment hosted, Foundry menyuntikkan variabel lingkungan di tingkat container; karena `.env` tidak termasuk dalam image terdeploy untuk setup lab ini, nilai container yang disuntikkan digunakan.

---

## Kompatibilitas versi

### Matriks versi paket

Alur kerja multi-agen membutuhkan versi paket tertentu. Versi yang tidak cocok menyebabkan error saat runtime.

| Paket | Versi Diperlukan | Perintah Cek |
|-------|-----------------|--------------|
| `agent-framework-foundry` | terbaru | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | terbaru | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | terbaru | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Kesalahan versi umum

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Perbaiki: pasang ulang agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Perbaiki: tingkatkan paket mcp
pip install mcp --upgrade
```

### Verifikasi semua versi sekaligus

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Keluaran yang diharapkan:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Masalah deployment

### Container gagal mulai setelah deployment

1. **Periksa log container:**
   - Buka sidebar **Foundry Toolkit** → perluas **Hosted Agents (Preview)** → klik agen Anda → perluas versinya → **Container Details** → **Logs**.
   - Cari stack trace Python atau kesalahan modul yang hilang.

2. **Kegagalan umum saat startup container:**

   | Kesalahan di log | Penyebab | Perbaikan |
   |------------------|----------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` kurang paket | Tambahkan paket, deploy ulang |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` atau variabel env `.env` tidak diatur | Perbarui `agent.yaml` → bagian `environment_variables` (hosted) atau `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Managed Identity tidak dikonfigurasi | Foundry mengatur ini secara otomatis - pastikan deploy lewat ekstensi |
   | `OSError: port 8088 already in use` | Dockerfile membuka port salah atau ada konflik port | Pastikan `EXPOSE 8088` di Dockerfile dan `CMD ["python", "main.py"]` |
   | Container keluar dengan kode 1 | Exception tidak tertangani di `main()` | Uji secara lokal dulu ([Modul 5](05-test-locally.md)) untuk menemukan kesalahan sebelum deploy |

3. **Deploy ulang setelah memperbaiki:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pilih agen yang sama → deploy versi baru.

### Deployment memakan waktu lama

Container multi-agen butuh waktu lebih lama untuk mulai karena membuat 4 instance agen saat startup. Perkiraan waktu normal startup:

| Tahap | Durasi yang Diharapkan |
|-------|----------------------|
| Build image container | 1-3 menit |
| Push image ke ACR | 30-60 detik |
| Startup container (agen tunggal) | 15-30 detik |
| Startup container (multi-agen) | 30-120 detik |
| Agen tersedia di Playground | 1-2 menit setelah "Started" |

> Jika status "Pending" terus lebih dari 5 menit, periksa log container untuk kesalahan.

---

## Masalah RBAC dan izin

### `403 Forbidden` atau `AuthorizationFailed`

Anda memerlukan peran **[Foundry User](https://aka.ms/foundry-ext-project-role)** pada proyek Foundry Anda (sebelumnya bernama **Azure AI User** - ID peran tidak berubah):

1. Buka [Azure Portal](https://portal.azure.com) → sumber daya proyek Foundry Anda.
2. Klik **Access control (IAM)** → **Role assignments**.
3. Cari nama Anda → pastikan tercantum **Foundry User** (atau label lama **Azure AI User**).
4. Jika belum ada: **Add** → **Add role assignment** → cari **Foundry User** → berikan ke akun Anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk detail.

### Model deployment tidak dapat diakses

Jika agen mengembalikan kesalahan terkait model:

1. Verifikasi model sudah dideploy: sidebar Foundry → perluas proyek → **Models** → cek apakah `gpt-4.1-mini` (atau model Anda) dengan status **Succeeded**.
2. Pastikan nama deployment cocok: bandingkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` di `.env` (atau `agent.yaml`) dengan nama deployment sebenarnya di sidebar.
3. Jika deployment sudah kadaluarsa (tingkat gratis): deploy ulang dari [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Masalah Foundry Local (Jalur B)

### Layanan Foundry Local tidak berjalan

```powershell
# Periksa status
foundry local status

# Mulai layanan jika sedang berhenti
foundry local start
```

| Gejala | Penyebab | Perbaikan |
|--------|----------|----------|
| Health check mengembalikan `503` | Layanan belum mulai | Jalankan `foundry local start` atau klik **Start** di sidebar Foundry Toolkit |
| Health check timeout | Model masih dimuat | Tunggu 30–60 detik setelah mulai; model besar butuh lebih lama |
| `StatusCode: 404` pada `/v1/health` | Port salah | Default `5273`. Cek dengan `foundry local status` port sebenarnya |
| Sumber daya tidak cukup | Foundry Local butuh ~4 GB RAM bebas | Tutup aplikasi lain |
| Gagal unduh model | Ruang disk rendah | Model berukuran 2–8 GB. Kosongkan ruang, lalu jalankan `foundry model pull <name>` |

### Nama model tidak cocok

```powershell
# Daftar model yang diunduh dan alias tepatnya
foundry model list
```

Set `AZURE_AI_MODEL_DEPLOYMENT_NAME` di `.env` ke alias persis seperti yang ditampilkan (misal, `phi-4-mini`, bukan `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` saat menjalankan lokal (Jalur B)

`main.py` lab ini menggunakan `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local membutuhkan variabel ini menunjuk ke layanan lokal - **bukan** `AZURE_AI_PROJECT_ENDPOINT`. Pastikan `.env` Anda berisi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Alat MCP masih membuat panggilan keluar (Jalur B)

Ini wajar. Alat `search_microsoft_learn_for_plan` mengambil sumber belajar dari `https://learn.microsoft.com/api/mcp`. **Hanya query nama keterampilan** yang melalui jaringan - teks resume dan JD diproses sepenuhnya di perangkat Anda dan tidak pernah dikirim. Jika operasi offline penuh diperlukan, tambahkan fallback `try/except` di alat yang mengembalikan URL statis `learn.microsoft.com` saat endpoint tidak dapat dijangkau.

---

## Mendapatkan bantuan

Jika Anda terjebak setelah mencoba perbaikan di atas:

1. **Periksa log server** - Sebagian besar kesalahan menghasilkan stack trace Python di terminal. Baca traceback lengkapnya.
2. **Cari pesan kesalahan** - Salin teks error dan cari di [Microsoft Q&A untuk Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Buka isu** - Buat isu di [repositori workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) dengan:
   - Pesan kesalahan atau screenshot
   - Versi paket Anda (`pip list | Select-String "agent-framework"`)
   - Versi Python Anda (`python --version`)
   - Apakah masalah terjadi lokal atau setelah deploy

---

### Titik pemeriksaan

- [ ] Anda tahu cara memeriksa dan memperbaiki masalah konfigurasi `.env`
- [ ] Anda dapat memverifikasi versi paket sesuai matriks yang diperlukan
- [ ] Anda tahu cara memeriksa log container untuk kegagalan deployment
- [ ] Anda dapat memverifikasi peran RBAC di Azure Portal

---

**Sebelumnya:** [07 - Verify in Playground](07-verify-in-playground.md) · **Selanjutnya:** [09 - Summary →](09-summary.md) · **Beranda:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->