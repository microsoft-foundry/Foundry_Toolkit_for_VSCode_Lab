# Module 8 - 문제 해결

이 모듈은 워크숍 중에 자주 발생하는 모든 일반적인 문제에 대한 참조 가이드입니다. 즐겨찾기에 추가하세요 - 문제가 발생할 때마다 다시 돌아오게 될 것입니다.

---

## 1. 권한 오류

### 1.1 `agents/write` 권한 거부

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**근본 원인:** <strong>프로젝트</strong> 수준에 `Azure AI User` 역할이 없습니다. 워크숍에서 가장 흔한 오류입니다.

**수정 - 단계별:**

1. [https://portal.azure.com](https://portal.azure.com)을 엽니다.
2. 상단 검색창에 **Foundry 프로젝트** 이름을 입력합니다 (예: `workshop-agents`).
3. **중요:** 상위 계정/허브 리소스가 아닌 **"Microsoft Foundry project"** 유형이 표시된 결과를 클릭하세요. 이들은 권한 범위(RBAC)가 다른 별도의 리소스입니다.
4. 프로젝트 페이지 왼쪽 탐색에서 **액세스 제어 (IAM)** 를 클릭합니다.
5. **역할 할당** 탭을 클릭하여 이미 역할이 있는지 확인합니다:
   - 이름 또는 이메일을 검색합니다.
   - `Azure AI User`가 이미 나열되어 있다면 → 오류의 원인이 다릅니다 (아래 8단계 확인).
   - 나열되지 않았다면 → 추가를 진행합니다.
6. **+ 추가** → <strong>역할 할당 추가</strong>를 클릭합니다.
7. <strong>역할</strong> 탭에서:
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles)를 검색합니다.
   - 결과에서 선택합니다.
   - <strong>다음</strong>을 클릭합니다.
8. <strong>멤버</strong> 탭에서:
   - <strong>사용자, 그룹 또는 서비스 주체</strong>를 선택합니다.
   - <strong>+ 멤버 선택</strong>을 클릭합니다.
   - 이름 또는 이메일 주소를 검색합니다.
   - 본인을 선택합니다.
   - <strong>선택</strong>을 클릭합니다.
9. **검토 + 할당** → 다시 <strong>검토 + 할당</strong>을 클릭합니다.
10. **1-2분 기다립니다** - RBAC 변경 사항이 전파되기까지 시간이 걸립니다.
11. 실패한 작업을 다시 시도합니다.

> **왜 Owner/Contributor가 충분하지 않은가:** Azure RBAC에는 두 가지 권한 유형이 있습니다 - <em>관리 작업</em>과 *데이터 작업*. Owner 및 Contributor는 관리 작업(리소스 생성, 설정 편집)을 허용하지만, 에이전트 작업은 `agents/write` **데이터 작업** 권한이 필요하며 이는 `Azure AI User`, `Azure AI Developer`, `Azure AI Owner` 역할에만 포함됩니다. 자세한 내용은 [Foundry RBAC 문서](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)를 참조하세요.

### 1.2 리소스 프로비저닝 중 `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**근본 원인:** 이 구독/리소스 그룹에서 Azure 리소스를 생성하거나 수정할 권한이 없습니다.

