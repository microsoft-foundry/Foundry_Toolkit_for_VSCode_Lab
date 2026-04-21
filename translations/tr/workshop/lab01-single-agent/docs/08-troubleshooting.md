# Modül 8 - Sorun Giderme

Bu modül, atölye sırasında karşılaşılan her yaygın sorun için bir başvuru rehberidir. Yer işareti olarak kaydedin - bir şeyler ters gittiğinde tekrar kullanacaksınız.

---

## 1. İzin hataları

### 1.1 `agents/write` izni reddedildi

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**Temel neden:** **proje** düzeyinde `Azure AI User` rolünüz yok. Bu atölyedeki en yaygın hatadır.

**Adım adım çözüm:**

1. [https://portal.azure.com](https://portal.azure.com) adresini açın.
2. Üst arama çubuğuna **Foundry projenizin** adını yazın (ör. `workshop-agents`).
3. **Önemli:** Türü **"Microsoft Foundry project"** olan sonucu tıklayın, ana hesap/hub kaynağını değil. Bunlar farklı RBAC kapsamlarına sahip farklı kaynaklardır.
4. Proje sayfasının sol gezinti çubuğunda **Access control (IAM)**'ı tıklayın.
5. Rol atamalarını kontrol etmek için **Role assignments** sekmesini tıklayın:
   - Adınızı veya e-postanızı arayın.
   - Eğer `Azure AI User` zaten listelenmişse → hata başka bir nedenden kaynaklanıyor (aşağıdaki 8. adıma bakın).
   - Listelenmemişse → eklemeye devam edin.
6. **+ Add** → **Add role assignment** tıklayın.
7. **Role** sekmesinde:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) arayın.
   - Sonuçlardan seçin.
   - **Next** tıklayın.
8. **Members** sekmesinde:
   - **User, group, or service principal** seçin.
   - **+ Select members** tıklayın.
   - Adınızı veya e-posta adresinizi arayın.
   - Sonuçlardan kendinizi seçin.
   - **Select** tıklayın.
9. **Review + assign** → tekrar **Review + assign** tıklayın.
10. **1-2 dakika bekleyin** - RBAC değişikliklerinin yayılması zaman alır.
11. Başarısız olan işlemi yeniden deneyin.

