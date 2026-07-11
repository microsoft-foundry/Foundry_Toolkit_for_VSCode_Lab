# 모듈 8 - 문제 해결

이 모듈은 일반적인 문제에 대한 참조 가이드입니다. 즐겨찾기에 추가하고 문제가 발생할 때 돌아오세요.

---

## 1. 권한 오류

### 1.1 `agents/write` 권한 거부

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**근본 원인:** <strong>프로젝트</strong> 수준에서 `Azure AI User` 역할이 누락되었습니다. 이것은 가장 흔한 워크숍 오류입니다.

**해결 방법:**
1. [portal.azure.com](https://portal.azure.com) 열기.
2. Foundry <strong>프로젝트</strong> 이름 검색 → 유형이 <strong>"Microsoft Foundry project"</strong>인 결과 클릭 (부모 계정 아님).
3. **액세스 제어(IAM)** → **+ 추가** → **역할 할당 추가**.
4. 역할: **Azure AI User** → 다음.
5. 구성원: 본인 선택 → 검토 + 할당 → 검토 + 할당.
6. **1~2분 대기** → 재시도.

> **Owner/Contributor가 충분하지 않은 이유:** 이 역할들은 <em>관리</em> 작업만 부여합니다. 에이전트 작업은 `agents/write` <em>데이터 작업</em>이 필요하며, 이는 `Azure AI User`, `Azure AI Developer`, 또는 `Azure AI Owner`에만 있습니다. 자세한 내용은 [Foundry RBAC 문서](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)를 참조하세요.

### 1.2 프로비저닝 중 `AuthorizationFailed`

**해결 방법:** 관리자에게 리소스 그룹에 <strong>Contributor</strong>를 할당하도록 요청하거나 프로젝트를 대신 생성하고 본인에게 <strong>Azure AI User</strong>를 부여하도록 하세요.

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# "등록됨"까지 기다리세요
```

---

## 2. 도커 오류

> Docker는 <strong>선택 사항</strong>입니다. 이 문제들은 Docker Desktop이 설치되고 확장 기능이 로컬 빌드를 시도할 때만 적용됩니다.

### 2.1 Docker 데몬이 실행 중이 아님

**해결 방법:** Docker Desktop 시작 → "실행 중" 상태 대기 → `docker info`로 확인 → 재시도.

### 2.2 종속성 오류로 빌드 실패

**해결 방법:** `requirements.txt` 철자 확인, 먼저 로컬에서 테스트: `pip install -r requirements.txt`.

### 2.3 플랫폼 불일치 (Apple Silicon)

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 인증 오류

### 3.1 `DefaultAzureCredential` 실패

**해결 방법 (순서대로 시도):**
1. `az login` (재인증)
2. `az account set --subscription "<id>"` (올바른 구독 설정)
3. VS Code → 계정 → 로그아웃 → 다시 로그인
4. 확인: `az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 로컬에서는 토큰 작동, 호스팅에서는 작동하지 않음

**예상:** 호스팅된 에이전트는 사용자 자격 증명이 아닌 시스템 관리 ID를 사용합니다. 호스팅 에이전트가 인증 오류가 발생하면:
- `agent.yaml` 내 `AZURE_AI_PROJECT_ENDPOINT`가 올바른지 확인
- 프로젝트의 관리 ID가 모델 액세스 권한을 갖고 있는지 확인

---

## 4. 모델 오류

### 4.1 모델 배포를 찾을 수 없음

**해결 방법:** 이름은 <strong>대소문자 구분</strong>입니다. `.env` → `AZURE_AI_MODEL_DEPLOYMENT_NAME`과 Foundry 사이드바 → 모델에서 정확한 이름 비교.

### 4.2 예상치 못한 모델 출력

**해결 방법:** `main.py`의 `AGENT_INSTRUCTIONS` 검토 (잘리지 않았나요?). 다른 모델 시도 (`gpt-4.1` vs `gpt-4.1-mini`).

---

## 5. 배포 오류

### 5.1 ACR pull 권한 없음

**해결 방법:** Azure 포털 → 컨테이너 레지스트리 → 액세스 제어 (IAM) → Foundry 프로젝트 관리 ID에 **AcrPull** 역할 추가.

### 5.2 에이전트 시작 실패 ("대기 중" 또는 "실패" 상태 유지)

사이드바의 컨테이너 로그 확인. 일반 원인:

| 로그 메시지 | 해결 방법 |
|-------------|-----|
| `ModuleNotFoundError` | 누락된 패키지를 `requirements.txt`에 추가 후 재배포 |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | `agent.yaml`의 `environment_variables`에 환경 변수 추가 |
| `Address already in use` | 포트 8088을 바인드하는 프로세스가 하나만 있도록 확인 |

### 5.3 배포 시간 초과

**해결 방법:** 인터넷 연결 점검. 첫 배포는 >100MB입니다. 프록시 뒤에 있나요? Docker Desktop 프록시 설정 구성하세요.

---

## 6. 경로 B - Foundry Local

### 6.1 Foundry Local이 시작되지 않음

| 문제 | 해결 방법 |
|-------|-----|
| `foundry: command not found` | 재설치: `winget install Microsoft.FoundryLocal` |
| 리소스 부족 | Foundry Local은 약 4GB RAM이 필요합니다. 다른 앱 종료하세요. |
| 모델 다운로드 실패 | 디스크 공간 확인 (모델 크기 2–8 GB). 재시도: `foundry local models pull <name>` |

### 6.2 Foundry Local 모델 오류

| 문제 | 해결 방법 |
|-------|-----|
| 응답 지연 | 정상 - 로컬 모델은 GPU가 없으면 CPU에서 실행됩니다. 기다려 주세요. |
| 품질 저하 출력 | 하드웨어가 허용한다면 더 큰 모델을 사용해 보세요. `phi-4-mini`가 균형 잡힌 선택입니다. |
| 연결 거부 | Foundry Local이 실행 중인지 확인: `foundry local status`. 필요 시 재시작. |

---

## 7. 빠른 참조: RBAC 역할

| 역할 | 범위 | 부여 권한 |
|------|-------|--------|
| **Azure AI User** | 프로젝트 | 데이터 작업: `agents/write`, `agents/read` |
| **Azure AI Developer** | 프로젝트/계정 | 데이터 작업 + 프로젝트 생성 |
| **Azure AI Owner** | 계정 | 전체 액세스 + 역할 관리 |
| **Contributor** | 구독/RG | 관리 작업만 (**데이터 작업 없음**) |
| **Owner** | 구독/RG | 관리 + 역할 할당 (**데이터 작업 없음**) |

---

## 8. 워크숍 완료 체크리스트

| 번호 | 항목 | 모듈 |
|---|------|--------|
| 1 | 필수 조건 설치 및 확인 | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit 확장 설치, 프로젝트 연결 (또는 경로 B 구성) | [01](01-setup.md) |
| 3 | 호스팅된 에이전트 스캐폴딩 | [02](02-create-hosted-agent.md) |
| 4 | `.env` 구성, 지침 작성, 종속성 설치 | [03](03-configure-and-code.md) |
| 5 | 로컬 에이전트 테스트 - 3가지 기능 시나리오 통과 | [04](04-test-locally.md) |
| 6 | Foundry에 배포 (경로 A만) | [05](05-deploy-to-foundry.md) |
| 7 | 예외/안전성 테스트 클라우드에서 통과 (경로 A만) | [06](06-verify-in-playground.md) |
| 8 | 요약 검토 및 다음 단계 식별 | [07](07-summary.md) |

---

**이전:** [07 - 요약](07-summary.md) · **홈:** [워크숍 README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->