**수정:**
1. 구독 관리자에게 Foundry 프로젝트가 생성된 리소스 그룹에 대해 **Contributor** 역할을 할당해 달라고 요청하세요.
2. 또는 관리자가 Foundry 프로젝트를 대신 생성하고 프로젝트에 **Azure AI User** 권한을 부여하도록 요청하세요.

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) 관련 `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**근본 원인:** Foundry에 필요한 리소스 공급자가 Azure 구독에 등록되어 있지 않습니다.

**수정:**

1. 터미널을 열고 다음을 실행하세요:
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. 등록이 완료될 때까지 기다리세요(1~5분 소요될 수 있음):
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   예상 출력을 확인하세요: `"Registered"`
3. 작업을 다시 시도하세요.

---

## 2. Docker 오류 (Docker가 설치된 경우에만)

> Docker는 이 워크숍에서 <strong>선택 사항</strong>입니다. 이 오류는 Docker Desktop이 설치되어 있고 Foundry 확장 프로그램이 로컬 컨테이너 빌드를 시도할 때만 발생합니다.

### 2.1 Docker 데몬이 실행 중이지 않음

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**수정 - 단계별:**

1. 시작 메뉴(Windows) 또는 응용 프로그램 폴더(macOS)에서 <strong>Docker Desktop</strong>을 찾아 실행합니다.
2. Docker Desktop 창에 <strong>"Docker Desktop is running"</strong>이 표시될 때까지 기다립니다 - 일반적으로 30~60초 소요됩니다.
3. 시스템 트레이(Windows) 또는 메뉴 막대(macOS)에 있는 Docker 고래 아이콘을 찾으세요. 아이콘 위에 마우스를 올려 상태를 확인합니다.
4. 터미널에서 다음을 확인하세요:
   ```powershell
   docker info
   ```
   Docker 시스템 정보(서버 버전, 저장소 드라이버 등)가 출력되면 Docker가 실행 중인 것입니다.
5. **Windows 전용:** Docker가 여전히 시작되지 않는 경우:
   - Docker Desktop → <strong>설정</strong> (톱니바퀴 아이콘) → <strong>일반</strong>을 엽니다.
   - <strong>WSL 2 기반 엔진 사용</strong>이 체크되어 있는지 확인합니다.
   - <strong>적용 및 다시 시작</strong>을 클릭합니다.
   - WSL 2가 설치되어 있지 않다면, 관리자 권한 PowerShell에서 `wsl --install`을 실행하고 컴퓨터를 재시작하세요.
6. 배포를 다시 시도합니다.

### 2.2 Docker 빌드가 종속성 오류로 실패함

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**수정:**
1. `requirements.txt`를 열어 모든 패키지 이름이 올바르게 철자되었는지 확인하세요.
2. 버전 고정이 올바른지 확인하세요:
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. 먼저 로컬에서 설치를 테스트하세요:
   ```bash
   pip install -r requirements.txt
   ```
4. 개인 패키지 인덱스를 사용하는 경우, Docker가 네트워크에 접근할 수 있는지 확인하세요.

### 2.3 컨테이너 플랫폼 불일치 (Apple Silicon)

Apple Silicon Mac(M1/M2/M3/M4)에서 배포하는 경우 컨테이너는 `linux/amd64`용으로 빌드되어야 합니다. Foundry의 컨테이너 런타임이 AMD64를 사용하기 때문입니다.

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> 대부분 경우 Foundry 확장의 배포 명령이 이 작업을 자동으로 처리합니다. 아키텍처 관련 오류가 발생하면 `--platform` 플래그를 사용해 수동으로 빌드하고 Foundry 팀에 연락하세요.

---

## 3. 인증 오류

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) 토큰 수신 실패

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**근본 원인:** `DefaultAzureCredential` 체인의 인증 소스 중 유효한 토큰이 없습니다.

**수정 - 순서대로 시도하세요:**

1. **Azure CLI 재로그인** (가장 일반적인 해결방법):
   ```bash
   az login
   ```
   브라우저 창이 열립니다. 로그인한 후 VS Code로 돌아갑니다.

2. **올바른 구독 설정:**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   올바른 구독이 아닐 경우:
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code에서 재로그인:**
   - VS Code 왼쪽 하단에 있는 <strong>계정</strong> 아이콘(사람 모양)을 클릭하세요.
   - 계정 이름 클릭 → <strong>로그아웃</strong>.
   - 다시 계정 아이콘 클릭 → **Microsoft에 로그인**.
   - 브라우저 로그인 절차를 완료하세요.

4. **서비스 주체(CI/CD 시나리오만 해당):**
   - `.env`에 다음 환경 변수를 설정하세요:
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - 에이전트 프로세스를 재시작하세요.

5. **토큰 캐시 확인:**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   실패한다면 CLI 토큰이 만료된 것입니다. `az login`을 다시 실행하세요.

### 3.2 토큰은 로컬에서는 작동하지만 호스팅 배포에서는 안됨

**근본 원인:** 호스팅된 에이전트는 개인 자격 증명과 다른 시스템 관리 Id를 사용합니다.

**수정:** 이는 정상적인 동작입니다 - 관리 Id가 배포 중 자동으로 프로비저닝됩니다. 호스팅 에이전트가 여전히 인증 오류가 발생하면:
1. Foundry 프로젝트의 관리 Id가 Azure OpenAI 리소스에 액세스할 수 있는지 확인하세요.
2. `agent.yaml`의 `PROJECT_ENDPOINT`가 올바른지 확인하세요.

---

## 4. 모델 오류

### 4.1 모델 배포를 찾을 수 없음

```
Error: Model deployment not found / The specified deployment does not exist
```

**수정 - 단계별:**

1. `.env` 파일을 열고 `AZURE_AI_MODEL_DEPLOYMENT_NAME` 값을 확인합니다.
2. VS Code에서 **Microsoft Foundry** 사이드바를 엽니다.
3. 프로젝트를 확장한 후 → <strong>Model Deployments</strong>를 엽니다.
4. 거기에 나열된 배포 이름과 `.env` 값을 비교하세요.
5. 이름은 <strong>대소문자 구분</strong>합니다 - `gpt-4o`와 `GPT-4o`는 다릅니다.
6. 이름이 일치하지 않으면, `.env`를 사이드바에 표시된 정확한 이름으로 수정하세요.
7. 호스팅 배포의 경우 `agent.yaml`도 업데이트하세요:
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 모델이 예상치 않은 내용을 반환함

**수정:**
1. `main.py`의 `EXECUTIVE_AGENT_INSTRUCTIONS` 상수를 검토하세요. 잘리거나 손상되지 않았는지 확인합니다.
2. 모델 온도 설정(구성 가능 시)을 확인하세요 - 낮은 값이 더 결정론적(output 예측 가능) 결과를 생성합니다.
3. 배포된 모델을 비교하세요 (예: `gpt-4o` vs `gpt-4o-mini`) - 모델마다 기능이 다릅니다.

---

## 5. 배포 오류

### 5.1 ACR 풀 권한

```
Error: AcrPullUnauthorized
```

**근본 원인:** Foundry 프로젝트의 관리 Id가 Azure Container Registry에서 컨테이너 이미지를 가져올 수 없습니다.

**수정 - 단계별:**

1. [https://portal.azure.com](https://portal.azure.com)을 엽니다.
2. 상단 검색창에 <strong>[Container registries](https://learn.microsoft.com/azure/container-registry/container-registry-intro)</strong>를 검색합니다.
3. Foundry 프로젝트와 연결된 레지스트리를 클릭합니다(보통 같은 리소스 그룹에 있음).
4. 왼쪽 탐색에서 **액세스 제어 (IAM)** 를 클릭합니다.
5. **+ 추가** → **역할 할당 추가** 클릭.
6. <strong>[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)</strong>을 검색 후 선택. <strong>다음</strong>을 클릭.
7. **관리 Id** 선택 → **+ 멤버 선택** 클릭.
8. Foundry 프로젝트의 관리 Id를 찾아 선택.
9. <strong>선택</strong> → **검토 + 할당** → **검토 + 할당** 클릭.

> 이 역할 할당은 보통 Foundry 확장 프로그램에 의해 자동으로 설정됩니다. 오류가 발생하면 자동 설정이 실패했을 수 있습니다. 다시 배포하면 확장이 설정을 재시도할 수 있습니다.

### 5.2 배포 후 에이전트가 시작하지 않음

**증상:** 컨테이너 상태가 5분 이상 "Pending" 상태이거나 "Failed"로 표시됨.

**수정 - 단계별:**

1. VS Code의 **Microsoft Foundry** 사이드바를 엽니다.
2. 호스팅된 에이전트를 선택 → 버전을 선택하세요.
3. 상세 패널에서 **Container Details** → <strong>로그</strong> 섹션 또는 링크를 찾아봅니다.
4. 컨테이너 시작 로그를 읽으세요. 일반 원인:

| 로그 메시지 | 원인 | 수정 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 누락된 종속성 | `requirements.txt`에 추가 후 재배포 |
| `KeyError: 'PROJECT_ENDPOINT'` | 누락된 환경 변수 | `agent.yaml`의 `env:` 아래에 환경 변수 추가 |
| `OSError: [Errno 98] Address already in use` | 포트 충돌 | `agent.yaml`에 `port: 8088` 설정 및 한 프로세스만 바인드 확인 |
| `ConnectionRefusedError` | 에이전트가 수신 대기 시작 안 함 | `main.py`의 `from_agent_framework()` 호출이 시작 시 실행되는지 확인 |

5. 문제를 수정한 후 [Module 6](06-deploy-to-foundry.md)에서 다시 배포하세요.

### 5.3 배포 시간이 초과됨

**수정:**
1. 인터넷 연결 상태를 확인하세요 - Docker 푸시는 크기가 클 수 있습니다 (>100MB 첫 배포 시).
2. 회사 프록시 뒤에 있다면 Docker Desktop 프록시 설정을 확인하세요: **Docker Desktop** → <strong>설정</strong> → <strong>리소스</strong> → <strong>프록시</strong>.
3. 다시 시도하세요 - 네트워크 일시적 문제일 수 있습니다.

---

## 6. 빠른 참조: RBAC 역할

| 역할 | 일반 범위 | 권한 내용 |
|------|---------------|----------------|
| **Azure AI User** | 프로젝트 | 데이터 작업: 에이전트 빌드, 배포, 호출 (`agents/write`, `agents/read`) |
| **Azure AI Developer** | 프로젝트 또는 계정 | 데이터 작업 + 프로젝트 생성 |
| **Azure AI Owner** | 계정 | 전체 액세스 + 역할 할당 관리 |
| **Azure AI Project Manager** | 프로젝트 | 데이터 작업 + 다른 사람에게 Azure AI User 할당 가능 |
| **Contributor** | 구독/리소스 그룹 | 관리 작업 (리소스 생성/삭제). **데이터 작업 미포함** |
| **Owner** | 구독/리소스 그룹 | 관리 작업 + 역할 할당. **데이터 작업 미포함** |
| **Reader** | 어느 곳이나 | 읽기 전용 관리 액세스 |

> **핵심 요점:** `Owner`와 `Contributor` 역할에는 데이터 작업이 포함되지 않습니다. 에이전트 작업을 위해서는 항상 `Azure AI *` 역할이 필요하며, 이 워크숍의 최소 역할은 <strong>프로젝트 범위의 Azure AI User</strong>입니다.

---

## 7. 워크숍 완료 체크리스트

모든 작업을 완료했다는 최종 확인용으로 사용하세요:

| # | 항목 | 모듈 | 완료? |
|---|------|--------|---|
| 1 | 모든 사전 요구사항 설치 및 확인 | [00](00-prerequisites.md) | |
| 2 | Foundry Toolkit 및 Foundry 확장 프로그램 설치 | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry 프로젝트 생성 (또는 기존 프로젝트 선택) | [02](02-create-foundry-project.md) | |
| 4 | 모델 배포됨(e.g., gpt-4o) | [02](02-create-foundry-project.md) | |
| 5 | 프로젝트 범위에서 Azure AI 사용자 역할 할당됨 | [02](02-create-foundry-project.md) | |
| 6 | 호스티드 에이전트 프로젝트 골격 생성됨(agent/) | [03](03-create-hosted-agent.md) | |
| 7 | `.env`에 PROJECT_ENDPOINT 및 MODEL_DEPLOYMENT_NAME 구성됨 | [04](04-configure-and-code.md) | |
| 8 | main.py에서 에이전트 명령어 맞춤화됨 | [04](04-configure-and-code.md) | |
| 9 | 가상 환경 생성 및 종속성 설치됨 | [04](04-configure-and-code.md) | |
| 10 | F5 또는 터미널로 로컬에서 에이전트 테스트됨(4가지 스모크 테스트 통과) | [05](05-test-locally.md) | |
| 11 | Foundry Agent Service에 배포됨 | [06](06-deploy-to-foundry.md) | |
| 12 | 컨테이너 상태가 "시작됨" 또는 "실행 중"으로 표시됨 | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground에서 검증됨(4가지 스모크 테스트 통과) | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground에서 검증됨(4가지 스모크 테스트 통과) | [07](07-verify-in-playground.md) | |

> **축하합니다!** 모든 항목을 체크하셨다면 워크숍을 모두 완료하신 것입니다. 호스티드 에이전트를 처음부터 구축하고, 로컬에서 테스트하며, Microsoft Foundry에 배포하고, 프로덕션 환경에서 검증하셨습니다.

---

**이전:** [07 - Verify in Playground](07-verify-in-playground.md) · **홈:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 노력하고 있으나, 자동 번역에는 오류나 부정확함이 포함될 수 있음을 유의하시기 바랍니다. 원본 문서의 원어 버전이 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역 사용으로 인한 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->