> **Neden Owner/Contributor yeterli değildir:** Azure RBAC iki tür izin içerir - *yönetim işlemleri* ve *veri işlemleri*. Owner ve Contributor yönetim işlemlerine (kaynak oluşturma, ayar düzenleme) izin verir, ancak agent işlemleri `agents/write` **veri işlemi** gerektirir; bu izin sadece `Azure AI User`, `Azure AI Developer` veya `Azure AI Owner` rollerinde vardır. Bkz. [Foundry RBAC dokümanı](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 Kaynak sağlama sırasında `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**Temel neden:** Bu abonelik/kaynak grubunda Azure kaynakları oluşturma veya değiştirme izniniz yok.

**Çözüm:**
1. Abonelik yöneticinizden Foundry projenizin bulunduğu kaynak grubunda size **Contributor** rolü atamasını isteyin.
2. Alternatif olarak, projeyi onlar sizin için oluştursun ve size projede **Azure AI User** rolü versin.

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) için `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**Temel neden:** Azure aboneliği Foundry için gerekli kaynak sağlayıcıyı kaydetmedi.

**Çözüm:**

1. Bir terminal açın ve çalıştırın:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. Kaydın tamamlanmasını bekleyin (1-5 dakika sürebilir):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   Beklenen çıktı: `"Registered"`
3. İşlemi yeniden deneyin.

---

## 2. Docker hataları (yalnızca Docker yüklüyse)

> Docker bu atölye için **isteğe bağlıdır**. Bu hatalar yalnızca Docker Desktop yüklüyse ve Foundry eklentisi yerel bir konteyner oluşturmayı deniyorsa geçerlidir.

### 2.1 Docker daemon çalışmıyor

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**Adım adım çözüm:**

1. Başlat menünüzde (Windows) veya Uygulamalar klasöründe (macOS) **Docker Desktop**'ı bulun ve açın.
2. Docker Desktop penceresinde **"Docker Desktop is running"** mesajını bekleyin - genellikle 30-60 saniye sürer.
3. Sistem tepsisinde (Windows) veya menü çubuğunda (macOS) balina simgesini bulun. Üzerine gelerek durumunu doğrulayın.
4. Bir terminal açın ve doğrulayın:
   ```powershell
   docker info
   ```
   Eğer Docker sistem bilgisi (Sunucu Versiyonu, Depolama Sürücüsü vb.) yazdırılırsa, Docker çalışıyor demektir.
5. **Windows’a özgü:** Docker hala başlamıyorsa:
   - Docker Desktop → **Settings** (dişli ikonu) → **General**.
   - **Use the WSL 2 based engine** seçeneğinin işaretli olduğundan emin olun.
   - **Apply & restart** tıklayın.
   - WSL 2 yüklü değilse, yükseltilmiş PowerShell’de `wsl --install` komutunu çalıştırın ve bilgisayarınızı yeniden başlatın.
6. Dağıtımı yeniden deneyin.

### 2.2 Docker derleme bağımlılık hataları

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**Çözüm:**
1. `requirements.txt` dosyasını açın ve tüm paket adlarının doğru yazıldığını kontrol edin.
2. Sürüm sabitlemenin doğru olduğundan emin olun:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. Önce yerelde kurulumu test edin:
   ```bash
   pip install -r requirements.txt
   ```
4. Özel bir paket indeksinde çalışıyorsanız, Docker’ın buna ağ erişimine sahip olduğundan emin olun.

### 2.3 Konteyner platform uyuşmazlığı (Apple Silicon)

Apple Silicon Mac (M1/M2/M3/M4) üzerinden dağıtım yapıyorsanız, konteyner `linux/amd64` için oluşturulmalıdır çünkü Foundry konteyner çalışma zamanı AMD64 kullanır.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry eklentisinin dağıtım komutu çoğu durumda bunu otomatik olarak halleder. Mimariden kaynaklanan hatalar görürseniz, `--platform` bayrağı ile manuel oluşturun ve Foundry ekibiyle iletişime geçin.

---

## 3. Kimlik doğrulama hataları

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) token alamıyor

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Temel neden:** `DefaultAzureCredential` zincirindeki hiçbir kimlik bilgisi geçerli token içermiyor.

**Çözüm - her adımı sırayla deneyin:**

1. **Azure CLI ile tekrar giriş yapın** (en yaygın çözüm):
   ```bash
   az login
   ```
   Bir tarayıcı penceresi açılır. Oturum açın, sonra VS Code’a geri dönün.

2. **Doğru aboneliği seçin:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   Bu doğru abonelik değilse:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code üzerinden tekrar giriş yapın:**
   - VS Code’un sol altındaki **Accounts** simgesini (insan simgesi) tıklayın.
   - Hesap adınıza tıklayın → **Çıkış Yap**.
   - Tekrar Accounts simgesine tıklayın → **Microsoft hesabıyla giriş yap**.
   - Tarayıcıdan oturum açma işlemini tamamlayın.

4. **Servis princial (yalnızca CI/CD senaryoları):**
   - `.env` dosyanıza şu ortam değişkenlerini ekleyin:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - Ardından agent işleminizi yeniden başlatın.

5. **Token önbelleğini kontrol edin:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   Bu başarısız olursa, CLI token’ınız süresi dolmuştur. Yeniden `az login` çalıştırın.

### 3.2 Token yerelde çalışıyor, barındırılan dağıtımda çalışmıyor

**Temel neden:** Barındırılan agent sistem yönetimli bir kimlik kullanır, bu da kişisel kimliğinizden farklıdır.

**Çözüm:** Bu beklenen davranıştır - yönetilen kimlik dağıtım sırasında otomatik olarak oluşturulur. Barındırılan agent hala kimlik doğrulama hatası alıyorsa:
1. Foundry projesinin yönetilen kimliğinin Azure OpenAI kaynağına erişimi olduğundan emin olun.
2. `agent.yaml` içindeki `PROJECT_ENDPOINT` değerinin doğru olduğunu doğrulayın.

