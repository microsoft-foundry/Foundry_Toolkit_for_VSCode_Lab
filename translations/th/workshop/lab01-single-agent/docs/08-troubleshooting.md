# Module 8 - การแก้ไขปัญหา

โมดูลนี้เป็นคู่มืออ้างอิงสำหรับทุกปัญหาทั่วไปที่พบในระหว่างเวิร์กช็อป ทำเครื่องหมายหน้านี้ไว้ - คุณจะกลับมาเปิดดูทุกครั้งที่มีปัญหาเกิดขึ้น

---

## 1. ข้อผิดพลาดสิทธิ์การใช้งาน

### 1.1 ปฏิเสธสิทธิ์ `agents/write`

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**สาเหตุหลัก:** คุณไม่มีบทบาท `Azure AI User` ในระดับ **โปรเจกต์** ซึ่งเป็นข้อผิดพลาดที่พบมากที่สุดในเวิร์กช็อปนี้

**การแก้ไข - ทีละขั้นตอน:**

1. เปิด [https://portal.azure.com](https://portal.azure.com)
2. ในแถบค้นหาด้านบน พิมพ์ชื่อ **โปรเจกต์ Foundry** ของคุณ (เช่น `workshop-agents`)
3. **สำคัญ:** คลิกผลลัพธ์ที่แสดงประเภท **"Microsoft Foundry project"** ไม่ใช่บัญชีแม่/ทรัพยากร hub ซึ่งเป็นทรัพยากรที่ต่างกันและมีขอบเขต RBAC ต่างกัน
4. ในแถบเมนูด้านซ้ายของหน้าโปรเจกต์ คลิก **Access control (IAM)**
5. คลิกแท็บ **Role assignments** เพื่อตรวจสอบว่าคุณมีบทบาทนี้แล้วหรือไม่:
   - ค้นหาชื่อหรืออีเมลของคุณ
   - หากมีบทบาท `Azure AI User` แล้ว → ข้อผิดพลาดมีสาเหตุอื่น (ตรวจสอบขั้นตอนที่ 8 ด้านล่าง)
   - หากไม่มี → ดำเนินการเพิ่มบทบาทนี้
6. คลิก **+ Add** → **Add role assignment**
7. ในแท็บ **Role**:
   - ค้นหา [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)
   - เลือกบทบาทจากผลลัพธ์
   - คลิก **Next**
8. ในแท็บ **Members**:
   - เลือก **User, group, or service principal**
   - คลิก **+ Select members**
   - ค้นหาชื่อหรืออีเมลของคุณ
   - เลือกตัวคุณเองจากผลลัพธ์
   - คลิก **Select**
9. คลิก **Review + assign** → อีกครั้งที่ **Review + assign**
10. **รอ 1-2 นาที** - การเปลี่ยนแปลง RBAC ใช้เวลาสักครู่ในการเผยแพร่
11. ลองทำงานที่ล้มเหลวอีกครั้ง

> **เหตุผลที่ Owner/Contributor ไม่เพียงพอ:** Azure RBAC มีสองประเภทของสิทธิ์ - *management actions* และ *data actions* Owner และ Contributor ให้สิทธิ์ management actions (สร้างทรัพยากร แก้ไขการตั้งค่า) แต่การทำงานของ agent ต้องการ `agents/write` **data action** ซึ่งมีในบทบาท `Azure AI User`, `Azure AI Developer` และ `Azure AI Owner` เท่านั้น ดูรายละเอียดได้ที่ [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)

### 1.2 `AuthorizationFailed` ระหว่างการจัดเตรียมทรัพยากร

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**สาเหตุหลัก:** คุณไม่มีสิทธิ์สร้างหรือแก้ไขทรัพยากร Azure ในการสมัครสมาชิก/กลุ่มทรัพยากรนี้

**การแก้ไข:**
1. ขอให้ผู้ดูแลระบบการสมัครสมาชิกของคุณมอบบทบาท **Contributor** ให้กับคุณในกลุ่มทรัพยากรที่โปรเจกต์ Foundry ของคุณอยู่
2. หรือขอให้พวกเขาสร้างโปรเจกต์ Foundry ให้และมอบบทบาท **Azure AI User** บนโปรเจกต์นั้นให้คุณ

### 1.3 `SubscriptionNotRegistered` สำหรับ [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource)

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**สาเหตุหลัก:** การสมัครสมาชิก Azure ยังไม่มีการลงทะเบียน resource provider ที่จำเป็นสำหรับ Foundry

**การแก้ไข:**

1. เปิดเทอร์มินัลและรัน:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```

2. รอจนการลงทะเบียนเสร็จสมบูรณ์ (อาจใช้เวลาประมาณ 1-5 นาที):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   ผลลัพธ์ที่คาดหวัง: `"Registered"`
3. ลองทำงานอีกครั้ง

---

## 2. ข้อผิดพลาด Docker (เฉพาะกรณีติดตั้ง Docker เท่านั้น)

> Docker เป็น **ทางเลือก** สำหรับเวิร์กช็อปนี้ ข้อผิดพลาดเหล่านี้ใช้เฉพาะกรณีติดตั้ง Docker Desktop และส่วนขยาย Foundry พยายามสร้าง container ในเครื่องเท่านั้น

### 2.1 Docker daemon ไม่ทำงาน

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**การแก้ไข - ทีละขั้นตอน:**

1. **ค้นหา Docker Desktop** ในเมนู Start (Windows) หรือ Applications (macOS) แล้วเปิดใช้งาน
2. รอจนหน้าต่าง Docker Desktop แสดงข้อความ **"Docker Desktop is running"** ซึ่งปกติจะใช้เวลาประมาณ 30-60 วินาที
3. มองหาไอคอนวาฬ Docker ที่ system tray (Windows) หรือ menu bar (macOS) เอาเมาส์ชี้เพื่อยืนยันสถานะ
4. ตรวจสอบในเทอร์มินัล:
   ```powershell
   docker info
   ```
   หากแสดงข้อมูลระบบ Docker (Server Version, Storage Driver ฯลฯ) แสดงว่า Docker กำลังทำงานอยู่
5. **สำหรับ Windows:** หาก Docker ยังไม่เริ่มทำงาน:
   - เปิด Docker Desktop → **Settings** (ไอคอนรูปเฟือง) → **General**
   - ตรวจสอบว่าเลือก **Use the WSL 2 based engine** แล้ว
   - คลิก **Apply & restart**
   - หากยังไม่มี WSL 2 ลงไว้ ให้รัน `wsl --install` ใน PowerShell ที่เปิดสิทธิ์ระดับผู้ดูแล จากนั้นรีสตาร์ทคอมพิวเตอร์
6. ลองดีพลอยใหม่อีกครั้ง

### 2.2 การสร้าง Docker ล้มเหลวเนื่องจากข้อผิดพลาด dependencies

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**การแก้ไข:**
1. เปิดไฟล์ `requirements.txt` และตรวจสอบให้แน่ใจว่าชื่อแพ็กเกจสะกดถูกต้องทั้งหมด
2. ตรวจสอบการกำหนดเวอร์ชันว่าเป็นไปตามที่ต้องการ:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```

3. ทดสอบติดตั้งในเครื่องก่อน:
   ```bash
   pip install -r requirements.txt
   ```

4. หากใช้ private package index ให้ตรวจสอบว่า Docker สามารถเชื่อมต่อเครือข่ายได้

### 2.3 ความไม่ตรงกันของแพลตฟอร์ม container (Apple Silicon)

ถ้าดีพลอยจากเครื่อง Mac Apple Silicon (M1/M2/M3/M4) ต้องสร้าง container สำหรับ `linux/amd64` เท่านั้น เพราะ runtime container ของ Foundry ใช้ AMD64

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> คำสั่ง deploy ของส่วนขยาย Foundry จะจัดการเรื่องนี้ให้อัตโนมัติในส่วนใหญ่ ถ้าเจอข้อผิดพลาดเกี่ยวกับสถาปัตยกรรม ให้สร้างด้วยตนเองโดยใช้ธง `--platform` แล้วติดต่อทีม Foundry

---

## 3. ข้อผิดพลาดการพิสูจน์ตัวตน

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) ไม่สามารถรับ token

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**สาเหตุหลัก:** ไม่มีแหล่งข้อมูลการพิสูจน์ตัวตนในโซ่ `DefaultAzureCredential` ที่มี token ที่ถูกต้อง

