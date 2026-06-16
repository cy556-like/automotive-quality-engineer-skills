---
name: qi-xlsx
description: >-
  质量文档Excel生成技能。当用户请求涉及以下场景时触发：
  (1) 生成质量相关的Excel表格（控制计划、FMEA表、SPC数据表等）
  (2) 质量数据表格的格式化与计算
  (3) PPAP提交包中的Excel文件
  (4) 基于openpyxl的Excel编程生成
  (5) 质量KPI跟踪表的创建
  NOT for Word文档生成（qi-docx）、PPT生成（qi-pptx）、纯数据分析（无输出文件）。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    primaryEnv: null
---

# 质量文档Excel生成 (qi-xlsx)

## 概述

本技能专门用于生成汽车行业质量管理相关的Excel(.xlsx)表格文件。基于openpyxl库，支持控制计划、FMEA表、SPC数据表、PPAP检查清单、Cpk计算表等质量核心文件的自动生成，确保表格格式符合AIAG标准和各OEM客户要求。

## 何时触发

- 用户要求生成Excel格式的质量表格
- 需要创建控制计划、FMEA表、SPC表等
- 质量数据的表格化处理和计算

## 支持的表格类型

### 五大核心工具表格
| 表格类型 | 模板名 | 说明 |
|---|---|---|
| 控制计划 | control_plan | 试生产/生产控制计划 |
| PFMEA表 | pfmea_sheet | AIAG-VDA格式PFMEA |
| DFMEA表 | dfmea_sheet | AIAG-VDA格式DFMEA |
| SPC数据表 | spc_data | SPC原始数据记录表 |
| MSA(Gage R&R)表 | gage_rr | Gage R&R数据和分析表 |
| PPAP检查清单 | ppap_checklist | PPAP 18要素检查表 |
| PSW(零件提交保证书) | psw | PPAP提交保证书 |

### 过程分析表格
| 表格类型 | 模板名 | 说明 |
|---|---|---|
| 过程流程图 | process_flow | 过程流程图数据表 |
| 特殊特性清单 | special_chars | CC/SC特性清单 |
| Cpk计算表 | cpk_calculation | 过程能力计算表 |
| 8D跟踪表 | 8d_tracker | 8D措施跟踪表 |
| 不合格品统计 | defect_tracking | 不合格品统计表 |

### KPI跟踪表格
| 表格类型 | 模板名 | 说明 |
|---|---|---|
| PPM跟踪表 | ppm_tracker | 供应商/产线PPM跟踪 |
| FPY看板 | fpy_dashboard | 首检合格率跟踪 |
| COPQ分析表 | copq_analysis | 质量成本分析 |
| 供应商评分卡 | supplier_scorecard | 供应商绩效评估 |
| 质量月报数据表 | quality_monthly_data | 月度质量指标汇总 |

## Excel生成工作流

### Step 1: 确定表格类型
根据用户需求确定表格类型和模板

### Step 2: 收集数据
引导用户提供表格所需的数据

### Step 3: 执行生成脚本
```bash
python3 scripts/generate_xlsx.py \
  --template <模板名> \
  --data <数据文件.json> \
  --output <输出路径.xlsx> \
  [--language <zh|en>]
```

### Step 4: 验证与调整
1. 检查表格格式和公式
2. 确认数据计算正确
3. 验证客户特定格式要求

## openpyxl生成模式

### 控制计划生成示例
```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "控制计划"

# 定义样式
header_font = Font(name='黑体', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='003366', end_color='003366', fill_type='solid')
header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 表头定义
control_plan_headers = [
    '过程编号', '过程名称/操作描述', '机器/装置/工装',
    '特性编号', '产品', '过程', '特殊特性分类',
    '产品/过程规格/公差', '评价/测量技术', '样本',
    '频率', '控制方法', '反应计划'
]

# 写入表头
for col, header in enumerate(control_plan_headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment
    cell.border = thin_border

# 设置列宽
column_widths = [10, 20, 15, 10, 15, 15, 12, 18, 15, 10, 10, 15, 15]
for i, width in enumerate(column_widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = width

wb.save('control_plan.xlsx')
```

### FMEA表格生成示例
```python
# AIAG-VDA FMEA格式
fmea_headers = [
    'FMEA编号', '项目', '过程步骤', '过程要素',
    '功能/要求', '失效模式', '失效影响', 'S',
    '失效原因', 'O', '现有预防控制', '现有探测控制', 'D',
    'AP', '建议措施', '责任人/目标日期', '措施状态',
    '措施后的S', '措施后的O', '措施后的D', '措施后的AP'
]
```

### SPC数据表（含公式）
```python
# Cpk自动计算
ws['Cpk'] = '=MIN((USL-Xbar)/(3*StDev),(Xbar-LSL)/(3*StDev))'
ws['Ppk'] = '=MIN((USL-Xbar)/(3*StDev_overall),(Xbar-LSL)/(3*StDev_overall))'
```

## 表格格式规范

### AIAG标准表格格式
- 表头：深蓝底白字，黑体11pt
- 数据区：宋体10pt
- 特殊特性列：红色字体或黄色底色标注
- 表格边框：单实线
- 冻结首行：便于大数据表浏览

### 数据验证规则
```python
from openpyxl.worksheet.datavalidation import DataValidation

# 特殊特性分类下拉
dv_special = DataValidation(
    type="list",
    formula1='"CC,SC,★,◇,无"',
    allow_blank=True
)
ws.add_data_validation(dv_special)
dv_special.add('G2:G100')

# 严重度/频度/探测度评分（1-10）
dv_rating = DataValidation(
    type="whole",
    operator="between",
    formula1=1,
    formula2=10
)
ws.add_data_validation(dv_rating)
dv_rating.add('H2:H100')  # 严重度列
```

## 参考文档

读取 `references/xlsx_templates.md` 获取各类表格模板详细规范。
