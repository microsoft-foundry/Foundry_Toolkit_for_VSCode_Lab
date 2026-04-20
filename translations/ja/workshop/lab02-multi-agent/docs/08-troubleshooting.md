# Module 8 - トラブルシューティング（マルチエージェント）

このモジュールでは、マルチエージェントワークフローに特有の一般的なエラー、修正方法、およびデバッグ手法を扱います。Foundryの一般的なデプロイメントの問題については、[Lab 01トラブルシューティングガイド](../../lab01-single-agent/docs/08-troubleshooting.md)も参照してください。

---

## クイックリファレンス：エラー → 修正

| エラー / 症状 | 想定される原因 | 修正方法 |
|----------------|-------------|-----|
| `RuntimeError: Missing required environment variable(s)` | `.env`ファイルがないか、値が設定されていない | `.env`を作成し、`PROJECT_ENDPOINT=<your-endpoint>` と `MODEL_DEPLOYMENT_NAME=<your-model>` を設定する |
| `ModuleNotFoundError: No module named 'agent_framework'` | 仮想環境がアクティベートされていないか依存関係がインストールされていない | `.\.venv\Scripts\Activate.ps1` を実行後、`pip install -r requirements.txt` を実行 |
| `ModuleNotFoundError: No module named 'mcp'` | MCPパッケージがインストールされていない（requirementsに含まれていない） | `pip install mcp` を実行するか、`requirements.txt`にトランジティブ依存関係として含まれているか確認 |
| エージェントは起動するが空のレスポンスを返す | `output_executors`の不一致またはエッジが欠落 | `output_executors=[gap_analyzer]`を確認し、`create_workflow()` 内の全てのエッジが存在するか検証 |
| ギャップカードが1枚しか表示されない（他は欠落） | GapAnalyzerの指示が不完全 | `GAP_ANALYZER_INSTRUCTIONS` に `CRITICAL:` の段落を追加する — 詳しくは [Module 3](03-configure-agents.md) を参照 |
| フィットスコアが0または表示されない | MatchingAgentが上流データを受け取っていない | `add_edge(resume_parser, matching_agent)`と`add_edge(jd_agent, matching_agent)`の両方が存在することを確認 |
| `POST https://learn.microsoft.com/api/mcp → 4xx/5xx` | MCPサーバーがツール呼び出しを拒否している | インターネット接続を確認。ブラウザーで `https://learn.microsoft.com/api/mcp` を開き、再試行する |
| 出力にMicrosoft LearnのURLがない | MCPツールが登録されていないかエンドポイントが間違っている | GapAnalyzerの `tools=[search_microsoft_learn_for_plan]` と `MICROSOFT_LEARN_MCP_ENDPOINT` が正しいか確認 |
| `Address already in use: port 8088` | 他のプロセスがポート8088を使用中 | `netstat -ano \| findstr :8088`（Windows）または `lsof -i :8088`（macOS/Linux）を実行し、競合プロセスを停止 |
| `Address already in use: port 5679` | Debugpyのポート競合 | 他のデバッグセッションを停止。`netstat -ano \| findstr :5679` で該当プロセスを特定し終了 |
| Agent Inspectorが開かない | サーバーが完全に起動していないかポート競合 | "Server running" のログを待ち、ポート5679が空いているか確認 |
| `azure.identity.CredentialUnavailableError` | Azure CLIにサインインしていない | `az login` を実行し、その後サーバーを再起動 |
| `azure.core.exceptions.ResourceNotFoundError` | モデルデプロイメントが存在しない | `MODEL_DEPLOYMENT_NAME` がFoundryプロジェクトの展開済みモデルと一致するか確認 |
| デプロイ後にコンテナの状態が「Failed」 | コンテナが起動時にクラッシュした | Foundryのサイドバーでコンテナログを確認。よくある原因：env変数の欠落またはインポートエラー |
| デプロイが5分以上「Pending」のまま | コンテナの起動に時間がかかっている、またはリソース制限 | マルチエージェントは4つのエージェントインスタンスを作成するため最大5分待つ。まだ保留ならログを確認 |
| `ValueError` が `WorkflowBuilder` から発生 | グラフ構成が無効 | `start_executor`が設定されているか、`output_executors`がリスト形式か、循環エッジがないか確認 |

---

## 環境および設定の問題

### `.env` の値が欠落または誤っている

`.env` ファイルは `PersonalCareerCopilot/` ディレクトリ (`main.py` と同じ階層) に配置する必要があります：