**การแก้ไข - ลองแต่ละขั้นตอนตามลำดับ:**

1. **ล็อกอินใหม่ผ่าน Azure CLI** (การแก้ปัญหาที่พบมากที่สุด):
   ```bash
   az login
   ```
   จะเปิดหน้าต่างเบราว์เซอร์ ให้ลงชื่อเข้าใช้ แล้วกลับมาที่ VS Code

2. **ตั้งค่าการสมัครสมาชิกให้ถูกต้อง:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   หากไม่ใช่การสมัครสมาชิกที่ถูกต้อง:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **ล็อกอินใหม่ผ่าน VS Code:**
   - คลิกไอคอน **Accounts** (รูปคน) ที่มุมล่างซ้ายของ VS Code
   - คลิกชื่อบัญชีของคุณ → **Sign Out**
   - คลิกไอคอน Accounts อีกครั้ง → **Sign in to Microsoft**
   - ทำตามขั้นตอนการล็อกอินในเบราว์เซอร์ให้เสร็จ

4. **ใช้ service principal (สำหรับกรณี CI/CD เท่านั้น):**
   - ตั้งค่าตัวแปรแวดล้อมใน `.env` ดังนี้:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - จากนั้นรีสตาร์ทกระบวนการ agent ของคุณ

5. **ตรวจสอบ token cache:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   หากล้มเหลว นั่นหมายความว่า token ของ CLI หมดอายุแล้ว ให้รัน `az login` อีกครั้ง

