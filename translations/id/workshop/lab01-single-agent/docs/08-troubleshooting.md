# Modul 8 - Pemecahan Masalah

Modul ini adalah panduan referensi untuk setiap masalah umum yang ditemui selama lokakarya. Tandai halaman ini - Anda akan kembali ke sini setiap kali ada yang salah.

---

## 1. Kesalahan izin

### 1.1 Izin `agents/write` ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```
  
**Penyebab utama:** Anda tidak memiliki peran `Azure AI User` di tingkat **proyek**. Ini adalah kesalahan paling umum di lokakarya.

**Perbaikan - langkah demi langkah:**

1. Buka [https://portal.azure.com](https://portal.azure.com).  
2. Di bilah pencarian atas, ketik nama **proyek Foundry** Anda (misalnya, `workshop-agents`).  
3. **Kritis:** Klik hasil yang menunjukkan tipe **"Microsoft Foundry project"**, BUKAN sumber daya akun/hub induk. Ini adalah sumber daya berbeda dengan cakupan RBAC yang berbeda.  
4. Di navigasi kiri halaman proyek, klik **Access control (IAM)**.  
5. Klik tab **Role assignments** untuk memeriksa apakah Anda sudah memiliki peran:  
   - Cari nama atau email Anda.  
   - Jika `Azure AI User` sudah terdaftar → kesalahan disebabkan oleh hal lain (periksa Langkah 8 di bawah).  
   - Jika tidak terdaftar → lanjutkan untuk menambahkannya.  
6. Klik **+ Add** → **Add role assignment**.  
7. Di tab **Role**:  
   - Cari [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).  
   - Pilih dari hasil pencarian.  
   - Klik **Next**.  
8. Di tab **Members**:  
   - Pilih **User, group, or service principal**.  
   - Klik **+ Select members**.  
   - Cari nama atau alamat email Anda.  
   - Pilih diri Anda dari hasil.  
   - Klik **Select**.  
9. Klik **Review + assign** → **Review + assign** lagi.  
10. **Tunggu 1-2 menit** - perubahan RBAC membutuhkan waktu untuk dipropagasi.  
11. Coba ulang operasi yang gagal.

> **Mengapa Owner/Contributor tidak cukup:** Azure RBAC memiliki dua jenis izin - *tindakan manajemen* dan *tindakan data*. Owner dan Contributor memberikan tindakan manajemen (membuat sumber daya, mengedit pengaturan), tetapi operasi agen memerlukan **tindakan data** `agents/write`, yang hanya termasuk dalam peran `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Lihat [dokumentasi Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` saat penyediaan sumber daya

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```
  
**Penyebab utama:** Anda tidak memiliki izin untuk membuat atau memodifikasi sumber daya Azure dalam langganan/grup sumber daya ini.

**Perbaikan:**  
1. Minta administrator langganan Anda untuk memberi Anda peran **Contributor** pada grup sumber daya tempat proyek Foundry Anda berada.  
2. Atau, minta mereka membuat proyek Foundry untuk Anda dan memberi Anda **Azure AI User** pada proyek tersebut.

### 1.3 `SubscriptionNotRegistered` untuk [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```
  
**Penyebab utama:** Langganan Azure belum mendaftarkan penyedia sumber daya yang diperlukan untuk Foundry.

**Perbaikan:**

1. Buka terminal dan jalankan:  
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
  
2. Tunggu hingga pendaftaran selesai (bisa memakan waktu 1-5 menit):  
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
  
   Output yang diharapkan: `"Registered"`  
3. Coba ulang operasi.

---

## 2. Kesalahan Docker (hanya jika Docker terpasang)

> Docker adalah **opsional** untuk lokakarya ini. Kesalahan ini hanya berlaku jika Anda memasang Docker Desktop dan ekstensi Foundry mencoba membangun container secara lokal.

### 2.1 Docker daemon tidak berjalan

```
Error: Docker build failed / Cannot connect to Docker daemon
```
  
**Perbaikan - langkah demi langkah:**

1. **Cari Docker Desktop** di menu Start Anda (Windows) atau Aplikasi (macOS) dan jalankan aplikasinya.  
2. Tunggu hingga jendela Docker Desktop menampilkan **"Docker Desktop is running"** - ini biasanya memakan waktu 30-60 detik.  
3. Cari ikon paus Docker di baki sistem (Windows) atau bilah menu (macOS). Arahkan kursor untuk memastikan statusnya.  
4. Verifikasi di terminal:  
   ```powershell
   docker info
   ```
  
   Jika ini mencetak informasi sistem Docker (Server Version, Storage Driver, dll.), Docker sudah berjalan.  
5. **Khusus Windows:** Jika Docker masih tidak mau mulai:  
   - Buka Docker Desktop → **Settings** (ikon gir) → **General**.  
   - Pastikan **Use the WSL 2 based engine** dicentang.  
   - Klik **Apply & restart**.  
   - Jika WSL 2 belum terpasang, jalankan `wsl --install` di PowerShell yang dijalankan sebagai administrator dan restart komputer Anda.  
6. Coba ulang penerapan.

### 2.2 Docker build gagal dengan kesalahan dependensi

```
Error: pip install failed / Could not find a version that satisfies the requirement
```
  
**Perbaikan:**  
1. Buka `requirements.txt` dan pastikan semua nama paket sudah benar ejaannya.  
2. Pastikan versi yang dipasang sudah sesuai:  
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
  
3. Uji pemasangan secara lokal terlebih dahulu:  
   ```bash
   pip install -r requirements.txt
   ```
  
4. Jika menggunakan indeks paket privat, pastikan Docker memiliki akses jaringan ke sana.

### 2.3 Ketidaksesuaian platform container (Apple Silicon)

Jika melakukan deploy dari Mac Apple Silicon (M1/M2/M3/M4), container harus dibangun untuk `linux/amd64` karena runtime container Foundry menggunakan AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```
  
> Perintah deploy ekstensi Foundry biasanya menangani ini secara otomatis dalam kebanyakan kasus. Jika Anda melihat kesalahan terkait arsitektur, bangun manual dengan flag `--platform` dan hubungi tim Foundry.

---

## 3. Kesalahan autentikasi

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) gagal mengambil token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```
  
**Penyebab utama:** Tidak ada sumber kredensial dalam rantai `DefaultAzureCredential` yang memiliki token yang valid.

**Perbaikan - coba setiap langkah secara berurutan:**

1. **Login ulang melalui Azure CLI** (perbaikan paling umum):  
   ```bash
   az login
   ```
  
   Sebuah jendela browser akan terbuka. Masuk, lalu kembali ke VS Code.

2. **Setel langganan yang benar:**  
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
  
   Jika ini bukan langganan yang tepat:  
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```
  
3. **Login ulang melalui VS Code:**  
   - Klik ikon **Accounts** (ikon orang) di kiri bawah VS Code.  
   - Klik nama akun Anda → **Sign Out**.  
   - Klik ikon Accounts lagi → **Sign in to Microsoft**.  
   - Selesaikan alur masuk di browser.

4. **Service principal (hanya untuk skenario CI/CD):**  
   - Atur variabel lingkungan ini dalam `.env` Anda:  
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
  
   - Lalu restart proses agen Anda.

5. **Periksa cache token:**  
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
  
   Jika ini gagal, token CLI Anda sudah kedaluwarsa. Jalankan `az login` lagi.

### 3.2 Token berhasil secara lokal tapi gagal di deploy yang dihosting

**Penyebab utama:** Agen yang dihosting menggunakan identitas terkelola sistem, yang berbeda dengan kredensial pribadi Anda.

**Perbaikan:** Ini adalah perilaku yang diharapkan - identitas terkelola dibuat secara otomatis saat deployment. Jika agen yang dihosting masih mendapat kesalahan autentikasi:  
1. Pastikan identitas terkelola proyek Foundry memiliki akses ke sumber daya Azure OpenAI.  
2. Verifikasi `PROJECT_ENDPOINT` di `agent.yaml` sudah benar.

---

## 4. Kesalahan model

### 4.1 Deployment model tidak ditemukan

```
Error: Model deployment not found / The specified deployment does not exist
```
  
**Perbaikan - langkah demi langkah:**

1. Buka file `.env` Anda dan catat nilai `AZURE_AI_MODEL_DEPLOYMENT_NAME`.  
2. Buka panel samping **Microsoft Foundry** di VS Code.  
3. Perluas proyek Anda → **Model Deployments**.  
4. Bandingkan nama deployment yang terdaftar dengan nilai `.env` Anda.  
5. Nama bersifat **case-sensitive** - `gpt-4o` berbeda dengan `GPT-4o`.  
6. Jika tidak cocok, perbarui `.env` Anda dengan nama yang tepat seperti yang ditampilkan di panel samping.  
7. Untuk deployment yang dihosting, juga perbarui `agent.yaml`:  
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```


### 4.2 Model merespons dengan konten yang tidak diharapkan

**Perbaikan:**  
1. Tinjau konstanta `EXECUTIVE_AGENT_INSTRUCTIONS` di `main.py`. Pastikan tidak terpotong atau rusak.  
2. Periksa pengaturan suhu model (jika dapat dikonfigurasi) - nilai yang lebih rendah memberikan output yang lebih deterministik.  
3. Bandingkan model yang dideploy (misalnya, `gpt-4o` vs `gpt-4o-mini`) - model berbeda memiliki kemampuan berbeda.

---

## 5. Kesalahan deployment

### 5.1 Otorisasi tarik ACR

```
Error: AcrPullUnauthorized
```
  
**Penyebab utama:** Identitas terkelola proyek Foundry tidak dapat menarik image container dari Azure Container Registry.

**Perbaikan - langkah demi langkah:**

1. Buka [https://portal.azure.com](https://portal.azure.com).  
2. Cari **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** di bilah pencarian atas.  
3. Klik pada registry yang terkait dengan proyek Foundry Anda (biasanya dalam grup sumber daya yang sama).  
4. Di navigasi kiri, klik **Access control (IAM)**.  
5. Klik **+ Add** → **Add role assignment**.  
6. Cari **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** dan pilih. Klik **Next**.  
7. Pilih **Managed identity** → klik **+ Select members**.  
8. Temukan dan pilih identitas terkelola proyek Foundry.  
9. Klik **Select** → **Review + assign** → **Review + assign**.

> Penugasan peran ini biasanya diatur otomatis oleh ekstensi Foundry. Jika Anda melihat kesalahan ini, pengaturan otomatis mungkin gagal. Anda juga dapat mencoba redeploy - ekstensi bisa mencoba ulang pengaturan.

### 5.2 Agen gagal mulai setelah deployment

**Gejala:** Status container tetap "Pending" lebih dari 5 menit atau menunjukkan "Failed".

**Perbaikan - langkah demi langkah:**

1. Buka panel samping **Microsoft Foundry** di VS Code.  
2. Klik pada agen yang dihosting → pilih versinya.  
3. Di panel detail, periksa **Container Details** → cari bagian atau tautan **Logs**.  
4. Baca log startup container. Penyebab umum:

| Pesan Log | Penyebab | Perbaikan |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | Dependensi hilang | Tambahkan ke `requirements.txt` dan redeploy |
| `KeyError: 'PROJECT_ENDPOINT'` | Variabel lingkungan hilang | Tambahkan env var ke `agent.yaml` di bawah `env:` |
| `OSError: [Errno 98] Address already in use` | Konflik port | Pastikan `agent.yaml` memiliki `port: 8088` dan hanya satu proses yang menggunakan port tersebut |
| `ConnectionRefusedError` | Agen tidak mulai mendengarkan | Periksa `main.py` - panggilan `from_agent_framework()` harus berjalan saat startup |

5. Perbaiki masalah, lalu redeploy dari [Modul 6](06-deploy-to-foundry.md).

### 5.3 Waktu deployment habis

**Perbaikan:**  
1. Periksa koneksi internet Anda - push Docker bisa besar (>100MB untuk deploy pertama).  
2. Jika menggunakan proxy perusahaan, pastikan pengaturan proxy Docker Desktop sudah dikonfigurasi: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.  
3. Coba lagi - gangguan jaringan bisa menyebabkan kegagalan sementara.

---

## 6. Referensi cepat: peran RBAC

| Peran | Cakupan tipikal | Apa yang diberikan |
|------|-----------------|--------------------|
| **Azure AI User** | Proyek | Tindakan data: membangun, mendeploy, dan memanggil agen (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Proyek atau Akun | Tindakan data + pembuatan proyek |
| **Azure AI Owner** | Akun | Akses penuh + manajemen penugasan peran |
| **Azure AI Project Manager** | Proyek | Tindakan data + dapat memberikan Azure AI User ke orang lain |
| **Contributor** | Langganan/Grup Sumber Daya | Tindakan manajemen (buat/hapus sumber daya). **TIDAK termasuk tindakan data** |
| **Owner** | Langganan/Grup Sumber Daya | Tindakan manajemen + penugasan peran. **TIDAK termasuk tindakan data** |
| **Reader** | Mana saja | Akses manajemen hanya baca |

> **Poin penting:** `Owner` dan `Contributor` **TIDAK** termasuk tindakan data. Anda selalu memerlukan peran `Azure AI *` untuk operasi agen. Peran minimum untuk lokakarya ini adalah **Azure AI User** di cakupan **proyek**.

---

## 7. Daftar periksa penyelesaian lokakarya

Gunakan ini sebagai tanda akhir bahwa Anda telah menyelesaikan semuanya:

| # | Item | Modul | Lulus? |
|---|------|--------|-------|
| 1 | Semua prasyarat terpasang dan diverifikasi | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit dan ekstensi Foundry terpasang | [01](01-install-foundry-toolkit.md) | |
| 3 | Proyek Foundry dibuat (atau proyek yang sudah ada dipilih) | [02](02-create-foundry-project.md) | |
| 4 | Model sudah diterapkan (misalnya, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Peranan Pengguna Azure AI ditugaskan pada lingkup proyek | [02](02-create-foundry-project.md) | |
| 6 | Proyek agen yang dihosting telah dibuat (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` dikonfigurasi dengan PROJECT_ENDPOINT dan MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Instruksi agen disesuaikan di main.py | [04](04-configure-and-code.md) | |
| 9 | Lingkungan virtual dibuat dan dependensi diinstal | [04](04-configure-and-code.md) | |
| 10 | Agen diuji secara lokal dengan F5 atau terminal (4 tes singkat berhasil) | [05](05-test-locally.md) | |
| 11 | Diterapkan ke Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status kontainer menunjukkan "Started" atau "Running" | [06](06-deploy-to-foundry.md) | |
| 13 | Diverifikasi di VS Code Playground (4 tes singkat berhasil) | [07](07-verify-in-playground.md) | |
| 14 | Diverifikasi di Foundry Portal Playground (4 tes singkat berhasil) | [07](07-verify-in-playground.md) | |

> **Selamat!** Jika semua item telah dicentang, Anda telah menyelesaikan seluruh lokakarya. Anda telah membangun agen yang dihosting dari nol, mengujinya secara lokal, menerapkannya ke Microsoft Foundry, dan memvalidasinya di produksi.

---

**Sebelumnya:** [07 - Verifikasi di Playground](07-verify-in-playground.md) · **Beranda:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berusaha untuk akurasi, harap diingat bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau kesalahan interpretasi yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->