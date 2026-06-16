#!/usr/bin/env python3
"""
SPC统计分析工具 - 支持Xbar-R、I-MR、P/C/U控制图和过程能力分析
Usage: python3 spc_analysis.py --data <data_file.csv> --chart-type <Xbar-R|I-MR|P|C|U> --usl <值> --lsl <值> --output <output_path>
"""

import argparse
import json
import sys
import os
import numpy as np
from datetime import datetime

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC[wght].ttf')
    plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def load_data(filepath):
    """从CSV或JSON文件加载数据"""
    if filepath.endswith('.csv'):
        if HAS_PANDAS:
            return pd.read_csv(filepath)
        else:
            data = []
            with open(filepath, 'r') as f:
                lines = f.readlines()
                headers = lines[0].strip().split(',')
                for line in lines[1:]:
                    values = line.strip().split(',')
                    data.append(dict(zip(headers, values)))
            return data
    elif filepath.endswith('.json'):
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        raise ValueError(f"不支持的文件格式: {filepath}")


def calculate_xbar_r(data, subgroup_size):
    """计算Xbar-R控制图的控制限"""
    n_subgroups = len(data) // subgroup_size
    subgroups = [data[i*subgroup_size:(i+1)*subgroup_size] for i in range(n_subgroups)]
    
    xbar = [np.mean(sg) for sg in subgroups]
    ranges = [np.max(sg) - np.min(sg) for sg in subgroups]
    
    xbar_bar = np.mean(xbar)
    r_bar = np.mean(ranges)
    
    # 控制限系数（A2, D3, D4）
    control_factors = {
        2: {'A2': 1.880, 'D3': 0, 'D4': 3.267, 'd2': 1.128},
        3: {'A2': 1.023, 'D3': 0, 'D4': 2.574, 'd2': 1.693},
        4: {'A2': 0.729, 'D3': 0, 'D4': 2.282, 'd2': 2.059},
        5: {'A2': 0.577, 'D3': 0, 'D4': 2.114, 'd2': 2.326},
        6: {'A2': 0.483, 'D3': 0, 'D4': 2.004, 'd2': 2.534},
        7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924, 'd2': 2.704},
        8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864, 'd2': 2.847},
        9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816, 'd2': 2.970},
    }
    
    factors = control_factors.get(subgroup_size)
    if factors is None:
        raise ValueError(f"不支持子组大小: {subgroup_size}，支持2-9")
    
    ucl_xbar = xbar_bar + factors['A2'] * r_bar
    lcl_xbar = xbar_bar - factors['A2'] * r_bar
    ucl_r = factors['D4'] * r_bar
    lcl_r = factors['D3'] * r_bar
    
    return {
        'xbar': xbar,
        'ranges': ranges,
        'xbar_bar': xbar_bar,
        'r_bar': r_bar,
        'ucl_xbar': ucl_xbar,
        'lcl_xbar': lcl_xbar,
        'ucl_r': ucl_r,
        'lcl_r': lcl_r,
        'factors': factors,
        'subgroup_size': subgroup_size,
        'n_subgroups': n_subgroups
    }


def calculate_i_mr(data):
    """计算I-MR控制图的控制限"""
    individuals = data
    moving_ranges = [abs(data[i] - data[i-1]) for i in range(1, len(data))]
    
    x_bar = np.mean(individuals)
    mr_bar = np.mean(moving_ranges)
    
    d2 = 1.128  # n=2时的d2值
    
    ucl_i = x_bar + 2.66 * mr_bar
    lcl_i = x_bar - 2.66 * mr_bar
    ucl_mr = 3.267 * mr_bar
    lcl_mr = 0
    
    return {
        'individuals': individuals,
        'moving_ranges': moving_ranges,
        'x_bar': x_bar,
        'mr_bar': mr_bar,
        'ucl_i': ucl_i,
        'lcl_i': lcl_i,
        'ucl_mr': ucl_mr,
        'lcl_mr': lcl_mr,
        'd2': d2
    }


def calculate_capability(data, usl, lsl, sigma_within=None):
    """计算过程能力指数"""
    x_bar = np.mean(data)
    
    if sigma_within is None:
        sigma_within = np.std(data, ddof=1)
    
    sigma_overall = np.std(data, ddof=1)
    
    cp = (usl - lsl) / (6 * sigma_within) if sigma_within > 0 else 0
    cpk = min((usl - x_bar) / (3 * sigma_within), (x_bar - lsl) / (3 * sigma_within)) if sigma_within > 0 else 0
    pp = (usl - lsl) / (6 * sigma_overall) if sigma_overall > 0 else 0
    ppk = min((usl - x_bar) / (3 * sigma_overall), (x_bar - lsl) / (3 * sigma_overall)) if sigma_overall > 0 else 0
    
    return {
        'Cp': round(cp, 4),
        'Cpk': round(cpk, 4),
        'Pp': round(pp, 4),
        'Ppk': round(ppk, 4),
        'X_bar': round(x_bar, 4),
        'Sigma_within': round(sigma_within, 4),
        'Sigma_overall': round(sigma_overall, 4),
        'USL': usl,
        'LSL': lsl
    }


