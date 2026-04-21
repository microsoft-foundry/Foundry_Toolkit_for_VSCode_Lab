# Modul 8 - Pemecahan Masalah (Multi-Agen)

Modul ini membahas kesalahan umum, perbaikan, dan strategi debugging yang spesifik untuk alur kerja multi-agen. Untuk masalah umum penerapan Foundry, juga lihat [panduan pemecahan masalah Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Referensi cepat: Kesalahan → Perbaikan

| Kesalahan / Gejala | Penyebab Kemungkinan | Perbaikan |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | File `.env` hilang atau nilai belum diatur | Buat `.env` dengan `PROJECT_ENDPOINT=<your-endpoint>` dan `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Lingkungan virtual tidak diaktifkan atau dependensi belum diinstal | Jalankan `.\.venv\Scripts\Activate.ps1` kemudian `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Paket MCP tidak diinstal (hilang dari requirements) | Jalankan `pip install mcp` atau cek `requirements.txt` sudah termasuk sebagai dependensi transitif |
| Agen mulai tapi mengembalikan respons kosong | Ketidakcocokan `output_executors` atau edges hilang | Verifikasi `output_executors=[gap_analyzer]` dan semua edges ada di `create_workflow()` |
| Hanya 1 kartu gap (sisanya hilang) | Instruksi GapAnalyzer tidak lengkap | Tambahkan paragraf `CRITICAL:` ke `GAP_ANALYZER_INSTRUCTIONS` - lihat [Modul 3](03-configure-agents.md) |
| Skor kecocokan 0 atau tidak ada | MatchingAgent tidak menerima data dari hulu | Pastikan ada `add_edge(resume_parser, matching_agent)` dan `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Server MCP menolak panggilan alat | Periksa koneksi internet. Coba buka `https://learn.microsoft.com/api/mcp` di browser. Coba lagi |
| Tidak ada URL Microsoft Learn di output | Alat MCP tidak terdaftar atau endpoint salah | Pastikan `tools=[search_microsoft_learn_for_plan]` pada GapAnalyzer dan `MICROSOFT_LEARN_MCP_ENDPOINT` benar |
| `Address already in use: port 8088` | Proses lain menggunakan port 8088 | Jalankan `netstat -ano \| findstr :8088` (Windows) atau `lsof -i :8088` (macOS/Linux) dan hentikan proses yang konflik |
| `Address already in use: port 5679` | Konflik port Debugpy | Hentikan sesi debug lain. Jalankan `netstat -ano \| findstr :5679` untuk menemukan dan hentikan proses tersebut |
| Agent Inspector tidak terbuka | Server belum sepenuhnya berjalan atau konflik port | Tunggu log "Server running". Periksa port 5679 bebas |
| `azure.identity.CredentialUnavailableError` | Belum masuk ke Azure CLI | Jalankan `az login` lalu mulai ulang server |
| `azure.core.exceptions.ResourceNotFoundError` | Deployment model tidak ada | Pastikan `MODEL_DEPLOYMENT_NAME` cocok dengan model yang sudah dipasang di proyek Foundry Anda |
| Status kontainer "Failed" setelah deployment | Kontainer crash saat mulai | Periksa log kontainer di sidebar Foundry. Umum: variabel env hilang atau error impor |
| Deployment menunjukkan "Pending" selama > 5 menit | Kontainer terlalu lama mulai atau batas sumber daya | Tunggu hingga 5 menit untuk multi-agen (membuat 4 instance agen). Jika masih pending, cek log |
| `ValueError` dari `WorkflowBuilder` | Konfigurasi grafik tidak valid | Pastikan `start_executor` diset, `output_executors` berupa list, dan tidak ada edges melingkar |

---

## Masalah lingkungan dan konfigurasi

### Nilai `.env` hilang atau salah

File `.env` harus ada di direktori `PersonalCareerCopilot/` (tingkat yang sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Isi `.env` yang diharapkan:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Menemukan PROJECT_ENDPOINT Anda:**  
- Buka sidebar **Microsoft Foundry** di VS Code → klik kanan proyek Anda → **Copy Project Endpoint**.  
- Atau buka [Azure Portal](https://portal.azure.com) → proyek Foundry Anda → **Overview** → **Project endpoint**.

> **Menemukan MODEL_DEPLOYMENT_NAME Anda:** Di sidebar Foundry, perluas proyek Anda → **Models** → cari nama model yang sudah dideploy (misal, `gpt-4.1-mini`).

### Prioritas variabel env

`main.py` menggunakan `load_dotenv(override=False)`, artinya:

| Prioritas | Sumber | Menang jika keduanya diset? |
|----------|--------|-----------------------------|
| 1 (tertinggi) | Variabel lingkungan shell | Ya |
| 2 | File `.env` | Hanya jika variabel shell tidak diset |

Ini berarti variabel runtime Foundry (set lewat `agent.yaml`) lebih diutamakan dibanding nilai `.env` saat deployment host.

---

## Kompatibilitas versi

### Matriks versi paket

Alur kerja multi-agen membutuhkan versi paket tertentu. Versi yang tidak cocok menyebabkan error saat runtime.

| Paket | Versi yang Dibutuhkan | Perintah Cek |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | pre-release terbaru | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Kesalahan versi umum

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Perbaikan: tingkatkan ke rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` tidak ditemukan atau Inspector tidak kompatibel:**

```powershell
# Perbaiki: instal dengan flag --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Perbaiki: tingkatkan paket mcp
pip install mcp --upgrade
```

### Verifikasi semua versi sekaligus

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Output yang diharapkan:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## Masalah alat MCP

### Alat MCP tidak mengembalikan hasil

**Gejala:** Kartu gap menampilkan "No results returned from Microsoft Learn MCP" atau "No direct Microsoft Learn results found".

**Penyebab mungkin:**

1. **Masalah jaringan** - Endpoint MCP (`https://learn.microsoft.com/api/mcp`) tidak bisa diakses.  
   ```powershell
   # Uji konektivitas
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Jika ini mengembalikan `200`, endpoint dapat dijangkau.

2. **Query terlalu spesifik** - Nama keahlian terlalu niche untuk pencarian Microsoft Learn.  
   - Ini normal untuk keahlian yang sangat khusus. Alat memiliki URL fallback di respons.

3. **Timeout sesi MCP** - Koneksi Streamable HTTP kedaluwarsa.  
   - Coba permintaan ulang. Sesi MCP bersifat sementara dan mungkin perlu koneksi ulang.

### Penjelasan log MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Arti | Tindakan |
|-----|---------|--------|
| `GET → 405` | Probing klien MCP saat inisialisasi | Normal - abaikan |
| `POST → 200` | Panggilan alat berhasil | Sesuai harapan |
| `DELETE → 405` | Probing klien MCP saat pembersihan | Normal - abaikan |
| `POST → 400` | Bad request (query rusak) | Periksa parameter `query` di `search_microsoft_learn_for_plan()` |
| `POST → 429` | Terbatas oleh rate limit | Tunggu dan coba lagi. Kurangi parameter `max_results` |
| `POST → 500` | Error server MCP | Bersifat sementara - coba ulang. Jika terus terjadi, API Microsoft Learn MCP mungkin sedang down |
| Timeout koneksi | Masalah jaringan atau server MCP tidak tersedia | Periksa koneksi internet. Coba `curl https://learn.microsoft.com/api/mcp` |

---

## Masalah deployment

### Kontainer gagal mulai setelah deployment

1. **Periksa log kontainer:**  
   - Buka sidebar **Microsoft Foundry** → perluas **Hosted Agents (Preview)** → klik agen Anda → buka versinya → **Container Details** → **Logs**.  
   - Cari stack trace Python atau error modul tidak ditemukan.

2. **Kegagalan umum saat start kontainer:**

   | Error di log | Penyebab | Perbaikan |
   |--------------|----------|-----------|
   | `ModuleNotFoundError` | `requirements.txt` kurang paket | Tambahkan paket, deploy ulang |
   | `RuntimeError: Missing required environment variable` | Variabel env di `agent.yaml` tidak diset | Perbarui bagian `environment_variables` di `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Managed Identity belum dikonfigurasi | Foundry menetapkan ini otomatis - pastikan deploy lewat extension |
   | `OSError: port 8088 already in use` | Dockerfile expose port salah atau konflik port | Pastikan `EXPOSE 8088` di Dockerfile dan `CMD ["python", "main.py"]` benar |
   | Kontainer keluar dengan kode 1 | Exception tak tertangani di `main()` | Tes lokal dulu ([Modul 5](05-test-locally.md)) untuk tangkap error sebelum deploy |

3. **Deploy ulang setelah perbaikan:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → pilih agen yang sama → deploy versi baru.

### Deployment terlalu lama

Kontainer multi-agen butuh waktu lebih lama karena membuat 4 instance agen saat mulai. Waktu mulai normal:

| Tahap | Durasi yang Diharapkan |
|-------|------------------------|
| Build image kontainer | 1-3 menit |
| Push image ke ACR | 30-60 detik |
| Mulai kontainer (agen tunggal) | 15-30 detik |
| Mulai kontainer (multi-agen) | 30-120 detik |
| Agen tersedia di Playground | 1-2 menit setelah "Started" |

> Jika status "Pending" terus lebih dari 5 menit, periksa log kontainer untuk error.

---

## Masalah RBAC dan izin

### `403 Forbidden` atau `AuthorizationFailed`

Anda membutuhkan peran **[Azure AI User](https://aka.ms/foundry-ext-project-role)** di proyek Foundry Anda:

1. Masuk ke [Azure Portal](https://portal.azure.com) → resource proyek Foundry Anda.  
2. Klik **Access control (IAM)** → **Role assignments**.  
3. Cari nama Anda → pastikan **Azure AI User** tercantum.  
4. Jika tidak ada: **Add** → **Add role assignment** → cari **Azure AI User** → tugaskan ke akun Anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk detail.

### Deployment model tidak dapat diakses

Jika agen mengembalikan error terkait model:

1. Pastikan model sudah dideploy: sidebar Foundry → buka proyek → **Models** → periksa `gpt-4.1-mini` (atau model Anda) dengan status **Succeeded**.  
2. Pastikan nama deployment cocok: bandingkan `MODEL_DEPLOYMENT_NAME` di `.env` (atau `agent.yaml`) dengan nama deployment aktual di sidebar.  
3. Jika deployment kadaluarsa (free tier): deploy ulang dari [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Masalah Agent Inspector

### Inspector terbuka tapi menunjukkan "Disconnected"

1. Pastikan server berjalan: cek terminal ada pesan "Server running on http://localhost:8088".  
2. Periksa port `5679`: Inspector terhubung via debugpy di port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Restart server dan buka lagi Inspector.

### Inspector menunjukkan respons sebagian

Respons multi-agen panjang dan mengalir secara bertahap. Tunggu respons penuh selesai (bisa 30-60 detik tergantung jumlah kartu gap dan panggilan alat MCP).

Jika respons selalu terpotong:  
- Periksa instruksi GapAnalyzer sudah menyertakan blok `CRITICAL:` yang mencegah penggabungan kartu gap.  
- Cek batas token model Anda - `gpt-4.1-mini` mendukung hingga 32K token output, yang seharusnya cukup.

---

## Tips performa

### Respons lambat

Alur kerja multi-agen secara inheren lebih lambat karena ketergantungan berurutan dan panggilan alat MCP.

| Optimasi | Cara | Dampak |
|-------------|-----|--------|
| Kurangi panggilan MCP | Turunkan parameter `max_results` pada alat | Lebih sedikit perjalanan HTTP |
| Permudah instruksi | Prompt agen lebih singkat dan fokus | Inferensi LLM lebih cepat |
| Gunakan `gpt-4.1-mini` | Lebih cepat daripada `gpt-4.1` untuk pengembangan | Percepatan sekitar 2x |
| Kurangi detail kartu gap | Permudah format kartu gap di instruksi GapAnalyzer | Lebih sedikit output yang dihasilkan |

### Waktu respons tipikal (lokal)

| Konfigurasi | Waktu yang Diharapkan |
|--------------|----------------------|
| `gpt-4.1-mini`, 3-5 kartu gap | 30-60 detik |
| `gpt-4.1-mini`, 8+ kartu gap | 60-120 detik |
| `gpt-4.1`, 3-5 kartu gap | 60-120 detik |
---

## Mendapatkan bantuan

Jika Anda mengalami kesulitan setelah mencoba perbaikan di atas:

1. **Periksa log server** - Sebagian besar kesalahan menghasilkan jejak tumpukan Python di terminal. Baca jejak kesalahan secara lengkap.
2. **Cari pesan kesalahan** - Salin teks kesalahan dan cari di [Microsoft Q&A untuk Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Buka isu** - Buat isu di [repositori workshop](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) dengan:
   - Pesan kesalahan atau tangkapan layar
   - Versi paket Anda (`pip list | Select-String "agent-framework"`)
   - Versi Python Anda (`python --version`)
   - Apakah masalah terjadi secara lokal atau setelah penyebaran

---

### Checkpoint

- [ ] Anda dapat mengidentifikasi dan memperbaiki kesalahan multi-agen yang paling umum menggunakan tabel referensi cepat
- [ ] Anda tahu cara memeriksa dan memperbaiki masalah konfigurasi `.env`
- [ ] Anda dapat memverifikasi versi paket sesuai matriks yang diperlukan
- [ ] Anda memahami entri log MCP dan dapat mendiagnosis kegagalan alat
- [ ] Anda tahu cara memeriksa log kontainer untuk kegagalan penyebaran
- [ ] Anda dapat memverifikasi peran RBAC di Portal Azure

---

**Sebelumnya:** [07 - Verifikasi di Playground](07-verify-in-playground.md) · **Beranda:** [Lab 02 README](../README.md) · [Beranda Workshop](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berusaha untuk memberikan terjemahan yang akurat, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa asalnya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan penerjemah manusia profesional. Kami tidak bertanggung jawab atas kesalahpahaman atau kesalahan tafsir yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->