# Lab 02 - 다중 에이전트 워크플로우: 이력서 → 직무 적합도 평가기

## 전체 학습 경로

이 문서는 <strong>WorkflowBuilder</strong>를 통해 조율되는 네 개의 전문화된 에이전트를 사용하여 이력서와 직무 적합도를 평가하는 <strong>다중 에이전트 워크플로우</strong>를 구축, 테스트 및 배포하는 과정을 안내합니다.

> **필수 조건:** Lab 02를 시작하기 전에 [Lab 01 - 단일 에이전트](../../lab01-single-agent/README.md)를 완료하세요.

---

## 모듈

| # | 모듈 | 수행할 작업 |
|---|--------|---------------|
| 0 | [필수 조건](00-prerequisites.md) | Lab 01 완료 확인, 다중 에이전트 개념 이해 |
| 1 | [다중 에이전트 아키텍처 이해](01-understand-multi-agent.md) | WorkflowBuilder, 에이전트 역할, 오케스트레이션 그래프 학습 |
| 2 | [다중 에이전트 프로젝트 스캐폴딩](02-scaffold-multi-agent.md) | Foundry 확장 도구를 사용하여 다중 에이전트 워크플로우 스캐폴딩 |
| 3 | [에이전트 및 환경 구성](03-configure-agents.md) | 4개 에이전트에 대한 지침 작성, MCP 도구 구성, 환경 변수 설정 |
| 4 | [오케스트레이션 패턴](04-orchestration-patterns.md) | 병렬 팬아웃, 순차 집계, 대체 패턴 탐색 |
| 5 | [로컬 테스트](05-test-locally.md) | Agent Inspector로 F5 디버그, 이력서 + 직무 설명으로 스모크 테스트 실행 |
| 6 | [Foundry에 배포](06-deploy-to-foundry.md) | 컨테이너 빌드, ACR에 푸시, 호스팅 에이전트 등록 |
| 7 | [Playground에서 검증](07-verify-in-playground.md) | VS Code 및 Foundry 포털 플레이그라운드에서 배포된 에이전트 테스트 |
| 8 | [문제 해결](08-troubleshooting.md) | 일반적인 다중 에이전트 문제 수정 (MCP 오류, 출력 잘림, 패키지 버전) |

---

## 예상 시간

| 경험 수준 | 소요 시간 |
|-----------------|------|
| 최근에 Lab 01 완료 | 45-60분 |
| Azure AI 경험 있음 | 60-90분 |
| 다중 에이전트 첫 사용 | 90-120분 |

---

## 아키텍처 개요

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**뒤로 가기:** [Lab 02 README](../README.md) · [워크숍 홈](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있지만, 자동 번역에는 오류나 부정확성이 있을 수 있음을 유의하시기 바랍니다. 원문은 해당 원어로 작성된 문서가 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역의 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->