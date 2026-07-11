# Modul 8 - Penyelesaian Masalah

Modul ini merangkumi kesilapan biasa, pembetulan, dan strategi debugging khas untuk aliran kerja multi-ejen.

## Isu output Ejen

### GapAnalyzer mengatakan “Saya masih tidak mempunyai laporan padanan”

**Gejala:** Respons GapAnalyzer meminta anda untuk menampal laporan padanan dengan “Kemahiran Hilang” dan “Kekurangan Sijil.” Ini terjadi walaupun anda menghantar kedua-dua resume dan deskripsi kerja.

**Sebab:** Teks JD tidak disalurkan ke JD Agent. Dengan `context_mode="last_agent"`, `resume_executor` adalah satu-satunya pelaksana yang pernah melihat mesej asal pengguna. Jika `RESUME_PARSER_INSTRUCTIONS` tidak memasukkan teks JD dalam outputnya, JD Agent tidak mempunyai JD untuk dianalisis, MatchingAgent tidak dapat mengira skor kesesuaian, dan GapAnalyzer menerima input yang tidak bermakna.

**Diagnosis:**

Dalam log pelayan, cari jangka MatchingAgent. Jika ia mengandungi:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
pengaliran tidak ada atau rosak.

**Pembetulan:** Sahkan bahawa `RESUME_PARSER_INSTRUCTIONS` dalam `main.py` mengandungi bahagian `[JOB DESCRIPTION PASS-THROUGH]` dan peraturan:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Juga sahkan bahawa `JOB_DESCRIPTION_INSTRUCTIONS` mengandungi peraturan relay `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jika mana-mana blok arahan itu adalah cangkang dari wizard scaffold, gantikannya dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent mengeluarkan “Tidak dapat mengira skor kesesuaian - tiada JD diberikan”

Ini adalah punca akar yang sama seperti di atas. MatchingAgent menerima output JD Agent tetapi bahagian `[PARSED RESUME PASS-THROUGH]` hilang atau kosong, jadi ia tidak dapat membandingkan dua profil tersebut. Sahkan:
1. `JOB_DESCRIPTION_INSTRUCTIONS` termasuk peraturan relay: `Salin [PARSED RESUME] secara literal - Matching Agent bergantung kepadanya di hiliran.`
2. `MATCHING_AGENT_INSTRUCTIONS` memberitahu ejen untuk mencari bahagian `[JD REQUIREMENTS]` dan `[PARSED RESUME PASS-THROUGH]`.

Gantikan kedua-dua blok arahan dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Respons muncul dua kali

**Gejala:** Output GapAnalyzer (atau keseluruhan output paip) muncul dua kali dalam respons Agent Inspector.

**Sebab:** `WorkflowBuilder` menggunakan semantik OR untuk tepi masuk - pelaksana hiliran beroperasi sebaik sahaja **mana-mana** pendahulu selesai. Jika `matching_executor` mempunyai dua tepi masuk (satu dari `resume_executor` dan satu dari `jd_executor`), ia beroperasi dua kali: sekali apabila ResumeParser selesai dan sekali lagi apabila JD Agent selesai. GapAnalyzer kemudian juga berjalan dua kali.

**Pembetulan:** Pastikan graf `WorkflowBuilder` adalah paip urutan yang ketat tanpa fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # BUKAN dari resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jika anda mempunyai baris `.add_edge(resume_executor, matching_executor)` yang tersesat, buangkannya. Relay `[PARSED RESUME PASS-THROUGH]` dalam output JD Agent sudah memberi akses MatchingAgent kepada resume.

---

## Isu persekitaran dan konfigurasi

### Nilai `.env` hilang atau salah

Fail `.env` mesti berada di direktori `PersonalCareerCopilot/` (tahap yang sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Kandungan `.env` yang dijangka:

**Jalur A - awan Foundry:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Jalur B - Foundry Tempatan:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Kedua-dua jalur menggunakan `FOUNDRY_PROJECT_ENDPOINT`. Nilainya berbeza: awan menggunakan endpoint Foundry `https://`; tempatan menggunakan `http://localhost:5273/v1`. Jalankan `foundry model list` untuk mengesahkan alias model tepat bagi Jalur B.

