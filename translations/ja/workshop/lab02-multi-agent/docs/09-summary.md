# モジュール9 - まとめと次のステップ

⏱️ 約5分

**おめでとうございます！** Microsoft FoundryとFoundry Toolkit for VS Codeを使って、マルチエージェントワークフローを構築、テストし（Path Aの場合は）デプロイしました。

---

## 何を構築したか

**Resume → Job Fit Evaluator** － マルチエージェントホスト型ワークフローで、以下のことを行います：
- HTTP経由で履歴書＋職務記述書を受け取る（`POST /responses`）
- 4つの専門化されたエージェントを連続パイプラインで実行し、それぞれのエージェントが後続に必要なデータを中継
- 適合スコア（0〜100の内訳つき）、スキルと認定のギャップリスト、および各ギャップに対するMicrosoft Learnのリンクつき個別学習ロードマップを返す
- Microsoft Learn MCPサーバー（`https://learn.microsoft.com/api/mcp`）を呼び出して、特定されたスキルギャップごとの公式学習リソースを取得
- Microsoft Foundry Agent Service上で単一のコンテナ化されたホスト型エージェントとして動作

---

## 学んだ重要な概念

| 概念 | 練習内容 |
|---------|-------------------|
| <strong>マルチエージェントオーケストレーション</strong> | `WorkflowBuilder`の連続パイプラインでの`add_edge()`利用 |
| <strong>エージェント専門化</strong> | 4つの特化エージェントは1つの汎用エージェントより優れる |
| **Content Routerパターン** | ResumeParserがルーターも兼ねる - JDテキストを `[JOB DESCRIPTION PASS-THROUGH]` セクションに保持し、下流エージェントがアクセス可能にする（`context_mode="last_agent"`では`start_executor`のみが生のユーザーメッセージを見るために必要） |
| **Content Relayパターン** | JD Agentが`[PARSED RESUME PASS-THROUGH]`を転送し、MatchingAgentが両方のプロファイルを受け取り、ファンイングラフのORセマンティクスによる二重トリガーを回避 |
| **MCPツール統合** | `@tool` と `streamable_http_client` で外部MCPサーバーを呼び出し |
| <strong>ホスト型エージェントのライフサイクル</strong> | スキャフォールディング → 設定 → ローカルテスト → デプロイ → クラウド検証 |
| **`context_mode="last_agent"`** | 各エグゼキューターは直接前任者の出力のみを見る |
| **Foundry Toolkitワークフロー** | スキャフォールドウィザード、Agent Inspector、Workflow Visualizer、ワンクリックデプロイ |

---

## 完了した内容

<details open>
<summary><strong>🅰️ パスA - Foundryサブスクリプション</strong></summary>

- [x] Lab 01 のセットアップ確認：プロジェクト、モデル、RBACが有効
- [x] Workflowsテンプレートを使ったマルチエージェントプロジェクトのスキャフォールディング
- [x] 4つのエージェント指示セットの作成（ResumeParser、JD Agent、MatchingAgent、GapAnalyzer）
- [x] Microsoft Learn MCPツールと`streamable_http_client`の統合
- [x] `WorkflowBuilder`でワークフローグラフを配線（連続パイプライン＋コンテンツリレー）
- [x] 3つのスモークテストでローカルテスト（Agent Inspector） - 適合スコア、ギャップカード、MCP URL
- [x] Foundry Agent Serviceへのデプロイ（コンテナ化、マネージドアイデンティティ）
- [x] クラウドプレイグラウンドで確認 - ローカル結果との構造的整合性

</details>

<details open>
<summary><strong>🅱️ パスB - Foundry Local</strong></summary>

- [x] Lab 01 のセットアップ確認：Foundry Localでローカルモデル稼働中
- [x] Workflowsテンプレートを使ったマルチエージェントプロジェクトのスキャフォールディング
- [x] ４つのエージェント指示セット作成とワークフローグラフ配線
- [x] Microsoft Learn MCPツールの統合
- [x] 3つのスモークテストでローカルテスト
- [x] クラウドリソース不要のマルチエージェント動作の検証

</details>

---

## 次のステップ

### 学習を継続する

| リソース | 説明 |
|----------|-------------|
| **[Agent Framework SDKリファレンス](https://learn.microsoft.com/agent-framework/)** | `agent-framework-foundry`、`WorkflowBuilder`、`AgentExecutor`のAPIドキュメント |
| **[MCPツールカタログ](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)** | エージェントを他のMCPサーバーに接続（Bing、GitHub、カスタム） |
| **[知識の追加（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | ドキュメント、ベクターストア、Bing検索でエージェントをグラウンディング |
| **[Foundry評価機能](https://learn.microsoft.com/azure/foundry/evaluations/overview)** | 自動評価者でエージェント品質を大規模に計測 |
| **[Microsoft Foundryドキュメント](https://learn.microsoft.com/azure/foundry/)** | プラットフォーム全体のリファレンス |
| **[Foundry Toolkit 新機能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 拡張機能のリリースノートと変更履歴 |

### このワークフローを拡張するアイデア

- **5番目のエージェントを追加** - ギャップレポートに基づく面接質問を生成する面接コーチ
- **Bingグラウンディングツールを追加** - JD Agentが類似の求人を検索して要件を充実させる
- <strong>履歴書データベースに接続</strong> - カスタム`@tool`経由で候補者のプロファイルをデータベースから取得
- <strong>異なるモデルを試す</strong> - `gpt-4.1`と`gpt-4.1-mini`の出力品質と遅延を比較
- **Foundryで評価** - Evaluations機能を使い、ゴールデンデータセットに対するフィットレポートをスコアリング

### パスBユーザー向け：クラウドデプロイにアップグレード

クラウドデプロイ準備ができたら：
1. Azureサブスクリプションを取得する（[azure.microsoft.com/free](https://azure.microsoft.com/free/)）
2. [Lab 01, モジュール01](../../lab01-single-agent/docs/01-setup.md)を完了（プロジェクト作成、モデル展開、RBAC割当）
3. `.env`をFoundryプロジェクトエンドポイントとモデル展開名で更新
4. [モジュール06 - Foundryへデプロイ](06-deploy-to-foundry.md)から続行

---

## リソースのクリーンアップ（任意）

ワークショップで作成したAzureリソースを削除する場合：

### オプション1：リソースグループを削除（すべて削除）

```powershell
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### オプション2：ホスト型エージェントだけを削除

1. [ai.azure.com](https://ai.azure.com) → プロジェクト → <strong>ビルド</strong> → <strong>エージェント</strong> を開く。
2. <strong>PersonalCareerCopilot</strong>を探して<strong>削除</strong>をクリック。

### オプション3：モデル展開を削除

1. Foundryサイドバーでプロジェクトを展開 → <strong>モデル</strong>。
2. モデル展開を右クリック → <strong>削除</strong>。

> **コスト注意:** ホストエージェントは動作時のみ課金。停止または削除で継続課金なし。モデル展開は予約容量にわずかな課金あり—不要なら削除推奨。

---

**前へ:** [08 - トラブルシューティング](08-troubleshooting.md) · **ホーム:** [Lab 02 README](../README.md) · [ワークショップホーム](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->