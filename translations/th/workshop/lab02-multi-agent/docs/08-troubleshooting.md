# Module 8 - การแก้ไขปัญหา (Multi-Agent)

โมดูลนี้ครอบคลุมถึงข้อผิดพลาดทั่วไป การแก้ไข และกลยุทธ์การดีบักเฉพาะในเวิร์กโฟลว์มัลติเอเจนต์ สำหรับปัญหาการปรับใช้ Foundry ทั่วไป โปรดดูคู่มือแก้ไขปัญหา [Lab 01](../../lab01-single-agent/docs/08-troubleshooting.md) ด้วย

---

## อ้างอิงด่วน: ข้อผิดพลาด → การแก้ไข

| ข้อผิดพลาด / อาการ | สาเหตุที่เป็นไปได้ | วิธีแก้ไข |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | ไม่มีไฟล์ `.env` หรือค่าตัวแปรไม่ได้ตั้ง | สร้างไฟล์ `.env` พร้อม `PROJECT_ENDPOINT=<your-endpoint>` และ `MODEL_DEPLOYMENT_NAME=<your-model>` |
| `ModuleNotFoundError: No module named 'agent_framework'` | ยังไม่ได้เปิดใช้งาน virtual environment หรือยังไม่ได้ติดตั้ง dependencies | รัน `.\.venv\Scripts\Activate.ps1` จากนั้นรัน `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'mcp'` | ไม่ได้ติดตั้งแพ็กเกจ MCP (หายไปใน requirements) | รัน `pip install mcp` หรือเช็คให้แน่ใจว่าใน `requirements.txt` รวม MCP เป็น dependency แบบ transitve |
| ตัวเอเจนต์เริ่มทำงานแต่ได้การตอบกลับว่างเปล่า | `output_executors` ไม่ตรงกันหรือขอบที่ขาดหายไป | ตรวจสอบ `output_executors=[gap_analyzer]` และให้ทุกขอบอยู่ใน `create_workflow()` |
| มี Gap Card เพียงใบเดียว (ใบอื่นขาดหายไป) | คำสั่ง GapAnalyzer ไม่ครบถ้วน | เพิ่มย่อหน้าที่ขึ้นต้นด้วย `CRITICAL:` ใน `GAP_ANALYZER_INSTRUCTIONS` - ดู [Module 3](03-configure-agents.md) |
| คะแนน Fit เป็น 0 หรือไม่มี | MatchingAgent ไม่ได้รับข้อมูลขาเข้า | ตรวจสอบให้มีทั้ง `add_edge(resume_parser, matching_agent)` และ `add_edge(jd_agent, matching_agent)` |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP server ปฏิเสธคำขอเครื่องมือ | ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต ทดลองเปิด `https://learn.microsoft.com/api/mcp` ในเว็บเบราว์เซอร์ และลองใหม่ |
| ไม่มี URL Microsoft Learn ในผลลัพธ์ | MCP tool ไม่ได้ลงทะเบียนหรือตั้ง endpoint ผิดพลาด | ตรวจสอบ `tools=[search_microsoft_learn_for_plan]` บน GapAnalyzer และตรวจสอบว่า `MICROSOFT_LEARN_MCP_ENDPOINT` ถูกต้อง |
| `Address already in use: port 8088` | มีโปรเซสอื่นใช้พอร์ต 8088 อยู่ | รันคำสั่ง `netstat -ano \| findstr :8088` (Windows) หรือ `lsof -i :8088` (macOS/Linux) เพื่อตรวจหาและหยุดโปรเซสที่ขัดแย้ง |
| `Address already in use: port 5679` | ขัดแย้งพอร์ต debugpy | หยุดการดีบักอื่นๆ รัน `netstat -ano \| findstr :5679` เพื่อตรวจหาและฆ่าโปรเซส |
| Agent Inspector เปิดไม่ขึ้น | เซิร์ฟเวอร์ยังไม่เริ่มทำงานเต็มที่ หรือพอร์ตถูกขัดแย้ง | รอจนเห็นข้อความ "Server running" ในล็อก ตรวจสอบให้พอร์ต 5679 ว่าง |
| `azure.identity.CredentialUnavailableError` | ยังไม่ได้ลงชื่อเข้าใช้ Azure CLI | รันคำสั่ง `az login` จากนั้นเริ่มเซิร์ฟเวอร์ใหม่ |
| `azure.core.exceptions.ResourceNotFoundError` | การปรับใช้โมเดลไม่มีอยู่จริง | ตรวจสอบว่า `MODEL_DEPLOYMENT_NAME` ตรงกับโมเดลที่ปรับใช้ในโปรเจกต์ Foundry ของคุณ |
| สถานะคอนเทนเนอร์เป็น "Failed" หลังการปรับใช้ | คอนเทนเนอร์ล้มเหลวตอนเริ่มต้น | ตรวจสอบล็อกคอนเทนเนอร์ใน Foundry sidebar โดยทั่วไปมักเกิดจากตัวแปร env หายหรือ import ผิดพลาด |
| การปรับใช้แสดงสถานะ "Pending" นานเกิน 5 นาที | คอนเทนเนอร์ใช้เวลานานเกินไปในการเริ่มต้น หรือมีข้อจำกัดทรัพยากร | รอได้สูงสุด 5 นาทีสำหรับมัลติเอเจนต์ (จะสร้างอินสแตนซ์เอเจนต์ 4 ตัว) หากยังค้างอยู่ ให้เช็คล็อก |
| `ValueError` จาก `WorkflowBuilder` | กราฟการตั้งค่าไม่ถูกต้อง | ตรวจสอบว่า `start_executor` ถูกตั้งไว้, `output_executors` เป็น list และไม่มีขอบที่วนลูป |

