# Modül 8 - Sorun Giderme

Bu modül, çoklu ajan iş akışına özgü yaygın hatalar, düzeltmeler ve hata ayıklama stratejilerini kapsar.

## Ajan çıktı problemleri

### GapAnalyzer "Hâlâ eşleşen rapor elimde yok" diyor

**Belirti:** GapAnalyzer’ın yanıtı, “Eksik Beceriler” ve “Sertifika Boşlukları” ile bir eşleşen rapor yapıştırmanızı ister. Bu, hem özgeçmiş hem de iş tanımı gönderdiğinizde bile olur.

**Neden:** JD metni JD Ajanına aşağı akışta geçmemiştir. `context_mode="last_agent"` ile `resume_executor` kullanıcının orijinal mesajını gören tek işlemdir. Eğer `RESUME_PARSER_INSTRUCTIONS` çıktısında JD metni yoksa, JD Ajanının ayrıştıracak bir JD’si olmaz, MatchingAgent uyum puanı hesaplayamaz ve GapAnalyzer anlamsız bir giriş alır.

**Teşhis:**

Sunucu kayıtlarında MatchingAgent span’ını arayın. İçinde:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
geçiş eksik veya bozuk demektir.

**Düzeltme:** `main.py` dosyasındaki `RESUME_PARSER_INSTRUCTIONS` içinde `[JOB DESCRIPTION PASS-THROUGH]` bölümü ve şu kuralla olduğundan emin olun:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
Ayrıca `JOB_DESCRIPTION_INSTRUCTIONS` içinde `[PARSED RESUME PASS-THROUGH]` geçiş kuralı olduğundan emin olun:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
Eğer herhangi bir kural bloğu iskelet sihirbazdan alınmışsa, onu [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) dosyasından tam haliyle değiştirin.

### MatchingAgent "Uygunluk puanı hesaplanamıyor - JD sağlanmadı" çıktısı veriyor

Bu, yukarıdaki ile aynı temel nedendir. MatchingAgent JD Ajanının çıktısını aldı ama `[PARSED RESUME PASS-THROUGH]` bölümü yoktu veya boştu, bu yüzden iki profili karşılaştıramadı. Şunları doğrulayın:
1. `JOB_DESCRIPTION_INSTRUCTIONS` içinde geçiş kuralı: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.` yer alıyor.
2. `MATCHING_AGENT_INSTRUCTIONS` ajanı `[JD REQUIREMENTS]` ve `[PARSED RESUME PASS-THROUGH]` bölümlerini araması için talimat verir.

Her iki talimat bloğunu da [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) dosyasından tam sürümlerle değiştirin.

### Yanıt iki kez görünüyor

**Belirti:** GapAnalyzer çıktısı (ya da tüm boru hattı çıktısı) Ajan Denetleyici yanıtında iki kez görünüyor.

**Neden:** `WorkflowBuilder` gelen kenarlar için VEYA semantiği kullanır - aşağıdaki işlemci herhangi bir öncül tamamlanır tamamlanmaz tetiklenir. Eğer `matching_executor`’ın iki gelen kenarı varsa (biri `resume_executor`’dan, biri `jd_executor`’dan), iki kez çalışır: birinci kez ResumeParser bitince, ikinci kez JD Ajanı bitince. GapAnalyzer da iki kez çalışır.

**Düzeltme:** `WorkflowBuilder` grafiğinin kesinlikle sıralı bir boru hattı olup fan-in olmamasını sağlayın:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor'dan DEĞİLDİR
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

Eğer fazladan `.add_edge(resume_executor, matching_executor)` satırı varsa, silin. JD Ajanının çıktısındaki `[PARSED RESUME PASS-THROUGH]` Relay zaten MatchingAgent’a özgeçmiş erişimi sağlar.

---

## Ortam ve yapılandırma sorunları

### Eksik veya yanlış `.env` değerleri

`.env` dosyası `PersonalCareerCopilot/` dizininde olmalıdır (`main.py` ile aynı seviyede):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

Beklenen `.env` içeriği:

**Yol A - Foundry bulut:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**Yol B - Foundry Yerel:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> Her iki yol `FOUNDRY_PROJECT_ENDPOINT` kullanır. Değer farklıdır: bulutta `https://` Foundry uç noktası; yerelde `http://localhost:5273/v1`. Yol B için kesin model takma adını doğrulamak için `foundry model list` komutunu çalıştırın.

