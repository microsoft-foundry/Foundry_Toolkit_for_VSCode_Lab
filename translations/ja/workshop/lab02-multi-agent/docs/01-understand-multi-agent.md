# モジュール 1 - アーキテクチャの理解

⏱️ 約5分

コードを書く前に、何を作っているのか、どのように動作するのかを簡単に説明します。

---

## 作成するもの

<strong>履歴書</strong>と<strong>職務内容</strong>を貼り付けます。ワークフローは次のものを返します：

- 適合スコア（0～100、内訳付き）
- スキルおよび資格のギャップ一覧
- 各ギャップに対応したMicrosoft Learnリンク付きのパーソナライズされた学習ロードマップ

---

## 4つのエージェント

一人のエージェントが解析、スコアリング、計画を同時に行おうとすると、雑で浅い結果になりがちです。作業を4つの専門的なエージェントに分割すると、より良い結果が得られます：

| エージェント | 役割 |
|-------------|---------|
| **ResumeParser** | 履歴書を解析し、職務内容をそのまま`[JOB DESCRIPTION PASS-THROUGH]`にコピーして下流のエージェントに渡す |
| **JobDescriptionAgent** | パススルーからJD要件を抽出し、`[PARSED RESUME]`を`[PARSED RESUME PASS-THROUGH]`として伝達 |
| **MatchingAgent** | 両方の注釈付きセクションを比較し、0～100の適合スコアとギャップリストを作成 |
| **GapAnalyzer** | 学習ロードマップを構築し、各ギャップに対してMicrosoft Learnを検索 |

---

## オーケストレーショングラフ

ワークフローは<strong>逐次パイプライン</strong>で、各エージェントが出力を次に渡します：

```mermaid
flowchart LR
    A["ユーザー入力"] --> B["履歴書パーサー"]
    B -- "解析された履歴書＋職務記述リレー" --> C["職務記述エージェント"]
    C -- "職務記述の要件＋履歴書リレー" --> D["マッチングエージェント"]
    D -- "適合レポート＋ギャップ" --> E["ギャップ分析＋MCP"]
    E --> F["最終出力"]

    style A fill:#4A90D9,color:#fff
    style B fill:#7B68EE,color:#fff
    style C fill:#7B68EE,color:#fff
    style D fill:#E67E22,color:#fff
    style E fill:#27AE60,color:#fff
    style F fill:#4A90D9,color:#fff
```

1. <strong>ResumeParser</strong>がユーザー入力を受け取り、履歴書を解析し、JDを`[JOB DESCRIPTION PASS-THROUGH]`にコピーします。
2. <strong>JD Agent</strong>が構造化された要件を抽出し、`[PARSED RESUME PASS-THROUGH]`を伝達します。
3. <strong>MatchingAgent</strong>が両方のセクションを比較し、適合スコアとギャップリストを作成します。
4. <strong>GapAnalyzer</strong>がロードマップを構築し、各ギャップに対してMicrosoft Learn MCPツールを呼び出します。

---

## これがコードにどうマッピングされるか

`main.py`でこのグラフを`WorkflowBuilder`で記述します：

```python
workflow_agent = (
    WorkflowBuilder(
        start_executor=resume_executor,       # ユーザー入力を最初に受け取るエージェント
        output_executors=[gap_executor],      # 最後のエージェント - その出力が応答となる
    )
    .add_edge(resume_executor, jd_executor)       # ResumeParser → JDエージェント
    .add_edge(jd_executor, matching_executor)     # JDエージェント → MatchingAgent
    .add_edge(matching_executor, gap_executor)    # MatchingAgent → GapAnalyzer
    .build()
    .as_agent()
)
```

各`Agent`は`AgentExecutor`でラップされています。`add_edge()`呼び出しは厳密な逐次パイプラインを定義し、各エージェントは直接の前任者の出力のみを受け取ります。

> `context_mode="last_agent"`は各エグゼキューターが直接の前任者の出力だけを見ることを意味します。ResumeParserとJD Agentはラベル付きセクションでデータを順にリレーするので、下流の各エージェントは必要なデータだけを正確に受け取れます。

---

## MCPツール

GapAnalyzerには1つのツールがあります：`search_microsoft_learn_for_plan`。これは`https://learn.microsoft.com/api/mcp`に接続し、各スキルギャップに対して実際のMicrosoft Learnリンクを返します。

ツールが実行されると、これらのログが表示されます — 全て期待されるものです：

```
GET  https://learn.microsoft.com/api/mcp → 405   ← connection probe, normal
POST https://learn.microsoft.com/api/mcp → 200   ← actual tool call
DELETE https://learn.microsoft.com/api/mcp → 405 ← cleanup probe, normal
```

`POST`がエラーを返す場合のみ注意してください。

---

**前へ：** [00 - 前提条件](00-prerequisites.md) · **次へ：** [02 - プロジェクトのスキャフォールド →](02-scaffold-multi-agent.md)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：
本書類は AI 翻訳サービス [Co-op Translator](https://github.com/Azure/co-op-translator) を使用して翻訳されています。正確性を期していますが、自動翻訳には誤りや不正確な部分が含まれる可能性があることをご承知おきください。原文の原語版が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や解釈違いについても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->