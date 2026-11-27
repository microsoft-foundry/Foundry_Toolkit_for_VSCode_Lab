# Modul 8 - Penyelesaian Masalah

Modul ini merangkumi ralat biasa, pembetulan, dan strategi pengesanan masalah khusus untuk aliran kerja pelbagai ejen.

## Isu output ejen

### GapAnalyzer mengatakan “Saya masih belum mendapat laporan padanan”

**Gejala:** Respons GapAnalyzer meminta anda untuk menampal laporan padanan dengan “Kemahiran Hilang” dan “Kekurangan Sijil.” Ini berlaku walaupun anda telah menghantar kedua-dua resume dan keterangan kerja.

**Punca:** Teks JD tidak dihantar ke bawah kepada JD Agent. Dengan `context_mode="last_agent"`, `resume_executor` adalah satu-satunya pelaksana yang pernah melihat mesej asal pengguna. Jika `RESUME_PARSER_INSTRUCTIONS` tidak memasukkan teks JD dalam outputnya, JD Agent tidak mempunyai JD untuk diurai, MatchingAgent tidak boleh mengira skor padanan, dan GapAnalyzer menerima input yang tidak bermakna.

**Diagnosis:**

Dalam log pelayan, cari span MatchingAgent. Jika ia mengandungi:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
penyaluran itu hilang atau rosak.

**Pembetulan:** Sahkan bahawa `RESUME_PARSER_INSTRUCTIONS` dalam `main.py` mengandungi seksyen `[JOB DESCRIPTION PASS-THROUGH]` dan peraturan:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Sahkan juga bahawa `JOB_DESCRIPTION_INSTRUCTIONS` mengandungi peraturan penyaluran `[PARSED RESUME PASS-THROUGH]`:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Jika mana-mana blok arahan itu adalah stub dari wizard scaffold, gantikannya dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### MatchingAgent mengeluarkan “Tidak dapat mengira skor padanan - tiada JD disediakan”

Ini adalah punca utama yang sama seperti di atas. MatchingAgent menerima output JD Agent tetapi seksyen `[PARSED RESUME PASS-THROUGH]` hilang atau kosong, jadi ia tidak dapat membandingkan kedua-dua profil. Sahkan:
1. `JOB_DESCRIPTION_INSTRUCTIONS` mengandungi peraturan penyaluran: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` memberitahu ejen untuk mencari seksyen `[JD REQUIREMENTS]` dan `[PARSED RESUME PASS-THROUGH]`.

Gantikan kedua-dua blok arahan dengan versi lengkap dari [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py).

### Respons muncul dua kali

**Gejala:** Output GapAnalyzer (atau keseluruhan output saluran) muncul dua kali dalam respons Pemeriksa Ejen.

**Punca:** `WorkflowBuilder` menggunakan semantik ATAU untuk tepi masuk - pelaksana hiliran dijalankan sebaik sahaja **mana-mana** pendahulu selesai. Jika `matching_executor` mempunyai dua tepi masuk (satu dari `resume_executor` dan satu dari `jd_executor`), ia akan dijalankan dua kali: sekali apabila ResumeParser selesai dan sekali lagi apabila JD Agent selesai. GapAnalyzer juga kemudian berjalan dua kali.

**Pembetulan:** Pastikan graf `WorkflowBuilder` adalah saluran berurutan ketat tanpa fan-in:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # NOT from resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Jika anda mempunyai baris `.add_edge(resume_executor, matching_executor)` yang berselerak, keluarkannya. Penyaluran `[PARSED RESUME PASS-THROUGH]` dalam output JD Agent sudah memberikan akses MatchingAgent kepada resume.

---

## Isu persekitaran dan konfigurasi

### Nilai `.env` hilang atau salah

Fail `.env` mesti berada dalam direktori `PersonalCareerCopilot/` (peringkat yang sama dengan `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Kandungan `.env` yang dijangka:

**Jejak A - Foundry awan:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Jejak B - Foundry Tempatan:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Kedua-dua jejak menggunakan `FOUNDRY_PROJECT_ENDPOINT`. Nilainya berbeza: awan menggunakan titik akhir Foundry `https://`; tempatan menggunakan `http://localhost:5273/v1`. Jalankan `foundry model list` untuk mengesahkan alias model tepat untuk Jejak B.

