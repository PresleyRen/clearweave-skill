# ClearWeave · 清织

**中英文去 AI 味、反防御写作、学术文风与成稿精准清理。**

[English](README.md) · [Skill 入口](skills/clearweave/SKILL.md) · [功能与规则索引](docs/capabilities.md) · [真实论文示例](docs/scholarly-examples.md)

ClearWeave 用于英文论文、中文文章、技术文档、README 和工作邮件。它清理套话与重复，直接呈现研究贡献，修正学术语法，并从指定样稿中提取可复用的文风。正文语言、说明语言、文体和修改幅度可以分别设置。

## 能做什么

| 模块 | 具体功能 | 常见交付 |
| --- | --- | --- |
| **lieflat 精准清理** | 按十一类中文规则定位，只改命中片段；锁定段落、标题层级、列表和表格，保留其余原文。 | 规则对应的最小修改稿 |
| **语料对比与改动验收** | 测量中文表达候选、段落与标题指标；比较两组语料，核对每处改动及未改区域。 | 位置报告、语料测量、改动清单核验 |
| **双语去 AI 味** | 调整空泛开场、机械段落、反复总结、过度解释、中文翻译腔和英文名词化。 | 自然清楚的修订稿 |
| **反防御写作** | 区分空道歉、预设辩解、重复保留词与必要条件；把贡献、证据和比较条件直接写清楚。 | 聚焦研究内容的摘要、引言与结论 |
| **论文语法** | 按句子功能选择时态；检查主谓一致、冠词、单复数、指代、修饰关系、平行结构和信息顺序。 | 语法修订与逐项说明 |
| **论证与章节组织** | 围绕问题、方法、证据和贡献安排段落，综合相关工作，区分研究计划与已完成结果。 | 反向提纲、章节草稿、结构修改 |
| **真实样稿文风** | 从指定论文或个人样稿提取句式、语气、结构与术语习惯；按语言、领域和章节组织档案。 | 作者、团队或领域文风档案 |
| **定稿偏好学习** | 比较初稿与认可的定稿，记录改动及适用范围，整理待确认的文风偏好。 | 带来源的偏好提案 |
| **原意与术语核对** | 核对数字、单位、否定、条件、证据强度、比较对象、工作状态，以及引语、公式和代码。 | 修改前后差异与待复核位置 |
| **审稿与回复** | 定位论证缺口、证据不足和前后矛盾；组织逐条回复并核对引用的修订正文。 | 审稿意见、回复信、净稿 |
| **翻译、起草与压缩** | 按材料写作，转换语言和地区用语，合并重复信息。 | 目标语言正文 |
| **长文、多文件与维护** | 维护术语和论断台账，处理指定文件，按能力编号定位规则、来源、冲突和测试。 | 逐文件结果与扩展入口 |

## 完整功能图

```text
原稿 / 论文 / 笔记 / 指定样稿 + 本次要求
                       │
                       ▼
任务与风格：语言 · 文体 · 章节 · 修改强度 · 项目风格指南
                       │
                       ▼
信息台账：事实 · 数值 · 条件 · 引用 · 术语 · 研究状态
                       │
           ┌───────────┴───────────────────┐
           ▼                               ▼
完整编辑路径                         lieflat 成稿精准清理
润色 / 重写 / 翻译 / 起草             锁定结构与未命中原文
双语表达 · 反防御与贡献                    │
论文语法 · 论证组织                        ▼
真实样稿文风 · 定稿偏好              LF01–LF11 中文规则
           │                       ├─ 翻案 / 列举 / 句间结构
           │                       ├─ 破折号 / 冒号 / 标题编号
           │                       ├─ 拟人 / 已有数据 / 空起手
           │                       └─ 五类翻译句式 / 段首回指
           │                               │
           │                       体裁与作者习惯复核
           │                       每处修改 → 规则 → 最小片段
           └───────────┬───────────────────┘
                       ▼
复核：compare 字面差异 · risk 变化线索 · 编辑者语义核对
      scholar 学术与文风 · tone 候选/分母/语料对比/改动清单
                       │
                       ▼
交付：正文 / 诊断 / 修改说明 / 回复信 / 文风档案
只诊断请求在选定路径中返回定位与建议，原稿保持不变。

扩展：问题 → CW 能力 → LF 规则 / CF 冲突 → 文件 → 正反例 → 真实文本复测
```

## 安装与调用

```bash
git clone --branch v0.4.0 https://github.com/PresleyRen/clearweave-skill.git
cd clearweave-skill
python3 tools/install_skill.py --project /你的项目绝对路径
```

