生成质量相关的Word文档。

## 支持的模板

- 8d_report — 8D问题解决报告
- vda63_audit_report — VDA 6.3审核报告
- quality_plan — 产品质量计划
- work_instruction — 作业指导书
- inspection_instruction — 检验指导书
- scar_report — 供应商纠正措施报告
- customer_complaint — 客户投诉处理报告

## 执行步骤

1. 确认模板类型和输出路径

2. 收集文档所需数据

3. 生成文档：
```bash
python3 scripts/generate_quality_doc.py \
  --type docx \
  --template "$ARGUMENTS中的模板名" \
  --data <data.json> \
  --output <output.docx>
```

## 参数

- $ARGUMENTS: 模板名称，例如 "8d_report" 或 "work_instruction"

## 示例

```
/qi-docx 8d_report
/qi-docx work_instruction
```
