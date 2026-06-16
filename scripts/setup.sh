#!/bin/bash
# 环境安装脚本 - 安装质量工程师技能所需的Python依赖

echo "======================================"
echo "汽车质量改进工程师Skills - 环境安装"
echo "======================================"

# 检查Python版本
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "错误: 未找到Python，请先安装Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python版本: $PYTHON_VERSION"

# 安装Python依赖
echo ""
echo "正在安装Python依赖..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install \
    python-docx>=1.1.0 \
    python-pptx>=1.0.0 \
    openpyxl>=3.1.0 \
    lxml>=5.0.0 \
    Pillow>=10.0.0 \
    matplotlib>=3.8.0 \
    numpy>=1.24.0 \
    scipy>=1.10.0 \
    pandas>=2.0.0 \
    jinja2>=3.1.0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Python依赖安装完成"
else
    echo ""
    echo "❌ Python依赖安装失败，请检查网络连接或手动安装"
    exit 1
fi

# 验证安装
echo ""
echo "验证安装..."
$PYTHON_CMD -c "
import docx; print(f'  python-docx: {docx.__version__ if hasattr(docx, \"__version__\") else \"OK\"}')
import pptx; print(f'  python-pptx: {pptx.__version__ if hasattr(pptx, \"__version__\") else \"OK\"}')
import openpyxl; print(f'  openpyxl: {openpyxl.__version__ if hasattr(openpyxl, \"__version__\") else \"OK\"}')
import matplotlib; print(f'  matplotlib: {matplotlib.__version__}')
import numpy; print(f'  numpy: {numpy.__version__}')
import scipy; print(f'  scipy: {scipy.__version__}')
import pandas; print(f'  pandas: {pandas.__version__}')
print('  所有依赖安装验证通过!')
"

echo ""
echo "======================================"
echo "安装完成！"
echo "======================================"
