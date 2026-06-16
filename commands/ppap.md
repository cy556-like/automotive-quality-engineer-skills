启动PPAP（生产件批准程序）流程。

## 执行步骤

1. 创建工作会话：
```bash
python3 scripts/session_manager.py --action create --skill ppap --project "$ARGUMENTS"
```

2. 读取 `skills/ppap/SKILL.md` 获取PPAP 18要素完整工作流

3. 确认提交等级（默认Level 3）

4. 生成PPAP检查清单：
```bash
python3 scripts/ppap_checklist.py --level <1-5> --customer <客户名> --output ppap_checklist.xlsx
```

5. 逐项引导用户准备18要素

6. 生成PSW和提交包：
```bash
python3 scripts/generate_quality_doc.py --type xlsx --template psw --data <data.json> --output psw.xlsx
```

## 参数

- $ARGUMENTS: 零件信息，格式: "零件编号 客户名 提交等级"
- 例如: "ABC-123 大众 3"

## 示例

```
/ppap ABC-123 大众
/ppap 转向节 丰田 3
```
