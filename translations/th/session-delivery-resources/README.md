# วิธีการสอนเซสชันนี้

ขอบคุณที่สอนเซสชันนี้!

ก่อนที่จะสอนเวิร์กช็อป โปรด:

1. อ่านเอกสารนี้และทรัพยากรทั้งหมดที่รวมอยู่ให้ครบทั้งหมด
2. ดูบันทึกการสอนเซสชันและการเดินทางดูเวิร์กช็อปตั้งแต่ต้นจบ
3. ทำทั้งสองห้องปฏิบัติการแบบลงมือทำตั้งแต่ต้นจนจบบนเครื่องของคุณเอง **อย่างน้อยหนึ่งครั้ง** ก่อนงาน
4. ตรวจสอบโปรเจกต์ Microsoft Foundry ของคุณ การปรับใช้โมเดล และโควต้า
5. ติดต่อผู้ดูแลหากมีข้อสงสัยใด ๆ

---

## สรุปไฟล์

| ทรัพยากร                      | ลิงก์                                                                             | คำอธิบาย                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| สไลด์เวิร์กช็อป           | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | สไลด์นำเสนอสำหรับเวิร์กช็อปนี้พร้อมบันทึกผู้นำเสนอและวิดีโอสาธิตฝังอยู่                   |
| บันทึกการสอนเซสชัน    | _จะจัดเตรียมโดยผู้ดูแล_                                               | การแนะนำเวิร์กช็อปและการเดินผ่านสไลด์บันทึก                                              |
| บันทึกการสาธิตเวิร์กช็อปตั้งแต่ต้นจนจบ | _จะจัดเตรียมโดยผู้ดูแล_                                               | บันทึกตั้งแต่ต้นจนจบของทั้งสองห้องปฏิบัติการจากมุมมองของผู้เรียน                        |
| เอกสารเวิร์กช็อป        | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | ที่เก็บแหล่งที่มา README ห้องปฏิบัติการ โมดูลขั้นตอนทีละขั้น                             |
| ห้องปฏิบัติการ 01 - ตัวแทนเดียว         | [Lab 01](../workshop/lab01-single-agent/README.md)                               | ห้องปฏิบัติการแบบลงมือทำ: สร้าง ทดสอบ และปรับใช้เอเย่นต์ *Explain Like I'm an Executive*    |
| ห้องปฏิบัติการ 02 - กระบวนงานหลายตัวแทน | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | ห้องปฏิบัติการแบบลงมือทำ: สร้างกระบวนการทำงาน *Resume to Job Fit Evaluator* แบบ 4 ตัวแทน     |
| สาธิต 1: Executive Agent             | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | สาธิตห้อง 01: แปลศัพท์เทคนิคเป็นสรุปสำหรับผู้บริหาร                                        |
| สาธิต 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | สาธิตห้อง 02: กระบวนงาน 4 ตัวแทนที่ประเมินความเหมาะสมของเรซูเม่กับงานและสร้างคำแนะนำ     |

