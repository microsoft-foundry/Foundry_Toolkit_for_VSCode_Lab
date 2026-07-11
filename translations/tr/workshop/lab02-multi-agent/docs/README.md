# Lab 02 - Çoklu Ajan İş Akışı: Özgeçmiş → İş Uygunluk Değerlendiricisi

## Tam Öğrenme Yolu

Bu dokümantasyon, **WorkflowBuilder** aracılığıyla düzenlenen dört özel ajan kullanarak özgeçmişten işe uyumu değerlendiren **çoklu ajan iş akışı** oluşturma, test etme ve dağıtma sürecinizde size rehberlik eder.

> **Önkoşul:** Lab 02'ye başlamadan önce [Lab 01 - Tek Ajan](../../lab01-single-agent/README.md) tamamlama zorunludur.

---

## Modüller

| # | Modül | Yapacaklarınız |
|---|--------|---------------|
| 0 | [Giriş](00-prerequisites.md) | Ne inşa edeceğiniz, Lab 01 doğrulaması, Lab 02 ile Lab 01 karşılaştırması |
| 1 | [Çoklu Ajan Mimarisini Anlama](01-understand-multi-agent.md) | WorkflowBuilder öğrenme, ajan rolleri, düzenleme grafiği |
| 2 | [Çoklu Ajan Projesi Tabanını Kurma](02-scaffold-multi-agent.md) | Foundry uzantı sihirbazını kullanarak temel projeyi hazırlama |
| 3 | [Ajanları & Ortamı Yapılandırma](03-configure-agents.md) | 4 ajana talimat yazma, MCP aracını yapılandırma, ortam değişkenleri ayarlama |
| 4 | [Düzenleme Desenleri](04-orchestration-patterns.md) | Ardışık zincir, içerik iletimi ve WorkflowBuilder OR-semantikleri |
| 5 | [Yerelde Test Etme](05-test-locally.md) | Agent Inspector ile F5 hata ayıklama, özgeçmiş + iş ilanı ile hızlı testler yapma |
| 6 | [Foundry'e Dağıtma](06-deploy-to-foundry.md) | Konteyner oluşturma, ACR'ye itme, barındırılan ajanı kaydetme |
| 7 | [Oyun Alanında Doğrulama](07-verify-in-playground.md) | Dağıtılan ajanın VS Code ve Foundry Portal oyun alanlarında testi |
| 8 | [Sorun Giderme](08-troubleshooting.md) | Yaygın çoklu ajan sorunlarını giderme (MCP hataları, kısaltılmış çıktı, paket sürümleri) |
| 9 | [Özet & Sonraki Adımlar](09-summary.md) | İnşa ettikleriniz, öğrenilen temel kavramlar, temizlik ve sonraki yönlendirmeler |

---

**Geriye:** [Lab 02 README](../README.md) · [Atölye Ana Sayfası](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->