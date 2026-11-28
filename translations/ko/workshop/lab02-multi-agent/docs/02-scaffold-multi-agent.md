# 모듈 2 - 멀티 에이전트 프로젝트 스캐폴딩

⏱️ 약 5분

이 모듈에서는 [Foundry Toolkit for VS Code](https://aka.ms/foundrytk)를 사용하여 <strong>멀티 에이전트 프로젝트를 스캐폴딩</strong>합니다. 이 마법사는 `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`과 VS Code 디버그 구성을 생성하므로, 모듈 3에서 4-에이전트 워크플로 연결에 집중할 수 있습니다.

> **핵심 개념:** 스캐폴드는 하나의 에이전트가 있는 작동 중인 스텁입니다. 자리 표시자 로직은 모듈 3에서 `WorkflowBuilder` 그래프로 교체합니다. 보일러플레이트를 처음부터 작성하지 않습니다.

> **참고 구현:** [`PersonalCareerCopilot/`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot)은 완전한 작동 예제입니다. 진행하면서 작업을 비교하는 데 사용하세요.

### 스캐폴드 마법사 흐름

```mermaid
flowchart LR
    A[Command Palette: Create New Hosted Agent] --> B[Language: Python]
    B --> C[API Type: Response API]
    C --> D[Template: Workflows]
    D --> E[Select Model]
    E --> F[Workspace Folder and Agent Name]
    F --> G[Generated Project]
```

---

## 1단계: Create Hosted Agent 마법사 열기

1. `Ctrl+Shift+P`를 눌러 <strong>명령 팔레트</strong>를 엽니다.
2. 입력: <strong>Foundry Toolkit: Create new Hosted Agent</strong>를 선택합니다.
3. 마법사가 **Agent Details** 탭에서 열립니다.

> **대안:** 활동 표시줄에서 **Foundry Toolkit** 아이콘을 클릭 → **Hosted Agents** 옆의 **+** 아이콘 클릭 → **Create New Hosted Agent** 클릭.

---

## 2단계: 설정 선택

![샘플에서 Hosted Agent 생성 - Workflows 템플릿이 선택된 Agent Details 탭](../../../../../translated_images/ko/02-scaffold-wizard-details.af4798708b4a87f4.webp)

1. 왼쪽 네비게이션/옵션 섹션에서 다음을 선택합니다:

| 메뉴 | 선택 | 설명 |
|--------|-----------|-------|
| <strong>언어</strong> | Python | C# (.NET)도 지원 |
| <strong>프레임워크</strong> | Agent Framework | `Agent`, `AgentExecutor`, `WorkflowBuilder` 제공 |
| **API 유형** | Response API | `POST /responses` - 플랫폼 관리 기록, 스트리밍 지원 |
| <strong>템플릿</strong> | **Workflows** | 여러 에이전트를 순차 처리 |

2. 선택 후 **Next** 클릭

![샘플에서 Hosted Agent 생성 - 폴더 이름으로 PersonalCareerCopilot이 표시된 생성 탭](../../../../../translated_images/ko/02-scaffold-wizard-create.ae0c285c309698ba.webp)

3. 다음 창에서 다음을 선택합니다:

| 메뉴 | 선택 | 설명 |
|--------|-----------|-------|
| **작업 공간 폴더** | 대상 폴더 찾아보기 | 예: 이 저장소의 `workshop/lab02-multi-agent/` |
| **에이전트 이름** | `PersonalCareerCopilot` | 이것이 프로젝트 디렉터리 이름이 됨 |
| **모델 배포** | 배포한 모델 선택 | 예: Lab 01의 `gpt-4.1-mini` |

4. **Create** 클릭하여 프로젝트 스캐폴딩. VS Code가 파일을 생성하고 폴더를 엽니다.

> **팁:** [`gpt-4.1-mini`](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series)는 멀티 에이전트 개발에 속도와 품질을 잘 조화합니다.

---

## 3단계: 생성된 프로젝트 검사

스캐폴딩 완료 후 탐색기(`Ctrl+Shift+E`)에서 다음 파일들이 보이는지 확인하세요:

```
📂 <your-agent-name>/
├── .azdignore          ← Files excluded from Azure Developer CLI deployments
├── .dockerignore       ← Files excluded from Docker builds
├── .env                ← Environment variables (placeholders - fill in Module 3)
├── .vscode/
│   ├── launch.json     ← Debug config (F5 → run + Agent Inspector)
│   └── tasks.json      ← VS Code task definitions
├── agent.yaml          ← Agent definition (kind: hosted, protocol: responses)
├── Dockerfile          ← Container config for deployment
├── main.py             ← Stub agent entry point (replace with WorkflowBuilder in Module 3)
└── requirements.txt    ← Python dependencies
```

> **중요:** 이 스캐폴딩된 폴더를 VS Code에서 직접 열어야 `.vscode/launch.json`와 `tasks.json`가 F5 디버깅에 올바르게 적용됩니다.

### 주요 파일 설명

| 파일 | 목적 |
|------|---------|
| `agent.yaml` | `kind: hosted` 선언, 환경 변수 매핑, `/responses` 프로토콜 정의 |
| `main.py` | 스텁: 하나의 `FoundryChatClient` → `Agent` → `ResponsesHostServer`. 모듈 3에서 4개의 에이전트 + `WorkflowBuilder`로 대체 |
| `Dockerfile` | `python:3.12-slim`, `requirements.txt` 설치, 포트 8088 공개, `python main.py` 실행 |
| `requirements.txt` | `agent-framework-foundry`, `agent-framework-foundry-hosting`, `mcp<2,>=1.24.0`, `debugpy` |

> **참고:** 전체 생성 콘텐츠는 [`PersonalCareerCopilot/agent.yaml`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) 및 [`PersonalCareerCopilot/requirements.txt`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/requirements.txt) 참조.

---

### ✅ 체크포인트

- [ ] 스캐폴드 마법사 완료 - 탐색기에서 새 프로젝트 폴더 확인
- [ ] 예상된 모든 파일 존재 확인: `agent.yaml`, `main.py`, `Dockerfile`, `requirements.txt`, `.env`
- [ ] `agent.yaml`가 `kind: hosted`와 `protocol: responses` 표시
- [ ] `main.py`가 `Agent`, `FoundryChatClient`, `ResponsesHostServer`를 가져옴
- [ ] 스캐폴드된 폴더가 VS Code 작업 공간 루트로 열림
- [ ] `main.py`는 스텁임을 이해함 - `WorkflowBuilder`가 모듈 3에서 추가됨

---

**이전:** [01 - 멀티 에이전트 아키텍처 이해](01-understand-multi-agent.md) · **다음:** [03 - 에이전트 및 환경 구성 →](03-configure-agents.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->