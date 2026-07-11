# このセッションの配信方法

セッションの配信ありがとうございます！

ワークショップを配信する前に、以下をお願いします：

1. このドキュメントおよび含まれるすべてのリソースを全文お読みください。
2. セッション配信の録画とワークショップのエンドツーエンドのウォークスルーを視聴してください。
3. 両方のハンズオンラボをイベント前に <strong>少なくとも一度</strong> 自分のマシンでエンドツーエンドで実施してください。
4. Microsoft Foundry プロジェクト、モデル展開、およびクォータを検証してください。
5. わからないことがあれば、メンテナーに連絡してください。

---

## ファイル概要

| リソース                       | リンク                                                                             | 説明                                                                                |
|-------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| ワークショップのスライドデッキ   | [Workshop Deck](../../../session-delivery-resources/foundry-toolkit-deck.pptx)                                               | プレゼンテーションスライド（発表者ノートおよび埋め込みデモビデオ含む）                   |
| セッション配信録画             | _メンテナーから提供予定_                                                               | ワークショップのイントロおよびスライドのウォークスルー録画                              |
| ワークショップエンドツーエンド録画 | _メンテナーから提供予定_                                                               | 両方のラボを学習者視点で継続的に実施した録画                                           |
| ワークショップドキュメント       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab) | ソースリポジトリ、ラボのREADME、段階的なモジュール                                       |
| ラボ01 - シングルエージェント      | [Lab 01](../workshop/lab01-single-agent/README.md)                               | ハンズオンラボ：*Explain Like I'm an Executive* ホスト型エージェントの構築、テスト、展開   |
| ラボ02 - マルチエージェントワークフロー | [Lab 02](../workshop/lab02-multi-agent/README.md)                                | ハンズオンラボ：4エージェントの *Resume to Job Fit Evaluator* ワークフローの構築         |
| デモ1：エグゼクティブエージェント   | [Lab01 agent](../../../workshop/lab01-single-agent/agent)                                              | ラボ01デモ：技術用語を経営陣向け要約に翻訳                                               |
| デモ2：Resume to Job Fit Evaluator | [PersonalCareerCopilot](../../../workshop/lab02-multi-agent/PersonalCareerCopilot)                     | ラボ02デモ：履歴書適合度を評価し推奨を生成する4エージェントワークフロー               |

