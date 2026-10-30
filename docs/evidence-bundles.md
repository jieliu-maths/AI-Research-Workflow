# Portable evidence bundles / 可移植证据包

An external theorem prover, symbolic computation, scientific experiment, or
literature assistant can return evidence to this workflow. Its success status
never promotes the project's claim ledger automatically.

外部证明器、符号计算、实验或文献工具的输出只能作为待审证据，不能自动
升级命题状态。证据包用于记录和核验，不会执行其中的命令。

## Inspect a bundle

```bash
python3 tools/evidencectl.py /path/to/bundle/evidence.json
```

Paths inside the record are relative to the bundle directory by default. Use
`--root /path/to/evidence-root` only when the record is stored elsewhere.
The inspector checks fields, relative file paths, SHA-256 digests, and basic
outcome consistency. It rejects symlinks, path escapes, duplicate references,
and a passed formal certificate that declares placeholders. It does not
replay commands, inspect the code for correctness, verify a proof kernel, check
an axiom inventory, or certify the honesty of a reported outcome.

检查器核验元数据、文件内容和基本一致性，拒绝路径越界及符号链接。
它不会重新执行命令，也不会判定数学真实性、统计有效性或文献结论。

## Record format, version 1.0

```json
{
  "schema_version": "1.0",
  "status": "evidence_only",
  "kind": "finite_check",
  "statement": "The exact statement tested.",
  "scope": "The precise finite domain and assumptions.",
  "derivation_roots": ["The definitions and external results used."],
  "files": [{"path": "results.json", "sha256": "REPLACE_WITH_ACTUAL_SHA256"}],
  "execution": {
    "command": ["python3", "verify.py"],
    "tool_version": "Python VERSION",
    "exit_code": 0
  },
  "outcome": "passed",
  "limitations": ["A finite check does not prove an unbounded theorem."],
  "review_required": ["Independent code and scope audit; owner approval."]
}
```

The JSON above is a format illustration, not a valid certificate. To compute a
digest, use `hashlib.sha256(Path(...).read_bytes()).hexdigest()`. The runnable
examples produce complete bundles. Record commands as argument lists, with a
documented working directory and portable output placeholder where necessary.
Include input data, exact source, raw output/logs, dependency lockfiles, and
the toolchain configuration in `files` as applicable. Hashing a log preserves
its contents; it does not establish that the logged command actually ran.

## Evidence classes and review

| Kind | Required interpretation |
| --- | --- |
| `finite_check` | Exact arithmetic on an explicitly finite domain; no universal extrapolation. |
| `formal_certificate` | Submitted formal result; independently rerun its checker and audit the informal-to-formal statement mapping. |
| `numerical_experiment` | Floating-point or empirical evidence with declared data, seeds, error/uncertainty, controls, and limitations. |
| `source_audit` | Recorded source passage and applicability audit; `execution` must be `null`. |

For `formal_certificate`, add a `formal` object containing `theorem` (the exact
qualified identifier), `axioms` (an explicit list, possibly empty), and
`has_placeholders` (boolean). Include Lean/toolchain versions, dependency locks,
formal sources, full build output, and an axiom report in `files`. Check for
`sorry`, admitted axioms, unsafe assumptions, statement weakening, and hidden
dependencies during independent review. A field claiming an empty axiom list
is not itself evidence that no axioms were used.

Both a passed and a failed command are useful evidence: outcomes are `passed`,
`failed`, or `inconclusive`. A passed execution must report exit code zero;
a failed check may exit zero while finding a counterexample. An admission of
failure is not a rejected theorem or a rejection of an entire route.

In AI4Math, attach the reviewed bundle through a task's existing artifact
reference. A formal bundle may support `lean_certificate`; finite computations
need a scoped derivation audit, numerical work remains `numerical`, and source
audits need an exact hypothesis match. Existing claim vocabularies stay intact:
`formal_exact` denotes an exact identity in its stated formal model, not an
automatic synonym for “Lean checked.” The human evidence gate remains in force.

在 AI4Math 中，证据包通过现有任务产物引用接入。独立审查须确认命题、
假设、量词、依赖和核验范围，再由负责人决定是否更新正式记录。
AI4S 的数据分离、复现、误差与结论范围审查同样不可省略。
