# 既知の問題

このドキュメントは、現在のリポジトリの状態における既知の問題を追跡しています。

> 最終更新日: 2026-04-15。Python 3.13 / Windows の `.venv_ga_test` でテスト済み。

---

## 現在のパッケージ固定バージョン（3つのエージェントすべて）

| パッケージ | 現在のバージョン |
|---------|----------------|
| `agent-framework-azure-ai` | `1.0.0rc3` |
| `agent-framework-core` | `1.0.0rc3` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` |
| `azure-ai-agentserver-core` | `1.0.0b16` |
| `agent-dev-cli` | `--pre` *(修正済み— KI-003 を参照)* |

---

## KI-001 — GA 1.0.0 アップグレードの阻害: `agent-framework-azure-ai` が削除

**ステータス:** オープン | **重大度:** 🔴 高 | **種類:** 破壊的変更

### 説明

`agent-framework-azure-ai` パッケージ（`1.0.0rc3` に固定）は GA リリース（1.0.0、2026-04-02 リリース）で **削除/非推奨** となりました。代替は以下です：

- `agent-framework-foundry==1.0.0` — Foundry ホスト型エージェントパターン
- `agent-framework-openai==1.0.0` — OpenAI バックのエージェントパターン

全ての `main.py` ファイルは `agent_framework.azure` から `AzureAIAgentClient` をインポートしていますが、GA パッケージでは `ImportError` が発生します。`agent_framework.azure` 名前空間は GA でも存在しますが、今は Azure Functions クラス（`DurableAIAgent`、`AzureAISearchContextProvider`、`CosmosHistoryProvider`）のみを含み、Foundry エージェントは含みません。

### 確認済みエラー（`.venv_ga_test`）

```
ImportError: cannot import name 'AzureAIAgentClient' from 'agent_framework.azure'
  (~\.venv_ga_test\Lib\site-packages\agent_framework\azure\__init__.py)
```

### 影響ファイル

| ファイル | 行 |
|------|------|
| `ExecutiveAgent/main.py` | 15 |
| `workshop/lab01-single-agent/agent/main.py` | 15 |
| `workshop/lab02-multi-agent/PersonalCareerCopilot/main.py` | 22 |

---

## KI-002 — `azure-ai-agentserver` が GA `agent-framework-core` と非互換

**ステータス:** オープン | **重大度:** 🔴 高 | **種類:** 破壊的（アップストリームでブロック）

### 説明

`azure-ai-agentserver-agentframework==1.0.0b17`（最新）は `agent-framework-core<=1.0.0rc3` を厳密に固定しています。これを GA の `agent-framework-core==1.0.0` と共にインストールすると、pip は `agent-framework-core` を rc3 に <strong>ダウングレード</strong> し、結果として `agent-framework-foundry==1.0.0` と `agent-framework-openai==1.0.0` が破損します。

全てのエージェントで HTTP サーバーにバインドするために使用されている `from azure.ai.agentserver.agentframework import from_agent_framework` 呼び出しもこれによりブロックされます。

### 確認済み依存関係コンフリクト（`.venv_ga_test`）

```
ERROR: pip's dependency resolver does not currently take into account all the packages
that are installed. This behaviour is the source of the following dependency conflicts.
agent-framework-foundry 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
agent-framework-openai 1.0.0 requires agent-framework-core<2,>=1.0.0,
  but you have agent-framework-core 1.0.0rc3 which is incompatible.
```

### 影響ファイル

3つの `main.py` ファイル全て — トップレベルのインポートおよび `main()` 内の関数内インポート。

---

## KI-003 — `agent-dev-cli --pre` フラグ不要に

**ステータス:** ✅ 修正済み（非破壊） | **重大度:** 🟢 低

### 説明

全ての `requirements.txt` ファイルには以前、プレリリース CLI を取得するために `agent-dev-cli --pre` が含まれていました。GA 1.0.0 が 2026-04-02 にリリースされて以来、安定版 `agent-dev-cli` はもはや `--pre` フラグなしで入手可能です。

**修正内容:** 3つの `requirements.txt` 全てから `--pre` フラグが削除されました。

---

## KI-004 — Dockerfile が `python:3.14-slim`（プレリリース版ベースイメージ）を使用

**ステータス:** オープン | **重大度:** 🟡 低

### 説明

全ての `Dockerfile` は `FROM python:3.14-slim` を使用しており、これはプレリリース版の Python ビルドを追跡しています。本番環境へのデプロイでは安定版リリース（例: `python:3.12-slim`）に固定するべきです。

### 影響ファイル

- `ExecutiveAgent/Dockerfile`
- `workshop/lab01-single-agent/agent/Dockerfile`
- `workshop/lab02-multi-agent/PersonalCareerCopilot/Dockerfile`

---

## 参照

- [agent-framework-core on PyPI](https://pypi.org/project/agent-framework-core/)
- [agent-framework-foundry on PyPI](https://pypi.org/project/agent-framework-foundry/)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**:  
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性には努めておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文のネイティブ言語版が正式な情報源とみなされます。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の使用により生じたいかなる誤解や誤訳についても当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->