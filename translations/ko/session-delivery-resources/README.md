# 이 세션 전달 방법

이 세션을 전달해 주셔서 감사합니다!

워크숍을 진행하기 전에 다음을 수행해 주세요:

1. 이 문서와 포함된 모든 리소스를 전부 읽으세요.
2. 세션 전달 녹화와 워크숍 전 과정을 시청하세요.
3. 두 개의 핸즈온 랩을 최소 **한 번 이상** 본인 컴퓨터에서 처음부터 끝까지 진행해 보세요.
4. Microsoft Foundry 프로젝트, 모델 배포, 할당량을 검증하세요.
5. 불명확한 사항이 있으면 유지 관리자에게 문의하세요.

---

## 파일 요약

| 리소스                       | 링크                                                                                     | 설명                                                                                   |
|-------------------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| 워크숍 슬라이드 자료            | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                            | 발표자 노트와 내장된 데모 비디오가 포함된 워크숍 발표 슬라이드                           |
| 세션 전달 녹화                | _유지 관리자가 제공 예정_                                                                  | 워크숍 소개 및 슬라이드 안내 녹화                                                       |
| 워크숍 전 과정 녹화           | _유지 관리자가 제공 예정_                                                                  | 학습자의 관점에서 본 두 랩의 끝까지 진행 녹화                                           |
| 워크숍 문서                   | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)        | 소스 리포지토리, 랩 README, 단계별 모듈                                                  |
| 랩 01 - 단일 에이전트          | [Lab 01](../workshop/lab01-single-agent/README.md)                                       | 핸즈온 랩: *Explain Like I'm an Executive* 호스팅 에이전트 빌드, 테스트, 배포            |
| 랩 02 - 다중 에이전트 워크플로우 | [Lab 02](../workshop/lab02-multi-agent/README.md)                                        | 핸즈온 랩: 4 에이전트 *Resume to Job Fit Evaluator* 워크플로우 빌드                       |
| 데모 1: Executive Agent         | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                     | 랩 01 데모: 기술 용어를 임원 요약으로 번역                                              |
| 데모 2: Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)           | 랩 02 데모: 이력서-직무 적합도 점수를 매기고 추천을 생성하는 4 에이전트 워크플로우        |

> **강사용 노트:** 슬라이드 데크와 비디오 링크는 녹화가 공개된 후 추가됩니다. 그전까지는 최신 자료를 위해 유지 관리자에게 연락하세요 ([연락처](#연락처) 참조).

---

## 시작하기

이 워크숍은 개발자가 **Microsoft Foundry Toolkit** 확장으로 VS Code 내에서 <strong>Microsoft Foundry Agent Service</strong>에 AI 에이전트를 <strong>호스팅 에이전트</strong>로 빌드, 테스트 및 배포하는 방법을 가르칩니다.

워크숍은 슬라이드, **2개의 라이브 데모**, **2개의 핸즈온 랩** 등 여러 섹션으로 나뉩니다.

### 시간 배분

#### 전체 진행 (약 2시간)

| 시간           | 설명                                                                 |
|----------------|----------------------------------------------------------------------|
| 0:00 - 10:00   | 소개: 호스팅 에이전트, Foundry Agent Service, 툴킷                   |
| 10:00 - 20:00  | 데모: Executive Agent 전체 과정                                      |
| 20:00 - 60:00  | 랩 01 - 단일 에이전트 (빌드, 로컬 테스트, 배포, 플레이그라운드)       |
| 60:00 - 110:00 | 랩 02 - 다중 에이전트 워크플로우 (Resume to Job Fit Evaluator)       |
| 110:00 - 120:00| 마무리, Q&A, 추가 학습 자료                                          |

#### 단축 진행 (약 75분)

| 시간          | 설명                                                  |
|--------------|------------------------------------------------------|
| 0:00 - 10:00 | 소개 및 개요                                          |
| 10:00 - 20:00| 데모: Executive Agent                                 |
| 20:00 - 70:00| 랩 01만 진행 (랩 02는 셀프 페이스 안내)               |
| 70:00 - 75:00| 마무리 및 Q&A                                        |

### 준비 사항

| 리소스                       | 링크                                                                                      | 설명                                              |
|------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------|
| 워크숍 문서                 | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)         | 워크숍 문서 및 소스                                |
| 랩 01 설명서               | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                            | 핸즈온 랩: 단일 호스팅 에이전트                    |
| 랩 02 설명서               | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                             | 핸즈온 랩: 다중 에이전트 워크플로우                 |
| 사전 요구사항 체크리스트    | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)            | 요구 도구, 계정, Azure 접근 권한                    |
| 호스팅 에이전트 빠른 시작 (azd) | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | `azd`로 호스팅 에이전트 배포 공식 빠른 시작            |
| 호스팅 에이전트 지역 가용성    | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | 지원되는 호스팅 에이전트 지역(프리뷰)                |

