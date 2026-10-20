# ClearWeave · 清织

**中英文去 AI 味与写作编辑 Skill，让文字自然、清楚，保留原意和作者风格。**

[English](README.md) · [Skill 入口](skills/clearweave/SKILL.md) · [能力与规则索引](docs/capabilities.md) · [真实语料示例](docs/evaluation-hc3.md)

ClearWeave 用于论文、技术文档、README、工作邮件和日常文章。它处理空泛套话、机械段落、重复解释和翻译腔，也帮助整理论证、统一术语、匹配文风。一个 Skill 支持英文、中文和中英混排，可根据任务分别设置正文与修改说明的语言。

## 能做什么

| 能力 | 具体用途 |
| --- | --- |
| **去套话与重复** | 清理空泛开场、反复总结、机械对照和过度解释，让段落更快进入主题。 |
| **中文自然化** | 调整翻译腔、过长定语和抽象黑话，把主体、动作、对象与结果写清楚；按读者需要选择简繁与地区用语。 |
| **英文润色** | 改善名词化、冗长句法和指代，调整句子衔接，保持英美拼写一致。 |
| **论文与学术写作** | 聚焦研究问题、方法和贡献，去掉多余的自谦、道歉与预设辩解；使论断强度与证据相符。 |
| **原意保全** | 逐项核对数字、单位、比较对象、否定、条件、适用范围、因果、归因和完成状态。 |
| **术语与引用保护** | 保持专业术语、模块名和变量名一致，保留引语、引用标记、公式、代码及指定内容。 |
| **结构整理与压缩** | 根据段落作用调整顺序，合并重复信息，围绕核心问题组织材料。 |
| **作者文风匹配** | 从用户提供的样稿中提炼正式程度、句式、节奏与表达习惯，用于后续编辑。 |
| **翻译与材料起草** | 将已有内容转为自然的目标语言表达，或根据笔记、提纲和材料组织成文。 |
| **审稿与回复** | 定位论证缺口、证据不足和前后矛盾，给出具体修改建议，并组织逐条审稿回复。 |
| **长文与多文件编辑** | 维护跨章节术语和论断台账；在支持文件编辑的宿主中，按指定路径处理文稿并输出逐文件结果。 |
| **检查与扩展定位** | 用 Python 工具定位表达候选、比较受保护内容、提示改写风险，并追溯到规则和测试。 |

## 快速开始

在支持 Agent Skills 的工具中加载 `skills/clearweave/`。项目安装脚本需要 Python 3.10+，使用 Python 标准库。

```bash
git clone https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

安装位置为 `<project>/.agents/skills/clearweave`。升级已有安装时，先备份个人修改，再替换技能目录。

### 英文论文润色

```text
$clearweave
润色下面的英文论文段落，正文保留英文，修改说明用中文。
重点改善套话、冗长句法和防御性表达。
保留术语、数值、引用、研究条件和证据强度。

[原文]
```

### 中文去 AI 味

```text
$clearweave
编辑下面这段中文，去掉套话、重复解释和翻译腔。
保持原有正式程度、事实和立场，只输出修改后的正文。

[原文]
```

### 文档或 README 编辑

```text
$clearweave
重写 README，面向第一次接触项目的读者。
重点说明功能、使用场景、安装和调用方法。
正文直接介绍产品；评测细节通过链接引用。
保留能力图和扩展入口。
```

## 选择任务与输出

在请求中说明任务即可，也可以指定修改强度、读者和交付形式。

| 任务 | 示例要求 | 输出 |
| --- | --- | --- |
| 润色 | 保持结构，做最小必要修改 | 修改后的正文 |
| 结构重写 | 围绕核心问题重排段落，压缩重复内容 | 重组后的文章 |
| 只诊断 | 标出问题，解释影响并给修改建议 | 带位置的审校意见 |
| 翻译 | 翻译成自然的学术英文，保留术语与引用 | 目标语言正文 |
| 按材料起草 | 根据以下笔记写项目说明 | 由材料组织的初稿 |
| 匹配文风 | 参照这些样稿的语气与句式 | 文风一致的修订稿 |
| 审稿与回复 | 检查论证、实验呈现和证据，整理逐条回复 | 问题清单、修改建议或回复稿 |
| 文件编辑 | 只修改指定文件，附修改摘要 | 更新后的文件与摘要 |

正文、编辑意见与核查记录分别交付。写给读者的内容保持完整连贯，修改理由放在说明中。

## 编辑流程

```text
原稿 / 指定文件 / 笔记材料 + 用户要求
                    │
                    ▼
