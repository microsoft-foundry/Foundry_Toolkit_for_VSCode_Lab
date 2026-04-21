# Modül 8 - Sorun Giderme (Çoklu Ajan)

Bu modül çoklu ajan iş akışına özgü yaygın hataları, çözümleri ve hata ayıklama stratejilerini kapsar. Genel Foundry dağıtım sorunları için ayrıca [Lab 01 sorun giderme kılavuzuna](../../lab01-single-agent/docs/08-troubleshooting.md) bakınız.

---

## Hızlı başvuru: Hata → Çözüm

| Hata / Belirti | Muhtemel Neden | Çözüm |
|----------------|----------------|-------|
| `RuntimeError: Missing required environment variable(s)` | `.env` dosyası yok veya değerler ayarlanmamış | `PROJECT_ENDPOINT=<your-endpoint>` ve `MODEL_DEPLOYMENT_NAME=<your-model>` içeren `.env` oluşturun |
| `ModuleNotFoundError: No module named 'agent_framework'` | Sanal ortam etkin değil veya bağımlılıklar yüklenmemiş | `.\.venv\Scripts\Activate.ps1` çalıştırın sonra `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | MCP paketi kurulu değil (requirements’de eksik) | `pip install mcp` çalıştırın veya `requirements.txt` içinde transitif bağımlılık olarak ekli olduğundan emin olun |
| Ajan başlatılıyor ama boş yanıt dönüyor | `output_executors` uyumsuz veya eksik bağlantılar | `output_executors=[gap_analyzer]` ve tüm kenarların `create_workflow()` içinde var olduğunu kontrol edin |
| Sadece 1 gap kartı var (diğerleri eksik) | GapAnalyzer talimatları eksik | `GAP_ANALYZER_INSTRUCTIONS` içine `CRITICAL:` paragrafını ekleyin - bkz. [Modül 3](03-configure-agents.md) |
| Uyum skoru 0 ya da yok | MatchingAgent yukarı akış verisi almadı | Hem `add_edge(resume_parser, matching_agent)` hem de `add_edge(jd_agent, matching_agent)` var mı kontrol edin |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP sunucusu araç çağrısını reddetti | İnternet bağlantısını kontrol edin. `https://learn.microsoft.com/api/mcp` adresini tarayıcıda açmayı deneyin. Tekrar deneyin |
| Çıktıda Microsoft Learn URL’si yok | MCP aracı kayıtlı değil veya uç nokta yanlış | GapAnalyzer’da `tools=[search_microsoft_learn_for_plan]` ve `MICROSOFT_LEARN_MCP_ENDPOINT` doğru olduğundan emin olun |
| `Address already in use: port 8088` | Başka bir işlem 8088 portunu kullanıyor | Windows için `netstat -ano \| findstr :8088`, macOS/Linux için `lsof -i :8088` çalıştırıp çakışan işlemi durdurun |
| `Address already in use: port 5679` | Debugpy port çakışması | Diğer debug oturumlarını durdurun. `netstat -ano \| findstr :5679` ile işlemi bulun ve kapatın |
| Agent Inspector açılmıyor | Sunucu tam başlamadı veya port çakışması | "Server running" günlük mesajını bekleyin. 5679 portunun boş olduğundan emin olun |
| `azure.identity.CredentialUnavailableError` | Azure CLI ile giriş yapılmamış | `az login` komutunu çalıştırıp sunucuyu yeniden başlatın |
| `azure.core.exceptions.ResourceNotFoundError` | Model dağıtımı yok | `MODEL_DEPLOYMENT_NAME` değerinin Foundry projenizde dağıtılmış bir modelle eşleştiğini kontrol edin |
| Dağıtım sonrası "Failed" durumda konteyner | Konteyner başlatılırken çökme | Foundry kenar çubuğundaki konteyner loglarını kontrol edin. Yaygın: eksik ortam değişkeni veya import hatası |
| Dağıtım 5 dakikadan fazla "Pending" gösteriyor | Konteyner başlatması uzun sürüyor veya kaynak sınırı var | Çoklu ajan 4 ajanın başlatılması nedeniyle uzayabilir. Yine de bekleniyorsa logları kontrol edin |
| `ValueError` from `WorkflowBuilder` | Geçersiz grafik konfigürasyonu | `start_executor` ayarlı, `output_executors` liste ve döngüsel kenar yok olduğundan emin olun |