### 강사용 사전 조건

전달 전에 다음을 확인하세요:

- 리소스 생성 권한(소유자 또는 리소스 그룹 기여자 권한)이 있는 **Azure 구독**.
- [호스팅 에이전트를 지원하는 지역](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)의 **Microsoft Foundry 프로젝트** 접근.
- Foundry 프로젝트 내 **gpt-4.1** (또는 **gpt-4.1-mini**) 할당량.
- 다음 도구 설치:
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 확장](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI (`azd`)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/) (선택 사항)
  - Python 3.10 이상

전달 전에 [호스팅 에이전트 `azd` 빠른 시작](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)을 최소 한 번 실행하여, 학습자가 막힐 경우 참조할 수 있도록 정상 작동하는 Foundry 프로젝트, 모델 배포, Azure 컨테이너 레지스트리를 준비하세요.

---

## 슬라이드 진행 안내

데크는 랩의 흐름과 동일합니다. 각 섹션별 제안 토킹 포인트:

| 섹션                      | 핵심 메시지                                                                                               |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| 제목 및 아젠다             | 포털 전환 없이 *VS Code to Foundry* 워크숍임을 소개                                                      |
| 왜 호스팅 에이전트인가?     | 관리형 런타임, ACR 기반 배포, OpenAI 호환 `/responses` API, Foundry 프로젝트 범위                         |
| 아키텍처 다이어그램        | [README 아키텍처](../README.md#architecture) 설명: 스캐폴드, 인스펙터, ACR, 에이전트 서비스               |
| 호스팅 에이전트 구성요소    | `agent.yaml`, `Dockerfile`, `main.py`, `requirements.txt` 각 파일 역할                                   |
| 라이브 데모: Executive Agent | VS Code로 전환하여 [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) 데모 전체 진행 (데모 1 참조) |
| 라이브 데모: Resume to Job Fit Evaluator | VS Code로 전환하여 [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) 4 에이전트 데모 실행 (데모 2 참조) |
| 랩 01 개요                 | 학습자에게 인계. [`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md) 안내 |
| 다중 에이전트 패턴          | 순차 실행 vs 병행 실행 vs 핸드오프 - 랩 02 시작 전에 미리 소개                                          |
| 랩 02 개요                 | 학습자에게 인계. [`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md) 안내 |
| 마무리 및 자료             | [추가 리소스](#추가-자료) 섹션의 학습 지속 링크                                           |

---

## 데모

전달에는 2개의 라이브 데모가 포함됩니다. 각각에 10분씩 배정하세요.

| 데모                  | 랩   | 파일                                                                                 | 보여줄 내용                                            |
|----------------------|-------|--------------------------------------------------------------------------------------|-------------------------------------------------------|
| Executive Agent       | 랩 01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)         | 단일 호스팅 에이전트; 기술 용어를 임원 요약으로 변환     |
| Resume to Job Fit Evaluator | 랩 02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4 에이전트 오케스트레이션; 이력서-직무 적합도 점수 및 추천 생성 |

### 데모 1: Executive Agent

[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent)에 있는 독립형 에이전트입니다. 랩 01 전에 10분 데모로 사용하세요.

1. [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py)를 열고 에이전트 정의(시스템 프롬프트, 모델, 프레임워크)를 설명하세요.
2. `F5`를 눌러 <strong>Agent Inspector</strong>를 로컬에서 실행하세요.
3. [README](../README.md#see-it-in-action)에 있는 샘플 프롬프트를 붙여넣고 임원 요약 응답을 보여주세요.
4. 배포 산출물을 설명하기 위해 [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml)과 [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile)를 보여주세요.
5. 완료 대기 없이 배포 흐름(Docker 빌드, ACR 푸시, 호스팅 에이전트 생성)을 시연하세요.

### 데모 2: Resume to Job Fit Evaluator

[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)에 있는 4 에이전트 워크플로우입니다. 랩 02 전에 10분 데모로 사용하세요.

1. [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)를 열어 4 에이전트가 순차적으로 연결된 오케스트레이션을 보여주세요.
2. `F5`를 눌러 다중 에이전트 워크플로우용 <strong>Agent Inspector</strong>를 실행하세요.
3. 검사기 채팅에 짧은 직무 기술서와 샘플 이력서를 붙여넣으세요.
4. 4 에이전트 파이프라인(이력서 파서, 직무 요구사항 추출기, 적합도 평가기, 추천 작성기)를 진행하며 설명하세요.
5. 각 하위 에이전트 출력이 다음 에이전트 컨텍스트가 되는 핸드오프 패턴을 강조하세요.
6. [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml)를 보여 주고 데모 1의 단일 에이전트와 비교하세요.

---

## 전달 팁

- **초기 기대치 설정:** 호스팅 에이전트는 프리뷰 상태입니다 - 지역 한계와 할당량을 미리 알리면 랩 중에 놀라지 않습니다.
- **먼저 사전 요구사항 작업 실행:** 두 랩 모두 `Validate prerequisites` VS Code 작업이 포함되어 있으며, 코드를 작성하기 전에 학습자가 반드시 실행하게 하세요.
- **Agent Inspector를 계속 보여주세요:** 대부분의 "아하" 순간은 학습자가 로컬 `/responses` 왕복이 활성화되는 것을 볼 때 발생합니다.
- **대체 프로젝트 준비:** 학습자의 Foundry 프로젝트가 할당량 제한에 걸리면 배포 단계를 막지 않도록 미리 준비된 프로젝트를 공유하세요.
- **학습자를 짝지어 주세요:** 랩 02(다중 에이전트)는 학습자가 파트너와 오케스트레이션을 논의할 수 있으면 훨씬 수월합니다.
- **문서 모듈을 체크포인트로 사용:** 각 랩의 `docs/` 폴더는 8개의 번호별 모듈로 나뉘므로 자연스러운 휴식 지점으로 활용하세요.
- **공유 랩 머신에서 기본 Docker 이미지를 미리 당겨 놓으세요** 레지스트리 속도 제한을 피할 수 있습니다.

---

## 전달 중 문제 해결

| 증상                         | 우선 시도할 것                                                                              |
|------------------------------|--------------------------------------------------------------------------------------------|
| Agent Inspector가 연결되지 않음   | 포트 `8088`이 비어 있고 `Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` 작업이 실행 중인지 확인하세요. |
| 디버거가 연결되지 않음           | 포트 `5679`가 비어 있는지 확인하세요; `debugpy`가 이미 바인딩된 경우 VS Code를 재시작하세요.    |
| `azd up`가 인증 오류로 실패      | `az login`과 `azd auth login`을 실행하고 올바른 테넌트가 선택되었는지 확인하세요.              |
| 배포가 ACR 푸시 단계에서 멈춤     | Docker Desktop이 실행 중이고 레지스트리에 대해 `AcrPush` 권한이 있는지 확인하세요.            |
| 모델이 404 / 배포 불가 반환        | `agent.yaml` 내 모델 배포 이름이 Foundry 프로젝트 내 배포 이름과 일치해야 합니다.             |

| 호스트 에이전트가 `Provisioning` 상태에서 멈춤         | 프로젝트 지역이 [호스트 에이전트를 지원하는지](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)와 할당량이 있는지 확인하세요. |
| 플레이그라운드가 401 오류 반환                       | VS Code 활동 표시줄에서 Foundry 확장 프로그램을 다시 인증하세요.                                     |

자세한 안내를 위해 각 실습에는 자체 `08-troubleshooting.md` 문서가 제공되며, 학습자에게 안내하세요:

- 실습 01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- 실습 02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## 이 세션 맞춤화하기

워크샵을 청중에 맞게 조정하실 수 있습니다. 일반적인 변형은 다음과 같습니다:

- **백엔드 청중:** `agent.yaml`, Docker, ACR에 더 많은 시간을 할애하고 플레이그라운드 데모는 줄이세요.
- **시민 개발자 청중:** Foundry 확장 UI에서 스캐폴딩 작업을 진행하고 CLI 단계는 줄이세요.
- **단일 트랙 60분 세션:** 소개, 데모 및 실습 01만 진행하세요.
- **워크샵 전용(슬라이드 없음) 형식:** 두 실습 README를 모두 열고 기본 스크립트로 사용하세요.

실습을 확장하는 경우, 변경 사항을 PR로 기여하여 다른 강사들이 혜택을 받을 수 있게 해주세요.

---

## 추가 자료

- [Microsoft Foundry 문서](https://learn.microsoft.com/azure/ai-foundry/)
- [호스트 에이전트 개요](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [빠른 시작: 첫 호스트 에이전트 배포 (`azd`)](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [호스트 에이전트 배포 방법](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 연락처

이 세션 진행에 대한 질문이 있으면 [워크샵 저장소](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues)에 이슈를 열고 담당자에게 태그를 지정하세요.

| 역할                | 이름           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| 담당자 / 연락처     | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->