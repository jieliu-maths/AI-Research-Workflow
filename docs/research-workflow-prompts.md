# Reusable prompts for the research workflow

The canonical reusable kernel in the examples below is the standalone
repository directory:

`<WORKFLOW_LIBRARY>`

The source copy keeps this angle-bracket placeholder so the repository remains portable.
`workflow init`, `migrate`, and `upgrade` replace it automatically in the copy
installed into a mathematical project. If an older installed copy still shows
the literal placeholder, Codex must first locate the unique verified standalone
library in the saved-project list. A legacy `.research-workflow.json`
`source_hint` is only an untrusted candidate and is never sufficient by itself.
Use the verified repository's `workflow` launcher; no source research-project
path is required.

## Prompt 0 — safely locate the library and upgrade an older project

This short bootstrap prompt contains no machine path and is the recommended
entry point for an older project.

```text
请升级当前旧项目，但不要信任当前项目 `.research-workflow.json` 中已有的 `source_hint`，也不要从任何数学项目目录安装工作流。

先调用 Codex 项目列表，寻找独立的 `AI Research Workflow` 项目。候选根目录必须含 `.research-workflow-library.json`，其中 `kind` 必须为 `standalone-proof-ledger-research-workflow-library`、`library_id` 必须为 `ai-research-workflow-kernel`；再执行 `"<候选目录>/workflow" identify` 核对相同身份，并执行 `"<候选目录>/workflow" self-check`。候选目录自身若含 `.research-workflow.json`，立即排除。若没有唯一合格候选，只向我询问路径，不要猜测。

确认唯一工作流库后，完整读取该目录的 `docs/research-workflow-prompts.md`，找到 “Prompt A — migrate or upgrade an older project”，把其中 `<WORKFLOW_LIBRARY>` 解释为已验证的工作流库绝对路径，并严格执行整段 Prompt A。当前 Codex 项目才是升级目标；工作流库和其他数学项目都不是目标。
```

## Prompt A — migrate or upgrade an older project

