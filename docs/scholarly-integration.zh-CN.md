# 学术写作能力整合

[English](scholarly-integration.md) · [中文文档中心](README.zh-CN.md)

## 四层编辑结构

| 层级 | 处理内容 | 对应模块 |
| --- | --- | --- |
| 自然表达 | 结构、句法、套话和翻译痕迹 | `english.md`, `chinese.md` |
| 直接的研究写作 | 必要限定、贡献聚焦、结果中性呈现 | `anti-defensive.md`, `academic.md` |
| 学术语法 | 按功能选择时态、主谓一致、冠词、修饰和信息流 | `academic-grammar.md` |
| 基于样稿的文风 | 样稿选择、语料测量、修辞画像、认可定稿偏好 | `author-voice.md`, `clearweave_scholar.py` |

所有层共享 `preservation.md` 的保真规则。任务路由、输出语言和修改幅度由 `SKILL.md` 统一控制。

## 新增来源如何互补

| ID | 来源 | 采用的主要能力 | 实现 |
| --- | --- | --- | --- |
| S33 | mronkko/claude-academic-research | 根据句子的修辞功能选择时态；保持术语一致；相关工作按综合论证组织 | CW38, CW39, CW42 |
| S34 | HD0NG/claude-skills | 区分贡献、过程、结果和解释时的语态；建立带领域与章节范围的文风档案 | CW38, CW39, CW43 |
| S35 | YoakeLee/academic-paper-writing-skill | 检查语法中心、主谓一致、悬垂修饰、冠词和词形；结构重写时使用反向提纲 | CW40, CW41, CW42 |
| S36 | Jingyang-Zhu/personal-academic-writing-skill | 从真实技术论文提取稳定论证与解释习惯；保留样稿来源与重复文献处理 | CW38, CW43, CW44 |
| S37 | shannhk/writing-style-extractor | 区分表面统计、句法、结构与实际可用的风格画像；风格判断必须有样本依据 | CW43, CW44 |
| S38 | snowmays/style-alchemy | 按体裁归组样本，生成机器可读画像；区分内容偏好与写作风格 | CW43, CW44, CW45 |
| S39 | YuanZHAO321/Scientific-Writing | 在授权结构修改时按“文档→段落→句子”顺序处理；使用已知到新信息推进 | CW38, CW41, CW46 |
| S40 | KalarisLabs/research-agent-skills | 根据项目证据起草；连接研究问题、实验比较与贡献结论 | CW38, CW42, CW48 |
| S41 | Allan9719/scientific-writer-skill | 先判断句子功能再决定语法形式；区分起草、编辑、诊断与教学 | CW38–CW42 |
| S42 | jzOcb/writing-style-skill | 从初稿/定稿配对中提取候选偏好；保留样例、版本和可回退记录 | CW43, CW45, CW46 |
| S43 | OvOYu/anti-defensive-writing | 区分诊断、局部润色、重构和起草；回复信引用最终正文而不是另写一版 | CW37, CW38, CW46 |
| S44 | Worigin0314/academic-defensive-writing-auditor | 修改前区分防御性表达、必要限定、混合表达与正常文本 | CW37, CW38, CW47 |
| S45 | Mseymur/HCI-Academic-Writing | 区分语域问题与贡献定位；用具体技术/实证增量替代空泛标签 | CW37, CW38, CW42, CW46 |

## 主要冲突与处理

| 冲突 | 处理原则 | 回归测试 |
| --- | --- | --- |
| 更强表达 vs 不确定性 | 删除空道歉，保留概率和适用范围 | CF27；W19-4703；W19-5028 |
| 修正语法 vs 原样引用 | 正文可修正；引用内容单独标注，不静默修改 | CF28 |
| Methods 过去时 vs 当前算法行为 | 按句子功能选时态，不按章节机械决定 | CF29 |
| 模仿样稿 vs 样稿事实 | 只提取表达习惯，事实使用当前稿件自己的内容 | CF30 |
| 句长统计 vs 强制配额 | 统计只作描述，不强制改到某个数值 | CF31 |
| 论文模板 vs 当前证据 | 只使用与研究类型匹配的修辞步骤 | CF32 |
| 作者习惯中的语法错误 | 明显语法错误修正，稳定表达习惯可以保留 | CF33 |
| 一次定稿偏好 vs 全局规则 | 每条偏好保留适用范围和待确认状态 | CF34 |
| 限定数量 vs 论断解释 | 所有真正影响论断的独立条件继续放在相关论断旁边 | CF01, CW37 |
| 回复信摘录 vs 另行润色 | 回复信复制最终稿真实片段；正文变化后同步更新 | CW46 |

## 扩展步骤

1. 保存原文、错误输出、请求模式和希望区分的正确行为。
2. 使用 `clearweave_trace.py` 定位 CW 能力、CF 冲突、来源决定和模块。
3. 增加一个错误案例和一个合法近似案例；解析问题放 Python 测试，编辑问题放应用案例。
4. 只修改最小范围规则，然后重新运行回归和至少一个真实文本应用。
5. 更新 `capabilities.json`、`feature-map.json`、来源审计和生成表格，并把实测结果写入评测报告。

## 来源追踪

S33–S45 都按固定 commit 记录；文件哈希或 Git blob ID 保存在 `scholarly-source-snapshots.json`。完整取舍保存在来源审计中。来源只是方法参考，不意味着运行或依赖上游项目；ClearWeave 的运行指令和代码独立实现。
