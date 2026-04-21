# ปัญหาที่ทราบ

เอกสารนี้ติดตามปัญหาที่ทราบกับสถานะที่เก็บปัจจุบัน

> อัปเดตล่าสุด: 2026-04-15 ทดสอบกับ Python 3.13 / Windows ใน `.venv_ga_test`

---

## การตรึงแพ็กเกจปัจจุบัน (ทั้งสามตัวแทน)

| แพ็กเกจ | เวอร์ชั่นปัจจุบัน |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(แก้ไขแล้ว — ดู KI-003)* |

---

## KI-001 — การอัปเกรด GA 1.0.0 ถูกบล็อก: `agent-framework-azure-ai` ถูกลบ

**สถานะ:** เปิด | **ความรุนแรง:** 🔴 สูง | **ประเภท:** ทำให้เกิดความเสียหาย

### คำอธิบาย

แพ็กเกจ `agent-framework-azure-ai` (ตรึงที่ `1.0.0rc3`) ถูก **ลบ/เลิกใช้**
ในเวอร์ชั่น GA (1.0.0, ปล่อย 2026-04-02) แทนด้วย:

- `agent-framework-foundry==1.0.0` — รูปแบบตัวแทนที่โฮสต์โดย Foundry
- `agent-framework-openai==1.0.0` — รูปแบบตัวแทนที่ใช้ OpenAI

ไฟล์ `main.py` ทั้งสามไฟล์นำเข้า `AzureAIAgentClient` จาก `agent_framework.azure` ซึ่ง
ทำให้เกิด `ImportError` ภายใต้แพ็กเกจ GA. `agent_framework.azure` namespace ยังมีอยู่
ใน GA แต่ตอนนี้ประกอบด้วยเฉพาะคลาส Azure Functions (`DurableAIAgent`,
`AzureAISearchContextProvider`, `CosmosHistoryProvider`) — ไม่ใช่ตัวแทน Foundry.

### ข้อผิดพลาดที่ยืนยันแล้ว (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### ไฟล์ที่ได้รับผลกระทบ

| ไฟล์ | บรรทัด |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` ไม่เข้ากันกับ GA `agent-framework-core`

**สถานะ:** เปิด | **ความรุนแรง:** 🔴 สูง | **ประเภท:** ทำให้เกิดความเสียหาย (ถูกบล็อกโดยต้นน้ำ)

### คำอธิบาย

`azure-ai-agentserver-agentframework==1.0.0b17` (ล่าสุด) ตรึงเข้มข้น
`agent-framework-core<=1.0.0rc3`. การติดตั้งพร้อมกับ `agent-framework-core==1.0.0` (GA)
ทำให้ pip ต้อง **ดาวน์เกรด** `agent-framework-core` กลับไปเป็น `rc3` ซึ่งจะทำให้
`agent-framework-foundry==1.0.0` และ `agent-framework-openai==1.0.0` เสียหาย

คำสั่ง `from azure.ai.agentserver.agentframework import from_agent_framework` ที่ใช้โดยตัวแทนทั้งหมดเพื่อนำไปผูกกับเซิร์ฟเวอร์ HTTP จึงถูกบล็อกเช่นกัน

### ความขัดแย้งของการพึ่งพาที่ยืนยันแล้ว (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### ไฟล์ที่ได้รับผลกระทบ

ไฟล์ `main.py` ทั้งสามไฟล์ — ทั้งการนำเข้าระดับบนและการนำเข้าในฟังก์ชัน `main()`.

---

## KI-003 — ไม่ต้องใช้แฟล็ก `agent-dev-cli --pre` อีกต่อไป

**สถานะ:** ✅ แก้ไขแล้ว (ไม่ทำให้เสียหาย) | **ความรุนแรง:** 🟢 ต่ำ

### คำอธิบาย

ไฟล์ `requirements.txt` ทั้งหมดเคยระบุ `agent-dev-cli --pre` เพื่อดึง CLI เวอร์ชันก่อนปล่อย เนื่องจาก GA 1.0.0 ถูกปล่อยในวันที่ 2026-04-02 เวอร์ชันปล่อยเสถียรของ `agent-dev-cli` จึงพร้อมใช้งานโดยไม่ต้องใช้แฟล็ก `--pre`

**วิธีแก้ไขที่นำมาใช้:** แฟล็ก `--pre` ถูกลบออกจากไฟล์ `requirements.txt` ทั้งสามไฟล์แล้ว

---

## KI-004 — Dockerfiles ใช้ `python:3.14-slim` (ภาพพื้นฐานก่อนปล่อย)

**สถานะ:** เปิด | **ความรุนแรง:** 🟡 ต่ำ

### คำอธิบาย

`Dockerfile` ทั้งหมดใช้ `FROM python:3.14-slim` ซึ่งติดตามการสร้าง Python ก่อนปล่อย สำหรับการใช้งานจริงควรตรึงเป็นเวอร์ชันเสถียร (เช่น `python:3.12-slim`)

### ไฟล์ที่ได้รับผลกระทบ

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## แหล่งอ้างอิง

- [agent-framework-core บน PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry บน PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ข้อจำกัดความรับผิดชอบ**:  
เอกสารฉบับนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้เราจะพยายามให้มีความถูกต้องสูงสุด แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความคลาดเคลื่อน เอกสารต้นฉบับในภาษาดั้งเดิมควรถือเป็นแหล่งข้อมูลที่ได้รับการยอมรับอย่างเป็นทางการ สำหรับข้อมูลที่สำคัญ ควรใช้บริการแปลโดยมนุษย์มืออาชีพ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดใดๆ ที่เกิดจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->