# 모듈 9 - 요약 및 다음 단계

⏱️ 약 5분

**축하합니다!** Microsoft Foundry와 VS Code용 Foundry Toolkit을 사용하여 다중 에이전트 워크플로를 구축, 테스트하고 (경로 A인 경우) 배포했습니다.

---

## 구축한 내용

**이력서 → 직무 적합도 평가기** - 다중 에이전트 호스팅 워크플로로서:
- HTTP (`POST /responses`)를 통해 이력서 + 직무 설명을 받음
- 네 개의 전문화된 에이전트를 순차 파이프라인으로 실행 - 각 에이전트는 후속 에이전트가 필요한 데이터를 전달함
- 적합 점수(0–100 및 세부 내역), 기술 및 자격증 격차 목록, 각 격차별 실제 Microsoft Learn 링크가 포함된 개인 맞춤 학습 로드맵을 반환
- Microsoft Learn MCP 서버(`https://learn.microsoft.com/api/mcp`)를 호출하여 각 식별된 기술 격차에 대한 공식 학습 자료를 가져옴
- Microsoft Foundry Agent Service 내 단일 컨테이너 환경 호스팅 에이전트로 실행됨

---

## 배운 주요 개념

| 개념 | 연습한 내용 |
|---------|-------------------|
| **다중 에이전트 오케스트레이션** | `WorkflowBuilder` 순차 파이프라인과 `add_edge()` 사용 |
| **에이전트 전문화** | 네 개의 집중 에이전트가 한 명의 범용 에이전트보다 뛰어남 |
| **컨텐츠 라우터 패턴** | ResumeParser가 라우터 역할 겸함 - JD 텍스트를 `[JOB DESCRIPTION PASS-THROUGH]` 섹션에 보존하여 후속 에이전트가 접근 가능하도록 함 (`context_mode="last_agent"`는 `start_executor`만 원시 사용자 메시지를 보기 때문임) |
| **컨텐츠 릴레이 패턴** | JD Agent가 `[PARSED RESUME PASS-THROUGH]`를 전달해 MatchingAgent가 두 프로필을 모두 얻음; 팬인 그래프가 발생시키는 OR-시멘틱의 이중 트리거 방지 |
| **MCP 도구 통합** | `@tool`과 `streamable_http_client`를 이용해 외부 MCP 서버 호출 |
| **호스팅 에이전트 라이프사이클** | 스캐폴드 → 구성 → 로컬 테스트 → 배포 → 클라우드에서 검증 |
| **`context_mode="last_agent"`** | 각 실행기는 직접 전임자의 출력만 봄 |
| **Foundry Toolkit 워크플로** | 스캐폴드 마법사, 에이전트 검사기, 워크플로 시각화, 원클릭 배포 |

---

## 완료한 작업

<details open>
<summary><strong>🅰️ 경로 A - Foundry 구독자</strong></summary>

- [x] Lab 01 설정 검증: 프로젝트, 모델, RBAC가 여전히 활성화됨
- [x] Workflows 템플릿으로 다중 에이전트 프로젝트 스캐폴딩 완료
- [x] 네 개의 에이전트 지시서 작성(ResumeParser, JD Agent, MatchingAgent, GapAnalyzer)
- [x] Microsoft Learn MCP 도구를 `streamable_http_client`와 통합
- [x] `WorkflowBuilder`로 워크플로 그래프 연결(순차 파이프라인과 컨텐츠 릴레이)
- [x] 3가지 스모크 테스트로 로컬 테스트 완료(에이전트 검사기) - 적합 점수, 격차 카드, MCP URL
- [x] Foundry Agent Service에 배포(컨테이너화, 관리 ID)
- [x] 클라우드 플레이그라운드에서 검증 - 로컬 결과와 구조적 일관성 확인

</details>

<details open>
<summary><strong>🅱️ 경로 B - Foundry Local</strong></summary>

- [x] Lab 01 설정 검증: Foundry Local이 로컬 모델로 실행 중
- [x] Workflows 템플릿으로 다중 에이전트 프로젝트 스캐폴딩 완료
- [x] 네 개의 에이전트 지시서 작성 및 워크플로 그래프 연결
- [x] Microsoft Learn MCP 도구 통합 완료
- [x] 3가지 스모크 테스트로 로컬 테스트 완료
- [x] 클라우드 리소스 없이 다중 에이전트 동작 검증 완료

</details>

---

## 다음 단계

### 학습 계속하기

| 리소스 | 설명 |
|----------|-------------|
| **[Agent Framework SDK 참조](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`, `WorkflowBuilder`, `AgentExecutor` API 문서 |
| **[MCP 도구 카탈로그](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | 에이전트를 다른 MCP 서버들(Bing, GitHub, 맞춤형)과 연결 |
| **[지식 추가 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 문서, 벡터 스토어, Bing 검색으로 에이전트 기반 확장 |
| **[Foundry 평가 도구](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 자동 평가자로 대규모 에이전트 품질 측정 |
| **[Microsoft Foundry 문서](https://learn.microsoft.com/azure/foundry/)** | 전체 플랫폼 참조 자료 |
| **[Foundry Toolkit - 신규 기능](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 확장 기능 릴리스 노트 및 변경 로그 |

### 이 워크플로 확장 아이디어

- **다섯 번째 에이전트 추가** - 격차 보고서를 바탕으로 예상 인터뷰 질문을 생성하는 인터뷰 코치
- **Bing 기반 도구 추가** - JD Agent가 유사 직무 공고를 검색해 요구사항 풍부화
- **이력서 데이터베이스 연결** - 맞춤 `@tool`로 데이터베이스에서 후보자 프로필 가져오기
- **다양한 모델 시도** - `gpt-4.1`과 `gpt-4.1-mini` 출력 품질 및 대기 시간 비교
- **Foundry로 평가** - 평가 기능으로 황금 데이터셋과 적합도 보고서 점수 비교

### 경로 B 사용자를 위한: 클라우드 배포로 업그레이드

클라우드에 배포할 준비가 되면:
1. Azure 구독 얻기 ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [Lab 01, 모듈 01](../../lab01-single-agent/docs/01-setup.md) 완료 (프로젝트 생성, 모델 배포, RBAC 할당)
3. `.env` 파일을 Foundry 프로젝트 엔드포인트와 모델 배포 이름으로 업데이트
4. [모듈 06 - Foundry 배포](06-deploy-to-foundry.md)에서 계속 진행

---

## 리소스 정리 (선택 사항)

워크숍 동안 만든 Azure 리소스를 제거하려면:

### 옵션 1: 리소스 그룹 삭제 (모든 항목 제거)

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 옵션 2: 호스팅 에이전트만 삭제

1. [ai.azure.com](https://ai.azure.com) → 프로젝트 → **Build** → **Agents** 열기.
2. **PersonalCareerCopilot** 찾기 → **Delete** 클릭.

### 옵션 3: 모델 배포 삭제

1. Foundry 사이드바에서 프로젝트 확장 → **Models** 선택.
2. 모델 배포 우클릭 → **Delete** 선택.

> **비용 안내:** 호스팅 에이전트는 실행 중일 때만 비용 발생. 에이전트를 중지하거나 삭제하면 지속 요금 없음. 모델 배포는 예약 용량에 대해 소액 요금이 발생할 수 있으니 완료 시 삭제 권장.

---

**이전:** [08 - 문제 해결](08-troubleshooting.md) · **홈:** [Lab 02 README](../README.md) · [워크숍 홈](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->