### 3.2 Token ใช้งานได้ในเครื่องแต่ไม่ใช่ในดีพลอยโฮสต์

**สาเหตุหลัก:** โฮสต์เอเจนต์ใช้ managed identity ที่ระบบดูแล แตกต่างจากข้อมูลประจำตัวส่วนตัวของคุณ

**การแก้ไข:** นี่เป็นพฤติกรรมปกติ - managed identity จะถูกจัดเตรียมโดยอัตโนมัติขณะดีพลอย หากโฮสต์เอเจนต์ยังมีปัญหาการพิสูจน์ตัวตน:
1. ตรวจสอบว่า managed identity ของโปรเจกต์ Foundry มีสิทธิ์เข้าถึง Azure OpenAI resource
2. ตรวจสอบว่า `PROJECT_ENDPOINT` ใน `agent.yaml` ถูกต้อง

---

## 4. ข้อผิดพลาดโมเดล

### 4.1 ไม่พบการดีพลอยโมเดล

```
Error: Model deployment not found / The specified deployment does not exist
```

**การแก้ไข - ทีละขั้นตอน:**

1. เปิดไฟล์ `.env` แล้วจดค่าของ `AZURE_AI_MODEL_DEPLOYMENT_NAME`
2. เปิดแถบด้านข้าง **Microsoft Foundry** ใน VS Code
3. ขยายโปรเจกต์ของคุณ → **Model Deployments**
4. เปรียบเทียบชื่อ deployment ที่แสดงกับค่าใน `.env` ของคุณ
5. ชื่อจำเป็นต้อง **ตรงตามตัวอักษร** - `gpt-4o` ต่างจาก `GPT-4o`
6. หากไม่ตรงกัน ปรับค่าใน `.env` ให้เหมือนกับชื่อที่แสดงในแถบด้านข้าง
7. สำหรับการดีพลอยโฮสต์ ให้แก้ไข `agent.yaml` ด้วย:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 โมเดลตอบกลับเนื้อหาที่ไม่คาดคิด

**การแก้ไข:**
1. ตรวจสอบค่าคงที่ `EXECUTIVE_AGENT_INSTRUCTIONS` ใน `main.py` ให้แน่ใจว่าไม่ได้ถูกตัดหรือเสียหาย
2. ตรวจสอบการตั้งค่าอุณหภูมิของโมเดล (ถ้ากำหนดได้) - ค่าต่ำกว่าจะให้ผลลัพธ์ที่คาดเดาได้มากขึ้น
3. เปรียบเทียบโมเดลที่ดีพลอย (เช่น `gpt-4o` กับ `gpt-4o-mini`) - โมเดลแต่ละตัวมีความสามารถต่างกัน

---

## 5. ข้อผิดพลาดในการดีพลอย

### 5.1 การอนุญาตในการดึงภาพจาก ACR

```
Error: AcrPullUnauthorized
```

