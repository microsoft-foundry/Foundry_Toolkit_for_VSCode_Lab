# モジュール 7 - まとめと次のステップ

⏱️ 約5分

**おめでとうございます！** Microsoft FoundryとVS Code用Foundry Toolkitを使用して、ホスト型AIエージェントを構築、テストし、（パスAの場合は）デプロイしました。

---

## 作成したもの

「経営幹部向けにわかりやすく説明する」タイプのエージェントで：
- 技術的なインシデント報告や運用アップデートをHTTP経由（`POST /responses`）で受け取る
- それらを平易な経営陣向け要約に翻訳する
- 構造化された出力フォーマット（何が起きたか／ビジネス影響／次のステップ）に従う
- 関連ないリクエストやプロンプトインジェクションの試みを拒否する
- Microsoft Foundryエージェントサービスのコンテナ型ホストエージェントとして動作

---

## 学んだ主要な概念

| コンセプト | 実践したこと |
|---------|-------------------|
| **Agent Frameworkのアーキテクチャ** | `FoundryChatClient` → `Agent` → `ResponsesHostServer` のパイプライン |
| <strong>ホストエージェントのライフサイクル</strong> | 足場作成 → 設定 → ローカルテスト → デプロイ → クラウドで検証 |
| <strong>システムプロンプト設計</strong> | 役割、対象者、出力形式、ルール、安全条件、例示 |
| <strong>ローカルとホストの違い</strong> | ID（個人認証情報 vs 管理ID）、エンドポイント、ネットワーク経路 |
| <strong>安全境界</strong> | プロンプトインジェクション防御、役割遵守、例外処理の適切な対応 |
| **Foundry Toolkitのワークフロー** | プロジェクト作成、モデルデプロイ、エージェント足場作成、Agent Inspector、ワンクリックデプロイ |

---

## 完了したこと

### パスA (Foundryサブスクリプション)

- [x] Foundry Toolkitをセットアップし、デプロイ済みモデルを含むFoundryプロジェクトを作成
- [x] 自動生成されたプロジェクト構成でホスト型エージェントの足場を作成
- [x] 安全ルールを含む構造化されたエージェント指示を書いた
- [x] 3つの機能シナリオでローカルテスト（Agent Inspector）
- [x] Foundry Agent Serviceへ（コンテナ型で）デプロイ
- [x] クラウドプレイグラウンドで4つの例外・安全テストを検証

### パスB (Foundry Local)

- [x] ローカルモデルエンドポイントでFoundry Toolkitをセットアップ
- [x] ホスト型エージェントプロジェクトの足場を作成
- [x] 安全ルールを含む構造化エージェント指示を書いた
- [x] 3つの機能シナリオでローカルテスト
- [x] クラウドリソース不要でエージェント動作を検証

---

## 次のステップ

### 学習を続ける

| リソース | 説明 |
|----------|-------------|
| **[Lab 02 - マルチエージェントオーケストレーション](../../lab02-multi-agent/docs/README.md)** | オーケストレーションパターンによる4エージェントのワークフロー（履歴書→職適性評価）を構築 |
| **[エージェントにツールを追加](https://learn.microsoft.com/azure/foundry/agents/concepts/tool-catalog)** | Tool Catalogを介してAPIやデータベース、カスタム関数と連携 |
| **[知識の追加（RAG）](https://learn.microsoft.com/azure/foundry/agents/concepts/knowledge)** | 文書、ベクトルストア、Bing検索でエージェントの根拠を強化 |
| **[Microsoft Foundryドキュメント](https://learn.microsoft.com/azure/foundry/)** | プラットフォーム全面リファレンス |
| **[Agent Framework SDKリファレンス](https://learn.microsoft.com/agent-framework/)** | `agent-framework`パッケージのAPIドキュメント |
| **[Foundry Toolkit - 新機能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#version-history)** | 拡張機能リリースノートと変更履歴 |

### エージェント拡張のアイデア

- <strong>日付ツールを追加</strong> - 要約に「本日時点での」文脈を含める
- <strong>インシデントデータベースに接続</strong> - ツール機能で実際のインシデント詳細を取得
- **Bingグラウンディングツールを追加** - 最新ニュースを検索し追加の文脈を取得
- <strong>異なるモデルを試す</strong> - `gpt-4.1`と`gpt-4.1-mini`の出力品質を比較
- **Foundryで評価** - 評価機能を利用してエージェント品質を大規模に測定

### パスBユーザー向け：クラウドデプロイにアップグレード

クラウドにデプロイする準備ができたら：
1. Azureサブスクリプションを取得する ([azure.microsoft.com/free](https://azure.microsoft.com/free/))
2. [モジュール 01、セットアップ](01-setup.md#step-2-set-up-based-on-your-access)を完了（プロジェクト作成、モデルデプロイ、RBAC割当）
3. `.env`をFoundryプロジェクトのエンドポイントとモデルデプロイ名に更新
4. [モジュール 05 - Foundryへのデプロイ](05-deploy-to-foundry.md)から続行

---

## リソースのクリーンアップ（任意）

ワークショップ中に作成したAzureリソースを削除したい場合：

### オプション1：リソースグループを削除（すべてを削除）

```bash
az group delete --name rg-hosted-agents-workshop --yes --no-wait
```

### オプション2：ホスト型エージェントのみ削除

1. [ai.azure.com](https://ai.azure.com) → プロジェクト → <strong>ビルド</strong> → <strong>エージェント</strong> を開く。
2. エージェントをクリック → <strong>削除</strong> をクリック。

### オプション3：モデルデプロイメントを削除

1. Foundryサイドバーでプロジェクトを展開 → <strong>モデル</strong>。
2. モデルデプロイメントを右クリック → <strong>削除</strong>。

> **コストに関する注意：** ホスト型エージェントは稼働中のみ課金されます。停止または削除すると継続的な料金は発生しません。モデルデプロイメントは予約容量のためわずかな課金がある可能性があります。不要になったら削除してください。

---

**前へ：** [06 - プレイグラウンドでの検証](06-verify-in-playground.md) · **次へ：** [08 - トラブルシューティング（リファレンス）→](08-troubleshooting.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->