```
PersonalCareerCopilot/
├── .env                  ← Must be here
├── main.py
├── agent.yaml
├── Dockerfile
└── requirements.txt
```

期待される `.env` の内容：

```env
PROJECT_ENDPOINT=https://<your-project-name>.services.ai.azure.com/api/projects/<your-project-id>
MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

> **PROJECT_ENDPOINTを見つける方法：**  
- VS Codeの **Microsoft Foundry** サイドバーを開き → プロジェクトを右クリック → **Copy Project Endpoint** を選択。  
- または [Azure Portal](https://portal.azure.com) にアクセス → Foundryプロジェクト → <strong>概要</strong> → **Project endpoint**。

> **MODEL_DEPLOYMENT_NAMEを見つける方法：** Foundryサイドバーでプロジェクトを展開 → **Models** → 展開済みモデル名を確認（例：`gpt-4.1-mini`）。

### 環境変数の優先順位

`main.py` は `load_dotenv(override=False)` を使用しているため：

| 優先順位 | ソース | 両方設定されている場合に優先されるか |
|----------|--------|----------------------|
| 1（最高） | シェル環境変数 | はい |
| 2 | `.env`ファイル | シェル変数が設定されていない場合のみ |

つまり、ホストされたデプロイ時にはFoundryのランタイム環境変数（`agent.yaml`経由で設定）が`.env`の値より優先されます。

---

## バージョン互換性

### パッケージバージョンマトリクス

マルチエージェントワークフローには特定のパッケージバージョンが必要です。バージョンが合っていないとランタイムエラーになります。

| パッケージ | 必要バージョン | 確認コマンド |
|---------|-----------------|---------------|
| `agent-framework-core` | `1.0.0rc3` | `pip show agent-framework-core` |
| `agent-framework-azure-ai` | `1.0.0rc3` | `pip show agent-framework-azure-ai` |
| `azure-ai-agentserver-agentframework` | `1.0.0b16` | `pip show azure-ai-agentserver-agentframework` |
| `azure-ai-agentserver-core` | `1.0.0b16` | `pip show azure-ai-agentserver-core` |
| `agent-dev-cli` | 最新プレリリース | `pip show agent-dev-cli` |
| Python | 3.10以上 | `python --version` |

### よくあるバージョンエラー

**`ImportError: cannot import name 'WorkflowBuilder' from 'agent_framework'`**

```powershell
# 修正: rc3にアップグレード
pip install agent-framework-core==1.0.0rc3 agent-framework-azure-ai==1.0.0rc3
```

**`agent-dev-cli` が見つからない、またはInspectorが非互換：**

```powershell
# 修正: --pre フラグを使ってインストール
pip install agent-dev-cli --pre --upgrade
```

**`AttributeError: module 'mcp.client' has no attribute 'streamable_http'`**

```powershell
# 修正：mcpパッケージをアップグレードする
pip install mcp --upgrade
```

### すべてのバージョンを一括で確認

```powershell
pip list | Select-String "agent-framework|azure-ai-agent|agent-dev|mcp|debugpy"
```

期待される出力例：

```
agent-dev-cli                  x.x.x
agent-framework-azure-ai       1.0.0rc3
agent-framework-core            1.0.0rc3
azure-ai-agentserver-agentframework 1.0.0b16
azure-ai-agentserver-core      1.0.0b16
debugpy                         x.x.x
mcp                             x.x.x
```

---

## MCPツールの問題

### MCPツールが結果を返さない

**症状:** ギャップカードに「No results returned from Microsoft Learn MCP」や「No direct Microsoft Learn results found」と表示される。

**考えられる原因：**

1. <strong>ネットワーク障害</strong> - MCPエンドポイント（`https://learn.microsoft.com/api/mcp`）にアクセスできない。  
   ```powershell
   # 接続性をテストする
   Invoke-WebRequest -Uri "https://learn.microsoft.com/api/mcp" -Method POST -UseBasicParsing
   ```
   ここで `200` が返っていればエンドポイントに到達可能。

2. <strong>クエリが特定しすぎている</strong> - Microsoft Learnの検索に対してスキル名が専門的すぎる。  
   - 非常に限定的なスキルではこれは正常。ツールはレスポンス内にフォールバックURLを含む。

3. **MCPセッションのタイムアウト** - Streamable HTTP接続がタイムアウトした。  
   - リクエストを再試行。MCPセッションは一時的で、再接続が必要な場合がある。

