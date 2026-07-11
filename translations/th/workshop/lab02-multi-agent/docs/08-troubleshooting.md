# โมดูล 8 - การแก้ไขปัญหา

โมดูลนี้ครอบคลุมถึงข้อผิดพลาดทั่วไป, วิธีแก้ไข และกลยุทธ์การดีบั๊กที่เฉพาะเจาะจงสำหรับเวิร์กโฟลว์หลายตัวแทน

## ปัญหาผลลัพธ์ของตัวแทน

### GapAnalyzer แจ้งว่า “ฉันยังไม่มีรายงานที่ตรงกัน”

**อาการ:** การตอบกลับของ GapAnalyzer ขอให้คุณวางรายงานที่ตรงกันพร้อม “ทักษะที่ขาด” และ “ช่องว่างการรับรอง” ซึ่งเกิดขึ้นแม้ว่าคุณจะส่งทั้งเรซูเม่และคำบรรยายงานแล้ว

**สาเหตุ:** ข้อความคำบรรยายงานไม่ได้ถูกส่งต่อไปยัง JD Agent ด้วย `context_mode="last_agent"` `resume_executor` เป็นผู้ประมวลผลเดียวที่เห็นข้อความต้นฉบับของผู้ใช้ ถ้า `RESUME_PARSER_INSTRUCTIONS` ไม่มีข้อความคำบรรยายงานในผลลัพธ์ JD Agent จะไม่มีคำบรรยายให้อ่าน วิเคราะห์ได้ MatchingAgent จึงไม่สามารถคำนวณคะแนนความเหมาะสม และ GapAnalyzer จะได้รับข้อมูลเข้าแบบไม่มีความหมาย

**วิเคราะห์:**

ในบันทึกเซิร์ฟเวอร์ ให้ค้นหาช่วง MatchingAgent หากมันมี:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
 การส่งผ่านขาดหายหรือมีปัญหา

**แก้ไข:** ยืนยันว่า `RESUME_PARSER_INSTRUCTIONS` ใน `main.py` มีส่วน `[JOB DESCRIPTION PASS-THROUGH]` และกฎ:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
 และยืนยันว่า `JOB_DESCRIPTION_INSTRUCTIONS` มีส่วนกฎส่งต่อ `[PARSED RESUME PASS-THROUGH]` ด้วย:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
 ถ้ากลุ่มคำสั่งใดเป็นแบบร่างจากตัวช่วยสร้างโครงร่าง ให้แทนที่ด้วยเวอร์ชันสมบูรณ์จาก [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)

### MatchingAgent แสดงข้อความ “ไม่สามารถคำนวณคะแนนความเหมาะสม - ไม่มีคำบรรยายงาน”

นี่คือสาเหตุเดียวกับด้านบน MatchingAgent ได้รับผลลัพธ์จาก JD Agent แต่ส่วน `[PARSED RESUME PASS-THROUGH]` หายไปหรือว่างเปล่า จึงไม่สามารถเปรียบเทียบสองโปรไฟล์ได้ ยืนยัน:
1. `JOB_DESCRIPTION_INSTRUCTIONS` รวมกฎส่งต่อ: `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.`
2. `MATCHING_AGENT_INSTRUCTIONS` บอกตัวแทนให้ค้นหาส่วน `[JD REQUIREMENTS]` และ `[PARSED RESUME PASS-THROUGH]`

แทนที่กลุ่มคำสั่งทั้งสองด้วยเวอร์ชันสมบูรณ์จาก [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)

### การตอบกลับปรากฏซ้ำสองครั้ง

**อาการ:** ผลลัพธ์ GapAnalyzer (หรือผลลัพธ์ของท่อทั้งหมด) ปรากฏซ้ำในคำตอบของ Agent Inspector

**สาเหตุ:** `WorkflowBuilder` ใช้ตรรกะ OR สำหรับเส้นทางเข้า - ตัวดำเนินการถัดไปจะทำงานทันทีที่ **ผู้ใดผู้หนึ่ง** เสร็จสิ้น หาก `matching_executor` มีทางเข้า 2 ทาง (จาก `resume_executor` กับ `jd_executor`) มันจะทำงานสองครั้ง: ครั้งหนึ่งเมื่อ ResumeParser เสร็จ และอีกครั้งเมื่อ JD Agent เสร็จ GapAnalyzer ก็จะทำงานสองครั้งตามไปด้วย

**แก้ไข:** ให้แน่ใจว่าแผนภูมิ `WorkflowBuilder` เป็นท่อที่ทำงานตามลำดับอย่างเคร่งครัดโดยไม่มีการผสานสายเข้า:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # ไม่ใช่จาก resume_executor
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

