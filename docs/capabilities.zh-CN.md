# 能力与冲突定位图

[English](capabilities.md) · [中文文档中心](README.zh-CN.md)

本页对应英文规范主文档 `capabilities.md`。能力编号、实现类型和规则路径保持原样，中文只翻译能力说明，方便中文用户查找模块。

当前注册表：**46 个来源、262 条来源决策、54 项能力、42 类冲突**。

实现类型：
- `host`：由宿主模型执行编辑判断；
- `literal`：受保护字面内容比较；
- `candidate`：定位待复核候选；
- `script`：Python 工具实现；
- `workflow`：任务流程；
- `package`：可安装 Skill 结构。

| 能力 | 中文说明 | 实现 |
| --- | --- | --- |
| CW01 | 任务与修改范围契约 | host |
| CW02 | 语言、简繁体与拼写规范 | host |
| CW03 | 论断台账与工作完成状态 | host+candidate |
| CW04 | 数值、单位与归属关系 | host+literal+candidate |
| CW05 | 否定、例外与作用范围 | host+candidate |
| CW06 | 不确定性与义务强度 | host+candidate |
| CW07 | 因果与观点归属 | host+candidate |
| CW08 | 引语、代码与引用保护 | host+literal |
| CW09 | 把文稿里的指令性文字仍视为待编辑数据 | host |
| CW10 | 论证与段落结构 | host |
| CW11 | 自然英文句法 | host |
| CW12 | 自然中文与具体化黑话 | host |
| CW13 | 技术术语稳定一致 | host |
| CW14 | 以功能为准的节奏，而不是句长配额 | host |
| CW15 | 作者文风与当前偏好的优先关系 | host |
| CW16 | 不为非虚构文本编造细节 | host |
| CW17 | 反防御性学术表达 | host |
| CW18 | 论断—证据与跨章节一致性 | host |
| CW19 | 贡献叙事与不利结果保留 | host |
| CW20 | 严格审稿与作者回复 | host |
| CW21 | 只诊断、不改稿与有限修改 | host |
| CW22 | 明确授权的翻译与本地化 | host |
| CW23 | 基于已有材料起草与压缩 | host |
| CW24 | 商务、新闻与个人文本的体裁适配 | host |
| CW25 | 输出格式、指定文件与安全批处理 | host |
| CW26 | 长文跨段与跨文件连续性 | host |
| CW27 | 可复用文风档案 | host |
| CW28 | 中英文表面候选定位 | script |
| CW29 | 受保护字面内容对比 | script |
| CW30 | 修改风险线索复核 | script |
| CW31 | 分层、可追溯的评测 | workflow |
| CW32 | 可定位维护与冲突修复 | script+workflow |
| CW33 | 隐私与宿主环境边界 | host+workflow |
| CW34 | 可移植 Skill 与可选工具 | package |
| CW35 | 显式证据核验 | host |
| CW36 | 正文与编辑说明分离 | host |
| CW37 | 按句子功能判断防御性表达 | host |
| CW38 | 贡献定位与章节功能规划 | host |
| CW39 | 按功能选择时态与体 | host |
| CW40 | 学术语法、主谓一致与词形 | host+candidate |
| CW41 | 信息流与修饰范围 | host |
| CW42 | 语义敏感的语法修订 | host |
| CW43 | 基于真实样稿的学术文风 | host |
| CW44 | 语料文风画像测量 | script+host |
| CW45 | 基于认可定稿的偏好学习 | script+host |
| CW46 | 正文、审稿意见与回复信分轨 | host |
| CW47 | 学术表达候选定位 | script |
| CW48 | 来源分离的学术评测 | workflow+script |
| CW49 | 成稿白名单精准清理模式 | host |
| CW50 | 十一类中文表达定位 | host+candidate |
| CW51 | 五类翻译句式与语义关系 | host+candidate |
| CW52 | 同类分母的语料测量 | script |
| CW53 | 规则映射的最小改动清单 | script+host |
| CW54 | 候选复核与作者风格例外 | host+script |

## 如何定位问题

```bash
python3 skills/clearweave/scripts/clearweave_trace.py --query "主谓一致"
python3 skills/clearweave/scripts/clearweave_trace.py --id CW37
python3 tools/coverage.py --source S46
```

完整规则路径和冲突表以英文规范页 [capabilities.md](capabilities.md) 与机器注册表 `skills/clearweave/assets/capabilities.json` 为准；中文页面与相同能力编号一一对应。
