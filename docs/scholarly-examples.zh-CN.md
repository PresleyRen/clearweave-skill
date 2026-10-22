# 真实论文与中文文本修改示例

[English](scholarly-examples.md) · [中文文档中心](README.zh-CN.md)

本页是公开文本的编辑演示。论文原文与英文修订稿保留原语言，中文部分解释修改目的与保留项。来源、作者和许可证与英文规范页一致。

[测试说明中文版](evaluation-scholarly.zh-CN.md) · [原始输入](../evals/scholarly-2026-10-20/samples.json) · [输出记录](../evals/scholarly-2026-10-20/outputs.json)

## D19-1410 · Sentence-BERT

作者：Nils Reimers、Iryna Gurevych。来源：[ACL Anthology D19-1410](https://aclanthology.org/D19-1410/)。许可：CC BY 4.0。

### 原文关键片段

> BERT (Devlin et al., 2018) and RoBERTa (Liu et al., 2019) has set a new state-of-the-art performance ... a modification of the pretrained BERT network that use siamese and triplet network structures ...

### 修订关键片段

> BERT (Devlin et al., 2018) and RoBERTa (Liu et al., 2019) have set a new state of the art ... a modification of the pretrained BERT network that uses siamese and triplet network structures ...

### 修改说明

- `has set` → `have set`：并列主语要求复数谓语。
- `network that use` → `network that uses`：关系从句谓语与单数先行词一致。
- `sentence embeddings methods` → `sentence embedding methods`：修正名词修饰结构。
- 保留 10,000、50 million、~65 hours、about 5 seconds、引用和原有性能比较。
- 压缩“本论文中我们提出……”式发表框架，直接进入方法贡献。
- 最后一个 `it` 的指代存在潜在歧义；缺少全文证据时不擅自扩大比较结论。

## W19-5034 · scispaCy

来源：[ACL Anthology W19-5034](https://aclanthology.org/W19-5034/)。本轮作为保持原文的控制样本。

处理决定：
- 保留实际承担信息功能的对照结构；
- 保留技术词 `robust`；
- 不因为文本“像模板”就强制重写。

## W19-5028 · Clinical Concept Extraction

原摘要在负面结果前使用了 `Unfortunately` 一类态度标记。ClearWeave 删除情绪性铺垫，直接呈现结果：

> The resulting concepts do not yield performance gains on the document-level clinical coding task.

修改重点：
- 删除作者情绪，不删除负面结果；
- 不把“没有提升”改写成“仍然很有潜力”；
- 结果强度保持不变。

## Semantic Chain Shifts

处理重复叠加的不确定表达，同时保留真正的不确定性、可能机制和历史时间范围。这里的目标不是让句子更“自信”，而是去掉重复 hedge。

## Circular Economy

修正主谓一致并压缩重复框架；假设、比较与证据陈述保持不变。

## SQuAD

作为保持原文的控制样本：
- 保留与人工表现的比较；
- 保留全部数字；
- 保留原作者对结果的解释；
- 不因为摘要结构规整就进行额外风格修改。

## HC3-Chinese 中文样本

中文样本用于检查重复、翻译式连接和信息保全。第 2605 行的一次初稿在自检后恢复了“喜欢”和明确的另一种可能性，说明仅靠字面比较不足以覆盖所有语义变化。

Lieflat 0.4.0 的更小改动示例见 [精准清理测试中文版](evaluation-lieflat.zh-CN.md)。
