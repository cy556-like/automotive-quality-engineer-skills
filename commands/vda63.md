启动VDA 6.3过程审核流程。

## 执行步骤

1. 创建工作会话：
```bash
python3 scripts/session_manager.py --action create --skill vda6-3 --project "$ARGUMENTS"
```

2. 读取 `skills/vda6-3/SKILL.md` 获取VDA 6.3 P1-P7完整审核流程

3. 按过程要素逐一审核：
   - P1: 潜在供应商分析
   - P2: 项目管理
   - P3: 产品和过程开发策划
   - P4: 产品和过程开发落实
   - P5: 供应商管理
   - P6: 过程分析（P6.1-P6.6）
   - P7: 客户关怀、满意度和服务

4. 每个要素评分（0-10分）

5. 计算总体评分和评级（A/B/C）

6. 生成审核报告：
```bash
python3 scripts/generate_quality_doc.py --type docx --template vda63_audit_report --data <data.json> --output <output.docx>
```

## 参数

- $ARGUMENTS: 审核对象描述，例如 "供应商A年度审核"

## 示例

```
/vda63 供应商A年度审核
/vda63 注塑车间过程审核
```
