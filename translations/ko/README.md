# Foundry Toolkit + Foundry 호스티드 에이전트 워크숍

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

<strong>Microsoft Foundry Agent Service</strong>에 AI 에이전트를 <strong>호스티드 에이전트</strong>로 빌드, 테스트 및 배포하세요 — 모두 VS Code에서 <strong>Microsoft Foundry 확장</strong>과 <strong>Foundry Toolkit</strong>을 사용하여 진행합니다.

> **호스티드 에이전트는 현재 프리뷰 상태입니다.** 지원되는 지역이 제한적이니 [지역 가용성](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)을 참조하세요.

> 각 랩 내 `agent/` 폴더는 Foundry 확장에 의해 <strong>자동으로 스캐폴딩</strong>됩니다 — 이후 코드를 커스터마이징하고, 로컬에서 테스트 후 배포합니다.

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabic](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgarian](../bg/README.md) | [Burmese (Myanmar)](../my/README.md) | [Chinese (Simplified)](../zh-CN/README.md) | [Chinese (Traditional, Hong Kong)](../zh-HK/README.md) | [Chinese (Traditional, Macau)](../zh-MO/README.md) | [Chinese (Traditional, Taiwan)](../zh-TW/README.md) | [Croatian](../hr/README.md) | [Czech](../cs/README.md) | [Danish](../da/README.md) | [Dutch](../nl/README.md) | [Estonian](../et/README.md) | [Finnish](../fi/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Greek](../el/README.md) | [Hebrew](../he/README.md) | [Hindi](../hi/README.md) | [Hungarian](../hu/README.md) | [Indonesian](../id/README.md) | [Italian](../it/README.md) | [Japanese](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Korean](./README.md) | [Lithuanian](../lt/README.md) | [Malay](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Nepali](../ne/README.md) | [Nigerian Pidgin](../pcm/README.md) | [Norwegian](../no/README.md) | [Persian (Farsi)](../fa/README.md) | [Polish](../pl/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Portuguese (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romanian](../ro/README.md) | [Russian](../ru/README.md) | [Serbian (Cyrillic)](../sr/README.md) | [Slovak](../sk/README.md) | [Slovenian](../sl/README.md) | [Spanish](../es/README.md) | [Swahili](../sw/README.md) | [Swedish](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Thai](../th/README.md) | [Turkish](../tr/README.md) | [Ukrainian](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamese](../vi/README.md)

> **로컬에 클론 하시겠습니까?**
>
> 이 저장소는 50개 이상의 언어 번역을 포함하여 다운로드 크기가 매우 큽니다. 번역 없이 클론하려면 스팽스 체크아웃을 사용하세요:
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
> 이렇게 하면 훨씬 빠른 다운로드로 강좌를 완료하는 데 필요한 모든 것을 얻을 수 있습니다.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

## 아키텍처

```mermaid
flowchart TB
    subgraph Local["로컬 개발 (VS 코드)"]
        direction TB
        FE["마이크로소프트 파운드리
        확장"]
        FoundryToolkit["파운드리 툴킷
        확장"]
        Scaffold["스캐폴드 에이전트 코드
        (main.py · agent.yaml · Dockerfile)"]
        Inspector["에이전트 검사기
        (로컬 테스트)"]
        FE -- "새 호스팅 에이전트 생성" --> Scaffold
        Scaffold -- "F5 디버그" --> Inspector
        FoundryToolkit -.- Inspector
    end

    subgraph Cloud["마이크로소프트 파운드리"]
        direction TB
        ACR["Azure 컨테이너
        레지스트리"]
        AgentService["파운드리 에이전트 서비스
        (호스팅 에이전트 런타임)"]
        Model["Azure OpenAI
        (gpt-4.1 / gpt-4.1-mini)"]
        Playground["파운드리 플레이그라운드
        & VS 코드 플레이그라운드"]
        ACR --> AgentService
        AgentService -- "/responses API" --> Model
        AgentService --> Playground
    end

    Scaffold -- "배포
    (Docker 빌드 + 푸시)" --> ACR
    Inspector -- "POST /responses
    (localhost:8088)" --> Scaffold
    Playground -- "프롬프트 테스트" --> AgentService

    style Local fill:#f0f4ff,stroke:#4a6cf7,stroke-width:2px
    style Cloud fill:#fff4e6,stroke:#f59e0b,stroke-width:2px
```
**흐름:** Foundry 확장이 에이전트를 스캐폴딩 → 코드 및 지침 커스터마이징 → Agent Inspector로 로컬 테스트 → Foundry에 배포(ACR로 Docker 이미지 푸시) → Playground에서 검증.

---

## 만들 내용

| 랩 | 설명 | 상태 |
|-----|-------------|--------|
| **랩 01 - 단일 에이전트** | <strong>"임원이 이해할 수 있게 설명하기" 에이전트</strong>를 만들고 로컬에서 테스트한 뒤 Foundry에 배포 | ✅ 가능 |
| **랩 02 - 다중 에이전트 워크플로우** | 이력서 적합도를 평가하고 학습 로드맵을 생성하는 4개의 에이전트 협업 시스템, **"이력서 → 직무 적합 평가기"** 빌드 | ✅ 가능 |

---

## 임원 에이전트를 만나보세요

이 워크숍에서는 기술 전문 용어를 차분하고 이사회에 제출할 수 있는 요약으로 번역해 주는 AI 에이전트인 <strong>"임원이 이해할 수 있게 설명하기" 에이전트</strong>를 만듭니다. 솔직히, 경영진 누구도 "v3.2에 도입된 동기식 호출로 인한 스레드 풀 고갈" 같은 말을 듣고 싶어하지 않으니까요.

이 에이전트는 내가 잘 작성한 사후 분석 보고서에 "*그래서… 웹사이트가 다운인가요 아니면 아닌가요?*"라는 반응을 여러 번 받은 후에 만들었습니다.

### 작동 방식

기술 업데이트를 입력하면 에이전트가 전문 용어 없이, 스택 트레이스나 불안감 없이 세 가지 핵심 요점으로 임원용 요약을 제공합니다. 즉, **무슨 일이 일어났고**, **비즈니스 영향**, 그리고 <strong>다음 단계</strong>입니다.

### 실제 예시

**사용자 발화:**
> "API 지연 시간이 v3.2에서 도입된 동기 호출로 인해 발생한 스레드 풀 고갈 때문에 증가했습니다."

**에이전트 응답:**

> **임원 요약:**
> - **발생한 일:** 최신 릴리스 후 시스템 속도가 느려졌습니다.
> - **비즈니스 영향:** 일부 사용자가 서비스 이용 중 지연을 경험했습니다.
> - **다음 단계:** 변경 사항을 롤백했으며 재배포 전에 수정 작업이 진행 중입니다.

### 이 에이전트를 사용하는 이유

매우 단순하고 단일 목적에 집중된 에이전트로, 복잡한 도구 체인에 얽매이지 않고 호스티드 에이전트 워크플로우를 처음부터 끝까지 배우기에 완벽합니다. 사실, 모든 엔지니어링 팀에서 하나쯤 필요할 기능입니다.

---

## 워크숍 구조

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

> **참고:** 각 랩 내 `agent/` 폴더는 명령 팔레트에서 `Microsoft Foundry: Create a New Hosted Agent`를 실행하면 <strong>Microsoft Foundry 확장</strong>이 생성합니다. 생성된 파일들은 에이전트 지침, 도구, 설정에 맞게 수정됩니다. 랩 01에서 이 과정을 처음부터 직접 따라해 볼 수 있습니다.

---

## 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab.git
cd Foundry_Toolkit_for_VSCode_Lab
```

### 2. Python 가상 환경 설정

```bash
python -m venv venv
```

가상 환경 활성화:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. 의존성 설치

```bash
pip install -r workshop/lab01-single-agent/agent/requirements.txt
```

### 4. 환경 변수 설정

에이전트 폴더 내 예제 `.env` 파일을 복사하고 값을 채우세요:

```bash
cp workshop/lab01-single-agent/agent/.env.example workshop/lab01-single-agent/agent/.env
```

`workshop/lab01-single-agent/agent/.env` 수정:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-account>.services.ai.azure.com/api/projects/<your-project>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

### 5. 워크숍 랩 따라하기

각 랩은 독립적인 모듈로 구성되어 있습니다. 기본을 배우려면 <strong>랩 01</strong>부터 시작하고, 다중 에이전트 워크플로우는 <strong>랩 02</strong>를 진행하세요.

#### 랩 01 - 단일 에이전트 ([전체 지침](workshop/lab01-single-agent/README.md))

| # | 모듈 | 링크 |
|---|--------|------|
| 1 | 필수 조건 읽기 | [00-prerequisites.md](workshop/lab01-single-agent/docs/00-prerequisites.md) |
| 2 | Foundry Toolkit 및 Foundry 확장 설치 | [01-install-foundry-toolkit.md](workshop/lab01-single-agent/docs/01-install-foundry-toolkit.md) |
| 3 | Foundry 프로젝트 생성 | [02-create-foundry-project.md](workshop/lab01-single-agent/docs/02-create-foundry-project.md) |
| 4 | 호스티드 에이전트 생성 | [03-create-hosted-agent.md](workshop/lab01-single-agent/docs/03-create-hosted-agent.md) |
| 5 | 지침 및 환경 설정 | [04-configure-and-code.md](workshop/lab01-single-agent/docs/04-configure-and-code.md) |
| 6 | 로컬 테스트 | [05-test-locally.md](workshop/lab01-single-agent/docs/05-test-locally.md) |
| 7 | Foundry에 배포 | [06-deploy-to-foundry.md](workshop/lab01-single-agent/docs/06-deploy-to-foundry.md) |
| 8 | Playground에서 검증 | [07-verify-in-playground.md](workshop/lab01-single-agent/docs/07-verify-in-playground.md) |
| 9 | 문제 해결 | [08-troubleshooting.md](workshop/lab01-single-agent/docs/08-troubleshooting.md) |

#### 랩 02 - 다중 에이전트 워크플로우 ([전체 지침](workshop/lab02-multi-agent/README.md))

| # | 모듈 | 링크 |
|---|--------|------|
| 1 | 필수 조건 (랩 02) | [00-prerequisites.md](workshop/lab02-multi-agent/docs/00-prerequisites.md) |
| 2 | 다중 에이전트 아키텍처 이해 | [01-understand-multi-agent.md](workshop/lab02-multi-agent/docs/01-understand-multi-agent.md) |
| 3 | 다중 에이전트 프로젝트 스캐폴딩 | [02-scaffold-multi-agent.md](workshop/lab02-multi-agent/docs/02-scaffold-multi-agent.md) |
| 4 | 에이전트 및 환경 구성 | [03-configure-agents.md](workshop/lab02-multi-agent/docs/03-configure-agents.md) |
| 5 | 오케스트레이션 패턴 | [04-orchestration-patterns.md](workshop/lab02-multi-agent/docs/04-orchestration-patterns.md) |
| 6 | 로컬 테스트 (다중 에이전트) | [05-test-locally.md](workshop/lab02-multi-agent/docs/05-test-locally.md) |
| 7 | Foundry에 배포 | [06-deploy-to-foundry.md](workshop/lab02-multi-agent/docs/06-deploy-to-foundry.md) |
| 8 | 플레이그라운드에서 확인 | [07-verify-in-playground.md](workshop/lab02-multi-agent/docs/07-verify-in-playground.md) |
| 9 | 문제 해결 (멀티 에이전트) | [08-troubleshooting.md](workshop/lab02-multi-agent/docs/08-troubleshooting.md) |

---

## 유지 관리자

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

## 필요한 권한 (간략 참고)

| 시나리오 | 필요한 역할 |
|----------|---------------|
| 새 Foundry 프로젝트 만들기 | Foundry 리소스에 대한 **Azure AI 소유자** |
| 기존 프로젝트에 배포 (새 리소스) | 구독에 대한 **Azure AI 소유자** + <strong>기여자</strong> |
| 완전히 구성된 프로젝트에 배포 | 계정에 대한 **읽기 권한자** + 프로젝트에 대한 **Azure AI 사용자** |

> **중요:** Azure `소유자` 및 `기여자` 역할에는 <em>관리</em> 권한만 포함되며, <em>개발</em> (데이터 작업) 권한은 포함되지 않습니다. 에이전트를 빌드하고 배포하려면 **Azure AI 사용자** 또는 <strong>Azure AI 소유자</strong>가 필요합니다.

---

## 참고 자료

- [빠른 시작: 첫 번째 호스팅 에이전트 배포 (VS Code)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent)
- [호스팅 에이전트란?](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [VS Code에서 호스팅 에이전트 워크플로우 만들기](https://learn.microsoft.com/azure/foundry/agents/how-to/vs-code-agents-workflow-pro-code)
- [호스팅 에이전트 배포](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Foundry를 위한 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
- [아키텍처 리뷰 에이전트 샘플](https://github.com/Azure-Samples/agent-architecture-review-sample) - MCP 도구, Excalidraw 다이어그램, 이중 배포가 포함된 실제 호스팅 에이전트

---

## 라이선스

[MIT](../../LICENSE)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력했으나, 자동 번역에는 오류나 부정확성이 포함될 수 있음을 유의하시기 바랍니다. 원본 문서는 해당 원어로 된 문서를 권위 있는 출처로 간주해야 합니다. 중요한 정보의 경우, 전문 인력의 번역을 권장합니다. 본 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->