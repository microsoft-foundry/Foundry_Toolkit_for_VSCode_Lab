# Bu oturum nasıl sunulur

Bu oturumu sunduğunuz için teşekkürler!

Atölyeyi sunmadan önce lütfen:

1. Bu belgeyi ve içindeki tüm kaynakları tamamen okuyun.
2. Oturum sunum kaydını ve atölye baştan sona yürütmesini izleyin.
3. Her iki uygulamalı laboratuvarı kendi makinenizde **en az bir kez** baştan sona yürütün.
4. Microsoft Foundry projenizi, model dağıtımlarınızı ve kota durumunuzu doğrulayın.
5. Anlaşılmayan bir şey olursa sorumlu kişiye ulaşın.

---

## Dosya özeti

| Kaynak                      | Bağlantı                                                                             | Açıklama                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Atölye sunum dosyası           | [Atölye Dosyası](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | Bu atölye için sunum slaytları, sunucu notları ve gömülü demo videoları                     |
| Oturum sunum kaydı             | _Sorumlu tarafından sağlanacak_                                               | Atölye giriş ve slayt geçiş kaydı                                                         |
| Atölye baştan sona kaydı       | _Sorumlu tarafından sağlanacak_                                               | Her iki laboratuvarın katılımcı bakış açısıyla baştan sona kaydı                            |
| Atölye belgelendirmesi         | [Depo](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | Kaynak kod deposu, laboratuvar README dosyaları, adım adım modüller                         |
| Laboratuvar 01 - tek ajan       | [Laboratuvar 01](../workshop/lab01-single-agent/README.md)                               | Uygulamalı laboratuvar: *Executive gibi Açıkla* barındırılan ajan oluşturma, test ve dağıtım |
| Laboratuvar 02 - çok ajanlı iş akışı | [Laboratuvar 02](../workshop/lab02-multi-agent/README.md)                                | Uygulamalı laboratuvar: 4 ajanlı *Özgeçmişten İş Uyum Değerlendiricisi* iş akışı oluşturma  |
| Demo 1: Executive Agent             | [Lab01 ajan](../../../workshop/lab01-single-agent/agent)                                              | Laboratuvar 01 demo: teknik jargonları yönetici özeti haline çevirme                        |
| Demo 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | Laboratuvar 02 demo: özgeçmiş-iş uyumunu puanlayan ve öneriler üreten 4 ajanlı iş akışı     |

> **Eğitmenler için not:** Slayt dosyası ve video bağlantıları kayıtlar yayınlandıktan sonra eklenecektir. O zamana kadar en güncel dosyalar için sorumluya ([İletişim](#i̇letişim)) bildirin.

---

## Başlarken

Bu atölyede geliştiricilere AI ajanları nasıl oluşturacakları, test edecekleri ve VS Code’dan tamamen **Microsoft Foundry Agent Service**’e **Barındırılan Ajanlar** olarak nasıl dağıtacakları öğretilir; kullanılan araç **Microsoft Foundry Toolkit** eklentisidir.

Atölye slaytlar, **2 canlı demo** ve **2 uygulamalı laboratuvar** dahil olmak üzere birkaç bölüme ayrılmıştır.

### Zamanlama

#### Tam sunum (yaklaşık 2 saat)

| Zaman           | Açıklama                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | Giriş: barındırılan ajanlar, Foundry Agent Service ve araç seti      |
| 10:00 - 20:00   | Demo: Executive Agent baştan sona                                   |
| 20:00 - 60:00   | Laboratuvar 01 - tek ajan (oluşturma, yerel test, dağıtım, oyun alanı)|
| 60:00 - 110:00  | Laboratuvar 02 - çok ajanlı iş akışı (Özgeçmişten İş Uyum Değerlendiricisi) |
| 110:00 - 120:00 | Kapanış, soru-cevap ve devam eden öğrenme kaynakları               |

#### Kısa sunum (yaklaşık 75 dakika)

| Zaman          | Açıklama                                                  |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | Giriş ve genel bakış                                      |
| 10:00 - 20:00 | Demo: Executive Agent                                   |
| 20:00 - 70:00 | Sadece Laboratuvar 01 (katılımcılara Laboratuvar 02’yi kendi hızlarında yapmalarını söyleyin) |
| 70:00 - 75:00 | Kapanış ve soru-cevap                                  |

### Hazırlık

| Kaynak                       | Bağlantı                                                                                          | Açıklama                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| Atölye dokümantasyonu         | [Depo](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | Atölye dokümantasyonu ve kaynak kod                 |
| Laboratuvar 01 talimatları    | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | Uygulamalı laboratuvar: tek barındırılan ajan       |
| Laboratuvar 02 talimatları    | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | Uygulamalı laboratuvar: çok ajanlı iş akışı         |
| Ön koşullar kontrol listesi   | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | Gerekli araçlar, hesaplar ve Azure erişimi           |
| Barındırılan ajanlar hızlı başlangıç (azd) | [Öğren](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | `azd` ile barındırılan ajan dağıtımına resmi hızlı başlangıç |
| Barındırılan ajanların bölge kullanılabilirliği | [Öğren](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | Barındırılan ajanların desteklenen bölgeleri (önizleme)  |

### Eğitmen ön koşulları

Sunum yapmadan önce, aşağıdakilere sahip olduğunuzdan emin olun:

- Kaynak grupta sahiplik veya katkı sağlayıcı (Owner veya Contributor) izni olan bir **Azure aboneliği**.
- [Barındırılan ajanları destekleyen bir bölgede](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) bulunan bir **Microsoft Foundry projesine** erişim.
- Foundry projenizde **gpt-4.1** (veya **gpt-4.1-mini**) kotası.
- Aşağıdaki araçların yüklü olması:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit eklentisi](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (İsteğe bağlı)
  - Python 3.10 veya üzeri

Teslimattan önce bir kez en az [Hosted agents quickstart with `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) çalıştırarak, sorun yaşanması durumunda referans alınacak iyi durumda bir Foundry projesi, model dağıtımı ve Azure Container Registry’niz olsun.

---

## Slayt yürütme

Dosya laboratuvarlarla aynı akışı takip eder. Her bölüm için önerilen konuşma noktaları:

| Bölüm                      | Temel mesaj                                                                                                |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| Başlık ve gündem            | Portal değiştirmeye gerek olmadan *VS Code’dan Foundry’ye* atölye olarak çerçeveleyin.                        |
| Neden barındırılan ajanlar? | Yönetilen çalışma zamanı, ACR tabanlı dağıtım, OpenAI uyumlu `/responses` API’si, Foundry projelerine sınırlı erişim. |
| Mimari diyagramı            | [README mimari](../README.md#architecture) üzerinden geçin: iskelet, Inspector, ACR, Agent Service.            |
| Barındırılan ajanın anatomisi | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - her dosyanın işlevi.                            |
| Canlı demo: Executive Agent | VS Code’a geçin ve [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) demoyu baştan sona çalıştırın ([Demo 1](#demo-1-executive-agent) bakınız). |
| Canlı demo: Resume to Job Fit Evaluator | VS Code’a geçin ve [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4 ajan demoyu çalıştırın ([Demo 2](#demo-2-resume-to-job-fit-evaluator) bakınız). |
| Laboratuvar 01 özeti         | Katılımcılara bırakın. [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)ye yönlendirin. |
| Çok ajanlı desenler          | Ardışık, eşzamanlı ve devir - Laboratuvar 02 başlamadan önce ön gösterim.                                     |
| Laboratuvar 02 özeti         | Katılımcılara bırakın. [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)ye yönlendirin. |
| Kapanış ve kaynaklar         | [Ek kaynaklar](#ek-kaynaklar) bölümündeki devam eden öğrenme linkleri.                              |

---

## Demolar

Teslimatta 2 canlı demo vardır. Her biri için 10 dakika ayırın.

| Demo | Laboratuvar | Dosyalar | Ne gösterilecek |
|------|-----|-------|--------------|
| Executive Agent | Laboratuvar 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | Tek barındırılan ajan; teknik jargonları yönetici özetine çevirir |
| Resume to Job Fit Evaluator | Laboratuvar 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4 ajanlı orkestrasyon; özgeçmiş-iş uyumunu puanlar ve öneri üretir |

### Demo 1: Executive Agent

[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) içindeki bağımsız ajan. Laboratuvar 01 öncesinde 10 dakikalık demo olarak kullanın.

1. [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) dosyasını açın ve ajan tanımını (sistem istemi, model, çerçeve) inceleyin.
2. **Agent Inspector**’ı yerelde başlatmak için `F5` tuşuna basın.
3. [README](../README.md#see-it-in-action) dosyasından örnek istemi yapıştırın ve yönetici özeti yanıtını gösterin.
4. Dağıtım artefaktlarını açıklamak için [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) ve [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) dosyalarını gösterin.
5. Tamamlanmayı beklemeden dağıtım akışını (Docker build, ACR push, barındırılan ajan oluşturma) gösterin.

### Demo 2: Resume to Job Fit Evaluator

[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) içindeki 4 ajanlı iş akışı. Laboratuvar 02 öncesinde 10 dakikalık demo olarak kullanın.

1. [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) dosyasını açın ve dört ajanın nasıl ardışık bir orkestrasyonda bağlandığını gösterin.
2. Çok ajanlı iş akışı için **Agent Inspector**’ı başlatmak üzere `F5` tuşuna basın.
3. Inspector sohbetine kısa bir iş tanımı ve örnek bir özgeçmiş yapıştırın.
4. Dört ajan hattını inceleyin: özgeçmiş ayrıştırıcı, iş gereksinimi çıkarıcı, uygunluk puanlayıcı ve öneri yazarı.
5. Her alt ajanın çıktısının bir sonraki ajanın bağlamı olması ve devir desenini nasıl vurguladığını gösterin.
6. Tek ajan versiyonu ile karşılaştırmak için [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) dosyasını gösterin (Demo 1’den).

---

## Sunum ipuçları

- **Beklentileri erken belirleyin.** Barındırılan ajanlar önizlemede - bölge sınırlarını ve kotayı önceden vurgulayın ki katılımcılar laboratuvar sırasında sürpriz yaşamasın.
- **Ön koşullar görevini önce çalıştırın.** Her iki laboratuvarda da `Ön koşulları doğrula` adlı VS Code görevi bulunur - kod yazmaya başlamadan önce katılımcılara çalıştırmalarını söyleyin.
- **Agent Inspector görünür olsun.** Çoğu “aha” anı, katılımcılar yerel `/responses` dolaşımı ışığını gördüğünde olur.
- **Yedek proje bulundurun.** Bir katılımcının Foundry projesi kota sorununa takılırsa, o adım için önceden sağlanmış proje paylaşarak tüm odayı engellemekten kaçının.
- **Katılımcıları eşleştirin.** Laboratuvar 02 (çok ajan) katılımcıların bir partnerle orkestrasyonu konuşabildiğinde anlamlı biçimde daha kolaydır.
- **Doküman modüllerini kontrol noktası olarak kullanın.** Her laboratuvarın `docs/` klasörü 8 numaralı modüle bölünmüştür - bunları doğal duraklama noktaları olarak kullanın.
- **Paylaşılan laboratuvar makinelerinde temel Docker görüntüsünü önceden çekin** böylece kayıt defteri oran sınırlarına takılmazsınız.

---

## Sunum sırasında sorun giderme

| Belirti                                     | İlk denenmesi gereken                                                                             |
|----------------------------------------------|--------------------------------------------------------------------------------------------------|
| Agent Inspector bağlanamıyor                 | `8088` portunun boş olduğunu ve `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` görevlerinin çalıştığını doğrulayın. |
| Hata ayıklayıcı bağlanamıyor                  | `5679` portunun boş olduğunu kontrol edin; `debugpy` zaten bağlıysa VS Code’u yeniden başlatın.  |
| `azd up` kimlik doğrulama hatası veriyor       | `az login` ve `azd auth login` komutlarını çalıştırın, doğru kiracı seçili olsun.                  |
| Dağıtım ACR push aşamasında takılıyor          | Docker Desktop’un çalıştığını ve kullanıcının kayıt defterinde `AcrPush` yetkisi olduğunu kontrol edin. |
| Model 404 döndürüyor / deployment-not-found hatası veriyor | `agent.yaml` içindeki model dağıtım adı Foundry projesindeki ile eşleşmelidir.                    |

| Barındırılan ajan `Provisioning` aşamasında takıldı         | Proje bölgesinin [barındırılan ajanları destekleyip desteklemediğini](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) ve kota olup olmadığını doğrulayın. |
| Playground 401 dönüyor                       | Foundry uzantısını VS Code etkinlik çubuğundan yeniden kimlik doğrulayın.                                   |

Daha derin rehberlik için, her laboratuvar kendi `08-troubleshooting.md` dokümanıyla birlikte gelir - öğrenenleri oraya yönlendirin:

- Laboratuvar 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- Laboratuvar 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## Bu oturumu özelleştirme

Çalıştayınızı dinleyici kitlenize uyarlayabilirsiniz. Yaygın varyasyonlar:

- **Arka uç dinleyicileri:** `agent.yaml`, Docker ve ACR üzerinde daha fazla zaman harcayın; playground demosunu kısaltın.
- **Vatandaş geliştirici kitlesi:** iskele oluşturma için Foundry uzantısı UI'sında kalın; CLI adımlarını azaltın.
- **Tek oturum 60 dakikalık slot:** sadece giriş, demo ve Laboratuvar 01'i sunun.
- **Sadece çalıştay (slaytsız) formatı:** her iki laboratuvarın README dosyalarını açın ve bunları ana betik olarak kullanın.

Laboratuvarları genişletirseniz, yapılan değişiklikleri diğer eğitmenlerin faydalanması için lütfen pull request ile geri gönderin.

---

## Ek kaynaklar

- [Microsoft Foundry belgelendirmesi](https://learn.microsoft.com/azure/ai-foundry/)
- [Barındırılan ajanlar genel bakış](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Hızlı başlangıç: ilk barındırılan ajanın dağıtımı (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [Barındırılan ajan dağıtımı (nasıl yapılır)](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## İletişim

Bu oturumu sunmayla ilgili sorularınız varsa, lütfen [workshop deposunda](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) bir issue açın ve sorumlu kişiyi etiketleyin.

| Rol                 | İsim            | GitHub                                                  |
|---------------------|-----------------|---------------------------------------------------------|
| Sorumlu / iletişim  | Shivam Goyal    | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->