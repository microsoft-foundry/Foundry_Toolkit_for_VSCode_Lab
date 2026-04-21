# Known Issues

Dokumen ini melacak masalah yang diketahui dengan status repositori saat ini.

> Terakhir diperbarui: 2026-04-15. Diuji terhadap Python 3.13 / Windows di `.venv_ga_test`.

---

## Current Package Pins (semua tiga agen)

| Package | Versi Saat Ini |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(diperbaiki — lihat KI-003)* |

---

## KI-001 — GA 1.0.0 Upgrade Terblokir: `agent-framework-azure-ai` Dihapus

**Status:** Terbuka | **Tingkat Keparahan:** 🔴 Tinggi | **Tipe:** Breaking

### Deskripsi

Paket `agent-framework-azure-ai` (dipin pada `1.0.0rc3`) telah **dihapus/digosongkan**
pada rilis GA (1.0.0, dirilis 2026-04-02). Paket ini digantikan oleh:

- `agent-framework-foundry==1.0.0` — pola agen yang di-host di Foundry
- `agent-framework-openai==1.0.0` — pola agen yang didukung oleh OpenAI

Ketiga berkas `main.py` mengimpor `AzureAIAgentClient` dari `agent_framework.azure`, yang
menimbulkan `ImportError` pada paket GA. Namespace `agent_framework.azure` masih ada
dalam GA tetapi sekarang hanya berisi kelas Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — bukan agen Foundry.

### Kesalahan yang dikonfirmasi (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Berkas yang terdampak

| Berkas | Baris |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Tidak Kompatibel dengan GA `agent-framework-core`

**Status:** Terbuka | **Tingkat Keparahan:** 🔴 Tinggi | **Tipe:** Breaking (terblokir dari hulu)

### Deskripsi

`azure-ai-agentserver-agentframework==1.0.0b17` (terbaru) memasang pin ketat
`agent-framework-core<=1.0.0rc3`. Menginstalnya bersama `agent-framework-core==1.0.0` (GA)
memaksa pip untuk **menurunkan versi** `agent-framework-core` kembali ke `rc3`, yang kemudian mematahkan
`agent-framework-foundry==1.0.0` dan `agent-framework-openai==1.0.0`.

Panggilan `from azure.ai.agentserver.agentframework import from_agent_framework` yang digunakan oleh semua
agen untuk mengikat server HTTP juga terblokir.

### Konflik ketergantungan yang dikonfirmasi (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Berkas yang terdampak

Ketiga berkas `main.py` — baik impor tingkat atas maupun impor di dalam fungsi `main()`.

---

## KI-003 — Flag `agent-dev-cli --pre` Tidak Lagi Diperlukan

**Status:** ✅ Diperbaiki (non-breaking) | **Tingkat Keparahan:** 🟢 Rendah

### Deskripsi

Semua berkas `requirements.txt` sebelumnya menyertakan `agent-dev-cli --pre` untuk mengunduh
CLI prarilis. Sejak GA 1.0.0 dirilis pada 2026-04-02, rilis stabil
`agent-dev-cli` sekarang tersedia tanpa flag `--pre`.

**Perbaikan diterapkan:** Flag `--pre` telah dihapus dari ketiga berkas `requirements.txt`.

---

## KI-004 — Dockerfile Menggunakan `python:3.14-slim` (Gambar Dasar Prarilis)

**Status:** Terbuka | **Tingkat Keparahan:** 🟡 Rendah

### Deskripsi

Semua `Dockerfile` menggunakan `FROM python:3.14-slim` yang mengikuti build Python prarilis.
Untuk penempatan produksi, ini sebaiknya dipin ke rilis stabil (misalnya, `python:3.12-slim`).

### Berkas yang terdampak

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Referensi

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berusaha untuk akurat, harap diketahui bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sah. Untuk informasi penting, disarankan penerjemahan oleh penerjemah manusia profesional. Kami tidak bertanggung jawab atas kesalahpahaman atau kesalahan tafsir yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->