### MCPログの解説

```
GET https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
POST https://learn.microsoft.com/api/mcp → 200
DELETE https://learn.microsoft.com/api/mcp → 405 (Method Not Allowed)
```

| ログ | 意味 | 対処 |
|-----|---------|--------|
| `GET → 405` | MCPクライアントが初期化時にプローブ | 正常 - 無視してOK |
| `POST → 200` | ツール呼び出し成功 | 期待される挙動 |
| `DELETE → 405` | MCPクライアントがクリーンアップ時にプローブ | 正常 - 無視してOK |
| `POST → 400` | 不正なリクエスト（不正フォーマットクエリ） | `search_microsoft_learn_for_plan()`の`query`パラメータをチェック |
| `POST → 429` | レート制限 | 待機して再試行。`max_results`パラメータを減らす |
| `POST → 500` | MCPサーバーエラー | 一時的問題 - リトライ。継続ならMicrosoft Learn MCP APIの障害の可能性 |
| 接続タイムアウト | ネットワーク問題またはMCPサーバーが利用不可 | インターネット接続を確認。`curl https://learn.microsoft.com/api/mcp` を試す |

---

## デプロイメントの問題

### デプロイ後にコンテナが起動しない

1. **コンテナログを確認：**  
   - **Microsoft Foundry** サイドバーを開き → **Hosted Agents (Preview)** を展開 → エージェントをクリック → バージョンを展開 → **Container Details** → <strong>Logs</strong>へ。  
   - Pythonのスタックトレースやモジュール見つからないエラーを探す。

2. **よくあるコンテナ起動失敗の原因と対処：**

   | ログのエラー | 原因 | 修正方法 |
   |--------------|-------|-----|
   | `ModuleNotFoundError` | `requirements.txt` にパッケージが欠落 | パッケージを追加し再デプロイ |
   | `RuntimeError: Missing required environment variable` | `agent.yaml`の環境変数設定が不足 | `agent.yaml`の`environment_variables`セクションを更新 |
   | `azure.identity.CredentialUnavailableError` | マネージドID未設定 | Foundryが自動設定するので拡張機能経由でデプロイしているか確認 |
   | `OSError: port 8088 already in use` | DockerfileのEXPOSEポート誤指定またはポート競合 | Dockerfileの`EXPOSE 8088`と起動コマンド(`CMD ["python", "main.py"]`)を確認 |
   | コンテナがコード1で終了 | `main()`内の例外未処理 | 最初にローカルでテスト（[Module 5](05-test-locally.md)）し、エラーを確認してからデプロイ |

3. **修正後に再デプロイ：**  
   - `Ctrl+Shift+P` → **Microsoft Foundry: Deploy Hosted Agent** → 同じエージェントを選択し新しいバージョンをデプロイ。

### デプロイに時間がかかりすぎる

マルチエージェントのコンテナは起動時に4つのエージェントインスタンスを作成するため、起動に時間がかかります。標準的な起動時間：

| ステージ | 目安時間 |
|-------|------------------|
| コンテナイメージビルド | 1～3分 |
| ACRへのイメージプッシュ | 30～60秒 |
| コンテナ起動（シングルエージェント） | 15～30秒 |
| コンテナ起動（マルチエージェント） | 30～120秒 |
| Playgroundでエージェント利用可能になるまで | 「Started」ログの1～2分後 |

> 5分以上「Pending」が続く場合はコンテナログをエラー確認。

---

## RBACおよび権限の問題

### `403 Forbidden` または `AuthorizationFailed`

