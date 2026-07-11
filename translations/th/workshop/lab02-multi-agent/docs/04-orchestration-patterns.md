# โมดูล 4 - รูปแบบการจัดการกระบวนการ

⏱️ ~10 นาที

ในโมดูลนี้ คุณจะได้สำรวจรูปแบบการจัดการกระบวนการที่ใช้ใน Resume Job Fit Evaluator และเรียนรู้วิธีอ่าน ปรับแก้ และขยายกราฟเวิร์กโฟลว์ การเข้าใจรูปแบบเหล่านี้เป็นสิ่งสำคัญสำหรับการแก้ไขปัญหาการไหลของข้อมูลและสร้าง [เวิร์กโฟลว์หลายตัวแทน](https://learn.microsoft.com/agent-framework/workflows/) ของคุณเอง

---

## รูปแบบที่ 1: โซ่ลำดับ

รูปแบบพื้นฐานในเวิร์กโฟลว์คือ **โซ่ลำดับ** - ผลลัพธ์ของตัวแทนแต่ละตัวถูกป้อนโดยตรงไปยังตัวถัดไป

```mermaid
flowchart LR
    RP[ตัวแยกวิเคราะห์ประวัติย่อ] --> JD[ตัวแทน JD]
    JD --> MA[ตัวแทนจับคู่]
    MA --> GA[ตัววิเคราะห์ช่องว่าง]
```

ในโค้ด การเรียก `add_edge()` แต่ละครั้งจะสร้างขั้นตอนหนึ่งในโซ่:

```python
.add_edge(resume_executor, jd_executor)       # ผลลัพธ์ ResumeParser → JD Agent
.add_edge(jd_executor, matching_executor)     # ผลลัพธ์ JD Agent → MatchingAgent
.add_edge(matching_executor, gap_executor)    # ผลลัพธ์ MatchingAgent → GapAnalyzer
```

> **ทำไมต้องเป็นลำดับ ไม่ใช่ fan-out/fan-in?** `WorkflowBuilder` ใช้ **OR-semantics** สำหรับขาเข้าที่เข้ามา: ตัวประมวลผลขั้นตอนถัดไปจะทำงานทันทีเมื่อมี **อย่างใดอย่างหนึ่ง** ของตัวก่อนหน้าทำงานเสร็จ หาก `matching_executor` มีขาเข้า 2 ขา (จากทั้ง `resume_executor` และ `jd_executor`) ตัวนี้จะถูกเรียกใช้งานสองครั้ง — ครั้งหนึ่งเมื่อ ResumeParser เสร็จสิ้น และอีกครั้งเมื่อ JD Agent เสร็จสิ้น — ทำให้ GapAnalyzer ทำงานสองครั้งและผลลัพธ์ปรากฏสองครั้งด้วย การทำงานแบบลำดับช่วยหลีกเลี่ยงปัญหานี้ทั้งหมด

## รูปแบบที่ 2: การส่งต่อเนื้อหา

เนื่องจาก `context_mode="last_agent"` หมายความว่าตัวดำเนินการแต่ละตัวจะเห็นเพียง **ผลลัพธ์จากตัวก่อนหน้าโดยตรง** เท่านั้น ตัวแทนในโซ่ลำดับจึงต้องส่งผ่านข้อมูลอย่างชัดเจนที่ตัวแทนด้านล่างต้องการ

ในเวิร์กโฟลว์นี้:
- **ResumeParser** คัดลอก JD ตรงตัวเข้าไปใน `[JOB DESCRIPTION PASS-THROUGH]` (เพื่อให้ JD Agent สามารถค้นหาได้)
- **JD Agent** คัดลอก `[PARSED RESUME]` ตรงตัวเข้าไปใน `[PARSED RESUME PASS-THROUGH]` (เพื่อให้ MatchingAgent สามารถเปรียบเทียบโปรไฟล์ทั้งสอง)

```
ResumeParser output
└─ [PARSED RESUME]               ← extracted by JD Agent
└─ [JOB DESCRIPTION PASS-THROUGH] ← extracted by JD Agent

JD Agent output
└─ [JD REQUIREMENTS]             ← extracted by MatchingAgent
└─ [PARSED RESUME PASS-THROUGH]  ← extracted by MatchingAgent
```

แต่ละส่วนของการส่งต่อต้องถูกคัดลอก **อย่างตรงตัว** - การสรุปหรือเขียนใหม่จะทำให้ตัวแทนขั้นตอนล่างที่ต้องพึ่งพาเสียหาย

---

## กราฟเวิร์กโฟลว์แบบเต็ม

การรวมรูปแบบโซ่ลำดับและการส่งต่อเนื้อหาทำให้เกิดเวิร์กโฟลว์ทั้งหมด:

```mermaid
flowchart LR
    U[ป้อนข้อมูลผู้ใช้] --> RP[ตัวแยกวิเคราะห์ประวัติย่อ]
    RP --> JD[ตัวแทน JD]
    JD --> MA[ตัวแทนจับคู่]
    MA --> GA[ตัววิเคราะห์ช่องว่าง + MCP]
    GA --> O[ผลลัพธ์สุดท้าย]
```

Agent Inspector จะแสดงโครงสร้างกราฟนี้เหมือนกันเมื่อเอเจนต์ทำงานในเครื่องท้องถิ่น ดูที่ [โมดูล 5 - ทดสอบในเครื่อง](05-test-locally.md) สำหรับภาพหน้าจอ

---

## การอ่านโค้ด WorkflowBuilder

ฟังก์ชัน `create_workflow()` ฉบับเต็มอยู่ใน [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) การเรียก `add_edge()` ทั้งสามครั้งสร้างท่อโซ่ตามลำดับ:

| # | Edge | ผลลัพธ์ |
|---|------|--------|
| 1 | `resume_executor → jd_executor` | JD Agent รับ `[PARSED RESUME]` + `[JOB DESCRIPTION PASS-THROUGH]` |
| 2 | `jd_executor → matching_executor` | MatchingAgent รับ `[JD REQUIREMENTS]` + `[PARSED RESUME PASS-THROUGH]` |
| 3 | `matching_executor → gap_executor` | GapAnalyzer รับรายงานความเหมาะสม + รายการช่องว่าง |

---

## การแก้ไขกราฟ

### การเพิ่มเอเจนต์ใหม่

เพื่อเพิ่มเอเจนต์ตัวที่ห้า (เช่น **InterviewPrepAgent** หลัง GapAnalyzer):

1. กำหนดค่าคงที่ `INTERVIEW_PREP_INSTRUCTIONS`
2. สร้างออบเจ็กต์ `Agent` + `AgentExecutor` (รูปแบบเดียวกับสี่เอเจนต์ที่มีอยู่)
3. เพิ่ม `.add_edge(gap_executor, interview_exec)` ใน `WorkflowBuilder`
4. อัปเดต `output_executors=[interview_exec]`

> **สำคัญ:** `start_executor` คือเอเจนต์เดียวที่รับอินพุตดิบจากผู้ใช้ เอเจนต์อื่นทั้งหมดจะรับผลลัพธ์จาก edge ด้านบน

---

## ความผิดพลาดของกราฟที่พบบ่อย

| ความผิดพลาด | อาการ | วิธีแก้ |
|---------|---------|-----|
| ขาด edge ไปยัง `output_executors` | เอเจนต์ทำงานแต่ผลลัพธ์ว่างเปล่า | ตรวจสอบให้แน่ใจว่ามีเส้นทางจาก `start_executor` ไปยังเอเจนต์ทุกตัวใน `output_executors` |
| การพึ่งพาห่วงวน | วนลูปไม่รู้จบหรือหมดเวลา | ตรวจสอบว่าไม่มีเอเจนต์ใดป้อนกลับไปยังเอเจนต์ด้านบน |
| เอเจนต์ใน `output_executors` ที่ไม่มี edge เข้า | ผลลัพธ์ว่างเปล่า | เพิ่ม `add_edge(source, that_agent)` อย่างน้อยหนึ่งครั้ง |
| `output_executors` หลายตัวโดยไม่มี fan-in | ผลลัพธ์มีเพียงการตอบสนองของเอเจนต์เดียว | ใช้เอเจนต์ผลลัพธ์ตัวเดียวที่รวมผลลัพธ์ หรือยอมรับผลลัพธ์หลายตัว |
| ขาด `start_executor` | เกิด `ValueError` ตอนสร้างเวิร์กโฟลว์ | กำหนด `start_executor` ทุกครั้งใน `WorkflowBuilder()` |

---

## การดีบักกราฟ

### การใช้ Agent Inspector

1. เริ่มเอเจนต์ในเครื่องด้วย F5
2. เปิด Agent Inspector (`Ctrl+Shift+P` → **Foundry Toolkit: Open Agent Inspector**)
3. ส่งข้อความทดสอบ
4. ในแผงตอบกลับของ Inspector ให้ดู **สตรีมเอาต์พุต** - จะแสดงผลลัพธ์ที่ตัวแทนแต่ละตัวมีส่วนในการทำงานตามลำดับ


### การใช้ logging

เพิ่ม logging ใน `main.py` เพื่อติดตามการไหลของข้อมูล:

```python
import logging
logger = logging.getLogger("resume-job-fit")

# ใน main() หลังจากสร้างเวิร์กโฟลว์:
logger.info("Workflow graph built with edges: RP→JD, JD→MA, MA→GA")
```

บันทึกของเซิร์ฟเวอร์แสดงลำดับการทำงานของเอเจนต์และการเรียกใช้เครื่องมือ MCP:

```
INFO:agent_framework:Executing agent: ResumeParser
INFO:agent_framework:Executing agent: JobDescriptionAgent
INFO:agent_framework:Executing agent: MatchingAgent
INFO:agent_framework:Executing agent: GapAnalyzer
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Kubernetes")
POST https://learn.microsoft.com/api/mcp → 200
INFO:agent_framework:Tool call: search_microsoft_learn_for_plan(skill="Terraform")
POST https://learn.microsoft.com/api/mcp → 200
```

---

### จุดตรวจสอบ

- [ ] คุณสามารถระบุรูปแบบการจัดการกระบวนการสองแบบในเวิร์กโฟลว์: โซ่ลำดับและการส่งต่อเนื้อหา
- [ ] คุณเข้าใจว่าทำไม `context_mode="last_agent"` ต้องมีการส่งต่อข้อมูลอย่างชัดเจนระหว่างเอเจนต์
- [ ] คุณสามารถอ่านโค้ด `WorkflowBuilder` และจับคู่แต่ละการเรียก `add_edge()` กับกราฟภาพได้
- [ ] คุณรู้วิธีเพิ่มเอเจนต์ใหม่ไปยังปลายทางของท่อโซ่
- [ ] คุณสามารถระบุความผิดพลาดทั่วไปของกราฟและอาการของพวกมันได้

---

**ก่อนหน้า:** [03 - กำหนดค่า Agents & Environment](03-configure-agents.md) · **ถัดไป:** [05 - ทดสอบในเครื่อง →](05-test-locally.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ปฏิเสธความรับผิดชอบ**:
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) ขณะที่เราพยายามให้ความถูกต้อง โปรดทราบว่าการแปลโดยอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางควรถูกพิจารณาเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ แนะนำให้ใช้การแปลโดยมนุษย์มืออาชีพ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดที่เกิดขึ้นจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->