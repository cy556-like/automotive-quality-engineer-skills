启动DMAIC六西格玛改进项目。

## 执行步骤

1. 创建工作会话：
```bash
python3 scripts/session_manager.py --action create --skill dmaic --project "$ARGUMENTS"
```

2. 读取 `skills/dmaic/SKILL.md` 获取DMAIC五阶段完整工作流

3. 按DMAIC五个阶段执行：
   - Define: 定义问题、项目章程、SIPOC
   - Measure: 量化现状、建立基线、MSA确认
   - Analyze: 识别关键因素、假设检验、回归分析
   - Improve: 制定改进方案、DOE验证
   - Control: SPC监控、标准化、防错

4. 每阶段完成后保存检查点

5. 根据需要调用关联技能：
   - /spc — 过程能力分析
   - /msa — 测量系统分析
   - /fmea — 风险评估

## 参数

- $ARGUMENTS: 改进项目名称，例如 "降低注塑件PPM"

## 示例

```
/dmaic 降低注塑件PPM
/dmaic 提高FPY至98%
```
