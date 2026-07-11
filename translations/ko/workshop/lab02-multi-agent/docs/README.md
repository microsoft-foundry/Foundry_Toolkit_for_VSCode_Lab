# 실습 02 - 멀티 에이전트 워크플로우: 이력서 → 직무 적합성 평가기

## 전체 학습 경로

본 문서는 네 명의 전문화된 에이전트를 <strong>WorkflowBuilder</strong>를 통해 조율하여 이력서와 직무 적합성을 평가하는 <strong>멀티 에이전트 워크플로우</strong>를 구축, 테스트, 배포하는 과정을 안내합니다.

> **전제 조건:** 실습 02를 시작하기 전에 [실습 01 - 싱글 에이전트](../../lab01-single-agent/README.md)를 완료하세요.

---

## 모듈

| # | 모듈 | 수행할 작업 |
|---|--------|---------------|
| 0 | [소개](00-prerequisites.md) | 구축할 내용, 실습 01 확인, 실습 02와 실습 01 비교 |
| 1 | [멀티 에이전트 아키텍처 이해](01-understand-multi-agent.md) | WorkflowBuilder, 에이전트 역할, 오케스트레이션 그래프 학습 |
| 2 | [멀티 에이전트 프로젝트 스캐폴딩](02-scaffold-multi-agent.md) | Foundry 확장 마법사를 사용하여 기본 프로젝트 스캐폴딩 |
| 3 | [에이전트 및 환경 구성](03-configure-agents.md) | 4개 에이전트 지침 작성, MCP 도구 구성, 환경 변수 설정 |
| 4 | [오케스트레이션 패턴](04-orchestration-patterns.md) | 순차 체인, 콘텐츠 전달, WorkflowBuilder OR-세멘틱스 |
| 5 | [로컬 테스트](05-test-locally.md) | 에이전트 인스펙터로 F5 디버깅, 이력서 + 직무 설명서 스모크 테스트 실행 |
| 6 | [Foundry에 배포](06-deploy-to-foundry.md) | 컨테이너 빌드, ACR 푸시, 호스팅 에이전트 등록 |
| 7 | [플레이그라운드에서 검증](07-verify-in-playground.md) | VS Code 및 Foundry 포털 플레이그라운드에서 배포된 에이전트 테스트 |
| 8 | [문제 해결](08-troubleshooting.md) | 일반적인 멀티 에이전트 문제 해결 (MCP 오류, 출력 누락, 패키지 버전) |
| 9 | [요약 및 다음 단계](09-summary.md) | 구축 내용, 핵심 개념 학습, 정리 및 다음 단계 안내 |

---

**뒤로가기:** [실습 02 README](../README.md) · [워크숍 홈](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->