安装位置为项目的 `.agents/skills/clearweave`。更新已有安装时，先备份自定义内容，再替换对应目录。Python 工具使用 Python 3.10+ 标准库。

```text
$clearweave
润色这段英文论文：去套话与防御性表达，检查主谓一致、时态、冠词和修饰关系。
正文保留英文，说明用中文；保持数值、引用、术语和证据强度。
[原文]
```

```text
$clearweave
根据我提供的论文样稿提取文风，按领域、章节、句式、术语和论证顺序整理。
用这个档案编辑下面的摘要。只输出英文正文。
[样稿与待编辑摘要]
```

```text
$clearweave
给这段中文去 AI 味，保留正式程度，压缩重复解释，只给修改后的正文。
[原文]
```

更多用法见[学术提示词](skills/clearweave/prompts/scholarly.md)和[精准清理提示词](skills/clearweave/prompts/precision.md)。

## lieflat 成稿精准清理

适合“只去味，不顺便润色”的中文成稿。先读取指定文风资料，再定位规则、核对上下文，只改需要处理的片段。

| 规则 | 能力 |
| --- | --- |
| LF01–LF03 | 检查虚设误解、密集列举和相邻句重复；保留真实对照、完整项目和叙事顺序。 |
| LF04–LF06 | 按作用处理破折号、提示性冒号和装饰性标题编号；保留作者标点习惯与交叉引用。 |
| LF07–LF09 | 把冗余职业拟人、泛化概括和空起手改为原文已支持的直接表达。 |
| LF10 | 检查长定语、当…时、话题壳、句首连接词和复述提示语，保持时间、条件、转折与推断关系。 |
| LF11 | 给对象明确的非首段评论补回指，帮助上下段衔接。 |

```text
$clearweave
按 lieflat 白名单模式清理这份中文成稿。
保留标题、段落、列表、表格、事实和未命中的原文。
参考我提供的语言DNA.md，只输出修改后的正文。
[原文与风格资料]
```

普通英文润色、论文语法和全文重写继续使用完整编辑路径。逐条规则、工具用法与对照示例见 [lieflat 整合说明](docs/lieflat-integration.md) 和 [本轮真实文本记录](docs/evaluation-lieflat.md)。

## 真实文本效果

学术版测试使用已发表论文摘要检查语法、反防御编辑与术语保留，用另外三篇 NLP 摘要建立领域文风档案，并加入两条中文 HC3 历史回答。

| 样本 | 处理效果 |
| --- | --- |
| Sentence-BERT 摘要 | 修正并列主语和关系从句的一致性，精简表达，保留实验数量、时间和引用。 |
| Clinical Concept Extraction 摘要 | 去掉结果前的情绪性引导语，完整保留没有性能收益的研究发现。 |
| Semantic Chain Shifts 摘要 | 合并重复的可能性表达，同时保留 `may`、`likely` 与时间范围。 |
| scispaCy 摘要 | 保留必要的转折、专业词和原有结构。 |
| 中文 HC3 回答 | 压缩重复称谓和说明，保留立场、日期、条件与不确定表达。 |

查看[完整原文与修订稿](docs/scholarly-examples.md)、[测试记录](docs/evaluation-scholarly.md)和[已有 HC3 样例](docs/evaluation-hc3.md)。

## 本地检查与文风工具

模型完成编辑、翻译、论证审查和文风应用；以下 Python 工具提供位置、差异、测量和维护索引。

```bash
# 表达、字面差异与变化线索
python3 skills/clearweave/scripts/clearweave_check.py lint draft.md --language both --format json
python3 skills/clearweave/scripts/clearweave_check.py compare original.md revised.md --format json
python3 skills/clearweave/scripts/clearweave_risk.py original.md revised.md --format json

# 学术语法与反防御扫描
python3 skills/clearweave/scripts/clearweave_scholar.py scan draft.md --language both

# 从样稿生成画像、比较正文、整理定稿偏好
python3 skills/clearweave/scripts/clearweave_scholar.py profile samples.json --kind author --label my-papers > profile.json
python3 skills/clearweave/scripts/clearweave_scholar.py compare-profile profile.json draft.md
python3 skills/clearweave/scripts/clearweave_scholar.py learn original.md final.md --scope English-abstract
```

中文精准清理工具：

```bash
# 定位十一类候选；按作者习惯保留破折号
python3 skills/clearweave/scripts/clearweave_tone.py scan draft.md --genre academic
python3 skills/clearweave/scripts/clearweave_tone.py scan draft.md --keep-rule LF04

# 语料测量与对比；A、B 使用同一套分母
python3 skills/clearweave/scripts/clearweave_tone.py measure corpus/
python3 skills/clearweave/scripts/clearweave_tone.py compare-corpora --a reference/ --b drafts/

# 检查规则编号、原文片段、结构与未列出的改动
python3 skills/clearweave/scripts/clearweave_tone.py verify-edits original.md revised.md edits.json
```