> **`FOUNDRY_PROJECT_ENDPOINT` nasıl bulunur:** 
- VS Code’da **Foundry Toolkit** yan panelini açın → projenize sağ tıklayın → **Copy Project Endpoint**.
- Ya da [Azure Portal](https://portal.azure.com) → Foundry projeniz → **Genel Bakış** → **Project endpoint**.

> **`AZURE_AI_MODEL_DEPLOYMENT_NAME` nasıl bulunur:** Foundry Toolkit yan panelinde projenizi genişletin → **Models** → dağıtılmış model adınızı bulun (örneğin `gpt-4.1-mini`).

### Çevresel değişken önceliği

`main.py` `load_dotenv(override=True)` kullanır, bu:

| Öncelik | Kaynak | Her ikisi ayarlıysa hangisi geçer? |
|----------|--------|------------------------------|
| 1 (en yüksek) | `.env` dosyası | Evet |
| 2 | Kabuk / konteyner ortam değişkeni | `.env` içinde aynı anahtar yoksa kullanılır |

Yerelde geliştirmede `.env` gerçek kaynak olur (dosya düzenleme anında etkiler). Hosted dağıtımda Foundry ortam değişkenlerini konteyner seviyesinde enjekte eder; bu lab yapılandırmasında `.env` imajın parçası olmadığından konteyner içi değer kullanılır.

---

## Sürüm uyumluluğu

### Paket sürüm matrisi

Çoklu ajan iş akışı belirli paket sürümleri gerektirir. Uyumsuz sürümler çalışma zamanı hatalarına yol açar.

| Paket | Gerekli Sürüm | Kontrol Komutu |
|---------|-----------------|---------------|
| `agent-framework-foundry` | en güncel | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | en güncel | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | en güncel | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### Yaygın sürüm hataları

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Düzeltme: agent-framework-foundry yeniden yükleyin
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Düzeltme: mcp paketini yükselt
pip install mcp --upgrade
```

### Tüm sürümleri aynı anda doğrulama

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

Beklenen çıktı:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## Dağıtım sorunları

### Konteyner dağıtımdan sonra başlamıyor

1. **Konteyner günlüklerini kontrol edin:**
   - **Foundry Toolkit** yan panelini açın → **Hosted Agents (Preview)**’i genişletin → ajanınıza tıklayın → sürümü genişletin → **Container Details** → **Logs**.
   - Python yığın izlerini veya eksik modül hatalarını arayın.

2. **Yaygın konteyner başlangıç hataları:**

   | Günlüklerdeki Hata | Neden | Çözüm |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` eksik paket içeriyor | Paketi ekleyin, dağıtımı tekrar yapın |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` veya `.env` ortam değişkenleri ayarlanmadı | `agent.yaml` içindeki `environment_variables` bölümü (hosted) veya `.env` (yerel) güncelleyin |
   | `azure.identity.CredentialUnavailableError` | Yönetilen Kimlik yapılandırılmamış | Foundry bunu otomatik yapar - uzantı üzerinden dağıttığınızdan emin olun |
   | `OSError: port 8088 already in use` | Dockerfile yanlış port açıyor veya port çakışması var | Dockerfile’da `EXPOSE 8088` ve `CMD ["python", "main.py"]` doğrulayın |
   | Konteyner kod 1 ile çıkıyor | `main()`’de yakalanmamış istisna var | Önce yerelde test edin ([Modül 5](05-test-locally.md)) hataları dağıtmadan bulun |

3. **Düzeltmeden sonra yeniden dağıtın:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → aynı ajanı seçin → yeni sürüm dağıtın.

### Dağıtım çok uzun sürüyor

Çoklu ajan konteynerleri, başlangıçta 4 ajan örneği oluşturdukları için daha uzun başlar. Normal başlangıç süreleri:

| Aşama | Beklenen süre |
|-------|------------------|
| Konteyner imajı oluşturma | 1-3 dakika |
| İmajın ACR’ye gönderilmesi | 30-60 saniye |
| Konteyner başlatma (tek ajan) | 15-30 saniye |
| Konteyner başlatma (çoklu ajan) | 30-120 saniye |
| Playground’da ajan kullanılabilir | "Başlatıldı"dan 1-2 dakika sonra |

> "Beklemede" durumu 5 dakikadan uzun sürerse, konteyner günlüklerini hata için kontrol edin.

---

## RBAC ve izin sorunları

### `403 Forbidden` veya `AuthorizationFailed`

Foundry projenizde **[Foundry User](https://aka.ms/foundry-ext-project-role)** rolüne ihtiyacınız var (önceden **Azure AI User** olarak adlandırılırdı - rol ID değişmedi):

1. [Azure Portal](https://portal.azure.com) → Foundry **projeniz** kaynağına gidin.
2. **Erişim kontrolü (IAM)** → **Rol atamaları**’na tıklayın.
3. Adınızı arayın → **Foundry User** (veya eski adıyla **Azure AI User**) listede var mı kontrol edin.
4. Yoksa: **Ekle** → **Rol ataması ekle** → **Foundry User** arayın → hesabınıza atayın.

Ayrıntılar için [Microsoft Foundry için RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokümantasyonuna bakın.

### Model dağıtımı erişilemez

Eğer ajan model ile ilgili hatalar veriyorsa:

1. Modelin dağıtıldığını doğrulayın: Foundry yan paneli → projenizi genişletin → **Models** → durum **Succeeded** olan `gpt-4.1-mini` (veya modeliniz) var mı kontrol edin.
2. Dağıtım adı eşleşiyor mu kontrol edin: `.env` (veya `agent.yaml`) içindeki `AZURE_AI_MODEL_DEPLOYMENT_NAME` ile yan paneldeki gerçek dağıtım adını karşılaştırın.
3. Dağıtım süresi dolduysa (ücretsiz katman): [Model Kataloğu](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) üzerinden yeniden dağıtın (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Yerel sorunları (Yol B)

### Foundry Yerel servisi çalışmıyor

```powershell
# Durumu kontrol et
foundry local status

# Hizmet durduysa başlat
foundry local start
```

| Belirti | Neden | Çözüm |
|---------|-------|-----|
| Sağlık kontrolü `503` döndürüyor | Servis başlatılmadı | `foundry local start` komutunu çalıştırın veya Foundry Toolkit yan panelinde **Start** düğmesine tıklayın |
| Sağlık kontrolü zaman aşımına uğruyor | Model hâlâ yükleniyor | Başlatmadan sonra 30-60 saniye bekleyin; büyük modeller daha uzun sürer |
| `/v1/health` çağrısında `StatusCode: 404` | Yanlış port | Varsayılan `5273`. Gerçek port için `foundry local status` komutunu kontrol edin |
| Yetersiz kaynaklar | Foundry Local yaklaşık 4 GB RAM boş alan ister | Diğer uygulamaları kapatın |
| Model indirilemiyor | Disk alanı yetersiz | Modeller 2-8 GB boyutunda. Alan açın, sonra `foundry model pull <name>` komutunu kullanın |

### Model adı uyuşmazlığı

```powershell
# İndirilen modelleri ve bunların tam takma adlarını listele
foundry model list
```

`.env` içindeki `AZURE_AI_MODEL_DEPLOYMENT_NAME` değerini tam gösterilen takma ada göre ayarlayın (örneğin `phi-4-mini`, `Phi-4-mini` değil).

### Yerel çalıştırmada `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (Yol B)

Lab’ın `main.py` dosyası `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` kullanır. Foundry Local bu değişkenin yerel servise işaret etmesini ister - **AZURE_AI_PROJECT_ENDPOINT değil**. `.env` dosyanızda şunlar olmalı:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP aracı yine dışa çağrı yapıyor (Yol B)

Bu beklenen bir durumdur. `search_microsoft_learn_for_plan` aracı `https://learn.microsoft.com/api/mcp` adresinden öğrenim kaynaklarını getirir. **Sadece beceri adı sorgusu** ağ üzerinden gider - özgeçmiş ve iş tanımı metni cihazınızda tamamen işlenir ve asla gönderilmez. Tam çevrimdışı çalışma gerekiyorsa, aracın içine uç noktaya ulaşılamadığında statik bir `learn.microsoft.com` URL’si döndüren bir `try/except` yedekleme ekleyin.

---

## Yardım alma

Yukarıdaki düzeltmeleri denedikten sonra takıldıysanız:

1. **Sunucu günlüklerini kontrol edin** - Çoğu hata terminalde Python yığın izlemesi verir. Tüm geri izlemeyi okuyun.
2. **Hata mesajında arama yapın** - Hata metnini kopyalayıp [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) içinde arama yapın.
3. **Bir sorun açın** - [Çalıştay deposunda](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) bir sorun dosyası oluşturun:
   - Hata mesajı veya ekran görüntüsü
   - Paket sürümleriniz (`pip list | Select-String "agent-framework"`)
   - Python sürümünüz (`python --version`)
   - Sorunun yerelde mi yoksa dağıtımdan sonra mı olduğu

---

### Kontrol noktası

- [ ] `.env` yapılandırma sorunlarını kontrol edip düzeltebiliyorsunuz
- [ ] Paket sürümlerinin gerekli matrise uyduğunu doğrulayabiliyorsunuz
- [ ] Konteyner günlüklerini dağıtım hataları için kontrol etmeyi biliyorsunuz
- [ ] Azure Portal’da RBAC rollerini doğrulayabiliyorsunuz

---

**Önceki:** [07 - Playground’da Doğrulama](07-verify-in-playground.md) · **Sonraki:** [09 - Özet →](09-summary.md) · **Ana Sayfa:** [Lab 02 README](../README.md) · [Çalıştay Anasayfa](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->