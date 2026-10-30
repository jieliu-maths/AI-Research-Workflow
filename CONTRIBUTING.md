# Contributing / 贡献指南

Run `./workflow self-check` from the source repository before proposing a change.
Use Python 3.10+ and the standard library for kernel additions. Add regression
coverage for changes to state semantics, installation, evidence acceptance,
protected files, or path boundaries. Documentation-only edits need link and
command checks rather than tests that mirror the prose.

Keep mathematical targets, route decisions, and claim acceptance with the
project owner. Distinguish a consistency check, an empirical observation, and
an independently audited proof. Preserve existing run artifacts and local
project modifications. Document breaking schema changes and provide explicit
migrations rather than silently normalizing unfamiliar statuses.

Use synthetic teaching fixtures for public examples. Exclude personal paths,
credentials, unpublished project state, private run logs, and generated local
configuration. The publication check covers common patterns only; review the
release tree and the history being published. References to other systems
must use dated primary sources and distinguish source, model, data, and service
licenses. Do not vendor their code without reviewing the applicable license.

For a contribution, explain the concrete problem, resulting behavior, tests,
and remaining limits. Contributions are made under the repository's MIT License.
Report reproducible problems through GitHub Issues with the OS, Python/kernel
version, expected/observed behavior, and a minimal synthetic example.

中文：提交前自检；保持人工批准、证据范围与状态语义。只用合成案例，
不提交私人研究、密钥或本机配置。涉及安装、路径、证据和状态语义的
修改须有回归覆盖；描述问题、结果、验证及尚存限制。
