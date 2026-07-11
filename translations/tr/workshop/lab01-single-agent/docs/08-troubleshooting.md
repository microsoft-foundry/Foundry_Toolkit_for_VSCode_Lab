# Modül 8 - Sorun Giderme

Bu modül, yaygın sorunlar için bir referans kılavuzudur. Yer işareti koyun ve bir şeyler ters gittiğinde geri dönün.

---

## 1. İzin hataları

### 1.1 `agents/write` izni reddedildi

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**Temel neden:** **proje** düzeyinde eksik `Azure AI User` rolü. Bu en yaygın çalışma atölyesi hatasıdır.

**Çözüm:**
1. [portal.azure.com](https://portal.azure.com) sitesini açın.
2. Foundry **proje** adınızı arayın → türü **"Microsoft Foundry project"** olan sonucu tıklayın (ana hesap değil).
3. **Erişim kontrolü (IAM)** → **+ Ekle** → **Rol ataması ekle**.
4. Rol: **Azure AI User** → İleri.
5. Üyeler: Kendinizi seçin → İncele + ata → İncele + ata.
6. **1–2 dakika bekleyin** → tekrar deneyin.

> **Neden Sahip/Katkıda Bulunan yeterli değil:** Bu roller sadece *yönetim* işlemleri verir. Ajan işlemleri `agents/write` *veri işlemi* gerektirir; bu yalnızca `Azure AI User`, `Azure AI Developer` veya `Azure AI Owner` içindedir. Bakınız [Foundry RBAC belgeleri](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

### 1.2 Sağlama sırasında `AuthorizationFailed`

**Çözüm:** Yöneticinizden kaynak grubunda **Contributor** atamasını yapmasını isteyin veya projenizi onlar için oluşturup size üzerinde **Azure AI User** yetkisi versin.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# "Kayıtlı" olana kadar bekleyin
```

---

## 2. Docker hataları

> Docker **isteğe bağlıdır**. Bu hatalar yalnızca Docker Desktop yüklüyse ve eklenti yerel derleme yapmaya çalışıyorsa geçerlidir.

### 2.1 Docker daemon çalışmıyor

**Çözüm:** Docker Desktop'u başlatın → "çalışıyor" durumunu bekleyin → `docker info` ile doğrulayın → tekrar deneyin.

### 2.2 Bağımlılık hataları ile derleme başarısız olur

**Çözüm:** `requirements.txt` yazımını kontrol edin, önce yerelde test edin: `pip install -r requirements.txt`.

### 2.3 Platform uyumsuzluğu (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. Kimlik doğrulama hataları

### 3.1 `DefaultAzureCredential` başarısız olur

**Çözüm (sırayla deneyin):**
1. `az login` (yeniden kimlik doğrula)
2. `az account set --subscription "<id>"` (doğru abonelik)
3. VS Code → Hesaplar → Oturumu Kapat → Tekrar Oturum Aç
4. Doğrulayın: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 Jeton yerelde çalışıyor ama barındırmada çalışmıyor

**Beklenen:** Barındırılan ajanlar sistem yönetimli kimlik kullanır, sizin kimlik bilgileriniz değil. Barındırılan ajan kimlik doğrulama hatası alıyorsa:
- `agent.yaml` içindeki `AZURE_AI_PROJECT_ENDPOINT` doğru mu kontrol edin
- Projenin yönetimli kimliği model erişimine sahip mi kontrol edin

---

## 4. Model hataları

### 4.1 Model dağıtımı bulunamadı

**Çözüm:** İsim **büyük/küçük harfe duyarlıdır**. `.env` içindeki `AZURE_AI_MODEL_DEPLOYMENT_NAME` ile Foundry kenar çubuğundaki Models bölümündeki tam adı karşılaştırın.

### 4.2 Beklenmeyen model çıktısı

**Çözüm:** `main.py` içindeki `AGENT_INSTRUCTIONS`'ı gözden geçirin (kesiliyor mu?). Farklı bir model deneyin (`gpt-4.1` veya `gpt-4.1-mini`).

---

## 5. Dağıtım hataları

### 5.1 ACR çekme yetkisi yok

**Çözüm:** Azure Portal → Container Registry → Erişim kontrolü (IAM) → Foundry projesinin yönetimli kimliğine **AcrPull** rolü ekleyin.

### 5.2 Ajan başlatılamıyor ("Beklemede" veya "Hata"da kalıyor)

Kenar çubuğunda konteyner günlüklerini kontrol edin. Yaygın nedenler:

| Günlük mesajı | Çözüm |
|-------------|-----|
| `ModuleNotFoundError` | Eksik paketi `requirements.txt` dosyasına ekleyin, yeniden dağıtın |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | `agent.yaml` içindeki `environment_variables` altında ortam değişkeni ekleyin |
| `Address already in use` | Yalnızca bir işlem 8088 portunu kullanıyor olmalı |

### 5.3 Dağıtım zaman aşımına uğruyor

**Çözüm:** İnternet bağlantınızı kontrol edin. İlk dağıtım 100MB üzeri veri gönderir. Proxy arkasında mısınız? Docker Desktop proxy ayarlarını yapılandırın.

---

## 6. Yol B - Foundry Local

### 6.1 Foundry Local başlamıyor

| Sorun | Çözüm |
|-------|-----|
| `foundry: command not found` | Yeniden yükleyin: `winget install Microsoft.FoundryLocal` |
| Yetersiz kaynak | Foundry Local için ~4GB RAM boş olmalı. Diğer uygulamaları kapatın. |
| Model indirilemiyor | Disk alanını kontrol edin (modeller 2–8 GB arası). Tekrar deneyin: `foundry local models pull <name>` |

### 6.2 Foundry Local model hataları

| Sorun | Çözüm |
|-------|-----|
| Yavaş yanıtlar | Beklenen - yerel modeller CPU üzerinde çalışır, GPU yoksa. Sabırlı olun. |
| Düşük kaliteli çıktı | Donanımınız izin veriyorsa daha büyük model deneyin. `phi-4-mini` iyi bir dengedir. |
| Bağlantı reddedildi | Foundry Local çalışıyor mu kontrol edin: `foundry local status`. Gerekirse yeniden başlatın. |

---

## 7. Hızlı referans: RBAC rolleri

| Rol | Kapsam | Verilenler |
|------|-------|--------|
| **Azure AI User** | Proje | Veri işlemleri: `agents/write`, `agents/read` |
| **Azure AI Developer** | Proje/Hesap | Veri işlemleri + proje oluşturma |
| **Azure AI Owner** | Hesap | Tam erişim + rol yönetimi |
| **Contributor** | Abonelik/KG | Sadece yönetim işlemleri (**veri işlemi içermez**) |
| **Owner** | Abonelik/KG | Yönetim + rol atama (**veri işlemi içermez**) |

---

## 8. Atölye tamamlama kontrol listesi

| # | Madde | Modül |
|---|------|--------|
| 1 | Önkoşullar yüklendi ve doğrulandı | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit eklentisi yüklendi, proje bağlandı (veya Yol B yapılandırıldı) | [01](01-setup.md) |
| 3 | Barındırılan ajan iskeleti oluşturuldu | [02](02-create-hosted-agent.md) |
| 4 | `.env` yapılandırıldı, talimatlar yazıldı, bağımlılıklar yüklendi | [03](03-configure-and-code.md) |
| 5 | Ajan yerelde test edildi - 3 işlevsel senaryo geçti | [04](04-test-locally.md) |
| 6 | Foundry'ye dağıtıldı (sadece Yol A) | [05](05-deploy-to-foundry.md) |
| 7 | Kenar durum/ güvenlik testleri bulutta geçti (sadece Yol A) | [06](06-verify-in-playground.md) |
| 8 | Özet gözden geçirildi, sonraki adımlar belirlendi | [07](07-summary.md) |

---

**Önceki:** [07 - Özet](07-summary.md) · **Ana Sayfa:** [Atölye README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->