# Modül 7 - Özet & Sonraki Adımlar

⏱️ ~5 dk

**Tebrikler!** Microsoft Foundry ve VS Code için Foundry Toolkit kullanarak barındırılan bir yapay zeka ajanı oluşturdunuz, test ettiniz ve (Eğer Yol A'daysanız) dağıttınız.

---

## Ne inşa ettiniz

Bir **"Bir Yönetici Gibi Açıkla"** ajanı:
- Teknik olay raporları veya operasyonel güncellemeleri HTTP üzerinden alır (`POST /responses`)
- Bunları sade ve anlaşılır yönetici özetlerine çevirir
- Yapılandırılmış bir çıktı formatını takip eder (Ne oldu / İş etkisi / Sonraki adım)
- Konuyla alakasız istekleri ve istem enjeksiyonu girişimlerini reddeder
- Microsoft Foundry Agent Service içinde konteynerlenmiş barındırılan ajan olarak çalışır

---

## Öğrendiğiniz temel kavramlar

| Kavram | Pratik yaptığınız şey |
|---------|-------------------|
| **Agent Framework mimarisi** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` iş akışı |
| **Barındırılan Ajan yaşam döngüsü** | İskele oluşturma → Yapılandırma → Yerelde test → Dağıtım → Bulutta doğrulama |
| **Sistem prompt mühendisliği** | Rol, hedef kitle, çıktı formatı, kurallar, güvenlik kısıtlamaları ve örnekler |
| **Yerel ve barındırılan farkları** | Kimlik (kişisel kimlik bilgisi vs. yönetilen kimlik), uç noktalar, ağ yolu |
| **Güvenlik sınırları** | İstem enjeksiyon savunması, rol uyumu, sınır durumların zarif yönetimi |
| **Foundry Toolkit iş akışı** | Proje oluşturma, model dağıtımı, ajan iskele oluşturma, Agent Inspector, tek tıklama ile dağıtım |

---

## Tamamladığınız işler

### Yol A (Foundry aboneliği)

- [x] Foundry Toolkit’i kurdunuz ve dağıtılmış bir model ile Foundry projesi oluşturdunuz
- [x] Otomatik oluşturulmuş proje yapısıyla barındırılan agent iskele yaptınız
- [x] Güvenlik kuralları ile yapılandırılmış agent talimatları yazdınız
- [x] 3 işlevsel senaryoyla yerelde test ettiniz (Agent Inspector)
- [x] Foundry Agent Service’e (konteynerlenmiş) dağıttınız
- [x] Bulut oyun alanında 4 sınır durumu/güvenlik testi ile doğruladınız

### Yol B (Foundry Yerel)

- [x] Yerel model uç noktası ile Foundry Toolkit’i kurdunuz
- [x] Barındırılan agent projesi iskele yaptınız
- [x] Güvenlik kuralları ile yapılandırılmış agent talimatları yazdınız
- [x] 3 işlevsel senaryoyla yerelde test ettiniz
- [x] Bulut kaynaklarına ihtiyaç duymadan agent davranışını doğruladınız

---

## Sonraki adımlar

### Öğrenmeye devam edin

| Kaynak | Açıklama |
|----------|-------------|
| **[Lab 02 - Çoklu Ajan Orkestrasyonu](../../lab02-multi-agent/docs/README.md)** | Orkestrasyon desenleri ile 4 ajanlık iş akışı oluşturun (Özgeçmiş → İş Uygunluk Değerlendiricisi) |
| **[Ajanınıza araçlar ekleyin](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | API’ler, veritabanları veya özel fonksiyonları Araç Kataloğu üzerinden bağlayın |
| **[Bilgi ekleyin (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ajanınızı dökümanlar, vektör mağazaları veya Bing araması ile güçlendirin |
| **[Microsoft Foundry dokümantasyonu](https://learn.microsoft.com/azure/foundry/)** | Tam platform referansı |
| **[Agent Framework SDK referansı](https://learn.microsoft.com/agent-framework/)** | `agent-framework` paketi için API dokümantasyonu |
| **[Foundry Toolkit - Neler Yeni](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Eklenti sürüm notları ve değişiklik listesi |

### Ajanınızı geliştirmek için fikirler

- **Bir tarih aracı ekleyin** - Ajanın özetlere “bugün itibariyle” bağlamını dahil etmesini sağlayın
- **Bir olay veritabanına bağlanın** - Araç fonksiyonu ile gerçek olay detaylarını çekin
- **Bir Bing temelli araç ekleyin** - Ajanın ek bağlam için güncel haberleri araştırmasını sağlayın
- **Farklı modelleri deneyin** - `gpt-4.1` vs. `gpt-4.1-mini` çıktı kalitesini karşılaştırın
- **Foundry ile değerlendirin** - Değerlendirme özelliğini kullanarak ajan kalitesini ölçekli ölçün

### Yol B kullanıcıları için: Bulut dağıtımına geçiş yapın

Buluta dağıtıma hazır olduğunuzda:
1. Bir Azure aboneliği edinin ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [Modül 01, Kurulum](01-setup.md#step-2-set-up-based-on-your-access) adımını tamamlayın (proje oluşturun, modeli dağıtın, RBAC atayın)
3. `.env` dosyanızı Foundry proje uç noktası ve model dağıtım adıyla güncelleyin
4. [Modül 05 - Foundry’ye dağıtım](05-deploy-to-foundry.md) bölümünden devam edin

---

## Kaynakları temizleme (isteğe bağlı)

Bu atölye sırasında oluşturulan Azure kaynaklarını kaldırmak isterseniz:

### Seçenek 1: Kaynak grubunu silin (her şeyi kaldırır)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Seçenek 2: Sadece barındırılan ajanı silin

1. [ai.azure.com](https://ai.azure.com) → projenize → **Build** → **Agents** menüsünü açın.
2. Ajanınıza tıklayın → **Delete** butonuna tıklayın.

### Seçenek 3: Model dağıtımını silin

1. Foundry kenar çubuğunda projenizi genişletin → **Models**.
2. Model dağıtımına sağ tıklayın → **Delete**.

> **Maliyet notu:** Barındırılan ajanlar yalnızca çalıştıklarında maliyet oluşturur. Ajanı durdurur ya da silerseniz, devam eden bir ücret olmaz. Model dağıtımı, ayrılmış kapasite için küçük bir ücret oluşturabilir - işlemi bitirdiyseniz silin.

---

**Önceki:** [06 - Oyun Alanında Doğrulama](06-verify-in-playground.md) · **Sonraki:** [08 - Sorun Giderme (Referans) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->