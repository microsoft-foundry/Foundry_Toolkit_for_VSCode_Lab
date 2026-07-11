# Modul 8 - Pemecahan Masalah

Modul ini adalah panduan referensi untuk masalah umum. Tandai dan kembali saat sesuatu tidak berjalan dengan baik.

---

## 1. Kesalahan izin

### 1.1 Izin `agents/write` ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Penyebab utama:** Tidak adanya peran `Azure AI User` di tingkat **proyek**. Ini adalah kesalahan #1 dalam workshop.

**Perbaikan:**
1. Buka [portal.azure.com](https://portal.azure.com).
2. Cari nama **proyek** Foundry Anda → klik hasil dengan tipe **"Microsoft Foundry project"** (BUKAN akun induk).
3. **Access control (IAM)** → **+ Add** → **Add role assignment**.
4. Peran: **Azure AI User** → Berikutnya.
5. Anggota: Pilih diri Anda sendiri → Tinjau + tetapkan → Tinjau + tetapkan.
6. **Tunggu 1–2 menit** → coba lagi.

> **Mengapa Owner/Contributor tidak cukup:** Peran ini hanya memberikan aksi *manajemen*. Operasi agen memerlukan *aksi data* `agents/write`, yang hanya ada di `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Lihat [dokumentasi Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` selama penyediaan

**Perbaikan:** Minta admin Anda memberikan **Contributor** pada grup sumber daya, atau minta mereka membuat proyek dan memberi Anda **Azure AI User** pada proyek itu.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# Tunggu sampai: "Terdaftar"
```

---

## 2. Kesalahan Docker

> Docker bersifat **opsional**. Hal ini hanya berlaku jika Docker Desktop terinstal dan ekstensi mencoba membangun secara lokal.

### 2.1 Docker daemon tidak berjalan

**Perbaikan:** Mulai Docker Desktop → tunggu status "running" → verifikasi dengan `docker info` → coba lagi.

### 2.2 Build gagal karena ketergantungan

**Perbaikan:** Periksa ejaan `requirements.txt`, uji secara lokal terlebih dahulu: `pip install -r requirements.txt`.

### 2.3 Ketidakcocokan platform (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Kesalahan otentikasi

### 3.1 `DefaultAzureCredential` gagal

**Perbaikan (coba sesuai urutan):**
1. `az login` (otentikasi ulang)
2. `az account set --subscription "<id>"` (langganan yang benar)
3. VS Code → Akun → Keluar → Masuk lagi
4. Verifikasi: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Token berfungsi secara lokal tetapi tidak dihosting

**Harapan:** Agen yang dihosting menggunakan identitas yang dikelola sistem, bukan kredensial Anda. Jika agen yang dihosting mendapat kesalahan otentikasi:
- Verifikasi `AZURE_AI_PROJECT_ENDPOINT` di `agent.yaml` benar
- Periksa bahwa identitas terkelola proyek memiliki akses model

---

## 4. Kesalahan model

### 4.1 Penyebaran model tidak ditemukan

**Perbaikan:** Nama bersifat **case-sensitive**. Bandingkan `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` dengan nama persis di sidebar Foundry → Models.

### 4.2 Output model tidak terduga

**Perbaikan:** Tinjau `AGENT_INSTRUCTIONS` di `main.py` (tidak terpotong?). Coba model lain (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. Kesalahan penyebaran

### 5.1 Penarikan ACR tidak diizinkan

**Perbaikan:** Azure Portal → Container Registry → Access control (IAM) → Tambahkan peran **AcrPull** ke identitas terkelola proyek Foundry.

### 5.2 Agen gagal mulai (tetap "Pending" atau "Failed")

Periksa log kontainer di sidebar. Penyebab umum:

| Pesan log | Perbaikan |
|-------------|-----|
| `ModuleNotFoundError` | Tambahkan paket yang hilang ke `requirements.txt`, deploy ulang |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | Tambahkan variabel lingkungan ke `agent.yaml` di bawah `environment_variables` |
| `Address already in use` | Pastikan hanya satu proses yang mengikat ke port 8088 |

### 5.3 Penyebaran waktu habis

**Perbaikan:** Periksa koneksi internet. Penyebaran pertama mengirimkan >100MB. Apakah di belakang proxy? Konfigurasikan pengaturan proxy Docker Desktop.

---

## 6. Jalur B - Foundry Lokal

### 6.1 Foundry Lokal tidak mau mulai

| Masalah | Perbaikan |
|-------|-----|
| `foundry: command not found` | Pasang ulang: `winget install Microsoft.FoundryLocal` |
| Sumber daya tidak cukup | Foundry Lokal butuh ~4GB RAM kosong. Tutup aplikasi lain. |
| Unduh model gagal | Periksa ruang disk (model 2–8 GB). Coba lagi: `foundry local models pull <name>` |

### 6.2 Kesalahan model Foundry Lokal

| Masalah | Perbaikan |
|-------|-----|
| Respon lambat | Diharapkan - model lokal berjalan di CPU kecuali jika Anda memiliki GPU. Bersabar. |
| Output kualitas rendah | Coba model yang lebih besar jika perangkat keras Anda memungkinkan. `phi-4-mini` adalah keseimbangan yang baik. |
| Koneksi ditolak | Verifikasi Foundry Lokal berjalan: `foundry local status`. Mulai ulang jika perlu. |

---

## 7. Referensi cepat: peran RBAC

| Peran | Lingkup | Memberi |
|------|-------|--------|
| **Azure AI User** | Proyek | Aksi data: `agents/write`, `agents/read` |
| **Azure AI Developer** | Proyek/Akun | Aksi data + pembuatan proyek |
| **Azure AI Owner** | Akun | Akses penuh + manajemen peran |
| **Contributor** | Langganan/RG | Hanya aksi manajemen (**tidak** aksi data) |
| **Owner** | Langganan/RG | Manajemen + penugasan peran (**tidak** aksi data) |

---

## 8. Daftar periksa penyelesaian workshop

| # | Item | Modul |
|---|------|--------|
| 1 | Prasyarat terpasang dan diverifikasi | [00](00-prerequisites.md) |
| 2 | Ekstensi Foundry Toolkit terpasang, proyek terhubung (atau Jalur B dikonfigurasi) | [01](01-setup.md) |
| 3 | Agen yang dihosting sudah dibangun | [02](02-create-hosted-agent.md) |
| 4 | `.env` dikonfigurasi, instruksi ditulis, dependensi terpasang | [03](03-configure-and-code.md) |
| 5 | Agen diuji secara lokal - 3 skenario fungsional lolos | [04](04-test-locally.md) |
| 6 | Dideploy ke Foundry (Jalur A saja) | [05](05-deploy-to-foundry.md) |
| 7 | Tes kasus tepi/keamanan lolos di cloud (Jalur A saja) | [06](06-verify-in-playground.md) |
| 8 | Ringkasan ditinjau, langkah selanjutnya diidentifikasi | [07](07-summary.md) |

---

**Sebelumnya:** [07 - Ringkasan](07-summary.md) · **Beranda:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau penafsiran yang keliru yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->