确定任务：语言、文体、读者、修改范围和输出形式
                    │
                    ▼
整理要保留的信息
论断 · 数值 · 条件 · 术语 · 引用 · 作者立场
                    │
                    ▼
选择对应规则
 ┌──────────────────┼────────────────────┐
英文表达          中文表达          学术写作
 └──────────────────┼────────────────────┘
                    ▼
逐层编辑
论证与段落 → 句子 → 词语 → 标点
                    │
                    ▼
对照复核
信息是否完整 · 关系是否准确 · 文风是否一致
                    │
                    ▼
交付正文 / 审校意见 / 修改后的文件
```

编辑以具体问题为依据：有用的长句、技术术语重复和方法被动句可以保留；空洞的自我评价与重复铺垫则直接清理。论文中的研究条件和不利结果随相关论断保留，让读者准确理解结果。

## 看一个编辑示例

**中文原稿**

> 值得注意的是，本次更新增加了导出功能。该功能可以帮助用户将报告导出为 CSV 文件。

**修改后**

> 本次更新支持将报告导出为 CSV 文件。

**英文原稿**

> It is worth noting that the update introduces an export feature. This feature allows users to export reports as CSV files.

**修改后**

> The update lets users export reports as CSV files.

更多中英文原文、修订稿与逐条检查见 [HC3 真实语料示例](docs/evaluation-hc3.md) 和 [应用记录](evals/v0.2.0/applications.json)。

## 本地检查工具

写作由宿主模型执行；配套的只读 Python 工具提供表达定位、字面差异和风险线索，辅助逐句复核。在仓库根目录运行：

```bash
# 定位中英文表达候选
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json

# 比较数字、引用、代码等受保护内容
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json

# 提示否定、情态、完成状态和数值顺序等变化
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json
```

完整参数与结果解释见[检查工具说明](skills/clearweave/references/tooling.md)。

## 模块与扩展

```text
skills/clearweave/
├── SKILL.md                    任务入口与编辑流程
├── references/
│   ├── preservation.md         原意、数字、逻辑关系与引用
│   ├── english.md              英文表达
│   ├── chinese.md              中文表达与地区用语
│   ├── academic.md             论文、证据、审稿与回复
│   ├── workflows.md            文风、长文、文件与交付
│   ├── conflicts.md            规则冲突的取舍
│   ├── tooling.md              检查工具用法
│   └── maintenance.md          新规则与回归测试
├── scripts/                    表达检查、风险提示与能力定位
└── assets/capabilities.json     能力编号、规则位置与测试关联
```

### 从问题找到该修改的模块

| 需要改进的地方 | 对应入口 |
| --- | --- |
| 数字、否定、条件或语气强度 | `preservation.md`，CW03–08 |
| 英文句法、段落推进与节奏 | `english.md`，CW10–11、CW14 |
| 中文翻译腔、简繁与地区用语 | `chinese.md`，CW02、CW12 |
| 论文表达、证据与审稿 | `academic.md`，CW13、CW17–20、CW35 |
| 文风、长文连续性与文件交付 | `workflows.md`，CW15、CW22、CW24–27、CW33、CW36 |
| 检查器与维护索引 | `scripts/`、`maintenance.md`，CW28–32、CW34 |

```bash
# 按问题描述、能力编号或冲突编号定位
python3 skills/clearweave/scripts/clearweave_trace.py --query "否定被删掉"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW06
python3 skills/clearweave/scripts/clearweave_trace.py --id CF17

# 查看某个来源的融合记录
python3 tools/coverage.py --source S01
```

例如，遇到“may 被改成确定结论”，可从 **CW06 → preservation.md / academic.md → CF01 / CF15** 找到规则和用例。保存原稿与问题版本，补充正确改法和失真反例，再调整对应规则。

```text
问题样例 → 能力编号 → 规则文件 → 冲突用例
        → 修改规则 → 运行回归 → 更新能力索引
