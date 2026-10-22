# 来源与融合取舍

[English](sources.md) · [中文文档中心](README.zh-CN.md)

ClearWeave 当前来源注册表覆盖 **46 个项目/实现**。这些来源用于提取方法、冲突案例和可复用规则，不代表安装了 46 个依赖，也不代表每个来源都是独立方法。机器可读的逐条采用/调整记录保存在 [source-audit.json](source-audit.json) 和 [feature-map.json](feature-map.json)。

## 来源总览

| ID | 来源 | 主要吸收能力 |
| --- | --- | --- |
| S01 | cbsteh/anti-ai-writing | 先检查证据与主张强度，再处理文风 |
| S02 | Kiterlin/anti-defensive-writing | 区分必要限定与空防御 |
| S03 | Simon-Chng/anti-defensive-writing | 区分局部润色、结构修改和正文/回复 |
| S04 | Adkid-Zephyr/anti-defensive-writing-Skill | 贡献聚焦与实验叙事；排除选择性隐藏负面结果 |
| S05 | blader/humanizer | 段落结构、套话、重复与文风参考 |
| S06 | conorbronsdon/avoid-ai-writing | 诊断与改写分离、受保护内容、有限修改 |
| S07 | hardikpandya/stop-slop | 精简开场、空泛重要性和重复总结 |
| S08 | Aboudjem/humanizer-skill | 多模式编辑、受保护文本与上下文判断 |
| S09 | keez97/humanizer | 结构/句子/词汇分层诊断 |
| S10 | apoapostolov/humanizer | 编辑任务路由与保真优先 |
| S11 | smyrick/humanize-text | 改前改后论断和字面保全 |
| S12 | ashgreat/humanizer | 学术英文中过度分段、元话语和自夸处理 |
| S13 | kjmagnan1s/anti-slop | 可维护规则库、文风保护与复核 |
| S14 | ryanmaule/humanize | 最小必要修改与只诊断模式 |
| S15 | spuvr/humanizer | 连贯性、节奏与不过度解释 |
| S16 | hachisuka-mh/humanizer | 文风指纹思路；排除伪检测概率 |
| S17 | jalaalrd/anti-ai-slop-writing | 个人文风与媒介适配；排除机械禁词 |
| S18 | israelsaba/ai-writing-detector-skill | 可解释候选定位与多语言规则分离 |
| S19 | op7418/Humanizer-zh | 中文否定、条件、范围、归因和完成状态保全 |
| S20 | syw2039/humanizer-zh | 中文正式程度、最小改动与样稿校准 |
| S21 | ksufer/humanizer-zh-skill | 按博客、新闻、公文、评论等文体分流 |
| S22 | jiji262/humanizer-chinese | 中文模板、翻译腔和结构模式库 |
| S23 | ai-zixun/humanizer-zh | 中文长文主线、段落功能和翻译腔 |
| S24 | acchuang/zh-tw-humanizer | 台湾繁体中文本地化和受保护内容 |
| S25 | huang-kaibo/content-humanizer | 内容平台场景中的口语化模式；仅选择性采用 |
| S26 | masterball-w/Master-humanizer-skill | 中文模式观察与文体分类；排除强制标点清零 |
| S27 | nothing0here/humanizer-zh | 中文职场、技术和双语场景覆盖 |
| S28 | holygeek00/humanizer-zh-cn | 识别黑话背后的信息缺失，而非机械禁词 |
| S29 | labarba/sciwrite | 五轮学术写作审查：赘词、语态、句法、术语、数字 |
| S30 | softaworks/writing-clearly-and-concisely | 清晰简洁写作与 AI 套话审查 |
| S31 | K-Dense-AI/scientific-writing | 论断—证据、方法—结果—结论一致性 |
| S32 | YuanZHAO321/Academic-Writing | 论文组织、段落、句子和审稿回复 |
| S33 | mronkko/claude-academic-research | 按修辞功能选时态、术语一致、相关工作综合 |
| S34 | HD0NG/claude-skills | 贡献/过程/结果/解释语态与章节文风画像 |
| S35 | YoakeLee/academic-paper-writing-skill | 主谓一致、冠词、悬垂修饰和反向提纲 |
| S36 | Jingyang-Zhu/personal-academic-writing-skill | 从真实技术论文提取稳定论证习惯 |
| S37 | shannhk/writing-style-extractor | 句法、结构、表面统计和样稿证据 |
| S38 | snowmays/style-alchemy | 按体裁归组的机器可读文风画像 |
| S39 | YuanZHAO321/Scientific-Writing | 文档→段落→句子层级修订与信息流 |
| S40 | KalarisLabs/research-agent-skills | ML 论文中问题、方法、实验、贡献连接 |
| S41 | Allan9719/scientific-writer-skill | 功能优先、学术语法和分模式写作 |
| S42 | jzOcb/writing-style-skill | 从初稿/定稿配对提取候选偏好 |
| S43 | OvOYu/anti-defensive-writing | 防御性表达、局部润色、重构和回复信引用一致性 |
| S44 | Worigin0314/academic-defensive-writing-auditor | 防御性写作分类、必要限定和结果解释约束 |
| S45 | Mseymur/HCI-Academic-Writing | 语域、贡献定位、研究问题与相关工作组织 |
| S46 | larashero3-dotcom/lieflat-less-ai-tone | 中文成稿白名单精准清理、11 类规则和语料测量方法 |

## 融合原则

所有来源进入 ClearWeave 前都经过冲突处理，主要原则如下：

1. **事实与证据边界优先于文风。**
2. **规则命中只产生候选，不自动决定修改。**
3. **真实限制、负面结果、条件和不确定性不能因为“去 AI 味”而删除。**
4. **作者或项目风格可以影响表达，但不能覆盖当前任务和事实。**
5. **不把单个词、破折号、被动句、句长或检测分数作为作者身份结论。**
6. **对学术文本，术语一致性和论断—证据关系优先于句式多样性。**
7. **lieflat 精准模式只在明确选择时锁定未命中文本；完整编辑模式仍可处理结构、语法和论证。**

## 追踪具体来源

```bash
python3 tools/coverage.py --source S01
python3 tools/coverage.py --source S44
python3 tools/coverage.py --source S46
```

需要逐条查看某一来源的“采用 / 调整 / 排除”记录时，使用 [source-audit.json](source-audit.json)；需要看能力落在哪个模块时，使用 [中文能力索引](capabilities.zh-CN.md)。
