# 汽车行业质量改进工程师AI Skills工具集

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

汽车行业质量改进工程师AI Skills工具集，涵盖IATF 16949、五大核心工具(APQP/FMEA/SPC/MSA/PPAP)、8D/DMAIC/PDCA等质量改进方法论，支持Word/PPT/Excel文档自动生成。

## 🚀 功能概览

### 五大核心工具
| 工具 | 功能 | 支持的文档输出 |
|---|---|---|
| **APQP** | 先期产品质量策划五阶段管理 | 项目计划表(xlsx)、可行性报告(docx)、评审汇报(pptx) |
| **FMEA** | AIAG-VDA七步法失效模式分析 | FMEA表(xlsx)、分析报告(docx)、评审PPT(pptx) |
| **SPC** | 统计过程控制与过程能力分析 | 控制图(png)、Cpk报告(xlsx)、分析报告(docx) |
| **MSA** | 测量系统分析(Gage R&R等) | Gage R&R数据表(xlsx)、分析报告(docx) |
| **PPAP** | 生产件批准18要素管理 | PSW表(xlsx)、检查清单(xlsx)、提交包(docx) |

### 质量改进方法
| 方法 | 功能 | 支持的文档输出 |
|---|---|---|
| **8D** | 八步问题解决与根本原因分析 | 8D报告(docx)、5Why表(xlsx)、汇报PPT(pptx) |
| **VDA 6.3** | 过程审核P1-P7评估 | 审核报告(docx)、评分表(xlsx)、审核汇报(pptx) |
| **DMAIC** | 六西格玛改进项目 | 项目报告(docx)、分析表(xlsx)、汇报PPT(pptx) |

### 文档生成工具
| 工具 | 支持格式 | 说明 |
|---|---|---|
| **qi-docx** | Word(.docx) | 8D报告、审核报告、质量计划、作业指导书等 |
| **qi-pptx** | PowerPoint(.pptx) | 8D汇报、评审汇报、质量月报、培训材料等 |
| **qi-xlsx** | Excel(.xlsx) | 控制计划、FMEA表、SPC数据表、PPAP清单等 |

## 📦 安装

### 1. 环境要求
- Python 3.8+
- pip

### 2. 安装依赖
```bash
cd automotive-quality-engineer-skills
chmod +x scripts/setup.sh
./scripts/setup.sh
```

或手动安装：
```bash
pip install -r requirements.txt
```

### 3. 安装到AI Agent
```bash
# Claude Code
cp -r skills/ ~/.claude/skills/

# Codex CLI
cp -r skills/ ~/.codex/skills/

# OpenClaw
cp -r skills/ ~/.openclaw/workspace/skills/
```

## 🔧 使用示例

### SPC分析
```bash
python3 scripts/spc_analysis.py \
  --data spc_data.csv \
  --chart-type Xbar-R \
  --usl 10.05 \
  --lsl 9.95 \
  --subgroup-size 5 \
  --output ./spc_results/
```

### FMEA风险评估
```bash
# 单项评估
python3 scripts/fmea_risk_eval.py --s 8 --o 5 --d 4

# 批量评估
python3 scripts/fmea_risk_eval.py --batch fmea_data.json --output results.json
```

### PPAP检查清单
```bash
python3 scripts/ppap_checklist.py --level 3 --customer "大众" --output ppap_checklist.xlsx
```

### 质量文档生成
```bash
# 生成8D报告(Word)
python3 scripts/generate_quality_doc.py --type docx --template 8d_report --data 8d_data.json --output 8d_report.docx

# 生成8D汇报(PPT)
python3 scripts/generate_quality_doc.py --type pptx --template 8d_presentation --data 8d_data.json --output 8d_presentation.pptx

# 生成控制计划(Excel)
python3 scripts/generate_quality_doc.py --type xlsx --template control_plan --data cp_data.json --output control_plan.xlsx
```

## 📚 知识库

