启动FMEA（失效模式与影响分析）流程。

## 执行步骤

1. 创建工作会话：
```bash
python3 scripts/session_manager.py --action create --skill fmea --project "$ARGUMENTS"
```

2. 读取 `skills/fmea/SKILL.md` 获取AIAG-VDA七步法完整工作流

3. 先确认FMEA类型：
   - 如果用户说"DFMEA" → 设计FMEA
   - 如果用户说"PFMEA" → 过程FMEA
   - 如果未指定 → 询问用户

4. 按AIAG-VDA FMEA七步法执行：
   - Step1: 策划与准备 — 定义范围和团队
   - Step2: 结构分析 — 建立分析层级
   - Step3: 功能分析 — 定义功能和要求
   - Step4: 失效分析 — 识别失效链路(FE→FM→FC)
   - Step5: 风险分析 — 评估S-O-D，确定AP
   - Step6: 优化 — 制定措施降低风险
   - Step7: 结果文件化 — 形成FMEA报告

5. 风险评估使用：
```bash
python3 scripts/fmea_risk_eval.py --s <严重度> --o <频度> --d <探测度>
```

6. 生成FMEA表格：
```bash
python3 scripts/generate_quality_doc.py --type xlsx --template pfmea_sheet --data <data.json> --output <output.xlsx>
```

## 参数

- $ARGUMENTS: 分析对象描述，例如 "注塑成型过程PFMEA"

## 示例

```
/fmea 注塑成型过程PFMEA
/fmea 转向节DFMEA
```
