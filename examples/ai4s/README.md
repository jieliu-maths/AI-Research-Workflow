# AI4S synthetic example / 通用科研合成示例

```bash
python3 examples/ai4s/experiment.py --output-dir /tmp/ai4s-demo
python3 tools/evidencectl.py /tmp/ai4s-demo/evidence.json
```

Run from the repository root with a fresh output directory. This standard-library
example compares a constant baseline with a linear predictor on synthetic data.
It fits on 100 training samples (seed 11), selects the model on 40 validation
samples (seed 22), then evaluates that frozen choice once on 40 held-out samples
(seed 33). It retains the data, source, result, seed inventory, and file hashes.

The result is a numerical observation on one synthetic split. It establishes
neither a theorem nor real-world effectiveness, causality, significance, or
robustness across independent repeats. No actual experiment budget is spent
beyond this local CPU computation. No service receives data.

中文：本例展示“训练拟合—验证选择—一次保留测试”的最小复现实验，
包含常数基线、固定随机种子和原始数据。结果只适用于这一次合成数据
划分，不代表真实科学发现，也不构成数学证明或统计显著性结论。
