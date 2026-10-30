# AI4S profile — experimental / AI4S 通用科研试验版

The main release is **AI4Math-first**. This optional profile reuses evidence
lineage, frozen questions, separate review, scoped failure, and owner decisions
for computational and empirical research. It has its own scientific protocol:
mathematical proof statuses are not reused as empirical truth labels.

```bash
./workflow init-ai4s ../my-science-project --project-name "My science project"
./workflow init-ai4s ../my-science-project --project-name "My science project" --apply
```

The parent directory must exist and the target must be new. The preview does
not write; apply stages a complete scaffold before publishing the directory.
Existing projects and symlinked target ancestors are refused. The scaffold
contains a charter, scientific claim ledger, independent-role instructions,
experiment plan, and the portable evidence inspector. It starts with no
approved hypothesis and creates no app tasks.

**Implemented:** fresh scaffold, experiment protocol, provenance/controls/sealed
evaluation templates, shared evidence bundle inspection, offline synthetic demo.

**Not implemented:** managed upgrades/migration, automatic experiments, scientific
claim graph validation, role registry, dashboard/report generation, external
data connectors, statistical analysis services, or a wet-lab execution system.
Do not apply AI4Math `migrate`/`upgrade` to this profile.

中文：主版本聚焦 AI4Math。AI4S 是可独立初始化的试验版，增加数据来源、
许可、对照、消融、固定划分、不确定性、资源预算和复现要求。
它复用证据与人工决策原则，但不把数学证明状态套用到实验结论上。
目前只支持新目录初始化，不支持自动实验、迁移升级或数学看板。
