生成质量相关的PowerPoint演示文稿。

## 支持的模板

- 8d_presentation — 8D问题解决汇报
- quality_monthly — 质量月报
- apqp_review — APQP阶段评审
- fmea_review — FMEA评审会议
- ppap_submission — PPAP提交汇报
- vda63_audit — VDA 6.3审核汇报

## 执行步骤

1. 确认演示类型和内容

2. 收集汇报数据

3. 生成演示文稿：
```bash
python3 scripts/generate_quality_doc.py \
  --type pptx \
  --template "$ARGUMENTS中的模板名" \
  --data <data.json> \
  --output <output.pptx>
```

## 参数

- $ARGUMENTS: 模板名称

## 示例

```
/qi-pptx 8d_presentation
/qi-pptx quality_monthly
```