> **Mencari `FOUNDRY_PROJECT_ENDPOINT` anda:** 
- Buka bar sisi **Foundry Toolkit** dalam VS Code → klik kanan projek anda → **Salin Project Endpoint**. 
- Atau pergi ke [Azure Portal](https://portal.azure.com) → projek Foundry anda → **Gambaran Keseluruhan** → **Project endpoint**.

> **Mencari `AZURE_AI_MODEL_DEPLOYMENT_NAME` anda:** Dalam bar sisi Foundry Toolkit, kembangkan projek anda → **Models** → cari nama model yang dideploy (contoh, `gpt-4.1-mini`).

### Keutamaan pembolehubah persekitaran

`main.py` menggunakan `load_dotenv(override=True)`, yang bermaksud:

| Keutamaan | Sumber | Menang apabila kedua-dua diset? |
|----------|--------|-----------------------------|
| 1 (tertinggi) | fail `.env` | Ya |
| 2 | Pembolehubah persekitaran Shell / kontena | Digunakan apabila kunci yang sama tiada dalam `.env` |

Dalam pembangunan tempatan, ini menjadikan `.env` sebagai sumber kebenaran (pengeditan `.env` memberi kesan segera pada runtime). Dalam penyebaran dihoskan, Foundry menyuntik pembolehubah persekitaran pada peringkat kontena; kerana `.env` bukan sebahagian daripada imej yang dihoskan untuk set makmal ini, nilai kontena yang disuntik digunakan.

---

## Keserasian versi

### Matriks versi pakej

Aliran kerja multi-ejen memerlukan versi pakej tertentu. Versi yang tidak sepadan menyebabkan ralat masa jalan.

| Pakej | Versi Diperlukan | Arahan Semak |
|---------|-----------------|---------------|
| `agent-framework-foundry` | terkini | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | terkini | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | terkini | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Ralat versi biasa

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Betulkan: pasang semula agent-framework-foundry
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Baiki: naik taraf pakej mcp
pip install mcp --upgrade
```

### Sahkan semua versi sekaligus

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Output dijangka:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Isu penyebaran

### Kontena gagal dimulakan selepas penyebaran

1. **Semak log kontena:**
   - Buka bar sisi **Foundry Toolkit** → kembangkan **Hosted Agents (Preview)** → klik ejen anda → kembangkan versi → **Container Details** → **Logs**.
   - Cari jejak tumpukan Python atau ralat modul hilang.

2. **Kegagalan permulaan kontena biasa:**

   | Ralat dalam log | Sebab | Pembetulan |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` hilang pakej | Tambah pakej, sebarkan semula |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` atau `.env` env vars tidak diset | Kemas kini bahagian `environment_variables` dalam `agent.yaml` (hoskan) atau `.env` (tempatan) |
   | `azure.identity.CredentialUnavailableError` | Identiti Terurus tidak dikonfigurasikan | Foundry menetapkannya secara automatik - pastikan anda menyebar melalui sambungan |
   | `OSError: port 8088 already in use` | Dockerfile mendedahkan port salah atau konflik port | Sahkan `EXPOSE 8088` dalam Dockerfile dan `CMD ["python", "main.py"]` |
   | Kontena keluar dengan kod 1 | Pengecualian tidak ditangani dalam `main()` | Uji secara tempatan dahulu ([Modul 5](05-test-locally.md)) untuk kesilapan sebelum menyebar |

3. **Sebarkan semula selepas pembetulan:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → pilih ejen yang sama → sebarkan versi baru.

### Penyebaran mengambil masa terlalu lama

Kontena multi-ejen mengambil masa lebih lama untuk bermula kerana ia mencipta 4 instans ejen pada permulaan. Masa permulaan biasa:

| Tahap | Tempoh Dijangka |
|-------|------------------|
| Membina imej kontena | 1-3 minit |
| Tolak imej ke ACR | 30-60 saat |
| Mula kontena (ejen tunggal) | 15-30 saat |
| Mula kontena (multi-ejen) | 30-120 saat |
| Ejen tersedia di Playground | 1-2 minit selepas "Started" |

> Jika status "Pending" berterusan lebih 5 minit, periksa log kontena untuk ralat.

---

## Isu RBAC dan kebenaran

### `403 Forbidden` atau `AuthorizationFailed`

Anda memerlukan peranan **[Foundry User](https://aka.ms/foundry-ext-project-role)** pada projek Foundry anda (dahulu dinamakan **Azure AI User** - ID peranan tidak berubah):

1. Pergi ke [Azure Portal](https://portal.azure.com) → sumber **projek** Foundry anda.
2. Klik **Access control (IAM)** → **Role assignments**.
3. Cari nama anda → sahkan **Foundry User** (atau label lama **Azure AI User**) disenaraikan.
4. Jika tiada: **Tambah** → **Add role assignment** → cari **Foundry User** → tetapkan pada akaun anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk maklumat lanjut.

### Penyebaran model tidak boleh diakses

Jika ejen mengembalikan ralat berkaitan model:

1. Sahkan model telah disebarkan: bar sisi Foundry → kembangkan projek → **Models** → periksa `gpt-4.1-mini` (atau model anda) dengan status **Succeeded**.
2. Sahkan nama penyebaran sepadan: bandingkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `.env` (atau `agent.yaml`) dengan nama penyebaran sebenar dalam bar sisi.
3. Jika penyebaran tamat tempoh (peringkat percuma): sebarkan semula dari [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Isu Foundry Tempatan (Jalur B)

### Perkhidmatan Foundry Tempatan tidak berjalan

```powershell
# Semak status
foundry local status

# Mulakan perkhidmatan jika ia dihentikan
foundry local start
```

| Gejala | Sebab | Pembetulan |
|---------|-------|-----|
| Pemeriksaan kesihatan mengembalikan `503` | Perkhidmatan tidak bermula | `foundry local start` atau klik **Start** di bar sisi Foundry Toolkit |
| Pemeriksaan kesihatan tamat masa | Model masih memuat | Tunggu 30–60 s selepas mula; model besar ambil masa lebih lama |
| `StatusCode: 404` pada `/v1/health` | Port salah | Lalai adalah `5273`. Semak `foundry local status` untuk port sebenar |
| Sumber tidak mencukupi | Foundry Local memerlukan ~4 GB RAM kosong | Tutup aplikasi lain |
| Muat turun model gagal | Ruang cakera rendah | Model 2–8 GB. Kosongkan ruang, kemudian `foundry model pull <name>` |

### Ketidaksesuaian nama model

```powershell
# Senaraikan model yang dimuat turun dan alias tepat mereka
foundry model list
```

Tetapkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `.env` kepada alias tepat yang dipaparkan (contohnya, `phi-4-mini`, bukan `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pada jalankan tempatan (Jalur B)

`main.py` makmal menggunakan `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local memerlukan pembolehubah ini menunjuk ke perkhidmatan tempatan - **bukan** `AZURE_AI_PROJECT_ENDPOINT`. Pastikan `.env` anda mengandungi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Alat MCP masih membuat panggilan keluar (Jalur B)

Ini dijangka. Alat `search_microsoft_learn_for_plan` mendapatkan sumber pembelajaran dari `https://learn.microsoft.com/api/mcp`. **Hanya pertanyaan nama kemahiran** yang dihantar melalui rangkaian - teks resume dan JD diproses sepenuhnya pada peranti anda dan tidak pernah dihantar. Jika perlu operasi sepenuhnya luar talian, tambah fallback `try/except` dalam alat yang mengembalikan URL statik `learn.microsoft.com` apabila endpoint tidak boleh dicapai.

---

## Mendapatkan bantuan

Jika anda tersekat selepas mencuba pembetulan di atas:

1. **Semak log pelayan** - Kebanyakan ralat menghasilkan jejak tumpukan Python dalam terminal. Baca traceback penuh.
2. **Cari mesej ralat** - Salin teks ralat dan cari di [Microsoft Q&A untuk Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services).
3. **Buka isu** - Failkan isu di [repositori bengkel](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) dengan:
   - Mesej ralat atau tangkapan layar
   - Versi pakej anda (`pip list | Select-String "agent-framework"`)
   - Versi Python anda (`python --version`)
   - Sama ada isu berlaku secara tempatan atau selepas penyebaran

---

### Titik semak

- [ ] Anda tahu cara semak dan betulkan isu konfigurasi `.env`
- [ ] Anda boleh mengesahkan versi pakej sepadan dengan matriks diperlukan
- [ ] Anda tahu cara semak log kontena untuk kegagalan penyebaran
- [ ] Anda boleh mengesahkan peranan RBAC dalam Azure Portal

---

**Sebelum:** [07 - Verify in Playground](07-verify-in-playground.md) · **Seterusnya:** [09 - Summary →](09-summary.md) · **Laman Utama:** [Lab 02 README](../README.md) · [Workshop Home](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->