def check_nelson_rules(xbar, ucl, lcl, center):
    """检查Nelson规则异常模式"""
    violations = []
    
    # 规则1: 1个点超出3σ
    for i, val in enumerate(xbar):
        if val > ucl or val < lcl:
            violations.append({
                'rule': '规则1',
                'index': i,
                'value': val,
                'description': f'第{i+1}个点({val:.4f})超出控制限[{lcl:.4f}, {ucl:.4f}]'
            })
    
    # 规则2: 连续9个点在中心线同一侧
    for i in range(len(xbar) - 8):
        above = all(xbar[j] > center for j in range(i, i+9))
        below = all(xbar[j] < center for j in range(i, i+9))
        if above or below:
            side = "上方" if above else "下方"
            violations.append({
                'rule': '规则2',
                'index': i,
                'value': None,
                'description': f'第{i+1}-{i+9}个点连续在中心线{side}'
            })
    
    # 规则3: 连续6个点递增或递减
    for i in range(len(xbar) - 5):
        increasing = all(xbar[j+1] > xbar[j] for j in range(i, i+5))
        decreasing = all(xbar[j+1] < xbar[j] for j in range(i, i+5))
        if increasing or decreasing:
            trend = "递增" if increasing else "递减"
            violations.append({
                'rule': '规则3',
                'index': i,
                'value': None,
                'description': f'第{i+1}-{i+6}个点连续{trend}'
            })
    
    return violations


def plot_xbar_r(result, output_path):
    """绘制Xbar-R控制图"""
    if not HAS_MATPLOTLIB:
        print("警告: matplotlib未安装，跳过图表生成")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Xbar图
    x = range(1, result['n_subgroups'] + 1)
    ax1.plot(x, result['xbar'], 'bo-', markersize=5, label='Xbar')
    ax1.axhline(y=result['xbar_bar'], color='g', linestyle='-', label=f'CL={result["xbar_bar"]:.4f}')
    ax1.axhline(y=result['ucl_xbar'], color='r', linestyle='--', label=f'UCL={result["ucl_xbar"]:.4f}')
    ax1.axhline(y=result['lcl_xbar'], color='r', linestyle='--', label=f'LCL={result["lcl_xbar"]:.4f}')
    ax1.set_title('Xbar控制图', fontsize=14)
    ax1.set_xlabel('子组编号')
    ax1.set_ylabel('Xbar')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # R图
    ax2.plot(x, result['ranges'], 'ro-', markersize=5, label='R')
    ax2.axhline(y=result['r_bar'], color='g', linestyle='-', label=f'CL={result["r_bar"]:.4f}')
    ax2.axhline(y=result['ucl_r'], color='r', linestyle='--', label=f'UCL={result["ucl_r"]:.4f}')
    ax2.axhline(y=result['lcl_r'], color='r', linestyle='--', label=f'LCL={result["lcl_r"]:.4f}')
    ax2.set_title('R控制图', fontsize=14)
    ax2.set_xlabel('子组编号')
    ax2.set_ylabel('R')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Xbar-R控制图已保存到: {output_path}")


