# Modul 8 - Pemecahan Masalah

Modul ini adalah panduan referensi untuk masalah umum. Tandai dan kembali ketika ada yang salah.

---

## 1. Kesalahan izin

### 1.1 `agents/write` izin ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Penyebab utama:** Peran `Azure AI User` hilang di tingkat **proyek**. Ini adalah kesalahan nomor 1 di workshop.

**Perbaikan:**
1. Buka [portal.azure.com](https://portal.azure.com).
2. Cari nama **proyek** Foundry Anda → klik hasil dengan tipe **"Microsoft Foundry project"** (BUKAN akun induk).
3. **Kontrol akses (IAM)** → **+ Tambah** → **Tambahkan penugasan peran**.
4. Peran: **Azure AI User** → Berikutnya.
5. Anggota: Pilih diri Anda → Tinjau + tetapkan → Tinjau + tetapkan.
6. **Tunggu 1–2 menit** → coba lagi.

> **Mengapa Owner/Contributor tidak cukup:** Peran ini hanya memberikan tindakan *manajemen*. Operasi agen membutuhkan `agents/write` *tindakan data*, yang hanya ada di `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Lihat [dokumentasi Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` selama penyediaan

**Perbaikan:** Minta admin Anda menetapkan **Contributor** pada grup sumber daya, atau minta mereka membuat proyek untuk Anda dan memberikan **Azure AI User** pada proyek tersebut.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Wait until: "Registered"
```

---

## 2. Kesalahan Docker

> Docker adalah **opsional**. Ini hanya berlaku jika Docker Desktop terpasang dan ekstensi mencoba membuat build lokal.

### 2.1 Docker daemon tidak berjalan

**Perbaikan:** Mulai Docker Desktop → tunggu status "berjalan" → verifikasi dengan `docker info` → coba lagi.

### 2.2 Build gagal karena kesalahan dependensi

**Perbaikan:** Periksa ejaan `requirements.txt`, uji secara lokal terlebih dahulu: `pip install -r requirements.txt`.

### 2.3 Ketidakcocokan platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Kesalahan autentikasi

### 3.1 `DefaultAzureCredential` gagal

**Perbaikan (coba sesuai urutan):**
1. `az login` (autentikasi ulang)
2. `az account set --subscription "<id>"` (langganan yang benar)
3. VS Code → Akun → Keluar → Masuk kembali
4. Verifikasi: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token bekerja secara lokal tapi tidak dihosting

**Diharapkan:** Agen yang dihosting menggunakan identitas yang dikelola sistem, bukan kredensial Anda. Jika agen yang dihosting mengalami kesalahan autentikasi:
- Verifikasi `AZURE_AI_MODEL_DEPLOYMENT_NAME` dalam `agent.yaml` mengarah ke nama penyebaran model Anda (`FOUNDRY_PROJECT_ENDPOINT` disisipkan oleh Foundry saat runtime - jangan deklarasikan di `agent.yaml`)
- Periksa bahwa identitas yang dikelola proyek memiliki akses model

---

## 4. Kesalahan model

### 4.1 Penyebaran model tidak ditemukan

**Perbaikan:** Nama bersifat **case-sensitive**. Bandingkan `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` dengan nama tepat di sidebar Foundry → Models.

### 4.2 Output model tidak terduga

**Perbaikan:** Tinjau `AGENT_INSTRUCTIONS` dalam `main.py` (tidak terpotong?). Coba model berbeda (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Kesalahan penyebaran

### 5.1 ACR tarik tidak diizinkan

**Perbaikan:** Azure Portal → Container Registry → Kontrol akses (IAM) → Tambahkan peran **AcrPull** ke identitas terkelola proyek Foundry.

### 5.2 Agen gagal mulai (tetap "Pending" atau "Failed")

Periksa log kontainer di sidebar. Penyebab umum:

| Pesan log | Perbaikan |
|-------------|-----|
| `ModuleNotFoundError` | Tambahkan paket yang hilang ke `requirements.txt`, deploy ulang |
| `ValueError: Missing required environment variables` | Pastikan `AZURE_AI_MODEL_DEPLOYMENT_NAME` dideklarasikan di `agent.yaml` di bawah `environment_variables` dan memiliki nilai, lalu deploy ulang. `FOUNDRY_PROJECT_ENDPOINT` disisipkan oleh Foundry saat runtime |
| `Address already in use` | Pastikan hanya satu proses yang mengikat port 8088 |

### 5.3 Penyebaran habis waktu

**Perbaikan:** Periksa koneksi internet. Deploy pertama mengunggah >100MB. Apakah di belakang proxy? Konfigurasikan pengaturan proxy Docker Desktop.

---

## 6. Jalur B - Foundry Lokal

### 6.1 Foundry Lokal tidak mau mulai

| Masalah | Perbaikan |
|-------|-----|
| `foundry: command not found` | Instal ulang: `winget install Microsoft.FoundryLocal` |
| Sumber daya tidak cukup | Foundry Lokal membutuhkan ~4GB RAM bebas. Tutup aplikasi lain. |
| Gagal unduh model | Periksa ruang disk (model 2–8 GB). Coba lagi: `foundry local models pull <name>` |

### 6.2 Kesalahan model Foundry Lokal

| Masalah | Perbaikan |
|-------|-----|
| Respons lambat | Diharapkan - model lokal berjalan di CPU kecuali Anda memiliki GPU. Bersabarlah. |
| Output kualitas buruk | Coba model yang lebih besar jika perangkat keras Anda memungkinkan. `phi-4-mini` adalah keseimbangan yang baik. |
| Koneksi ditolak | Verifikasi Foundry Lokal berjalan: `foundry local status`. Restart jika perlu. |

---

## 7. Referensi cepat: peran RBAC

| Peran | Lingkup | Hak Akses |
|------|-------|--------|
| **Azure AI User** | Proyek | Tindakan data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Proyek/Akun | Tindakan data + pembuatan proyek |
| **Azure AI Owner** | Akun | Akses penuh + manajemen peran |
| **Contributor** | Langganan/RG | Hanya tindakan manajemen (**tidak** tindakan data) |
| **Owner** | Langganan/RG | Manajemen + penugasan peran (**tidak** tindakan data) |

---

## 8. Daftar periksa penyelesaian workshop

| # | Item | Modul |
|---|------|--------|
| 1 | Prasyarat terpasang dan diverifikasi | [00](00-prerequisites.md) |
| 2 | Ekstensi Foundry Toolkit terpasang, proyek terhubung (atau Jalur B dikonfigurasi) | [01](01-setup.md) |
| 3 | Agen yang dihosting telah disiapkan | [02](02-create-hosted-agent.md) |
| 4 | `.env` dikonfigurasi, instruksi ditulis, dependensi terpasang | [03](03-configure-and-code.md) |
| 5 | Agen diuji secara lokal - 3 skenario fungsional berhasil | [04](04-test-locally.md) |
| 6 | Disebarkan ke Foundry (hanya Jalur A) | [05](05-deploy-to-foundry.md) |
| 7 | Tes kasus tepi/keamanan berhasil di cloud (hanya Jalur A) | [06](06-verify-in-playground.md) |
| 8 | Ringkasan ditinjau, langkah selanjutnya diidentifikasi | [07](07-summary.md) |

---

**Sebelumnya:** [07 - Ringkasan](07-summary.md) · **Beranda:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->