---

## 4. Model hataları

### 4.1 Model dağıtımı bulunamadı

```
Error: Model deployment not found / The specified deployment does not exist
```

**Adım adım çözüm:**

1. `.env` dosyanızı açın ve `AZURE_AI_MODEL_DEPLOYMENT_NAME` değerini not edin.
2. VS Code’da **Microsoft Foundry** kenar çubuğunu açın.
3. Projenizi genişletin → **Model Deployments**.
4. Oradaki dağıtım adı ile `.env` değerini karşılaştırın.
5. İsim **büyük/küçük harfe duyarlıdır** - `gpt-4o` ile `GPT-4o` farklıdır.
6. Eşleşmiyorsa, `.env` dosyanızdaki adı kenar çubuğunda görünen tam isimle güncelleyin.
7. Barındırılan dağıtım için ayrıca `agent.yaml` dosyasını da güncelleyin:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 Model beklenmedik içerikle yanıt veriyor

**Çözüm:**
1. `main.py` içindeki `EXECUTIVE_AGENT_INSTRUCTIONS` sabitini gözden geçirin. Kesildiği veya bozulduğu olmadığından emin olun.
2. Model sıcaklık ayarını kontrol edin (ayar varsa) - daha düşük değerler daha belirgin çıktılar verir.
3. Dağıtılan modeli karşılaştırın (örneğin `gpt-4o` ile `gpt-4o-mini`) - farklı modeller farklı yeteneklere sahiptir.

---

## 5. Dağıtım hataları

### 5.1 ACR çekme yetkilendirmesi

```
Error: AcrPullUnauthorized
```

**Temel neden:** Foundry projesinin yönetilen kimliği konteyner imajını Azure Container Registry’den çekemiyor.

**Adım adım çözüm:**

