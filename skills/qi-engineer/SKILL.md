---
name: qi-engineer
description: >-
  汽车行业质量改进工程师主技能路由。当用户请求涉及以下场景时触发：
  (1) 汽车行业质量管理相关任务（IATF 16949、VDA、CQI等标准）
  (2) 五大核心工具（APQP、FMEA、SPC、MSA、PPAP）的创建、分析或评审
  (3) 质量改进方法论（8D、DMAIC、PDCA、六西格玛、精益）
  (4) 质量文档生成（控制计划、作业指导书、审核报告、8D报告等）
  (5) 质量数据分析（PPM、Cpk、FPY、COPQ等KPI分析）
  (6) 供应商质量管理（审核、评估、改进）
  (7) 过程审核与产品审核（VDA 6.3、VDA 6.5）
  (8) 客户投诉处理与纠正措施
  NOT for 通用软件开发、非汽车行业的一般质量管理、纯设计任务。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    primaryEnv: null
    emoji: "🔧"
    os:
      - darwin
      - linux
      - win32
---

# 汽车行业质量改进工程师技能

## 概述

本技能是汽车行业质量改进工程师的综合AI助手，涵盖从产品策划到过程控制、从问题解决到持续改进的全链路质量管理能力。基于IATF 16949:2016质量管理体系标准，集成了五大核心工具、常用改进方法论以及文档自动生成功能。

## 何时触发

当用户提到以下关键词或场景时，激活本技能：
- **核心工具**：APQP、FMEA（DFMEA/PFMEA）、SPC、MSA、PPAP
- **改进方法**：8D、DMAIC、PDCA、六西格玛、精益、A3
- **标准规范**：IATF 16949、VDA 6.3、VDA 6.5、CQI评估、CSR
- **质量文档**：控制计划、作业指导书、流程图、审核报告
- **数据分析**：Cpk/Ppk、PPM、FPY/FTQ、COPQ、OEE
- **供应商质量**：供应商审核、SCAR、二方审核
- **问题解决**：客户投诉、纠正措施、预防措施、5Why、鱼骨图

## 子技能路由表

根据用户请求，路由到对应的子技能：

| 用户请求模式 | 路由目标 | 说明 |
|---|---|---|
| APQP、产品质量策划、项目策划 | `apqp` | APQP五个阶段的策划与文件生成 |
| FMEA、DFMEA、PFMEA、失效模式分析 | `fmea` | AIAG-VDA FMEA七步法分析与文档 |
| SPC、统计过程控制、控制图、Cpk | `spc` | 统计过程控制分析与图表生成 |
| MSA、测量系统分析、Gage R&R | `msa` | 测量系统分析与评估 |
| PPAP、生产件批准、提交包 | `ppap` | PPAP 18要素清单与提交包生成 |
| 8D、问题解决、纠正措施、客户投诉 | `8d-report` | 8D问题解决报告 |
| VDA 6.3、过程审核、P1-P7 | `vda6-3` | VDA 6.3过程审核评估与报告 |
| DMAIC、六西格玛、改善项目 | `dmaic` | 六西格玛DMAIC改进项目 |
| 生成Word文档、质量报告docx | `qi-docx` | 质量相关Word文档生成 |
| 生成PPT、汇报演示pptx | `qi-pptx` | 质量相关PPT演示文稿生成 |
| 生成Excel、数据表xlsx | `qi-xlsx` | 质量相关Excel表格生成 |

## 工作流

### Phase 1: 需求识别
1. 分析用户请求，确定涉及的质量管理领域
2. 识别适用的标准、工具和方法论
3. 确定输出格式需求（Word/PPT/Excel）

### Phase 2: 知识加载
1. 读取 `knowledge/` 目录下对应的参考文档
2. 加载相关标准要求和最佳实践
3. 确认适用的客户特定要求(CSR)

### Phase 3: 技能路由
1. 根据需求匹配到具体子技能
2. 将上下文传递给子技能
3. 必要时组合多个子技能协作

### Phase 4: 执行与输出
1. 子技能执行具体任务
2. 生成文档或分析结果
3. 输出到 `/home/z/my-project/download/`

## 与其他技能的协作

- `qi-docx` / `qi-pptx` / `qi-xlsx` — 所有子技能都可能调用文档生成技能
- `charts` — SPC控制图、Cpk分析图、趋势图等数据可视化
- `web-search` — 查询最新标准更新或行业数据
- `pdf` — 生成PDF格式的质量报告

## 中断恢复机制

多步骤技能（8D、APQP、FMEA、VDA 6.3、DMAIC等）在执行过程中，**每完成一个步骤必须保存检查点**，确保对话中断后可恢复。

### 核心原则
1. **每步必存**：完成一个步骤后立即调用 `session_manager.py` 保存检查点
2. **文件持久**：所有中间输出保存到磁盘文件，不依赖对话上下文
3. **恢复优先**：对话恢复后，第一步先调用 `resume` 读取历史状态

### 操作流程
```bash
# 1. 创建工作会话
python3 scripts/session_manager.py --action create --skill <技能名> --project "项目名"

# 2. 每步保存检查点（关键！）
python3 scripts/session_manager.py --action checkpoint \
  --session-id <id> --step "当前步骤" \
  --data '{"key": "value"}' \
  --output-file "输出文件路径" \
  --next-hint "下一步做什么"

# 3. 对话中断后恢复
python3 scripts/session_manager.py --action resume --session-id <id>

# 4. 查看所有进行中的会话
python3 scripts/session_manager.py --action list

# 5. 完成会话
python3 scripts/session_manager.py --action complete --session-id <id>
```

### 模型恢复行为
当对话恢复时，模型应该：
1. 调用 `resume` 读取会话状态和所有历史检查点
2. 向用户确认当前进度："已恢复到D4步骤，之前完成了..."
3. 从当前步骤继续执行
4. 继续每步保存检查点

## 反模式

- ❌ 不应脱离IATF 16949框架谈论质量管理
- ❌ 不应忽略客户特定要求(CSR)直接套用通用规则
- ❌ 不应将FMEA当作填表任务，应确保团队充分分析
- ❌ 不应在缺乏数据的情况下进行SPC分析
- ❌ 不应跳过根本原因分析直接制定纠正措施
- ❌ 不应在多步骤流程中跳过检查点保存（风险：中断后无法恢复）
