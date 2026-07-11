# ラボ 02 - マルチエージェント ワークフロー: 履歴書 → 職務適合評価

## 学習パス全体

このドキュメントは、**WorkflowBuilder** を介してオーケストレーションされる4つの専門エージェントを用いて履歴書と職務の適合性を評価する<strong>マルチエージェント ワークフロー</strong>の構築、テスト、およびデプロイ方法を順に解説します。

> **前提条件:** ラボ 02 を始める前に [Lab 01 - Single Agent](../../lab01-single-agent/README.md) を完了してください。

---

## モジュール

| # | モジュール | 内容 |
|---|--------|---------------|
| 0 | [導入](00-prerequisites.md) | 作成内容、ラボ 01 の確認、ラボ 02 とラボ 01 の比較 |
| 1 | [マルチエージェント アーキテクチャの理解](01-understand-multi-agent.md) | WorkflowBuilder、エージェントの役割、オーケストレーショングラフの学習 |
| 2 | [マルチエージェント プロジェクトのスキャフォールド](02-scaffold-multi-agent.md) | Foundry 拡張ウィザードで基本プロジェクトをスキャフォールド |
| 3 | [エージェントと環境設定](03-configure-agents.md) | 4つのエージェントの指示を書き、MCPツールを設定、環境変数をセット |
| 4 | [オーケストレーション パターン](04-orchestration-patterns.md) | 逐次チェーン、コンテンツリレー、WorkflowBuilder の OR セマンティクス |
| 5 | [ローカルテスト](05-test-locally.md) | Agent Inspector で F5 デバッグ、履歴書＋求人票でスモークテスト実行 |
| 6 | [Foundry へデプロイ](06-deploy-to-foundry.md) | コンテナをビルドし、ACRにプッシュ、ホストエージェントを登録 |
| 7 | [Playground で検証](07-verify-in-playground.md) | VS Code と Foundry ポータルのプレイグラウンドでデプロイ済エージェントをテスト |
| 8 | [トラブルシューティング](08-troubleshooting.md) | 一般的なマルチエージェントの問題（MCPエラー、出力切断、パッケージバージョン）を修正 |
| 9 | [まとめと次のステップ](09-summary.md) | 作成内容、習得した主要概念、クリーンアップ、次の進むべき道 |

---

**戻る:** [Lab 02 README](../README.md) · [ワークショップ ホーム](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->