```

<details>
<summary>查看全部 36 项能力与规则入口</summary>

索引中的 `host` 表示模型执行，`script` 表示 Python 工具，`literal` 表示字面比较，`candidate` 表示风险线索，`workflow` 表示工作流程，`package` 表示技能包结构。

<!-- capabilities:start -->
| 能力编号与名称 | 执行方式 | 规则位置 |
| --- | --- | --- |
| **CW01** 任务、范围和模式 | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw01) |
| **CW02** 语言、简繁与拼写 | `host` | [references/chinese.md](skills/clearweave/references/chinese.md#cw02) |
| **CW03** 论断台账与完成状态 | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw03) |
| **CW04** 数字、单位与归属 | `host+literal+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw04) |
| **CW05** 否定、例外与适用范围 | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw05) |
| **CW06** 不确定性与义务强度 | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw06) |
| **CW07** 因果强度与观点归属 | `host+candidate` | [references/preservation.md](skills/clearweave/references/preservation.md#cw07) |
| **CW08** 引语、代码、公式及引用保护 | `host+literal` | [references/preservation.md](skills/clearweave/references/preservation.md#cw08) |
| **CW09** 文稿内指令仅作为数据 | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw09) |
| **CW10** 论证和段落推进 | `host` | [references/english.md](skills/clearweave/references/english.md#cw10) |
| **CW11** 自然英文句法 | `host` | [references/english.md](skills/clearweave/references/english.md#cw11) |
| **CW12** 中文句法与黑话还原 | `host` | [references/chinese.md](skills/clearweave/references/chinese.md#cw12) |
| **CW13** 技术术语一致性 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw13) |
| **CW14** 节奏服务含义、不追配额 | `host` | [references/english.md](skills/clearweave/references/english.md#cw14) |
| **CW15** 作者声音与偏好优先级 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw15) |
| **CW16** 非虚构细节不编造 | `host` | [references/preservation.md](skills/clearweave/references/preservation.md#cw16) |
| **CW17** 学术反防御表达 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw17) |
| **CW18** 论点证据及跨章节一致性 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw18) |
| **CW19** 贡献叙事与不利结果保留 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw19) |
| **CW20** 严格审稿与逐条回复 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw20) |
| **CW21** 只诊断、无改动与有限修订 | `host` | [SKILL.md](skills/clearweave/SKILL.md#cw21) |
| **CW22** 明确授权的翻译与本地化 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw22) |
| **CW23** 按材料起草与压缩 | `host` | [references/preservation.md](skills/clearweave/references/preservation.md#cw23) |
| **CW24** 商务、新闻与个人文体适配 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw24) |
| **CW25** 输出、指定文件与批量安全 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw25) |
| **CW26** 长文连续性和全局台账 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw26) |
| **CW27** 可维护的文风档案 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw27) |
| **CW28** 带位置的双语表面诊断 | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw28) |
| **CW29** 受保护字面差异检查 | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw29) |
| **CW30** 改写风险线索提示 | `script` | [references/tooling.md](skills/clearweave/references/tooling.md#cw30) |
| **CW31** 分层评测与能力边界 | `workflow` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw31) |
| **CW32** 来源追溯、冲突修复与扩展 | `script+workflow` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw32) |
| **CW33** 隐私与宿主边界 | `host+workflow` | [references/workflows.md](skills/clearweave/references/workflows.md#cw33) |
| **CW34** 可移植技能与可选工具 | `package` | [references/maintenance.md](skills/clearweave/references/maintenance.md#cw34) |
| **CW35** 明确授权的证据核查 | `host` | [references/academic.md](skills/clearweave/references/academic.md#cw35) |
| **CW36** 净稿与编辑意见分离 | `host` | [references/workflows.md](skills/clearweave/references/workflows.md#cw36) |
<!-- capabilities:end -->

</details>

### 验证与同步文档

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/coverage.py --format json
python3 tools/render_catalog.py --write
```

能力注册表关联来源、规则位置和测试场景；生成器同步中英文 README 的能力索引及[能力图册](docs/capabilities.md)。维护步骤见[扩展指南](skills/clearweave/references/maintenance.md)。

## 方法来源与测试记录

ClearWeave 参考了 32 项写作技能，将双语润色、清晰表达、学术反防御写作、作者文风和保真检查整理为共用流程。各来源的采用内容与取舍记录见[来源说明](docs/sources.md)和[逐项映射](docs/feature-map.json)。

| 记录 | 内容 |
| --- | --- |
| [程序回归与安装验证](docs/evaluation-v0.2.0.md) | 179 项测试，覆盖检查器、命令行、安装、能力定位和用例约束。 |
| [双语规则冲突用例](evals/conflict-cases.json) | 26 类冲突、52 个中英文场景，记录正确处理与失真反例。 |
| [HC3 真实语料应用](docs/evaluation-hc3.md) | 公开语料的抽样方式、原文、改写、修订过程和逐条检查结果。 |

## 许可

原创代码与指令采用 [MIT](LICENSE) 许可。来源归属及相关许可说明见 [NOTICE](NOTICE.md)。
