# モジュール 7 - Playground での検証

⏱️ 約10分

このモジュールでは、展開したマルチエージェント ワークフローを VS Code と Foundry ポータルでテストし、エージェントがローカルでのテストと同じ挙動をすることを確認します。

---

## 展開後に再度テストする理由は？

ホスト環境はローカル環境といくつか重要な点で異なります：

| | ローカル | ホスト |
|--|-------|--------|
| **ID** | 個人のサインイン (`DefaultAzureCredential`) | 展開時に自動プロビジョニングされたエージェント専用の Entra ID |
| <strong>エンドポイント</strong> | `http://localhost:8088/responses` | Foundry Agent Service 管理の URL |
| <strong>ネットワーク</strong> | マシンから Azure OpenAI + MCP へ | Azure バックボーン（低遅延） |

環境変数の誤設定、RBAC の問題、または MCP のアウトバウンド呼び出しブロックの問題はここで最初に現れます。

---

## オプション A: VS Code Playground でのテスト（最初に推奨）

### ステップ 1: ホストされたエージェントへ移動

1. アクティビティバーの **Foundry Toolkit** アイコンをクリックします。
2. プロジェクトを展開 → **Hosted Agents (Preview)** → エージェントを見つけます。

![resume-job-fit-evaluator とその展開済みバージョンが表示された Foundry Toolkit サイドバーの Hosted Agents (Preview)](../../../../../translated_images/ja/06-foundry-sidebar-agent-status.a45994bfb5c21284.webp)

### ステップ 2: バージョンの選択

1. エージェントをクリックしてバージョンを展開します。
2. `v1` をクリック → ステータスが **active** であることを確認（サイドバーには「Running」または「Started」と表示される場合がありますが、どちらも準備完了を示します）。

### ステップ 3: Playground を開く

1. **Playground** をクリック（またはバージョンを右クリック → **Open in Playground**）。
2. チャットウィンドウが VS Code のタブで開きます。

### ステップ 4: スモークテストを実行

[モジュール 5](05-test-locally.md) の同じ3つのテストを使用します。Playgroundの入力ボックスにそれぞれのメッセージを入力し、**Send**（または **Enter**）を押します。

#### テスト 1 - フル履歴書 + JD（標準フロー）

モジュール 5 のテスト1（Jane Doe + Contoso Ltd のシニアクラウドエンジニア）のフル履歴書 + JD プロンプトを貼り付けます。

**期待結果:**
- フィットスコアの内訳計算（100点満点スケール）
- マッチしたスキルのセクション
- 欠落スキルのセクション
- **欠落スキルごとに1つのギャップカード** と Microsoft Learn の URL
- 学習ロードマップ（タイムラインあり）

#### テスト 2 - 簡易ショートテスト（最小入力）

```
RESUME: 3 years Python developer, knows Django and PostgreSQL, no cloud experience.

JOB: Cloud DevOps Engineer requiring AWS, Kubernetes, Terraform, CI/CD. 5 years needed.
```

**期待結果:**
- 低いフィットスコア（40未満）
- 正直な評価と段階的学習パス
- 複数のギャップカード（AWS、Kubernetes、Terraform、CI/CD、経験ギャップ）

#### テスト 3 - 高フィット候補者

```
RESUME:
10 years Azure Cloud Architect. AZ-305 certified. Expert in AKS, Terraform, Azure DevOps, 
Azure Functions, Helm, Prometheus, Grafana, Python, Go. Led platform team of 8.

JOB:
Senior Cloud Engineer. Required: AKS, Terraform, Azure DevOps, Python. Preferred: Helm, Go.
5+ years experience. AZ-305 preferred.
```

**期待結果:**
- 高いフィットスコア（80以上）
- 面接準備と仕上げに注力
- ギャップカードはほぼなしまたはなし
- 準備に特化した短いタイムライン

### ステップ 5: ローカル結果と比較

モジュール 5 で記録したローカルのメモまたはブラウザタブを開き、各テストについて：

- レスポンスの<strong>構造が同じか</strong>（フィットスコア、ギャップカード、ロードマップ）
- <strong>同じスコアリングルーブリックを使用しているか</strong>（100点満点の内訳）
- ギャップカードに<strong>Microsoft Learn の URL が残っているか</strong>
- **欠落スキルごとに1つのギャップカード** があるか（切り捨てなし）

> <strong>些細な表現の違いは正常です</strong> - モデルは非決定的です。構造、スコアの一貫性、MCPツールの利用に注目してください。

---

## オプション B: Foundry ポータルでのテスト

