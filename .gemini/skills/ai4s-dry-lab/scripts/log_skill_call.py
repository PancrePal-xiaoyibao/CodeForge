#!/usr/bin/env python3
"""
log_skill_call.py — 记录 skill 调用历史

功能:
- 记录 skill 调用的时间、skill 名称、参数、结果
- 支持查询历史记录
- 支持导出统计报告

用法:
    python log_skill_call.py log <skill_name> [parameters...]
    python log_skill_call.py list [--last N]
    python log_skill_call.py stats
    python log_skill_call.py export [output_path]

参数:
    log: 记录一次 skill 调用
    list: 列出最近的调用记录
    stats: 显示统计信息
    export: 导出调用历史

示例:
    python log_skill_call.py log ai4s-dry-lab ooda
    python log_skill_call.py log deep-research "单细胞拟时序分析"
    python log_skill_call.py list --last 10
    python log_skill_call.py stats
    python log_skill_call.py export logs/skill_calls.csv
"""

import sys
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse


# 默认日志文件位置
DEFAULT_LOG_DIR = Path.home() / ".ai4s" / "logs"
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "skill_calls.jsonl"


def get_log_file() -> Path:
    """获取日志文件路径"""
    # 首先检查环境变量
    import os
    env_log_file = os.environ.get("AI4S_LOG_FILE")
    if env_log_file:
        return Path(env_log_file)

    # 检查项目目录
    project_log = Path("docs/skill_calls.jsonl")
    if project_log.parent.exists():
        return project_log

    # 使用默认位置
    return DEFAULT_LOG_FILE


def ensure_log_dir(log_file: Path):
    """确保日志目录存在"""
    log_file.parent.mkdir(parents=True, exist_ok=True)


def log_skill_call(skill_name: str, parameters: List[str], result: str = "success", notes: str = ""):
    """
    记录一次 skill 调用

    Args:
        skill_name: skill 名称
        parameters: 调用参数
        result: 调用结果 (success/failed/cancelled)
        notes: 备注
    """
    log_file = get_log_file()
    ensure_log_dir(log_file)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "parameters": parameters,
        "result": result,
        "notes": notes,
        "user": get_username(),
        "cwd": str(Path.cwd()),
    }

    # 追加到 JSONL 文件
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ 已记录 skill 调用: {skill_name}")
    print(f"   时间: {entry['timestamp']}")
    print(f"   参数: {' '.join(parameters)}")
    print(f"   结果: {result}")
    print(f"   日志: {log_file}")


def get_username() -> str:
    """获取当前用户名"""
    import os
    import getpass
    try:
        return os.environ.get('USER') or os.environ.get('USERNAME') or getpass.getuser()
    except Exception:
        return "unknown"


def list_skill_calls(last_n: int = 20):
    """
    列出最近的 skill 调用记录

    Args:
        last_n: 显示最近 N 条记录
    """
    log_file = get_log_file()

    if not log_file.exists():
        print("⚠️ 日志文件不存在")
        return

    entries = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        print("⚠️ 没有调用记录")
        return

    # 显示最近 N 条
    recent = entries[-last_n:]

    print(f"📊 最近 {len(recent)} 条 skill 调用记录:")
    print()

    for i, entry in enumerate(recent, 1):
        timestamp = entry.get('timestamp', 'N/A')
        skill = entry.get('skill', 'N/A')
        params = entry.get('parameters', [])
        result = entry.get('result', 'N/A')

        # 格式化时间
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            time_str = timestamp

        # 结果图标
        result_icon = "✅" if result == "success" else "❌" if result == "failed" else "⚠️"

        print(f"{i:2d}. {time_str} | {result_icon} {skill}")
        if params:
            print(f"    参数: {' '.join(params)}")


def show_stats():
    """显示统计信息"""
    log_file = get_log_file()

    if not log_file.exists():
        print("⚠️ 日志文件不存在")
        return

    entries = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        print("⚠️ 没有调用记录")
        return

    # 统计信息
    total_calls = len(entries)
    skill_counts = {}
    result_counts = {"success": 0, "failed": 0, "cancelled": 0}

    for entry in entries:
        skill = entry.get('skill', 'unknown')
        result = entry.get('result', 'unknown')

        skill_counts[skill] = skill_counts.get(skill, 0) + 1
        if result in result_counts:
            result_counts[result] += 1

    # 输出统计
    print(f"📊 Skill 调用统计:")
    print(f"   总调用次数: {total_calls}")
    print()

    print("按 skill 统计:")
    for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {skill}: {count} 次")
    print()

    print("按结果统计:")
    for result, count in result_counts.items():
        if count > 0:
            icon = "✅" if result == "success" else "❌" if result == "failed" else "⚠️"
            print(f"   {icon} {result}: {count} 次")


def export_history(output_path: Optional[str] = None):
    """
    导出调用历史

    Args:
        output_path: 输出文件路径 (默认: docs/skill_calls.csv)
    """
    log_file = get_log_file()

    if not log_file.exists():
        print("⚠️ 日志文件不存在")
        return

    if output_path is None:
        output_path = "docs/skill_calls.csv"

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 读取 JSONL
    entries = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        print("⚠️ 没有调用记录")
        return

    # 写入 CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'skill', 'parameters', 'result', 'notes', 'user', 'cwd'])
        writer.writeheader()

        for entry in entries:
            # 将 parameters 列表转换为字符串
            row = entry.copy()
            row['parameters'] = ' '.join(row.get('parameters', []))
            writer.writerow(row)

    print(f"✅ 已导出调用历史到: {output_file}")
    print(f"   记录数: {len(entries)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='记录 skill 调用历史')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # log 命令
    log_parser = subparsers.add_parser('log', help='记录一次 skill 调用')
    log_parser.add_argument('skill_name', help='skill 名称')
    log_parser.add_argument('parameters', nargs='*', help='调用参数')
    log_parser.add_argument('--result', default='success', choices=['success', 'failed', 'cancelled'],
                           help='调用结果')
    log_parser.add_argument('--notes', default='', help='备注')

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出最近的调用记录')
    list_parser.add_argument('--last', type=int, default=20, help='显示最近 N 条记录')

    # stats 命令
    subparsers.add_parser('stats', help='显示统计信息')

    # export 命令
    export_parser = subparsers.add_parser('export', help='导出调用历史')
    export_parser.add_argument('output_path', nargs='?', help='输出文件路径')

    args = parser.parse_args()

    if args.command == 'log':
        log_skill_call(args.skill_name, args.parameters, args.result, args.notes)
    elif args.command == 'list':
        list_skill_calls(args.last)
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'export':
        export_history(args.output_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
