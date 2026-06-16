#!/usr/bin/env python3
"""
FMEA风险评估工具 - 支持AIAG-VDA FMEA七步法中的风险分析
Usage: python3 fmea_risk_eval.py --s <严重度> --o <频度> --d <探测度> [--output <output_path>]
"""

import argparse
import json
import os

# AIAG-VDA AP（行动优先级）判定矩阵
# 格式: AP_MATRIX[S][O][D] = 'H'/'M'/'L'
# 简化版，实际应使用完整查表

def get_action_priority(s, o, d):
    """
    根据AIAG-VDA FMEA手册的AP判定矩阵确定行动优先级
    
    优先级判定逻辑（简化版）：
    - S=9-10 且 O≥4 → H
    - S=9-10 且 O=2-3 且 D≥5 → H
    - S=9-10 且 O=2-3 且 D≤4 → M
    - S=9-10 且 O=1 → M
    - S=6-8 且 O≥6 且 D≥5 → H
    - S=6-8 且 O≥5 且 D≥4 → M
    - S=6-8 且 O≤4 → L或M
    - S=4-5 且 O≥7 且 D≥5 → M
    - S=4-5 其他 → L
    - S≤3 → L
    """
    if s >= 9:
        if o >= 4:
            return 'H'
        elif o >= 2:
            if d >= 5:
                return 'H'
            else:
                return 'M'
        else:
            return 'M'
    elif s >= 6:
        if o >= 6 and d >= 5:
            return 'H'
        elif o >= 5 and d >= 4:
            return 'M'
        elif o >= 4:
            if d >= 6:
                return 'M'
            else:
                return 'M'
        elif o >= 3 and d >= 7:
            return 'M'
        else:
            return 'L'
    elif s >= 4:
        if o >= 7 and d >= 5:
            return 'M'
        elif o >= 5 and d >= 6:
            return 'M'
        else:
            return 'L'
    else:
        return 'L'


def get_rpn(s, o, d):
    """计算传统RPN值（用于参考对比）"""
    return s * o * d


def evaluate_risk(s, o, d):
    """综合风险评估"""
    ap = get_action_priority(s, o, d)
    rpn = get_rpn(s, o, d)
    
    # 风险描述
    if ap == 'H':
        risk_level = "高风险"
        action_required = "必须立即采取行动，降低风险"
    elif ap == 'M':
        risk_level = "中等风险"
        action_required = "应采取行动，可按优先级排序"
    else:
        risk_level = "低风险"
        action_required = "可考虑行动，但非强制要求"
    
    # 改进建议
    suggestions = []
    if s >= 9:
        suggestions.append("严重度为9-10，涉及安全/法规，优先考虑设计变更以降低严重度")
    if o >= 7:
        suggestions.append("频度较高，优先考虑预防措施（修改设计/过程、增加防错）")
    if d >= 7:
        suggestions.append("探测度较高（探测能力弱），优先增加/改进探测方法")
    
    if o <= 3 and d <= 3:
        suggestions.append("当前预防控制和探测控制较好，可维持现状")
    
    return {
        'S': s,
        'O': o,
        'D': d,
        'AP': ap,
        'RPN': rpn,
        'risk_level': risk_level,
        'action_required': action_required,
        'suggestions': suggestions
    }


def batch_evaluate(fmea_data):
    """批量评估FMEA风险"""
    results = []
    for item in fmea_data:
        s = item.get('S', 1)
        o = item.get('O', 1)
        d = item.get('D', 1)
        result = evaluate_risk(s, o, d)
        result['failure_mode'] = item.get('failure_mode', '')
        result['failure_effect'] = item.get('failure_effect', '')
        result['failure_cause'] = item.get('failure_cause', '')
        results.append(result)
    
    # 按AP排序
    ap_order = {'H': 0, 'M': 1, 'L': 2}
    results.sort(key=lambda x: (ap_order[x['AP']], -x['RPN']))
    
    return results


def generate_summary(results):
    """生成FMEA评估摘要"""
    h_count = sum(1 for r in results if r['AP'] == 'H')
    m_count = sum(1 for r in results if r['AP'] == 'M')
    l_count = sum(1 for r in results if r['AP'] == 'L')
    
    return {
        'total_items': len(results),
        'high_priority': h_count,
        'medium_priority': m_count,
        'low_priority': l_count,
        'high_priority_items': [
            {
                'failure_mode': r.get('failure_mode', ''),
                'failure_cause': r.get('failure_cause', ''),
                'S': r['S'], 'O': r['O'], 'D': r['D'],
                'RPN': r['RPN'],
                'suggestions': r['suggestions']
            }
            for r in results if r['AP'] == 'H'
        ],
        'recommendation': (
            f"共{len(results)}个失效模式，其中{h_count}个高优先级(H)需要立即行动，"
            f"{m_count}个中优先级(M)需要安排改进，{l_count}个低优先级(L)可维持现状。"
        )
    }


def main():
    parser = argparse.ArgumentParser(description='FMEA风险评估工具')
    parser.add_argument('--s', type=int, help='严重度(1-10)')
    parser.add_argument('--o', type=int, help='频度(1-10)')
    parser.add_argument('--d', type=int, help='探测度(1-10)')
    parser.add_argument('--batch', help='批量评估JSON数据文件路径')
    parser.add_argument('--output', default='./fmea_evaluation.json', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.batch:
        # 批量评估
        with open(args.batch, 'r', encoding='utf-8') as f:
            fmea_data = json.load(f)
        results = batch_evaluate(fmea_data)
        summary = generate_summary(results)
        
        output = {
            'summary': summary,
            'details': results
        }
        
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"FMEA批量评估完成！")
        print(f"  高优先级(H): {summary['high_priority']}")
        print(f"  中优先级(M): {summary['medium_priority']}")
        print(f"  低优先级(L): {summary['low_priority']}")
        print(f"  建议: {summary['recommendation']}")
        print(f"详细结果已保存到: {args.output}")
    
    elif args.s and args.o and args.d:
        # 单项评估
        result = evaluate_risk(args.s, args.o, args.d)
        print(f"\nFMEA风险评估结果:")
        print(f"  严重度(S): {result['S']}")
        print(f"  频度(O): {result['O']}")
        print(f"  探测度(D): {result['D']}")
        print(f"  行动优先级(AP): {result['AP']} ({result['risk_level']})")
        print(f"  RPN: {result['RPN']}")
        print(f"  行动要求: {result['action_required']}")
        if result['suggestions']:
            print(f"  改进建议:")
            for s in result['suggestions']:
                print(f"    - {s}")
    else:
        parser.print_help()
        print("\n示例:")
        print("  单项评估: python3 fmea_risk_eval.py --s 8 --o 5 --d 4")
        print("  批量评估: python3 fmea_risk_eval.py --batch fmea_data.json --output results.json")


if __name__ == '__main__':
    main()
