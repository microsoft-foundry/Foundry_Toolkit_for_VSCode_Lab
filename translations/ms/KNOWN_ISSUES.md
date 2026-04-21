# Isu Dikenali

Dokumen ini menjejaki isu yang diketahui dengan keadaan repositori semasa.

> Dikemaskini terakhir: 2026-04-15. Diuji dengan Python 3.13 / Windows dalam `.venv_ga_test`.

---

## Pin Pakej Semasa (ketiga-tiga ejen)

| Pakej | Versi Semasa |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(tetap — lihat KI-003)* |

---

## KI-001 — Kemas Kini GA 1.0.0 Disekat: `agent-framework-azure-ai` Dibuang

**Status:** Terbuka | **Keterukan:** 🔴 Tinggi | **Jenis:** Memecahkan

### Penerangan

Pakej `agent-framework-azure-ai` (dipin pada `1.0.0rc3`) telah **dibuang/dihentikan**
dalam keluaran GA (1.0.0, dikeluarkan 2026-04-02). Ia digantikan oleh:

- `agent-framework-foundry==1.0.0` — corak ejen yang dihoskan oleh Foundry
- `agent-framework-openai==1.0.0` — corak ejen disokong oleh OpenAI

Ketiga-tiga fail `main.py` mengimport `AzureAIAgentClient` daripada `agent_framework.azure`, yang
menimbulkan `ImportError` di bawah pakej GA. Namespace `agent_framework.azure` masih wujud
dalam GA tetapi kini hanya mengandungi kelas Fungsi Azure (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — bukan ejen Foundry.

### Ralat Disahkan (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### Fail terjejas

| Fail | Baris |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` Tidak Serasi dengan GA `agent-framework-core`

**Status:** Terbuka | **Keterukan:** 🔴 Tinggi | **Jenis:** Memecahkan (disekat oleh hulu)

### Penerangan

`azure-ai-agentserver-agentframework==1.0.0b17` (terkini) mengikat ketat
`agent-framework-core<=1.0.0rc3`. Memasang ia bersama dengan `agent-framework-core==1.0.0` (GA)
memaksa pip untuk **menurunkan** `agent-framework-core` kembali ke `rc3`, yang kemudian memecahkan
`agent-framework-foundry==1.0.0` dan `agent-framework-openai==1.0.0`.

Panggilan `from azure.ai.agentserver.agentframework import from_agent_framework` yang digunakan oleh semua
ejen untuk mengikat pelayan HTTP juga disekat.

### Konflik pergantungan Disahkan (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### Fail terjejas

Ketiga-tiga fail `main.py` — sama ada import peringkat atas dan import dalam fungsi `main()`.

---

## KI-003 — Bendera `agent-dev-cli --pre` Tidak Lagi Diperlukan

**Status:** ✅ Diperbaiki (tidak memecahkan) | **Keterukan:** 🟢 Rendah

### Penerangan

Semua fail `requirements.txt` sebelum ini menyertakan `agent-dev-cli --pre` untuk menarik
CLI prarilis. Sejak GA 1.0.0 dikeluarkan pada 2026-04-02, keluaran stabil
`agent-dev-cli` kini tersedia tanpa bendera `--pre`.

**Pembaikan diterapkan:** Bendera `--pre` telah dikeluarkan dari ketiga-tiga fail `requirements.txt`.

---

## KI-004 — Dockerfiles Menggunakan `python:3.14-slim` (Imej Asas Prarilis)

**Status:** Terbuka | **Keterukan:** 🟡 Rendah

### Penerangan

Semua `Dockerfile` menggunakan `FROM python:3.14-slim` yang menjejaki binaan Python prarilis.
Untuk pengeluaran, ini harus dipin kepada keluaran stabil (contohnya, `python:3.12-slim`).

### Fail terjejas

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## Rujukan

- [agent-framework-core di PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry di PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila maklum bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat kritikal, terjemahan profesional oleh manusia adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->