Foundryプロジェクトに **[Azure AI User](https://aka.ms/foundry-ext-project-role)** ロールが必要です：

1. [Azure Portal](https://portal.azure.com) → Foundryの<strong>プロジェクト</strong>リソースへ。
2. **アクセス制御 (IAM)** → <strong>ロール割り当て</strong>をクリック。
3. 名前で検索し、**Azure AI User** がリストにあるか確認。
4. 無ければ：<strong>追加</strong> → <strong>ロール割り当ての追加</strong> → **Azure AI User** を検索 → 自分のアカウントに割り当て。

詳細は[Microsoft FoundryのRBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)ドキュメント参照。

### モデルデプロイメントがアクセスできない

エージェントがモデル関連のエラーを返す場合：

1. モデルがデプロイ済みか確認：Foundryサイドバー → プロジェクト展開 → **Models** → `gpt-4.1-mini`（または使用モデル）の状態が **Succeeded** であること。
2. デプロイメント名が一致しているか確認： `.env` または `agent.yaml` の `MODEL_DEPLOYMENT_NAME` とサイドバーの実際のデプロイメント名を比較。
3. デプロイが期限切れ（無料プランの場合）：[Model Catalog](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)から再デプロイ (`Ctrl+Shift+P` → **Microsoft Foundry: Open Model Catalog**)。

---

## Agent Inspectorの問題

### Inspectorは開くが「Disconnected」と表示される

1. サーバーが起動中か確認：ターミナルに "Server running on http://localhost:8088" のログがあるかチェック。
2. ポート5679を確認：Inspectorはdebugpy経由でポート5679に接続。  
   ```powershell
   netstat -ano | findstr :5679
   ```
3. サーバーを再起動し、Inspectorを再度開く。

### Inspectorが部分的なレスポンスを表示する

マルチエージェントのレスポンスは長く、ストリーミングで徐々に返されます。レスポンスの完全な受信完了（ギャップカードの数とMCPツール呼び出しの数によって30～60秒かかる場合あり）を待ってください。

レスポンスが一貫して切れる場合：

- GapAnalyzerの指示にギャップカードを結合させない `CRITICAL:` ブロックが含まれているか確認。
- モデルのトークン制限を確認。`gpt-4.1-mini`は最大32Kトークン出力対応で十分なはずです。

---

## パフォーマンスのヒント

### レスポンスが遅い

マルチエージェントワークフローは、シーケンシャルな依存とMCPツール呼び出しのため、単一エージェントより本質的に遅くなります。

| 最適化 | 方法 | 影響 |
|-------------|-----|--------|
| MCP呼び出しを減らす | ツールの `max_results` パラメータを下げる | HTTPラウンドトリップ回数減少 |
| 指示を簡潔にする | エージェントへのプロンプトを短く焦点を絞る | LLM推論が速くなる |
| `gpt-4.1-mini` を使う | `gpt-4.1`より開発が高速 | 約2倍の速度改善 |
| ギャップカードの詳細を減らす | GapAnalyzerの指示内でギャップカード形式を簡素化 | 出力生成が少なくなる |

### ローカルでの典型的な応答時間

| 設定 | 目安時間 |
|--------------|---------------|
| `gpt-4.1-mini`、ギャップカード3～5枚 | 30～60秒 |
| `gpt-4.1-mini`、ギャップカード8枚以上 | 60～120秒 |
| `gpt-4.1`、ギャップカード3～5枚 | 60～120秒 |
---

## ヘルプを得る

上記の修正を試みた後に問題が解決しない場合は：

1. <strong>サーバーログを確認する</strong> - ほとんどのエラーはターミナルにPythonのスタックトレースを生成します。完全なトレースバックを読みます。
2. <strong>エラーメッセージを検索する</strong> - エラーのテキストをコピーして、[Microsoft Q&A for Azure AI](https://learn.microsoft.com/answers/tags/azure-ai-services)で検索します。
3. <strong>問題を報告する</strong> - [ワークショップリポジトリ](https://github.com/ShivamGoyal03/ai-toolkit-hosted-agents-workshop/issues)で問題を記録します:
   - エラーメッセージまたはスクリーンショット
   - パッケージのバージョン (`pip list | Select-String "agent-framework"`)
   - Pythonのバージョン (`python --version`)
   - 問題がローカルかデプロイ後か

---

### チェックポイント

- [ ] クイックリファレンステーブルを使って、最も一般的なマルチエージェントのエラーを特定し修正できる
- [ ] `.env` の設定問題を確認・修正する方法を知っている
- [ ] パッケージのバージョンが必要なマトリックスと一致するか確認できる
- [ ] MCPのログエントリーを理解し、ツールの障害を診断できる
- [ ] デプロイ失敗のためにコンテナログを確認する方法を知っている
- [ ] AzureポータルでRBACロールを確認できる

---

**前へ:** [07 - Playgroundでの検証](07-verify-in-playground.md) · **ホーム:** [Lab 02 README](../README.md) · [ワークショップホーム](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**:  
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご了承ください。原文のネイティブ言語による文書が正式な情報源と見なされます。重要な情報については、専門の人間による翻訳を推奨します。当該翻訳の使用により生じたいかなる誤解や誤訳についても、一切の責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->