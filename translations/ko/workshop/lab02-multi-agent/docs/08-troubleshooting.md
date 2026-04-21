# Module 8 - 문제 해결 (멀티 에이전트)

이 모듈은 멀티 에이전트 워크플로우에서 발생하는 일반적인 오류, 해결 방법 및 디버깅 전략에 대해 다룹니다. Foundry 배포 문제에 대해서는 [Lab 01 문제 해결 가이드](../../lab01-single-agent/docs/08-troubleshooting.md)도 참고하세요.

---

## 빠른 참고: 오류 → 해결책

| 오류 / 증상 | 가능한 원인 | 해결책 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env` 파일 없음 또는 값 미설정 | `PROJECT_ENDPOINT=<your-endpoint>` 및 `MODEL_DEPLOYMENT_NAME=<your-model>`가 포함된 `.env` 생성 |
| `ModuleNotFoundError: No module named 'agent_framework'` | 가상 환경 미활성화 또는 의존성 미설치 | `.\.venv\Scripts\Activate.ps1` 실행 후 `pip install -r requirements.txt` 실행 |
| `ModuleNotFoundError: No module named 'mcp'` | MCP 패키지 미설치 (requirements 누락) | `pip install mcp` 실행 또는 `requirements.txt`에 포함 여부 확인 |
| 에이전트가 시작되나 빈 응답 반환 | `output_executors` 불일치 또는 엣지 누락 | `output_executors=[gap_analyzer]` 및 `create_workflow()` 내 모든 엣지 존재 확인 |
| 격차 카드가 1개만 존재 (나머지 없음) | GapAnalyzer 지침 불완전 | `GAP_ANALYZER_INSTRUCTIONS`에 `CRITICAL:` 문단 추가 - [Module 3](03-configure-agents.md) 참고 |
| 적합도 점수 0 또는 없음 | MatchingAgent에 상류 데이터 미전달 | `add_edge(resume_parser, matching_agent)` 및 `add_edge(jd_agent, matching_agent)` 모두 존재 확인 |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCP 서버가 도구 호출 거부 | 인터넷 연결 확인. 브라우저에서 `https://learn.microsoft.com/api/mcp` 열기. 재시도 |
| 출력에 Microsoft Learn URL 없음 | MCP 도구 미등록 또는 엔드포인트 오류 | GapAnalyzer의 `tools=[search_microsoft_learn_for_plan]` 및 `MICROSOFT_LEARN_MCP_ENDPOINT` 올바른지 확인 |
| `Address already in use: port 8088` | 포트 8088을 다른 프로세스가 사용 중 | Windows: `netstat -ano \| findstr :8088` 실행, macOS/Linux: `lsof -i :8088` 실행 후 충돌 프로세스 종료 |
| `Address already in use: port 5679` | Debugpy 포트 충돌 | 다른 디버그 세션 종료. `netstat -ano \| findstr :5679` 실행해 해당 프로세스 종료 |
| Agent Inspector가 열리지 않음 | 서버 미완료 시작 또는 포트 충돌 | "Server running" 로그 대기. 포트 5679가 사용 중인지 확인 |
| `azure.identity.CredentialUnavailableError` | Azure CLI 미로그인 상태 | `az login` 실행 후 서버 재시작 |
| `azure.core.exceptions.ResourceNotFoundError` | 모델 배포 존재하지 않음 | `MODEL_DEPLOYMENT_NAME`이 Foundry 프로젝트에서 배포된 모델과 일치하는지 확인 |
| 배포 후 컨테이너 상태 "Failed" | 시작 시 컨테이너 충돌 | Foundry 사이드바에서 컨테이너 로그 확인. 주로 환경 변수 누락 또는 import 오류 |
| 배포가 5분 이상 "Pending" 상태 | 컨테이너 시작 지연 또는 리소스 제한 | 멀티 에이전트는 4개 인스턴스 생성하므로 최대 5분 대기. 여전히 대기 시 로그 확인 |
| `ValueError` from `WorkflowBuilder` | 그래프 구성 오류 | `start_executor` 설정, `output_executors`가 리스트이며 순환 엣지 없음 확인 |

