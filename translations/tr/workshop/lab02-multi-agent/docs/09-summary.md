# Modül 9 - Özet & Sonraki Adımlar

⏱️ ~5 dk

**Tebrikler!** Microsoft Foundry ve Foundry Toolkit for VS Code kullanarak çoklu ajan iş akışını oluşturup test ettiniz ve (Eğer Yol A üzerindeyseniz) dağıttınız.

---

## Oluşturduklarınız

**Özgeçmiş → İş Uygunluğu Değerlendiricisi** - çoklu ajan barındırılan bir iş akışı:
- HTTP üzerinden özgeçmiş + iş tanımı alır (`POST /responses`)
- Dört uzman ajanı ardışık bir pipeline’da çalıştırır - her ajan, ardılı için gereken veriyi iletir
- Uygunluk puanı (0–100 arası detaylı), beceri ve sertifika boşluk listesi ve her boşluk için gerçek Microsoft Learn bağlantıları içeren kişiselleştirilmiş öğrenme yol haritası döner
- Microsoft Learn MCP sunucusunu (`https://learn.microsoft.com/api/mcp`) her belirlenen beceri boşluğu için resmi öğrenme kaynaklarını almak üzere çağırır
- Microsoft Foundry Agent Service’de tek bir konteynerleşmiş barındırılan ajan olarak çalışır

---

## Öğrendiğiniz temel kavramlar

