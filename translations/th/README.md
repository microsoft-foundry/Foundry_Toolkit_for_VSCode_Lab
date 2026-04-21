# ชุดเครื่องมือ Foundry + เวิร์กช็อปตัวแทนโฮสต์ Foundry

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Agent Framework](https://img.shields.io/badge/Microsoft%20Agent%20Framework-v1.0.0rc3-5E5ADB?logo=microsoft&logoColor=white)](https://github.com/microsoft/agents)
[![Hosted Agents](https://img.shields.io/badge/Hosted%20Agents-Enabled-5E5ADB?logo=microsoft&logoColor=white)](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/hosted-agents/)
[![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agent%20Service-0078D4?logo=microsoft&logoColor=white)](https://ai.azure.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4.1-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/ai-services/openai/)
[![Azure CLI](https://img.shields.io/badge/Azure%20CLI-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/cli/azure/install-azure-cli)
[![Azure Developer CLI](https://img.shields.io/badge/azd-Required-0078D4?logo=microsoftazure&logoColor=white)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
[![Docker](https://img.shields.io/badge/Docker-Optional-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

สร้าง ทดสอบ และปรับใช้เอเย่นต์ AI ไปยัง **บริการเอเย่นต์ Microsoft Foundry** ในฐานะ **เอเย่นต์โฮสต์** - ทั้งหมดทำได้จาก VS Code โดยใช้ **ส่วนขยาย Microsoft Foundry** และ **ชุดเครื่องมือ Foundry**.

> **เอเย่นต์โฮสต์ ตอนนี้อยู่ในสถานะพรีวิว** เขตที่สนับสนุมนั้นจำกัด - ดูเพิ่มเติมได้ที่ [ความพร้อมใช้งานตามภูมิภาค](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability).

> โฟลเดอร์ `agent/` ภายในแต่ละห้องปฏิบัติการจะถูก **สร้างขึ้นอัตโนมัติ** โดยส่วนขยาย Foundry - จากนั้นคุณสามารถปรับแต่งโค้ด ทดสอบในเครื่อง และปรับใช้ได้.

### 🌐 รองรับหลายภาษา

#### รองรับผ่าน GitHub Action (อัตโนมัติ & อัปเดตเสมอ)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[ภาษาอาหรับ](../ar/README.md) | [ภาษาเบงกาลี](../bn/README.md) | [ภาษาบัลแกเรีย](../bg/README.md) | [ภาษาพม่า (เมียนมา)](../my/README.md) | [ภาษาจีน (ตัวย่อ)](../zh-CN/README.md) | [ภาษาจีนดั้งเดิม (ฮ่องกง)](../zh-HK/README.md) | [ภาษาจีนดั้งเดิม (มาเก๊า)](../zh-MO/README.md) | [ภาษาจีนดั้งเดิม (ไต้หวัน)](../zh-TW/README.md) | [ภาษาโครเอเชีย](../hr/README.md) | [ภาษาเช็ก](../cs/README.md) | [ภาษาเดนมาร์ก](../da/README.md) | [ภาษาดัตช์](../nl/README.md) | [ภาษาเอสโตเนีย](../et/README.md) | [ภาษาฟินแลนด์](../fi/README.md) | [ภาษาฝรั่งเศส](../fr/README.md) | [ภาษาเยอรมัน](../de/README.md) | [ภาษากรีก](../el/README.md) | [ภาษาฮิบรู](../he/README.md) | [ภาษาฮินดี](../hi/README.md) | [ภาษาฮังการี](../hu/README.md) | [ภาษาอินโดนีเซีย](../id/README.md) | [ภาษาอิตาเลียน](../it/README.md) | [ภาษาญี่ปุ่น](../ja/README.md) | [ภาษาคันนาดา](../kn/README.md) | [ภาษาเขมร](../km/README.md) | [ภาษาเกาหลี](../ko/README.md) | [ภาษาลิทัวเนีย](../lt/README.md) | [ภาษามาเลย์](../ms/README.md) | [ภาษามาลายาลัม](../ml/README.md) | [ภาษามราธี](../mr/README.md) | [ภาษาเนปาลี](../ne/README.md) | [ภาษาไนจีเรีย pidgin](../pcm/README.md) | [ภาษานอร์เวย์](../no/README.md) | [ภาษาเปอร์เซีย (ฟาร์ซี)](../fa/README.md) | [ภาษาโปแลนด์](../pl/README.md) | [ภาษาโปรตุเกส (บราซิล)](../pt-BR/README.md) | [ภาษาโปรตุเกส (โปรตุเกส)](../pt-PT/README.md) | [ภาษาปัญจาบ (กูรมุขิ)](../pa/README.md) | [ภาษาโรมาเนีย](../ro/README.md) | [ภาษารัสเซีย](../ru/README.md) | [ภาษาเซอร์เบียน (ขีริลลิก)](../sr/README.md) | [ภาษาสโลวัก](../sk/README.md) | [ภาษาสโลวีเนีย](../sl/README.md) | [ภาษาสเปน](../es/README.md) | [ภาษาสวาฮิลี](../sw/README.md) | [ภาษาสวีเดน](../sv/README.md) | [ภาษาตากาล็อก (ฟิลิปปินส์)](../tl/README.md) | [ภาษาทมิฬ](../ta/README.md) | [ภาษาเทลูกู](../te/README.md) | [ภาษาไทย](./README.md) | [ภาษาเตอร์กิช](../tr/README.md) | [ภาษายูเครน](../uk/README.md) | [ภาษาอูรดู](../ur/README.md) | [ภาษาเวียดนาม](../vi/README.md)

> **ต้องการโคลนไว้ในเครื่อง?**
>
> ที่เก็บนี้รวมการแปลมากกว่า 50 ภาษา ซึ่งเพิ่มขนาดดาวน์โหลดอย่างมีนัยสำคัญ หากต้องการโคลนโดยไม่รวมการแปล ให้ใช้ sparse checkout:
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
> วิธีนี้จะให้ทุกอย่างที่คุณต้องการเพื่อทำคอร์สนี้ให้เสร็จรวดเร็วขึ้นมาก
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## สถาปัตยกรรม

```mermaid
flowchart TB
    subgraph Local["การพัฒนาในเครื่อง (VS Code)"]
        direction TB
        FE["ส่วนขยาย Microsoft Foundry"]
        FoundryToolkit["ส่วนขยาย Foundry Toolkit"]
        Scaffold["รหัสตัวแทนแบบ Scaffolded
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["ตัวตรวจสอบตัวแทน
        (ทดสอบในเครื่อง)"]
        FE -- "สร้างตัวแทนโฮสต์ใหม่" --> Scaffold
        Scaffold -- "ดีบัก F5" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["Microsoft Foundry"]
        direction TB
        ACR["Azure Container
        Registry"]
        AgentService["บริการตัวแทน Foundry
        (เวลารันตัวแทนโฮสต์)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["สนามเล่น Foundry
        & สนามเล่น VS Code"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "ปรับใช้
    (สร้าง + ดัน Docker)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "ทดสอบพร้อมท์" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**โฟลว์:** ส่วนขยาย Foundry สร้างโครงร่างเอเย่นต์ → คุณปรับแต่งโค้ดและคำสั่ง → ทดสอบในเครื่องด้วย Agent Inspector → ปรับใช้ไปยัง Foundry (ภาพ Docker ถูกส่งขึ้น ACR) → ตรวจสอบใน Playground.

---

## สิ่งที่คุณจะสร้าง

| ห้องปฏิบัติการ | คำอธิบาย | สถานะ |
|-----|-------------|--------|
| **ห้องปฏิบัติการ 01 - เอเย่นต์เดี่ยว** | สร้าง **"เอเย่นต์อธิบายเหมือนเป็นผู้บริหาร"** ทดสอบในเครื่อง และปรับใช้ไปยัง Foundry | ✅ มีให้ใช้งาน |
| **ห้องปฏิบัติการ 02 - เวิร์กโฟลว์หลายเอเย่นต์** | สร้าง **"ผู้ประเมินความเหมาะสมกับงานจากประวัติย่อ"** - เอเย่นต์ 4 ตัวร่วมกันให้คะแนนความเหมาะสมของประวัติย่อและสร้างแผนการเรียนรู้ | ✅ มีให้ใช้งาน |

---

## พบกับ Executive Agent

ในเวิร์กช็อปนี้คุณจะสร้าง **"เอเย่นต์อธิบายเหมือนเป็นผู้บริหาร"** - เอเย่นต์ AI ที่นำเทคนิคภาษาที่ยุ่งยากซับซ้อนและแปลงเป็นสรุปที่สงบเรียบร้อยพร้อมสำหรับห้องประชุมคณะกรรมการ เพราะต้องยอมรับว่าคนในซี-suite ไม่มีใครอยากฟังเรื่อง "thread pool exhaustion caused by synchronous calls introduced in v3.2."

ผมสร้างเอเย่นต์นี้หลังเหตุการณ์ที่โพสต์มอร์เท็มที่เตรียมไว้อย่างดีหลายครั้งได้รับคำตอบว่า: *"งั้น... เว็บไซต์ล่มหรือเปล่า?"*

### วิธีทำงาน

คุณป้อนการอัปเดตทางเทคนิคเข้าไป มันจะตอบกลับสรุปสำหรับผู้บริหาร - ประเด็นสำคัญสามข้อ ไม่มีศัพท์แสงเทคนิค ไม่มี stack traces ไม่มีความวิตกกังวลแต่อย่างใด แค่ **เกิดอะไรขึ้น**, **ผลกระทบทางธุรกิจ**, และ **ขั้นตอนถัดไป**.

### ดูตัวอย่างการใช้งาน

**คุณพูดว่า:**
> "ความหน่วงของ API เพิ่มขึ้นเนื่องจาก thread pool exhaustion caused by synchronous calls introduced in v3.2."

**เอเย่นต์ตอบกลับ:**

> **สรุปสำหรับผู้บริหาร:**
> - **เกิดอะไรขึ้น:** หลังจากปล่อยเวอร์ชันล่าสุด ระบบทำงานช้าลง
> - **ผลกระทบทางธุรกิจ:** ผู้ใช้บางรายประสบกับความล่าช้าในการใช้งานบริการ
> - **ขั้นตอนถัดไป:** เปลี่ยนแปลงถูกย้อนกลับ และกำลังเตรียมการแก้ไขก่อนนำไปปรับใช้ใหม่

### ทำไมถึงต้องเอเย่นต์นี้?

มันเป็นเอเย่นต์ที่ง่ายมาก ทำงานเฉพาะจุดเดียว — เหมาะสำหรับเรียนรู้เวิร์กโฟลว์เอเย่นต์โฮสต์แบบครบวงจรโดยไม่ต้องยุ่งกับสายเครื่องมือที่ซับซ้อน และอย่างซื่อสัตย์? ทุกทีมวิศวกรรมควรมีเอเย่นต์แบบนี้สักตัวหนึ่ง.

---

## โครงสร้างเวิร์กช็อป

```
📂 Foundry_Toolkit_for_VSCode_Lab/
├── 📄 README.md                      ← You are here
├── 📂 ExecutiveAgent/                ← Standalone hosted agent project
│   ├── agent.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── 📂 workshop/
    ├── 📂 lab01-single-agent/        ← Full lab: docs + agent code
    │   ├── README.md                 ← Hands-on lab instructions
    │   ├── 📂 docs/                  ← Step-by-step tutorial modules
    │   │   ├── 00-prerequisites.md
    │   │   ├── 01-install-foundry-toolkit.md
    │   │   ├── 02-create-foundry-project.md
    │   │   ├── 03-create-hosted-agent.md
    │   │   ├── 04-configure-and-code.md
    │   │   ├── 05-test-locally.md
    │   │   ├── 06-deploy-to-foundry.md
    │   │   ├── 07-verify-in-playground.md
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

> **หมายเหตุ:** โฟลเดอร์ `agent/` ภายในแต่ละห้องปฏิบัติการคือสิ่งที่ **ส่วนขยาย Microsoft Foundry** สร้างขึ้นเมื่อคุณรันคำสั่ง `Microsoft Foundry: Create a New Hosted Agent` จาก Command Palette จากนั้นไฟล์ต่างๆ จะถูกปรับแต่งด้วยคำสั่งและเครื่องมือของเอเย่นต์คุณ ห้องปฏิบัติการ 01 จะเดินคุณผ่านขั้นตอนการสร้างนี้ตั้งแต่ต้น.

---

## เริ่มต้นใช้งาน

### 1. โคลนที่เก็บข้อมูล

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. ตั้งค่าสภาพแวดล้อมเสมือน Python

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

### 4. กำหนดค่าตัวแปรสภาพแวดล้อม

คัดลอกไฟล์ตัวอย่าง `.env` ภายในโฟลเดอร์ agent แล้วกรอกค่าของคุณ:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

แก้ไข `workshop/lab01-single-agent/agent/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. ทำตามห้องปฏิบัติการเวิร์กช็อป

แต่ละห้องปฏิบัติการแยกตัวออกมาเป็นโมดูลของตัวเอง เริ่มที่ **ห้องปฏิบัติการ 01** เพื่อเรียนรู้พื้นฐาน จากนั้นไปต่อยัง **ห้องปฏิบัติการ 02** สำหรับเวิร์กโฟลว์หลายเอเย่นต์

#### ห้องปฏิบัติการ 01 - เอเย่นต์เดียว ([คำแนะนำเต็มรูปแบบ](workshop/lab01-single-agent/README.md))

| # | โมดูล | ลิงก์ |
|---|--------|------|
| 1 | อ่านข้อกำหนดเบื้องต้น | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | ติดตั้ง Foundry Toolkit & ส่วนขยาย Foundry | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | สร้างโปรเจกต์ Foundry | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | สร้างเอเย่นต์โฮสต์ | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | กำหนดคำสั่งและสภาพแวดล้อม | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | ทดสอบในเครื่อง | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | ปรับใช้ไปยัง Foundry | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | ตรวจสอบใน playground | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | แก้ไขปัญหา | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### ห้องปฏิบัติการ 02 - เวิร์กโฟลว์หลายเอเย่นต์ ([คำแนะนำเต็มรูปแบบ](workshop/lab02-multi-agent/README.md))

| # | โมดูล | ลิงก์ |
|---|--------|------|
| 1 | ข้อกำหนดเบื้องต้น (ห้องปฏิบัติการ 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | เข้าใจสถาปัตยกรรมหลายเอเย่นต์ | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | สร้างโครงโปรเจกต์หลายเอเย่นต์ | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | กำหนดค่าเอเย่นต์และสภาพแวดล้อม | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | รูปแบบการประสานงาน | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | ทดสอบในเครื่อง (หลายเอเย่นต์) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | ดีพลอยไปยัง Foundry | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | ยืนยันใน playground | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | แก้ไขปัญหา (หลายเอเจนต์) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## ผู้ดูแล

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

## สิทธิ์ที่จำเป็น (อ้างอิงด่วน)

| สถานการณ์ | บทบาทที่จำเป็น |
|----------|---------------|
| สร้างโปรเจกต์ Foundry ใหม่ | **Azure AI Owner** บนทรัพยากร Foundry |
| ดีพลอยไปยังโปรเจกต์ที่มีอยู่ (ทรัพยากรใหม่) | **Azure AI Owner** + **Contributor** บน subscription |
| ดีพลอยไปยังโปรเจกต์ที่ตั้งค่าเสร็จสมบูรณ์ | **Reader** บนบัญชี + **Azure AI User** บนโปรเจกต์ |

> **สำคัญ:** บทบาท Azure `Owner` และ `Contributor` มีสิทธิ์แค่ *การจัดการ* ไม่รวมสิทธิ์ *การพัฒนา* (การกระทำข้อมูล) คุณจะต้องใช้ **Azure AI User** หรือ **Azure AI Owner** สำหรับการสร้างและดีพลอยเอเจนต์

---

## เอกสารอ้างอิง

- [เริ่มต้นอย่างรวดเร็ว: ดีพลอยเอเจนต์โฮสต์ตัวแรกของคุณ (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [เอเจนต์โฮสต์คืออะไร?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [สร้างโฟลว์งานเอเจนต์โฮสต์ใน VS Code](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [ดีพลอยเอเจนต์โฮสต์](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [RBAC สำหรับ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [ตัวอย่างเอเจนต์รีวิวสถาปัตยกรรม](https://github.com/Azure-Samples/agent-architecture-review-sample) - เอเจนต์โฮสต์ในโลกความจริงกับเครื่องมือ MCP, แผนภาพ Excalidraw และดีพลอยสองทาง

---


## ใบอนุญาต

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษาด้วย AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้เราจะพยายามให้ความถูกต้องสูงสุด โปรดทราบว่าการแปลอัตโนมัติอาจประกอบด้วยข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นฉบับเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลโดยมนุษย์มืออาชีพ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดที่เกิดขึ้นจากการใช้การแปลฉบับนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->