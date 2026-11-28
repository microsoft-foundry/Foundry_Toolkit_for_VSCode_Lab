# Modul 8 - Pemecahan Masalah

Modul ini membahas kesalahan umum, perbaikan, dan strategi debugging khusus untuk alur kerja multi-agent.

## Masalah output agen

### GapAnalyzer mengatakan "Saya masih belum memiliki laporan yang cocok"

**Gejala:** Respon GapAnalyzer meminta Anda untuk menempelkan laporan yang cocok dengan "Keterampilan yang Hilang" dan "Kesenjangan Sertifikasi." Ini terjadi meskipun Anda mengirimkan resume dan deskripsi pekerjaan.

**Penyebab:** Teks JD tidak diteruskan ke JD Agent. Dengan `context_mode="last_agent"`, `resume_executor` adalah eksekutor satu-satunya yang pernah melihat pesan asli pengguna. Jika `RESUME_PARSER_INSTRUCTIONS` tidak menyertakan teks JD dalam outputnya, JD Agent tidak memiliki JD untuk diurai, MatchingAgent tidak bisa menghitung skor kecocokan, dan GapAnalyzer menerima input yang tidak bermakna.

**Diagnosis:**

Dalam log server, cari span MatchingAgent. Jika mengandung:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
lalu jalur penerusan hilang atau rusak.

**Perbaikan:** Konfirmasi bahwa `RESUME_PARSER_INSTRUCTIONS` di `main.py` berisi bagian `[JOB DESCRIPTION PASS-THROUGH]` dan aturan:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Juga konfirmasi bahwa `JOB_DESCRIPTION_INSTRUCTIONS` mengandung aturan relay `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jika salah satu blok instruksi ini adalah stub dari penyihir scaffold, gantilah dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent mengeluarkan "Tidak dapat menghitung skor kecocokan - tidak ada JD yang diberikan"

Ini adalah penyebab utama yang sama seperti di atas. MatchingAgent menerima output JD Agent tetapi bagian `[PARSED RESUME PASS-THROUGH]` hilang atau kosong, sehingga tidak dapat membandingkan kedua profil. Konfirmasikan:
1. `JOB_DESCRIPTION_INSTRUCTIONS` menyertakan aturan relay: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` memberi tahu agen untuk mencari bagian `[JD REQUIREMENTS]` dan `[PARSED RESUME PASS-THROUGH]`.

Gantilah kedua blok instruksi dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Respons muncul dua kali

**Gejala:** Output GapAnalyzer (atau seluruh output pipeline) muncul dua kali dalam respons Agent Inspector.

**Penyebab:** `WorkflowBuilder` menggunakan semantik OR untuk edge masuk - eksekutor lanjutan aktif segera setelah **salah satu** pendahulu selesai. Jika `matching_executor` memiliki dua edge masuk (satu dari `resume_executor` dan satu dari `jd_executor`), ia aktif dua kali: sekali saat ResumeParser selesai dan sekali lagi saat JD Agent selesai. GapAnalyzer juga berjalan dua kali.

**Perbaikan:** Pastikan grafik `WorkflowBuilder` adalah pipeline berurutan secara ketat tanpa fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jika Anda memiliki baris `.add_edge(resume_executor, matching_executor)` yang tersesat, hapus. Relay `[PARSED RESUME PASS-THROUGH]` dalam output JD Agent sudah memberi MatchingAgent akses ke resume.

---

## Masalah lingkungan dan konfigurasi

### Nilai `.env` yang hilang atau salah