```text
请在当前项目中迁移或升级 proof-ledger agentic research workflow。

最新工作流内核位于：
<WORKFLOW_LIBRARY>

执行任何迁移命令前，必须先确认工作流来源；即使上一行已经是绝对路径，也不能跳过：
1. 先调用 Codex 项目列表，寻找独立的 `AI Research Workflow` 项目；候选根目录必须含 `.research-workflow-library.json`，且其中 `kind` 为 `standalone-proof-ledger-research-workflow-library`、`library_id` 为 `ai-research-workflow-kernel`；
2. 对候选执行 `"<候选目录>/workflow" identify`，只接受返回同一 `kind` 与 `library_id` 的目录；随后执行 `"<候选目录>/workflow" self-check`；
3. 当前数学项目的 `.research-workflow.json` 中的 `source_hint` 只能作为备用候选。只有它也通过上述身份检查，且目录自身不含 `.research-workflow.json`，才可采用；不得因为路径中存在 `workflow` 文件就信任它；
4. 若没有唯一通过检查的候选，只向我询问工作流库的绝对路径，不要猜测。绝对不要从任何数学项目目录安装工作流。
确认成功后，把本提示其余位置同名的工作流库占位符都解释为这个已验证的绝对路径。

本提示同时明确授权：把当前任务作为本项目的 Director，并在升级完成后检查或恢复另外两个独立顶层 Codex 任务 Researcher 与 Critic。三个任务必须出现在侧栏中并直接共享当前保存的项目目录；不得把 Researcher 或 Critic 建成 Director 的子 agent。侧栏标题固定为 `0 Director`、`1 Researcher`、`2 Critic`。

目标是让当前项目获得版本化的 validator、machine-readable state schema、proof-map Dashboard、完整版本化 run 模板、evidence lineage 和可持续升级机制，同时完整保留当前项目自己的数学内容、历史 run、失败路线和人工审批边界。

请执行以下工作：

1. 先阅读当前项目的 AGENTS.md、WORKFLOW.md、PROJECT_CHARTER.md、STATE.md、research/proof_ledger.md、research/proof_map.md、research/route_matrix.md、agents/protocol.md 和 runs/_template/。把这些文件视为当前项目的 canonical 来源，不要从新内核复制任何具体 claim、route、公式、参数或数学 guardrail。
2. 检查当前项目是否已有 .research-workflow.json：
   - 如果没有，执行 `"<WORKFLOW_LIBRARY>/workflow" migrate .`；
   - 如果已有，先执行 `"<WORKFLOW_LIBRARY>/workflow" status .`，再执行 `"<WORKFLOW_LIBRARY>/workflow" upgrade .`。
3. 审核预览中的 resolved target、整套 run-template replacement、managed-file changes、managed-block changes、conflicts 和 state-mapping gate。不得覆盖本地修改过的 managed file 或 managed block；有冲突时读取双方内容，给出最小合并方案，保留项目特有规则。
4. 明确区分 `route_id` 与 `run_id`：数学路线统一映射为 `route:<slug>`，一次执行统一为 `R<number>`。旧项目若曾把同一个 R 编号同时用于路线和 run，只做结构拆分，不改变路线结论、proof status 或批准状态；无法唯一判断的映射必须留给我审批。保留 `formal`、`formal_exact`、`conjectural`、`established` 的原始语义，不得把 `formal` 自动升级为 `formal_exact`。
5. 如果没有冲突，或者冲突已通过不改变数学含义的最小合并解决，则在同一命令末尾增加 `--apply` 并执行。确认工具先进行无写入 preflight，且失败时已回滚。不要删除文件，不要重写历史 raw artifacts。
6. 确认 `brief.md`、`task-brief.md`、`learning-note-Txxx.md`、`status.md`、`amendments.md`、`resolution-Txxx.md`、`state_update_proposal.md`、`director-run-summary.md` 和 `route-review.md` 都是同一模板版本；确认同时存在 `manifest.json`、`Txxx.json`、`state-transition.json`、`orchestration.json`、`route-review.json` 及对应 JSON Schema。严格逻辑前提只写入 `claim.depends_on`；`supports/tests/blocks/warns_circularity` 作为非严格 proof-map 边；`blocking` 必须由已审批的 `theorem_targets` 依赖闭包推导。
7. 如果当前项目还没有 research/machine/project-state.json：扫描 STATE、proof ledger、proof map、route matrix 和已经裁决的 run artifacts，生成 research/machine/project-state.proposal.json。逐项记录 claim 状态、依赖、blocking、route canonical/operational 状态、精确 rejection scope、evidence path/hash 和 derivation_roots。任何无法从 canonical 文本唯一确定的字段都标为需要人工判断；不要用推测补齐，也不要把 proposal 当成正式 machine mirror。
8. 如果已有 machine state，只做 schema/kernel 兼容性升级；不得用最新内核项目的 project-state.json 覆盖它，也不得刷新 canonical hash 来掩盖 drift。
9. 对历史 run 只可先执行 `workflowctl.py hydrate-run . Rxxx --proposal-only` 生成哈希清单和待审映射；不得自动生成正式 sidecar。运行 Python 语法检查、内核自动测试、JSON 解析、workflow status、researchctl validate、`validate-proposal`、summary、dashboard 和 `dashboard-proposal`。确认两种 Dashboard 都可在中文与英文界面之间切换，且切换不会翻译或改写项目自己的数学命题、路线结论与备注。Dashboard 主视图必须使用定理目标、证明前提、数学地位、路线结论、保留结果与未决缺口等数学科研语言；记录格式和运行诊断只能折叠在“研究记录检查”的技术详情中。若 migration 尚待语义映射，清楚说明 warning；proposal Dashboard 必须醒目标注“NOT CANONICAL”。
10. 检查 research/machine/workspace-roles.json：调用任务重命名能力（set_thread_title）把当前任务登记并重命名为 `0 Director`；先复用仍可访问且确实属于当前项目的 `1 Researcher`、`2 Critic`，只为缺失、关闭或不可访问的这两个角色新建任务。创建前用 Codex 项目列表精确解析当前 saved project；每个缺失角色各调用一次新建任务能力（create_thread，不是 spawn_agent），并明确选择“直接使用 saved project/local”，不要创建隔离 worktree。两个初始消息分别要求读取 AGENTS.md、WORKFLOW.md、agents/protocol.md 和自己的角色文件，运行 validator，只回复角色就绪状态，不选择路线、不启动 run。不得调用 spawn_agent 或任何子 agent 机制替代它们。使用 wait_threads 等待两个任务都返回就绪或明确报错，把 project ID、project path、三个 task/thread ID、host ID、固定标题和状态写入 workspace-roles.json；Director 标记 is_current_task=true，另外两者为 false。若任一角色创建失败，报告“workspace bootstrap incomplete”，不得静默降级。
11. 最终按以下顺序汇报：版本变化；实际修改；保留的项目文件；冲突；机器状态映射结果；三角色任务及其侧栏标题；验证结果；需要我批准的 canonical 变更。没有明确批准时，不修改 proof-ledger status、STATE 的数学结论、全局 notation 或 paper/main.tex。

不要只给迁移建议；在上述安全边界内直接完成可执行的迁移或升级与验证。只有数学状态映射、冲突中的数学含义或新的权限确实需要我决定时才停下来请求确认。
```