[Foundry ポータル](https://ai.azure.com) は、チームメンバーや利害関係者と共有するのに便利な Web ベースのプレイグラウンドを提供します。

### ステップ 1: Foundry ポータルを開く

1. ブラウザを開き、[https://ai.azure.com](https://ai.azure.com) にアクセスします。
2. ワークショップで使用しているのと同じ Azure アカウントでサインインします。

### ステップ 2: プロジェクトへ移動

1. ホームページの左サイドバーで **Recent projects** を探します。
2. プロジェクト名（例：`workshop-agents`）をクリックします。
3. ない場合は、**All projects** をクリックして検索します。

### ステップ 3: 展開済みエージェントを探す

1. プロジェクトの左ナビゲーションで **Build** → **Agents** （または<strong>Agents</strong>セクション）をクリックします。
2. エージェントの一覧が表示されます。展開済みのエージェント（例：`resume-job-fit-evaluator`）を探します。
3. エージェント名をクリックして詳細ページを開きます。

### ステップ 4: Playground を開く

1. エージェント詳細ページの上部ツールバーを確認します。
2. **Open in playground** （または **Try in playground**）をクリックします。
3. チャットインターフェイスが開きます。

### ステップ 5: 同じスモークテストを実行

上記の VS Code Playground セクションの 3 つのテストをすべて繰り返します。レスポンスをローカル結果（モジュール 5）および VS Code Playground 結果（オプションA）と比較します。

---

## マルチエージェント固有の検証

基本的な正確性以上に、以下のマルチエージェント固有の動作を検証します：

### MCP ツールの実行

| チェック項目 | 検証方法 | 合格条件 |
|-------|---------------|----------------|
| MCP 呼び出しが成功 | ギャップカードに `learn.microsoft.com` の URL がある | フェールバックメッセージではなく実際の URL |
| 複数の MCP 呼び出し | 高/中優先度のギャップごとにリソースがある | 最初のギャップカードだけでない |
| MCP フェールバック処理 | URL が欠落した場合はフェールバックテキストを確認 | URL 有無にかかわらずギャップカードを生成している |

### エージェントの連携

| チェック項目 | 検証方法 | 合格条件 |
|-------|---------------|----------------|
| 全4エージェントが実行済み | 出力にフィットスコアとギャップカードがある | スコアは MatchingAgent、カードは GapAnalyzer 由来 |
| 順次実行 | レスポンスタイムが合理的（2分未満） | 3分超ならターミナルログでエラー確認 |
| データフローの一貫性 | ギャップカードはマッチングレポートのスキルを参照 | JD にない虚偽のスキルなし |

---

## 検証ルーブリック

マルチエージェント ワークフローのホストされた動作を評価するために、このルーブリックを使用します：

| # | 基準 | 合格条件 | 合格? |
|---|----------|---------------|-------|
| 1 | <strong>機能的正確性</strong> | エージェントが履歴書 + JD にフィットスコアとギャップ分析で応答 | |
| 2 | <strong>スコアリングの一貫性</strong> | フィットスコアは100点満点の内訳計算を使用 | |
| 3 | <strong>ギャップカードの完全性</strong> | 欠落スキルごとに1枚（切り捨てや結合なし） | |
| 4 | **MCP ツール統合** | ギャップカードに実際の Microsoft Learn URL が入っている | |
| 5 | <strong>構造の一貫性</strong> | 出力構造がローカルとホスト間で一致している | |
| 6 | <strong>応答時間</strong> | ホストされたエージェントがフル評価を2分以内に応答 | |
| 7 | <strong>エラーなし</strong> | HTTP 500 エラー、タイムアウト、空のレスポンスなし | |

> 「合格」とは、少なくとも一つのプレイグラウンド（VS Code またはポータル）で、3つのスモークテストすべてにおいて7つの基準をすべて満たすことを意味します。

---

## Playground の問題トラブルシューティング

| 症状 | 考えられる原因 | 解決策 |
|---------|-------------|-----|
| Playground が読み込まない | コンテナが `active` 状態でない | [モジュール 6](06-deploy-to-foundry.md) に戻り、展開状況を確認。`creating` 状態なら待機 |
| エージェントが空のレスポンスを返す | モデル展開名の不一致 | `agent.yaml` → `environment_variables` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` が展開モデルと一致するか確認 |
| エージェントがエラーメッセージを返す | [RBAC](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) 権限不足 | プロジェクトスコープで **[Foundry User](https://aka.ms/foundry-ext-project-role)**（旧 Azure AI User）を割り当て |
| ギャップカードに Microsoft Learn URL がない | MCP アウトバウンドがブロックされているか MCP サーバーが利用不可 | コンテナが `learn.microsoft.com` にアクセスできるか確認。詳細は [モジュール 8](08-troubleshooting.md) |
| ギャップカードが1枚のみ（切り捨て） | GapAnalyzer 指示に "CRITICAL" ブロックが不足 | [モジュール 3, ステップ 2.4](03-configure-agents.md) を確認 |
| フィットスコアがローカルと大幅に異なる | 異なるモデルまたは指示が展開されている | `agent.yaml` の環境変数とローカルの `.env` を比較。必要なら再展開 |
| ポータルで「Agent not found」 | 展開がまだ反映中か失敗 | 2分待ってリフレッシュ。まだ見つからなければ [モジュール 6](06-deploy-to-foundry.md) から再展開 |

---

### チェックポイント

- [ ] VS Code Playground でエージェントをテスト - 3つのスモークテストすべて合格
- [ ] [Foundry ポータル](https://ai.azure.com) Playground でエージェントをテスト - 3つのスモークテストすべて合格
- [ ] レスポンスがローカルのテスト結果と構造的に一致（フィットスコア、ギャップカード、ロードマップ）
- [ ] ギャップカードに Microsoft Learn の URL がある（ホスト環境で MCP ツールが動作）
- [ ] 欠落スキルごとに1枚のギャップカード（切り捨てなし）
- [ ] テスト中にエラーやタイムアウトなし
- [ ] 検証ルーブリックの完了（7つの基準すべて合格）

---

**前へ:** [06 - Foundry への展開](06-deploy-to-foundry.md) · **次へ:** [08 - トラブルシューティング →](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->