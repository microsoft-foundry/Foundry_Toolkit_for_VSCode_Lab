# เวิร์กช็อป Foundry Toolkit + Foundry Hosted Agents

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.1.0%2B-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

สร้าง ทดสอบ และนำ AI agents ไปใช้ที่ **Microsoft Foundry Agent Service** ในฐานะ **Hosted Agents** - ทั้งหมดนี้ทำได้จาก VS Code โดยใช้ **ส่วนขยาย Microsoft Foundry** และ **Foundry Toolkit**

> **Hosted Agents กำลังอยู่ในสถานะพรีวิว** ปัจจุบันรองรับเฉพาะบางภูมิภาคเท่านั้น - ดูได้ที่ [region availability](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)

> โฟลเดอร์ `agent/` ภายในแต่ละแลปจะถูก **สร้างขึ้นโดยอัตโนมัติ** โดยส่วนขยาย Foundry - คุณสามารถปรับแต่งโค้ด ทดสอบในเครื่อง และนำไปใช้งานได้เลย

### 🌐 รองรับหลายภาษา

#### รองรับผ่าน GitHub Action (อัตโนมัติและทันสมัยตลอดเวลา)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](../ko/README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](./README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **ต้องการโคลนแบบโลคัล?**
>
> รีโพสโพซิทอรีนี้มีการแปลมากกว่า 50 ภาษา ซึ่งจะทำให้ขนาดการดาวน์โหลดใหญ่ขึ้นมาก หากต้องการโคลนโดยไม่มีภาษาอื่น ๆ ให้ใช้ sparse checkout:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
> cd Foundry_Toolkit_for_VSCode_Lab
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> วิธีนี้จะได้ขนาดไฟล์ที่เล็กกว่าและดาวน์โหลดได้รวดเร็วขึ้นสำหรับการเรียนคอร์สนี้
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## สถาปัตยกรรม

```mermaid
flowchart TB
    subgraph Local["พัฒนาในเครื่อง (VS Code)"]
        direction TB
        FE["Microsoft Foundry
        Extension"]
        FoundryToolkit["Foundry Toolkit
        Extension"]
        Scaffold["Scaffolded Agent Code
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["Agent Inspector
        (Local Testing)"]
        FE -- "Create New
        Hosted Agent" --> Scaffold
        Scaffold -- "ดีบักด้วย F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["Foundry Agent Service
        (Hosted Agent Runtime)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["Foundry Playground
        & VS Code Playground"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "Deploy
    (Docker build + push)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> โครงสร้างพื้นฐาน
    Playground -- "ทดสอบคำสั่งกระตุ้น" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```

**ลำดับการทำงาน:** ส่วนขยาย Foundry จะสร้างโครงร่างตัวแทน → คุณปรับแต่งโค้ดและคำสั่ง → ทดสอบในเครื่องด้วย Agent Inspector → นำไปใช้ที่ Foundry (ส่ง Docker image เข้า ACR) → ตรวจสอบใน Playground

---

## สิ่งที่คุณจะสร้าง

| แลป | คำอธิบาย | สถานะ |
|-----|-------------|--------|
| **แลป 01 - ตัวแทนเดี่ยว** | สร้าง **ตัวแทน "อธิบายเหมือนคุณเป็นผู้บริหาร"** ทดสอบในเครื่อง และนำไปใช้กับ Foundry | ✅ พร้อมใช้งาน |
| **แลป 02 - เวิร์กโฟลว์ตัวแทนหลายคน** | สร้าง **"รีซูเม่ → ตัวประเมินความเหมาะสมงาน"** - ตัวแทน 4 คนร่วมกันให้คะแนนความเหมาะสมและสร้างแผนการเรียนรู้ | ✅ พร้อมใช้งาน |

---

## รู้จักตัวแทนผู้บริหาร

ในเวิร์กช็อปนี้คุณจะสร้าง **"ตัวแทนอธิบายเหมือนคุณเป็นผู้บริหาร"** - ตัวแทน AI ที่แปลศัพท์เทคนิคที่ซับซ้อนเป็นสรุปที่สงบและพร้อมใช้ในการประชุมคณะกรรมการ เพราะพูดตามตรง ไม่มีใครในระดับ C-suite อยากฟังเรื่อง "thread pool exhaustion caused by synchronous calls introduced in v3.2."

ฉันสร้างตัวแทนนี้หลังจากประสบเหตุหลายครั้งที่รายงานสภาพที่ฉันเขียนมาอย่างดีที่สุดกลับได้รับคำตอบ: *"งั้น... เว็บไซต์ล่มหรือไม่ล่มกันแน่?"*

