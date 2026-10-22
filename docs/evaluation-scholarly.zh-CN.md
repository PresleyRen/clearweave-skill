# 真实论文与文风测试

[English](evaluation-scholarly.md) · [中文文档中心](README.zh-CN.md)

日期：2026-10-20。运行版本：ClearWeave **0.3.0**。测试输入来自已有公开文本，不是为了测试临时编写的“AI 味”句子。原始文本、作者、许可证、固定版本和 SHA256 都保存在原始测试记录中。

## 数据与角色划分

| 角色 | 来源 | 数量 |
| --- | --- | ---: |
| 领域文风画像 | BERT、Stanza、Dense Passage Retrieval 已发表摘要 | 3 |
| 已发表论文编辑 | Sentence-BERT、scispaCy、SQuAD、Clinical Concept Extraction、Semantic Chain Shifts、Circular Economy | 6 |
| 中文编辑 | HC3-Chinese `open_qa.jsonl` 第 2188、2605 行，`chatgpt_answers[0]` | 2 |

ACL 元数据固定在 `acl-org/acl-anthology@0d4dd55c88a79724914e339ba3511086c05653d0`。用于建立领域画像的三篇文本与实际编辑样本在论文 ID 和完整文本上互不重叠，因此这里建立的是**多作者 NLP 领域画像**，不是某个作者的个人文风。

SQuAD 的 XML 元数据没有摘要。主分支保存了同一篇论文 PDF 第 1 页经过核对的摘要摘录，并保留缺失来源与 PDF 追溯信息。

## 执行过程

当前会话中的助手读取最终模块，使用三篇画像文本作为领域表达参考，对编辑输入进行修改，并执行一次针对性的自检。

Python 工具实际执行了：
- 领域画像测量；
- 原文与修改稿扫描；
- 受保护字面内容对比；
- 风险词与关系变化提示；
- 数据与 runtime 指纹核对；
- 临时项目安装；
- `scan`、`profile`、`compare-profile`、`learn` 四个命令的实际运行。

整个确定性测试集通过 **287 项测试**。这个数字包含程序、fixture 和来源链接测试，不代表 287 次模型改写。

## 实际结果

| 指标 | 结果 |
| --- | ---: |
| 可用于编辑的输入 | 8：6 篇论文 + 2 条中文回答 |
| 实际修改 | 6：4 篇论文 + 2 条中文回答 |
| 保持不变的控制样本 | 2：scispaCy、SQuAD |
| 学术扫描候选 | 5 → 0 |
| 受保护字面内容出现变化的修改稿 | 0 / 6 |
| 触发风险线索的修改稿 | 4 / 6 |
| 文风画像样本 | 3，拥有独立 ID 与哈希 |
| 确定性回归测试 | 287 通过 |

“5 → 0”只表示这组样本中窄规则正则候选的数量变化，不是自然度得分或 AI 概率。“受保护字面内容无变化”也只表示指定字面项一致，不等于完整语义等价。

## 真实修改中的主要变化

### Sentence-BERT

修正了并列主语与关系从句的一致问题，压缩了“发表论文式”开场，并明确网络输入要求。数字和引用保留。

源文最后一个 `it` 的指代仍可能存在歧义。由于缺少完整论文上下文，没有擅自扩大比较结论。

### Clinical Concept Extraction

删除负面结果前的情绪性引导，把实际结果直接陈述出来。“这些概念没有提升文档级临床编码任务表现”的负面结论完整保留。

### Semantic Chain Shifts

把重复叠加的可能性表达合并，同时保留 `may`、可能机制和历史时间范围。

### Circular Economy

删除重复框架表达，并修正主谓一致，同时保留假设和证据陈述。

### scispaCy 与 SQuAD

作为保持原文的控制样本。scispaCy 中承担功能的对照和专业词 `robust` 被保留；SQuAD 保留与人工表现的实质比较、所有数字和原作者的解释。

### HC3 中文

压缩重复描述。第 2605 行在第一次修改后经过自检，恢复了“喜欢”以及明确的另一种可能性。初稿和最终版本都保存在输出记录里，这个语义问题没有被字面检查器捕获。

## 风险线索复核

| 案例 | 线索变化 | 复核结果 |
| --- | --- | --- |
| Sentence-BERT | `requires` → `must / time required`；`causes` → `creating` | 要求关系和因果关系仍保留，但连接表达发生变化 |
| Semantic Chain Shifts | `may possibly` → `may` | 删除重复可能性，仍保留不确定性 |
| HC3 第 2188 行 | “因为” → “因此” | 原文的限制仍作为原因存在；历史事实没有更新 |
| HC3 第 2605 行 | “可能”出现次数增加 | 不同可能性分别表达，没有新增因果结论 |

这些线索全部保留为待复核警告。

## 复现

```bash
python3 tools/evaluate_scholarly.py
python3 tools/evaluate_scholarly.py --download --write
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
```

第一条命令离线回放诊断。`--download` 会重新取得固定公开来源并核对原始 XML / JSONL；SQuAD 的恢复摘录按照已审核记录核对，不会把它伪装成新的 PDF 下载。

查看 [真实修改示例中文版](scholarly-examples.zh-CN.md) · [原始测试记录](../evals/scholarly-2026-10-20/)。

## 许可

ACL 示例论文按 ACL Anthology 对应时期许可使用，当前这些 2016–2020 年示例为 CC BY 4.0。HC3-Chinese 使用 CC BY-SA 4.0。示例是 ClearWeave 的编辑演示，不代表原作者认可这些修改。
