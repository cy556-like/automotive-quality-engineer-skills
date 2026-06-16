启动SPC（统计过程控制）分析。

## 执行步骤

1. 读取 `skills/spc/SKILL.md` 获取SPC分析完整工作流

2. 确认分析参数：
   - 数据文件路径（CSV/JSON）
   - 控制图类型：Xbar-R / I-MR / P / C / U
   - 规格上限(USL)和下限(LSL)
   - 子组大小（默认5）

3. 执行SPC分析：
```bash
python3 scripts/spc_analysis.py \
  --data <数据文件> \
  --chart-type <控制图类型> \
  --usl <规格上限> \
  --lsl <规格下限> \
  --subgroup-size <子组大小> \
  --output <输出目录>
```

4. 读取分析结果：
```bash
cat <输出目录>/spc_results.json
```

5. 向用户报告：
   - 过程是否稳定（有无Nelson规则违反）
   - Cpk/Ppk值及过程能力评级
   - 控制图是否出现异常模式
   - 改进建议

## 参数

- $ARGUMENTS: 数据文件路径和分析参数，格式: "数据文件 图类型 USL LSL"
- 例如: "spc_data.csv Xbar-R 10.05 9.95"

## 示例

```
/spc spc_data.csv Xbar-R 10.05 9.95
/spc diameter_data.csv I-MR 50.1 49.9
```
