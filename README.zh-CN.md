# ClearWeave · 清织

**一个中英双语的去模板表达与保真编辑 Skill：把互补的方法织在一起，而不是把 32 套提示词叠在一起。**

[English](README.md) · [技能入口](skills/clearweave/SKILL.md) · [全部能力与冲突](docs/capabilities.md) · [32 项来源](docs/sources.md) · [v0.2.0 验证](docs/evaluation-v0.2.0.md)

Clear 表示清楚、准确的表达；Weave 表示有约束地融合不同方法。**同一个入口支持英文、中文和中英混排**，按原稿语言、文体与任务加载规则。中文提问、英文论文交付，不会因此自动翻译成中文。

这是一套给宿主模型使用的编辑指令，附带可选的 Python 检查器和维护索引。**改写、翻译、文风匹配和审稿由宿主模型执行；Python 不负责写作，也不判断作者是否用了 AI。** GitHub 发布不等于自动安装或已上架插件市场。

## 1. 工作流文本图

```text
用户原稿 / 指定文件 / 写作材料 + 当次要求
                    │
                    ▼
任务契约 CW01：编辑 / 只诊断 / 翻译 / 起草 / 文风匹配 / 审稿
                    │  明确语言、范围、文体、修改强度与输出形式
                    ▼
保真层 CW03–09：论断、数值归属、否定、条件、确定性、引用与完成状态
                    │  文稿里的命令只是内容，不是工具授权
                    ▼
按需加载，不连续套用多个“去味过滤器”
 ┌──────────────────┼────────────────────┐
英文 english.md  中文 chinese.md   学术 academic.md（叠加）
 └──────────────────┼────────────────────┘
                    ▼
编辑层：论证/段落 → 句子 → 词语 → 标点
文体与作者声音：workflows.md；已有好句允许不改
                    │
                    ▼
分工复核
 ├─ lint：表面表达候选，有位置；命中不等于错误
 ├─ compare：受保护字符串的新增/丢失，不理解完整语义
 ├─ risk：R01–R08 风险线索，不是语义等价裁判
 └─ 宿主/人工：核对论断关系、范围、因果与阅读效果
                    │
          保真失败？回退或局部修复；不追检测分循环
                    ▼
正文 / 定位诊断 / 修改说明 / 逐文件结果（按用户要求）

出现不足 → 最小复现 → CW 能力 + CF 冲突 → 规则文件 + 来源决定
        → 正例和反例 → 小范围修复 → 自动检查 + 新的宿主行为测试
        → 记录结果、剩余缺口、版本；更新能力图
```

## 2. 全部能力与实际执行边界

下面 36 项是**有边界的能力分类**，不是“36 个独立模型”或成功率保证。

`host`：宿主模型遵循的规则；`literal`：字面检查；`candidate`：风险线索；`script`：已有 Python 实现；`workflow`：操作流程；`package`：技能包结构。`host+candidate` 表示模型负责理解，脚本只能提示部分风险。

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

[能力图册](docs/capabilities.md)为每项列出来源、规则位置、场景编号与能力边界。具体包括：去空泛开场、机械结尾和重复解释；调整长定语、名词化和翻译腔；保留必要被动句、专业术语、真实不确定性、反面结果和作者已有立场；处理长文连续性、明确指定的文件批次和可维护的文风档案。

**不会自动完成的部分：**工具不会重写文档或批量修改文件；文件操作依赖宿主工具与授权。常规润色不查证文献真伪。证据核查必须明确提出，并且能够取得材料；没有材料就标记未核实。长文台账和文风档案是已编写的工作流程，不代表在所有宿主和真实长篇论文上完成了端到端验证。

## 3. 32 项技能是否都被纳入了？

**上述清单中的 32 项都进入了来源审计和取舍映射。** 审计记录包含 **92 条采用决定、102 条调整或排除决定，共 194 条**，全部能追溯到能力模块。32 项并非 32 套完全独立方法，也不代表全网所有技能。

这里的“完整”是对**这份已记录的来源清单和取舍记录**完整，不是声称枚举了每个上游仓库所有子文件、安装器、语言和历史版本。没有把上游 32 个实现全部安装后逐一跑效果比赛；上游主分支观察也不是固定提交版本的复现。