Berkas `.env` harus berada di direktori `PersonalCareerCopilot/` (tingkat yang sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Konten `.env` yang diharapkan:

**Jalur A - cloud Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Jalur B - Foundry Lokal:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Kedua jalur menggunakan `FOUNDRY_PROJECT_ENDPOINT`. Nilainya berbeda: cloud menggunakan endpoint `https://` Foundry; lokal menggunakan `http://localhost:5273/v1`. Jalankan `foundry model list` untuk mengonfirmasi alias model yang tepat untuk Jalur B.

> **Menemukan `FOUNDRY_PROJECT_ENDPOINT` Anda:** 
- Buka sidebar **Foundry Toolkit** di VS Code → klik kanan proyek Anda → **Copy Project Endpoint**. 
- Atau pergi ke [Azure Portal](https://portal.azure.com) → proyek Foundry Anda → **Overview** → **Project endpoint**.

> **Menemukan `AZURE_AI_MODEL_DEPLOYMENT_NAME` Anda:** Di sidebar Foundry Toolkit, kembangkan proyek Anda → **Models** → temukan nama model yang diterapkan (misal, `gpt-4.1-mini`).

### Prioritas variabel lingkungan

`main.py` menggunakan `load_dotenv(override=True)`, yang berarti:

| Prioritas | Sumber | Menang ketika keduanya disetel? |
|----------|--------|------------------------------|
| 1 (tertinggi) | berkas `.env` | Ya |
| 2 | Variabel lingkungan shell / container | Digunakan jika kunci yang sama tidak ada di `.env` |

Dalam pengembangan lokal, ini menjadikan `.env` sebagai sumber kebenaran (mengedit `.env` langsung mempengaruhi eksekusi). Dalam deployment yang dihosting, Foundry menyuntikkan variabel lingkungan di tingkat container; karena `.env` bukan bagian dari gambar yang diterapkan untuk pengaturan lab ini, nilai kontainer yang disuntikkan digunakan.

---

## Kompatibilitas versi

### Matriks versi paket

Alur kerja multi-agent membutuhkan versi paket tertentu. Versi yang tidak cocok menyebabkan kesalahan runtime.

| Paket | Versi yang Dibutuhkan | Perintah Cek |
|---------|--------------------|--------------|
| `agent-framework-foundry` | terbaru | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | terbaru | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | terbaru | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Kesalahan versi umum

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Fix: reinstall agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Fix: upgrade mcp package
pip install mcp --upgrade
```

### Verifikasi semua versi sekaligus

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Output yang diharapkan:

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
   - Buka sidebar **Foundry Toolkit** → di bawah proyek Anda, klik **Agents** → tab **Hosted Agent** → klik agen Anda. Periksa **Status** di tab **Details**, lalu buka tab **Playground** dan gunakan tab **Logs** di panel **Session Details** untuk melihat output container.
   - Cari jejak tumpukan Python atau kesalahan modul yang hilang.

2. **Kegagalan umum saat memulai container:**

   | Kesalahan di log | Penyebab | Perbaikan |
   |------------------|----------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` paket hilang | Tambahkan paket, deploy ulang |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | Variabel lingkungan `agent.yaml` atau `.env` tidak disetel | Perbarui bagian `agent.yaml` → `environment_variables` (hosted) atau `.env` (lokal) |
   | `azure.identity.CredentialUnavailableError` | Identitas Terkelola tidak dikonfigurasi | Foundry mengatur ini secara otomatis - pastikan Anda melakukan deployment melalui ekstensi |
   | `OSError: port 8088 already in use` | Dockerfile mengekspos port salah atau konflik port | Verifikasi `EXPOSE 8088` di Dockerfile dan `CMD ["python", "main.py"]` |
   | Container keluar dengan kode 1 | Exception yang tidak tertangani di `main()` | Uji secara lokal dulu ([Modul 5](05-test-locally.md)) untuk menangkap kesalahan sebelum deployment |

3. **Deploy ulang setelah memperbaiki:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pilih agen yang sama → deploy versi baru.

### Deployment memakan waktu terlalu lama

Container multi-agent membutuhkan waktu lebih lama untuk mulai karena mereka membuat 4 instance agen saat startup. Waktu startup normal:

| Tahap | Durasi yang Diharapkan |
|-------|------------------------|
| Build gambar container | 1-3 menit |
| Push gambar ke ACR | 30-60 detik |
| Mulai container (agen tunggal) | 15-30 detik |
| Mulai container (multi-agent) | 30-120 detik |
| Agen tersedia di Playground | 1-2 menit setelah "Started" |

> Jika status "Pending" bertahan lebih dari 5 menit, periksa log container untuk kesalahan.

---

## Masalah RBAC dan izin

### `403 Forbidden` atau `AuthorizationFailed`

Anda memerlukan peran **[Foundry User](https://aka.ms/foundry-ext-project-role)** pada proyek Foundry Anda (sebelumnya bernama **Azure AI User** - ID peran tidak berubah):

1. Pergi ke [Azure Portal](https://portal.azure.com) → sumber daya **proyek** Foundry Anda.
2. Klik **Access control (IAM)** → **Role assignments**.
3. Cari nama Anda → konfirmasi **Foundry User** (atau label lama **Azure AI User**) tercantum.
4. Jika tidak ada: **Tambah** → **Tambahkan penugasan peran** → cari **Foundry User** → tetapkan ke akun Anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk detail.

### Deployment model tidak dapat diakses

Jika agen mengembalikan kesalahan terkait model:

1. Verifikasi model sudah dideploy: sidebar Foundry → kembangkan proyek → **Models** → periksa ada `gpt-4.1-mini` (atau model Anda) dengan status **Succeeded**.
2. Verifikasi nama deployment cocok: bandingkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` di `.env` (atau `agent.yaml`) dengan nama deployment aktual di sidebar.
3. Jika deployment kedaluwarsa (tingkat gratis): deploy ulang dari [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Masalah Foundry Lokal (Jalur B)

### Layanan Foundry Lokal tidak berjalan

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Gejala | Penyebab | Perbaikan |
|---------|----------|----------|
| Health check menghasilkan `503` | Layanan tidak mulai | `foundry local start` atau klik **Start** di sidebar Foundry Toolkit |
| Health check kedaluwarsa | Model masih memuat | Tunggu 30–60 detik setelah memulai; model besar butuh waktu lebih lama |
| `StatusCode: 404` di `/v1/health` | Port salah | Default adalah `5273`. Periksa `foundry local status` untuk port sebenarnya |
| Sumber daya tidak cukup | Foundry Lokal butuh ~4 GB RAM bebas | Tutup aplikasi lain |
| Download model gagal | Ruang disk rendah | Model berukuran 2–8 GB. Bebaskan ruang, lalu `foundry model pull <name>` |

### Ketidaksesuaian nama model

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Setel `AZURE_AI_MODEL_DEPLOYMENT_NAME` di `.env` ke alias tepat yang ditampilkan (misal, `phi-4-mini`, bukan `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pada jalankan lokal (Jalur B)

Lab menggunakan `main.py` menggunakan `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Lokal membutuhkan variabel ini menunjuk ke layanan lokal - **bukan** `AZURE_AI_PROJECT_ENDPOINT`. Pastikan `.env` Anda berisi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Alat MCP masih membuat panggilan keluar (Jalur B)

Ini diharapkan. Alat `search_microsoft_learn_for_plan` mengambil sumber belajar dari `https://learn.microsoft.com/api/mcp`. **Hanya kueri nama keterampilan** yang melewati jaringan - resume dan teks JD diproses sepenuhnya di perangkat Anda dan tidak pernah dikirim. Jika operasi sepenuhnya offline diperlukan, tambahkan fallback `try/except` di alat yang mengembalikan URL statis `learn.microsoft.com` saat endpoint tidak dapat dijangkau.

---

## Mendapatkan bantuan

Jika Anda terjebak setelah mencoba perbaikan di atas:

1. **Periksa log server** - Sebagian besar kesalahan menghasilkan jejak tumpukan Python di terminal. Bacalah traceback lengkapnya.
2. **Cari pesan kesalahan** - Salin teks kesalahan dan cari di [Microsoft Q&A untuk Foundry Agent Service](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Buka isu** - Ajukan isu di [repository workshop](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) dengan:
   - Pesan kesalahan atau tangkapan layar
   - Versi paket Anda (`pip list | Select-String "agent-framework"`)
   - Versi Python Anda (`python --version`)
   - Apakah masalah lokal atau setelah deployment

---

### Titik pemeriksaan

- [ ] Anda tahu cara memeriksa dan memperbaiki masalah konfigurasi `.env`
- [ ] Anda dapat memverifikasi versi paket sesuai matriks yang dibutuhkan
- [ ] Anda tahu cara memeriksa log container untuk kegagalan deployment
- [ ] Anda dapat memverifikasi peran RBAC di Azure Portal

---

**Sebelumnya:** [07 - Verifikasi di Playground](07-verify-in-playground.md) · **Selanjutnya:** [09 - Ringkasan →](09-summary.md) · **Beranda:** [Lab 02 README](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->