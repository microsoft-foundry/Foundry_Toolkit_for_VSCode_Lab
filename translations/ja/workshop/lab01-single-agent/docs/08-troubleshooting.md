# Module 8 - トラブルシューティング

このモジュールは、ワークショップ中に遭遇するあらゆる一般的な問題のリファレンスガイドです。ブックマークしておいてください—何か問題が起きたときに何度も参照します。

---

## 1. 権限エラー

### 1.1 `agents/write` 権限拒否

```
Error: lacks the required data action 
Microsoft.CognitiveServices/accounts/AIServices/agents/write 
to perform POST /api/projects/{projectName}/assistants operation.
```

**根本原因:** <strong>プロジェクト</strong> レベルで `Azure AI User` ロールを持っていません。これがワークショップで最も一般的なエラーです。

**修正手順:**

1. [https://portal.azure.com](https://portal.azure.com) を開きます。
2. 上部の検索バーに **Foundry プロジェクト** の名前（例: `workshop-agents`）を入力します。
3. **重要:** 「Microsoft Foundry project」タイプの結果をクリックしてください。親アカウントやハブリソースではありません。これらは異なる RBAC スコープを持つ別のリソースです。
4. プロジェクトページの左ナビゲーションで **アクセス制御 (IAM)** をクリックします。
5. <strong>ロールの割り当て</strong> タブをクリックし既にロールがあるか確認します：
   - 自分の名前やメールアドレスを検索します。
   - `Azure AI User` が既にリストにある場合 → エラーの原因は別です（下記ステップ8を参照）。
   - リストにない場合 → 追加します。
6. **+ 追加** → <strong>ロール割り当ての追加</strong> をクリックします。
7. <strong>ロール</strong> タブで：
   - [`Azure AI User`](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry#built-in-roles) を検索します。
   - 結果から選択します。
   - <strong>次へ</strong> をクリックします。
8. <strong>メンバー</strong> タブで：
   - **ユーザー、グループ、またはサービスプリンシパル** を選択します。
   - **+ メンバーの選択** をクリックします。
   - 自分の名前またはメールアドレスを検索します。
   - 結果から自分を選択します。
   - <strong>選択</strong> をクリックします。
9. **レビュー + 割り当て** → 再度 **レビュー + 割り当て** をクリックします。
10. **1〜2分待つ**—RBAC の変更が反映されるまで時間がかかります。
11. 失敗した操作を再実行します。

> **なぜオーナー/共同作成者では足りないのか:** Azure RBAC には、「管理操作」と「データ操作」という2種類の権限があります。オーナーや共同作成者は管理操作（リソースの作成、設定の編集）を許可しますが、エージェント操作は `agents/write` の<strong>データ操作</strong>が必要で、これは `Azure AI User`、`Azure AI Developer`、または `Azure AI Owner` ロールにのみ含まれています。[Foundry RBAC ドキュメント](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry) をご参照ください。

### 1.2 リソース作成時の `AuthorizationFailed`

```
Error: AuthorizationFailed - The client does not have authorization to perform action 
'Microsoft.CognitiveServices/accounts/write'
```

**根本原因:** このサブスクリプションやリソースグループで Azure リソースの作成や変更の権限がありません。

**修正:**
1. サブスクリプション管理者に Foundry プロジェクトが存在するリソースグループに <strong>共同作成者</strong> ロールを割り当ててもらいます。
2. または、管理者に Foundry プロジェクトの作成を依頼し、プロジェクトに対して **Azure AI User** の権限を付与してもらいます。

### 1.3 [Microsoft.CognitiveServices](https://learn.microsoft.com/azure/ai-services/openai/how-to/create-resource) の `SubscriptionNotRegistered`

```
Error: SubscriptionNotRegistered for Microsoft.CognitiveServices
```

**根本原因:** Foundry に必要なリソース プロバイダーが Azure サブスクリプションに登録されていません。

**修正:**

1. ターミナルを開き、以下を実行します：
   ```bash
   az provider register --namespace Microsoft.CognitiveServices
   ```
2. 登録完了まで待つ（1～5分かかることがあります）：
   ```bash
   az provider show --namespace Microsoft.CognitiveServices --query "registrationState"
   ```
   期待される出力: `"Registered"`
3. 操作を再試行します。

---

## 2. Docker エラー（Docker がインストールされている場合のみ）

> Docker はこのワークショップでは <strong>オプション</strong> です。これらのエラーは Docker Desktop がインストールされていて、Foundry 拡張機能がローカルコンテナビルドを試みた場合のみ発生します。

### 2.1 Docker デーモンが起動していない

```
Error: Docker build failed / Cannot connect to Docker daemon
```

**修正手順:**

1. スタートメニュー（Windows）またはアプリケーション（macOS）で **Docker Desktop** を見つけて起動します。
2. Docker Desktop のウィンドウに **「Docker Desktop is running」** が表示されるまで待ちます（通常30～60秒）。
3. システムトレイ（Windows）またはメニューバー（macOS）にある Docker の鯨アイコンを確認し、ステータスをホバーで確認します。
4. ターミナルで確認：
   ```powershell
   docker info
   ```
   ここで Docker のシステム情報（サーバーバージョン、ストレージドライバーなど）が表示されれば、Docker は動作中です。
5. **Windows 固有の手順:** Docker が開始しない場合：
   - Docker Desktop を開き → <strong>設定</strong>（ギアアイコン）→ <strong>全般</strong> に進みます。
   - **WSL 2 ベースのエンジンを使用する** にチェックが入っていることを確認します。
   - <strong>適用して再起動</strong> をクリックします。
   - WSL 2 がインストールされていない場合は、管理者権限の PowerShell で `wsl --install` を実行し、パソコンを再起動してください。
6. 再度展開を試してください。

### 2.2 Docker ビルドが依存関係エラーで失敗する

```
Error: pip install failed / Could not find a version that satisfies the requirement
```

**修正:**
1. `requirements.txt` を開いて、すべてのパッケージ名が正しく綴られているか確認します。
2. バージョンの固定が正しいか確認します：
   ```
   agent-framework-azure-ai==1.0.0rc3
   agent-framework-core==1.0.0rc3
   azure-ai-agentserver-agentframework==1.0.0b16
   azure-ai-agentserver-core==1.0.0b16
   ```
3. まずローカルでインストールを試します：
   ```bash
   pip install -r requirements.txt
   ```
4. プライベートパッケージインデックスを使っている場合は、Docker がそれにアクセスできるネットワーク設定になっているか確認します。

### 2.3 コンテナプラットフォームの不一致（Apple Silicon）

Apple Silicon Mac (M1/M2/M3/M4) から展開する場合、コンテナは `linux/amd64` 用にビルドする必要があります。Foundry のコンテナランタイムは AMD64 を使用しているためです。

```bash
docker build --platform linux/amd64 -t myagent:v1 .
```

> Foundry 拡張機能のデプロイコマンドはほとんどの場合この処理を自動で行います。アーキテクチャ関連のエラーが発生したら、`--platform` フラグを使って手動でビルドし、Foundry チームに連絡してください。

---

## 3. 認証エラー

### 3.1 [`DefaultAzureCredential`](https://learn.microsoft.com/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview) でトークン取得失敗

```
Error: DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**根本原因:** `DefaultAzureCredential` チェーン内のどの認証情報ソースも有効なトークンを持っていません。

**修正 - 順番に試してください:**

1. **Azure CLI で再ログイン**（最もよく効く対処法）：
   ```bash
   az login
   ```
   ブラウザウィンドウが開きます。サインイン後、VS Code に戻ります。

2. **正しいサブスクリプションを設定：**
   ```bash
   az account show --query "{name:name, id:id}" -o table
   ```
   これが正しいサブスクリプションでない場合：
   ```bash
   az account set --subscription "<your-subscription-id>"
   ```

3. **VS Code から再ログイン：**
   - VS Code 左下の <strong>アカウント</strong> アイコン（人型）をクリック。
   - 自分のアカウント名をクリックし → <strong>サインアウト</strong>。
   - 再びアカウントアイコンをクリック → **Microsoft にサインイン**。
   - ブラウザでのサインイン手続きを完了します。

4. **サービスプリンシパル（CI/CD シナリオのみ）：**
   - `.env` に以下の環境変数を設定します：
     ```
     AZURE_TENANT_ID=<your-tenant-id>
     AZURE_CLIENT_ID=<your-client-id>
     AZURE_CLIENT_SECRET=<your-client-secret>
     ```
   - その後、エージェントプロセスを再起動してください。

5. **トークンキャッシュを確認：**
   ```bash
   az account get-access-token --resource https://cognitiveservices.azure.com
   ```
   これが失敗する場合、CLI のトークンが期限切れです。再度 `az login` を実行してください。

### 3.2 ローカルではトークンが有効だがホスト展開で失敗する

**根本原因:** ホスト型エージェントはシステム管理のマネージドIDを使用し、個人の認証情報とは異なります。

**修正:** これは正常動作です—マネージドIDは配備時に自動的に作成されます。ホスト型エージェントで認証エラーが続く場合：
1. Foundry プロジェクトのマネージド ID が Azure OpenAI リソースにアクセスできるか確認します。
2. `agent.yaml` 内の `PROJECT_ENDPOINT` が正しいか検証してください。

---

## 4. モデル関連エラー

### 4.1 モデル展開が見つからない

```
Error: Model deployment not found / The specified deployment does not exist
```

**修正手順:**

1. `.env` ファイルを開き、`AZURE_AI_MODEL_DEPLOYMENT_NAME` の値を確認します。
2. VS Code の **Microsoft Foundry** サイドバーを開きます。
3. プロジェクトを展開し → **Model Deployments** を開きます。
4. 画面に表示されている展開名と `.env` の値を比較します。
5. 名前は <strong>大文字小文字を区別</strong> します—`gpt-4o` と `GPT-4o` は別物です。
6. 一致しない場合は、サイドバー表示の正確な名前に `.env` を更新します。
7. ホストデプロイの場合は `agent.yaml` も更新してください：
   ```yaml
   env:
     - name: MODEL_DEPLOYMENT_NAME
       value: "<exact-deployment-name>"
   ```

### 4.2 モデルの応答内容が予期しない

**修正:**
1. `main.py` 内の `EXECUTIVE_AGENT_INSTRUCTIONS` 定数をレビューし、途中で切れていないか破損していないか確認します。
2. モデルの temperature 設定（変更可能なら）を確認—低い値ほど決定論的な出力になります。
3. デプロイしているモデル（例：`gpt-4o` と `gpt-4o-mini`）を比べ、各モデルの能力差を考慮してください。

---

## 5. デプロイ関連エラー

### 5.1 ACR のプル権限エラー

```
Error: AcrPullUnauthorized
```

**根本原因:** Foundry プロジェクトのマネージド ID が Azure Container Registry からコンテナイメージをプルする権限を持っていません。

**修正手順:**

1. [https://portal.azure.com](https://portal.azure.com) を開きます。
2. 上部の検索バーで **[コンテナレジストリ](https://learn.microsoft.com/azure/container-registry/container-registry-intro)** を検索します。
3. Foundry プロジェクトに関連付けられたレジストリをクリックします（通常は同じリソースグループ内）。
4. 左のナビゲーションで **アクセス制御 (IAM)** をクリックします。
5. **+ 追加** → <strong>ロール割り当ての追加</strong> をクリックします。
6. **[AcrPull](https://learn.microsoft.com/azure/container-registry/container-registry-roles)** を検索して選択し、<strong>次へ</strong> をクリックします。
7. **マネージドID** を選択 → **+ メンバーの選択** をクリックします。
8. Foundry プロジェクトのマネージド ID を検索して選択します。
9. <strong>選択</strong> → **レビュー + 割り当て** → 再度 **レビュー + 割り当て** をクリックします。

> 通常このロール割り当ては Foundry 拡張機能が自動で行います。このエラーが表示された場合は、自動セットアップが失敗しているかもしれません。再デプロイを試すと、拡張機能が再試行する場合があります。

### 5.2 デプロイ後にエージェントが起動しない

**症状:** コンテナステータスが 5 分以上「Pending」のまま、または「Failed」と表示される。

**修正手順:**

1. VS Code の **Microsoft Foundry** サイドバーを開きます。
2. ホスト型エージェントをクリックし → バージョンを選択します。
3. 詳細パネルの <strong>コンテナ詳細</strong> → <strong>ログ</strong> セクションまたはリンクを探します。
4. コンテナ起動ログを読みます。よくある原因：

| ログメッセージ | 原因 | 修正 |
|-------------|-------|-----|
| `ModuleNotFoundError: No module named 'xxx'` | 依存関係の欠如 | `requirements.txt` に追加して再デプロイ |
| `KeyError: 'PROJECT_ENDPOINT'` | 環境変数不足 | `agent.yaml` の `env:` に追加 |
| `OSError: [Errno 98] Address already in use` | ポート競合 | `agent.yaml` で `port: 8088` を設定し、同一ポートに複数プロセスがバインドされていないか確認 |
| `ConnectionRefusedError` | エージェントがリッスンを開始していない | `main.py` の `from_agent_framework()` の呼び出しが起動時に行われているか確認 |

5. 問題を修正し、[Module 6](06-deploy-to-foundry.md) から再デプロイしてください。

### 5.3 デプロイがタイムアウトする

**修正:**
1. インターネット接続を確認してください—Docker プッシュは大きくなることがあります（初回デプロイ時は100MB超）。
2. 会社のプロキシ環境下にいる場合は、Docker Desktop のプロキシ設定を正しく構成してください：**Docker Desktop** → <strong>設定</strong> → <strong>リソース</strong> → <strong>プロキシ</strong>。
3. もう一度試してください—ネットワークの一時的な問題で失敗することがあります。

---

## 6. クイックリファレンス：RBAC ロール

| ロール | 典型的スコープ | 付与される権限 |
|--------|----------------|----------------|
| **Azure AI User** | プロジェクト | データ操作：エージェントのビルド、デプロイ、呼び出し (`agents/write`, `agents/read`) |
| **Azure AI Developer** | プロジェクトまたはアカウント | データ操作 + プロジェクト作成 |
| **Azure AI Owner** | アカウント | フルアクセス + ロール割り当て管理 |
| **Azure AI Project Manager** | プロジェクト | データ操作 + 他者への Azure AI User 割り当て権限 |
| **Contributor** | サブスクリプション/リソースグループ | 管理操作（リソース作成/削除）<strong>データ操作は含まない</strong> |
| **Owner** | サブスクリプション/リソースグループ | 管理操作 + ロール割り当て。<strong>データ操作は含まない</strong> |
| **Reader** | どこでも | 読み取り専用の管理アクセス |

> **重要:** `Owner` と `Contributor` にはデータ操作権限は含まれません。エージェント操作には必ず `Azure AI *` ロールが必要です。このワークショップの最小ロールは <strong>プロジェクト</strong> スコープでの **Azure AI User** です。

---

## 7. ワークショップ完了チェックリスト

すべて完了したことを最終確認するために使ってください：

| No. | 項目 | モジュール | 完了? |
|-----|------|------------|-------|
| 1 | すべての前提条件のインストールと検証 | [00](00-prerequisites.md) | |
| 2 | Foundry ツールキットと Foundry 拡張機能のインストール | [01](01-install-foundry-toolkit.md) | |
| 3 | Foundry プロジェクトの作成（または既存プロジェクトの選択） | [02](02-create-foundry-project.md) | |
| 4 | モデルがデプロイされている（例：gpt-4o） | [02](02-create-foundry-project.md) | |
| 5 | プロジェクト範囲で Azure AI ユーザー ロールが割り当てられている | [02](02-create-foundry-project.md) | |
| 6 | ホステッド エージェント プロジェクトがスキャフォールドされている（agent/） | [03](03-create-hosted-agent.md) | |
| 7 | `.env` に PROJECT_ENDPOINT と MODEL_DEPLOYMENT_NAME が設定されている | [04](04-configure-and-code.md) | |
| 8 | main.py 内でエージェントの指示がカスタマイズされている | [04](04-configure-and-code.md) | |
| 9 | 仮想環境が作成され依存関係がインストールされている | [04](04-configure-and-code.md) | |
| 10 | F5 またはターミナルでローカルテストが行われている（4つのスモークテストが合格） | [05](05-test-locally.md) | |
| 11 | Foundry Agent Service にデプロイされている | [06](06-deploy-to-foundry.md) | |
| 12 | コンテナのステータスが「Started」または「Running」と表示されている | [06](06-deploy-to-foundry.md) | |
| 13 | VS Code Playground で検証済み（4つのスモークテストが合格） | [07](07-verify-in-playground.md) | |
| 14 | Foundry Portal Playground で検証済み（4つのスモークテストが合格） | [07](07-verify-in-playground.md) | |

> **おめでとうございます！** すべての項目にチェックが付いていれば、ワークショップは完了です。ホステッド エージェントをゼロから構築し、ローカルでテストし、Microsoft Foundry にデプロイし、本番環境で検証しました。

---

**前へ:** [07 - Verify in Playground](07-verify-in-playground.md) · **ホーム:** [Workshop README](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**:  
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な箇所が含まれる場合があることをご了承ください。原文はその言語において正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の使用により生じた誤解や解釈の相違について、当方は一切の責任を負いません。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->