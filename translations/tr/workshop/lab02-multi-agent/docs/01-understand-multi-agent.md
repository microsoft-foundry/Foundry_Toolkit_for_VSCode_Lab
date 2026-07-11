# Modül 1 - Mimariliği Anlama

⏱️ ~5 dk

Herhangi bir kod yazmadan önce, ne inşa ettiğiniz ve nasıl çalıştığına dair hızlı bir genel bakış.

---

## İnşa ettiğiniz şey

Bir **özgeçmiş** ve bir **iş tanımı** yapıştırıyorsunuz. İş akışı şunları döndürür:

- Uyum skoru (0–100 arası, dökümü ile birlikte)
- Beceri ve sertifika açıklarının listesi
- Her açık için Microsoft Learn bağlantıları içeren kişiselleştirilmiş öğrenme yol haritası

---

## Dört ajan

Tek bir ajanın hepsini birden çözümlemeye, puanlamaya ve planlamaya çalışması aceleye getirmeye ve yüzeysel çıktı vermeye eğilimlidir. İşin dört uzmanlaşmış ajana bölünmesi daha iyi sonuçlar verir:

| Ajan | Ne yapar |
|-------|-------------|
| **ResumeParser** | Özgeçmişi çözümler; iş tanımını (JD) kelimesi kelimesine `[JOB DESCRIPTION PASS-THROUGH]` olarak alt ajanlara kopyalar |
| **JobDescriptionAgent** | Geçişten JD gereksinimlerini çıkarır; `[PARSED RESUME]` bölümünü `[PARSED RESUME PASS-THROUGH]` olarak ileri iletir |
| **MatchingAgent** | Etiketli bölümleri karşılaştırır; 0–100 arasında uyum skoru ve açık listesi üretir |
| **GapAnalyzer** | Öğrenme yol haritası oluşturur; her açık için Microsoft Learn'da arama yapar |

---

## Koordinasyon grafiği

İş akışı bir **ardışık boru hattı**dır - her ajan çıktısını sonraki ajana iletir:

```mermaid
flowchart LR
    A["Kullanıcı Girişi"] --> B["Özgeçmiş Ayrıştırıcı"]
    B -- "ayrıştırılmış özgeçmiş + iş tanımı aktarımı" --> C["İş Tanımı Temsilcisi"]
    C -- "iş tanımı gereksinimleri + özgeçmiş aktarımı" --> D["Eşleştirme Temsilcisi"]
    D -- "uygunluk raporu + boşluklar" --> E["Boşluk Analizörü + MCP"]
    E --> F["Nihai Çıktı"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. **ResumeParser** kullanıcı girdisini alır, özgeçmişi çözümler ve iş tanımını `[JOB DESCRIPTION PASS-THROUGH]` olarak kopyalar.
2. **JD Agent** yapılandırılmış gereksinimleri çıkarır ve `[PARSED RESUME PASS-THROUGH]` olarak iletir.
3. **MatchingAgent** her iki bölümü karşılaştırır ve uyum skoru ile açık listesini üretir.
4. **GapAnalyzer** yol haritasını oluşturur ve her açık için Microsoft Learn MCP aracını çağırır.

---

## Bu kodla nasıl eşlenir

`main.py` içinde bu grafiği `WorkflowBuilder` ile tanımlarsınız:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # kullanıcı girdisini alan ilk ajan
        output_executors=[gap_executor],      # son ajan - çıktısı yanıt olarak verilir
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → İş Tanımı Ajanı
    .add_edge(jd_executor, matching_executor)     # İş Tanımı Ajanı → Eşleştirme Ajanı
    .add_edge(matching_executor, gap_executor)    # Eşleştirme Ajanı → Boşluk Analizörü
    .build()
    .as_agent()
)
```

Her `Agent` bir `AgentExecutor` ile sarılır. `add_edge()` çağrıları kesin ardışık bir boru hattını tanımlar - her ajan sadece doğrudan öncüsünün çıktısını alır.

> `context_mode="last_agent"` her yürütücünün sadece doğrudan öncüsünün çıktısını görmesi anlamına gelir. ResumeParser ve JD Agent verileri etiketli bölümler halinde iletir, böylece her alt ajan tam ihtiyaç duyduğu bilgiyi alır.

---

## MCP aracı

GapAnalyzer'ın bir aracı vardır: `search_microsoft_learn_for_plan`. Bu araç `https://learn.microsoft.com/api/mcp` adresine bağlanır ve her beceri açığı için gerçek Microsoft Learn bağlantıları döndürür.

Araç çalıştığında şu günlükleri görürsünüz - hepsi beklenen:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

`POST` bir hata döndürmedikçe endişelenmeyin.

---

**Önceki:** [00 - Önkoşullar](00-prerequisites.md) · **Sonraki:** [02 - Projeyi Kurmak →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba sarf etsek de, otomatik çevirilerin hata veya yanlışlık içerebileceğini lütfen unutmayınız. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu ortaya çıkabilecek yanlış anlamalardan veya yanlış yorumlamalardan sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->