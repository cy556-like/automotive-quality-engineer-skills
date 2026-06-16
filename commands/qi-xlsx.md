生成质量相关的Excel表格。

## 支持的模板

- control_plan — 控制计划
- pfmea_sheet — PFMEA表格
- dfmea_sheet — DFMEA表格
- spc_data — SPC数据记录表
- gage_rr — Gage R&R数据表
- ppap_checklist — PPAP检查清单
- psw — 零件提交保证书
- cpk_calculation — Cpk计算表

## 执行步骤

1. 确认表格类型

2. 收集表格数据

3. 生成表格：
```bash
python3 scripts/generate_quality_doc.py \
  --type xlsx \
  --template "$ARGUMENTS中的模板名" \
  --data <data.json> \
  --output <output.xlsx>
```

## 参数

- $ARGUMENTS: 模板名称

## 示例

```
/qi-xlsx control_plan
/qi-xlsx pfmea_sheet
```
