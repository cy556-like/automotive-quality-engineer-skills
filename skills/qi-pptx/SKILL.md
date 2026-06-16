---
name: qi-pptx
description: >-
  质量文档PPT生成技能。当用户请求涉及以下场景时触发：
  (1) 生成质量相关的PowerPoint演示文稿
  (2) 8D汇报演示、质量评审汇报、管理评审汇报
  (3) FMEA评审会议演示、APQP阶段评审演示
  (4) 质量培训材料PPT
  (5) 基于python-pptx的PPT编程生成
  NOT for Word文档生成（qi-docx）、Excel表格生成（qi-xlsx）、纯设计类PPT。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    primaryEnv: null
---

# 质量文档PPT生成 (qi-pptx)

## 概述

本技能专门用于生成汽车行业质量管理相关的PowerPoint(.pptx)演示文稿。基于python-pptx库，支持8D汇报、质量评审、管理评审、培训材料等演示文稿的自动生成，确保专业性和一致性。

## 何时触发

- 用户要求生成PPT格式的质量演示文稿
- 需要准备8D汇报、评审汇报等演示
- 质量培训材料的制作

## 支持的演示类型

| 演示类型 | 模板名 | 说明 | 典型页数 |
|---|---|---|---|
| 8D汇报 | 8d_presentation | 8D问题解决汇报 | 15-25页 |
| APQP阶段评审 | apqp_review | APQP各阶段评审汇报 | 20-30页 |
| FMEA评审 | fmea_review | FMEA团队评审会议 | 10-20页 |
| 质量月报 | quality_monthly | 月度质量绩效汇报 | 15-25页 |
| 管理评审 | management_review | 管理评审汇报 | 20-30页 |
| 客户投诉汇报 | customer_complaint | 客户投诉处理进度汇报 | 10-15页 |
| 质量培训 | quality_training | 质量工具/方法培训 | 30-50页 |
| PPAP提交汇报 | ppap_submission | PPAP提交评审汇报 | 15-20页 |
| VDA 6.3审核汇报 | vda63_audit | 审核结果汇报 | 15-20页 |

## PPT生成工作流

### Step 1: 确定演示类型和结构
根据汇报对象和目的确定演示结构：
- **向客户汇报**：重点突出措施和效果
- **内部评审**：重点突出分析过程和发现
- **管理层汇报**：重点突出风险和资源需求
- **培训**：重点突出理论和方法

### Step 2: 收集内容数据
引导用户提供：
- 关键数据和图表
- 分析结论
- 措施和进度信息
- 团队和项目背景

### Step 3: 执行生成脚本
```bash
python3 scripts/generate_pptx.py \
  --template <模板名> \
  --data <数据文件.json> \
  --output <输出路径.pptx> \
  [--logo <公司logo.png>] \
  [--language <zh|en>]
```

### Step 4: 验证与调整
1. 检查内容完整性
2. 确认数据图表准确
3. 调整排版和动画（如需要）

## python-pptx生成模式

### 演示文稿生成示例
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9宽屏
prs.slide_height = Inches(7.5)

# 添加标题页
slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
# 添加标题文本框
left, top, width, height = Inches(1), Inches(2), Inches(11), Inches(2)
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "8D问题解决汇报"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = RGBColor(0, 51, 102)
p.alignment = PP_ALIGN.CENTER

prs.save('8d_presentation.pptx')
```

### 常用幻灯片布局
```python
# 标题页布局
def add_title_slide(prs, title, subtitle, date):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # 添加标题
    # 添加副标题
    # 添加日期
    return slide

# 内容页布局（标题+要点）
def add_content_slide(prs, title, bullets):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # 添加标题
    # 添加要点列表
    return slide

# 图表页布局
def add_chart_slide(prs, title, chart_image_path):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # 添加标题
    # 添加图表图片
    return slide

# 表格页布局
def add_table_slide(prs, title, headers, rows):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    # 添加标题
    # 添加表格
    return slide
```

## PPT设计规范

### 配色方案（汽车行业专业风格）
| 元素 | 颜色 | RGB |
|---|---|---|
| 主色 | 深蓝 | #003366 |
| 辅色 | 钢蓝 | #4682B4 |
| 强调色 | 橙色 | #FF8C00 |
| 背景 | 白色 | #FFFFFF |
| 正文 | 深灰 | #333333 |
| 辅助文字 | 中灰 | #666666 |

### 字体规范
- 标题：微软雅黑/思源黑体 28-36pt
- 副标题：微软雅黑/思源黑体 20-24pt
- 正文：微软雅黑/思源黑体 14-18pt
- 注释：微软雅黑/思源黑体 10-12pt

### 内容密度
- 每页不超过6个要点
- 每个要点不超过2行
- 数据优先使用图表呈现
- 关键数字用大字号突出

## 参考文档

读取 `references/pptx_templates.md` 获取各类演示模板详细规范。
