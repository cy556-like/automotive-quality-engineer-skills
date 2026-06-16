---
name: qi-docx
description: >-
  质量文档Word生成技能。当用户请求涉及以下场景时触发：
  (1) 生成质量相关的Word文档（8D报告、审核报告、质量计划等）
  (2) 质量文档模板的填充与定制
  (3) 质量报告的格式化输出
  (4) 基于python-docx的Word文档编程生成
  NOT for PPT演示文稿生成（qi-pptx）、Excel表格生成（qi-xlsx）、PDF生成（pdf）。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    primaryEnv: null
---

# 质量文档Word生成 (qi-docx)

## 概述

本技能专门用于生成汽车行业质量管理相关的Word(.docx)文档。基于python-docx库，支持8D报告、VDA 6.3审核报告、质量计划、作业指导书等30+种质量文档的自动生成，确保文档符合IATF 16949和各OEM客户特定要求。

## 何时触发

- 用户要求生成Word格式的质量文档
- 需要创建8D报告、审核报告、质量计划等
- 质量文档的模板填充和格式化

## 支持的文档类型

### 核心工具文档
| 文档类型 | 模板名 | 说明 |
|---|---|---|
| APQP项目计划 | apqp_project_plan | APQP五阶段项目计划书 |
| 可行性分析报告 | feasibility_report | 产品/过程可行性分析 |
| DVP&R报告 | dvpr_report | 设计验证计划与报告 |

### 问题解决文档
| 文档类型 | 模板名 | 说明 |
|---|---|---|
| 8D报告 | 8d_report | 标准八步问题解决报告 |
| SCAR报告 | scar_report | 供应商纠正措施要求 |
| 客户投诉处理报告 | customer_complaint | 客户投诉处理全流程记录 |
| 5Why分析报告 | 5why_report | 五层原因分析报告 |

### 审核文档
| 文档类型 | 模板名 | 说明 |
|---|---|---|
| VDA 6.3审核报告 | vda63_audit_report | VDA 6.3过程审核完整报告 |
| 内部审核报告 | internal_audit_report | QMS内部审核报告 |
| 供应商审核报告 | supplier_audit | 供应商质量体系审核报告 |
| CQI评估报告 | cqi_assessment | CQI特殊过程评估报告 |

### 管理文档
| 文档类型 | 模板名 | 说明 |
|---|---|---|
| 质量计划 | quality_plan | 产品/项目质量计划 |
| 作业指导书 | work_instruction | 标准作业指导书 |
| 检验指导书 | inspection_instruction | 进货/过程/出货检验指导书 |
| 质量周报/月报 | quality_report | 定期质量绩效报告 |

## 文档生成工作流

### Step 1: 确定文档类型
根据用户需求确定文档类型和模板

### Step 2: 收集信息
引导用户提供文档所需的关键信息：
- 产品/零件信息
- 问题/审核相关数据
- 措施和结果信息
- 客户和项目背景

### Step 3: 执行生成脚本
```bash
python3 scripts/generate_docx.py \
  --template <模板名> \
  --data <数据文件.json> \
  --output <输出路径.docx> \
  [--logo <公司logo.png>] \
  [--language <zh|en>]
```

### Step 4: 验证与调整
1. 检查文档格式和内容完整性
2. 确认特殊特性标识正确
3. 验证客户特定要求(CSR)符合性
4. 如需修改，调整参数重新生成

## python-docx生成模式

### 直接生成模式（简单文档）
```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()
# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(10.5)

# 添加标题
doc.add_heading('8D报告', level=0)

# 添加表格
table = doc.add_table(rows=8, cols=4)
table.style = 'Table Grid'
# 填充内容...

doc.save('8d_report.docx')
```

### 模板填充模式（复杂文档）
```python
from docx import Document
import json

# 加载模板
doc = Document('templates/8d_report_template.docx')

# 替换占位符
with open('data.json', 'r') as f:
    data = json.load(f)

for paragraph in doc.paragraphs:
    for key, value in data.items():
        if f'{{{{{key}}}}}' in paragraph.text:
            paragraph.text = paragraph.text.replace(f'{{{{{key}}}}}', str(value))

doc.save('output/8d_report.docx')
```

## 文档格式规范

### 通用格式要求
- 标题字体：黑体/加粗宋体
- 正文字体：宋体 10.5pt（五号）
- 表格字体：宋体 9pt
- 页边距：上下2.54cm，左右3.17cm
- 表格边框：单实线
- 页眉：公司名称 + 文档编号
- 页脚：页码 + 保密等级

### IATF 16949文档控制要求
- 文档编号和版本号
- 修订历史记录
- 审批签名栏
- 分发记录

## 参考文档

读取 `references/docx_templates.md` 获取各类文档模板详细规范。