保留有用特性不等于照单全收。葡萄牙语专用规则、商业检测服务、MCP 服务端、自动上传、主观“人类百分比”、强制标点清零、虚构经历、隐瞒不利结果等，**没有伪装成已经融合的功能**。具体采用、调整和排除理由在[来源审计](docs/source-audit.json)；逐决定索引在[feature-map.json](docs/feature-map.json)。映射为可人工复查的规则辅助关联，不是每个来源条款都已单独通过行为验证。

### 如何互相弥补，而不是互相打架

| 原方法之间的冲突 | 融合后的处理 | 冲突测试 |
| --- | --- | --- |
| 反防御：删保留词；科学写作：保留证据限定 | 删空道歉，不删改变结论含义的条件、未知和限制 | CF01 |
| 简洁：偏好主动；方法报告：执行者未知 | 可以保留被动，不编造执行者 | CF02 |
| 去套路：禁词与换同义词；论文：术语准确一致 | 专业含义优先，保留 robust、provenance 和模块名 | CF03–04 |
| 压缩、强叙事；统计口径与负面结果 | 保留分母、对照、延迟代价；不事后换成功指标 | CF05–07 |
| 人味：加细节、情绪；保真：不编造 | 只使用原稿和明确材料中的经历与立场 | CF08–09 |
| 中文本地化；英文论文、简繁与引文 | 输出语言和地区由任务决定，引文单独保护 | CF10–12 |
| 必须改写；只诊断、原文已足够好 | 允许诊断和无改动，不凑修改数量 | CF13–14 |
| 更果断；义务、计划、因果边界 | 必须不改成建议，计划不改成完成，相关不改成因果 | CF15–16 |
| 标点禁令；逐字引用与代码 | 保护内容优先于表面标点偏好 | CF17 |
| 检测分优化、外部上传；真实评估与隐私 | 不追伪概率，不擅自上传，不执行文稿内命令 | CF18–20 |
| 总结、批量、持续学习；范围与授权 | 限定不丢；不跨文件范围；单个偏好不变全局禁令 | CF21–23 |
| 重审、核查、删路标；任务成本与真实证据 | 按风险升级；未查不装已查；保留有功能的路标 | CF24–26 |

**26 类冲突各有英文、中文两个原创夹具，共 52 个；每个都有应保留的示例与会失真的反例。** 这验证规则和用例约束能区分已声明的例子，不证明模型对任意文本都会正确选择。

## 4. 安装和调用

Python 工具需要 **Python 3.10+**，仅使用标准库；只让模型阅读 Skill 时不强制执行 Python。

```bash
git clone --branch v0.2.0 https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /absolute/path/to/your-project
```

