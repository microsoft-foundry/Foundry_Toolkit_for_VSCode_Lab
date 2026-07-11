# モジュール 8 - トラブルシューティング

このモジュールはよくある問題のリファレンスガイドです。ブックマークして、問題が発生したときに戻ってきてください。

---

## 1. 権限エラー

### 1.1 `agents/write` 権限拒否

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write
```

**原因：** <strong>プロジェクト</strong> レベルで `Azure AI User` ロールが欠落しています。これはワークショップで最も多いエラーです。

**修正方法：**
1. [portal.azure.com](https://portal.azure.com) を開きます。
2. Foundry <strong>プロジェクト</strong> 名を検索 → 種類が **"Microsoft Foundry project"** の結果をクリック（親アカウントではありません）。
3. **アクセス制御 (IAM)** → **+ 追加** → <strong>ロールの割り当てを追加</strong>。
4. ロール：**Azure AI User** → 次へ。
5. メンバー：自分を選択 → レビュー + 割り当て → レビュー + 割り当て。
6. **1～2分待機** → 再試行。

> **なぜ Owner/Contributor では不十分か：** これらのロールは<em>管理</em>アクションのみを付与します。エージェント操作には `agents/write` <em>データアクション</em> が必要で、これは `Azure AI User`、`Azure AI Developer`、または `Azure AI Owner` のみが持ちます。詳細は [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) を参照。

### 1.2 プロビジョニング中の `AuthorizationFailed`

**修正方法：** 管理者にリソースグループに対して **Contributor** を割り当ててもらうか、プロジェクトを作成してもらい、その上に **Azure AI User** を付与してもらいます。

### 1.3 `SubscriptionNotRegistered`

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
# 「登録済み」になるまで待ちます
```

---

## 2. Docker エラー

> Docker は<strong>オプション</strong>です。Docker Desktop がインストールされて拡張機能がローカルビルドを試みる場合のみ適用されます。

### 2.1 Docker デーモンが動作していない

**修正方法：** Docker Desktop を起動 → 「実行中」ステータスになるまで待つ → `docker info` で確認 → 再試行。

### 2.2 依存関係エラーでビルド失敗

**修正方法：** `requirements.txt` のスペルを確認し、まずローカルでテスト：`pip install -r requirements.txt`。

### 2.3 プラットフォーム不一致（Apple Silicon）

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

---

## 3. 認証エラー

### 3.1 `DefaultAzureCredential` が失敗する

**修正方法（順に試す）：**
1. `az login`（再認証）
2. `az account set --subscription "<id>"`（正しいサブスクリプション指定）
3. VS Code → アカウント → サインアウト → 再サインイン
4. 確認：`az account get-access-token --resource https://cognitiveservices.azure.com`

### 3.2 トークンはローカルで有効だがホスト環境で無効

**想定される状況：** ホスト型エージェントはシステム管理の ID（Managed Identity）を使用し、あなたの認証情報は使いません。ホスト型エージェントで認証エラーが出た場合：
- `agent.yaml` の `AZURE_AI_PROJECT_ENDPOINT` が正しいか確認
- プロジェクトのマネージド ID にモデルアクセスがあるか確認

---

## 4. モデルエラー

### 4.1 モデルのデプロイメントが見つからない

**修正方法：** 名前は<strong>大文字・小文字を区別</strong>します。`.env` 内の `AZURE_AI_MODEL_DEPLOYMENT_NAME` と Foundry サイドバー → Models にある正確な名前を比較してください。

### 4.2 予期しないモデル出力

**修正方法：** `main.py` の `AGENT_INSTRUCTIONS` を確認（切れていませんか？）。別のモデル（`gpt-4.1` と `gpt-4.1-mini` など）を試してください。

---

## 5. デプロイメントエラー

### 5.1 ACR プルが未認証

**修正方法：** Azure ポータル → コンテナ レジストリ → アクセス制御 (IAM) → Foundry プロジェクトのマネージド ID に **AcrPull** ロールを追加。

### 5.2 エージェント起動失敗（"Pending" または "Failed" のまま）

サイドバーでコンテナログを確認。一般的な原因：

| ログメッセージ | 修正 |
|-------------|-----|
| `ModuleNotFoundError` | `requirements.txt` に不足パッケージを追加し、再デプロイ |
| `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'` | `agent.yaml` の `environment_variables` に環境変数追加 |
| `Address already in use` | ポート 8088 をバインドするプロセスが一つだけであることを確認 |

### 5.3 デプロイメントがタイムアウトする

**修正方法：** インターネット接続を確認。初回デプロイは >100MB をアップロードします。プロキシ環境の場合は Docker Desktop のプロキシ設定を構成。

---

## 6. パス B - Foundry Local

### 6.1 Foundry Local が起動しない

| 問題 | 修正 |
|-------|-----|
| `foundry: command not found` | 再インストール：`winget install Microsoft.FoundryLocal` |
| リソース不足 | Foundry Local は約4GBの空きRAMが必要。他のアプリを閉じる。 |
| モデルのダウンロード失敗 | ディスク容量を確認（モデルは2〜8GB）。再試行：`foundry local models pull <name>` |

### 6.2 Foundry Local モデルエラー

| 問題 | 修正 |
|-------|-----|
| 反応が遅い | 予想される動作 - ローカルモデルはGPUがなければCPUで動作。気長に待つ。 |
| 出力の品質が悪い | ハードウェアが許せばより大型モデルを試す。`phi-4-mini` はバランスが良い。 |
| 接続拒否 | Foundry Local が起動中か確認：`foundry local status`。必要なら再起動。 |

---

## 7. クイックリファレンス：RBAC ロール

| ロール | スコープ | 権限 |
|------|-------|--------|
| **Azure AI User** | プロジェクト | データアクション：`agents/write`, `agents/read` |
| **Azure AI Developer** | プロジェクト/アカウント | データアクション + プロジェクト作成 |
| **Azure AI Owner** | アカウント | フルアクセス + ロール管理 |
| **Contributor** | サブスクリプション/RG | 管理アクションのみ（データアクション<strong>なし</strong>） |
| **Owner** | サブスクリプション/RG | 管理 + ロール割り当て（データアクション<strong>なし</strong>） |

---

## 8. ワークショップ完了チェックリスト

| # | 項目 | モジュール |
|---|------|--------|
| 1 | 前提条件のインストールと確認 | [00](00-prerequisites.md) |
| 2 | Foundry Toolkit 拡張機能のインストール、プロジェクト接続（またはパス B の設定） | [01](01-setup.md) |
| 3 | ホスト型エージェントのスカフォールド作成 | [02](02-create-hosted-agent.md) |
| 4 | `.env` 設定、指示文作成、依存関係インストール | [03](03-configure-and-code.md) |
| 5 | ローカルでエージェントをテスト - 3つの機能シナリオを通過 | [04](04-test-locally.md) |
| 6 | Foundry へのデプロイ（パス A のみ） | [05](05-deploy-to-foundry.md) |
| 7 | クラウドでのエッジケース/安全性テストを通過（パス A のみ） | [06](06-verify-in-playground.md) |
| 8 | サマリー確認、次のステップの明確化 | [07](07-summary.md) |

---

**前へ：** [07 - サマリー](07-summary.md) · **ホーム：** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->