### มันทำงานอย่างไร

คุณใส่ข้อมูลอัปเดตทางเทคนิคเข้าไป ตัวแทนจะตอบกลับด้วยสรุปสำหรับผู้บริหาร - 3 ประเด็นหลัก ไม่มีศัพท์เทคนิค ไม่มี trace ของ error ไม่มีความวิตกกังวล แค่ **เกิดอะไรขึ้น**, **ผลกระทบทางธุรกิจ**, และ **ขั้นตอนต่อไป**

### ดูมันทำงาน

**คุณพูดว่า:**
> "ความหน่วงของ API เพิ่มขึ้นเนื่องจาก thread pool หมดตัวเพราะ synchronous calls ที่เริ่มใช้ใน v3.2"

**ตัวแทนตอบว่า:**

> **สรุปสำหรับผู้บริหาร:**
> - **เกิดอะไรขึ้น:** หลังจากปล่อยเวอร์ชันล่าสุด ระบบทำงานช้าลง
> - **ผลกระทบทางธุรกิจ:** ผู้ใช้บางส่วนพบความล่าช้าในการใช้บริการ
> - **ขั้นตอนต่อไป:** ได้ยกเลิกรุ่นนี้และกำลังเตรียมแก้ไขก่อนนำไปใช้ใหม่

### ทำไมต้องตัวแทนนี้?

มันเป็นตัวแทนที่ง่ายและเน้นจุดประสงค์เดียว - เหมาะสำหรับเรียนรู้เวิร์กโฟลว์ของ hosted agent ตั้งแต่ต้นจนจบโดยไม่ต้องยุ่งกับเครื่องมือที่ซับซ้อน และจริงๆ แล้ว? ทุกทีมวิศวกรรมก็ควรมีตัวนี้

---

## โครงสร้างเวิร์กช็อป

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-setup.md
    │   │   ├── 02-create-hosted-agent.md
    │   │   ├── 03-configure-and-code.md
    │   │   ├── 04-test-locally.md
    │   │   ├── 05-deploy-to-foundry.md
    │   │   ├── 06-verify-in-playground.md
    │   │   ├── 07-summary.md
    │   │   └── 08-troubleshooting.md
    │   └── 📂 agent/                 ← Reference solution (auto-scaffolded by Foundry extension)
    │       ├── agent.yaml
    │       ├── Dockerfile
    │       ├── main.py
    │       └── requirements.txt
    └── 📂 lab02-multi-agent/         ← Resume → Job Fit Evaluator
        ├── README.md                 ← Hands-on lab instructions (end-to-end)
        ├── 📂 docs/                  ← Step-by-step tutorial modules
        │   ├── 00-prerequisites.md
        │   ├── 01-understand-multi-agent.md
        │   ├── 02-scaffold-multi-agent.md
        │   ├── 03-configure-agents.md
        │   ├── 04-orchestration-patterns.md
        │   ├── 05-test-locally.md
        │   ├── 06-deploy-to-foundry.md
        │   ├── 07-verify-in-playground.md
        │   └── 08-troubleshooting.md
        └── 📂 PersonalCareerCopilot/ ← Reference solution (multi-agent workflow)
            ├── agent.yaml
            ├── Dockerfile
            ├── main.py
            └── requirements.txt
```

> **หมายเหตุ:** โฟลเดอร์ `agent/` ภายในแต่ละแลปคือสิ่งที่ **ส่วนขยาย Microsoft Foundry** สร้างขึ้นเมื่อตอนคุณรันคำสั่ง `Microsoft Foundry: Create a New Hosted Agent` จาก Command Palette ไฟล์เหล่านี้จะถูกปรับแต่งด้วยคำสั่ง เครื่องมือ และการตั้งค่าของตัวแทนคุณ แลป 01 จะพาคุณสร้างสิ่งนี้จากศูนย์

---

## เริ่มต้น

### 1. โคลนรีโพสโพซิทอรี

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. สร้างสภาพแวดล้อมเสมือน Python

```bash
python -m venv venv
```

เปิดใช้งาน:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. ติดตั้ง dependencies

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. ตั้งค่าตัวแปรสภาพแวดล้อม

คัดลอกไฟล์ `.env` ตัวอย่างในโฟลเดอร์ agent และกรอกค่าของคุณ:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

แก้ไข `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. ทำตามแลปเวิร์กช็อป

แต่ละแลปมีโมดูลของตัวเอง เริ่มที่ **แลป 01** เพื่อเรียนรู้พื้นฐาน แล้วไปต่อที่ **แลป 02** สำหรับเวิร์กโฟลว์ตัวแทนหลายคน

