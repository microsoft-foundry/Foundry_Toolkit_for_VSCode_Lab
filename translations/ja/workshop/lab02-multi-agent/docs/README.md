# Lab 02 - マルチエージェントワークフロー：履歴書 → ジョブ適合性評価

## フルラーニングパス

このドキュメントでは、**WorkflowBuilder** を使ってオーケストレーションされた4つの専門エージェントによる履歴書とジョブの適合性を評価する <strong>マルチエージェントワークフロー</strong> の構築、テスト、デプロイ方法を案内します。

> **前提条件：** Lab 02を開始する前に [Lab 01 - シングルエージェント](../../lab01-single-agent/README.md) を完了してください。

---

## モジュール

| # | モジュール | 内容 |
|---|------------|------|
| 0 | [前提条件](00-prerequisites.md) | Lab 01の完了確認、マルチエージェントの概念理解 |
| 1 | [マルチエージェントアーキテクチャの理解](01-understand-multi-agent.md) | WorkflowBuilder、エージェントの役割、オーケストレーショングラフの学習 |
| 2 | [マルチエージェントプロジェクトのスキャフォールド](02-scaffold-multi-agent.md) | Foundry拡張機能を使ったマルチエージェントワークフローのスキャフォールド |
| 3 | [エージェントと環境の設定](03-configure-agents.md) | 4つのエージェントへの指示作成、MCPツールの設定、環境変数の定義 |
| 4 | [オーケストレーションパターン](04-orchestration-patterns.md) | 並列ファンアウト、直列集約、代替パターンの検討 |
| 5 | [ローカルテスト](05-test-locally.md) | Agent InspectorでF5デバッグ、履歴書＋勤務地情報でスモークテスト実行 |
| 6 | [Foundryへのデプロイ](06-deploy-to-foundry.md) | コンテナビルド、ACRへプッシュ、ホストエージェント登録 |
| 7 | [Playgroundで検証](07-verify-in-playground.md) | VS CodeとFoundryポータルのPlaygroundで展開済みエージェントをテスト |
| 8 | [トラブルシューティング](08-troubleshooting.md) | 一般的なマルチエージェントの問題解決（MCPエラー、出力切り捨て、パッケージバージョン） |

---

## 推定所要時間

| 経験レベル | 時間 |
|------------|------|
| 最近Lab 01を完了 | 45-60分 |
| 多少のAzure AI経験あり | 60-90分 |
| マルチエージェント初体験 | 90-120分 |

---

## アーキテクチャ概要

```
    User Input (Resume + Job Description)
                   │
              ┌────┴────┐
              ▼         ▼
         Resume       Job Description
         Parser         Agent
              └────┬────┘
                   ▼
             Matching Agent
                   │
                   ▼
             Gap Analyzer
             (+ MCP Tool)
                   │
                   ▼
          Final Output:
          Fit Score + Roadmap
```

---

**戻る:** [Lab 02 README](../README.md) · [ワークショップホーム](../../../README.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：  
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性の向上に努めておりますが、自動翻訳は誤りや不正確な箇所を含む可能性があることをご承知おきください。原文はその母語版が正本とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の使用に伴う誤解や誤訳について、当方は一切責任を負いません。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->