# Modul 8 - Penyelesaian Masalah (Multi-Ejen)

Modul ini merangkumi kesilapan biasa, pembetulan, dan strategi pengesanan ralat khusus untuk aliran kerja multi-ejen. Untuk isu umum penghantaran Foundry, rujuk juga [panduan penyelesaian masalah Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md).

---

## Rujukan cepat: Ralat → Pembetulan

| Ralat / Simptom | Punca Mungkin | Pembetulan |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | Fail `.env` tiada atau nilai tidak ditetapkan | Cipta `.env` dengan `PROJECT_ENDPOINT=<your-endpoint>` dan `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | Persekitaran maya tidak diaktifkan atau kebergantungan tidak dipasang | Jalankan `.\.venv\Scripts\Activate.ps1` kemudian `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | Pakej MCP tidak dipasang (hilang dalam keperluan) | Jalankan `pip install mcp` atau periksa `requirements.txt` termasuk sebagai kebergantungan transitif |
| Ejen bermula tetapi memberikan respons kosong | `output_executors` tidak sepadan atau tepi hilang | Sahkan `output_executors=[gap_analyzer]` dan semua tepi wujud dalam `create_workflow()` |
| Hanya 1 kad jurang (yang lain hilang) | Arahan GapAnalyzer tidak lengkap | Tambah perenggan `CRITICAL:` ke `GAP_ANALYZER_INSTRUCTIONS` - lihat [Modul 3](03-configure-agents.md) |
| Skor keserasian adalah 0 atau tiada | MatchingAgent tidak menerima data huluan | Sahkan kedua-dua `add_edge(resume_parser, matching_agent)` dan `add_edge(jd_agent, matching_agent)` wujud |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | Pelayan MCP menolak panggilan alat | Periksa sambungan internet. Cuba buka `https://learn.microsoft.com/api/mcp` dalam pelayar. Cuba semula |
| Tiada URL Microsoft Learn dalam output | Alat MCP tidak didaftarkan atau titik akhir salah | Sahkan `tools=[search_microsoft_learn_for_plan]` pada GapAnalyzer dan `MICROSOFT_LEARN_MCP_ENDPOINT` betul |
| `Address already in use: port 8088` | Proses lain menggunakan port 8088 | Jalankan `netstat -ano \| findstr :8088` (Windows) atau `lsof -i :8088` (macOS/Linux) dan hentikan proses bertembung |
| `Address already in use: port 5679` | Konflik port Debugpy | Hentikan sesi debug lain. Jalankan `netstat -ano \| findstr :5679` untuk cari dan tamatkan proses |
| Agent Inspector tidak boleh dibuka | Pelayan belum dimulakan sepenuhnya atau konflik port | Tunggu log "Server running". Periksa port 5679 adalah bebas |
| `azure.identity.CredentialUnavailableError` | Tidak masuk ke Azure CLI | Jalankan `az login` kemudian mulakan semula pelayan |
| `azure.core.exceptions.ResourceNotFoundError` | Penghantaran model tidak wujud | Periksa `MODEL_DEPLOYMENT_NAME` sepadan dengan model yang dilaksanakan dalam projek Foundry anda |
| Status kontena "Failed" selepas penghantaran | Kontena terhenti semasa mula | Periksa log kontena di bar sisi Foundry. Biasa: env var hilang atau ralat import |
| Penghantaran menunjukkan "Pending" lebih 5 minit | Kontena lambat mula atau had sumber | Tunggu sehingga 5 minit untuk multi-ejen (mencipta 4 ejen). Jika masih pending, periksa log |
| `ValueError` dari `WorkflowBuilder` | Konfigurasi graf tidak sah | Pastikan `start_executor` ditetapkan, `output_executors` adalah senarai, dan tiada tepi bulat |

---

## Isu persekitaran dan konfigurasi

### Nilai `.env` hilang atau salah

