# Academic Humanizer 整合验证

[English](evaluation-academic-humanizer.md) · [中文文档中心](README.zh-CN.md)

日期：2026-11-27。运行版本：ClearWeave **0.5.0**。本次新增英文学术 Draft / Polish / Cleanup 路径、按来源选择配套指南，以及常见 LaTeX 标签和交叉引用的字面保护。来源注册表和编写的冲突场景记录预期行为；下方独立试跑保存了实际模型输出。

## 本地检查

Python 3.12.14 下完整单元测试 **411 项全部通过**。包结构、来源映射、生成文档和官方 Skill 结构验证均通过。既有 scholarly 与 lieflat 回放命令也通过；它们使用各自历史版本的运行快照，没有被改称为 0.5.0 的新模型实验。

读取器测试覆盖两个同名 `academic-humanizer` 上游、错来源拒绝、离线行为、固定上游 URL 和独立摘要校验的 `examples` 资源。实际固定来源的三个文件均成功离线精确读取；故意交换两个本地来源时均失败。字面校验器测试覆盖不带数字的标签和引用键、支持的星号形式、外层受保护区域和相似普通文本。

以上为本地结果；已发布提交的 CI 结果另见 [GitHub Actions](https://github.com/PresleyRen/clearweave-skill/actions/workflows/validate.yml)。

## 新上下文配对试跑

两个代理均从不继承对话历史的新上下文开始，各自成批处理相同的四个合成请求，分别使用原有 `f25ac2e036616689e322d9eb857ccb1b287afe50` 版本和升级后的本地版本。两者均被要求离线工作，只收到普通写作请求和指定技能，没有收到预期答案、评审标准或另一组输出。保留的是代理实际交付的原始结果，维护者没有改写。

第三个新上下文代理只收到请求、原材料、评审标准和交替排列的 A/B 输出，没有看到条件映射或技能。四组比较均为平局，评审没有发现任一版本的保真或范围违例。

| 场景 | 请求 | 新版实际行为 |
| --- | --- | --- |
| AH01 | 根据中文实验记录写英文 Results | 保留两方法各自的错误数、中位延迟、离线英语条件和未测试事项，没有补造显著性结论。 |
| AH02 | 对英文 LaTeX 成稿做最小清理 | 仅删除一处空泛开头并调整随后单词的句首大写；其他措辞、标题、分段、平均延迟、随机种子、容差、重试次数、标签和引用均逐字保留。 |
| AH03 | 润色已清楚的学术段落 | 原样返回。 |
| AH04 | 只修主谓一致 | 只把 `suggests` 改为 `suggest`，其余文字不变。 |

两种条件下的三个已有文本场景也均与限定范围内的预期文本完全一致，没有受保护字面差异。风险工具对两组合法的 `suggests` → `suggest` 词形变化各报出一个候选；人工复核确认这是要求中的主谓一致修正。原始记录保留了这项提示，没有把它算作语义错误，也没有隐藏它。

## 证据与适用范围

[原始记录](../evals/academic-humanizer-2026-11-27/manifest.json) · [请求](../evals/academic-humanizer-2026-11-27/requests.json) · [评审标准](../evals/academic-humanizer-2026-11-27/rubric.json) · [原版本输出](../evals/academic-humanizer-2026-11-27/outputs-baseline.json) · [新版输出](../evals/academic-humanizer-2026-11-27/outputs-upgraded.json) · [盲评结果](../evals/academic-humanizer-2026-11-27/blind-review-results.json) · [字面与风险检查](../evals/academic-humanizer-2026-11-27/mechanical-checks.json)。

实际读取文件清单保存了对应指令摘要。父环境标识为 GPT-6 Astra Pro，子代理继承其模型；具体子模型快照和采样参数未开放或固定。每种条件内的四个场景共享上下文。这是带模型评审的小规模定向回归，不能替代独立人工评估、长文测试、客户端自动触发验证，也不证明写作质量普遍提升。离线试跑没有测试实时读取外部指南后的写作效果。本次没有测量检测器分数或投稿录用结果。