หากมีบรรทัด `.add_edge(resume_executor, matching_executor)` ที่ไม่จำเป็น ให้ลบออก กฎส่งต่อ `[PARSED RESUME PASS-THROUGH]` ในผลลัพธ์ JD Agent ให้ MatchingAgent เข้าถึงเรซูเม่อยู่แล้ว

---

## ปัญหาสภาพแวดล้อมและการตั้งค่า

### ค่าที่ขาดหรือผิดในไฟล์ `.env`

ไฟล์ `.env` ต้องอยู่ในไดเรกทอรี `PersonalCareerCopilot/` (ระดับเดียวกับ `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

เนื้อหา `.env` ที่คาดหวัง:

**เส้นทาง A - Foundry บนคลาวด์:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**เส้นทาง B - Foundry Local:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> ทั้งสองเส้นทางใช้ `FOUNDRY_PROJECT_ENDPOINT` แต่ค่าจะแตกต่างกัน: คลาวด์ใช้ endpoint Foundry แบบ `https://` ส่วนท้องถิ่นใช้ `http://localhost:5273/v1` รัน `foundry model list` เพื่อตรวจสอบนามแฝงโมเดลที่ถูกต้องสำหรับเส้นทาง B

> **การหา `FOUNDRY_PROJECT_ENDPOINT` ของคุณ:** 
- เปิดแถบเครื่องมือ **Foundry Toolkit** ใน VS Code → คลิกขวาที่โปรเจกต์ของคุณ → **Copy Project Endpoint** 
- หรือไปที่ [Azure Portal](https://portal.azure.com) → โปรเจกต์ Foundry ของคุณ → **ภาพรวม** → **Project endpoint**

> **การหา `AZURE_AI_MODEL_DEPLOYMENT_NAME` ของคุณ:** ในแถบ Foundry Toolkit ขยายโปรเจกต์ → **Models** → หาชื่อโมเดลที่เผยแพร่ (เช่น `gpt-4.1-mini`)

### ลำดับความสำคัญของตัวแปร Env

`main.py` ใช้ `load_dotenv(override=True)` หมายความว่า:

| ความสำคัญ | แหล่งที่มา | ชนะเมื่อทั้งสองตั้งค่า? |
|----------|--------|------------------------|
| 1 (สูงสุด) | ไฟล์ `.env` | ใช่ |
| 2 | ตัวแปรแวดล้อมใน shell / container | ใช้เมื่อคีย์เดียวกันไม่มีใน `.env` |

ในการพัฒนาเครื่องท้องถิ่น `.env` เป็นแหล่งข้อมูลหลัก (แก้ไข `.env` ก็มีผลทันที) ในการใช้งานแบบโฮสต์ Foundry จะฉีดตัวแปรแวดล้อมบนระดับ container; เนื่องจาก `.env` ไม่ได้รวมอยู่ในอิมเมจที่เผยแพร่สำหรับการตั้งค่าห้องทดลองนี้ ค่าที่ฉีดเข้า container จึงถูกใช้งาน

---

## ความเข้ากันได้ของเวอร์ชัน

### ตารางเวอร์ชันของแพ็กเกจ

เวิร์กโฟลว์หลายตัวแทนต้องการเวอร์ชันแพ็กเกจเฉพาะ การใช้เวอร์ชันผิดจะทำให้เกิดข้อผิดพลาดขณะรันไทม์

| แพ็กเกจ | เวอร์ชันที่ต้องการ | คำสั่งตรวจสอบ |
|---------|-----------------|---------------|
| `agent-framework-foundry` | ล่าสุด | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | ล่าสุด | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | ล่าสุด | `pip show debugpy` |
| Python | 3.12+ | `python --version` |

### ข้อผิดพลาดเวอร์ชันทั่วไป

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# แก้ไข: ติดตั้ง agent-framework-foundry ใหม่
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# แก้ไข: อัปเกรดแพ็กเกจ mcp
pip install mcp --upgrade
```

### ตรวจสอบเวอร์ชันทั้งหมดพร้อมกัน

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

ผลลัพธ์ที่คาดหวัง:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## ปัญหาการนำไปใช้

### Container ไม่สามารถเริ่มหลังจากนำไปใช้

1. **ตรวจสอบบันทึก container:**
   - เปิดแถบเครื่องมือ **Foundry Toolkit** → ขยาย **Hosted Agents (Preview)** → คลิกตัวแทนของคุณ → ขยายเวอร์ชัน → **รายละเอียด container** → **บันทึก**
   - มองหาสต็อกเทรซ Python หรือข้อผิดพลาดโมดูลที่ขาด

2. **ความล้มเหลวในการเริ่ม container ที่พบบ่อย:**

   | ข้อผิดพลาดในบันทึก | สาเหตุ | วิธีแก้ |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | ขาดแพ็กเกจใน `requirements.txt` | เพิ่มแพ็กเกจและนำไปใช้ใหม่ |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | ตัวแปร env ใน `agent.yaml` หรือ `.env` ไม่ตั้งค่า | แก้ไขใน `agent.yaml` → ส่วน `environment_variables` (แบบโฮสต์) หรือ `.env` (แบบท้องถิ่น) |
   | `azure.identity.CredentialUnavailableError` | ยังไม่ได้กำหนด Managed Identity | Foundry ตั้งค่านี้อัตโนมัติ - ตรวจสอบว่าคุณนำไปใช้ผ่านส่วนขยาย |
   | `OSError: port 8088 already in use` | Dockerfile เปิดพอร์ตผิดหรือปัญหาพอร์ตซ้ำซ้อน | ตรวจสอบ `EXPOSE 8088` ใน Dockerfile และ `CMD ["python", "main.py"]` |
   | Container ออกด้วยโค้ด 1 | ข้อยกเว้นไม่ถูกจัดการใน `main()` | ทดสอบในเครื่องก่อน ([โมดูล 5](05-test-locally.md)) เพื่อตรวจจับข้อผิดพลาดก่อนนำไปใช้ |

3. **นำไปใช้ใหม่หลังแก้ไข:**
   - กด `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → เลือกตัวแทนเดิม → นำไปใช้เวอร์ชันใหม่

### ใช้เวลานำไปใช้นานเกินไป

Container ตัวแทนหลายตัวใช้เวลานานกว่าจะเริ่มเพราะสร้างอินสแตนซ์ตัวแทน 4 ตัวเมื่อเริ่มต้น เวลาปกติ:

| ขั้นตอน | ระยะเวลาคาดหวัง |
|-------|------------------|
| สร้างอิมเมจ container | 1-3 นาที |
| ส่งอิมเมจไปยัง ACR | 30-60 วินาที |
| เริ่ม container (ตัวแทนเดี่ยว) | 15-30 วินาที |
| เริ่ม container (หลายตัวแทน) | 30-120 วินาที |
| ตัวแทนพร้อมใช้งานใน Playground | 1-2 นาทีหลังจากสถานะ "Started" |

> หากสถานะ "Pending" ค้างนานเกิน 5 นาที ให้ตรวจสอบบันทึก container สำหรับข้อผิดพลาด

---

## ปัญหา RBAC และสิทธิ์อนุญาต

### `403 Forbidden` หรือ `AuthorizationFailed`

คุณต้องมีบทบาท **[Foundry User](https://aka.ms/foundry-ext-project-role)** ในโปรเจกต์ Foundry ของคุณ (ชื่อเดิมคือ **Azure AI User** - รหัสบทบาทไม่เปลี่ยน):

1. ไปที่ [Azure Portal](https://portal.azure.com) → ทรัพยากรโปรเจกต์ Foundry ของคุณ
2. คลิก **Access control (IAM)** → **Role assignments**
3. ค้นหาชื่อของคุณ → ยืนยันมี **Foundry User** (หรือป้ายชื่อเก่า **Azure AI User**)
4. หากหายไป: **เพิ่ม** → **Add role assignment** → ค้นหา **Foundry User** → กำหนดให้บัญชีของคุณ

ดูเอกสาร [RBAC สำหรับ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) สำหรับรายละเอียด

### ไม่สามารถเข้าถึงการนำโมเดลไปใช้

หากตัวแทนรายงานข้อผิดพลาดเกี่ยวกับโมเดล:

1. ตรวจสอบว่าโมเดลถูกนำไปใช้แล้ว: ขยายโปรเจกต์ในแถบ Foundry → **Models** → ตรวจสอบ `gpt-4.1-mini` (หรือโมเดลของคุณ) ว่ามีสถานะ **Succeeded**
2. ตรวจสอบชื่อการนำไปใช้ตรงกัน: เปรียบเทียบ `AZURE_AI_MODEL_DEPLOYMENT_NAME` ใน `.env` (หรือ `agent.yaml`) กับชื่อจริงในแถบ
3. หากการนำไปใช้หมดอายุ (ระดับฟรี): นำไปใช้ใหม่จาก [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**)

---

## ปัญหา Foundry Local (เส้นทาง B)

### บริการ Foundry Local ไม่ทำงาน

```powershell
# ตรวจสอบสถานะ
foundry local status

# เริ่มบริการหากบริการถูกหยุดอยู่
foundry local start
```

| อาการ | สาเหตุ | วิธีแก้ |
|---------|-------|-----|
| ตรวจสอบสุขภาพรีเทิร์น `503` | บริการยังไม่เริ่ม | รัน `foundry local start` หรือคลิก **Start** ในแถบ Foundry Toolkit |
| ตรวจสอบสุขภาพหมดเวลารอ | โมเดลกำลังโหลด | รอ 30–60 วินาทีหลังเริ่ม; โมเดลใหญ่จะช้ากว่า |
| `StatusCode: 404` บน `/v1/health` | พอร์ตไม่ถูกต้อง | ค่าเริ่มต้นคือ `5273` ตรวจสอบพอร์ตจริงด้วย `foundry local status` |
| ทรัพยากรไม่พอ | Foundry Local ต้องการ RAM ว่างประมาณ 4 GB | ปิดแอปอื่น ๆ |
| ดาวน์โหลดโมเดลล้มเหลว | พื้นที่ดิสก์น้อย | โมเดลมีขนาด 2–8 GB เคลียร์พื้นที่แล้วรัน `foundry model pull <name>` |

### ชื่อโมเดลไม่ตรงกัน

```powershell
# แสดงรายการโมเดลที่ดาวน์โหลดและนามแฝงที่แน่นอนของพวกเขา
foundry model list
```

ตั้งค่า `AZURE_AI_MODEL_DEPLOYMENT_NAME` ใน `.env` เป็นนามแฝงที่แสดงเป๊ะ (เช่น `phi-4-mini` ไม่ใช่ `Phi-4-mini`)

### `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` เมื่อรันท้องถิ่น (เส้นทาง B)

`main.py` ของห้องทดลองใช้ `os.environ["FOUNDRY_PROJECT_ENDPOINT"]` Foundry Local ต้องการตัวแปรนี้ชี้ไปยังบริการท้องถิ่น - **ไม่ใช่** `AZURE_AI_PROJECT_ENDPOINT` ตรวจสอบว่า `.env` ของคุณมี:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### เครื่องมือ MCP ยังส่งคำขอออก (เส้นทาง B)

นี่เป็นเรื่องปกติ เครื่องมือ `search_microsoft_learn_for_plan` ดึงข้อมูลทรัพยากรการเรียนรู้จาก `https://learn.microsoft.com/api/mcp` **มีเพียงการค้นหาชื่อทักษะ** เท่านั้นที่ส่งทางเครือข่าย - ข้อความเรซูเม่และคำบรรยายงานถูกประมวลผลทั้งหมดในอุปกรณ์ของคุณและไม่ถูกส่งออก หากต้องการทำงานแบบออฟไลน์เต็มรูปแบบ ให้เพิ่มการจับข้อผิดพลาด `try/except` ในเครื่องมือเพื่อคืนค่า URL `learn.microsoft.com` คงที่เมื่อไม่สามารถเข้าถึง endpoint ได้

---

## การขอความช่วยเหลือ

หากคุณติดขัดหลังจากลองแก้ไขด้านบน:

1. **ตรวจสอบบันทึกเซิร์ฟเวอร์** - ข้อผิดพลาดส่วนใหญ่จะแสดงสแตกเทรซ Python ในเทอร์มินัล อ่านรายละเอียดการเรียกซ้ำทั้งหมด
2. **ค้นหาข้อความผิดพลาด** - คัดลอกข้อความข้อผิดพลาดแล้วค้นหาใน [Microsoft Q&A สำหรับ Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)
3. **เปิดประเด็นใหม่** - แจ้งปัญหาใน [ที่เก็บเวิร์กช็อป](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) พร้อม:
   - ข้อความข้อผิดพลาดหรือภาพหน้าจอ
   - เวอร์ชันแพ็กเกจของคุณ (`pip list | Select-String "agent-framework"`)
   - เวอร์ชัน Python ของคุณ (`python --version`)
   - ระบุว่าปัญหาเป็นในเครื่องหรือหลังนำไปใช้

---

### จุดตรวจสอบ

- [ ] คุณรู้วิธีตรวจสอบและแก้ไขปัญหาการตั้งค่า `.env`
- [ ] คุณสามารถยืนยันเวอร์ชันแพ็กเกจว่าตรงกับตารางที่ต้องการ
- [ ] คุณรู้วิธีตรวจสอบบันทึก container สำหรับความล้มเหลวของการนำไปใช้
- [ ] คุณสามารถยืนยันบทบาท RBAC ใน Azure Portal

---

**ก่อนหน้า:** [07 - ตรวจสอบใน Playground](07-verify-in-playground.md) · **ถัดไป:** [09 - สรุป →](09-summary.md) · **หน้าแรก:** [Lab 02 README](../README.md) · [หน้าแรกของเวิร์กช็อป](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->