## Prompt B — initialize a new project

```text
请在当前目录建立一个新的 proof-ledger agentic research project。

项目名称：<填写项目名称>
研究主题或初步目标：<填写问题、方程或研究方向>
已知关键文献或约束：<可选；没有就写“暂无”>
可复用工作流内核位于：
<WORKFLOW_LIBRARY>

执行任何初始化命令前，先调用 Codex 项目列表定位独立的 `AI Research Workflow` 项目。候选必须含 `.research-workflow-library.json`，其中 `kind` 为 `standalone-proof-ledger-research-workflow-library`、`library_id` 为 `ai-research-workflow-kernel`；并且 `"<候选目录>/workflow" identify` 返回相同身份、`"<候选目录>/workflow" self-check` 通过、候选目录自身不含 `.research-workflow.json`。旧项目的 `source_hint` 只能作为经过同样检查的备用候选，不能直接信任。没有唯一合格候选时只向我询问绝对路径，不要猜测。定位后，把本提示其余位置同名的工作流库占位符都解释为该路径。

本提示明确授权：当前任务就是本项目的 Director；在我批准准确目标和技术路线之后，调用任务重命名能力（set_thread_title）把当前任务重命名为 `0 Director`，并新建两个独立顶层 Codex 任务 `1 Researcher` 与 `2 Critic`。三个任务必须出现在侧栏中并直接共享新项目的 saved project 目录。不得把 Researcher 或 Critic 作为 Director 的子 agent。

请执行以下工作：

1. 先检查当前目录，保留所有已有文件。执行 `"<WORKFLOW_LIBRARY>/workflow" init . --project-name "<填写项目名称>"`。审核 resolved target 和冲突后，在不会覆盖已有内容的前提下，在同一命令末尾增加 `--apply` 并执行。
2. 确认已建立 AGENTS.md、WORKFLOW.md、PROJECT_CHARTER.md、STATE.md、research/、runs/_template/、agents/protocol.md、schemas/、tools/、tests/、dashboard/、项目级 research-workflow Skill 和 .research-workflow.json。检查整套 run 模板、`manifest.json`、`Txxx.json`、`state-transition.json`、`orchestration.json`、`route-review.md`、`route-review.json`、state-mapping proposal 模板及对应 JSON Schema 都存在。初始化结果必须是空的 S0 machine mirror：没有虚构的 proved claim、approved route、theorem target 或 active run。
3. 先整理我提供的初步信息：暂定问题、预期价值、希望得到的结果类型、已知文献、约束、已有证据与可接受范围；缺失项列为待确认问题，不得自行假定。然后调研 primary literature，综合分析可行性、价值、准确目标、主要困难与创新风险，并给出精确 theorem/page 定位。
4. 草拟 PROJECT_CHARTER.md、research/problem.md、notation.md、assumptions.md、core_difficulties.md 和 route_matrix.md；给出三到五条机制上不同的候选路线，包括建议的最佳路线、独立替代路线和便宜的 falsification route，并说明推荐理由、失败风险与判别试验。先用数学语言向我提交“准确目标 + 路线比较 + 推荐路线”审批；审批前不得建立正式证明框架、激活路线或启动构造 Run。
5. 为初始 proof ledger 和 proof map 生成 proposal，使用 P 编号描述可验证的数学命题，明确 dependencies、blocking、evidence gate 和最便宜的反证测试。数学路线 ID 使用 `route:<slug>`，run ID 使用 `R<number>`，不得混用。生成 research/machine/project-state.proposal.json，但在我批准 theorem target、phase boundary、外部输入和技术路线前，保持正式 project-state.json 为 S0，不启动路线构造 run。
   对每条候选路线同时写明首次构造前的 candidate preflight：项目认可的函数空间与范数、需要重算的维数相关伴随/边界项、第一非零变分及所需一致尺度、必须商去的既有恒等式、正反两侧及远场/低频/集中测试、截断运动与尾项清单，以及最小可能失败范围。
6. 只有在我批准准确目标与技术路线后，才建立正式 proof ledger、proof map 与第一轮证明框架。确认新项目已经作为 Codex saved project 可被精确解析；如果尚未保存为项目，停止并告诉我需要先把该目录加入 Codex 项目列表，不得改用子 agent。调用任务重命名能力（set_thread_title）把当前任务重命名为 `0 Director`，并分别调用两次 Codex 新建任务能力（create_thread，不是 spawn_agent）创建 `1 Researcher`、`2 Critic`。两个新任务都直接使用 saved project/local，不能使用隔离 worktree；初始消息要求读取项目协议和自己的角色文件、运行 validator、只回复 ROLE_READY，不启动 Run、不改变数学状态。使用 wait_threads 等待二者就绪；任一失败都报告“workspace bootstrap incomplete”，不得调用 spawn_agent 或其他子 agent 机制补位。
7. 以 research/machine/_template/workspace-roles.json 为模板，写入 research/machine/workspace-roles.json，记录 project ID、项目绝对路径、三个独立 task/thread ID、host ID、固定侧栏标题、模型、推理强度和状态；`0 Director` 必须标记 is_current_task=true，另外两者为 false。该文件只记录任务分工，不表示任何路线或命题获得批准。随后再次运行 researchctl validate。
8. 运行 Python 语法检查、JSON 解析、workflow status、researchctl validate、summary、dashboard 和 `python3 tools/researchctl.py report`。确认 Dashboard 可切换中英文且不改写数学内容；确认核心数学记录已经生成 `report/project-summary.md`、`.tex` 与 `.pdf`。
9. 最终先用数学语言汇报：目标问题、已知边界、主要困难、候选路线和最小可攻击瓶颈；然后列出创建的工作流文件、三个角色任务的侧栏标题与就绪状态、验证结果，以及需要我依次批准的 literature gate、problem gate 和 route gate。

不要复制工作流源仓库或任何其他项目的 P/R 数据、公式、参数、失败结论、证据哈希或数学 guardrail。不要因为目录初始化成功就宣称数学项目已经初始化完成；数学状态必须通过对应的人类 gate。
```

