# 모듈 7 - 요약 및 다음 단계

⏱️ 약 5분

**축하합니다!** Microsoft Foundry와 Foundry Toolkit for VS Code를 사용하여 호스팅된 AI 에이전트를 구축, 테스트하고 (경로 A인 경우) 배포했습니다.

---

## 당신이 만든 것

**"임원에게 설명하듯"** 하는 에이전트로서:
- 기술적 사고 보고서나 운영 업데이트를 HTTP (`POST /responses`)를 통해 수신
- 이를 평이한 언어의 임원 요약으로 번역
- 구조화된 출력 형식(무슨 일이 있었는지 / 비즈니스 영향 / 다음 단계)을 따름
- 주제와 관련 없는 요청 및 프롬프트 주입 시도를 거부
- Microsoft Foundry Agent Service에서 컨테이너화된 호스팅 에이전트로 실행

---

## 배운 주요 개념

| 개념 | 연습 내용 |
|---------|-------------------|
| **에이전트 프레임워크 아키텍처** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` 파이프라인 |
| **호스팅된 에이전트 수명 주기** | 스캐폴드 → 구성 → 로컬 테스트 → 배포 → 클라우드에서 검증 |
| **시스템 프롬프트 엔지니어링** | 역할, 대상, 출력 형식, 규칙, 안전 제약 및 예시 |
| **로컬과 호스팅의 차이** | 신원(개인 자격 증명 vs. 관리 ID), 엔드포인트, 네트워크 경로 |
| **안전 경계** | 프롬프트 주입 방어, 역할 준수, 예외 상황 우아한 처리 |
| **Foundry Toolkit 워크플로우** | 프로젝트 생성, 모델 배포, 에이전트 스캐폴딩, Agent Inspector, 원클릭 배포 |

---

## 완료한 작업

### 경로 A (Foundry 구독)

- [x] Foundry Toolkit 설정 및 배포된 모델로 Foundry 프로젝트 생성
- [x] 자동 생성된 프로젝트 구조로 호스팅 에이전트 스캐폴딩
- [x] 안전 규칙이 포함된 구조화된 에이전트 지침 작성
- [x] 3개의 기능 시나리오로 로컬 테스트 (Agent Inspector)
- [x] Foundry Agent Service에 배포 (컨테이너화)
- [x] 클라우드 플레이그라운드에서 4가지 예외/안전 테스트로 검증

### 경로 B (Foundry 로컬)

- [x] 로컬 모델 엔드포인트로 Foundry Toolkit 설정
- [x] 호스팅 에이전트 프로젝트 스캐폴딩
- [x] 안전 규칙이 포함된 구조화된 에이전트 지침 작성
- [x] 3개의 기능 시나리오로 로컬 테스트
- [x] 클라우드 자원 없이 에이전트 동작 검증

---

## 다음 단계

### 학습 계속하기

| 자료 | 설명 |
|----------|-------------|
| **[Lab 02 - 다중 에이전트 오케스트레이션](../../lab02-multi-agent/docs/README.md)** | 오케스트레이션 패턴으로 4에이전트 워크플로우 만들기 (이력서 → 직무 적합 평가기) |
| **[에이전트에 도구 추가하기](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Tool Catalog를 통해 API, 데이터베이스 또는 맞춤 함수 연결하기 |
| **[지식 추가 (RAG)](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 문서, 벡터 저장소, Bing 검색으로 에이전트 근거 마련하기 |
| **[Microsoft Foundry 문서](https://learn.microsoft.com/azure/foundry/)** | 전체 플랫폼 참조 |
| **[Agent Framework SDK 참조](https://learn.microsoft.com/agent-framework/)** | `agent-framework` 패키지용 API 문서 |
| **[Foundry Toolkit - 최신 정보](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 확장 릴리스 노트 및 변경 내역 |

### 에이전트 확장 아이디어

- **날짜 도구 추가** - 요약에 “오늘 날짜 기준” 문맥 포함시키기
- **사고 데이터베이스 연결** - 도구 함수를 통해 실제 사고 세부 정보 가져오기
- **Bing 근거 도구 추가** - 최근 뉴스를 조회해 추가 문맥 제공하기
- **다른 모델 시도** - `gpt-4.1`과 `gpt-4.1-mini` 출력 품질 비교
- **Foundry 평가 기능 사용** - 대규모로 에이전트 품질 측정하기

### 경로 B 사용자: 클라우드 배포로 업그레이드

클라우드에 배포할 준비가 되면:
1. Azure 구독 받기 ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [모듈 01, 설정](01-setup.md#step-2-set-up-based-on-your-access) 완료 (프로젝트 생성, 모델 배포, RBAC 할당)
3. Foundry 프로젝트 엔드포인트와 모델 배포 이름으로 `.env` 업데이트
4. [모듈 05 - Foundry에 배포](05-deploy-to-foundry.md)에서 계속 진행

---

## 리소스 정리 (선택 사항)

이 워크숍 동안 생성한 Azure 리소스를 제거하려면:

### 옵션 1: 리소스 그룹 삭제 (모두 삭제)

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### 옵션 2: 호스팅된 에이전트만 삭제

1. [ai.azure.com](https://ai.azure.com) → 프로젝트 → <strong>빌드</strong> → <strong>에이전트</strong> 열기
2. 에이전트 클릭 → <strong>삭제</strong> 클릭

### 옵션 3: 모델 배포 삭제

1. Foundry 사이드바에서 프로젝트 확장 → <strong>모델</strong> 선택
2. 모델 배포 우클릭 → <strong>삭제</strong> 선택

> **비용 안내:** 호스팅된 에이전트는 실행 중일 때만 비용이 발생합니다. 중지하거나 삭제하면 비용이 계속 발생하지 않습니다. 모델 배포는 예약 용량에 대해 소액 요금이 발생할 수 있으니 사용이 끝났으면 삭제하세요.

---

**이전:** [06 - 플레이그라운드에서 검증](06-verify-in-playground.md) · **다음:** [08 - 문제 해결 (참고) →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->