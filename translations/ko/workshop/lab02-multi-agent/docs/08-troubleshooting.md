# 모듈 8 - 문제 해결

이 모듈에서는 멀티 에이전트 워크플로우에 특화된 일반적인 오류, 수정 및 디버깅 전략을 다룹니다.

## 에이전트 출력 문제

### GapAnalyzer가 "여전히 매칭 리포트가 없다고 합니다"

**증상:** GapAnalyzer의 응답이 "Missing Skills"와 "Certification Gaps"가 포함된 매칭 리포트를 붙여넣으라고 합니다. 이 경우 이력서와 직무 설명을 모두 전송했는데도 발생합니다.

**원인:** JD 텍스트가 JD 에이전트로 하류로 전달되지 않았습니다. `context_mode="last_agent"` 설정에서는 `resume_executor`만 사용자의 원본 메시지를 봅니다. 만약 `RESUME_PARSER_INSTRUCTIONS`에 JD 텍스트가 출력에 포함되지 않으면 JD 에이전트에는 JD가 없고 MatchingAgent는 적합 점수를 계산할 수 없으며 GapAnalyzer는 의미 없는 입력을 받게 됩니다.

**진단:**

서버 로그에서 MatchingAgent 스팬을 찾으세요. 만약 포함되어 있다면:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
통과가 누락되었거나 깨진 상태입니다.

**수정:** `main.py`의 `RESUME_PARSER_INSTRUCTIONS`에 `[JOB DESCRIPTION PASS-THROUGH]` 섹션과 다음 규칙이 포함되어 있는지 확인하세요:
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
또한 `JOB_DESCRIPTION_INSTRUCTIONS`에 `[PARSED RESUME PASS-THROUGH]` 중계 규칙이 포함되어 있는지 확인하세요:
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
만약 둘 중 하나의 지시문 블록이 스캐폴드 마법사의 스텁이면 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)의 완성본으로 교체하세요.

### MatchingAgent가 “Cannot compute fit score - no JD provided”를 출력함

위와 동일한 근본 원인입니다. MatchingAgent는 JD Agent의 출력을 받았지만 `[PARSED RESUME PASS-THROUGH]` 섹션이 없거나 비어 있어서 두 프로필을 비교할 수 없었습니다. 다음을 확인하세요:
1. `JOB_DESCRIPTION_INSTRUCTIONS`에 `Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.` 중계 규칙이 포함되어 있는지
2. `MATCHING_AGENT_INSTRUCTIONS`가 `[JD REQUIREMENTS]`와 `[PARSED RESUME PASS-THROUGH]` 섹션을 찾도록 지시하는지