## Prompt D — operate one approved research run

```text
请作为当前项目的 Research Director，执行已经获得明确批准的当前 Run；不要自动开启下一 Run，也不要改变已批准的数学路线。

开始前读取 AGENTS.md、WORKFLOW.md、PROJECT_CHARTER.md、STATE.md、research/problem.md、research/notation.md、相关 proof-ledger/proof-map 行、agents/protocol.md、当前 Run 的 brief/status/amendments/orchestration，以及 research/machine/workspace-roles.json。先运行 researchctl validate；若 canonical drift 影响可靠性，只准备同步 proposal，不要静默刷新。

使用侧栏中共享同一 saved project 的独立 Director、Researcher、Critic 顶层任务。不得用 subagent 替代 Researcher 或 Critic。复用当前未完成任务，避免重复派发。

对每个新候选，在长推导前冻结并执行 candidate preflight：

1. 写出被检验的精确公式或参数化候选类；
2. 指明 canonical function space/norm，并证明候选在该拓扑中有定义、连续且尺度一致；
3. 按当前维数、方程约定和边界重新计算 adjoint、commutator、integration by parts；
4. 先计算参考解处的第一非零变分，和下游不等式需要的 uniform margin 比较；若用归一化修复尺度，必须同时求导归一化并重新测试 shrinking sequences 上的连续性；
5. 从完整 tangent covector 中商去所有已知 conservation/modulation/orthogonality/virial derivation roots，不能只比较一个特殊方向，也不能把 quotient norm 的 upper bound 说成 exact dependence；
6. 测试定理要求的全部符号方向、special solutions、远场/低频/集中扰动、对称方向和极限参数；
7. 完整列出 moving cutoff、annular commutator、exterior bulk、primitive boundary 与 tail；
8. 失败时分别说明 raw formula、locally repaired formula、精确被排除的 candidate class 和尚未测试的 alternatives。

每个 Task 只处理一个 claim，完整保存冻结 dispatch，并包含 candidate_class、canonical_topology、quotient_dependencies、scaling_regime、stress_tests、symbol_scope。Researcher 完成后由 Director 审核，再按预先冻结的独立读取顺序交给 Critic；原始产物不得静默改写，实质修正需要 resolution 和再次确认。

Director 在同一轮中持续等待可见角色任务返回，并在当前授权范围内继续依赖已满足的下一 Task。只有到达明确 human gate、Run 边界、新权限/新数学路线需求或真实基础设施故障时才停止。

每次面向我的汇报只写数学内容：当前定理目标、精确成立或被否定的命题、决定性公式/反例、对证明链的影响、仍缺什么、下一个最小数学问题及其正反结果。任何新符号第一次出现前，解释它表示什么、依赖哪些变量、尺度为何、为何需要、与既有记号的关系，以及只是局部记号还是建议加入全局 notation。除非可靠性受到影响或我主动要求，不汇报 hash、validator、文件清单、任务生命周期或其他计算机审计信息。

Run 结束时写数学化的 Director summary、failed/success learning note 和 state update proposal。没有我的明确批准，不修改 canonical proof status、全局 notation 或 paper/main.tex；没有新的路线批准，不开始下一 Run。

若同一路线连续三次 Run 都没有获得经 Critic 审核的决定性支撑，或更早出现重复障碍、重复推导根、结构性失败或循环论证，立即停止新的构造 Run。先由 Researcher 整理现有证据并针对实际困难重新系统检索原始文献，再由 Critic 独立审核，最后由 Director 用数学语言提出继续、修补、缩小、分支、暂停或局部否定的建议，等待我审批。

当我批准数学状态更新后，同步更新项目核心文件与 research log，并运行 `python3 tools/researchctl.py report`，重新生成 Markdown、LaTeX 与 PDF 三种阅读版本。
```

