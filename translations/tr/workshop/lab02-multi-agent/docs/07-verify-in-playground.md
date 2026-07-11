# Modül 7 - Playground'da Doğrulama

⏱️ ~10 dk

Bu modülde, dağıtılan çok ajanlı iş akışınızı VS Code ve Foundry Portal'da test ederek, ajanın yerel testle aynı şekilde davrandığını doğrularsınız.

---

## Dağıttıktan sonra neden tekrar test edilmeli?

Barındırılan ortam, yerelden birkaç önemli şekilde farklıdır:

| | Yerel | Barındırılan |
|--|-------|--------|
| **Kimlik** | Kişisel oturum açma (`DefaultAzureCredential`) | Dağıtım sırasında otomatik sağlanan her ajan için özel Entra kimliği |
| **Uç Nokta** | `http://localhost:8088/responses` | Foundry Ajan Hizmeti tarafından yönetilen URL |
| **Ağ** | Makineniz → Azure OpenAI + MCP | Azure omurgası (daha düşük gecikme) |

Yanlış yapılandırılmış bir ortam değişkeni, RBAC sorunu veya engellenen MCP çıkış çağrısı burada ilk olarak ortaya çıkar.

---

## Seçenek A: VS Code Playground'da Test Etme (ilk önerilen)

### 1. Adım: Barındırılan ajanınıza gidin

1. Aktivite Çubuğunda **Foundry Toolkit** simgesine tıklayın.
2. Projenizi genişletin → **Hosted Agents (Önizleme)** → ajanınızı bulun.

![Foundry Toolkit kenar çubuğu, Hosted Agents (Önizleme) gösteriyor; resume-job-fit-evaluator ve dağıtılan sürümleri](../../../../../translated_images/tr/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### 2. Adım: Bir sürüm seçin

1. Ajana tıklayarak sürümlerini genişletin.
2. `v1` üzerine tıklayın → durumun **aktif** olduğunu doğrulayın (kenar çubuğu "Çalışıyor" veya "Başlatıldı" gösterebilir - her ikisi de aynı hazır durumu belirtir).

### 3. Adım: Playground'u açın

1. **Playground**'a tıklayın (veya sürüme sağ tıklayıp **Playground'da Aç** seçin).
2. Bir sohbet penceresi VS Code sekmesinde açılır.

### 4. Adım: Duman testlerinizi çalıştırın

[Modül 5](05-test-locally.md)'ten aynı 3 testi kullanın. Her mesajı Playground giriş kutusuna yazın ve **Gönder** (veya **Enter**) tuşuna basın.

#### Test 1 - Tam özgeçmiş + İş Tanımı (standart akış)

Modül 5, Test 1'den tam özgeçmiş + İş Tanımı komutunu yapıştırın (Jane Doe + Contoso Ltd’de Kıdemli Bulut Mühendisi).

**Beklenen:**
- Uygunluk puanı ve detaylı hesaplama (100 puan ölçeğinde)
- Eşleşen Beceriler bölümü
- Eksik Beceriler bölümü
- **Her eksik beceri için bir boşluk kartı** ve Microsoft Learn URL’leriyle
- Zaman çizelgesi içeren öğrenme yolu

#### Test 2 - Hızlı kısa test (minimum girdi)

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**Beklenen:**
- Daha düşük uygunluk puanı (< 40)
- Aşamalı öğrenme yolu ile dürüst değerlendirme
- Birden fazla boşluk kartı (AWS, Kubernetes, Terraform, CI/CD, deneyim boşluğu)

#### Test 3 - Yüksek uygunluklu aday

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**Beklenen:**
- Yüksek uygunluk puanı (≥ 80)
- Mülakat hazırlığı ve cilalamaya odaklanma
- Çok az veya hiç boşluk kartı yok
- Hazırlığa odaklanmış kısa zaman çizelgesi

### 5. Adım: Yerel sonuçlarla karşılaştırın