Fail `.env` mesti berada dalam direktori `PersonalCareerCopilot/` (tahap sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Kandungan `.env` yang dijangka:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **Mencari PROJECT_ENDPOINT anda:**  
- Buka bar sisi **Microsoft Foundry** dalam VS Code → klik kanan projek anda → **Copy Project Endpoint**.  
- Atau pergi ke [Azure Portal](https://portal.azure.com) → projek Foundry anda → **Overview** → **Project endpoint**.

> **Mencari MODEL_DEPLOYMENT_NAME anda:** Dalam bar sisi Foundry, kembangkan projek anda → **Models** → cari nama model yang dihantar (contoh, `gpt-4.1-mini`).

### Keutamaan var lingkungan

`main.py` menggunakan `load_dotenv(override=False)`, bermakna:

| Keutamaan | Sumber | Menang jika kedua-duanya ditetapkan? |
|----------|--------|------------------------|
| 1 (tertinggi) | Pembolehubah persekitaran shell | Ya |
| 2 | Fail `.env` | Hanya jika var shell tidak ditetapkan |

Ini bermaksud var lingkungan runtime Foundry (ditetapkan melalui `agent.yaml`) mengambil keutamaan berbanding nilai `.env` semasa penghantaran dihoskan.

---

## Keserasian versi

### Matriks versi pakej

Aliran kerja multi-ejen memerlukan versi pakej tertentu. Versi tidak sepadan menyebabkan ralat runtime.

| Pakej | Versi Diperlukan | Perintah Semak |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | pratonton terkini | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Ralat versi biasa

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Betulkan: naik taraf ke rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` tidak ditemui atau Inspector tidak serasi:**

```powershell
# Pembetulan: pasang dengan bendera --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Baiki: naik taraf pakej mcp
pip install mcp --upgrade
```

### Sahkan semua versi sekali gus

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Output dijangka:

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

## Isu alat MCP

### Alat MCP tidak mengembalikan hasil

**Simptom:** Kad jurang memaparkan "No results returned from Microsoft Learn MCP" atau "No direct Microsoft Learn results found".

**Punca kemungkinan:**

1. **Isu rangkaian** - Titik akhir MCP (`https://learn.microsoft.com/api/mcp`) tidak dapat diakses.  
   ```powershell
   # Uji kesambungan
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Jika ini memulangkan `200`, titik akhir boleh dicapai.

2. **Pertanyaan terlalu spesifik** - Nama kemahiran terlalu khusus untuk carian Microsoft Learn.  
   - Ini dijangka untuk kemahiran sangat khusus. Alat ada URL gantian dalam respons.

3. **Masa tamat sesi MCP** - Sambungan HTTP Streamable tamat masa.  
   - Cuba hantar permintaan semula. Sesi MCP bersifat sementara dan mungkin perlu disambung semula.

### Penjelasan log MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Maksud | Tindakan |
|-----|---------|--------|
| `GET → 405` | Klien MCP menguji semasa inisialisasi | Normal - abaikan |
| `POST → 200` | Panggilan alat berjaya | Dijangka |
| `DELETE → 405` | Klien MCP menguji semasa pembersihan | Normal - abaikan |
| `POST → 400` | Permintaan buruk (pertanyaan rosak) | Periksa parameter `query` dalam `search_microsoft_learn_for_plan()` |
| `POST → 429` | Had kadar dicapai | Tunggu dan cuba semula. Kurangkan parameter `max_results` |
| `POST → 500` | Ralat pelayan MCP | Sementara - cuba semula. Jika berterusan, API Microsoft Learn MCP mungkin turun |
| Sambungan tamat masa | Isu rangkaian atau pelayan MCP tidak tersedia | Periksa internet. Cuba `curl https://learn.microsoft.com/api/mcp` |

---

## Isu penghantaran

### Kontena gagal mula selepas penghantaran

1. **Periksa log kontena:**  
   - Buka bar sisi **Microsoft Foundry** → kembangkan **Hosted Agents (Preview)** → klik ejen anda → kembangkan versi → **Container Details** → **Logs**.  
   - Cari jejak tumpukan Python atau ralat modul hilang.

2. **Kegagalan permulaan kontena biasa:**

   | Ralat dalam log | Punca | Pembetulan |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` hilang pakej | Tambah pakej, hantar semula |
   | `RuntimeError: Missing required environment variable` | var env dalam `agent.yaml` tidak ditetapkan | Kemas kini bahagian `environment_variables` dalam `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | Identiti Terkawal tidak dikonfigurasi | Foundry tetapkan ini secara automatik - pastikan anda menghantar melalui sambungan |
   | `OSError: port 8088 already in use` | Dockerfile dedahkan port salah atau konflik port | Sahkan `EXPOSE 8088` dalam Dockerfile dan `CMD ["python", "main.py"]` |
   | Kontena keluar dengan kod 1 | Pengecualian tidak ditangani dalam `main()` | Uji secara tempatan dahulu ([Modul 5](05-test-locally.md)) untuk mengesan ralat sebelum hantar |

3. **Hantar semula selepas pembetulan:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → pilih ejen yang sama → hantar versi baru.

### Penghantaran mengambil masa lama

Kontena multi-ejen mengambil masa lebih lama untuk mula kerana mereka mencipta 4 instans ejen semasa mula. Masa mula biasa:

| Tahap | Jangkaan tempoh |
|-------|------------------|
| Bina imej kontena | 1-3 minit |
| Tolak imej ke ACR | 30-60 saat |
| Mula kontena (ejen tunggal) | 15-30 saat |
| Mula kontena (multi-ejen) | 30-120 saat |
| Ejen tersedia di Playground | 1-2 minit selepas "Started" |

> Jika status "Pending" berterusan lebih 5 minit, periksa log kontena untuk ralat.

---

## Isu RBAC dan kebenaran

### `403 Forbidden` atau `AuthorizationFailed`

Anda memerlukan peranan **[Azure AI User](https://aka.ms/foundry-ext-project-role)** di projek Foundry anda:

1. Pergi ke [Azure Portal](https://portal.azure.com) → sumber **projek** Foundry anda.  
2. Klik **Access control (IAM)** → **Role assignments**.  
3. Cari nama anda → sahkan **Azure AI User** disenaraikan.  
4. Jika tiada: **Tambah** → **Add role assignment** → cari **Azure AI User** → laksanakan ke akaun anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk maklumat lanjut.

### Penghantaran model tidak dapat diakses

Jika ejen memberikan ralat berkaitan model:

1. Sahkan model dihantar: bar sisi Foundry → kembangkan projek → **Models** → periksa untuk `gpt-4.1-mini` (atau model anda) dengan status **Succeeded**.  
2. Sahkan nama penghantaran sepadan: bandingkan `MODEL_DEPLOYMENT_NAME` dalam `.env` (atau `agent.yaml`) dengan nama penghantaran sebenar dalam bar sisi.  
3. Jika penghantaran tamat tempoh (peringkat percuma): hantar semula dari [Katalog Model](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Isu Agent Inspector

### Inspector dibuka tetapi memaparkan "Disconnected"

1. Sahkan pelayan sedang berjalan: periksa "Server running on http://localhost:8088" dalam terminal.  
2. Periksa port `5679`: Inspector bersambung melalui debugpy pada port 5679.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Mulakan semula pelayan dan buka semula Inspector.

### Inspector menunjukkan respons separa

Respons multi-ejen panjang dan dihantar secara berperingkat. Tunggu respons penuh selesai (mungkin mengambil 30-60 saat bergantung pada bilangan kad jurang dan panggilan alat MCP).

Jika respons sentiasa dipotong:  
- Semak arahan GapAnalyzer mempunyai blok `CRITICAL:` yang menghalang penggabungan kad jurang.  
- Semak had token model anda - `gpt-4.1-mini` menyokong sehingga 32K token output, yang sepatutnya mencukupi.

---

## Petua prestasi

### Respons perlahan

Aliran kerja multi-ejen secara semula jadi lebih perlahan daripada ejen tunggal kerana pergantungan berurutan dan panggilan alat MCP.

| Pengoptimuman | Bagaimana | Kesan |
|-------------|-----|--------|
| Kurangkan panggilan MCP | Turunkan parameter `max_results` dalam alat | Kurangkan rundingan HTTP |
| Permudahkan arahan | Prompt ejen lebih pendek, fokus | Inference LLM lebih pantas |
| Gunakan `gpt-4.1-mini` | Lebih pantas daripada `gpt-4.1` untuk pembangunan | Peningkatan kelajuan ~2x |
| Kurangkan butiran kad jurang | Permudahkan format kad jurang dalam arahan GapAnalyzer | Output lebih sedikit untuk dihasilkan |

### Masa respons tipikal (tempatan)

| Konfigurasi | Masa dijangka |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 kad jurang | 30-60 saat |
| `gpt-4.1-mini`, 8+ kad jurang | 60-120 saat |
| `gpt-4.1`, 3-5 kad jurang | 60-120 saat |
---

## Mendapatkan bantuan

Jika anda tersekat selepas mencuba pembetulan di atas:

1. **Periksa log server** - Kebanyakan ralat menghasilkan jejak tumpukan Python di terminal. Baca jejak penuh.
2. **Cari mesej ralat** - Salin teks ralat dan cari di [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Buka isu** - Failkan isu di [repositori bengkel](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) dengan:
   - Mesej ralat atau tangkapan skrin
   - Versi pakej anda (`pip list | Select-String "agent-framework"`)
   - Versi Python anda (`python --version`)
   - Sama ada isu tersebut berlaku secara tempatan atau selepas pelancaran

---

### Penanda Aras

- [ ] Anda boleh mengenal pasti dan membetulkan ralat pelbagai agen yang paling biasa menggunakan jadual rujukan pantas
- [ ] Anda tahu cara memeriksa dan membetulkan isu konfigurasi `.env`
- [ ] Anda boleh mengesahkan versi pakej sepadan dengan matriks yang diperlukan
- [ ] Anda faham entri log MCP dan boleh mendiagnosis kegagalan alat
- [ ] Anda tahu cara memeriksa log kontena untuk kegagalan pelancaran
- [ ] Anda boleh mengesahkan peranan RBAC dalam Portal Azure

---

**Sebelumnya:** [07 - Verify in Playground](07-verify-in-playground.md) · **Utama:** [Lab 02 README](../README.md) · [Halaman Utama Bengkel](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan manusia profesional adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->