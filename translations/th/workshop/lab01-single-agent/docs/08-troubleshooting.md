# โมดูล 8 - การแก้ไขปัญหา

โมดูลนี้เป็นคู่มืออ้างอิงสำหรับปัญหาทั่วไป บันทึกหน้าหนังสือนี้ไว้และกลับมาเมื่อเกิดข้อผิดพลาด

---

## 1. ข้อผิดพลาดเรื่องสิทธิ์

### 1.1 สิทธิ์ `agents/write` ถูกปฏิเสธ

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**สาเหตุหลัก:** ขาดบทบาท `Azure AI User` ในระดับ **โปรเจ็กต์** นี่คือข้อผิดพลาดอันดับ 1 ของเวิร์กช็อป

**วิธีแก้ไข:**
1. เปิด [portal.azure.com](https://portal.azure.com)
2. ค้นหาชื่อโปรเจ็กต์ Foundry ของคุณ → คลิกผลลัพธ์ที่เป็นประเภท **"Microsoft Foundry project"** (ไม่ใช่บัญชีหลัก)
3. **Access control (IAM)** → **+ Add** → **Add role assignment**
4. บทบาท: **Azure AI User** → ต่อไป
5. สมาชิก: เลือกตัวคุณเอง → ตรวจสอบ + มอบหมาย → ตรวจสอบ + มอบหมาย
6. **รอ 1–2 นาที** → ลองใหม่

> **ทำไม Owner/Contributor ถึงไม่เพียงพอ:** บทบาทเหล่านี้อนุญาตเพียงการดำเนินการ *จัดการ* เท่านั้น การทำงานของเอเจนต์ต้องใช้ `agents/write` *data action* ซึ่งมีเพียงในบทบาท `Azure AI User`, `Azure AI Developer`, หรือ `Azure AI Owner` ดูรายละเอียดได้ที่ [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)

### 1.2 เกิด `AuthorizationFailed` ระหว่าง provisioning

**วิธีแก้ไข:** ขอให้แอดมินของคุณมอบบทบาท **Contributor** บนกลุ่มทรัพยากร หรือให้พวกเขาสร้างโปรเจ็กต์ให้และมอบ **Azure AI User** ให้คุณ

### 1.3 เกิดข้อผิดพลาด `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# รอจนกว่า: "ลงทะเบียนแล้ว"
```

---

## 2. ข้อผิดพลาด Docker

> Docker เป็น **ทางเลือก** ข้อผิดพลาดเหล่านี้ใช้เฉพาะเมื่อ Docker Desktop ถูกติดตั้งและส่วนขยายพยายามสร้างในเครื่อง

### 2.1 Docker daemon ไม่ทำงาน

**วิธีแก้ไข:** เริ่ม Docker Desktop → รอจนสถานะเป็น "running" → ตรวจสอบด้วยคำสั่ง `docker info` → ลองใหม่

### 2.2 สร้างล้มเหลวเพราะข้อผิดพลาดการพึ่งพา

**วิธีแก้ไข:** ตรวจสอบการสะกดในไฟล์ `requirements.txt` ทดสอบก่อนในเครื่อง: `pip install -r requirements.txt`

### 2.3 ความไม่ตรงกันของแพลตฟอร์ม (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. ข้อผิดพลาดการยืนยันตัวตน

### 3.1 `DefaultAzureCredential` ล้มเหลว

**วิธีแก้ไข (ลองตามลำดับ):**
1. `az login` (เข้าสู่ระบบใหม่)
2. `az account set --subscription "<id>"` (เลือก subscription ที่ถูกต้อง)
3. VS Code → บัญชี → ออกจากระบบ → เข้าสู่ระบบใหม่
4. ตรวจสอบ: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 โทเค็นใช้ได้ในเครื่องแต่ไม่ใช้ได้ในโฮสต์

**คาดหวัง:** เอเจนต์ที่โฮสต์ใช้ระบบ managed identity ไม่ใช่ credentials ของคุณ หากเอเจนต์โฮสต์ได้รับข้อผิดพลาดยืนยันตัวตน:
- ตรวจสอบว่า `AZURE_AI_PROJECT_ENDPOINT` ใน `agent.yaml` ถูกต้อง
- ตรวจสอบ managed identity ของโปรเจ็กต์ว่ามีสิทธิ์เข้าถึงโมเดล

---

## 4. ข้อผิดพลาดเกี่ยวกับโมเดล

### 4.1 ไม่พบ deployment ของโมเดล

**วิธีแก้ไข:** ชื่อเป็น **case-sensitive** เปรียบเทียบ `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` กับชื่อที่แน่นอนใน Foundry sidebar → Models

### 4.2 ผลลัพธ์โมเดลไม่คาดคิด

**วิธีแก้ไข:** ตรวจสอบ `AGENT_INSTRUCTIONS` ใน `main.py` (ไม่ถูกตัดทอนหรือไม่) ลองใช้โมเดลอื่น (`gpt-4.1` กับ `gpt-4.1-mini`)

---

## 5. ข้อผิดพลาดการ deployment

### 5.1 การดึงจาก ACR ถูกปฏิเสธ

**วิธีแก้ไข:** Azure Portal → Container Registry → Access control (IAM) → เพิ่มบทบาท **AcrPull** ให้กับ managed identity ของโปรเจ็กต์ Foundry

### 5.2 Agent เริ่มต้นไม่สำเร็จ (ติดสถานะ "Pending" หรือ "Failed")

ตรวจสอบล็อกคอนเทนเนอร์ใน sidebar สาเหตุทั่วไป:

| ข้อความล็อก | วิธีแก้ไข |
|-------------|-----|
| `ModuleNotFoundError` | เพิ่มแพ็กเกจที่ขาดใน `requirements.txt` แล้ว deploy ใหม่ |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | เพิ่มตัวแปร env ใน `agent.yaml` ภายใต้ `environment_variables` |
| `Address already in use` | ตรวจสอบให้มีเพียงกระบวนการเดียวที่ผูกกับพอร์ต 8088 |

### 5.3 Deployment หมดเวลา

**วิธีแก้ไข:** ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต การ deploy ครั้งแรกมีไฟล์ขนาด >100MB หากอยู่หลังพร็อกซี ตั้งค่าพร็อกซีใน Docker Desktop

---

## 6. เส้นทาง B - Foundry Local

### 6.1 Foundry Local เริ่มต้นไม่ได้

| ปัญหา | วิธีแก้ไข |
|-------|-----|
| `foundry: command not found` | ติดตั้งใหม่: `winget install Microsoft.FoundryLocal` |
| ทรัพยากรไม่เพียงพอ | Foundry Local ต้องการ RAM ว่างประมาณ 4GB ปิดแอปอื่นๆ |
| ดาวน์โหลดโมเดลล้มเหลว | ตรวจสอบพื้นที่ดิสก์ (โมเดลขนาด 2–8 GB) ลองใหม่: `foundry local models pull <name>` |

### 6.2 ข้อผิดพลาดของโมเดลใน Foundry Local

| ปัญหา | วิธีแก้ไข |
|-------|-----|
| ตอบสนองช้า | คาดหวัง - โมเดลในเครื่องรันบน CPU เว้นแต่คุณมี GPU กรุณารอ |
| ผลลัพธ์คุณภาพต่ำ | ลองใช้โมเดลที่ใหญ่ขึ้นถ้าอุปกรณ์ของคุณรองรับ `phi-4-mini` เป็นตัวเลือกที่สมดุล |
| การเชื่อมต่อถูกปฏิเสธ | ตรวจสอบว่า Foundry Local รันอยู่หรือไม่: `foundry local status` รีสตาร์ทถ้าจำเป็น |

---

## 7. อ้างอิงด่วน: บทบาท RBAC

| บทบาท | ขอบเขต | อนุญาต |
|------|-------|--------|
| **Azure AI User** | โปรเจ็กต์ | การกระทำข้อมูล: `agents/write`, `agents/read` |
| **Azure AI Developer** | โปรเจ็กต์/บัญชี | การกระทำข้อมูล + สร้างโปรเจ็กต์ |
| **Azure AI Owner** | บัญชี | เข้าถึงเต็มรูปแบบ + จัดการบทบาท |
| **Contributor** | Subscription/RG | การจัดการเท่านั้น (**ไม่มี** การกระทำข้อมูล) |
| **Owner** | Subscription/RG | การจัดการ + มอบหมายบทบาท (**ไม่มี** การกระทำข้อมูล) |

---

## 8. รายการตรวจสอบการสำเร็จของเวิร์กช็อป

| # | รายการ | โมดูล |
|---|------|--------|
| 1 | ติดตั้งและตรวจสอบความพร้อม | [00](00-prerequisites.md) |
| 2 | ติดตั้งส่วนขยาย Foundry Toolkit, เชื่อมต่อโปรเจ็กต์ (หรือกำหนดค่าเส้นทาง B) | [01](01-setup.md) |
| 3 | สร้างโครงร่างเอเจนต์โฮสต์ | [02](02-create-hosted-agent.md) |
| 4 | กำหนดค่า `.env`, เขียนคำสั่ง, ติดตั้ง dependencies | [03](03-configure-and-code.md) |
| 5 | ทดสอบเอเจนต์ในเครื่อง - ผ่าน 3 กรณีใช้งาน | [04](04-test-locally.md) |
| 6 | deploy สู่ Foundry (เฉพาะเส้นทาง A) | [05](05-deploy-to-foundry.md) |
| 7 | ทดสอบ edge-case/ความปลอดภัยในคลาวด์ผ่าน (เฉพาะเส้นทาง A) | [06](06-verify-in-playground.md) |
| 8 | ตรวจสอบสรุปและกำหนดขั้นตอนถัดไป | [07](07-summary.md) |

---

**ก่อนหน้า:** [07 - สรุป](07-summary.md) · **หน้าแรก:** [README เวิร์กช็อป](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->