Modül 5’te kaydettiğiniz yerel yanıtlar için notlarınızı veya tarayıcı sekmenizi açın. Her test için:

- Yanıtın **aynı yapıya** sahip olup olmadığını kontrol edin (uygunluk puanı, boşluk kartları, öğrenme yolu)
- **Aynı puanlama ölçütünü** kullanıyor mu (100 puan üzerinden detaylı)
- Boşluk kartlarında **Microsoft Learn URL'leri** hala var mı?
- Eksik beceri başına **bir boşluk kartı** var mı (kesilmiş veya eksik değil)?

> **Küçük ifade farkları normaldir** - model deterministik değildir. Yapıya, puanlamanın tutarlılığına ve MCP araç kullanımına odaklanın.

---

## Seçenek B: Foundry Portal'da Test Etme

[Foundry Portal](https://ai.azure.com) ekip arkadaşları veya paydaşlarla paylaşım için faydalı web tabanlı bir playground sağlar.

### 1. Adım: Foundry Portal'ı açın

1. Tarayıcınızı açın ve [https://ai.azure.com](https://ai.azure.com) adresine gidin.
2. Atölye boyunca kullandığınız aynı Azure hesabıyla oturum açın.

### 2. Adım: Projenize gidin

1. Ana sayfada, sol kenar çubuğundaki **Son projeler** bölümünü bulun.
2. Proje adınıza tıklayın (örneğin, `workshop-agents`).
3. Görmüyorsanız, **Tüm projeler**'e tıklayıp arama yapın.

### 3. Adım: Dağıtılan ajanınızı bulun

1. Projenin sol navigasyonunda **Build** → **Agents**'a tıklayın (veya **Agents** bölümünü arayın).
2. Ajan listesini görmelisiniz. Dağıttığınız ajanı bulun (örneğin, `resume-job-fit-evaluator`).
3. Ajan adına tıklayarak detay sayfasını açın.

### 4. Adım: Playground'u açın

1. Ajan detay sayfasında, üst araç çubuğuna bakın.
2. **Playground'da aç** (veya **Playground'da dene**) seçeneğine tıklayın.
3. Bir sohbet arayüzü açılır.

### 5. Adım: Aynı duman testlerini çalıştırın

Yukarıdaki VS Code Playground bölümündeki tüm 3 testi tekrar edin. Her yanıtı hem yerel sonuçlar (Modül 5) hem de VS Code Playground sonuçları (Yukarıdaki Seçenek A) ile karşılaştırın.

---

## Çok ajanlı özel doğrulama

Temel doğrulamanın ötesinde, bu çok ajanlı özel davranışları doğrulayın:

### MCP araç yürütmesi

| Kontrol | Nasıl doğrulanır | Geçme koşulu |
|-------|---------------|----------------|
| MCP çağrıları başarılı | Boşluk kartlarındaki URL'ler `learn.microsoft.com` | Gerçek URL’ler, yedek mesajlar değil |
| Birden çok MCP çağrısı | Her Yüksek/Orta öncelikli boşluk kaynaklara sahip | Sadece ilk boşluk kartı değil |
| MCP yedekleme çalışıyor | URL’ler eksikse, yedek metin var mı kontrol et | Ajan hala boşluk kartları üretiyor (URL olsun veya olmasın) |

### Ajan koordinasyonu

| Kontrol | Nasıl doğrulanır | Geçme koşulu |
|-------|---------------|----------------|
| 4 ajan da çalıştı | Çıktı uygunluk puanı VE boşluk kartları içeriyor | Puan MatchingAgent'tan, kartlar GapAnalyzer'dan gelir |
| Sıralı yürütme | Yanıt süresi makul (< 2 dk) | > 3 dk ise terminal günlüklerinde hata kontrolü yapın |
| Veri akışı bütünlüğü | Boşluk kartları, eşleştirme raporundaki becerilere referans veriyor | İlan dışı beceriler (halüsinasyon) yok |

---

## Doğrulama ölçütleri

Çok ajanlı iş akışınızın barındırılan davranışını değerlendirmek için bu ölçütleri kullanın:

| # | Kriter | Geçme koşulu | Geçti mi? |
|---|----------|---------------|-------|
| 1 | **Fonksiyonel doğruluk** | Ajan, özgeçmiş + iş tanımına uygunluk puanı ve boşluk analizli yanıt verir | |
| 2 | **Puanlama tutarlılığı** | Uygunluk puanı 100 puan ölçeğiyle ve detaylı hesaplamayla verilir | |
| 3 | **Boşluk kartlarının tamlığı** | Eksik beceri başına bir kart (kesilmiş ya da birleştirilmiş değil) | |
| 4 | **MCP araç entegrasyonu** | Boşluk kartlarında gerçek Microsoft Learn URL’leri bulunur | |
| 5 | **Yapısal tutarlılık** | Çıktı yapısı yerel ve barındırılan çalışmada uyumludur | |
| 6 | **Yanıt süresi** | Barındırılan ajan tam değerlendirme için 2 dakika içinde yanıt verir | |
| 7 | **Hata yok** | HTTP 500 hatası, zaman aşımı veya boş yanıt yok | |

> "Geçme" demek, 3 duman testinin tamamında en az bir playground (VS Code veya Portal) için tüm 7 kriterin sağlanması demektir.

---

## Playground sorun giderme

| Belirti | Muhtemel sebep | Çözüm |
|---------|-------------|-----|
| Playground yüklenmiyor | Container `aktif` durumda değil | [Modül 6](06-deploy-to-foundry.md)'ya dönün, dağıtım durumunu kontrol edin. `creating` ise bekleyin |
| Ajan boş yanıt veriyor | Model dağıtım adı uyuşmuyor | `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` dağıtılan modelinizle eşleşmeli |
| Ajan hata mesajı dönüyor | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) izni eksik | Proje kapsamına **[Foundry Kullanıcısı](https://aka.ms/foundry-ext-project-role)** rolünü atayın (önceki Azure AI Kullanıcısı) |
| Boşluk kartlarında Microsoft Learn URL'si yok | MCP çıkış engellenmiş veya MCP sunucusu kullanılamıyor | Container’ın `learn.microsoft.com` erişimi olup olmadığını kontrol edin. Bakınız [Modül 8](08-troubleshooting.md) |
| Sadece 1 boşluk kartı var (kesilmiş) | GapAnalyzer talimatlarında "CRITICAL" bloğu eksik | [Modül 3, 2.4 Adım](03-configure-agents.md)'i inceleyin |
| Uygunluk puanı yerel ile çok farklı | Farklı model veya talimat dağıtıldı | `agent.yaml` ortam değişkenlerini yerel `.env` ile karşılaştırın. Gerekirse yeniden dağıtım yapın |
| Portalda "Ajan bulunamadı" | Dağıtım henüz tamamlanmadı veya başarısız oldu | 2 dakika bekleyip yenileyin. Hala yoksa [Modül 6](06-deploy-to-foundry.md)'den yeniden dağıtın |

---

### Kontrol Noktası

- [ ] VS Code Playground'da ajan test edildi - 3 duman testinin tamamı geçerli
- [ ] [Foundry Portal](https://ai.azure.com) Playground'da ajan test edildi - 3 duman testi geçti
- [ ] Yanıtlar yerel testle yapısal olarak tutarlı (uygunluk puanı, boşluk kartları, öğrenme yolu)
- [ ] Boşluk kartlarında Microsoft Learn URL’leri mevcut (barındırılan ortamda MCP aracı çalışıyor)
- [ ] Her eksik beceri için bir boşluk kartı (kesilme yok)
- [ ] Test sırasında hata veya zaman aşımı olmadı
- [ ] Doğrulama ölçütleri tamamlandı (tüm 7 kriter geçti)

---

**Önceki:** [06 - Foundry'ye Dağıtım](06-deploy-to-foundry.md) · **Sonraki:** [08 - Sorun Giderme →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->