样稿格式、输出字段和各工具用法见[学术工具说明](skills/clearweave/references/scholarly-tools.md)。

## 快速定位与扩展

| 要改进的地方 | 入口 | 编号 |
| --- | --- | --- |
| 白名单模式、十一类中文规则、五类翻译句式 | `lieflat.md`、`lieflat-rules.json` | CW49–51 |
| 中文测量、改动清单、候选复核 | `clearweave_tone.py` | CW52–54 |
| 套话、翻译腔、句式 | `english.md`、`chinese.md` | CW10–14 |
| 防御表达、贡献叙事、正文与意见分离 | `anti-defensive.md` | CW37–38、CW46 |
| 时态、主谓一致、修饰与语义作用域 | `academic-grammar.md` | CW39–42 |
| 真人论文文风、样稿画像、定稿偏好 | `author-voice.md` | CW43–45 |
| 事实、条件、数字、引用 | `preservation.md` | CW03–09 |
| 语法扫描与画像程序 | `clearweave_scholar.py` | CW44–45、CW47 |
| 来源、测试和故障定位 | `maintenance.md`、`scholarly-tools.md` | CW31–32、CW48 |

```bash
python3 skills/clearweave/scripts/clearweave_trace.py --query "主谓一致"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW37
python3 tools/coverage.py --source S44
python3 tools/evaluate_scholarly.py
python3 -m unittest discover -s tests -v
python3 tools/validate_repo.py
python3 tools/render_catalog.py --write
```

新增规则时，保存一个问题样本和一个合理的相似表达，定位模块、补充测试，再更新能力索引。详见[整合与扩展说明](docs/scholarly-integration.md)。

<details>
<summary>展开全部 54 项能力及规则位置</summary>

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
| **CW37** 反防御表达分类与编辑 | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw37) |
| **CW38** 贡献叙事与章节功能 | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw38) |
| **CW39** 按句子功能选择时态 | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw39) |
| **CW40** 学术语法与主谓一致 | `host+candidate` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw40) |
| **CW41** 信息顺序与修饰关系 | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw41) |
| **CW42** 论断强度与语法作用域 | `host` | [references/academic-grammar.md](skills/clearweave/references/academic-grammar.md#cw42) |
| **CW43** 基于真实样稿的学术文风 | `host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw43) |
| **CW44** 文风画像测量与对比 | `script+host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw44) |
| **CW45** 从定稿修订提取偏好 | `script+host` | [references/author-voice.md](skills/clearweave/references/author-voice.md#cw45) |
| **CW46** 正文与审稿意见分离 | `host` | [references/anti-defensive.md](skills/clearweave/references/anti-defensive.md#cw46) |
| **CW47** 学术语法与反防御扫描 | `script` | [references/scholarly-tools.md](skills/clearweave/references/scholarly-tools.md#cw47) |
| **CW48** 真实论文分角色测试 | `workflow+script` | [references/scholarly-tools.md](skills/clearweave/references/scholarly-tools.md#cw48) |
| **CW49** 白名单成稿精准清理 | `host` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw49) |
| **CW50** 十一类中文表达定位 | `host+candidate` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw50) |
| **CW51** 五类翻译句式与语义关系 | `host+candidate` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw51) |
| **CW52** 同类分母的语料对比测量 | `script` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw52) |
| **CW53** 规则映射与未改区域核对 | `script+host` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw53) |
| **CW54** 候选复核与作者风格例外 | `host+script` | [references/lieflat.md](skills/clearweave/references/lieflat.md#cw54) |
<!-- capabilities:end -->

</details>

## 来源与测试

整合记录覆盖 **46 个来源、262 条采用与调整决定、54 项能力、42 类冲突及 84 个中英文冲突场景**。本轮新增 lieflat 精准清理、语料测量和改动清单验收。

[lieflat 整合](docs/lieflat-integration.md) · [精准清理测试](docs/evaluation-lieflat.md) · [来源与取舍](docs/sources.md) · [完整能力索引](docs/capabilities.md) · [整合说明](docs/scholarly-integration.md) · [真实论文测试](docs/evaluation-scholarly.md) · [原始测试数据](evals/scholarly-2026-10-20/)

## 许可

项目原创代码与指令使用 [MIT](LICENSE)。方法来源及署名见 [NOTICE](NOTICE.md)。真实样本文本按其来源许可提供，ACL 论文样例为 CC BY 4.0，HC3 样例为 CC BY-SA 4.0。
