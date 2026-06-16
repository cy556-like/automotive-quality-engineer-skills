启动MSA（测量系统分析）流程。

## 执行步骤

1. 读取 `skills/msa/SKILL.md` 获取MSA完整工作流

2. 确认MSA类型：
   - 计量型MSA（Gage R&R）— 连续数据
   - 计数型MSA — 通/止规、目视检查

3. 对于计量型MSA（Gage R&R）：
   - 确认零件数（通常10个）、操作者数（通常3人）、重复次数（通常3次）
   - 引导用户准备数据
   - 计算并评估：%GRR、ndc、偏倚、线性

4. 对于计数型MSA：
   - 评估操作者一致性、Kappa值
   - 风险分析（误判率/漏判率）

5. 生成MSA报告：
```bash
python3 scripts/generate_quality_doc.py --type xlsx --template gage_rr --data <data.json> --output <output.xlsx>
```

## 参数

- $ARGUMENTS: 测量系统描述，例如 "卡尺Gage R&R"

## 示例

```
/msa 卡尺Gage R&R
/msa 目视检查一致性分析
```
