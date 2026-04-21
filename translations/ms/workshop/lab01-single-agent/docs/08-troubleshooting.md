# Modul 8 - Penyelesaian Masalah

Modul ini adalah panduan rujukan untuk setiap isu biasa yang dihadapi semasa bengkel. Tandakan ia - anda akan kembali kepadanya setiap kali sesuatu tidak berjalan lancar.

---

## 1. Ralat kebenaran

### 1.1 Kebenaran `agents/write` ditolak

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Punca utama:** Anda tidak mempunyai peranan `Azure AI User` di peringkat **projek**. Ini adalah ralat yang paling biasa dalam bengkel.

**Pembetulan - langkah demi langkah:**

1. Buka [https://portal.azure.com](https://portal.azure.com).
2. Dalam bar carian di atas, taip nama **projek Foundry** anda (contohnya, `workshop-agents`).
3. **Penting:** Klik hasil yang menunjukkan jenis **"Microsoft Foundry project"**, BUKAN akaun/hub induk. Ini adalah sumber berbeza dengan skop RBAC berbeza.
4. Di navigasi kiri halaman projek, klik **Access control (IAM)**.
5. Klik tab **Role assignments** untuk memeriksa jika anda sudah mempunyai peranan:
   - Cari nama atau emel anda.
   - Jika `Azure AI User` sudah disenaraikan → ralat ini disebabkan oleh hal lain (semak Langkah 8 di bawah).
   - Jika tidak disenaraikan → teruskan untuk menambahnya.
6. Klik **+ Add** → **Add role assignment**.
7. Dalam tab **Role**:
   - Cari [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles).
   - Pilih dari hasil carian.
   - Klik **Next**.
8. Dalam tab **Members**:
   - Pilih **User, group, or service principal**.
   - Klik **+ Select members**.
   - Cari nama atau alamat emel anda.
   - Pilih diri anda dari hasil carian.
   - Klik **Select**.
9. Klik **Review + assign** → sekali lagi **Review + assign**.
10. **Tunggu 1-2 minit** - perubahan RBAC mengambil masa untuk disebarkan.
11. Cuba semula operasi yang gagal.

> **Kenapa Owner/Contributor tidak mencukupi:** Azure RBAC mempunyai dua jenis kebenaran - *tindakan pengurusan* dan *tindakan data*. Owner dan Contributor memberikan tindakan pengurusan (mencipta sumber, sunting tetapan), tetapi operasi agen memerlukan tindakan data `agents/write`, yang hanya termasuk dalam peranan `Azure AI User`, `Azure AI Developer`, atau `Azure AI Owner`. Lihat [dokumentasi Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 `AuthorizationFailed` semasa penyediaan sumber

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Punca utama:** Anda tiada kebenaran untuk mencipta atau mengubah sumber Azure dalam langganan/kumpulan sumber ini.

**Pembetulan:**
1. Minta pentadbir langganan anda memberikan peranan **Contributor** pada kumpulan sumber tempat projek Foundry anda berada.
2. Alternatifnya, minta mereka mencipta projek Foundry untuk anda dan berikan anda peranan **Azure AI User** pada projek itu.

### 1.3 `SubscriptionNotRegistered` untuk [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Punca utama:** Langganan Azure belum mendaftar penyedia sumber yang diperlukan untuk Foundry.

**Pembetulan:**

1. Buka terminal dan jalankan:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Tunggu pendaftaran selesai (boleh ambil masa 1-5 minit):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Output dijangka: `"Registered"`
3. Cuba semula operasi.

---

## 2. Ralat Docker (hanya jika Docker dipasang)

> Docker adalah **pilihan** untuk bengkel ini. Ralat ini hanya berlaku jika anda memasang Docker Desktop dan sambungan Foundry cuba membina kontena secara tempatan.

### 2.1 Docker daemon tidak berjalan

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Pembetulan - langkah demi langkah:**

1. **Cari Docker Desktop** dalam menu Mula anda (Windows) atau Aplikasi (macOS) dan lancarkannya.
2. Tunggu tetingkap Docker Desktop memaparkan **"Docker Desktop is running"** - biasanya mengambil masa 30-60 saat.
3. Cari ikon ikan paus Docker dalam dulang sistem anda (Windows) atau bar menu (macOS). Letakkan kursor atasnya untuk mengesahkan status.
4. Sahkan dalam terminal:
   ```powershell
   docker info
   ```
   Jika ini mencetak maklumat sistem Docker (Versi Server, Pemandu Penyimpanan, dll.), Docker sedang berjalan.
5. **Khas Windows:** Jika Docker masih tidak boleh mula:
   - Buka Docker Desktop → **Settings** (ikon gear) → **General**.
   - Pastikan **Use the WSL 2 based engine** ditandakan.
   - Klik **Apply & restart**.
   - Jika WSL 2 belum dipasang, jalankan `wsl --install` dalam PowerShell yang dinaik taraf dan mulakan semula komputer anda.
6. Cuba semula penyebaran.

### 2.2 Docker build gagal dengan ralat pergantungan

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Pembetulan:**
1. Buka `requirements.txt` dan pastikan semua nama pakej dieja dengan betul.
2. Pastikan penetapan versi adalah betul:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Uji pemasangan secara tempatan dahulu:
   ```bash
   pip install -r requirements.txt
   ```
4. Jika menggunakan indeks pakej peribadi, pastikan Docker mempunyai akses rangkaian kepadanya.

### 2.3 Ketidakpadanan platform kontena (Apple Silicon)

Jika menyebar dari Mac Apple Silicon (M1/M2/M3/M4), kontena mesti dibina untuk `linux/amd64` kerana persekitaran kontena Foundry menggunakan AMD64.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Perintah penyebaran sambungan Foundry mengendalikan secara automatik dalam kebanyakan kes. Jika anda melihat ralat berkaitan seni bina, bina secara manual dengan bendera `--platform` dan hubungi pasukan Foundry.

---

## 3. Ralat pengesahan

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) gagal mendapatkan token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Punca utama:** Tiada sumber kredensial dalam rantai `DefaultAzureCredential` yang mempunyai token yang sah.

**Pembetulan - cuba setiap langkah mengikut urutan:**

1. **Masuk semula melalui Azure CLI** (pembetulan paling biasa):
   ```bash
   az login
   ```
   Tetingkap pelayar terbuka. Log masuk, kemudian kembali ke VS Code.

2. **Tetapkan langganan yang betul:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Jika ini bukan langganan yang betul:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **Masuk semula melalui VS Code:**
   - Klik ikon **Accounts** (ikon orang) di bawah kiri VS Code.
   - Klik nama akaun anda → **Sign Out**.
   - Klik ikon Akaun sekali lagi → **Sign in to Microsoft**.
   - Selesaikan aliran masuk pelayar.

4. **Service principal (hanya senario CI/CD):**
   - Tetapkan pembolehubah persekitaran ini dalam `.env` anda:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Kemudian mulakan semula proses agen anda.

5. **Periksa cache token:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Jika gagal, token CLI anda telah tamat tempoh. Jalankan `az login` semula.

### 3.2 Token berfungsi secara tempatan tetapi tidak dalam penyebaran dihoskan

**Punca utama:** Agen dihoskan menggunakan identiti yang dikendalikan sistem, yang berbeza daripada kredensial peribadi anda.

**Pembetulan:** Ini adalah tingkah laku yang dijangka - identiti yang dikendalikan disediakan secara automatik semasa penyebaran. Jika agen dihoskan masih mendapat ralat pengesahan:
1. Pastikan identiti yang dikendalikan projek Foundry mempunyai akses ke sumber Azure OpenAI.
2. Sahkan `PROJECT_ENDPOINT` dalam `agent.yaml` adalah betul.

---

## 4. Ralat model

### 4.1 Penempatan model tidak ditemui

```
Error: Model deployment not found / The specified deployment does not exist
```

**Pembetulan - langkah demi langkah:**

1. Buka fail `.env` anda dan catat nilai `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
2. Buka bar sisi **Microsoft Foundry** dalam VS Code.
3. Kembangkan projek anda → **Model Deployments**.
4. Bandingkan nama penempatan yang disenaraikan dengan nilai `.env` anda.
5. Nama adalah **sensasitif huruf** - `gpt-4o` berbeza daripada `GPT-4o`.
6. Jika tidak sama, kemas kini `.env` anda untuk menggunakan nama tepat yang dipaparkan di bar sisi.
7. Untuk penyebaran dihoskan, juga kemas kini `agent.yaml`:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model memberi respons dengan kandungan tidak dijangka

**Pembetulan:**
1. Semak nilai `EXECUTIVE_AGENT_INSTRUCTIONS` dalam `main.py`. Pastikan ia tidak dipotong atau rosak.
2. Periksa tetapan suhu model (jika boleh dikonfigurasikan) - nilai rendah memberi output yang lebih deterministik.
3. Bandingkan model yang dikerahkan (contoh, `gpt-4o` vs `gpt-4o-mini`) - model berbeza ada keupayaan berbeza.

---

## 5. Ralat penyebaran

### 5.1 Kebenaran tarik ACR

```
Error: AcrPullUnauthorized
```

**Punca utama:** Identiti yang dikendalikan projek Foundry tidak boleh menarik imej kontena dari Azure Container Registry.

**Pembetulan - langkah demi langkah:**

1. Buka [https://portal.azure.com](https://portal.azure.com).
2. Cari **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** di bar carian atas.
3. Klik registri yang berkaitan dengan projek Foundry anda (biasanya dalam kumpulan sumber yang sama).
4. Di navigasi kiri, klik **Access control (IAM)**.
5. Klik **+ Add** → **Add role assignment**.
6. Cari peranan **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** dan pilih. Klik **Next**.
7. Pilih **Managed identity** → klik **+ Select members**.
8. Cari dan pilih identiti yang dikendalikan projek Foundry.
9. Klik **Select** → **Review + assign** → **Review + assign**.

> Penetapan peranan ini biasanya disediakan secara automatik oleh sambungan Foundry. Jika anda melihat ralat ini, penyediaan automatik mungkin gagal. Anda juga boleh cuba menyebarkan semula - sambungan mungkin mencuba semula penyediaan.

### 5.2 Agen gagal mula selepas penyebaran

**Gejala:** Status kontena kekal "Pending" lebih 5 minit atau menunjukkan "Failed".

**Pembetulan - langkah demi langkah:**

1. Buka bar sisi **Microsoft Foundry** dalam VS Code.
2. Klik pada agen dihoskan anda → pilih versi.
3. Dalam panel butiran, periksa **Container Details** → cari bahagian atau pautan **Logs**.
4. Baca log permulaan kontena. Punca biasa:

| Mesej log | Punca | Pembetulan |
|-------------|-------|-------------|
| `ModuleNotFoundError: No module named 'xxx'` | Pergantungan hilang | Tambah ke `requirements.txt` dan sebarkan semula |
| `KeyError: 'PROJECT_ENDPOINT'` | Pembolehubah persekitaran hilang | Tambah pembolehubah env ke `agent.yaml` di bawah `env:` |
| `OSError: [Errno 98] Address already in use` | Konflik port | Pastikan `agent.yaml` ada `port: 8088` dan hanya satu proses ikat ke port itu |
| `ConnectionRefusedError` | Agen tidak mula mendengar | Semak `main.py` - panggilan `from_agent_framework()` mesti dijalankan semasa permulaan |

5. Betulkan isu tersebut, kemudian sebarkan semula dari [Modul 6](06-deploy-to-foundry.md).

### 5.3 Masa penyebaran tamat

**Pembetulan:**
1. Periksa sambungan internet anda - push Docker boleh jadi besar (>100MB untuk penyebaran pertama).
2. Jika di belakang proksi korporat, pastikan tetapan proksi Docker Desktop dikonfigurasikan: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Cuba semula - gangguan rangkaian boleh menyebabkan kegagalan sementara.

---

## 6. Rujukan pantas: peranan RBAC

| Peranan | Skop biasa | Apa yang diberi |
|------|---------------|----------------|
| **Azure AI User** | Projek | Tindakan data: bina, sebarkan, dan panggil agen (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Projek atau Akaun | Tindakan data + penciptaan projek |
| **Azure AI Owner** | Akaun | Akses penuh + pengurusan penetapan peranan |
| **Azure AI Project Manager** | Projek | Tindakan data + boleh menetapkan Azure AI User kepada orang lain |
| **Contributor** | Langganan/RG | Tindakan pengurusan (buat/hapus sumber). **Tidak termasuk tindakan data** |
| **Owner** | Langganan/RG | Tindakan pengurusan + penetapan peranan. **Tidak termasuk tindakan data** |
| **Reader** | Mana-mana | Akses pengurusan baca sahaja |

> **Amaran utama:** `Owner` dan `Contributor` tidak termasuk tindakan data. Anda sentiasa memerlukan peranan `Azure AI *` untuk operasi agen. Peranan minimum untuk bengkel ini ialah **Azure AI User** pada skop **projek**.

---

## 7. Senarai semak penyelesaian bengkel

Gunakan ini sebagai pengesahan akhir bahawa anda telah menyelesaikan semua:

| # | Item | Modul | Lulus? |
|---|------|--------|---|
| 1 | Semua prasyarat dipasang dan disahkan | [00](00-prerequisites.md) | |
| 2 | Toolkit Foundry dan sambungan Foundry dipasang | [01](01-install-foundry-toolkit.md) | |
| 3 | Projek Foundry dicipta (atau projek sedia ada dipilih) | [02](02-create-foundry-project.md) | |
| 4 | Model diterapkan (contoh, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Peranan Pengguna Azure AI ditetapkan pada skop projek | [02](02-create-foundry-project.md) | |
| 6 | Projek ejen hos dijalankan (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env` dikonfigurasikan dengan PROJECT_ENDPOINT dan MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | Arahan ejen diubah suai dalam main.py | [04](04-configure-and-code.md) | |
| 9 | Persekitaran maya dibuat dan pergantungan dipasang | [04](04-configure-and-code.md) | |
| 10 | Ejen diuji secara tempatan dengan F5 atau terminal (4 ujian asap lulus) | [05](05-test-locally.md) | |
| 11 | Diterapkan ke Foundry Agent Service | [06](06-deploy-to-foundry.md) | |
| 12 | Status kontena menunjukkan "Bermula" atau "Berjalan" | [06](06-deploy-to-foundry.md) | |
| 13 | Disahkan dalam VS Code Playground (4 ujian asap lulus) | [07](07-verify-in-playground.md) | |
| 14 | Disahkan dalam Foundry Portal Playground (4 ujian asap lulus) | [07](07-verify-in-playground.md) | |

> **Tahniah!** Jika semua item telah ditandakan, anda telah menyelesaikan keseluruhan bengkel. Anda telah membina ejen hos dari awal, mengujinya secara tempatan, menerapkannya ke Microsoft Foundry, dan mengesahkannya dalam produksi.

---

**Sebelumnya:** [07 - Sahkan di Playground](07-verify-in-playground.md) · **Utama:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan profesional oleh manusia adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->