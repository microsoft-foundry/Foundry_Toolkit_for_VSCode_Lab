# Bilinen Sorunlar

Bu doküman mevcut depo durumu ile bilinen sorunları takip eder.

> Son güncelleme: 2026-04-15. Python 3.13 / Windows üzerinde `.venv_ga_test` ile test edildi.

---

## Mevcut Paket Sabitlemeleri (üç ajan için de)

| Paket | Mevcut Sürüm |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(düzeltilmiş — bkz KI-003)* |

---

## KI-001 — GA 1.0.0 Yükseltmesi Engellendi: `agent-framework-azure-ai` Kaldırıldı

**Durum:** Açık | **Ciddiyet:** 🔴 Yüksek | **Tip:** Kırıcı

### Açıklama

`agent-framework-azure-ai` paketi (`1.0.0rc3` olarak sabitlenmiş) GA sürümünde (1.0.0, 2026-04-02 yayınlandı) **kaldırıldı/iptal edildi**.
Yerini şöyle alan paketler aldı:

- `agent-framework-foundry==1.0.0` — Foundry tarafından barındırılan ajan modeli
- `agent-framework-openai==1.0.0` — OpenAI destekli ajan modeli

Üç `main.py` dosyasının tümü `AzureAIAgentClient`'i `agent_framework.azure`'dan içe aktarır ki bu GA paketlerinde `ImportError` oluşturur. `agent_framework.azure` isim alanı GA'da halen vardır ancak artık sadece Azure Fonksiyonları sınıflarını içerir (`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`) — Foundry ajanları değil.

### Onaylanmış hata (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Etkilenen dosyalar

| Dosya | Satır |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` GA `agent-framework-core` ile Uyumsuz

**Durum:** Açık | **Ciddiyet:** 🔴 Yüksek | **Tip:** Kırıcı (yukarı akışta engelleniyor)

### Açıklama

`azure-ai-agentserver-agentframework==1.0.0b17` (en güncel) `agent-framework-core<=1.0.0rc3` olarak sıkı sabitleme yapar. Bunu GA'nın (`agent-framework-core==1.0.0`) yanında kurmak pip'in `agent-framework-core`'u tekrar `rc3` sürümüne **düşürmesine** neden olur, bu da `agent-framework-foundry==1.0.0` ve `agent-framework-openai==1.0.0`'un bozulmasına yol açar.

Bütün ajanların HTTP sunucusunu bağlamak için kullandığı `from azure.ai.agentserver.agentframework import from_agent_framework` çağrısı da bu nedenle engellenmiştir.

### Onaylanmış bağımlılık çatışması (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Etkilenen dosyalar

Üç `main.py` dosyasının tamamı — hem üst seviye içe aktarma hem de `main()` fonksiyonundaki içe aktarma.

---

## KI-003 — `agent-dev-cli --pre` Bayrağı Artık Gerekli Değil

**Durum:** ✅ Düzeltildi (kırmayan) | **Ciddiyet:** 🟢 Düşük

### Açıklama

Tüm `requirements.txt` dosyaları önceden ön-sürüm CLI almak için `agent-dev-cli --pre` içeriyordu. 1.0.0 GA sürümü 2026-04-02'de yayınlandığından beri, `agent-dev-cli` stabil sürümü artık `--pre` bayrağı olmadan kullanılabilir.

**Uygulanan düzeltme:** Üç `requirements.txt` dosyasından `--pre` bayrağı kaldırıldı.

---

## KI-004 — Dockerfile'lar `python:3.14-slim` (Ön Sürüm Temel İmaj) Kullanıyor

**Durum:** Açık | **Ciddiyet:** 🟡 Düşük

### Açıklama

Tüm `Dockerfile` dosyaları `FROM python:3.14-slim` kullanmakta, bu ön sürüm Python derlemesini takip eder. Üretim dağıtımları için bu stabil bir sürüme (örneğin `python:3.12-slim`) sabitlenmelidir.

### Etkilenen dosyalar

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referanslar

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:  
Bu belge, AI çeviri hizmeti [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba göstersek de, otomatik çevirilerin hatalar veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilmektedir. Bu çevirinin kullanımı nedeniyle oluşabilecek yanlış anlamalar veya yorum hatalarından sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->