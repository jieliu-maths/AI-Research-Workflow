# AI4Math teaching example / 数学工作流教学示例

From the repository root, choose a new output directory:

```bash
python3 examples/ai4math/verify.py --output-dir /tmp/ai4math-demo
python3 tools/evidencectl.py /tmp/ai4math-demo/evidence.json
```

The script checks exactly 100 integer cases of the identity “the sum of the
first n odd positive integers equals n squared,” with n ranging from 0 to 99.
It uses exact Python integer arithmetic and returns a portable evidence bundle.
It requires no API key, model download, Lean installation, or network access.

Read the result as a **finite computation**, not a proof for every natural
number. The universal statement requires an argument such as induction, with
its own independent review. This fixture does not instantiate an approved
research run or change canonical mathematical state.

The intended role sequence is:

1. Director freezes the exact question and scope, subject to owner approval.
2. Researcher produces an argument and any authorized calculation.
3. Critic first develops a baseline independently, then checks the argument
   and whether the finite calculation is being overclaimed.
4. Director reports the precise consequence; the owner decides any state change.

Suggested Director report for this fixture: “The identity passes all 100
specified finite cases. This excludes a counterexample in that range but does
not establish the universal theorem. The remaining task is a complete proof.”

中文：运行上面两条命令即可离线体验证据生成与核验。100 个整数案例的
精确计算不会自动成为无限范围的证明；教学结果也不会写入任何正式研究
项目。三个角色的独立审查和人工批准仍是实际研究的必要步骤。