1. [https://portal.azure.com](https://portal.azure.com) adresini açın.
2. Üst arama çubuğuna **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** yazın.
3. Foundry projenize bağlı kayıt defterini tıklayın (genellikle aynı kaynak grubundadır).
4. Sol gezintide **Access control (IAM)** tıklayın.
5. **+ Add** → **Add role assignment** tıklayın.
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** rolünü arayın ve seçin. **Next** tıklayın.
7. **Managed identity** seçin → **+ Select members** tıklayın.
8. Foundry projesinin yönetilen kimliğini bulun ve seçin.
9. **Select** → **Review + assign** → **Review + assign** tıklayın.

> Bu rol ataması genellikle Foundry eklentisi tarafından otomatik yapılır. Bu hatayı görüyorsanız, otomatik kurulum başarısız olmuş olabilir. Yeniden dağıtım deneyebilirsiniz - eklenti kurulumu tekrar deneyebilir.

### 5.2 Agent dağıtımdan sonra başlamıyor

**Belirtiler:** Konteyner durumu 5 dakikadan uzun "Pending" şeklinde kalıyor veya "Failed" gösteriyor.

**Adım adım çözüm:**

1. VS Code’da **Microsoft Foundry** kenar çubuğunu açın.
2. Barındırılan agent’ınızı seçin → sürümünü seçin.
3. Detay panelinde **Container Details** → **Logs** bölümü veya bağlantısını kontrol edin.
4. Konteyner başlangıç loglarını okuyun. Yaygın nedenler:

| Log mesajı | Neden | Çözüm |
|-------------|-------|-------|
| `ModuleNotFoundError: No module named 'xxx'` | Eksik bağımlılık | `requirements.txt`'ye ekleyin ve yeniden dağıtın |
| `KeyError: 'PROJECT_ENDPOINT'` | Eksik ortam değişkeni | `agent.yaml` dosyasındaki `env:` altına ekleyin |
| `OSError: [Errno 98] Address already in use` | Port çatışması | `agent.yaml` dosyasında `port: 8088` olduğundan ve sadece bir sürecin bu portu kullandığından emin olun |
| `ConnectionRefusedError` | Agent dinleme başlatmadı | `main.py`'de `from_agent_framework()` çağrısı başlangıçta çalıştırılmalı |

5. Sorunu düzeltin, ardından [Modül 6](06-deploy-to-foundry.md) üzerinden yeniden dağıtım yapın.

### 5.3 Dağıtım zaman aşımı

**Çözüm:**
1. İnternet bağlantınızı kontrol edin - Docker push işlemi büyük (>100MB ilk dağıtım için) olabilir.
2. Kurumsal proxy arkasındaysanız, Docker Desktop proxy ayarlarının yapıldığından emin olun: **Docker Desktop** → **Settings** → **Resources** → **Proxies**.
3. Tekrar deneyin - ağ kesintileri geçici hatalara neden olabilir.

---

## 6. Hızlı referans: RBAC roller

| Rol | Tipik kapsam | Sağladığı izinler |
|------|-------------|-------------------|
| **Azure AI User** | Proje | Veri işlemleri: agent oluşturma, dağıtma, çağırma (`agents/write`, `agents/read`) |
| **Azure AI Developer** | Proje veya Hesap | Veri işlemleri + proje oluşturma |
| **Azure AI Owner** | Hesap | Tam erişim + rol ataması yönetimi |
| **Azure AI Project Manager** | Proje | Veri işlemleri + başkalarına Azure AI User atayabilir |
| **Contributor** | Abonelik/Kaynak Grubu | Yönetim işlemleri (kaynak oluşturma/silme). **Veri işlemleri içermez** |
| **Owner** | Abonelik/Kaynak Grubu | Yönetim işlemleri + rol ataması. **Veri işlemleri içermez** |
| **Reader** | Herhangi | Yalnızca yönetim erişimi okuma |

> **Ana not:** `Owner` ve `Contributor` veri işlemlerini içermez. Agent işlemleri için her zaman bir `Azure AI *` rolü gerekir. Bu atölye için minimum rol **Azure AI User** ve kapsam **proje** düzeyindedir.

---

## 7. Atölye tamamlama kontrol listesi

Her şeyi tamamladığınıza dair son kontrol için kullanın:

| # | Öğeler | Modül | Geçti? |
|---|---------|-------|--------|
| 1 | Tüm önkoşullar yüklendi ve doğrulandı | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit ve Foundry eklentileri yüklendi | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry projesi oluşturuldu (veya mevcut proje seçildi) | [02](02-create-foundry-project.md) | |
| 4 | Model dağıtıldı (örneğin, gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | Proje kapsamındaki Azure AI Kullanıcı rolü atandı | [02](02-create-foundry-project.md) | |
| 6 | Barındırılan ajan projesi hazırlandı (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env`, PROJECT_ENDPOINT ve MODEL_DEPLOYMENT_NAME ile yapılandırıldı | [04](04-configure-and-code.md) | |
| 8 | Agent talimatları main.py içinde özelleştirildi | [04](04-configure-and-code.md) | |
| 9 | Sanal ortam oluşturuldu ve bağımlılıklar yüklendi | [04](04-configure-and-code.md) | |
| 10 | Agent yerel olarak F5 veya terminal ile test edildi (4 adet temel testi geçti) | [05](05-test-locally.md) | |
| 11 | Foundry Agent Hizmetine dağıtıldı | [06](06-deploy-to-foundry.md) | |
| 12 | Konteyner durumu "Başlatıldı" veya "Çalışıyor" olarak görünüyor | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground'da doğrulandı (4 adet temel testi geçti) | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground'da doğrulandı (4 adet temel testi geçti) | [07](07-verify-in-playground.md) | |

> **Tebrikler!** Tüm maddeler işaretlendi ise, tüm atölyeyi tamamladınız. Baştan sona bir barındırılan ajan inşa ettiniz, yerel olarak test ettiniz, Microsoft Foundry'e dağıttınız ve üretimde doğruladınız.

---

**Önceki:** [07 - Playground'da Doğrulama](07-verify-in-playground.md) · **Anasayfa:** [Atölye README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri servisi [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hata veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belge, kendi doğal dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucunda ortaya çıkan yanlış anlamalar veya yorumlar için sorumluluk kabul edilmez.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->