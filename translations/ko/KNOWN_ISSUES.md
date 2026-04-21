# 알려진 문제

이 문서는 현재 저장소 상태에서 알려진 문제를 추적합니다.

> 최종 업데이트: 2026-04-15. Python 3.13 / Windows 환경 `.venv_ga_test`에서 테스트됨.

---

## 현재 패키지 고정 버전 (세 에이전트 모두)

| 패키지 | 현재 버전 |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(수정됨 — KI-003 참고)* |

---

## KI-001 — GA 1.0.0 업그레이드 차단: `agent-framework-azure-ai` 제거됨

**상태:** 진행 중 | **심각도:** 🔴 높음 | **유형:** 중대한 변경

### 설명

`agent-framework-azure-ai` 패키지(`1.0.0rc3`로 고정)는 GA 릴리스(1.0.0, 2026-04-02 출시)에서 **제거/더 이상 사용하지 않음** 처리되었습니다. 대체 패키지는 다음과 같습니다:

- `agent-framework-foundry==1.0.0` — Foundry 호스팅 에이전트 패턴
- `agent-framework-openai==1.0.0` — OpenAI 기반 에이전트 패턴

세 개의 모든 `main.py` 파일은 `agent_framework.azure`에서 `AzureAIAgentClient`를 임포트하는데,
GA 패키지에서는 `ImportError`가 발생합니다. `agent_framework.azure` 네임스페이스는 여전히 존재하지만,
이제는 Foundry 에이전트가 아닌 Azure Functions 클래스(`DurableAIAgent`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`)만 포함합니다.

### 확인된 오류 (`.venv_ga_test`)

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### 영향 받는 파일

| 파일 | 라인 |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — GA `agent-framework-core`와 호환되지 않는 `azure-ai-agentserver`

**상태:** 진행 중 | **심각도:** 🔴 높음 | **유형:** 중대한 변경 (상류 의존성 문제에 차단됨)

### 설명

`azure-ai-agentserver-agentframework==1.0.0b17`(최신)는 `agent-framework-core<=1.0.0rc3`으로 엄격히 고정합니다.
이 패키지를 GA 버전인 `agent-framework-core==1.0.0`과 함께 설치하면 pip가 `agent-framework-core`를 다시 `rc3`로 <strong>다운그레이드</strong>하여
`agent-framework-foundry==1.0.0` 및 `agent-framework-openai==1.0.0`이 작동하지 않게 됩니다.

따라서 모든 에이전트가 HTTP 서버 바인딩에 사용하는 `from azure.ai.agentserver.agentframework import from_agent_framework` 호출도 차단됩니다.

### 확인된 의존성 충돌 (`.venv_ga_test`)

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 영향 받는 파일

세 `main.py` 파일 모두 — 최상위 임포트 및 `main()` 내 함수 내부 임포트 모두 해당됨.

---

## KI-003 — `agent-dev-cli --pre` 플래그 더 이상 필요 없음

**상태:** ✅ 수정됨 (비중대한 변경) | **심각도:** 🟢 낮음

### 설명

이전의 모든 `requirements.txt` 파일에는 사전 출시 CLI를 가져오기 위해 `agent-dev-cli --pre`가 포함되어 있었습니다.
2026-04-02에 GA 1.0.0이 출시되면서, stable 릴리즈 `agent-dev-cli`는 더 이상 `--pre` 플래그 없이도 사용할 수 있습니다.

**적용된 수정:** 세 `requirements.txt` 파일에서 `--pre` 플래그가 제거되었습니다.

---

## KI-004 — Dockerfile이 `python:3.14-slim` (프리릴리즈 베이스 이미지) 사용 중

**상태:** 진행 중 | **심각도:** 🟡 낮음

### 설명

모든 `Dockerfile`은 베타 단계 Python 빌드인 `FROM python:3.14-slim`을 사용합니다.
운영 환경 배포를 위해서는 안정 버전(예: `python:3.12-slim`)으로 고정하는 것이 바람직합니다.

### 영향 받는 파일

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## 참고 자료

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 노력하고 있으나, 자동 번역에는 오류나 부정확성이 포함될 수 있음을 유의하시기 바랍니다. 원문 문서가 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문 인간 번역을 권장합니다. 본 번역 사용으로 인한 오해나 해석상 차이에 대해 당사는 책임지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->