두 지시문 블록 모두 [`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)에서 완성본으로 교체하세요.

### 응답이 두 번 나타남

**증상:** GapAnalyzer 출력(또는 전체 파이프라인 출력)이 Agent Inspector 응답에 두 번 나타납니다.

**원인:** `WorkflowBuilder`가 들어오는 엣지에 대해 OR-세만틱을 사용하여 <strong>어떤</strong> 선행 작업이 완료되면 하류 실행자가 바로 실행됩니다. `matching_executor`에 `resume_executor`와 `jd_executor`에서의 두 개의 입력 엣지가 있으면 ResumeParser가 끝났을 때 한 번, JD Agent가 끝났을 때 한 번 실행되어 GapAnalyzer도 두 번 실행됩니다.

**수정:** `WorkflowBuilder` 그래프가 팬인 없이 엄격히 순차적인 파이프라인이 되도록 하세요:

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor에서 아님
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

`.add_edge(resume_executor, matching_executor)` 같은 불필요한 라인이 있다면 제거하세요. JD Agent 출력의 `[PARSED RESUME PASS-THROUGH]` 중계는 이미 MatchingAgent가 이력서에 접근하도록 합니다.

---

## 환경 및 구성 문제

### .env 값 누락 또는 오류

`.env` 파일은 `PersonalCareerCopilot/` 디렉터리( `main.py`와 같은 수준)에 있어야 합니다:

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

예상되는 `.env` 내용:

**경로 A - Foundry 클라우드:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**경로 B - Foundry 로컬:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 두 경로 모두 `FOUNDRY_PROJECT_ENDPOINT`를 사용합니다. 값은 다릅니다: 클라우드는 `https://` Foundry 엔드포인트, 로컬은 `http://localhost:5273/v1` 입니다. 정확한 모델 별칭을 확인하려면 `foundry model list`를 실행하세요.

> **FOUNDRY_PROJECT_ENDPOINT 찾기:** 
- VS Code의 **Foundry Toolkit** 사이드바 열기 → 프로젝트 우클릭 → **Copy Project Endpoint**.
- 또는 [Azure Portal](https://portal.azure.com) → Foundry 프로젝트 → <strong>개요</strong> → **프로젝트 엔드포인트**.

> **AZURE_AI_MODEL_DEPLOYMENT_NAME 찾기:** Foundry Toolkit 사이드바에서 프로젝트 확장 → **Models** → 배포된 모델 이름 찾기 (예: `gpt-4.1-mini`).

### 환경 변수 우선순위

`main.py`는 `load_dotenv(override=True)`를 사용하므로:

| 우선순위 | 출처 | 두 설정이 모두 있을 때 우선 적용? |
|----------|--------|------------------------|
| 1 (최고) | `.env` 파일 | 예 |
| 2 | 셸 / 컨테이너 환경 변수 | `.env`에 같은 키가 없으면 사용 |

로컬 개발에서는 `.env`가 진실의 출처이며 (`.env` 편집 즉시 반영됨), 호스팅 배포에서는 Foundry가 컨테이너 레벨에서 환경 변수를 주입합니다. 이 실습 환경에서 `.env`는 이미지에 포함되지 않으므로 주입된 컨테이너 값이 사용됩니다.

---

## 버전 호환성

### 패키지 버전 매트릭스

멀티 에이전트 워크플로우는 특정 패키지 버전을 요구합니다. 버전 불일치 시 런타임 오류가 발생합니다.

| 패키지 | 요구 버전 | 확인 명령 |
|---------|-----------------|---------------|
| `agent-framework-foundry` | 최신 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 최신 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 최신 | `pip show debugpy` |
| Python | 3.12 이상 | `python --version` |

### 일반적인 버전 오류

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 수정: agent-framework-foundry를 다시 설치하세요
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 수정: mcp 패키지 업그레이드
pip install mcp --upgrade
```

### 모든 버전 한 번에 확인하기

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

예상 출력:

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## 배포 문제

### 배포 후 컨테이너가 시작되지 않음

1. **컨테이너 로그 확인:**
   - **Foundry Toolkit** 사이드바 열기 → **Hosted Agents (Preview)** 확장 → 에이전트 클릭 → 버전 확장 → **Container Details** → **Logs**.
   - Python 스택 트레이스나 모듈 누락 오류 찾기.

2. **일반적인 컨테이너 시작 실패 원인:**

   | 로그 내 오류 | 원인 | 수정 방법 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt`에 패키지 누락 | 패키지 추가 후 재배포 |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml` 또는 `.env` 환경 변수 미설정 | `agent.yaml` → `environment_variables`(호스팅) 또는 `.env`(로컬) 업데이트 |
   | `azure.identity.CredentialUnavailableError` | 관리형 ID 미설정 | Foundry가 자동 설정함 - 확장 프로그램으로 배포하는지 확인 |
   | `OSError: port 8088 already in use` | Dockerfile 포트 잘못 노출 또는 포트 충돌 | Dockerfile의 `EXPOSE 8088` 및 `CMD ["python", "main.py"]` 확인 |
   | 컨테이너가 코드 1로 종료 | `main()` 내 처리되지 않은 예외 | 로컬 테스트([모듈 5](05-test-locally.md))로 사전 오류 검출 |

3. **수정 후 재배포:**
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 동일 에이전트 선택 → 새 버전 배포.

### 배포 시간 지연

멀티 에이전트 컨테이너는 시작 시 4개의 에이전트 인스턴스를 생성하기 때문에 시작 시간이 더 길어집니다. 일반 예상 시간:

| 단계 | 예상 소요 시간 |
|-------|----------------|
| 컨테이너 이미지 빌드 | 1-3분 |
| 이미지 ACR 푸시 | 30-60초 |
| 컨테이너 시작 (단일 에이전트) | 15-30초 |
| 컨테이너 시작 (멀티 에이전트) | 30-120초 |
| 플레이그라운드에서 에이전트 사용 가능 | "Started" 후 1-2분 |

> "Pending" 상태가 5분 이상 지속되면 오류 확인을 위해 컨테이너 로그를 점검하세요.

---

## RBAC 및 권한 문제

### `403 Forbidden` 또는 `AuthorizationFailed`

Foundry 프로젝트에 **[Foundry User](https://aka.ms/foundry-ext-project-role)** 역할이 필요합니다 (과거 이름은 **Azure AI User**, 역할 ID는 동일):

1. [Azure Portal](https://portal.azure.com) → Foundry <strong>프로젝트</strong> 리소스로 이동.
2. **액세스 제어 (IAM)** → **역할 할당** 클릭.
3. 이름 검색 → **Foundry User** (또는 이전 이름 **Azure AI User**)가 목록에 있는지 확인.
4. 없으면: <strong>추가</strong> → **역할 할당 추가** → **Foundry User** 검색 → 계정에 할당.

자세한 내용은 [Microsoft Foundry RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 문서를 참조하세요.

### 모델 배포 접근 불가

에이전트가 모델 관련 오류를 반환하면:

1. 모델이 배포되었는지 확인: Foundry 사이드바 → 프로젝트 확장 → **Models** → `gpt-4.1-mini`(또는 본인 모델) 상태가 <strong>Succeeded</strong>인지 확인.
2. 배포 이름이 일치하는지 확인: `.env`(또는 `agent.yaml`)의 `AZURE_AI_MODEL_DEPLOYMENT_NAME`과 사이드바상의 실제 배포 이름 비교.
3. 배포가 만료된 경우(무료 등급): [모델 카탈로그](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)에서 재배포 (`Ctrl+Shift+P` → **Foundry Toolkit: Open Model Catalog**).

---

## Foundry Local 문제 (경로 B)

### Foundry Local 서비스가 실행 중이 아님

```powershell
# 상태 확인
foundry local status

# 서비스가 중지된 경우 시작하기
foundry local start
```

| 증상 | 원인 | 해결 방법 |
|---------|-------|-----|
| 헬스체크가 `503` 반환 | 서비스 미실행 | `foundry local start` 명령 실행 또는 Foundry Toolkit 사이드바에서 <strong>시작</strong> 클릭 |
| 헬스체크 타임아웃 | 모델 로딩 중 | 시작 후 30–60초 대기; 큰 모델은 더 오래 걸림 |
| `/v1/health` 요청 시 `StatusCode: 404` | 잘못된 포트 | 기본값은 `5273`임. `foundry local status`로 실제 포트 확인 |
| 자원 부족 | Foundry Local이 약 4GB RAM 여유 필요 | 다른 애플리케이션 종료 |
| 모델 다운로드 실패 | 디스크 공간 부족 | 모델 크기는 2–8GB. 공간 확보 후 `foundry model pull <이름>` 실행 |

### 모델 이름 불일치

```powershell
# 다운로드한 모델과 그 정확한 별칭을 나열하세요
foundry model list
```

`.env`의 `AZURE_AI_MODEL_DEPLOYMENT_NAME`은 표시된 별칭과 정확히 일치해야 합니다 (예: `phi-4-mini`, 대문자 구분).

### 로컬 실행 시 `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` (경로 B)

이 랩의 `main.py`는 `os.environ["FOUNDRY_PROJECT_ENDPOINT"]`를 사용합니다. Foundry Local은 이 변수가 로컬 서비스를 가리켜야 하며, `AZURE_AI_PROJECT_ENDPOINT`가 아닙니다. `.env` 파일을 다음과 같이 구성하세요:

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCP 도구가 여전히 외부 호출을 함 (경로 B)

이는 예상된 동작입니다. `search_microsoft_learn_for_plan` 도구는 `https://learn.microsoft.com/api/mcp`에서 학습 자료를 가져옵니다. **오직 기술 이름 쿼리만 네트워크를 통해 전송되며** 이력서와 JD 텍스트는 장치 내에서만 처리되고 전송되지 않습니다. 완전 오프라인 작동이 필요하면 도구에 `try/except` 예외처리를 추가하여 엔드포인트에 접근할 수 없을 때 정적 `learn.microsoft.com` URL을 반환하도록 하세요.

---

## 도움 받기

위의 수정 방법을 시도해도 문제가 해결되지 않으면:

1. **서버 로그 확인** - 대부분 오류는 터미널에 Python 스택 트레이스가 출력됩니다. 전체 추적 정보를 읽어보세요.
2. **오류 메시지 검색** - 오류 텍스트를 복사하여 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)에서 검색하세요.
3. **이슈 열기** - [워크숍 저장소](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)에 이슈를 등록하세요:
   - 오류 메시지 또는 스크린샷
   - 패키지 버전 (`pip list | Select-String "agent-framework"`)
   - Python 버전 (`python --version`)
   - 문제 발생 상황 (로컬 또는 배포 후)

---

### 점검 사항

- [ ] `.env` 구성 문제를 확인하고 수정하는 방법을 알고 있다
- [ ] 패키지 버전이 요구 매트릭스와 일치하는지 확인할 수 있다
- [ ] 배포 실패 시 컨테이너 로그를 확인할 수 있다
- [ ] Azure Portal에서 RBAC 역할을 확인할 수 있다

---

**이전:** [07 - 플레이그라운드에서 검증](07-verify-in-playground.md) · **다음:** [09 - 요약 →](09-summary.md) · **홈:** [랩 02 README](../README.md) · [워크숍 홈](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->