---

## ปัญหาเกี่ยวกับสภาพแวดล้อมและการตั้งค่า

### ค่าตัวแปร `.env` หายหรือไม่ถูกต้อง

ไฟล์ `.env` จะต้องอยู่ในไดเรกทอรี `PersonalCareerCopilot/` (ระดับเดียวกับ `main.py`):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

เนื้อหาไฟล์ `.env` ที่คาดหวัง:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **วิธีหา PROJECT_ENDPOINT:**  
- เปิดแถบด้านข้าง **Microsoft Foundry** ใน VS Code → คลิกขวาโปรเจกต์ของคุณ → **Copy Project Endpoint**  
- หรือไปที่ [Azure Portal](https://portal.azure.com) → เลือกโปรเจกต์ Foundry ของคุณ → **Overview** → **Project endpoint**

> **วิธีหา MODEL_DEPLOYMENT_NAME:** ในแถบ Foundry ขยายโปรเจกต์ → **Models** → ค้นหาชื่อโมเดลที่ปรับใช้ (เช่น `gpt-4.1-mini`)

### ลำดับความสำคัญของตัวแปร env

`main.py` ใช้ `load_dotenv(override=False)` หมายความว่า:

| ลำดับความสำคัญ | แหล่งที่มา | ตัวใดได้รับการเลือกหากตั้งทั้งสอง? |
|----------|--------|------------------------|
| 1 (สูงสุด) | ตัวแปรใน shell environment | ใช่ |
| 2 | ไฟล์ `.env` | ใช้ก็ต่อเมื่อไม่มีตัวแปรใน shell |

ซึ่งหมายความว่าตัวแปรใน runtime ของ Foundry (ตั้งผ่าน `agent.yaml`) จะมีลำดับความสำคัญสูงกว่า `.env` ในการปรับใช้แบบโฮสต์

---

## ความเข้ากันได้ของเวอร์ชัน

### ตารางเวอร์ชันแพ็กเกจ

เวิร์กโฟลว์มัลติเอเจนต์ต้องการเวอร์ชันแพ็กเกจเฉพาะ หากเวอร์ชันผิดพลาดจะทำให้เกิดข้อผิดพลาดระหว่างรันไทม์

| แพ็กเกจ | เวอร์ชันที่ต้องใช้ | คำสั่งตรวจสอบ |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | รุ่น pre-release ล่าสุด | `pip show agent-dev-cli` |
| Python | 3.10+ | `python --version` |

### ข้อผิดพลาดเวอร์ชันทั่วไป

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# แก้ไข: อัปเกรดเป็น rc3
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**ไม่พบ `agent-dev-cli` หรือ Inspector ไม่เข้ากัน:**

```powershell
# แก้ไข: ติดตั้งด้วยแฟลก --pre
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# แก้ไข: อัปเกรดแพ็กเกจ mcp
pip install mcp --upgrade
```

### ตรวจสอบเวอร์ชันทั้งหมดพร้อมกัน

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

ผลลัพธ์ที่คาดหวัง:

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## ปัญหาเกี่ยวกับเครื่องมือ MCP

### MCP tool ไม่ส่งผลลัพธ์กลับมา

**อาการ:** Gap cards แสดงข้อความ "No results returned from Microsoft Learn MCP" หรือ "No direct Microsoft Learn results found"

**สาเหตุที่เป็นไปได้:**

1. **ปัญหาเครือข่าย** - MCP endpoint (`https://learn.microsoft.com/api/mcp`) ไม่สามารถเข้าถึงได้  
   ```powershell
   # ทดสอบการเชื่อมต่อ
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ถ้าคืนค่าเป็น `200` แสดงว่า endpoint เข้าถึงได้

2. **คำค้นเฉพาะเจาะจงเกินไป** - ชื่อทักษะเฉพาะเจาะจงเกินกว่าจะค้นหาใน Microsoft Learn  
   - เป็นเรื่องปกติสำหรับทักษะที่เฉพาะเจาะจงมาก ๆ เครื่องมือมี URL สำรองในผลลัพธ์

3. **หมดเวลาการเชื่อมต่อ MCP** - การเชื่อมต่อ Streamable HTTP หมดเวลา  
   - ลองส่งคำขอใหม่อีกครั้ง MCP session เป็นแบบชั่วคราวและอาจต้องเชื่อมต่อใหม่

### คำอธิบายล็อก MCP

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| ล็อก | ความหมาย | การดำเนินการ |
|-----|---------|--------|
| `GET → 405` | MCP client ตรวจสอบในช่วงเริ่มต้น | ปกติ - ให้ไม่สนใจ |
| `POST → 200` | เรียกใช้เครื่องมือสำเร็จ | คาดหวังได้ |
| `DELETE → 405` | MCP client ตรวจสอบตอนล้างข้อมูล | ปกติ - ให้ไม่สนใจ |
| `POST → 400` | คำขอผิดพลาด (query ไม่ถูกต้อง) | ตรวจสอบพารามิเตอร์ `query` ใน `search_microsoft_learn_for_plan()` |
| `POST → 429` | ถูกจำกัดอัตรา | รอแล้วลองใหม่ ลด `max_results` ในพารามิเตอร์ |
| `POST → 500` | MCP server เกิดข้อผิดพลาด | เป็นชั่วคราว - ทดลองใหม่ หากยังเป็นอยู่ API MCP ของ Microsoft Learn อาจล่ม |
| หมดเวลาการเชื่อมต่อ | ปัญหาเครือข่าย หรือ MCP server ใช้งานไม่ได้ | ตรวจสอบอินเทอร์เน็ต ลองรัน `curl https://learn.microsoft.com/api/mcp` |

---

## ปัญหาการปรับใช้

### คอนเทนเนอร์ล้มเหลวตอนเริ่มต้นหลังการปรับใช้

1. **ตรวจสอบล็อกคอนเทนเนอร์:**  
   - เปิดแถบด้านข้าง **Microsoft Foundry** → ขยาย **Hosted Agents (Preview)** → คลิกเอเจนต์ของคุณ → ขยายเวอร์ชัน → **Container Details** → **Logs**  
   - มองหา stack trace ของ Python หรือข้อผิดพลาดโมดูลหาย

2. **ข้อผิดพลาดทั่วไปตอนเริ่มคอนเทนเนอร์:**

   | ข้อผิดพลาดในล็อก | สาเหตุ | วิธีแก้ไข |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` หายแพ็กเกจ | เพิ่มแพ็กเกจใหม่แล้วปรับใช้ใหม่ |
   | `RuntimeError: Missing required environment variable` | ตัวแปร env ใน `agent.yaml` ไม่ได้ตั้งค่า | อัปเดตส่วน `environment_variables` ใน `agent.yaml` |
   | `azure.identity.CredentialUnavailableError` | ยังไม่ได้ตั้งค่า Managed Identity | Foundry ตั้งให้อัตโนมัติ - ตรวจสอบว่าคุณปรับใช้ผ่านส่วนขยาย |
   | `OSError: port 8088 already in use` | Dockerfile เปิดเผยพอร์ตผิดหรือพอร์ตขัดแย้ง | ตรวจสอบ `EXPOSE 8088` ใน Dockerfile และ `CMD ["python", "main.py"]` |
   | คอนเทนเนอร์ออกด้วยรหัส 1 | มีข้อยกเว้นไม่ได้จับที่ `main()` | ทดสอบในเครื่อง ([Module 5](05-test-locally.md)) ก่อนปรับใช้ |

3. **ปรับใช้ใหม่หลังแก้ไข:**  
   - กด `Ctrl+Shift+P` → เลือก **Microsoft Foundry: Deploy Hosted Agent** → เลือกเอเจนต์เดียวกัน → ปรับใช้เวอร์ชันใหม่

### การปรับใช้ใช้เวลานานเกินไป

คอนเทนเนอร์มัลติเอเจนต์ใช้เวลานานกว่าเพราะสร้างอินสแตนซ์เอเจนต์ 4 ตัวตอนเริ่มต้น เวลาปกติในการเริ่มต้น:

| ขั้นตอน | เวลาที่คาดหวัง |
|-------|------------------|
| สร้างภาพคอนเทนเนอร์ | 1-3 นาที |
| ดันภาพไปยัง ACR | 30-60 วินาที |
| เริ่มคอนเทนเนอร์ (เอเจนต์เดียว) | 15-30 วินาที |
| เริ่มคอนเทนเนอร์ (มัลติเอเจนต์) | 30-120 วินาที |
| เอเจนต์พร้อมใช้งานใน Playground | 1-2 นาทีหลังขึ้นข้อความ "Started" |

> หากสถานะ "Pending" ค้างนานเกิน 5 นาที ให้ตรวจสอบล็อกคอนเทนเนอร์ว่ามีข้อผิดพลาดหรือไม่

---

## ปัญหา RBAC และสิทธิ์

### `403 Forbidden` หรือ `AuthorizationFailed`

คุณต้องมีบทบาท **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ในโปรเจกต์ Foundry ของคุณ:

1. ไปที่ [Azure Portal](https://portal.azure.com) → ทรัพยากรโปรเจกต์ Foundry ของคุณ  
2. คลิก **Access control (IAM)** → **Role assignments**  
3. ค้นหาชื่อคุณ → ยืนยันว่ามีบทบาท **Azure AI User**  
4. หากไม่มี: คลิก **Add** → **Add role assignment** → ค้นหาบทบาท **Azure AI User** → มอบหมายให้บัญชีของคุณ

ดูเอกสาร [RBAC สำหรับ Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) เพื่อรายละเอียดเพิ่มเติม

### ไม่สามารถเข้าถึงการปรับใช้โมเดลได้

หากเอเจนต์คืนค่าข้อผิดพลาดเกี่ยวกับโมเดล:

1. ตรวจสอบว่าโมเดลถูกปรับใช้แล้ว: ใน Foundry sidebar → ขยายโปรเจกต์ → **Models** → ตรวจสอบว่า `gpt-4.1-mini` (หรือโมเดลของคุณ) มีสถานะ **Succeeded**  
2. ตรวจสอบว่าชื่อการปรับใช้ตรงกัน: เปรียบเทียบค่า `MODEL_DEPLOYMENT_NAME` ในไฟล์ `.env` (หรือใน `agent.yaml`) กับชื่อการปรับใช้จริงใน sidebar  
3. หากการปรับใช้หมดอายุ (ระดับฟรี): ปรับใช้ใหม่จาก [Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)

---

## ปัญหา Agent Inspector

### Inspector เปิดขึ้นแต่แสดง "Disconnected"

1. ตรวจสอบว่าเซิร์ฟเวอร์กำลังทำงานอยู่: มองหาข้อความ "Server running on http://localhost:8088" ในเทอร์มินัล  
2. ตรวจสอบพอร์ต `5679`: Inspector เชื่อมต่อผ่าน debugpy บนพอร์ต 5679  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. รีสตาร์ทเซิร์ฟเวอร์แล้วเปิด Inspector ใหม่

### Inspector แสดงผลบางส่วน

การตอบสนองจากมัลติเอเจนต์อาจยาวและสตรีมเป็นส่วน ๆ กรุณารอจนกว่าจะสิ้นสุดคำตอบทั้งหมด (อาจใช้เวลาระหว่าง 30-60 วินาที ขึ้นอยู่กับจำนวน gap cards และการเรียก MCP tool)

หากคำตอบถูกตัดกลางคันอย่างสม่ำเสมอ:  
- ตรวจสอบคำสั่ง GapAnalyzer ว่ารวมบล็อก `CRITICAL:` ที่ป้องกันไม่ให้รวม gap cards  
- ตรวจสอบขีดจำกัดโทเคนของโมเดลคุณ - `gpt-4.1-mini` รองรับโทเคนขาออกสูงสุด 32K ซึ่งควรเพียงพอ

---

## เคล็ดลับการเพิ่มประสิทธิภาพ

### ตอบสนองช้า

เวิร์กโฟลว์มัลติเอเจนต์จะช้ากว่าแบบเอเจนต์เดี่ยวเนื่องจากความขึ้นต่อเนื่อง และการเรียกใช้ MCP tool

| การปรับแต่ง | วิธีทำ | ผลกระทบ |
|-------------|-----|--------|
| ลดจำนวนการเรียก MCP | ลดพารามิเตอร์ `max_results` ในเครื่องมือ | ลดรอบการส่ง HTTP |
| ทำคำสั่งให้สั้นลงและชัดเจน | ใช้พรอมต์เอเจนต์ที่สั้นและเน้นจุดสำคัญ | เพิ่มความเร็วในการประมวลผล LLM |
| ใช้ `gpt-4.1-mini` | เร็วกว่ารุ่น `gpt-4.1` ในการพัฒนา | เร็วขึ้นประมาณ 2 เท่า |
| ลดรายละเอียดใน gap card | ทำรูปแบบ gap card ในคำสั่ง GapAnalyzer ให้เรียบง่ายขึ้น | ลดปริมาณผลลัพธ์ที่ต้องสร้าง |

### เวลาตอบสนองทั่วไป (ท้องถิ่น)

| การตั้งค่า | เวลาที่คาดหวัง |
|--------------|---------------|
| `gpt-4.1-mini`, 3-5 gap cards | 30-60 วินาที |
| `gpt-4.1-mini`, 8+ gap cards | 60-120 วินาที |
| `gpt-4.1`, 3-5 gap cards | 60-120 วินาที |
---

## การขอความช่วยเหลือ

หากคุณติดขัดหลังจากลองแก้ไขด้านบน:

1. **ตรวจสอบบันทึกเซิร์ฟเวอร์** - ข้อผิดพลาดส่วนใหญ่จะแสดง Python stack trace ในเทอร์มินัล อ่าน full traceback ให้ครบถ้วน
2. **ค้นหาข้อความผิดพลาด** - คัดลอกข้อความผิดพลาดแล้วค้นหาใน [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)
3. **เปิดปัญหา (issue)** - สร้าง issue ใน [ที่เก็บเวิร์กช็อป (workshop repository)](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues) พร้อมกับ:
   - ข้อความผิดพลาดหรือภาพหน้าจอ
   - เวอร์ชันแพ็กเกจของคุณ (`pip list | Select-String "agent-framework"`)
   - เวอร์ชัน Python ของคุณ (`python --version`)
   - ระบุว่าปัญหาเป็นปัญหาท้องถิ่นหรือหลังการปรับใช้

---

### เช็คพอยต์

- [ ] คุณสามารถระบุและแก้ไขข้อผิดพลาดหลายเอเจนต์ที่พบบ่อยที่สุดโดยใช้ตารางอ้างอิงด่วน
- [ ] คุณรู้วิธีตรวจสอบและแก้ไขปัญหาการตั้งค่า `.env`
- [ ] คุณสามารถตรวจสอบว่าเวอร์ชันแพ็กเกจตรงกับเมตริกซ์ที่ต้องการหรือไม่
- [ ] คุณเข้าใจบันทึก MCP และสามารถวินิจฉัยความล้มเหลวของเครื่องมือได้
- [ ] คุณรู้วิธีตรวจสอบบันทึกคอนเทนเนอร์สำหรับความล้มเหลวในการปรับใช้
- [ ] คุณสามารถตรวจสอบบทบาท RBAC ใน Azure Portal ได้

---

**ก่อนหน้า:** [07 - Verify in Playground](07-verify-in-playground.md) · **หน้าแรก:** [Lab 02 README](../README.md) · [หน้าแรกเวิร์กช็อป](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ข้อจำกัดความรับผิดชอบ**:  
เอกสารฉบับนี้ได้รับการแปลโดยใช้บริการแปลภาษาอัตโนมัติ [Co-op Translator](https://github.com/Azure/co-op-translator) แม้เราจะพยายามให้การแปลมีความถูกต้อง แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความคลาดเคลื่อนได้ เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่ถูกต้อง สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้บริการแปลโดยมืออาชีพที่เป็นมนุษย์ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดที่เกิดจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->