> **Mencari `FOUNDRY_PROJECT_ENDPOINT` anda:** 
- Buka sidebar **Foundry Toolkit** dalam VS Code → klik kanan projek anda → **Salin Titik Akhir Projek**. 
- Atau pergi ke [Azure Portal](https://portal.azure.com) → projek Foundry anda → **Gambaran Keseluruhan** → **Titik akhir projek**.

> **Mencari `AZURE_AI_MODEL_DEPLOYMENT_NAME` anda:** Dalam sidebar Foundry Toolkit, kembangkan projek anda → **Model** → cari nama model yang diterapkan (contohnya, `gpt-4.1-mini`).

### Keutamaan pembolehubah persekitaran

`main.py` menggunakan `load_dotenv(override=True)`, yang bermaksud:

| Keutamaan | Sumber | Menang apabila kedua-duanya ditetapkan? |
|----------|--------|------------------------------|
| 1 (tertinggi) | Fail `.env` | Ya |
| 2 | Pembolehubah persekitaran Shell / kontena | Digunakan apabila kunci yang sama tidak hadir dalam `.env` |

Dalam pembangunan tempatan, ini menjadikan `.env` sumber kebenaran (menyunting `.env` terus menjejaskan larian). Dalam penghantaran dihoskan, Foundry menyuntik pembolehubah persekitaran pada tahap kontena; kerana `.env` bukan sebahagian daripada imej yang diterapkan untuk persediaan makmal ini, nilai kontena yang disuntik digunakan.

---

## Keserasian versi

### Matriks versi pakej

Aliran kerja multi-ejen memerlukan versi pakej tertentu. Versi yang tidak sepadan menyebabkan ralat masa jalan.

| Pakej | Versi Diperlukan | Perintah Semak |
|---------|-----------------|---------------|
| `agent-framework-foundry` | terkini | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | terkini | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | terkini | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Ralat versi biasa

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

## Isu penghantaran

### Kontena gagal bermula selepas penghantaran

1. **Semak log kontena:**
   - Buka sidebar **Foundry Toolkit** → di bawah projek anda, klik **Ejen** → tab **Ejen Dihoskan** → klik ejen anda. Semak **Status** pada tab **Butiran**, kemudian buka tab **Playground** dan gunakan tab **Log** dalam panel **Butiran Sesi** untuk melihat output kontena.
   - Cari jejak tumpukan Python atau ralat modul hilang.

2. **Kegagalan permulaan kontena biasa:**

   | Ralat dalam log | Punca | Pembetulan |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` hilang pakej | Tambah pakej, hantar semula |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` atau pembolehubah persekitaran `.env` tidak diset | Kemas kini `agent.yaml` → seksyen `environment_variables` (dihoskan) atau `.env` (tempatan) |
   | `azure.identity.CredentialUnavailableError` | Identiti Terurus tidak disediakan | Foundry menetapkannya secara automatik - pastikan anda menghantar menggunakan sambungan |
   | `OSError: port 8088 already in use` | Dockerfile mendedahkan port salah atau konflik port | Sahkan `EXPOSE 8088` dalam Dockerfile dan `CMD ["python", "main.py"]` |
   | Kontena keluar dengan kod 1 | Pengecualian tidak dikendalikan dalam `main()` | Uji secara tempatan dahulu ([Modul 5](05-test-locally.md)) untuk mengesan ralat sebelum menghantar |

3. **Hantar semula selepas membaiki:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Hantar Ejen Dihoskan** → pilih ejen yang sama → hantar versi baru.

### Penghantaran mengambil masa terlalu lama

Kontena multi-ejen mengambil masa lebih lama untuk bermula kerana mereka membuat 4 contoh ejen semasa permulaan. Masa permulaan biasa:

| Peringkat | Tempoh Dijangka |
|-------|------------------|
| Pembinaan imej kontena | 1-3 minit |
| Tolak imej ke ACR | 30-60 saat |
| Permulaan kontena (ejen tunggal) | 15-30 saat |
| Permulaan kontena (multi-ejen) | 30-120 saat |
| Ejen tersedia dalam Playground | 1-2 minit selepas "Dibuka" |

> Jika status "Menunggu" berterusan lebih dari 5 minit, periksa log kontena untuk ralat.

---

## Isu RBAC dan kebenaran

### `403 Forbidden` atau `AuthorizationFailed`

Anda memerlukan peranan **[Foundry User](https://aka.ms/foundry-ext-project-role)** pada projek Foundry anda (sebelumnya dinamakan **Azure AI User** - ID peranan tidak berubah):

1. Pergi ke [Azure Portal](https://portal.azure.com) → sumber **projek** Foundry anda.
2. Klik **Kawalan akses (IAM)** → **Penugasan peranan**.
3. Cari nama anda → sahkan **Foundry User** (atau label lama **Azure AI User**) disenaraikan.
4. Jika tiada: **Tambah** → **Tambah penugasan peranan** → cari **Foundry User** → tugaskan ke akaun anda.

Lihat dokumentasi [RBAC untuk Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) untuk butiran.

### Penghantaran model tidak boleh diakses

Jika ejen mengembalikan ralat berkaitan model:

1. Sahkan model diterapkan: sidebar Foundry → kembangkan projek → **Model** → periksa untuk `gpt-4.1-mini` (atau model anda) dengan status **Berjaya**.
2. Sahkan nama penghantaran sepadan: bandingkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `.env` (atau `agent.yaml`) dengan nama penghantaran sebenar dalam sidebar.
3. Jika penghantaran telah tamat tempoh (peringkat percuma): hantar semula dari [Katalog Model](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Buka Katalog Model**).

---

## Isu Foundry Local (Jejak B)

### Perkhidmatan Foundry Local tidak berjalan

```powershell
# Check status
foundry local status

# Start the service if it is stopped
foundry local start
```

| Gejala | Punca | Pembetulan |
|---------|-------|-----|
| Pemeriksaan kesihatan mengembalikan `503` | Perkhidmatan tidak dimulakan | `foundry local start` atau klik **Mula** dalam sidebar Foundry Toolkit |
| Pemeriksaan kesihatan tamat masa | Model masih dimuatkan | Tunggu 30–60 s selepas memulakan; model yang lebih besar mengambil masa lebih lama |
| `StatusCode: 404` pada `/v1/health` | Port salah | Lalai adalah `5273`. Semak `foundry local status` untuk port sebenar |
| Sumber tidak mencukupi | Foundry Local memerlukan ~4 GB RAM percuma | Tutup aplikasi lain |
| Muat turun model gagal | Ruang cakera rendah | Model adalah 2–8 GB. Kosongkan ruang, kemudian `foundry model pull <name>` |

### Ketidakpadanan nama model

```powershell
# List downloaded models and their exact aliases
foundry model list
```

Tetapkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `.env` kepada alias tepat ditunjukkan (contoh, `phi-4-mini`, bukan `Phi-4-mini`).

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` pada larian tempatan (Jejak B)

Lab ini menggunakan `main.py` dengan `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`. Foundry Local memerlukan pembolehubah ini menunjuk ke perkhidmatan tempatan - **bukan** `AZURE_AI_PROJECT_ENDPOINT`. Pastikan `.env` anda mengandungi:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### Alat MCP masih membuat panggilan keluar (Jejak B)

Ini dijangka. Alat `search_microsoft_learn_for_plan` mendapatkan sumber pembelajaran dari `https://learn.microsoft.com/api/mcp`. **Hanya pertanyaan nama kemahiran** yang menghantar melalui rangkaian - resume dan teks JD diproses sepenuhnya pada peranti anda dan tidak pernah dihantar. Jika operasi sepenuhnya luar talian diperlukan, tambah penggantian `try/except` dalam alat yang mengembalikan URL `learn.microsoft.com` statik apabila titik akhir tidak dapat dihubungi.

---

## Mendapatkan bantuan

Jika anda tersekat selepas mencuba pembetulan di atas:

1. **Semak log pelayan** - Kebanyakan ralat menghasilkan jejak tumpukan Python dalam terminal. Baca keseluruhan jejak balik.
2. **Cari mesej ralat** - Salin teks ralat dan cari dalam [Microsoft Q&A untuk Perkhidmatan Ejen Foundry](https://learn.microsoft.com/answers/tags/1581/foundry-agent-service).
3. **Buka isu** - Failkan isu pada [repositori bengkel](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) dengan:
   - Mesej ralat atau tangkapan layar
   - Versi pakej anda (`pip list | Select-String "agent-framework"`)
   - Versi Python anda (`python --version`)
   - Sama ada isu itu berlaku secara tempatan atau selepas penghantaran

---

### Titik semak

- [ ] Anda tahu bagaimana memeriksa dan membetulkan isu konfigurasi `.env`
- [ ] Anda boleh mengesahkan versi pakej menyamai matriks yang diperlukan
- [ ] Anda tahu bagaimana memeriksa log kontena untuk kegagalan penghantaran
- [ ] Anda boleh mengesahkan peranan RBAC dalam Portal Azure

---

**Sebelumnya:** [07 - Sahkan dalam Playground](07-verify-in-playground.md) · **Seterusnya:** [09 - Ringkasan →](09-summary.md) · **Utama:** [README Makmal 02](../README.md) · [Utama Bengkel](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->