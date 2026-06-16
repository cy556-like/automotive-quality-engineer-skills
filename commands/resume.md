恢复之前中断的工作会话。

## 执行步骤

1. 如果提供了session-id，直接恢复：
```bash
python3 scripts/session_manager.py --action resume --session-id "$ARGUMENTS"
```

2. 如果未提供session-id，先列出所有进行中的会话：
```bash
python3 scripts/session_manager.py --action list
```

3. 读取恢复结果，向用户确认：
   - 上次做到哪一步
   - 已完成哪些步骤
   - 下一步要做什么

4. 从当前步骤继续执行

## 参数

- $ARGUMENTS: 会话ID（可选），不提供则列出所有会话

## 示例

```
/resume                          ← 列出所有会话
/resume 8d-report_20260616       ← 恢复指定会话
```