def plot_i_mr(result, output_path):
    """绘制I-MR控制图"""
    if not HAS_MATPLOTLIB:
        print("警告: matplotlib未安装，跳过图表生成")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # I图
    x = range(1, len(result['individuals']) + 1)
    ax1.plot(x, result['individuals'], 'bo-', markersize=4, label='单值')
    ax1.axhline(y=result['x_bar'], color='g', linestyle='-', label=f'CL={result["x_bar"]:.4f}')
    ax1.axhline(y=result['ucl_i'], color='r', linestyle='--', label=f'UCL={result["ucl_i"]:.4f}')
    ax1.axhline(y=result['lcl_i'], color='r', linestyle='--', label=f'LCL={result["lcl_i"]:.4f}')
    ax1.set_title('I控制图（单值）', fontsize=14)
    ax1.set_xlabel('观测序号')
    ax1.set_ylabel('观测值')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # MR图
    x_mr = range(1, len(result['moving_ranges']) + 1)
    ax2.plot(x_mr, result['moving_ranges'], 'ro-', markersize=4, label='移动极差')
    ax2.axhline(y=result['mr_bar'], color='g', linestyle='-', label=f'CL={result["mr_bar"]:.4f}')
    ax2.axhline(y=result['ucl_mr'], color='r', linestyle='--', label=f'UCL={result["ucl_mr"]:.4f}')
    ax2.axhline(y=result['lcl_mr'], color='r', linestyle='--', label=f'LCL={result["lcl_mr"]:.4f}')
    ax2.set_title('MR控制图（移动极差）', fontsize=14)
    ax2.set_xlabel('观测序号')
    ax2.set_ylabel('移动极差')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"I-MR控制图已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='SPC统计分析工具')
    parser.add_argument('--data', required=True, help='数据文件路径(CSV/JSON)')
    parser.add_argument('--chart-type', required=True, choices=['Xbar-R', 'I-MR', 'P', 'C', 'U'], help='控制图类型')
    parser.add_argument('--usl', type=float, help='规格上限(USL)')
    parser.add_argument('--lsl', type=float, help='规格下限(LSL)')
    parser.add_argument('--subgroup-size', type=int, default=5, help='子组大小(默认5)')
    parser.add_argument('--output', default='./spc_output', help='输出目录')
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    # 加载数据
    raw_data = load_data(args.data)
    
    # 提取数值
    if isinstance(raw_data, list) and len(raw_data) > 0:
        if isinstance(raw_data[0], dict):
            values = [float(v) for v in raw_data[0].values()]
        else:
            values = [float(v) for v in raw_data]
    else:
        values = raw_data.iloc[:, 0].astype(float).tolist()
    
    results = {'chart_type': args.chart_type, 'timestamp': datetime.now().isoformat()}
    
    # 控制图分析
    if args.chart_type == 'Xbar-R':
        spc_result = calculate_xbar_r(values, args.subgroup_size)
        results.update(spc_result)
        plot_xbar_r(spc_result, os.path.join(args.output, 'xbar_r_chart.png'))
        
        # 过程能力分析
        if args.usl and args.lsl:
            sigma_within = spc_result['r_bar'] / spc_result['factors']['d2']
            cap = calculate_capability(values, args.usl, args.lsl, sigma_within)
            results['capability'] = cap
            
            # Nelson规则检查
            violations = check_nelson_rules(
                spc_result['xbar'], 
                spc_result['ucl_xbar'], 
                spc_result['lcl_xbar'], 
                spc_result['xbar_bar']
            )
            results['nelson_violations'] = violations
    
    elif args.chart_type == 'I-MR':
        spc_result = calculate_i_mr(values)
        results.update(spc_result)
        plot_i_mr(spc_result, os.path.join(args.output, 'i_mr_chart.png'))
        
        if args.usl and args.lsl:
            sigma_within = spc_result['mr_bar'] / spc_result['d2']
            cap = calculate_capability(values, args.usl, args.lsl, sigma_within)
            results['capability'] = cap
            
            violations = check_nelson_rules(
                spc_result['individuals'],
                spc_result['ucl_i'],
                spc_result['lcl_i'],
                spc_result['x_bar']
            )
            results['nelson_violations'] = violations
    
    # 保存结果
    # 移除不可序列化的对象
    results_to_save = {}
    for k, v in results.items():
        if isinstance(v, (np.integer,)):
            results_to_save[k] = int(v)
        elif isinstance(v, (np.floating,)):
            results_to_save[k] = float(v)
        elif isinstance(v, np.ndarray):
            results_to_save[k] = v.tolist()
        elif isinstance(v, list):
            results_to_save[k] = [float(x) if isinstance(x, (np.integer, np.floating)) else x for x in v]
        elif isinstance(v, dict):
            results_to_save[k] = {kk: float(vv) if isinstance(vv, (np.integer, np.floating)) else vv for kk, vv in v.items()}
        else:
            results_to_save[k] = v
    
    with open(os.path.join(args.output, 'spc_results.json'), 'w', encoding='utf-8') as f:
        json.dump(results_to_save, f, ensure_ascii=False, indent=2)
    
    print(f"\nSPC分析完成！结果已保存到: {args.output}")
    if 'capability' in results:
        cap = results['capability']
        print(f"\n过程能力分析结果:")
        print(f"  Cp  = {cap['Cp']}")
        print(f"  Cpk = {cap['Cpk']}")
        print(f"  Pp  = {cap['Pp']}")
        print(f"  Ppk = {cap['Ppk']}")
        
        if cap['Cpk'] >= 1.67:
            print("  结论: 过程能力优秀")
        elif cap['Cpk'] >= 1.33:
            print("  结论: 过程能力合格")
        elif cap['Cpk'] >= 1.0:
            print("  结论: 过程能力需改进")
        else:
            print("  结论: 过程能力不足，必须改进")


if __name__ == '__main__':
    main()