#### แลป 01 - ตัวแทนเดี่ยว ([คำแนะนำเต็ม](workshop/lab01-single-agent/README.md))

| # | โมดูล | ลิงก์ |
|---|--------|------|
| 1 | อ่านความต้องการเบื้องต้น | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | ติดตั้ง Foundry Toolkit & ส่วนขยาย Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 3 | สร้างโปรเจกต์ Foundry | [01-setup.md](workshop/lab01-single-agent/docs/01-setup.md) |
| 4 | สร้าง hosted agent | [02-create-hosted-agent.md](workshop/lab01-single-agent/docs/02-create-hosted-agent.md) |
| 5 | ตั้งค่าคำสั่งและสภาพแวดล้อม | [03-configure-and-code.md](workshop/lab01-single-agent/docs/03-configure-and-code.md) |
| 6 | ทดสอบในเครื่อง | [04-test-locally.md](workshop/lab01-single-agent/docs/04-test-locally.md) |
| 7 | นำไปใช้ที่ Foundry | [05-deploy-to-foundry.md](workshop/lab01-single-agent/docs/05-deploy-to-foundry.md) |
| 8 | ตรวจสอบใน playground | [06-verify-in-playground.md](workshop/lab01-single-agent/docs/06-verify-in-playground.md) |
| 9 | แก้ไขปัญหา | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### แลป 02 - เวิร์กโฟลว์ตัวแทนหลายคน ([คำแนะนำเต็ม](workshop/lab02-multi-agent/README.md))

| # | โมดูล | ลิงก์ |
|---|--------|------|
| 1 | ความต้องการเบื้องต้น (แลป 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | เข้าใจสถาปัตยกรรมตัวแทนหลายคน | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | สร้างโครงร่างโปรเจกต์ตัวแทนหลายคน | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | ตั้งค่าตัวแทนและสภาพแวดล้อม | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | แพตเทิร์นการประสานงาน | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ทดสอบในเครื่อง (ตัวแทนหลายคน) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |

| 7 | เผยแพร่สู่ Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | ตรวจสอบใน playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | การแก้ไขปัญหา (multi-agent) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## ผู้ดูแลระบบ

<table>
<tr>
    <td align="center"><a href="https://github.com/ShivamGoyal03">
        <img src="https://github.com/ShivamGoyal03.png" width="100px;" alt="Shivam Goyal"/><br />
        <sub><b>Shivam Goyal</b></sub>
    </a><br />
    </td>
</tr>
</table>

---

## สิทธิ์ที่ต้องการ (สรุปด่วน)

| สถานการณ์ | บทบาทที่ต้องการ |
|----------|---------------|
| สร้างโปรเจ็กต์ Foundry ใหม่ | **เจ้าของ Azure AI** บนทรัพยากร Foundry |
| เผยแพร่สู่โปรเจ็กต์ที่มีอยู่ (ทรัพยากรใหม่) | **เจ้าของ Azure AI** + **ผู้ร่วมมือ** บนการสมัครใช้งาน |
| เผยแพร่สู่โปรเจ็กต์ที่ตั้งค่าแล้วทั้งหมด | **ผู้อ่าน** บัญชี + **ผู้ใช้ Azure AI** บนโปรเจ็กต์ |

> **สำคัญ:** บทบาท `เจ้าของ` และ `ผู้ร่วมมือ` ของ Azure รวมเพียงสิทธิ์ *การจัดการ* เท่านั้น ไม่รวมสิทธิ์ *การพัฒนา* (การดำเนินการกับข้อมูล) คุณต้องมี **ผู้ใช้ Azure AI** หรือ **เจ้าของ Azure AI** เพื่อสร้างและเผยแพร่เอเจนต์

---

## แหล่งอ้างอิง

- [เริ่มต้นด่วน: เผยแพร่เอเจนต์โฮสต์ตัวแรกของคุณ (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [เอเจนต์โฮสต์คืออะไร?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [สร้างเวิร์กโฟลว์เอเจนต์โฮสต์ใน VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [เผยแพร่เอเจนต์โฮสต์](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC สำหรับ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ตัวอย่างเอเจนต์ตรวจสอบสถาปัตยกรรม](https://github.com/Azure-Samples/agent-architecture-review-sample) - เอเจนต์โฮสต์ใช้งานจริงพร้อมเครื่องมือ MCP, แผนภาพ Excalidraw และการเผยแพร่สองทาง

---


## ใบอนุญาต

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->