## Prompt C — repair only the three-role Codex workspace

```text
请为当前已安装 research workflow 的项目修复三角色运行拓扑。本提示明确授权你创建缺失的独立 Codex 任务。

1. 当前任务作为 Director。读取 AGENTS.md、WORKFLOW.md、agents/runtime_config.md、agents/protocol.md，以及 research/machine/workspace-roles.json（如存在），并调用任务重命名能力（set_thread_title）把当前任务重命名为 `0 Director`。
2. 从 Codex 项目列表精确找到当前 saved project。复用仍可访问的正确角色任务；只为缺失、关闭或不可访问的角色创建顶层任务，使侧栏中最终恰好有 `0 Director`、`1 Researcher`、`2 Critic`。三个任务直接使用 saved project/local、共享同一目录，不使用隔离 worktree。
3. 禁止使用 spawn_agent、subagent 或 Director 内部代理来替代上述任一角色。三者必须有不同的 task/thread ID。初始消息只要求读取项目协议、运行 validator 并回复 ROLE_READY；不要启动数学 run、选择路线或改变 canonical state。
4. 使用 wait_threads 等待三者返回就绪或明确失败；把识别出的 project ID、绝对项目路径、task/thread ID、host ID、标题、模型、推理强度和状态写入 research/machine/workspace-roles.json，并运行 `python3 tools/researchctl.py validate`。
5. 最终列出三个侧栏任务的标题和状态。任一任务无法建立时明确报告“workspace bootstrap incomplete”，不得静默降级。
```
