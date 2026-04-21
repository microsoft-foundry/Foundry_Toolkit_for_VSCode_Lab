# Lab 02 - Çoklu Ajan İş Akışı: Özgeçmiş → İş Uygunluk Değerlendiricisi

## Tam Öğrenme Yolu

Bu dokümantasyon, **WorkflowBuilder** aracılığıyla düzenlenen dört özel ajanı kullanarak özgeçmiş ile iş uyumunu değerlendiren bir **çoklu ajan iş akışı** oluşturmanızı, test etmenizi ve dağıtmanızı adım adım gösterir.

> **Önkoşul:** Lab 02'ye başlamadan önce [Lab 01 - Tek Ajan](../../lab01-single-agent/README.md) tamamlayın.

---

## Modüller

| # | Modül | Ne Yapacaksınız |
|---|--------|----------------|
| 0 | [Önkoşullar](00-prerequisites.md) | Lab 01 tamamlanmasını doğrulama, çoklu ajan kavramlarını anlama |
| 1 | [Çoklu Ajan Mimarisi Anlama](01-understand-multi-agent.md) | WorkflowBuilder, ajan rolleri, orkestrasyon grafiği öğrenme |
| 2 | [Çoklu Ajan Projesi iskeleti oluşturma](02-scaffold-multi-agent.md) | Foundry uzantısını kullanarak çoklu ajan iş akışı iskeleti oluşturma |
| 3 | [Ajanlar & Ortamı Yapılandırma](03-configure-agents.md) | 4 ajan için talimat yazma, MCP aracını yapılandırma, ortam değişkenlerini ayarlama |
| 4 | [Orkestrasyon Desenleri](04-orchestration-patterns.md) | Paralel fan-out, ardışık toplama ve alternatif desenleri keşfetme |
| 5 | [Yerelde Test Etme](05-test-locally.md) | Agent Inspector ile F5 hata ayıklama, özgeçmiş + JD ile duman testleri yapma |
| 6 | [Foundry’e Dağıtma](06-deploy-to-foundry.md) | Konteyner oluşturma, ACR’ye gönderme, barındırılan ajan kaydetme |
| 7 | [Playground’da Doğrulama](07-verify-in-playground.md) | VS Code ve Foundry Portal playgroundlarında dağıtılan ajanı test etme |
| 8 | [Sorun Giderme](08-troubleshooting.md) | Yaygın çoklu ajan sorunlarını çözme (MCP hataları, kısaltılmış çıktı, paket sürümleri) |

---

## Tahmini süre

| Deneyim seviyesi | Süre |
|-----------------|-------|
| Lab 01’i yeni tamamlayan | 45-60 dakika |
| Biraz Azure AI deneyimi olan | 60-90 dakika |
| Çoklu ajan ile ilk kez deneyen | 90-120 dakika |

---

## Mimari genel bakış

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**Geri Dön:** [Lab 02 README](../README.md) · [Çalıştay Anasayfa](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:  
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hatalar veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı nedeniyle oluşabilecek herhangi bir yanlış anlama veya yanlış yorumdan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->