**สาเหตุหลัก:** Managed identity ของโปรเจกต์ Foundry ไม่สามารถดึงภาพ container จาก Azure Container Registry ได้

**การแก้ไข - ทีละขั้นตอน:**

1. เปิด [https://portal.azure.com](https://portal.azure.com)
2. ค้นหา **[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** ในแถบค้นหาด้านบน
3. คลิกที่ registry ที่เกี่ยวข้องกับโปรเจกต์ Foundry ของคุณ (มักจะอยู่ในกลุ่มทรัพยากรเดียวกัน)
4. ในแถบเมนูด้านซ้าย คลิก **Access control (IAM)**
5. คลิก **+ Add** → **Add role assignment**
6. ค้นหา **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** แล้วเลือก คลิก **Next**
7. เลือก **Managed identity** → คลิก **+ Select members**
8. ค้นหาและเลือก managed identity ของโปรเจกต์ Foundry
9. คลิก **Select** → **Review + assign** → **Review + assign**

> การกำหนดบทบาทนี้มักเกิดขึ้นโดยอัตโนมัติจากส่วนขยาย Foundry หากพบข้อผิดพลาดนี้ อาจหมายความว่าการตั้งค่าอัตโนมัติไม่สำเร็จ คุณสามารถลองดีพลอยใหม่อีกครั้ง - ส่วนขยายอาจลองตั้งค่าอีกครั้ง

### 5.2 Agent ล้มเหลวในการเริ่มต้นหลังดีพลอย

**อาการ:** สถานะ container ค้างเป็น "Pending" นานเกิน 5 นาทีหรือแสดง "Failed"

**การแก้ไข - ทีละขั้นตอน:**

1. เปิดแถบด้านข้าง **Microsoft Foundry** ใน VS Code
2. คลิกที่ hosted agent ของคุณ → เลือกเวอร์ชัน
3. ในแผงรายละเอียด ดู **Container Details** → มองหาส่วนหรือทางลิงก์ **Logs**
4. อ่านบันทึกเริ่มต้น container สาเหตุทั่วไป:

| ข้อความในบันทึก | สาเหตุ | การแก้ไข |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | ขาด dependency | เพิ่มใน `requirements.txt` แล้วดีพลอยใหม่ |
| `KeyError: 'PROJECT_ENDPOINT'` | ขาด environment variable | เพิ่มตัวแปรใน `agent.yaml` ภายใต้ `env:` |
| `OSError: [Errno 98] Address already in use` | พอร์ตชนกัน | ตรวจสอบว่า `agent.yaml` กำหนด `port: 8088` และมีเพียงโปรเซสเดียวใช้พอร์ตนี้ |
| `ConnectionRefusedError` | Agent ไม่เริ่มฟัง | ตรวจสอบ `main.py` - ฟังก์ชัน `from_agent_framework()` ต้องถูกเรียกตอนเริ่มต้น |

5. แก้ไขปัญหาแล้วดีพลอยใหม่จาก [Module 6](06-deploy-to-foundry.md)

### 5.3 ดีพลอยหมดเวลารอ

**การแก้ไข:**
1. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต - การส่งภาพ Docker อาจมีขนาดใหญ่ (>100MB สำหรับดีพลอยครั้งแรก)
2. หากอยู่หลังพร็อกซีองค์กร ให้ตรวจสอบการตั้งค่าพร็อกซีใน Docker Desktop: **Docker Desktop** → **Settings** → **Resources** → **Proxies**
3. ลองใหม่อีกครั้ง - ปัญหาเครือข่ายชั่วคราวอาจทำให้ล้มเหลว

---

## 6. อ้างอิงด่วน: บทบาท RBAC

| บทบาท | ขอบเขตทั่วไป | สิ่งที่ให้สิทธิ์ |
|------|---------------|----------------|
| **Azure AI User** | โปรเจกต์ | การกระทำข้อมูล: สร้าง, ดีพลอย และเรียก agent (`agents/write`, `agents/read`) |
| **Azure AI Developer** | โปรเจกต์ หรือ บัญชี | การกระทำข้อมูล + การสร้างโปรเจกต์ |
| **Azure AI Owner** | บัญชี | เข้าถึงเต็มรูปแบบ + จัดการการมอบบทบาท |
| **Azure AI Project Manager** | โปรเจกต์ | การกระทำข้อมูล + สามารถมอบ Azure AI User ให้คนอื่นได้ |
| **Contributor** | การสมัครสมาชิก/กลุ่มทรัพยากร | การกระทำจัดการ (สร้าง/ลบทรัพยากร) **ไม่รวมการกระทำข้อมูล** |
| **Owner** | การสมัครสมาชิก/กลุ่มทรัพยากร | การกระทำจัดการ + การมอบบทบาท **ไม่รวมการกระทำข้อมูล** |
| **Reader** | ใดๆ | เข้าถึงอ่านได้อย่างเดียวสำหรับการจัดการ |

> **ข้อสรุปสำคัญ:** `Owner` และ `Contributor` **ไม่รวม** การกระทำข้อมูล คุณจำเป็นต้องมีบทบาท `Azure AI *` สำหรับการทำงานของ agent บทบาทขั้นต่ำสำหรับเวิร์กช็อปนี้คือ **Azure AI User** ในขอบเขต **โปรเจกต์**

---

## 7. รายการตรวจสอบการเสร็จสิ้นเวิร์กช็อป

ใช้รายการนี้สำหรับยืนยันขั้นสุดท้ายว่าคุณทำครบทุกขั้นตอนแล้ว:

| # | รายการ | โมดูล | ผ่าน? |
|---|------|--------|---|
| 1 | ติดตั้งและตรวจสอบข้อกำหนดทั้งหมดแล้ว | [00](00-prerequisites.md) | |
| 2 | ติดตั้ง Foundry Toolkit และส่วนขยาย Foundry แล้ว | [01](01-install-foundry-toolkit.md) | |
| 3 | สร้างโปรเจกต์ Foundry หรือเลือกโปรเจกต์ที่มีอยู่ | [02](02-create-foundry-project.md) | |
| 4 | โมเดลที่ปรับใช้แล้ว (เช่น gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | กำหนดบทบาทผู้ใช้ Azure AI ในขอบเขตโครงการ | [02](02-create-foundry-project.md) | |
| 6 | สร้างโครงร่างโปรเจ็กต์โฮสต์เอเจนต์แล้ว (agent/) | [03](03-create-hosted-agent.md) | |
| 7 | กำหนดค่า `.env` ด้วย PROJECT_ENDPOINT และ MODEL_DEPLOYMENT_NAME | [04](04-configure-and-code.md) | |
| 8 | ปรับแต่งคำสั่งเอเจนต์ใน main.py | [04](04-configure-and-code.md) | |
| 9 | สร้างสภาพแวดล้อมเสมือนและติดตั้ง dependencies แล้ว | [04](04-configure-and-code.md) | |
| 10 | ทดสอบเอเจนต์ในเครื่องด้วย F5 หรือเทอร์มินัล (ผ่านการทดสอบ 4 ครั้ง) | [05](05-test-locally.md) | |
| 11 | ปรับใช้งานกับ Foundry Agent Service แล้ว | [06](06-deploy-to-foundry.md) | |
| 12 | สถานะคอนเทนเนอร์แสดงว่า "เริ่มต้นแล้ว" หรือ "กำลังทำงาน" | [06](06-deploy-to-foundry.md) | |
| 13 | ตรวจสอบใน VS Code Playground (ผ่านการทดสอบ 4 ครั้ง) | [07](07-verify-in-playground.md) | |
| 14 | ตรวจสอบใน Foundry Portal Playground (ผ่านการทดสอบ 4 ครั้ง) | [07](07-verify-in-playground.md) | |

> **ขอแสดงความยินดี!** หากทำเครื่องหมายถูกครบทุกข้อ คุณได้ทำเวิร์กช็อปทั้งหมดสำเร็จแล้ว คุณได้สร้างเอเจนต์โฮสต์ตั้งแต่เริ่มต้น ทดสอบในเครื่อง ปรับใช้กับ Microsoft Foundry และยืนยันผลในสภาพแวดล้อมจริงแล้ว

---

**ก่อนหน้า:** [07 - ตรวจสอบใน Playground](07-verify-in-playground.md) · **หน้าแรก:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้เราจะพยายามให้ความถูกต้องสูงสุด โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความคลาดเคลื่อน เอกสารฉบับต้นฉบับในภาษาดั้งเดิมควรถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ควรใช้บริการแปลโดยมืออาชีพที่เป็นมนุษย์ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->