| Kavram | Uygulama yaptığınız konular |
|---------|-------------------|
| **Çoklu ajan orkestrasyonu** | `WorkflowBuilder` ardışık pipeline ile `add_edge()` kullanımı |
| **Ajan uzmanlaşması** | Dört odaklı ajan, tek genel amaçlı ajandan daha iyi performans gösterir |
| **İçerik Yönlendirici deseni** | ResumeParser aynı zamanda yönlendirici görevi görür - JD metnini `[JOB DESCRIPTION PASS-THROUGH]` bölümünde korur ki alt akış ajanları ona erişebilsin (gereklidir çünkü `context_mode="last_agent"` yalnızca `start_executor`'ın ham kullanıcı mesajını görmesi anlamına gelir) |
| **İçerik İletici deseni** | JD Agent, `[PARSED RESUME PASS-THROUGH]`'u ileri iletir, böylece MatchingAgent her iki profili de alır; fan-in grafikleri ile tetiklenen OR-semantiği çift tetiklemeyi önler |
| **MCP araç entegrasyonu** | `@tool` ve `streamable_http_client` ile harici MCP sunucusu çağrısı |
| **Barındırılan Ajan yaşam döngüsü** | Hazırlık → Yapılandırma → Yerel test → Dağıt → Bulut doğrulama |
| **`context_mode="last_agent"`** | Her yürütücü yalnızca doğrudan selefinin çıktısını görür |
| **Foundry Toolkit iş akışı** | Hazırlık sihirbazı, Ajan Denetleyici, İş Akışı Görselleştirici, tek tıkla dağıtım |

---

## Tamamladıklarınız

<details open>
<summary><strong>🅰️ Yol A - Foundry aboneliği</strong></summary>

- [x] Lab 01 kurulumu doğrulandı: proje, model ve RBAC aktif
- [x] Workflows şablonu kullanılarak çoklu ajan projesi hazırlandı
- [x] Dört ajan talimat seti yazıldı (ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Microsoft Learn MCP aracı `streamable_http_client` ile entegre edildi
- [x] İş akışı grafiği `WorkflowBuilder` ile bağlantılandırıldı (ardışık pipeline ve içerik iletimi)
- [x] 3 fonksiyonel test (Agent Denetleyici) ile yerelde test edildi - uygunluk puanı, boşluk kartları ve MCP URL’leri
- [x] Foundry Agent Service’e dağıtıldı (konteynerleşmiş, yönetilen kimlik)
- [x] Bulut oyun alanında doğrulandı - yerel sonuçlarla yapısal tutarlılık

</details>

<details open>
<summary><strong>🅱️ Yol B - Foundry Local</strong></summary>

- [x] Lab 01 kurulumu doğrulandı: Foundry Local yerelde model ile çalışıyor
- [x] Workflows şablonu ile çoklu ajan projesi hazırlandı
- [x] Dört ajan talimat seti yazıldı ve iş akışı grafiği oluşturuldu
- [x] Microsoft Learn MCP aracı entegre edildi
- [x] 3 fonksiyonel testle yerelde test edildi
- [x] Bulut kaynağına gerek olmadan çoklu ajan davranışı doğrulandı

</details>

---

## Sonraki adımlar

### Öğrenmeye devam edin

| Kaynak | Açıklama |
|----------|-------------|
| **[Agent Framework SDK referansı](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` için API dokümanları |
| **[MCP araç kataloğu](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | Ajanları diğer MCP sunucularına bağlama (Bing, GitHub, özel) |
| **[Bilgi ekleme (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | Ajanları belgeler, vektör mağazaları veya Bing araması ile destekleme |
| **[Foundry Değerlendirmeleri](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | Otomatik değerlendirme araçları ile ajan kalitesini ölçekle ölçme |
| **[Microsoft Foundry dokümantasyonu](https://learn.microsoft.com/azure/foundry/)** | Tam platform referansı |
| **[Foundry Toolkit - Yenilikler](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | Uzantı sürüm notları ve değişiklik günlüğü |

### Bu iş akışını genişletme fikirleri

- **5. ajan ekleyin** - Boşluk raporuna dayalı muhtemel mülakat soruları üreten bir görüşme koçu
- **Bing tabanlı bir araç ekleyin** - JD Ajanının benzer iş ilanlarını arayarak gereksinimleri zenginleştirmesini sağlayın
- **Bir özgeçmiş veritabanına bağlanın** - Bir `@tool` aracılığıyla aday profillerini bir veritabanından çekin
- **Farklı modeller deneyin** - `gpt-4.1` ve `gpt-4.1-mini` çıktı kalitesi ve gecikme süresini karşılaştırın
- **Foundry ile değerlendirin** - Uygunluk raporlarını altın veri setine karşı Değerlendirmeler özelliği ile puanlayın

### Yol B kullanıcıları için: Bulut dağıtımına yükseltme

Buluta dağıtıma hazır olduğunuzda:
1. Bir Azure aboneliği alın ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [Lab 01, Modül 01](../../lab01-single-agent/docs/01-setup.md) tamamlayın (proje oluşturun, modeli dağıtın, RBAC atayın)
3. `.env` dosyanızı Foundry proje uç noktası ve model dağıtım adı ile güncelleyin
4. [Modül 06 - Foundry’e dağıtım](06-deploy-to-foundry.md) kısmından devam edin

---

## Kaynakları temizleyin (isteğe bağlı)

Bu atölye sırasında oluşturulan Azure kaynaklarını kaldırmak isterseniz:

### Seçenek 1: Kaynak grubunu silin (her şeyi kaldırır)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### Seçenek 2: Sadece barındırılan ajanı silin

1. [ai.azure.com](https://ai.azure.com) → projenize gidin → **Build** → **Agents**.
2. **PersonalCareerCopilot** bulun → **Delete**’ye tıklayın.

### Seçenek 3: Model dağıtımını silin

1. Foundry kenar çubuğunda projenizi genişletin → **Models**.
2. Model dağıtımına sağ tıklayın → **Delete**.

> **Maliyet notu:** Barındırılan ajanlar sadece çalışırken ücretlendirilir. Ajanı durdurur veya silerseniz, devam eden bir ücret yoktur. Model dağıtımı, rezerve kapasite için küçük bir ücret alabilir - işi bitince bunu silin.

---

**Önceki:** [08 - Sorun Giderme](08-troubleshooting.md) · **Ana Sayfa:** [Lab 02 README](../README.md) · [Atölye Ana Sayfa](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->