| 文档 | 说明 |
|---|---|
| [IATF 16949概述](knowledge/iatf16949_summary.md) | IATF 16949:2016标准条款与要求概述 |
| [五大核心工具概述](knowledge/core_tools_overview.md) | APQP/FMEA/SPC/MSA/PPAP详细参考 |
| [汽车质量KPI](knowledge/automotive_kpis.md) | PPM/Cpk/FPY/COPQ等KPI指标体系 |
| [CQI评估概述](knowledge/cqi_assessments.md) | CQI-8/9/11/12/15/17/23/27特殊过程评估 |

## 🏗️ 项目结构

```
automotive-quality-engineer-skills/
├── .claude-plugin/          # Claude Code插件配置
│   ├── plugin.json          # 插件定义
│   └── marketplace.json     # 市场发布配置
├── skills/                  # 技能定义
│   ├── qi-engineer/         # 主路由技能
│   ├── apqp/                # APQP先期产品质量策划
│   ├── fmea/                # FMEA失效模式分析
│   ├── spc/                 # SPC统计过程控制
│   ├── msa/                 # MSA测量系统分析
│   ├── ppap/                # PPAP生产件批准
│   ├── 8d-report/           # 8D问题解决
│   ├── vda6-3/              # VDA 6.3过程审核
│   ├── dmaic/               # DMAIC六西格玛
│   ├── qi-docx/             # Word文档生成
│   ├── qi-pptx/             # PPT演示文稿生成
│   └── qi-xlsx/             # Excel表格生成
├── scripts/                 # Python工具脚本
│   ├── spc_analysis.py      # SPC统计分析
│   ├── fmea_risk_eval.py    # FMEA风险评估
│   ├── ppap_checklist.py    # PPAP检查清单生成
│   ├── generate_quality_doc.py # 文档生成工具
│   └── setup.sh             # 环境安装脚本
├── knowledge/               # 知识库参考文档
│   ├── iatf16949_summary.md
│   ├── core_tools_overview.md
│   ├── automotive_kpis.md
│   └── cqi_assessments.md
├── requirements.txt         # Python依赖
└── README.md
```

## 🔗 潜在调用工具清单

### 核心Python库
| 库 | 用途 | 安装 |
|---|---|---|
| python-docx | Word文档生成 | `pip install python-docx` |
| python-pptx | PowerPoint生成 | `pip install python-pptx` |
| openpyxl | Excel表格生成 | `pip install openpyxl` |
| matplotlib | 数据可视化/控制图 | `pip install matplotlib` |
| numpy | 数值计算 | `pip install numpy` |
| scipy | 统计分析 | `pip install scipy` |
| pandas | 数据处理 | `pip install pandas` |

### 外部AI工具（可通过API调用）
| 工具 | 用途 | 调用方式 |
|---|---|---|
| z-ai-web-dev-sdk | AI对话/文本生成/图像生成 | JavaScript SDK |
| web-search | 查询最新标准/行业数据 | z-ai SDK函数 |
| charts | 专业图表生成 | Skill调用 |
| pdf | PDF报告生成 | Skill调用 |

### 参考学习的外部仓库
| 仓库 | Stars | 学习要点 |
|---|---|---|
| [ferdinandobons/brand-docs](https://github.com/ferdinandobons/brand-docs) | 182⭐ | Word/PPT/Excel模板化生成架构 |
| [ningzimu/codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill) | 1862⭐ | AI Agent PPT生成技能 |
| [SkyworkAI/Skywork-Skills](https://github.com/SkyworkAI/Skywork-Skills) | 173⭐ | 多技能Office套件组织方式 |
| [bowenliang123/markdown-exporter](https://github.com/bowenliang123/markdown-exporter) | 235⭐ | 多格式文档导出技能 |
| [DDC_Skills_for_AI_Agents_in_Construction](https://github.com/datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction) | 180⭐ | 工程领域技能集架构参考 |

## 📄 License

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
