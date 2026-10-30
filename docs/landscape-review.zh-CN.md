# 科研工作流调研与项目定位

调研日期：**2026-10-30**。[English](landscape-review.en.md)。

## 范围与证据

本次针对官方仓库、许可证及研发方原始报告进行设计比较，并非穷尽式
综述。没有实际运行其他系统、购买闭源服务或开展效果对照实验。
“未发现完整开源实现”仅限本次所查来源；不能据此断言绝无代码发布。
性能与效率数字若来自研发方，不能当作本项目独立复现的结果。

需要区分四层：数学模型、证明或实验执行、文献与数据工具，以及长期
证据记录和研究决策。本项目主要解决第四层，应与其他层互补。

## 代表性系统

| 系统与一手来源 | 所查开放情况 | 值得学习的能力 | 与本项目的关系 |
| --- | --- | --- | --- |
| [QED](https://github.com/proofQED/QED) | [MIT](https://github.com/proofQED/QED/blob/main/LICENSE)，外接模型 CLI | 自然语言证明规划、子目标依赖图、结构与引用核验、细节审查及重试 | 是直接的 AI4Math 对照。学习细粒度引用与命题完整性检查；自动证明循环与本项目的人工路线／状态决策边界须分开。LLM 审查不是证明内核。 |
| [MathResearch Ledger](https://github.com/Caie777/math-research-ledger) | Apache-2.0，提供 MCP 接口 | 长期数学对象、依赖版本、有限上下文恢复、暂存检查点及独立人工接受 | 与证据记忆层直接重叠；后续应补上下文恢复与前提版本过期检查。区别应落在角色、预检与运行复盘契约，而非“账本”名称。 |
| [Lean Copilot](https://github.com/lean-dojo/LeanCopilot) | MIT 源代码；模型与工具链另计 | Lean 内的策略建议、前提检索、证明搜索 | 适合作为形式化工具来源；接入时保留版本、假设和非形式命题到形式命题的映射审查。 |
| [LeanDojo-v2](https://github.com/lean-dojo/LeanDojo-v2) | Apache-2.0 框架；外部模型与依赖另计 | 仓库跟踪、数据、训练、检索与证明器部署 | 不宜重复开发训练体系；更适合通过产物接入。 |
| [DeepSeek-Prover-V2](https://github.com/deepseek-ai/DeepSeek-Prover-V2) | 权重及示例公开，适用独立的 [模型许可证](https://github.com/deepseek-ai/DeepSeek-Prover-V2/blob/main/LICENSE-MODEL) | 专门生成 Lean 证明 | 模型、开放权重与完整科研工作流须分开比较。 |
| [Aletheia / Gemini Deep Think](https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/) | 有官方研究说明；本次未找到完整代理实现 | 自然语言候选生成、核验、修订及承认失败 | 强化明确停止和局部失败记录；自然语言核验仍需审查，不宣称模型能力对等。 |
| [Aristotle](https://www.harmonic.fun/aristotle/) 与 [数学研究计划](https://aristotle.harmonic.fun/sponsorships) | 托管服务；本次未找到完整后端 | 机器核验及已证、反驳、未决的区分 | 当前官网突出 C/Verilog，研究计划仍提及 Lean，须区分入口和访问范围；SDK 公开不代表后端开源。 |
| [AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) 与 [v3 / Agentic Scientist](https://github.com/SakanaAI/AI-Scientist-v3) | v2 当前为 [带用途限制的源码许可证](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/LICENSE)；v3 标注 Apache-2.0 | 实验搜索与论文流水线；v3 包括基线、消融、封闭最终评测、容器和运行记录 | 学习执行能力、评价隔离和示例；不能把所有版本统称同一种开源许可，也不能把论文生成当成真实性判据。 |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | [MIT](https://github.com/SamuelSchmidgall/AgentLaboratory/blob/main/LICENSE)，外接模型 | 文献、实验、报告与可调人工参与 | 学习完整易用入口；人工参与并非本项目独有。当前项目缺少自动执行和连接器。 |
| [PaperQA2](https://github.com/Future-House/paper-qa) | Apache-2.0，外部模型与检索另计 | 科学文献检索、证据提取和带引用回答 | 后续接入应保留原文、检索范围及假设匹配；检索分数不能证明引理。 |
| [Google AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) 与 [2026 更新](https://research.google/blog/a-new-era-of-innovation-google-research-at-io-2026/) | 托管／研究访问；本次未找到完整实现 | 多代理假设生成、反思、排序、演化及专家协作 | 学习路线多样性和廉价证伪；排序胜出不代表命题成立。公开工作已扩展到 Gemini for Science。 |
| [Kosmos / Edison](https://advances.edisonscientific.com/research/announcing-kosmos/) 与 [数据接入更新](https://edisonscientific.com/news/expanding-kosmos-data-access-capabilities) | 商业托管平台；本次未找到完整实现 | 结构化研究记忆、文献／代码来源追踪和数据获取 | 可追溯性并非我们的独创；应突出本地可查记录、证明依赖与人工接受机制。 |
| [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) 与 [2026 更新](https://deepmind.google/blog/alphaevolve-impact/) | 托管／研究系统；本次未找到完整生产实现 | 自动评价驱动的演化代码搜索 | 学习可执行的廉价筛选；优化指标与证明普遍命题有不同证据要求。 |

## 当前优势

较有说服力的定位是：**面向长期数学研究、由研究者掌握结论接受权的
证据与决策工作流**，尤其适合尚未全部形式化的自然语言证明。
优势来自已有机制的组合，不能逐项宣称原创或独有。QED 和
MathResearch Ledger 尤其接近；后者也已区分核验、暂存记录与人工接受：

1. **命题、路线、轮次分离**：一次候选失败只排除明确范围，不会自动
   否定整个路线或定理目标。
2. **推导来源与证明依赖明确**：不同代理重复同一决定性来源，不会被
   当作两条独立证明；必要依赖和循环风险可检查。
3. **数学预检与人工决策**：先检查候选的适定性、尺度、量词和盲区，
   再投入长推导；路线与正式结论变更必须明确批准。
4. **跨轮次积累**：原始产物、修正、失败范围和待解缺口可持续追踪。
5. **本地可读可迁移**：文本、JSON、双语证明图和保留本地修改的升级，
   减少对某个聊天或服务持续可用的依赖。

这些是代码与协议中可观察的设计特征，尚不能证明更高的正确率、研究
速度或定理难度。独立任务也不能机械保证推理独立或严格遵守阅读顺序。

## 缺口、改进与后续验收

| 优先级 | 原有缺口 | 本次 2.7.0 改进 | 后续验收标准 |
| --- | --- | --- | --- |
| P0 | 本机假设、公开入口不足 | 中英文首页、MIT、发布扫描、清洁公开提交 | 全新克隆能按文档复现，旧私人上下文不进入公开历史。 |
| P0 | 外部计算缺少具体回传契约 | 统一证据记录检查及原始文献逐项适用性模板 | 后续实现真实 Lean/CAS 重放与命题映射审查；当前仅核验元数据和内容。 |
| P0 | 难直观看到“计算不等于证明” | 可离线运行的 100 案例数学教学示例 | 再补多个数学方向的已审示例，不从有限检验推断无限结论。 |
| P1 | 数学规则不能直接套用实验科学 | 独立 AI4S 脚手架、冻结实验计划、带基线和保留测试的合成实验 | 在充分语义测试后增加科学命题结构、独立重复、不确定性和数据连接器。 |
| P1 | 协议复杂、手工操作较多 | 短入口、明确宿主边界、双语角色提示词 | 测量上手成本和单位人工审查时间内的有效进展，不为自动化削弱批准要求。 |
| P1 | 无工作流效果验证 | 明确能力边界和预注册比较方案 | 在相同模型、算力和人工预算下，对比单聊天与轻量多角色工作流。 |
| P2 | 缺少自动预算计量与服务适配 | 模板要求资源预算，路线图区分已实现与计划 | 实现有停止、取消和成本凭据的适配器，保留配置以便复现。 |

## 最直接对照带来的取舍

QED 的自动自然语言证明搜索和分阶段核验更完整，本次没有实现等价的
代理运行时。MathResearch Ledger 已有 MCP 连续研究入口及依赖版本
新鲜度机制，本次也没有实现这些能力。因此，人工接受、持续记忆与
来源追踪不能宣传为独有；更适合验证的差异是数学预检、先独立后比较
的审查、路线证据复盘、负责人批准与保留项目状态的升级机制的组合。
以后可通过经过审核的证据适配，而不是直接接受外部系统的状态决定。

## 应如何验证优势

以下仅为评价方案，尚未实施：选择已知证明重构、植入的错误命题、
局部失败路线、形式化命题错配及小型合成实验，分开发与封闭评测题。
在匹配模型、Token、算力和人工预算下，对比单聊天、轻量多角色及完整
账本流程。由不知道实验分组的外部审查者评价正确性、伪造引用、范围
夸大、证据独立、失败停止、复现和有效进展耗时。披露失败、成本、
重复种子及污染风险；不能用代理打分或验证器通过代替数学评价。

## 产品取舍

建议一个仓库维护 **AI4Math 核心 + AI4S 试验 profile**。只共享跨领域
仍有明确意义的证据与决策原则；数学证明和经验支持保留各自语义。
先用可审产物连接专业证明器、检索和实验工具，再逐步发展执行能力。
本次未复制这些参考项目的代码、权重或数据。
