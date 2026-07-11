# Foundry Araç Takımı + Foundry Barındırılan Ajanlar Atölyesi

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

AI ajanlarını **Microsoft Foundry Agent Hizmeti**'ne **Barındırılan Ajanlar** olarak VS Code üzerinden tamamen **Microsoft Foundry uzantısı** ve **Foundry Araç Takımı** kullanarak oluşturun, test edin ve dağıtın.

> **Barındırılan Ajanlar şu anda önizlemededir.** Desteklenen bölgeler sınırlıdır - bkz [bölge kullanılabilirliği](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> Her laboratuvardaki `agent/` klasörü Foundry uzantısı tarafından **otomatik olarak oluşturulur** - ardından kodu özelleştirir, yerel test yapar ve dağıtırsınız.

### 🌐 Çok Dilli Destek

#### GitHub Action ile Desteklenmektedir (Otomatik ve Her Zaman Güncel)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](./README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **Yerel Kopyalamayı mı Tercih Edersiniz?**
>
> Bu depo 50+ dil çevirisini içerir ve bu da indirme boyutunu önemli ölçüde artırır. Çeviriler olmadan klonlamak için sparse checkout kullanın:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Bu, kursu tamamlamak için ihtiyacınız olan her şeyi çok daha hızlı bir indirme ile sunar.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## Mimari

```mermaid
flowchart TB
    subgraph Local["Yerel Geliştirme (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "F5 Hata Ayıkla" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> İskele
    Playground -- "Test istemleri" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**Akış:** Foundry uzantısı ajanı oluşturur → siz kodu ve talimatları özelleştirirsiniz → Agent Inspector ile yerelde test edersiniz → Foundry’ye dağıtırsınız (Docker görüntüsü ACR’ye gönderilir) → Playground’da doğrulama yaparsınız.

---

## Ne inşa edeceksiniz

| Laboratuvar | Açıklama | Durum |
|-----|-------------|--------|
| **Laboratuvar 01 - Tek Ajan** | **"Yönetici Gibi Açıkla" Ajanı** oluşturun, yerelde test edin ve Foundry’ye dağıtın | ✅ Mevcut |
| **Laboratuvar 02 - Çoklu Ajan İş Akışı** | **"Özgeçmiş → İş Uygunluk Değerlendiricisi"** oluşturun - 4 ajan özgeçmiş uygunluğunu puanlamak ve öğrenme yol haritası oluşturmak için birlikte çalışır | ✅ Mevcut |

---

## Yönetici Ajanı ile Tanışın

Bu atölyede, teknik jargonları sakin, yönetim kurulu sunumlarına uygun özetlere çeviren **"Yönetici Gibi Açıkla" Ajanı** adlı bir AI ajanı oluşturacaksınız. Çünkü dürüst olalım, yönetim katında kim “v3.2’de tanıtılan eşzamanlı çağrılar nedeniyle oluşan iş parçacığı havuzu tükenmesi” hakkında duymak ister?

Bu ajanı, mükemmel hazırlanmış ölüm sonrası raporumun aldığı cevabi tepkiyi ("Yani... site mi kapandı, kapatılmadı mı?") çok fazla yaşadıktan sonra geliştirdim.

### Nasıl çalışır

Teknik bir güncelleme verirsiniz. O da size yönetici özeti verir - üç madde, jargon yok, yığın izleri yok, varoluşsal korku yok. Sadece **ne oldu**, **iş etkisi**, ve **sonraki adım**.

### Uygulamada görün

**Siz şöyle söylersiniz:**
> "API gecikmesi, v3.2’de tanıtılan eşzamanlı çağrılar nedeniyle oluşan iş parçacığı havuzu tükenmesinden dolayı arttı."

**Ajan şöyle cevap verir:**

> **Yönetici Özeti:**
> - **Ne oldu:** Son sürümden sonra sistem yavaşladı.
> - **İş etkisi:** Bazı kullanıcılar hizmeti kullanırken gecikme yaşadı.
> - **Sonraki adım:** Değişiklik geri alındı ve yeniden dağıtımdan önce bir düzeltme hazırlanıyor.

### Neden bu ajan?

Bu, aylak karmaşık araç zincirlerine takılmadan barındırılan ajan iş akışını baştan sona öğrenmek için mükemmel, tek amaçlı, son derece basit bir ajan. Ve dürüst olmak gerekirse? Her mühendislik ekibi böyle bir ajana ihtiyaç duyar.

---

## Atölye yapısı

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **Not:** Her laboratuvardaki `agent/` klasörü, Komut Paletinden `Microsoft Foundry: Yeni Barındırılan Ajan Oluştur` çalıştırıldığında **Microsoft Foundry uzantısı** tarafından oluşturulur. Dosyalar ardından ajanın talimatları, araçları ve yapılandırması ile özelleştirilir. Laboratuvar 01, bunu sıfırdan yeniden oluşturmanızı sağlar.

---

## Başlarken

### 1. Depoyu klonlayın

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Bir Python sanal ortamı kurun

```bash
python -m venv venv
```

Etkinleştirin:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. Ortam değişkenlerini yapılandırın

Ajan klasörü içindeki örnek `.env` dosyasını kopyalayın ve kendi değerlerinizi girin:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` dosyasını düzenleyin:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. Atölye laboratuvarlarını takip edin

Her laboratuvar kendi modülleriyle bağımsızdır. Temelleri öğrenmek için **Laboratuvar 01** ile başlayın, ardından çoklu ajan iş akışları için **Laboratuvar 02**'ye geçin.

#### Laboratuvar 01 - Tek Ajan ([tam talimatlar](workshop/lab01-single-agent/README.md))

| # | Modül | Bağlantı |
|---|--------|------|
| 1 | Ön koşulları okuyun | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit & Foundry uzantısını kurun | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | Bir Foundry projesi oluşturun | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | Bir barındırılan ajan oluşturun | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | Talimatları ve ortamı yapılandırın | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | Yerelde test edin | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | Foundry’ye dağıtın | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | Playground’da doğrulayın | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | Sorun giderme | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### Laboratuvar 02 - Çoklu Ajan İş Akışı ([tam talimatlar](workshop/lab02-multi-agent/README.md))

| # | Modül | Bağlantı |
|---|--------|------|
| 1 | Ön koşullar (Laboratuvar 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | Çoklu ajan mimarisini anlayın | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | Çoklu ajan projesi iskeletini oluşturun | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | Ajanları ve ortamı yapılandırın | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | Orkestrasyon kalıpları | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | Yerelde test edin (çoklu ajan) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | Foundry'e Dağıt | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | Oyun alanında doğrula | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | Sorun Giderme (çoklu ajan) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## Yöneten

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## Gerekli izinler (hızlı referans)

| Senaryo | Gerekli roller |
|----------|---------------|
| Yeni Foundry projesi oluştur | Foundry kaynağında **Azure AI Sahibi** |
| Var olan projeye dağıtım (yeni kaynaklar) | Abonelikte **Azure AI Sahibi** + **Katkıda Bulunan** |
| Tam yapılandırılmış projeye dağıtım | Hesapta **Okuyucu** + projede **Azure AI Kullanıcısı** |

> **Önemli:** Azure `Sahibi` ve `Katkıda Bulunan` rolleri yalnızca *yönetim* izinlerini içerir, *geliştirme* (veri işlemi) izinlerini içermez. Ajanları oluşturmak ve dağıtmak için **Azure AI Kullanıcısı** veya **Azure AI Sahibi** gereklidir.

---

## Referanslar

- [Hızlı Başlangıç: İlk barındırılan ajanın dağıtımı (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [Barındırılan ajanlar nedir?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code'da barındırılan ajan iş akışları oluşturma](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [Barındırılan ajan dağıtımı](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry için RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [Mimari İnceleme Ajan Örneği](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP araçları, Excalidraw diyagramları ve çift dağıtımlı gerçek dünya barındırılan ajanı

---


## Lisans

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->