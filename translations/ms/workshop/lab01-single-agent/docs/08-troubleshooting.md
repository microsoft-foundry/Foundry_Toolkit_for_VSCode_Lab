# Modul 8 - Penyelesaian Masalah

Modul ini adalah panduan rujukan untuk isu biasa. Tandakan ia dan kembali semula apabila sesuatu tidak berjalan dengan betul.

---

## 1. Ralat kebenaran

### 1.1 Kebenaran `agents/write` ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Punca utama:** Peranan `Azure AI User` hilang di peringkat **projek**. Ini adalah ralat bengkel nombor satu.

**Pembetulan:**
1. Buka [portal.azure.com](https://portal.azure.com).
2. Cari nama **projek** Foundry anda → klik hasil yang bertipe **"Microsoft Foundry project"** (BUKAN akaun induk).
3. **Kawalan akses (IAM)** → **+ Tambah** → **Tambah perlantikan peranan**.
4. Peranan: **Azure AI User** → Seterusnya.
5. Ahli: Pilih diri anda → Semak + lantik → Semak + lantik.
6. **Tunggu 1–2 minit** → cuba semula.

> **Kenapa Pemilik/Penyumbang tidak mencukupi:** Peranan ini hanya memberikan tindakan *pengurusan*. Operasi ejen memerlukan tindakan *data* `agents/write`, yang hanya terdapat dalam `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Lihat [dokumentasi RBAC Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` semasa penyediaan

**Pembetulan:** Minta pentadbir anda untuk memberikan **Contributor** pada kumpulan sumber, atau minta mereka buat projek untuk anda dan beri anda **Azure AI User** padanya.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Tunggu sehingga: "Didaftarkan"
```

---

## 2. Ralat Docker

> Docker adalah **pilihan**. Ini hanya terpakai jika Docker Desktop dipasang dan sambungan cuba bina secara tempatan.

### 2.1 Docker daemon tidak berjalan

**Pembetulan:** Mulakan Docker Desktop → tunggu status "berjalan" → sahkan dengan `docker info` → cuba semula.

### 2.2 Pembinaan gagal dengan ralat kebergantungan

**Pembetulan:** Sahkan ejaan `requirements.txt`, uji secara tempatan dahulu: `pip install -r requirements.txt`.

### 2.3 Ketidakpadanan platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Ralat pengesahan

### 3.1 `DefaultAzureCredential` gagal

**Pembetulan (cuba mengikut urutan):**
1. `az login` (pengesahan semula)
2. `az account set --subscription "<id>"` (langganan betul)
3. VS Code → Akaun → Log Keluar → Log Masuk sekali lagi
4. Sahkan: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token berfungsi secara tempatan tetapi tidak dihoskan

**Jangkaan:** Ejen hos menggunakan identiti yang diurus sistem, bukan kelayakan anda. Jika ejen hos mendapat ralat pengesahan:
- Sahkan `AZURE_AI_PROJECT_ENDPOINT` dalam `agent.yaml` adalah betul
- Periksa identiti yang diurus projek mempunyai akses model

---

## 4. Ralat model

### 4.1 Penyebaran model tidak ditemui

**Pembetulan:** Nama adalah **sensitif huruf besar kecil**. Bandingkan `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` dengan nama tepat dalam bar sisi Foundry → Model.

### 4.2 Output model tidak dijangka

**Pembetulan:** Semak `AGENT_INSTRUCTIONS` dalam `main.py` (tidak dipendekkan?). Cuba model lain (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Ralat penyebaran

### 5.1 Tarikan ACR tidak dibenarkan

**Pembetulan:** Azure Portal → Container Registry → Kawalan akses (IAM) → Tambah peranan **AcrPull** pada identiti yang diurus projek Foundry.

### 5.2 Ejen gagal bermula (terus "Pending" atau "Failed")

Semak log kontena di bar sisi. Punca biasa:

| Mesej log | Pembetulan |
|-------------|-----|
| `ModuleNotFoundError` | Tambah pakej yang hilang dalam `requirements.txt`, deploy semula |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Tambah pembolehubah env dalam `agent.yaml` di bawah `environment_variables` |
| `Address already in use` | Pastikan hanya satu proses menggunakan port 8088 |

### 5.3 Penyebaran tamat masa

**Pembetulan:** Semak sambungan internet. Deploy pertama melebihi 100MB. Di belakang proksi? Konfigurasikan tetapan proksi Docker Desktop.

---

## 6. Laluan B - Foundry Tempatan

### 6.1 Foundry Tempatan tidak boleh mula

| Isu | Pembetulan |
|-------|-----|
| `foundry: command not found` | Pasang semula: `winget install Microsoft.FoundryLocal` |
| Sumber tidak cukup | Foundry Tempatan perlukan ~4GB RAM kosong. Tutup aplikasi lain. |
| Muat turun model gagal | Semak ruang cakera (model 2–8 GB). Cuba semula: `foundry local models pull <name>` |

### 6.2 Ralat model Foundry Tempatan

| Isu | Pembetulan |
|-------|-----|
| Respons lambat | Dijangka - model tempatan berjalan di CPU kecuali anda ada GPU. Bersabar. |
| Output berkualiti rendah | Cuba model lebih besar jika perkakasan anda membenarkan. `phi-4-mini` adalah keseimbangan yang baik. |
| Sambungan ditolak | Sahkan Foundry Tempatan berjalan: `foundry local status`. Mulakan semula jika perlu. |

---

## 7. Rujukan cepat: peranan RBAC

| Peranan | Skop | Memberi |
|------|-------|--------|
| **Azure AI User** | Projek | Tindakan data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Projek/Akaun | Tindakan data + penciptaan projek |
| **Azure AI Owner** | Akaun | Akses penuh + pengurusan peranan |
| **Contributor** | Langganan/Kumpulan sumber | Hanya tindakan pengurusan (**tiada** tindakan data) |
| **Owner** | Langganan/Kumpulan sumber | Tindakan pengurusan + perlantikan peranan (**tiada** tindakan data) |

---

## 8. Senarai semak penyelesaian bengkel

| # | Item | Modul |
|---|------|--------|
| 1 | Prasyarat dipasang dan disahkan | [00](00-prerequisites.md) |
| 2 | Sambungan Foundry Toolkit dipasang, projek disambungkan (atau Laluan B dikonfigurasikan) | [01](01-setup.md) |
| 3 | Ejen hos dibina | [02](02-create-hosted-agent.md) |
| 4 | `.env` dikonfigurasikan, arahan ditulis, kebergantungan dipasang | [03](03-configure-and-code.md) |
| 5 | Ejen diuji secara tempatan - 3 senario berfungsi lulus | [04](04-test-locally.md) |
| 6 | Disebar ke Foundry (Laluan A sahaja) | [05](05-deploy-to-foundry.md) |
| 7 | Ujian kes tepi/keselamatan lulus di awan (Laluan A sahaja) | [06](06-verify-in-playground.md) |
| 8 | Ringkasan disemak, langkah seterusnya dikenal pasti | [07](07-summary.md) |

---

**Sebelum ini:** [07 - Ringkasan](07-summary.md) · **Utama:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan oleh manusia profesional adalah disyorkan. Kami tidak bertanggungjawab terhadap sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->