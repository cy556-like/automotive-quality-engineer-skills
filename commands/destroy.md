删除对话及所有关联文件。

## 执行步骤

1. 如果提供了session-id：
```bash
# 先预览要删除的内容
python3 scripts/session_manager.py --action destroy --session-id "$ARGUMENTS"

# 确认后执行删除
python3 scripts/session_manager.py --action destroy --session-id "$ARGUMENTS" --confirm
```

2. 如果未提供session-id，列出所有会话：
```bash
python3 scripts/session_manager.py --action list
```

3. 删除范围：
   - 会话检查点数据(session.json)
   - 所有生成的文档(outputs/目录)
   - GitHub云端备份（如已启用）

## ⚠️ 注意

此操作不可逆！删除后所有检查点和文档将无法恢复。

## 参数

- $ARGUMENTS: 会话ID（可选），不提供则列出所有会话

## 示例

```
/destroy                         ← 列出所有会话
/destroy 8d-report_20260616      ← 预览删除内容
/destroy 8d-report_20260616 --confirm  ← 确认删除
```