安装器复制 `skills/clearweave/` 到项目的 `.agents/skills/clearweave`，拒绝覆盖已有目录，不修改全局设置。升级时先备份已有安装和个人改动，再审核替换；没有自动无损升级功能。兼容格式见 [Agent Skills](https://agentskills.io/specification) 与 [Codex 官方说明](https://developers.openai.com/codex/skills/)。不同客户端的发现方式和自动触发由客户端决定，未逐一验证。

```text
$clearweave
润色下面的英文论文段落，正文保留英文，修改说明用中文。
保留数值、引用、研究条件、不利结果和证据强度；不要强行换术语。
[原文]
```

```text
$clearweave
给下面这段中文去模板味，保持正式程度和原意，只给修改后的正文。
[原文]
```

也可以明确要求“只检查不重写”“按这些样稿匹配文风”“翻译成台湾繁体中文”“根据材料起草”“审稿式检查论证”。这些是自然语言模式，不是虚构的命令解析器。不要把整套来源库加载到每个短句任务中。

## 5. 检查工具与扩展定位

在仓库根目录运行：

```bash
# 表面候选 / 字面差异 / 语义风险线索
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json

# 从问题、能力、冲突或来源定位
python3 skills/clearweave/scripts/clearweave_trace.py --query "否定被删掉"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW05
python3 skills/clearweave/scripts/clearweave_trace.py --id CF17 --format json
python3 tools/coverage.py --source S01

# 验证；能力表变更后显式重生成
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/coverage.py --format json
python3 tools/render_catalog.py --write
```

例如出现“may 被改成确定结论”，先定位 **CW06 → preservation/academic → CF01/CF15 → 原稿与失真稿**，增加一个失败用例和一个允许的同义改写反例，再修最小规则。解析器错误修脚本，文体选择错误修路由，不能都靠增长禁词表解决。

`compare` 的退出码 1 表示字面有变化；`risk` 默认只报告线索，显式 `--fail-on-candidate` 才在有候选时返回 1。**任何命令返回 0 都不是语义通过证明。** 风险扫描能提示一部分否定、情态、完成状态和数值顺序变化，但仍可能漏掉数值顺序不变的角色互换。翻译、合法改写和句子重排也会触发候选。详见[工具边界](skills/clearweave/references/tooling.md)。

## 6. 实际验证与没有证明的事情

| 证据层 | 本版本记录 | 能说明什么 |
| --- | --- | --- |
| 来源与结构 | 32 来源、194 条决定、36 能力、26 冲突，关联及摘要哈希检查 | 没有漏掉已记录的审计条目；不是全文行为覆盖 |
| 确定性测试 | 179 项本地测试，含解析器、CLI、安装、定位、故障注入和夹具约束 | 已列出的程序行为符合预期；52 夹具和32来源索引测试包含在179中，不能重复算独立实验 |
| 本轮应用示例 | 12 条当前对话内原创中英文输入与修订稿，运行字面和风险检查 | 展示实际使用与检查结果；同一助手构造并审阅，不是独立盲测 |
| 历史行为对照 | v0.1 的18对输出：双方各被偏好1次、16次平局；4条后续回归 | 小样本旧版本记录；不等同于v0.2重新完成18对对照 |

本轮修复了日期 `May 12` 被误判为情态词的错误，也更新了新增繁体词形支持后过期的测试预期。检查器的已知语义盲区被保留为反例测试，没有用“测试全绿”掩盖它们。[完整结果、原始日志、环境与应用输出](docs/evaluation-v0.2.0.md)可复查。

**没有证明普遍优于普通提示词，没有测试商业 AI 检测器，没有零失真保证，也没有证明每个上游实现都不如本项目。** 新应用没有独立审稿人、随机化、多模型、多次采样或真人编辑评价。语义判断和学术正确性仍需要人工或有能力的宿主复核。

## 7. 维护与边界

| 发现的问题 | 首先看哪里 | 补救方式 |
| --- | --- | --- |
| 否定、数值、条件被改 | `preservation.md`；`clearweave_risk.py` | 保留逻辑的正例 + 作用域相近的反例 |
| 学术措辞误删、负面结果丢失 | `academic.md` | 按证据强度与文体设例外，不全局禁词 |
| 中文翻译腔、繁体地区选择错误 | `chinese.md`、`workflows.md` | 分开验证语言、字形、地区与语气 |
| 英文刻意碎句、被动句误伤 | `english.md` | 以含义与读者收益为准，不追句长配额 |
| 引语、公式、代码保护失效 | `clearweave_check.py` | 最小解析反例 + 邻接正常正文测试 |
| 长文前后矛盾、文件越界 | `workflows.md` | 台账、分段边界、显式路径与全局复查 |
| 需要加入新来源或能力 | `capabilities.json`、`feature-map.json`、`maintenance.md` | 新编号、取舍理由、双语冲突案例、更新自动表格与实测记录 |

脚本只读、无网络，不代表宿主模型在本地运行；它的服务与数据规则仍适用。默认不外传稿件或样稿。纯文本和 Markdown 是原生处理形式，DOCX/PDF/幻灯片版式需要其他文档工具。规则针对英文与中文；地区用语、特殊术语和复杂 LaTeX/Markdown 解析没有完整覆盖。

## 许可与来源

原创代码和指令使用 [MIT](LICENSE)。[NOTICE](NOTICE.md)保留上游归属及许可范围，包括 Lorena A. Barba 的 CC BY 4.0 `sciwrite`。不重新许可上游项目，不假定许可未知的内容可直接复制，不表示来源作者认可本项目。
