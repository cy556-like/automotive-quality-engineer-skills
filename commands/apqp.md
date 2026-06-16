启动APQP（先期产品质量策划）流程。

## 执行步骤

1. 创建工作会话：
```bash
python3 scripts/session_manager.py --action create --skill apqp --project "$ARGUMENTS"
```

2. 读取 `skills/apqp/SKILL.md` 获取APQP五阶段完整工作流

3. 按APQP五个阶段逐步引导：
   - Phase1: 计划和确定项目 — 客户需求、目标设定
   - Phase2: 产品设计和开发 — DFMEA、DVP&R
   - Phase3: 过程设计和开发 — PFMEA、控制计划、MSA/SPC计划
   - Phase4: 产品和过程确认 — PPAP、有效生产运行
   - Phase5: 反馈、评定和纠正措施 — 持续改进

4. 每阶段完成后保存检查点

5. 根据需要调用关联技能：
   - /fmea — 生成DFMEA/PFMEA
   - /msa — 测量系统分析
   - /ppap — PPAP提交准备

## 参数

- $ARGUMENTS: 项目名称，例如 "新项目XYZ-001"

## 示例

```
/apqp 新项目XYZ-001
/apqp 电动车电池壳体开发
```
