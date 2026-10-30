# AI Research Workflow

**以 AI4Math 为核心，用明确证据、独立审查和人工批准推进长期数学研究。**

[English](README.md) · [调研与比较](docs/landscape-review.zh-CN.md) ·
[AI4S 试验版](profiles/ai4s/README.md) · [MIT 许可证](LICENSE)

当前版本 **2.7.0**。这是一套可复用的科研工作流内核，帮助研究者在多轮
AI 协作中维护定理目标、证明依赖、推导来源、失败候选和未解决缺口。
生成的论证与计算结果须经过相应证据审查和人工批准，才可更新正式结论。

## 核心能力

- **证明账本**：区分定理目标、证明义务、技术路线、执行轮次和证据，
  展示必要依赖、阻塞点和循环论证风险。
- **独立审查**：Director、Researcher、Critic 使用三个独立可见的顶层
  任务；Critic 先独立推导，再阅读构造。角色名称本身不代表证据独立。
- **限定失败范围**：保留被排除的精确候选类，避免把单个公式失败解释成
  整条路线不可能；无决定性进展时触发路线复盘及文献更新。
- **人工决策**：目标与路线选择、命题升级、全局记号和论文转入均由
  负责人明确批准。
- **持续记录**：版本化模板、事务安装、保留本地修改的升级、双语证明图，
  以及安装后项目的 Markdown、LaTeX、PDF 阅读副本。
- **外部证据接入**：核验来自证明器、计算和实验的证据记录，保留原始范围。

项目提供协议与本地工具，不内置大模型、证明搜索引擎、文献检索服务、
自动代理调度器或执行沙箱。目前尚无对照实验证明它能提高定理解决率或
科研生产率；结构一致性检查通过也不代表数学结论正确。

## 运行条件

- Python **3.10+**；内核和离线示例仅使用标准库。
- 下列命令需要 Bash 和 Git；CI 覆盖 macOS、Linux。Windows 可使用 WSL，
  但尚未单独验证该平台。
- 当前支持的角色协作需要 Codex 桌面版保存的项目及创建三个独立可见
  本地任务的能力。安装器只创建文件，不创建侧栏任务。其他宿主可以
  参考协议，目前没有随附并验证过的等价宿主适配器。
- 可选 XeLaTeX：用于 PDF 阅读副本。缺少时保留 Markdown、LaTeX，明确
  报告 PDF 未生成。
- 外部模型、证明器和服务需要各自的配置、权限与许可；离线示例和自检
  不需要 API Key。

## 快速上手

```bash
git clone https://github.com/jieliu-maths/AI-Research-Workflow.git
cd AI-Research-Workflow
./workflow identify
./workflow self-check
```

先体验数学教学示例，输出目录须尚不存在：

```bash
python3 examples/ai4math/verify.py --output-dir /tmp/ai4math-demo
python3 tools/evidencectl.py /tmp/ai4math-demo/evidence.json
```

它精确检验 100 个整数案例，明确保留从有限检验到普遍证明的缺口。
见[示例说明](examples/ai4math/README.md)。

预览一个新的 AI4Math 项目，核对名称与目录后应用：

```bash
./workflow init ../my-math-project --project-name "My math project"
./workflow init ../my-math-project --project-name "My math project" --apply
```

在 Codex 中把目标目录打开为保存的项目，使用[中文提示词](docs/research-workflow-prompts.md)
或[英文提示词](docs/research-workflow-prompts.en.md)。先提供研究问题、已知
文献、约束和期望结果。当前聊天作为 `0 Director`；准确目标与路线经你
批准后，再建立同项目的独立 `1 Researcher` 和 `2 Critic`。新目录初始
处于 S0，不含任何已批准的定理、命题或路线。

## 日常操作

在**已安装的数学项目**中运行：

```bash
python3 tools/researchctl.py validate
python3 tools/researchctl.py summary
python3 tools/researchctl.py blockers P001
python3 tools/researchctl.py dashboard
python3 tools/researchctl.py report
```

`P001` 是命题编号示意，须换成项目中已登记的编号。生成看板后打开
`dashboard/index.html` 切换中英文界面；命题和公式保持原文。负责人批准
并同步数学记录后，再生成阅读副本。当前源仓库不含项目数学状态，
在源仓库使用 `./workflow self-check`。

Critic 的“暂时经受住攻击”不等于证明。数值实验、有限检验和外部形式化
产物均须审核适用范围与命题对应关系。见[证据契约](docs/evidence-bundles.md)
和[完整数学协议](WORKFLOW.md)。

## 旧项目接入与升级

从通过身份核验的工作流源目录运行：

```bash
./workflow migrate /path/to/legacy-project
./workflow upgrade /path/to/installed-math-project
```

先预览，审阅后添加 `--apply`。迁移保留既有数学文件，并可能要求人工
确认语义映射；升级只替换未修改的受管文件及标记区块，本地修改作为
冲突保留，既有研究轮次不被覆盖。安装后，本地工具可独立运行；以后
升级仍需一个已核验的工作流源仓库。安装的工具附带 `WORKFLOW-LICENSE`，
它不会替你选择研究成果的许可证。

## AI4S 通用科研试验版

该版本另有科学实验协议，增加数据来源、对照、冻结划分、不确定性、
复现与资源预算。它复用证据和人工决策原则，保留自己的经验结论用语。

```bash
./workflow init-ai4s ../my-science-project --project-name "My science project"
./workflow init-ai4s ../my-science-project --project-name "My science project" --apply
python3 examples/ai4s/experiment.py --output-dir /tmp/ai4s-demo
python3 tools/evidencectl.py /tmp/ai4s-demo/evidence.json
```

父目录必须存在，目标目录须尚不存在。目前支持新项目脚手架、实验计划
和证据检查，尚无自动实验、受管升级、科学命题图验证、看板或报告生成。
见[试验版范围](profiles/ai4s/README.md)。

## 文档与开发

- [使用说明](使用说明.md)：常用操作入口。
- [中英文调研](docs/landscape-review.zh-CN.md)：已有工具、优势、缺口和证据边界。
- [路线图](ROADMAP.md)：已实现功能、下一阶段及评价方法。
- [贡献指南](CONTRIBUTING.md)：运行检查和提交要求。

使用 MIT 许可证，版权所有 2026 Jie Liu。相关项目仅作为研究参考，
本项目不捆绑或重新授权它们的代码、模型权重、数据或服务。
教学示例均为独立构造，不含私人研究结果。
