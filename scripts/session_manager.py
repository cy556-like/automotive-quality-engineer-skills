#!/usr/bin/env python3
"""
工作会话状态管理器 - 支持多步骤技能流程的中断恢复
确保对话中断后，模型能从检查点继续执行

Usage:
  # 创建新会话
  python3 session_manager.py --action create --skill 8d-report --project "XX客诉"

  # 保存检查点
  python3 session_manager.py --action checkpoint --session-id <id> --step "D4" --data '{"root_cause": "..."}'

  # 恢复会话（模型重新开始时调用）
  python3 session_manager.py --action resume --session-id <id>

  # 列出所有未完成会话
  python3 session_manager.py --action list

  # 完成会话
  python3 session_manager.py --action complete --session-id <id>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 会话存储目录
SESSION_DIR = os.path.expanduser("~/.qi-sessions")

# GitHub云端备份配置（可选，留空则不备份）
GITHUB_BACKUP = {
    "enabled": False,  # 设为True启用云端备份
    "token": "",       # GitHub Personal Access Token
    "repo": "",        # 格式: owner/repo，如 "cy556-like/automotive-quality-engineer-skills"
    "branch": "main",
    "path": "sessions/"  # GitHub仓库中的存储路径
}


def get_session_path(session_id):
    """获取会话文件路径"""
    return os.path.join(SESSION_DIR, f"{session_id}.json")


def create_session(skill, project, description=""):
    """创建新的工作会话"""
    os.makedirs(SESSION_DIR, exist_ok=True)
    
    session_id = f"{skill}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    session = {
        "session_id": session_id,
        "skill": skill,
        "project": project,
        "description": description,
        "status": "in_progress",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "current_step": None,
        "completed_steps": [],
        "checkpoints": {},
        "outputs": [],
        "context_summary": "",
        "next_action_hint": ""
    }
    
    # 根据技能类型定义步骤流程
    step_flows = {
        "8d-report": ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"],
        "apqp": ["Phase1", "Phase2", "Phase3", "Phase4", "Phase5"],
        "fmea": ["Step1_策划准备", "Step2_结构分析", "Step3_功能分析", 
                 "Step4_失效分析", "Step5_风险分析", "Step6_优化", "Step7_文件化"],
        "ppap": ["确定提交等级", "准备18要素", "有效生产运行", "填写PSW", "提交与批准"],
        "vda6-3": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
        "dmaic": ["Define", "Measure", "Analyze", "Improve", "Control"],
        "spc": ["数据采集", "控制图分析", "过程能力计算", "异常模式识别", "改进建议"],
        "msa": ["策划MSA研究", "数据采集", "Gage_R&R计算", "结果评估", "改进措施"],
    }
    
    session["steps"] = step_flows.get(skill, [])
    session["current_step"] = session["steps"][0] if session["steps"] else None
    
    session_path = get_session_path(session_id)
    with open(session_path, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 工作会话已创建")
    print(f"   会话ID: {session_id}")
    print(f"   技能: {skill}")
    print(f"   项目: {project}")
    print(f"   步骤流程: {' → '.join(session['steps'])}")
    print(f"   当前步骤: {session['current_step']}")
    print(f"\n💡 提示: 将此会话ID告知模型，中断后可使用以下命令恢复:")
    print(f"   python3 session_manager.py --action resume --session-id {session_id}")
    
    return session


def save_checkpoint(session_id, step, data_str, output_file=None, next_hint=""):
    """保存检查点 - 每完成一步就保存"""
    session_path = get_session_path(session_id)
    
    if not os.path.exists(session_path):
        print(f"❌ 会话不存在: {session_id}")
        return None
    
    with open(session_path, 'r', encoding='utf-8') as f:
        session = json.load(f)
    
    # 解析数据
    try:
        data = json.loads(data_str) if data_str else {}
    except json.JSONDecodeError:
        data = {"raw": data_str}
    
    # 保存检查点
    checkpoint = {
        "step": step,
        "timestamp": datetime.now().isoformat(),
        "data": data,
        "output_file": output_file
    }
    session["checkpoints"][step] = checkpoint
    
    # 更新已完成步骤
    if step not in session["completed_steps"]:
        session["completed_steps"].append(step)
    
    # 更新当前步骤（移动到下一步）
    steps = session.get("steps", [])
    if step in steps:
        idx = steps.index(step)
        if idx + 1 < len(steps):
            session["current_step"] = steps[idx + 1]
        else:
            session["current_step"] = "已完成"
    
    # 更新输出文件
    if output_file:
        session["outputs"].append({
            "step": step,
            "file": output_file,
            "timestamp": datetime.now().isoformat()
        })
    
    # 更新下一步提示
    if next_hint:
        session["next_action_hint"] = next_hint
    
    session["updated_at"] = datetime.now().isoformat()
    
    with open(session_path, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 检查点已保存: {step}")
    print(f"   已完成: {' → '.join(session['completed_steps'])}")
    print(f"   当前步骤: {session['current_step']}")
    if session["current_step"] != "已完成":
        remaining = [s for s in steps if s not in session["completed_steps"]]
        print(f"   剩余步骤: {' → '.join(remaining)}")
    else:
        print(f"   🎉 所有步骤已完成！")
    
    return session


def resume_session(session_id):
    """恢复会话 - 模型重新开始时调用，读取所有历史检查点"""
    session_path = get_session_path(session_id)
    
    if not os.path.exists(session_path):
        print(f"❌ 会话不存在: {session_id}")
        return None
    
    with open(session_path, 'r', encoding='utf-8') as f:
        session = json.load(f)
    
    print(f"📋 工作会话恢复报告")
    print(f"{'='*50}")
    print(f"会话ID: {session['session_id']}")
    print(f"技能: {session['skill']}")
    print(f"项目: {session['project']}")
    print(f"状态: {session['status']}")
    print(f"创建时间: {session['created_at']}")
    print(f"最后更新: {session['updated_at']}")
    
    steps = session.get("steps", [])
    print(f"\n📊 步骤进度:")
    for step in steps:
        if step in session["completed_steps"]:
            cp = session["checkpoints"].get(step, {})
            ts = cp.get("timestamp", "未知时间")
            out = cp.get("output_file", "")
            print(f"  ✅ {step} - 完成 ({ts})" + (f" → 输出: {out}" if out else ""))
        elif step == session.get("current_step"):
            print(f"  ⏳ {step} - 当前步骤（待继续）")
        else:
            print(f"  ⬜ {step} - 未开始")
    
    # 生成上下文摘要 - 模型可读取此内容恢复对话
    print(f"\n📝 上下文摘要（供模型读取）:")
    print(f"{'─'*50}")
    
    summary_parts = []
    for step in session["completed_steps"]:
        cp = session["checkpoints"].get(step, {})
        data = cp.get("data", {})
        if data:
            summary_parts.append(f"[{step}]: {json.dumps(data, ensure_ascii=False)}")
    
    context_summary = "\n".join(summary_parts)
    print(context_summary if context_summary else "(无历史数据)")
    
    print(f"\n{'─'*50}")
    print(f"🔄 下一步: {session.get('current_step', '已完成')}")
    if session.get("next_action_hint"):
        print(f"💡 提示: {session['next_action_hint']}")
    
    # 输出已生成的文件列表
    if session["outputs"]:
        print(f"\n📁 已生成的文件:")
        for out in session["outputs"]:
            exists = "✅" if os.path.exists(out["file"]) else "❌(文件丢失)"
            print(f"  {exists} {out['step']}: {out['file']}")
    
    # 返回结构化数据，方便模型解析
    resume_data = {
        "session_id": session["session_id"],
        "skill": session["skill"],
        "project": session["project"],
        "current_step": session.get("current_step"),
        "completed_steps": session["completed_steps"],
        "remaining_steps": [s for s in steps if s not in session["completed_steps"] and s != session.get("current_step")],
        "checkpoints": session["checkpoints"],
        "outputs": session["outputs"],
        "next_action_hint": session.get("next_action_hint", "")
    }
    
    # 同时输出JSON格式供程序读取
    resume_json_path = os.path.join(SESSION_DIR, f"{session_id}_resume.json")
    with open(resume_json_path, 'w', encoding='utf-8') as f:
        json.dump(resume_data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 恢复数据已保存: {resume_json_path}")
    
    return session


def list_sessions(status_filter=None):
    """列出所有工作会话"""
    if not os.path.exists(SESSION_DIR):
        print("暂无工作会话")
        return
    
    sessions = []
    for f in os.listdir(SESSION_DIR):
        if f.endswith('.json') and not f.endswith('_resume.json'):
            with open(os.path.join(SESSION_DIR, f), 'r', encoding='utf-8') as fp:
                session = json.load(fp)
                if status_filter is None or session.get("status") == status_filter:
                    sessions.append(session)
    
    if not sessions:
        print("暂无匹配的工作会话")
        return
    
    sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    
    print(f"📋 工作会话列表 (共{len(sessions)}个)")
    print(f"{'='*80}")
    print(f"{'会话ID':<35} {'技能':<12} {'项目':<15} {'进度':<15} {'状态'}")
    print(f"{'─'*80}")
    
    for s in sessions:
        completed = len(s.get("completed_steps", []))
        total = len(s.get("steps", []))
        progress = f"{completed}/{total}"
        print(f"{s['session_id']:<35} {s['skill']:<12} {s['project']:<15} {progress:<15} {s['status']}")


def complete_session(session_id):
    """完成会话"""
    session_path = get_session_path(session_id)
    
    if not os.path.exists(session_path):
        print(f"❌ 会话不存在: {session_id}")
        return
    
    with open(session_path, 'r', encoding='utf-8') as f:
        session = json.load(f)
    
    session["status"] = "completed"
    session["current_step"] = "已完成"
    session["updated_at"] = datetime.now().isoformat()
    
    with open(session_path, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 会话已标记为完成: {session_id}")


def backup_to_github(session_id):
    """将会话文件备份到GitHub仓库，确保即使本地环境被清理也能恢复"""
    import base64
    import urllib.request
    import urllib.error
    
    if not GITHUB_BACKUP["enabled"] or not GITHUB_BACKUP["token"] or not GITHUB_BACKUP["repo"]:
        print("⚠️ GitHub备份未启用。在 session_manager.py 中配置 GITHUB_BACKUP 以启用。")
        return False
    
    session_path = get_session_path(session_id)
    if not os.path.exists(session_path):
        print(f"❌ 会话不存在: {session_id}")
        return False
    
    with open(session_path, 'r', encoding='utf-8') as f:
        session_data = f.read()
    
    github_path = f"{GITHUB_BACKUP['path']}{session_id}.json"
    api_url = f"https://api.github.com/repos/{GITHUB_BACKUP['repo']}/contents/{github_path}"
    
    # 检查文件是否已存在（获取sha用于更新）
    existing_sha = None
    req = urllib.request.Request(
        f"{api_url}?ref={GITHUB_BACKUP['branch']}",
        headers={"Authorization": f"token {GITHUB_BACKUP['token']}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            existing_data = json.loads(resp.read().decode())
            existing_sha = existing_data.get("sha")
    except urllib.error.HTTPError:
        pass  # 文件不存在，首次上传
    
    # 上传/更新文件
    content_bytes = session_data.encode('utf-8')
    content_b64 = base64.b64encode(content_bytes).decode('ascii')
    
    payload = {
        "message": f"checkpoint: {session_id} @ {datetime.now().isoformat()}",
        "content": content_b64,
        "branch": GITHUB_BACKUP["branch"]
    }
    if existing_sha:
        payload["sha"] = existing_sha
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Authorization": f"token {GITHUB_BACKUP['token']}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            print(f"☁️ 已备份到GitHub: {result.get('content', {}).get('html_url', 'OK')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ GitHub备份失败: {e.code} {e.reason}")
        return False


def restore_from_github(session_id):
    """从GitHub仓库恢复会话文件（本地文件丢失时使用）"""
    import base64
    import urllib.request
    import urllib.error
    
    if not GITHUB_BACKUP["enabled"] or not GITHUB_BACKUP["token"] or not GITHUB_BACKUP["repo"]:
        print("❌ GitHub备份未启用")
        return False
    
    github_path = f"{GITHUB_BACKUP['path']}{session_id}.json"
    api_url = f"https://api.github.com/repos/{GITHUB_BACKUP['repo']}/contents/{github_path}?ref={GITHUB_BACKUP['branch']}"
    
    req = urllib.request.Request(
        api_url,
        headers={"Authorization": f"token {GITHUB_BACKUP['token']}"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            content = base64.b64decode(data["content"]).decode('utf-8')
        
        # 恢复到本地
        os.makedirs(SESSION_DIR, exist_ok=True)
        session_path = get_session_path(session_id)
        with open(session_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"☁️ 已从GitHub恢复会话: {session_id}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ GitHub恢复失败: {e.code} {e.reason}")
        return False


def main():
    parser = argparse.ArgumentParser(description='工作会话状态管理器')
    parser.add_argument('--action', required=True, 
                       choices=['create', 'checkpoint', 'resume', 'list', 'complete', 
                                'backup', 'restore', 'pull'],
                       help='操作类型')
    parser.add_argument('--session-id', help='会话ID')
    parser.add_argument('--skill', help='技能名称')
    parser.add_argument('--project', help='项目名称')
    parser.add_argument('--description', default='', help='项目描述')
    parser.add_argument('--step', help='当前步骤')
    parser.add_argument('--data', default='{}', help='步骤数据(JSON字符串)')
    parser.add_argument('--output-file', help='输出文件路径')
    parser.add_argument('--next-hint', default='', help='下一步操作提示')
    parser.add_argument('--status', help='过滤状态(list时使用)')
    parser.add_argument('--github-token', help='GitHub token（覆盖默认配置）')
    parser.add_argument('--github-repo', help='GitHub仓库（覆盖默认配置）')
    
    args = parser.parse_args()
    
    # 覆盖配置
    if args.github_token:
        GITHUB_BACKUP["token"] = args.github_token
        GITHUB_BACKUP["enabled"] = True
    if args.github_repo:
        GITHUB_BACKUP["repo"] = args.github_repo
        GITHUB_BACKUP["enabled"] = True
    
    if args.action == 'create':
        if not args.skill or not args.project:
            print("❌ 创建会话需要 --skill 和 --project 参数")
            sys.exit(1)
        session = create_session(args.skill, args.project, args.description)
        if GITHUB_BACKUP["enabled"]:
            backup_to_github(session["session_id"])
    
    elif args.action == 'checkpoint':
        if not args.session_id or not args.step:
            print("❌ 保存检查点需要 --session-id 和 --step 参数")
            sys.exit(1)
        session = save_checkpoint(args.session_id, args.step, args.data, args.output_file, args.next_hint)
        if session and GITHUB_BACKUP["enabled"]:
            backup_to_github(args.session_id)
    
    elif args.action == 'resume':
        if not args.session_id:
            print("❌ 恢复会话需要 --session-id 参数")
            sys.exit(1)
        # 先检查本地文件，不存在则从GitHub拉取
        if not os.path.exists(get_session_path(args.session_id)):
            if GITHUB_BACKUP["enabled"]:
                print("📂 本地文件不存在，尝试从GitHub恢复...")
                restore_from_github(args.session_id)
            else:
                print("❌ 本地文件不存在且未启用GitHub备份")
                sys.exit(1)
        resume_session(args.session_id)
    
    elif args.action == 'list':
        list_sessions(args.status)
    
    elif args.action == 'complete':
        if not args.session_id:
            print("❌ 完成会话需要 --session-id 参数")
            sys.exit(1)
        complete_session(args.session_id)
        if GITHUB_BACKUP["enabled"]:
            backup_to_github(args.session_id)
    
    elif args.action == 'backup':
        if not args.session_id:
            print("❌ 备份需要 --session-id 参数")
            sys.exit(1)
        backup_to_github(args.session_id)
    
    elif args.action == 'restore':
        if not args.session_id:
            print("❌ 恢复需要 --session-id 参数")
            sys.exit(1)
        restore_from_github(args.session_id)
    
    elif args.action == 'pull':
        # 从GitHub拉取所有会话文件到本地
        import base64
        import urllib.request
        import urllib.error
        
        if not GITHUB_BACKUP["enabled"]:
            print("❌ 未配置GitHub备份")
            sys.exit(1)
        
        api_url = f"https://api.github.com/repos/{GITHUB_BACKUP['repo']}/contents/{GITHUB_BACKUP['path']}?ref={GITHUB_BACKUP['branch']}"
        req = urllib.request.Request(api_url, headers={"Authorization": f"token {GITHUB_BACKUP['token']}"})
        
        try:
            with urllib.request.urlopen(req) as resp:
                files = json.loads(resp.read().decode())
            
            os.makedirs(SESSION_DIR, exist_ok=True)
            count = 0
            for f in files:
                if f["name"].endswith(".json") and not f["name"].endswith("_resume.json"):
                    content_url = f["download_url"]
                    urllib.request.urlretrieve(content_url, os.path.join(SESSION_DIR, f["name"]))
                    count += 1
            
            print(f"☁️ 已从GitHub拉取{count}个会话文件到本地")
        except urllib.error.HTTPError as e:
            print(f"❌ 拉取失败: {e.code} {e.reason}")


if __name__ == '__main__':
    main()
