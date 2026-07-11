# 모듈 1 - 아키텍처 이해하기

⏱️ ~5분

코드를 작성하기 전에, 여러분이 만드는 것과 그것이 어떻게 작동하는지에 대한 간략한 개요입니다.

---

## 여러분이 만드는 것

여러분은 <strong>이력서</strong>와 <strong>직무 설명서</strong>를 붙여넣습니다. 워크플로우는 다음을 반환합니다:

- 적합도 점수 (0~100, 세부 내역 포함)
- 기술 및 자격증 격차 목록
- 각 격차에 대해 Microsoft Learn 링크가 포함된 개인 맞춤 학습 로드맵

---

## 네 가지 에이전트

한 명의 에이전트가 한 번에 파싱, 점수 산출, 계획을 모두 하려 하면 급하게 처리하고 얕은 결과를 낼 가능성이 큽니다. 작업을 네 개의 전문 에이전트로 나누면 더 나은 결과를 얻습니다:

| 에이전트 | 역할 |
|-------|-------------|
| **ResumeParser** | 이력서를 파싱; 하위 에이전트용으로 직무 설명서를 그대로 `[JOB DESCRIPTION PASS-THROUGH]`에 복사 |
| **JobDescriptionAgent** | 직무 설명서 요구사항을 추출; `[PARSED RESUME]`를 `[PARSED RESUME PASS-THROUGH]`로 전달 |
| **MatchingAgent** | 두 섹션을 비교; 0~100 적합도 점수와 격차 목록 생성 |
| **GapAnalyzer** | 학습 로드맵 작성; 각 격차에 대해 Microsoft Learn 검색 |

---

## 오케스트레이션 그래프

워크플로우는 <strong>순차 파이프라인</strong>입니다 - 각 에이전트는 출력을 다음 에이전트에 넘깁니다:

```mermaid
flowchart LR
    A["사용자 입력"] --> B["이력서 파서"]
    B -- "파싱된 이력서 + 직무 설명 전달" --> C["직무 설명 에이전트"]
    C -- "직무 요구사항 + 이력서 전달" --> D["매칭 에이전트"]
    D -- "적합도 보고서 + 갭" --> E["갭 분석기 + MCP"]
    E --> F["최종 결과"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. <strong>ResumeParser</strong>가 사용자 입력을 받아 이력서를 파싱하고 JD를 `[JOB DESCRIPTION PASS-THROUGH]`에 복사합니다.
2. <strong>JD Agent</strong>가 구조화된 요구사항을 추출하고 `[PARSED RESUME PASS-THROUGH]`를 전달합니다.
3. <strong>MatchingAgent</strong>는 두 섹션을 비교하여 적합도 점수와 격차 목록을 만듭니다.
4. <strong>GapAnalyzer</strong>가 로드맵을 작성하고 각 격차에 대해 Microsoft Learn MCP 도구를 호출합니다.

---

## 이것이 코드에 어떻게 매핑되는지

`main.py`에서 `WorkflowBuilder`로 이 그래프를 설명합니다:

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # 사용자 입력을 받는 첫 번째 에이전트
        output_executors=[gap_executor],      # 마지막 에이전트 - 이 에이전트의 출력이 응답입니다
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JD 에이전트
    .add_edge(jd_executor, matching_executor)     # JD 에이전트 → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

각 `Agent`는 `AgentExecutor`로 래핑됩니다. `add_edge()` 호출은 엄격히 순차적인 파이프라인을 정의하며, 각 에이전트는 직접 이전 에이전트의 출력만 받습니다.

> `context_mode="last_agent"`는 각 실행기가 직접 이전 에이전트의 출력만 보도록 합니다. ResumeParser와 JD Agent는 데이터에 라벨 섹션을 달아 앞으로 전달하여 하위 에이전트가 정확히 필요한 것을 받도록 합니다.

---

## MCP 도구

GapAnalyzer는 하나의 도구를 갖고 있습니다: `search_microsoft_learn_for_plan`. 이 도구는 `https://learn.microsoft.com/api/mcp`에 연결되어 각 기술 격차에 대한 실제 Microsoft Learn 링크를 반환합니다.

도구가 실행될 때 아래 로그를 보게 되며, 이는 모두 정상입니다:

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

`POST`에서 오류가 반환되면 걱정하세요.

---

**이전:** [00 - 필수 조건](00-prerequisites.md) · **다음:** [02 - 프로젝트 스캐폴딩 →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 기하기 위해 노력하고 있으나, 자동 번역은 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원본 문서의 원어본이 권위 있는 자료로 간주되어야 합니다. 중요한 정보의 경우, 전문가의 인간 번역을 권장합니다. 이 번역 사용으로 인해 발생하는 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->