> **トレーナー向けメモ：** スライドデッキおよびビデオリンクは録画公開後に追加予定です。それまでの間は最新の資産についてはメンテナーに問い合わせてください（[Contacts](#連絡先)参照）。

---

## 開始方法

このワークショップでは、開発者が VS Code から **Microsoft Foundry Toolkit** 拡張機能を使って、**Microsoft Foundry Agent Service** に **Hosted Agents** としてAIエージェントを構築、テスト、展開する方法を学びます。

ワークショップはスライド、**2つのライブデモ**、および **2つのハンズオンラボ** に分かれています。

### タイムスケジュール

#### フル配信（約2時間）

| 時間             | 内容                                                                |
|-----------------|----------------------------------------------------------------------|
| 0:00 - 10:00    | イントロ：Hosted Agents、Foundry Agent Service、ツールキットの説明         |
| 10:00 - 20:00   | デモ：エグゼクティブエージェントのエンドツーエンド実演                    |
| 20:00 - 60:00   | ラボ01 - シングルエージェント（ビルド、ローカルテスト、展開、プレイグラウンド） |
| 60:00 - 110:00  | ラボ02 - マルチエージェントワークフロー（Resume to Job Fit Evaluator）    |
| 110:00 - 120:00 | まとめ、Q&A、継続学習リソースの案内                                     |

#### 短縮配信（約75分）

| 時間           | 内容                                                          |
|---------------|--------------------------------------------------------------|
| 0:00 - 10:00  | イントロおよび概要                                           |
| 10:00 - 20:00 | デモ：エグゼクティブエージェント                            |
| 20:00 - 70:00 | ラボ01のみ（ラボ02は自習を案内）                             |
| 70:00 - 75:00 | まとめとQ&A                                                  |

### 事前準備

| リソース                       | リンク                                                                                          | 説明                                       |
|--------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------|
| ワークショップドキュメント       | [Repository](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab)             | ワークショップのドキュメントとソース                 |
| ラボ01 手順書                  | [lab01-single-agent](../workshop/lab01-single-agent/README.md)                                | ハンズオンラボ：シングルホストエージェント           |
| ラボ02 手順書                  | [lab02-multi-agent](../workshop/lab02-multi-agent/README.md)                                  | ハンズオンラボ：マルチエージェントワークフロー       |
| 必要条件チェックリスト          | [00-prerequisites.md](../workshop/lab01-single-agent/docs/00-prerequisites.md)                | 必要なツール、アカウント、Azureアクセス               |
| Hosted agents クイックスタート（azd） | [Learn](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) | `azd` を使ったホスト型エージェント展開の公式クイックスタート |
| Hosted agents 対応リージョン      | [Learn](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability) | ホスト型エージェントの対応リージョン（プレビュー）     |

### トレーナーの必須条件

配信前に以下を確認してください：

- リソース作成権限（オーナーまたはリソースグループにおけるコントリビューター権限）を持つ<strong>Azureサブスクリプション</strong>。
- [ホスト型エージェントをサポートするリージョン](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)にある<strong>Microsoft Foundry プロジェクト</strong>へのアクセス。
- Foundry プロジェクトで **gpt-4.1**（または **gpt-4.1-mini**）のクォータを保有。
- 以下のツールをインストール済み：
  - [Visual Studio Code](https://code.visualstudio.com/)
  - [Microsoft Foundry Toolkit 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
  - [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
  - [Azure Developer CLI（`azd`）](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
  - [Docker Desktop](https://www.docker.com/)（任意）
  - Python 3.10 以上

配信前に必ず [Hosted agents クイックスタート（azd）](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) を一度実施して、問題なく動作する Foundry プロジェクト、モデル展開、Azure Container Registry を持っておくようにしてください。学習者が詰まった場合に参照用となります。

---

## スライドウォークスルー

スライドの流れはラボと同じです。各セクションの推奨説明ポイント：

| セクション                  | 重要メッセージ                                                                                           |
|-----------------------------|----------------------------------------------------------------------------------------------------------|
| タイトルとアジェンダ        | ポータルを切り替えずに *VS Code から Foundry* への流れとしてワークショップを位置づける。                  |
| なぜHosted Agentsか？       | マネージドランタイム、ACRベースの展開、OpenAI互換の `/responses` API 、Foundryプロジェクトにスコープ。    |
| アーキテクチャ図            | [READMEアーキテクチャ](../README.md#architecture)を説明：スキャフォールド、Inspector、ACR、Agent Service。|
| ホスト型エージェントの構成   | `agent.yaml`、`Dockerfile`、`main.py`、`requirements.txt` の役割を説明。                                   |
| ライブデモ：エグゼクティブエージェント | VS Code に切り替えて [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) のデモをエンドツーエンドで実演（[Demo 1](#デモ-1：エグゼクティブエージェント)参照）。           |
| ライブデモ：Resume to Job Fit Evaluator | VS Code に切り替えて [`PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) の4エージェントデモを実行（[Demo 2](#デモ-2：resume-to-job-fit-evaluator)参照）。  |
| ラボ01説明                  | 学習者に作業を渡す。[`workshop/lab01-single-agent/README.md`](../workshop/lab01-single-agent/README.md)を案内。 |
| マルチエージェントパターン   | 逐次実行、同時実行、ハンドオフの説明。ラボ02開始前にプレビュー。                                  |
| ラボ02説明                  | 学習者に作業を渡す。[`workshop/lab02-multi-agent/README.md`](../workshop/lab02-multi-agent/README.md)を案内。 |
| まとめとリソース            | [Additional resources](#追加リソース) セクションから継続学習のリンクを案内。                      |

---

## デモ

配信には2つのライブデモが含まれます。各10分程度を割り当ててください。

| デモ | ラボ | ファイル | 内容説明 |
|------|-----|-------|--------------|
| エグゼクティブエージェント | ラボ01 | [`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) | シングルホスト型エージェント；専門用語を経営陣向け要約に変換 |
| Resume to Job Fit Evaluator | ラボ02 | [`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) | 4エージェントオーケストレーション；履歴書適合度スコアと推奨を生成 |

### デモ 1：エグゼクティブエージェント

[`workshop/lab01-single-agent/agent/`](../../../workshop/lab01-single-agent/agent) にある単独エージェント。ラボ01の前に10分間のデモとして使用。

1. [`workshop/lab01-single-agent/agent/main.py`](../../../workshop/lab01-single-agent/agent/main.py) を開き、エージェント定義（システムプロンプト、モデル、フレームワーク）を説明。
2. `F5` を押して **Agent Inspector** をローカルで起動。
3. [README](../README.md#see-it-in-action) のサンプルプロンプトを貼り付けて、経営陣向け要約レスポンスを表示。
4. [`workshop/lab01-single-agent/agent/agent.yaml`](../../../workshop/lab01-single-agent/agent/agent.yaml) と [`workshop/lab01-single-agent/agent/Dockerfile`](../../../workshop/lab01-single-agent/agent/Dockerfile) を表示して展開成果物を説明。
5. 展開の流れ（Dockerビルド、ACRプッシュ、ホスト型エージェント作成）を完了待たずに実演。

### デモ 2：Resume to Job Fit Evaluator

[`workshop/lab02-multi-agent/PersonalCareerCopilot/`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot) にある4エージェントワークフロー。ラボ02の前に10分間のデモに使用。

1. [`PersonalCareerCopilot/main.py`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/main.py) を開き、4つのエージェントが逐次オーケストレーションでどのように連携しているか説明。
2. `F5` を押してマルチエージェントワークフローの **Agent Inspector** を起動。
3. インスペクターチャットに短い求人説明文とサンプル履歴書を貼り付け。
4. 4エージェントのパイプライン（履歴書解析、求人要件抽出、適合度スコアリング、推奨文作成）を説明。
5. 各サブエージェントの出力が次のエージェントのコンテキストになる流れを示し、ハンドオフパターンを強調。
6. [`PersonalCareerCopilot/agent.yaml`](../../../workshop/lab02-multi-agent/PersonalCareerCopilot/agent.yaml) を示して、デモ1のシングルエージェント版と比較。

---

## 配信のヒント

- **早めに期待値を設定しましょう。** Hosted agents はプレビュー段階のため、リージョン制限やクォータを最初に説明し、ラボ途中で驚かせないようにします。
- **まず必須条件のタスクを実行させましょう。** 両ラボには `Validate prerequisites` の VS Code タスクが付属しているので、コードを書く前に参加者に実行させます。
- **Agent Inspector を常に見える状態にしておきましょう。** 多くの「なるほど」体験は、ローカルの `/responses` ラウンドトリップが点灯するときに起こります。
- **バックアップ用のプロジェクトを用意しましょう。** 学習者の Foundry プロジェクトがクォータ上限に達した場合、展開ステップで部屋を止めないために、事前用意済みプロジェクトを共有します。
- **参加者をペアにしましょう。** ラボ02（マルチエージェント）は、オーケストレーションについてパートナーと話し合えると格段に容易になります。
- **ドキュメントのモジュールをチェックポイントとして使いましょう。** 各ラボの `docs/` フォルダーは番号付き8モジュールに分かれており、自然な休憩ポイントになります。
- **共有ラボマシンでベースDockerイメージを事前プルしておき、レジストリのレートリミットを回避しましょう。**

---

## 配信中のトラブルシューティング

| 症状                                         | 最初に試すこと                                                                                       |
|----------------------------------------------|----------------------------------------------------------------------------------------------------|
| Agent Inspectorが接続できない                 | ポート`8088`が空いていること、`Run Lab01 HTTP Server` / `Run Lab02 HTTP Server` タスクが実行中か確認。   |
| デバッガーがアタッチできない                   | ポート `5679` が空いているか確認。`debugpy` がすでにバインド済の場合、VS Code を再起動。            |
| `azd up` が認証エラーで失敗                    | `az login` と `azd auth login` を実行し、正しいテナントが選択されていることを確認。                |
| ACRプッシュで展開が止まる                      | Docker Desktop が起動中か、ユーザーがレジストリで `AcrPush` 権限を持つか確認。                    |
| モデルが404 / deployment-not-foundエラーを返す | `agent.yaml` のモデル展開名が Foundry プロジェクトの展開名と一致しているか確認。                    |

| `Provisioning` に詰まったホスト型エージェント         | プロジェクトのリージョンが[ホスト型エージェントをサポートしている](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#region-availability)ことと、クォータが利用可能であることを確認してください。 |
| Playgroundが401を返す                       | VS CodeのアクティビティバーからFoundry拡張機能を再認証してください。                                     |

より詳しいガイダンスについては、全てのラボにそれぞれ`08-troubleshooting.md`ドキュメントが付属しています。受講者に案内してください：

- ラボ01: [`workshop/lab01-single-agent/docs/08-troubleshooting.md`](../workshop/lab01-single-agent/docs/08-troubleshooting.md)
- ラボ02: [`workshop/lab02-multi-agent/docs/08-troubleshooting.md`](../workshop/lab02-multi-agent/docs/08-troubleshooting.md)

---

## このセッションのカスタマイズ

ワークショップは受講者に合わせて適宜調整してください。よくあるバリエーションは以下の通りです：

- **バックエンド向け受講者:** `agent.yaml`、Docker、ACRに時間を多めに割き、playgroundのデモを縮小します。
- **シチズン・デベロッパー向け:** Foundry拡張機能のUIでのスキャフォールディングに留め、CLIの手順を減らします。
- **60分の単一トラック枠:** 導入、デモ、ラボ01のみを実施します。
- **ワークショップのみ（スライドなし）形式:** 両方のラボのREADMEを開き、それらを主なスクリプトとして使用します。

ラボを拡張する場合は、他のトレーナーにも役立つようPRで変更を共有してください。

---

## 追加リソース

- [Microsoft Foundryドキュメント](https://learn.microsoft.com/azure/ai-foundry/)
- [ホスト型エージェント概要](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [クイックスタート：初めてのホスト型エージェントをデプロイ（`azd`）](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd)
- [ホスト型エージェントをデプロイする方法](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Microsoft Agent Framework](https://github.com/microsoft/agents)
- [Microsoft Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)

---

## 連絡先

このセッションの提供に関して質問がある場合は、[ワークショップリポジトリ](https://github.com/microsoft-foundry/Foundry_Toolkit_for_VSCode_Lab/issues)にイシューを開き、メンテナにタグを付けてください。

| 役割                | 名前           | GitHub                                                  |
|---------------------|----------------|---------------------------------------------------------|
| メンテナ / 連絡先  | Shivam Goyal   | [@ShivamGoyal03](https://github.com/ShivamGoyal03)      |

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->