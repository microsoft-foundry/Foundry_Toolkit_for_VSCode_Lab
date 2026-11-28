# Modul 8 - Penyelesaian Masalah

Modul ini adalah panduan rujukan untuk isu biasa. Tandakan dan kembali semula apabila sesuatu berjalan tidak betul.

---

## 1. Ralat kebenaran

### 1.1 `agents/write` kebenaran ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Punca utama:** Kekurangan peranan `Azure AI User` pada tahap **projek**. Ini adalah ralat nombor 1 dalam bengkel.

**Baiki:**
1. Buka [portal.azure.com](https://portal.azure.com).
2. Cari nama **projek** Foundry anda → klik keputusan jenis **"Microsoft Foundry project"** (BUKAN akaun induk).
3. **Kawalan capaian (IAM)** → **+ Tambah** → **Tambah tugasan peranan**.
4. Peranan: **Azure AI User** → Seterusnya.
5. Ahli: Pilih diri anda → Semak + tugaskan → Semak + tugaskan.
6. **Tunggu 1–2 minit** → cuba semula.

> **Kenapa Owner/Contributor tidak cukup:** Peranan ini hanya memberikan tindakan *pengurusan* sahaja. Operasi agen memerlukan `agents/write` *tindakan data*, yang hanya terdapat dalam `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Rujuk [Dokumen RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` semasa penyediaan

**Baiki:** Minta pentadbir anda memberikan **Contributor** pada kumpulan sumber, atau suruh mereka buat projek untuk anda dan berikan anda **Azure AI User** padanya.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Ralat Docker

> Docker adalah **pilihan**. Ini hanya terpakai jika Docker Desktop dipasang dan peluasan cuba bina secara tempatan.

### 2.1 Docker daemon tidak berjalan

**Baiki:** Mula Docker Desktop → tunggu status "berjalan" → sahkan dengan `docker info` → cuba semula.

### 2.2 Binaan gagal dengan ralat pergantungan

**Baiki:** Sahkan ejaan `requirements.txt`, uji secara tempatan dahulu: `pip install -r requirements.txt`.

### 2.3 Ketidakpadanan platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Ralat pengesahan

### 3.1 `DefaultAzureCredential` gagal

**Baiki (cuba mengikut urutan):**
1. `az login` (pengesahan semula)
2. `az account set --subscription "<id>"` (langganan betul)
3. VS Code → Akaun → Log Keluar → Log Masuk semula
4. Sahkan: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token berfungsi secara tempatan tetapi tidak dihoskan

**Jangkaan:** Ejen dihoskan menggunakan identiti sistem yang diurus, bukan kelayakan anda. Jika ejen dihoskan mendapat ralat pengesahan:
- Sahkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `agent.yaml` merujuk kepada nama penyebaran model anda (`FOUNDRY_PROJECT_ENDPOINT` disuntik oleh Foundry semasa masa jalan - jangan isytiharkan dalam `agent.yaml`)
- Semak bahawa identiti yang diurus projek mempunyai capaian model

---

## 4. Ralat model

### 4.1 Penyebaran model tidak ditemui

**Baiki:** Nama adalah **sensitif huruf besar kecil**. Bandingkan `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` dengan nama tepat di bar sisi Foundry → Models.

### 4.2 Output model tidak dijangka

**Baiki:** Semak `AGENT_INSTRUCTIONS` dalam `main.py` (tidak terpotong?). Cuba model lain (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Ralat penyebaran

### 5.1 Tarikan ACR tidak dibenarkan

**Baiki:** Portal Azure → Container Registry → Kawalan capaian (IAM) → Tambah peranan **AcrPull** kepada identiti yang diurus projek Foundry.

### 5.2 Ejen gagal mula (terus "Pending" atau "Failed")

Semak log kontena di bar sisi. Punca biasa:

| Mesej log | Baiki |
|-------------|-----|
| `ModuleNotFoundError` | Tambah pakej yang hilang ke `requirements.txt`, sebarkan semula |
| `ValueError: Missing required environment variables` | Sahkan `AZURE_AI_MODEL_DEPLOYMENT_NAME` diisytiharkan dalam `agent.yaml` di bawah `environment_variables` dan mempunyai nilai, kemudian sebarkan semula. `FOUNDRY_PROJECT_ENDPOINT` disuntik oleh Foundry semasa masa jalan |
| `Address already in use` | Pastikan hanya satu proses mengikat ke port 8088 |

### 5.3 Penyebaran tamat masa

**Baiki:** Semak sambungan internet. Penyebaran pertama menolak >100MB. Di belakang proksi? Konfigurasikan tetapan proksi Docker Desktop.

---

## 6. Laluan B - Foundry Lokal

### 6.1 Foundry Lokal tidak mula

| Isu | Baiki |
|-------|-----|
| `foundry: command not found` | Pasang semula: `winget install Microsoft.FoundryLocal` |
| Sumber tidak mencukupi | Foundry Lokal perlu ~4GB RAM kosong. Tutup aplikasi lain. |
| Muat turun model gagal | Semak ruang cakera (model adalah 2–8 GB). Cuba semula: `foundry local models pull <name>` |

### 6.2 Ralat model Foundry Lokal

| Isu | Baiki |
|-------|-----|
| Respons lambat | Dijangka - model tempatan berjalan pada CPU kecuali anda ada GPU. Bersabarlah. |
| Output kualiti rendah | Cuba model lebih besar jika perkakasan anda membolehkan. `phi-4-mini` adalah keseimbangan yang baik. |
| Sambungan ditolak | Sahkan Foundry Lokal berjalan: `foundry local status`. Mulakan semula jika perlu. |

---

## 7. Rujukan pantas: Peranan RBAC

| Peranan | Skop | Memberi |
|------|-------|--------|
| **Azure AI User** | Projek | Tindakan data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projek/Akaun | Tindakan data + penciptaan projek |
| **Azure AI Owner** | Akaun | Akses penuh + pengurusan peranan |
| **Contributor** | Langganan/RG | Tindakan pengurusan sahaja (**tiada** tindakan data) |
| **Owner** | Langganan/RG | Pengurusan + tugasan peranan (**tiada** tindakan data) |

---

## 8. Senarai semak penyelesaian bengkel

| # | Item | Modul |
|---|------|--------|
| 1 | Prasyarat dipasang dan disahkan | [00](00-prerequisites.md) |
| 2 | Pemasangan sambungan Foundry Toolkit, projek disambungkan (atau Laluan B dikonfigurasikan) | [01](01-setup.md) |
| 3 | Ejen dihoskan disiapkan | [02](02-create-hosted-agent.md) |
| 4 | `.env` dikonfigurasikan, arahan ditulis, pergantungan dipasang | [03](03-configure-and-code.md) |
| 5 | Ejen diuji secara tempatan - 3 senario berfungsi lulus | [04](04-test-locally.md) |
| 6 | Disebarkan ke Foundry (hanya Laluan A) | [05](05-deploy-to-foundry.md) |
| 7 | Ujian kes tepi/keselamatan lulus di awan (hanya Laluan A) | [06](06-verify-in-playground.md) |
| 8 | Ringkasan disemak, langkah seterusnya dikenal pasti | [07](07-summary.md) |

---

**Sebelumnya:** [07 - Ringkasan](07-summary.md) · **Laman Utama:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->