> **หมายเหตุสำหรับผู้ฝึกสอน:** จะมีการเพิ่มลิงก์สไลด์และวิดีโอเมื่อบันทึกเสร็จสมบูรณ์ จนกว่าจะถึงเวลานั้น ให้ติดต่อผู้ดูแล (ดูที่ [ติดต่อ](#ช่องทางติดต่อ)) เพื่อขอไฟล์ล่าสุด

---

## เริ่มต้น

เวิร์กช็อปนี้สอนนักพัฒนาวิธีสร้าง ทดสอบ และปรับใช้ตัวแทน AI ไปยัง **บริการ Microsoft Foundry Agent** ในฐานะ **Hosted Agents** โดยใช้ VS Code ทั้งหมด ผ่านส่วนขยาย **Microsoft Foundry Toolkit**

เวิร์กช็อปแบ่งเป็นหลายส่วนรวมทั้งสไลด์, **2 การสาธิตสด**, และ **2 ห้องปฏิบัติการแบบลงมือทำ**

### เวลา

#### การสอนเต็มรูปแบบ (ประมาณ 2 ชั่วโมง)

| เวลา           | คำอธิบาย                                                          |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | บทนำ: Hosted Agents, Foundry Agent Service, และ toolkit             |
| 10:00 - 20:00   | สาธิต: Executive Agent ตั้งแต่ต้นจนจบ                            |
| 20:00 - 60:00   | ห้องปฏิบัติการ 01 - ตัวแทนเดียว (สร้าง ทดสอบในเครื่อง ปรับใช้ สนามทดลอง) |
| 60:00 - 110:00  | ห้องปฏิบัติการ 02 - กระบวนงานหลายตัวแทน (Resume to Job Fit Evaluator) |
| 110:00 - 120:00 | สรุป ถาม-ตอบ และแหล่งความรู้เพิ่มเติม                              |

#### การสอนแบบย่อ (ประมาณ 75 นาที)

| เวลา          | คำอธิบาย                                                   |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | บทนำและภาพรวม                                             |
| 10:00 - 20:00 | สาธิต: Executive Agent                                     |
| 20:00 - 70:00 | เฉพาะห้องปฏิบัติการ 01 (แนะนำให้ผู้เข้าร่วมทำห้องปฏิบัติการ 02 เอง) |
| 70:00 - 75:00 | สรุปและถาม-ตอบ                                            |

### การเตรียมตัว

| ทรัพยากร                       | ลิงก์                                                                                          | คำอธิบาย                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| เอกสารเวิร์กช็อป         | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | เอกสารและแหล่งที่มาของเวิร์กช็อป                 |
| คู่มือห้องปฏิบัติการ 01            | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | ห้องปฏิบัติการแบบเอเย่นต์เดียว                   |
| คู่มือห้องปฏิบัติการ 02            | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | ห้องปฏิบัติการแบบกระบวนงานหลายตัวแทน            |
| รายการตรวจสอบข้อกำหนด        | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | เครื่องมือ บัญชี และการเข้าถึง Azure ที่จำเป็น     |
| เริ่มต้นอย่างรวดเร็วของ Hosted Agents (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | คำแนะนำอย่างเป็นทางการสำหรับการปรับใช้ hosted agent ด้วย `azd` |
| ความพร้อมใช้งานของภูมิภาคสำหรับ Hosted Agents | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | ภูมิภาคที่รองรับ hosted agents (ตัวอย่าง)          |

### ข้อกำหนดสำหรับผู้ฝึกสอน

ก่อนสอน ให้แน่ใจว่าคุณมี:

- **บัญชีสมาชิก Azure** ที่มีสิทธิ์สร้างทรัพยากร (Owner หรือ Contributor ในกลุ่มทรัพยากร)
- การเข้าถึง **โปรเจกต์ Microsoft Foundry** ใน [ภูมิภาคที่รองรับ hosted agents](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)
- โควต้า สำหรับ **gpt-4.1** (หรือ **gpt-4.1-mini**) ในโปรเจกต์ Foundry ของคุณ
- เครื่องมือดังต่อไปนี้ที่ติดตั้งไว้:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [ส่วนขยาย Microsoft Foundry Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (อ็อปชัน)
  - Python 3.10 ขึ้นไป

รัน [เริ่มต้นอย่างรวดเร็วของ Hosted agents ด้วย `azd`](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) อย่างน้อยหนึ่งครั้งก่อนสอน เพื่อให้มีโปรเจกต์ Foundry, การปรับใช้โมเดล และ Azure Container Registry ที่ทราบว่าทำงานได้ดี เผื่อผู้เรียนติดขัด

---

## การเดินผ่านสไลด์

สไลด์เดินตามลำดับเดียวกับห้องปฏิบัติการ ข้อเสนอแนะประเด็นพูดสำหรับแต่ละส่วน:

| ส่วน                     | ข้อความสำคัญ                                                                                                  |
|-----------------------------|--------------------------------------------------------------------------------------------------------------|
| ชื่อเรื่องและวาระการประชุม            | กำหนดกรอบเวิร์กช็อปเป็น *VS Code ไป Foundry* โดยไม่ต้องสลับพอร์ทัล                                   |
| ทำไมต้อง hosted agents?          | รันไทม์ที่จัดการ, ปรับใช้จาก ACR, API `/responses` ที่เข้ากันกับ OpenAI, กำหนดขอบเขตโปรเจกต์ Foundry       |
| แผนผังสถาปัตยกรรม        | เดินผ่าน [README สถาปัตยกรรม](../README.md#architecture): โครงสร้าง, Inspector, ACR, Agent Service           |
| โครงสร้างตัวแทนที่โฮสต์   | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` - ไฟล์แต่ละไฟล์ทำอะไร                             |
| สาธิตสด: Executive Agent  | สลับไป VS Code และรันเดโม [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) ตั้งแต่ต้นจนจบ (ดู [สาธิต 1](#สาธิต-1-executive-agent)) |
| สาธิตสด: Resume to Job Fit Evaluator | สลับไป VS Code และรันเดโม 4 ตัวแทน [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) (ดู [สาธิต 2](#สาธิต-2-resume-to-job-fit-evaluator)) |
| สรุปห้องปฏิบัติการ 01                | ส่งต่อให้ผู้เรียน ดูที่ [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) |
| รูปแบบตัวแทนหลายตัว              | ต่อเนื่อง เทียบกับพร้อมกัน เทียบกับส่งต่อ - ดูตัวอย่างก่อนห้องปฏิบัติการ 02 เริ่ม                        |
| สรุปห้องปฏิบัติการ 02                | ส่งต่อให้ผู้เรียน ดูที่ [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) |
| สรุปและแหล่งข้อมูลเพิ่มเติม       | ลิงก์เรียนต่อจากส่วน [แหล่งข้อมูลเพิ่มเติม](#แหล่งข้อมูลเพิ่มเติม)                                      |

---

## การสาธิต

การสาธิตสดสองรายการถูกรวมในการสอน ให้จัดเวลาให้แต่ละรายการ 10 นาที

| สาธิต | ห้องปฏิบัติการ | ไฟล์ | สิ่งที่จะแสดง |
|------|-----|-------|--------------|
| Executive Agent | ห้อง 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | ตัวแทนที่โฮสต์เดียว; แปลศัพท์เทคนิคเป็นสรุปสำหรับผู้บริหาร |
| Resume to Job Fit Evaluator | ห้อง 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | การประสานงาน 4 ตัวแทน; ประเมินความเหมาะสมเรซูเม่กับงานและสร้างคำแนะนำ |

### สาธิต 1: Executive Agent

ตัวแทนอิสระใน [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) ใช้การนี้สาธิต 10 นาทีก่อนห้องปฏิบัติการ 01

1. เปิด [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) และเดินผ่านคำนิยามของตัวแทน (ระบบพรอมต์, โมเดล, เฟรมเวิร์ก)
2. กด `F5` เพื่อเปิด **Agent Inspector** บนเครื่องของคุณ
3. วางพรอมต์ตัวอย่างจาก [README](../README.md#see-it-in-action) และแสดงผลตอบกลับสรุปสำหรับผู้บริหาร
4. แสดง [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) และ [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) เพื่ออธิบายสิ่งที่ใช้ในการปรับใช้
5. สาธิตขั้นตอนการปรับใช้ (สั่ง Docker build, ดันไป ACR, สร้าง hosted agent) โดยไม่ต้องรอจนเสร็จสมบูรณ์

### สาธิต 2: Resume to Job Fit Evaluator

กระบวนงาน 4 ตัวแทนใน [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) ใช้การนี้สาธิต 10 นาทีก่อนห้องปฏิบัติการ 02

1. เปิด [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) และแสดงการเชื่อมต่อของตัวแทนทั้งสี่ในการจัดลำดับดำเนินงาน
2. กด `F5` เพื่อเปิด **Agent Inspector** สำหรับกระบวนงานหลายตัวแทน
3. วางคำอธิบายงานสั้นและเรซูเม่ตัวอย่างในแชทของ Inspector
4. เดินผ่านขั้นตอนทั้งสี่: ตัวแยกเรซูเม่, ตัวดึงข้อมูลความต้องการงาน, ตัวประเมินความเหมาะสม, และตัวเขียนคำแนะนำ
5. ชี้ให้เห็นว่าผลลัพธ์ของแต่ละตัวแทนย่อยกลายเป็นบริบทสำหรับตัวแทนถัดไป โดยเน้นรูปแบบการส่งต่อ
6. แสดง [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) เพื่อเปรียบเทียบกับตัวแทนนักเดียวจากสาธิต 1

---

## เคล็ดลับการสอน

- **ตั้งความคาดหวังแต่เนิ่น ๆ** Hosted agents ยังเป็นรุ่นพรีวิว - แจ้งข้อจำกัดภูมิภาคและโควต้าให้เข้าใจก่อน เพื่อไม่ให้ผู้เข้าร่วมงานตกใจระหว่างทำห้องปฏิบัติการ
- **รันงานตรวจสอบข้อกำหนดก่อน** ทั้งสองห้องปฏิบัติการมาพร้อมกับงาน `Validate prerequisites` ใน VS Code - ให้ผู้เข้าร่วมรันก่อนเขียนโค้ดใด ๆ
- **แสดง Agent Inspector ไว้เสมอ** ช่วงเวลาที่เข้าใจมากที่สุดคือเมื่อผู้เรียนเห็นแสงตอบกลับจาก `/responses` ในเครื่องของตนเอง
- **เตรียมโปรเจกต์สำรอง** หากโปรเจกต์ Foundry ของผู้เรียนชนข้อจำกัดโควต้า แบ่งปันโปรเจกต์ที่เตรียมไว้ล่วงหน้าสำหรับขั้นตอนการปรับใช้แทนการบล็อกห้อง
- **จับคู่ผู้เข้าร่วม** ห้องปฏิบัติการ 02 (หลายตัวแทน) ง่ายขึ้นมากเมื่อผู้เรียนได้พูดคุยและวางแผนการทำงานกับเพื่อนคู่หู
- **ใช้โมดูลเอกสารเป็นจุดพัก** โฟลเดอร์ `docs/` ของแต่ละห้องปฏิบัติการแบ่งเป็น 8 โมดูลหมายเลข - ใช้เป็นช่วงพักตามธรรมชาติ
- **ดึงภาพ Docker พื้นฐานล่วงหน้า** บนเครื่องที่ใช้ร่วมกันในห้องปฏิบัติการเพื่อหลีกเลี่ยงข้อจำกัดอัตราการเข้าถึงรีจิสทรี

---

## การแก้ไขปัญหาระหว่างสอน

| อาการ                                     | สิ่งแรกที่ควรลอง                                                                                        |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Inspector เชื่อมต่อไม่ได้               | ยืนยันว่าพอร์ต `8088` ว่าง และงาน `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` กำลังทำงาน     |
| ดีบักเกอร์แนบการดีบักไม่ติด                     | ตรวจสอบว่าพอร์ต `5679` ว่าง; รีสตาร์ท VS Code หาก `debugpy` ผูกพอร์ตแล้ว                             |
| `azd up` ล้มเหลวด้วยข้อผิดพลาดการยืนยันตัวตน    | รัน `az login` และ `azd auth login` และตรวจสอบให้แน่ใจว่าเลือก tenant ถูกต้อง                        |
| การปรับใช้ค้างที่การดันไป ACR                | ตรวจสอบว่า Docker Desktop กำลังทำงานและผู้ใช้มีสิทธิ์ `AcrPush` บนรีจิสทรี                           |
| โมเดลตอบกลับ 404 / deployment-not-found     | ชื่อการปรับใช้โมเดลใน `agent.yaml` ต้องตรงกับชื่อการปรับใช้ในโปรเจกต์ Foundry                       |

| ตัวแทนโฮสต์ติดอยู่ในสถานะ `Provisioning`         | ตรวจสอบว่าโซนโปรเจกต์ [รองรับตัวแทนโฮสต์](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) และมีโควต้าเหลือใช้งานหรือไม่ |
| Playground ส่งกลับ 401                       | ลงชื่อเข้าใช้ส่วนขยาย Foundry ใหม่จากแถบกิจกรรม VS Code                                     |

สำหรับคำแนะนำเชิงลึกเพิ่มเติม ทุกห้องปฏิบัติการจะมาพร้อมเอกสาร `08-troubleshooting.md` ของตนเอง - ส่งลิงก์ไปยังผู้เรียน:

- ห้องปฏิบัติการ 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- ห้องปฏิบัติการ 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## การปรับแต่งเซสชันนี้

คุณสามารถปรับเวิร์กช็อปให้เหมาะกับกลุ่มเป้าหมายของคุณได้ ตัวอย่างรูปแบบยอดนิยม:

- **กลุ่มผู้ชมแบ็คเอนด์:** ให้เวลาเพิ่มเติมกับ `agent.yaml`, Docker และ ACR; ลดเวลาการสาธิต playground ลง
- **กลุ่มนักพัฒนาประชาชน:** อยู่ในส่วนขยาย Foundry UI เพื่อการสร้างสรรค์โครงสร้าง; ลดขั้นตอน CLI
- **เซสชันเดี่ยว 60 นาที:** นำเสนอแนะนำ, สาธิต และเฉพาะห้องทดลอง 01 เท่านั้น
- **รูปแบบเวิร์กช็อปอย่างเดียว (ไม่มีสไลด์):** เปิด README ของทั้งสองห้องทดลองและใช้เป็นสคริปต์หลัก

หากคุณขยายห้องปฏิบัติการ โปรดส่งการเปลี่ยนแปลงผ่าน PR เพื่อให้ผู้สอนคนอื่นได้รับประโยชน์

---

## แหล่งข้อมูลเพิ่มเติม

- [เอกสาร Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/)
- [ภาพรวมตัวแทนโฮสต์](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [เริ่มต้นอย่างรวดเร็ว: ติดตั้งตัวแทนโฮสต์ตัวแรกของคุณ (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [วิธีการติดตั้งตัวแทนโฮสต์](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit สำหรับ VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## ช่องทางติดต่อ

หากคุณมีคำถามเกี่ยวกับการจัดการเซสชันนี้ กรุณาเปิดประเด็นใน [ที่เก็บเวิร์กช็อป](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues) และติดแท็กผู้ดูแล

| บทบาท                | ชื่อ           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| ผู้ดูแล / ติดต่อ   | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->