---

## Ortam ve konfigürasyon sorunları

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

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **PROJECT_ENDPOINT nasıl bulunur:**  
- VS Code’da **Microsoft Foundry** yan menüsünü açın → projenize sağ tıklayın → **Copy Project Endpoint** seçin.  
- Ya da [Azure Portal](https://portal.azure.com)’a gidin → Foundry projeniz → **Overview** → **Project endpoint**.

> **MODEL_DEPLOYMENT_NAME nasıl bulunur:** Foundry yan menüsünde projenizi genişletin → **Models** → dağıtılmış model adınızı bulun (örneğin `gpt-4.1-mini`).

### Ortam değişkeni öncelik sırası

`main.py` dosyası `load_dotenv(override=False)` kullanır, yani:

| Öncelik | Kaynak | İkisi ayarlıysa hangisi geçerli? |
|---------|--------|----------------------------------|
| 1 (en yüksek) | Kabuk ortam değişkeni | Evet |
| 2 | `.env` dosyası | Kabuk değişkeni yoksa geçerli |

Bu, hosted dağıtımda Foundry çalışma zamanı ortam değişkenlerinin (`agent.yaml` ile ayarlanan) `.env` değerlerinden öncelikli olduğu anlamına gelir.

---

## Versiyon uyumluluğu

### Paket sürüm matrisi

Çoklu ajan iş akışı belirli paket sürümleri gerektirir. Uyuşmayan sürümler çalışma zamanı hatalarına yol açar.

| Paket | Gereken Sürüm | Kontrol Komutu |
|-------|---------------|----------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | en son pre-release | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### Yaygın sürüm hataları

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# Düzeltme: rc3'e yükseltme
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` bulunamadı veya Inspector uyumsuz:**

```powershell
# Düzeltme: --pre bayrağı ile yükleyin
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# Düzeltme: mcp paketini güncelleyin
pip install mcp --upgrade
```

### Tüm sürümleri bir kerede doğrulama

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

Beklenen çıktı:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCP araç sorunları

### MCP aracı sonuç döndürmüyor

**Belirti:** Gap kartları "Microsoft Learn MCP'den sonuç dönmedi" veya "Doğrudan Microsoft Learn sonucu bulunamadı" diyor.

**Olası nedenler:**

1. **Ağ sorunu** - MCP uç noktası (`https://learn.microsoft.com/api/mcp`) erişilemez durumda.  
   ```powershell
   # Bağlantıyı test et
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   Eğer bu `200` dönerse, uç nokta ulaşılabilir demektir.

2. **Sorgu çok spesifik** - Beceri adı Microsoft Learn araması için çok niş.  
   - Çok uzmanlaşmış becerilerde bu beklenen bir durumdur. Araç yanıtında bir yedek URL vardır.

3. **MCP oturum zaman aşımı** - Streamable HTTP bağlantısı zaman aşımına uğradı.  
   - İsteği yeniden deneyin. MCP oturumları geçicidir ve yeniden bağlanması gerekebilir.

### MCP logları açıklaması

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| Log | Anlamı | Yapılması Gereken |
|-----|---------|-------------------|
| `GET → 405` | MCP istemcisi başlatma sırasında deneme yapıyor | Normal – yok sayın |
| `POST → 200` | Araç çağrısı başarılı | Beklenen sonuç |
| `DELETE → 405` | MCP istemcisi temizleme sırasında deneme yapıyor | Normal – yok sayın |
| `POST → 400` | Hatalı istek (geçersiz sorgu) | `search_microsoft_learn_for_plan()` içindeki `query` parametresini inceleyin |
| `POST → 429` | Oran sınırlaması | Bekleyin ve yeniden deneyin. `max_results` parametresini azaltın |
| `POST → 500` | MCP sunucu hatası | Geçici – tekrar deneyin. Sürekli olursa Microsoft Learn MCP API kapalı olabilir |
| Bağlantı zaman aşımı | Ağ sorunu veya MCP sunucusu kullanılamıyor | İnterneti kontrol edin. `curl https://learn.microsoft.com/api/mcp` deneyin |

---

## Dağıtım sorunları

### Konteyner dağıtımdan sonra başlamıyor

1. **Konteyner loglarını kontrol edin:**  
   - **Microsoft Foundry** yan menüsünü açın → **Hosted Agents (Preview)** genişletin → ajanın üzerine tıklayın → sürümü genişletin → **Container Details** → **Logs**.  
   - Python yığın izleri veya eksik modül hatalarına bakın.

2. **Yaygın konteyner başlangıç hataları:**

   | Log'daki Hata | Neden | Çözüm |
   |---------------|-------|-------|
   | `ModuleNotFoundError` | `requirements.txt` paket eksik | Paketi ekleyin ve yeniden dağıtın |
   | `RuntimeError: Missing required environment variable` | `agent.yaml` ortam değişkenleri ayarlanmamış | `agent.yaml` → `environment_variables` bölümünü güncelleyin |
   | `azure.identity.CredentialUnavailableError` | Managed Identity yapılandırılmamış | Foundry otomatik ayarlar – uzantıdan dağıttığınızdan emin olun |
   | `OSError: port 8088 already in use` | Dockerfile yanlış port açıyor veya port çakışması | Dockerfile'da `EXPOSE 8088` ve `CMD ["python", "main.py"]` doğru mu kontrol edin |
   | Konteyner 1 koduyla çıkıyor | `main()` içinde işlenmemiş istisna | Önce yerelde test edin ([Modül 5](05-test-locally.md)) hataları yakalamak için |

3. **Düzeltmeden sonra yeniden dağıtım:**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → aynı ajanı seç → yeni sürümü dağıt.

### Dağıtım çok uzun sürüyor

Çoklu ajan konteynerleri başlatıldığında 4 ajan örneği oluşturur, bu yüzden başlangıç süresi daha uzundur. Normal beklentiler:

| Aşama | Tahmini Süre |
|-------|--------------|
| Konteyner imaj derleme | 1-3 dakika |
| İmajın ACR’ye yüklenmesi | 30-60 saniye |
| Konteyner başlatma (tek ajan) | 15-30 saniye |
| Konteyner başlatma (çoklu ajan) | 30-120 saniye |
| Playground’da ajan kullanıma hazır | "Started" sonrası 1-2 dakika |

> "Pending" durumu 5 dakikadan uzun sürüyorsa konteyner loglarını kontrol edin.

---

## RBAC ve izin sorunları

### `403 Forbidden` veya `AuthorizationFailed`

Foundry projenizde **[Azure AI User](https://aka.ms/foundry-ext-project-role)** rolüne ihtiyacınız var:

1. [Azure Portal](https://portal.azure.com) → Foundry **proje** kaynağınıza gidin.  
2. **Access control (IAM)** → **Role assignments** tıklayın.  
3. İsminizi arayın → **Azure AI User** listede olsun.  
4. Eksikse: **Add** → **Add role assignment** → **Azure AI User** arayın → hesabınıza atayın.

Detaylar için [Microsoft Foundry’de RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) dokümantasyonuna bakın.

### Model dağıtımına erişilemiyor

Ajan model ile ilgili hatalar veriyorsa:

1. Modelin dağıtılmış olduğunu doğrulayın: Foundry yan menüsü → projeyi açın → **Models** → `gpt-4.1-mini` (veya sizin model) etiketli ve **Succeeded** durumda model var mı bakın.  
2. Dağıtım adı doğru mu kontrol edin: `.env` (veya `agent.yaml`) içindeki `MODEL_DEPLOYMENT_NAME` ile yan menüdeki gerçek dağıtım ismi eşleşmeli.  
3. Dağıtım süresi dolduysa (ücretsiz katman): [Model Kataloğu](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) üzerinden yeniden dağıtın (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**).

---

## Agent Inspector sorunları

### Inspector açılıyor ama "Disconnected" gösteriyor

1. Sunucunun çalıştığını doğrulayın: Terminalde "Server running on http://localhost:8088" mesajı var mı kontrol edin.  
2. 5679 portunu kontrol edin: Inspector debugpy üzerinden 5679 portuna bağlanır.  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. Sunucuyu yeniden başlatıp Inspector’u tekrar açın.

### Inspector kısmi yanıt gösteriyor

Çoklu ajan yanıtları uzun ve akış halinde gelir. Tüm yanıt tamamlanana kadar bekleyin (gap kart sayısı ve MCP araç çağrılarına bağlı olarak 30-60 saniye sürebilir).

Yanıt sürekli kesiliyorsa:  
- GapAnalyzer talimatlarında gap kartların birleşmesini önleyen `CRITICAL:` bloğu var mı kontrol edin.  
- Model token sınırınızı kontrol edin - `gpt-4.1-mini` çıkış için 32K token destekler, bu yeterli olmalı.

---

## Performans ipuçları

### Yavaş yanıtlar

Çoklu ajan iş akışları, ardışık bağımlılıklar ve MCP araç çağrıları nedeniyle doğal olarak tek ajanlardan daha yavaştır.

| Optimizasyon | Nasıl | Etki |
|--------------|-------|-------|
| MCP çağrılarını azalt | Araçta `max_results` parametresini düşürün | Daha az HTTP turu |
| Talimatları sadeleştir | Daha kısa ve odaklı ajan istemleri hazırlayın | Daha hızlı LLM çıkarımı |
| `gpt-4.1-mini` kullan | Geliştirme için `gpt-4.1`'den daha hızlı | Yaklaşık 2 kat hız artışı |
| Gap kart detayını azalt | GapAnalyzer talimatlarında kart formatını basitleştirin | Daha az çıktı üretimi |

### Tipik yanıt süreleri (yerel)

| Konfigürasyon | Beklenen süre |
|---------------|---------------|
| `gpt-4.1-mini`, 3-5 gap kartı | 30-60 saniye |
| `gpt-4.1-mini`, 8+ gap kartı | 60-120 saniye |
| `gpt-4.1`, 3-5 gap kartı | 60-120 saniye |
---

## Yardım alma

Yukarıdaki düzeltmeleri denedikten sonra takılırsanız:

1. **Sunucu günlüklerini kontrol edin** - Çoğu hata terminalde Python yığını izini üretir. Tam traceback'i okuyun.
2. **Hata mesajını arayın** - Hata metnini kopyalayıp [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services) içinde arama yapın.
3. **Bir sorun açın** - Aşağıdakilerle [workshop deposunda](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) bir issue oluşturun:
   - Hata mesajı veya ekran görüntüsü
   - Paket sürümleriniz (`pip list | Select-String "agent-framework"`)
   - Python sürümünüz (`python --version`)
   - Sorunun yerel mi yoksa dağıtımdan sonra mı olduğu

---

### Kontrol listesi

- [ ] En yaygın çoklu ajan hatalarını hızlı başvuru tablosunu kullanarak tanımlayıp düzeltebiliyorsunuz
- [ ] `.env` yapılandırma sorunlarını nasıl kontrol edip düzelteceğinizi biliyorsunuz
- [ ] Paket sürümlerinin gereken matrisle eşleştiğini doğrulayabiliyorsunuz
- [ ] MCP günlük girişlerini anlıyor ve araç arızalarını teşhis edebiliyorsunuz
- [ ] Dağıtım hataları için konteyner günlüklerini nasıl kontrol edeceğinizi biliyorsunuz
- [ ] Azure Portal’da RBAC rollerini doğrulayabiliyorsunuz

---

**Önceki:** [07 - Verify in Playground](07-verify-in-playground.md) · **Ana Sayfa:** [Lab 02 README](../README.md) · [Workshop Ana Sayfa](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:  
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hatalar veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belge, kendi ana dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi tavsiye edilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalar veya yanlış yorumlardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->