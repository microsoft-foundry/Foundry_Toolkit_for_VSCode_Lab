# モジュール 8 - トラブルシューティング

このモジュールでは、マルチエージェントワークフローに固有の一般的なエラー、修正、およびデバッグ戦略を扱います。

## エージェント出力の問題

### GapAnalyzerが「まだマッチングレポートがありません」と言う場合

**症状:** GapAnalyzerの応答が「スキル不足」および「認定ギャップ」を含むマッチングレポートの貼り付けを求めます。これは履歴書と職務記述書の両方を送信した場合でも発生します。

**原因:** JDテキストがJDエージェントに渡されていません。`context_mode="last_agent"`では、`resume_executor`だけがユーザーの元のメッセージを受け取ります。`RESUME_PARSER_INSTRUCTIONS`にJDテキストが出力に含まれていない場合、JDエージェントは解析するJDがなく、MatchingAgentは適合スコアを計算できず、GapAnalyzerには意味のない入力が渡されます。

**診断:**

サーバーログでMatchingAgentのスパンを探します。以下が含まれている場合:
```
Cannot compute a numeric fit score because no job description (JD) was provided
```
パススルーが欠落または壊れています。

**修正:** `main.py`の`RESUME_PARSER_INSTRUCTIONS`に`[JOB DESCRIPTION PASS-THROUGH]`セクションと以下のルールが含まれているか確認してください。
```
The [JOB DESCRIPTION PASS-THROUGH] section MUST contain the FULL, UNMODIFIED JD text.
```
また、`JOB_DESCRIPTION_INSTRUCTIONS`に`[PARSED RESUME PASS-THROUGH]`のリレールールが含まれているか確認してください。
```
Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.
```
どちらかの指示ブロックがスカフォールドウィザードのスタブであれば、[`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)の完全なバージョンに置き換えてください。

### MatchingAgent が「適合スコアを計算できません - JDが提供されていません」と出力する場合

これは上記と同じ根本原因です。MatchingAgentはJDエージェントの出力を受け取りましたが`[PARSED RESUME PASS-THROUGH]`セクションが欠落または空だったため、両プロファイルを比較できません。以下を確認してください：
1. `JOB_DESCRIPTION_INSTRUCTIONS`にリレールール：`Copy [PARSED RESUME] verbatim - the Matching Agent depends on it downstream.` が含まれている。
2. `MATCHING_AGENT_INSTRUCTIONS`がエージェントに`[JD REQUIREMENTS]`および`[PARSED RESUME PASS-THROUGH]`セクションを探すよう指示している。

両方の指示ブロックを[`PersonalCareerCopilot/main.py`](../../../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py)の完全なバージョンに置き換えてください。

### 応答が2回表示される場合

**症状:** GapAnalyzer出力（またはパイプライン全体の出力）がAgent Inspectorの応答に2回表示されます。

**原因:** `WorkflowBuilder`は入力エッジに対してORセマンティクスを使います。つまり、<strong>いずれかの</strong>前任者が完了すると下流のExecutorが起動します。`matching_executor`に2つの入力エッジ（`resume_executor`からと`jd_executor`から）がある場合、ResumeParser完了時とJDエージェント完了時の2回起動します。結果、GapAnalyzerも2回実行されます。

**修正:** `WorkflowBuilder`グラフが厳密に単一シーケンシャルのパイプラインで、ファンインがないことを確認してください：

```python
workflow_agent = (
    WorkflowBuilder(start_executor=resume_executor, output_executors=[gap_executor])
    .add_edge(resume_executor, jd_executor)
    .add_edge(jd_executor, matching_executor)    # resume_executor からではありません
    .add_edge(matching_executor, gap_executor)
    .build().as_agent()
)
```

もし余分な`.add_edge(resume_executor, matching_executor)`行があれば削除してください。JDエージェントの出力にある`[PARSED RESUME PASS-THROUGH]`リレーにより、MatchingAgentはすでに履歴書にアクセスできます。

---

## 環境・構成の問題

### `.env` ファイルがない、または値が間違っている

`.env`ファイルは`PersonalCareerCopilot/`ディレクトリ（`main.py`と同階層）に置く必要があります：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

期待される`.env`の内容：

**パス A - Foundry クラウド:**

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

**パス B - Foundry ローカル:**

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

> 両パスは`FOUNDRY_PROJECT_ENDPOINT`を使います。値は違います：クラウドは`https://`のFoundryエンドポイント、ローカルは`http://localhost:5273/v1`です。`foundry model list`で正確なモデルエイリアスを確認してください（パスB用）。

> **`FOUNDRY_PROJECT_ENDPOINT`の見つけ方:** 
- VS Codeの<strong>Foundry Toolkit</strong>サイドバーを開き→プロジェクトを右クリック→**Copy Project Endpoint**。 
- または[Azure Portal](https://portal.azure.com)→Foundryプロジェクト→<strong>概要</strong>→**Project endpoint**。

> **`AZURE_AI_MODEL_DEPLOYMENT_NAME`の見つけ方:** Foundry Toolkitサイドバーでプロジェクトを展開→**Models**→デプロイ済みモデル名（例：`gpt-4.1-mini`）を探す。

### 環境変数の優先順位

`main.py`は`load_dotenv(override=True)`を使っています。これは以下を意味します：

| 優先順位 | ソース | 両方設定されている場合の勝者 |
|----------|--------|------------------------------|
| 1（最高） | `.env` ファイル | はい |
| 2 | シェル／コンテナ環境変数 | `.env`にないキーが使われる |

ローカル開発では`.env`が真実の情報源であり、編集するとすぐに反映されます。ホストされたデプロイではFoundryがコンテナレベルで環境変数を注入するので、このラボセットアップではデプロイ済みイメージに`.env`は含まれず、注入された値が使われます。

---

## バージョン互換性

### パッケージバージョンマトリックス

マルチエージェントワークフローには特定のパッケージバージョンが必要です。バージョン不一致はランタイムエラーの原因となります。

| パッケージ | 必要なバージョン | 確認コマンド |
|---------|-----------------|---------------|
| `agent-framework-foundry` | 最新 | `pip show agent-framework-foundry` |
| `agent-framework-foundry-hosting` | 最新 | `pip show agent-framework-foundry-hosting` |
| `mcp` | `<2,>=1.24.0` | `pip show mcp` |
| `debugpy` | 最新 | `pip show debugpy` |
| Python | 3.12以上 | `python --version` |

### よくあるバージョンエラー

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正: agent-framework-foundry を再インストールする
pip install agent-framework-foundry agent-framework-foundry-hosting
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：mcpパッケージをアップグレードする
pip install mcp --upgrade
```

### バージョンを一括で確認する

```powershell
pip list | Select-String "agent-framework|mcp|debugpy"
```

期待される出力：

```
agent-framework-foundry          x.x.x
agent-framework-foundry-hosting  x.x.x
debugpy                          x.x.x
mcp                              x.x.x
```

---

## デプロイに関する問題

### デプロイ後にコンテナが起動しない

1. **コンテナログの確認:**  
   - <strong>Foundry Toolkit</strong>サイドバーを開き→<strong>Hosted Agents (Preview)</strong>を展開→対象エージェントをクリック→バージョンを展開→**Container Details**→**Logs**。  
   - Pythonのスタックトレースやモジュール未検出エラーを探してください。

2. **よくあるコンテナ起動失敗原因:**

   | ログのエラー | 原因 | 修正 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt`にパッケージ不足 | パッケージ追加、再デプロイ |
   | `KeyError: 'FOUNDRY_PROJECT_ENDPOINT'` | `agent.yaml`または`.env`の環境変数未設定 | `agent.yaml`の`environment_variables`セクション（ホスト）または`.env`（ローカル）を更新 |
   | `azure.identity.CredentialUnavailableError` | マネージドアイデンティティ未設定 | Foundryが自動設定 - エクステンション経由のデプロイを確認 |
   | `OSError: port 8088 already in use` | Dockerfileのポート設定ミスまたはポート競合 | Dockerfileの`EXPOSE 8088`と`CMD ["python", "main.py"]`を確認 |
   | コンテナがコード1で終了 | `main()`の未処理例外 | 先にローカルテスト（[Module 5](05-test-locally.md)）でエラーを確認 |

3. **修正後の再デプロイ:**  
   - `Ctrl+Shift+P` → **Foundry Toolkit: Deploy Hosted Agent** → 同じエージェントを選択 → 新バージョンをデプロイ。

### デプロイに時間がかかる

マルチエージェントコンテナは起動時に4つのエージェントインスタンスを生成するため、起動に時間がかかります。通常の起動時間:

| ステージ | 予想所要時間 |
|-------|---------------|
| コンテナイメージビルド | 1～3分 |
| イメージをACRにプッシュ | 30～60秒 |
| コンテナ起動（単一エージェント） | 15～30秒 |
| コンテナ起動（マルチエージェント） | 30～120秒 |
| Playgroundでエージェント使用可能 | 「Started」表示後1～2分 |

> 「Pending」状態が5分以上続く場合は、コンテナログにエラーがないか確認してください。

---

## RBACおよび権限の問題

### `403 Forbidden` または `AuthorizationFailed`

Foundryプロジェクトで<strong>[Foundry User](https://aka.ms/foundry-ext-project-role)</strong> ロールが必要です（以前は<strong>Azure AI User</strong>、ロールIDは変更なし）：

1. [Azure Portal](https://portal.azure.com)に行き→Foundryの<strong>プロジェクト</strong>リソースへ。
2. **アクセス制御 (IAM)**→<strong>ロール割り当て</strong>をクリック。
3. 名前を検索し→**Foundry User**（または旧ラベルの<strong>Azure AI User</strong>）があるか確認。
4. なければ：<strong>追加</strong>→<strong>ロール割り当ての追加</strong>→<strong>Foundry User</strong>を検索→アカウントに割り当て。

詳細は[Microsoft FoundryのRBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)ドキュメントを参照してください。

### モデルデプロイが利用できない

エージェントがモデル関連のエラーを返す場合：

1. モデルがデプロイされているか確認：Foundryサイドバー→プロジェクト展開→**Models**→`gpt-4.1-mini`（または使用モデル）が<strong>Succeeded</strong>状態か確認。
2. デプロイメント名が一致しているか：`.env`（または`agent.yaml`）の`AZURE_AI_MODEL_DEPLOYMENT_NAME`とサイドバーの実際のデプロイ名を比較。
3. デプロイが有効期限切れの場合（無料プラン）：[Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)から再デプロイ（`Ctrl+Shift+P`→**Foundry Toolkit: Open Model Catalog**）。

---

## Foundry ローカルの問題（パスB）

### Foundry Localサービスが起動していない

```powershell
# ステータスを確認する
foundry local status

# 停止している場合はサービスを開始する
foundry local start
```

| 症状 | 原因 | 修正 |
|---------|-------|-----|
| ヘルスチェックで `503` が返る | サービスが起動していない | `foundry local start` または Foundry Toolkitサイドバーの<strong>Start</strong>をクリック |
| ヘルスチェックがタイムアウト | モデルがまだ読み込み中 | 起動後30～60秒待つ。大きいモデルはさらに必要 |
| `/v1/health`で`StatusCode: 404` | ポート誤り | デフォルトは`5273`。`foundry local status`で実際のポート確認 |
| リソース不足 | Foundry Localは約4GBの空きRAMが必要 | 他プログラムを閉じる |
| モデルのダウンロード失敗 | ディスク空き容量不足 | モデルは2～8GB。空きを増やしてから`foundry model pull <name>` |

### モデル名の不一致

```powershell
# ダウンロードしたモデルとそれらの正確な別名を一覧表示する
foundry model list
```

`.env`内の`AZURE_AI_MODEL_DEPLOYMENT_NAME`を正確なエイリアスに設定してください（例：`phi-4-mini`、`Phi-4-mini`ではありません）。

### ローカル実行時の`KeyError: 'FOUNDRY_PROJECT_ENDPOINT'`（パスB）

ラボの`main.py`は`os.environ["FOUNDRY_PROJECT_ENDPOINT"]`を使用しています。Foundry Localはこの変数をローカルサービスの指すものにする必要があり、`AZURE_AI_PROJECT_ENDPOINT`ではありません。`.env`に以下を含めてください：

```env
FOUNDRY_PROJECT_ENDPOINT=http://localhost:5273/v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=phi-4-mini
```

### MCPツールがまだ外部コールをする（パスB）

これは正常です。`search_microsoft_learn_for_plan`ツールは`https://learn.microsoft.com/api/mcp`から学習リソースを取得します。<strong>スキル名クエリのみ</strong>がネットワーク経由で送信され、履歴書とJDテキストは完全にローカルで処理され送信されません。完全オフライン運用が必要なら、到達不能時に静的な`learn.microsoft.com` URLを返す`try/except`のフォールバックをツールに追加してください。

---

## ヘルプの受け方

以上の修正を試しても解決しない場合：

1. <strong>サーバーログを確認</strong> - ほとんどのエラーはターミナルにPythonのスタックトレースを出します。トレースを最後まで読んでください。
2. <strong>エラーメッセージを検索</strong> - エラー文をコピーして[Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)で検索。
3. **Issueを開く** - [ワークショップリポジトリ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)に以下を添えてIssueを提出してください：
   - エラーメッセージやスクリーンショット
   - パッケージバージョン（`pip list | Select-String "agent-framework"`）
   - Pythonバージョン（`python --version`）
   - ローカルかデプロイ後かの区別

---

### チェックポイント

- [ ] `.env`構成問題の確認と修正方法がわかる
- [ ] パッケージバージョンが要求されるマトリックスに合致していることを確認できる
- [ ] デプロイ失敗時にコンテナログを確認できる
- [ ] Azure PortalでRBACロールを確認できる

---

**前:** [07 - Playgroundでの検証](07-verify-in-playground.md) · **次:** [09 - まとめ →](09-summary.md) · **ホーム:** [ラボ 02 README](../README.md) · [ワークショップ ホーム](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->