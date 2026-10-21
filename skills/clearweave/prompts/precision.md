# Precision cleanup prompts / 成稿精准清理

## 中文成稿

```text
$clearweave
按 lieflat 白名单模式清理下文，只改 LF01–LF11 明确命中的片段。
保留标题层级、段落、列表、表格、引语、代码和全部事实。
只输出正文。
[原文]
```

## 带作者样稿

```text
$clearweave
先读我提供的风格指南，再用 lieflat 模式清理中文成稿。
保留作者惯用标点、必要转折和正式程度。
另给出每处修改对应的 LF 编号和原文片段。
[风格指南与原文]
```

## 只诊断

```text
$clearweave
按 lieflat 检查这篇稿件，只列位置、LF 编号和上下文判断，不改原稿。
[原文]
```