---

## 환경 및 구성 문제

### `.env` 값 누락 또는 잘못됨

`.env` 파일은 `PersonalCareerCopilot/` 디렉터리에 있어야 합니다 (`main.py`와 동일 레벨):

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

예상 `.env` 내용:

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **PROJECT_ENDPOINT 찾기:**  
- VS Code의 **Microsoft Foundry** 사이드바 열기 → 프로젝트 우클릭 → **Copy Project Endpoint** 선택  
- 또는 [Azure Portal](https://portal.azure.com) → Foundry 프로젝트 → <strong>개요</strong> → **Project endpoint** 확인

> **MODEL_DEPLOYMENT_NAME 찾기:** Foundry 사이드바에서 프로젝트 확장 → **Models** → 배포된 모델 이름 찾기 (예: `gpt-4.1-mini`).

### 환경 변수 우선순위

`main.py`는 `load_dotenv(override=False)`를 사용하며, 이는 다음을 의미합니다:

| 우선순위 | 출처 | 둘 다 설정된 경우 우선권 |
|----------|--------|------------------------|
| 1 (가장 높음) | 셸 환경 변수 | 예 |
| 2 | `.env` 파일 | 셸 변수 미설정 시만 |

즉, Foundry 런타임 환경 변수(`agent.yaml` 통해 설정)는 호스팅 배포 시 `.env` 값보다 우선합니다.

---

## 버전 호환성

### 패키지 버전 표

멀티 에이전트 워크플로우는 특정 패키지 버전이 필요합니다. 버전 불일치 시 런타임 오류가 발생합니다.

| 패키지 | 필요 버전 | 확인 명령어 |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 최신 프리릴리스 | `pip show agent-dev-cli` |
| Python | 3.10 이상 | `python --version` |

### 흔한 버전 오류

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 수정: rc3로 업그레이드
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` 미설치 또는 Inspector 호환 안됨:**

```powershell
# 수정: --pre 플래그를 사용하여 설치
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 수정: mcp 패키지 업그레이드
pip install mcp --upgrade
```

### 모든 버전 한 번에 확인

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

예상 출력:

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

## MCP 도구 문제

### MCP 도구가 결과를 반환하지 않음

**증상:** 격차 카드에 "No results returned from Microsoft Learn MCP" 또는 "No direct Microsoft Learn results found" 표시.

**가능 원인:**

1. **네트워크 문제** - MCP 엔드포인트(`https://learn.microsoft.com/api/mcp`) 접근 불가.
   ```powershell
   # 연결 상태 테스트
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   이 요청이 `200`을 반환하면 엔드포인트에 연결 가능.

2. **질의가 너무 특정적임** - 기술명이 Microsoft Learn 검색에 너무 전문적임.
   - 매우 특수한 기술의 경우 예상됨. 도구 응답에 대체 URL 포함.

3. **MCP 세션 타임아웃** - Streamable HTTP 연결 시간 초과.
   - 요청 재시도. MCP 세션은 일시적이며 재연결 필요할 수 있음.

### MCP 로그 설명

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| 로그 | 의미 | 조치 |
|-----|---------|--------|
| `GET → 405` | 초기화 중 MCP 클라이언트 프로브 | 정상 - 무시 가능 |
| `POST → 200` | 도구 호출 성공 | 정상 |
| `DELETE → 405` | 정리 중 MCP 클라이언트 프로브 | 정상 - 무시 가능 |
| `POST → 400` | 잘못된 요청 (쿼리 형식 오류) | `search_microsoft_learn_for_plan()` 내 `query` 파라미터 확인 |
| `POST → 429` | 호출 제한 도달 | 대기 후 재시도. `max_results` 줄이기 |
| `POST → 500` | MCP 서버 오류 | 일시적 오류 - 재시도. 계속 문제시 Microsoft Learn MCP API 점검 |
| 연결 시간 초과 | 네트워크 문제 또는 MCP 서버 불가 | 인터넷 상태 확인. `curl https://learn.microsoft.com/api/mcp` 시도 |

---

## 배포 문제

### 배포 후 컨테이너 시작 실패

1. **컨테이너 로그 확인:**
   - **Microsoft Foundry** 사이드바 열기 → **Hosted Agents (Preview)** 확장 → 에이전트 클릭 → 버전 확장 → **Container Details** → **Logs** 확인
   - Python 스택 트레이스나 모듈 누락 오류 확인

2. **주요 컨테이너 시작 실패 원인:**

   | 로그 오류 | 원인 | 해결책 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt`에 패키지 누락 | 패키지 추가 후 재배포 |
   | `RuntimeError: Missing required environment variable` | `agent.yaml`의 환경 변수 미설정 | `agent.yaml` → `environment_variables` 섹션 업데이트 |
   | `azure.identity.CredentialUnavailableError` | 관리 ID 미구성 | Foundry가 자동 설정 - 확장으로 배포하는지 확인 |
   | `OSError: port 8088 already in use` | Dockerfile에 잘못된 포트 노출 또는 포트 충돌 | Dockerfile 내 `EXPOSE 8088` 및 `CMD ["python", "main.py"]` 확인 |
   | 컨테이너 종료 코드 1 | `main()` 내 처리되지 않은 예외 | 먼저 로컬 테스트 ([Module 5](05-test-locally.md))로 오류 잡기 |

3. **수정 후 재배포:**
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → 동일 에이전트 선택 → 새 버전 배포

### 배포 지연 문제

멀티 에이전트 컨테이너는 시작 시 4개 에이전트 인스턴스를 생성하므로 시간이 더 걸립니다. 정상 소요 시간:

| 단계 | 예상 소요 시간 |
|-------|------------------|
| 컨테이너 이미지 빌드 | 1~3분 |
| 이미지 ACR 푸시 | 30~60초 |
| 컨테이너 시작 (단일 에이전트) | 15~30초 |
| 컨테이너 시작 (멀티 에이전트) | 30~120초 |
| "Started" 후 에이전트 사용 가능 | 1~2분 |

> 5분 이상 "Pending" 상태가 지속되면 컨테이너 로그에서 오류 확인.

---

## RBAC 및 권한 문제

### `403 Forbidden` 또는 `AuthorizationFailed`

Foundry 프로젝트에 **[Azure AI User](https://aka.ms/foundry-ext-project-role)** 역할이 필요합니다:

1. [Azure Portal](https://portal.azure.com) → Foundry <strong>프로젝트</strong> 리소스로 이동
2. **액세스 제어 (IAM)** → **역할 할당** 클릭
3. 이름 검색 → <strong>Azure AI User</strong>가 목록에 있는지 확인
4. 누락 시: <strong>추가</strong> → **역할 할당 추가** → **Azure AI User** 검색 → 계정에 할당

자세한 내용은 [Microsoft Foundry용 RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 문서 참조.

### 모델 배포 접근 불가

에이전트가 모델 관련 오류를 반환하는 경우:

1. 모델 배포 확인: Foundry 사이드바 → 프로젝트 확장 → **Models** → `gpt-4.1-mini` (또는 사용 모델)의 상태가 <strong>Succeeded</strong>인지 확인
2. 배포 이름 일치 여부 확인: `.env` (또는 `agent.yaml`)의 `MODEL_DEPLOYMENT_NAME`과 사이드바 실제 배포 이름 비교
3. 배포 기간 만료(무료 티어) 시: [모델 카탈로그](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)에서 재배포 (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)

---

## Agent Inspector 문제

### Inspector는 열리나 "Disconnected" 표시

1. 서버 실행 여부 확인: 터미널에 "Server running on http://localhost:8088" 로그가 있는지 확인
2. 포트 `5679` 확인: Inspector는 debugpy를 통해 포트 5679로 연결합니다.
   ```powershell
   netstat -ano | findstr :5679
   ```
3. 서버를 재시작하고 Inspector를 다시 엽니다.

### Inspector가 부분 응답만 표시

멀티 에이전트 응답은 길고 점진적으로 스트리밍됩니다. 전체 응답이 완료될 때까지 기다리세요 (격차 카드 수와 MCP 도구 호출에 따라 30~60초 소요).

응답이 지속적으로 잘리면:  
- GapAnalyzer 지침에 격차 카드를 결합하지 않도록 하는 `CRITICAL:` 블록 포함 여부 확인  
- 모델 토큰 제한 확인 - `gpt-4.1-mini`는 최대 32K 출력 토큰 지원으로 충분함

---

## 성능 팁

### 느린 응답

멀티 에이전트 워크플로우는 의존성 순차 처리와 MCP 도구 호출로 인해 단일 에이전트보다 느립니다.

| 최적화 | 방법 | 영향 |
|-------------|-----|--------|
| MCP 호출 수 줄이기 | 도구 내 `max_results` 파라미터 낮추기 | HTTP 왕복 횟수 감소 |
| 지침 단순화 | 짧고 집중된 에이전트 프롬프트 | 빠른 LLM 추론 |
| `gpt-4.1-mini` 사용 | `gpt-4.1`보다 개발 시 빠름 | 약 2배 속도 향상 |
| 격차 카드 세부정보 감소 | GapAnalyzer 지침 내 격차 카드 형식 단순화 | 생성 출력 감소 |

### 일반 응답 시간 (로컬)

| 구성 | 예상 시간 |
|--------------|---------------|
| `gpt-4.1-mini`, 격차 카드 3-5개 | 30~60초 |
| `gpt-4.1-mini`, 격차 카드 8개 이상 | 60~120초 |
| `gpt-4.1`, 격차 카드 3-5개 | 60~120초 |
---

## 도움 받기

위의 수정 방법을 시도한 후에도 문제가 계속되면:

1. **서버 로그 확인** - 대부분의 오류는 터미널에 Python 스택 트레이스를 출력합니다. 전체 추적 정보를 읽어보세요.
2. **오류 메시지 검색** - 오류 텍스트를 복사하여 [Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)에서 검색하세요.
3. **이슈 등록** - [워크샵 저장소](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)에서 이슈를 등록할 때 다음을 포함하세요:
   - 오류 메시지 또는 스크린샷
   - 패키지 버전 (`pip list | Select-String "agent-framework"`)
   - Python 버전 (`python --version`)
   - 문제가 로컬에서 발생하는지 배포 후 발생하는지 여부

---

### 체크리스트

- [ ] 빠른 참조표를 사용해 가장 흔한 다중 에이전트 오류를 식별하고 수정할 수 있습니다
- [ ] `.env` 구성 문제를 확인하고 수정하는 방법을 알고 있습니다
- [ ] 패키지 버전이 요구 사항과 일치하는지 확인할 수 있습니다
- [ ] MCP 로그 항목을 이해하고 도구 실패를 진단할 수 있습니다
- [ ] 배포 실패 시 컨테이너 로그를 확인하는 방법을 알고 있습니다
- [ ] Azure 포털에서 RBAC 역할을 확인할 수 있습니다

---

**이전:** [07 - 플레이그라운드에서 검증](07-verify-in-playground.md) · **홈:** [랩 02 README](../README.md) · [워크샵 홈](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 노력하고 있으나, 자동 번역에는 오류나 부정확한 부분이 있을 수 있음을 알려드립니다. 원본 문서의 원어본이 권위 있는 출처로 간주되어야 합니다. 중요한 정보에 대해서는 전문 인력에 의한 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해서는 저희가 책임지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->