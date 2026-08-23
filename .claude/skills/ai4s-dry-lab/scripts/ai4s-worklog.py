#!/usr/bin/env python3
"""
ai4s-worklog.py — AI4S Dry Lab Worklog 工具
用法:
  python ai4s-worklog.py append --phase 02 --step 02a --method "..." --result "..."
  python ai4s-worklog.py status
  python ai4s-worklog.py report --phase 02
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WORKLOG_PATH = PROJECT_ROOT / "docs" / "WORKLOG.md"


def get_template() -> str:
    return f"""# 实验记录 (Worklog)

**项目**: {PROJECT_ROOT.name}
**创建日期**: {datetime.now().strftime('%Y-%m-%d')}
**格式说明**: 每个 Phase 的每个 Step 记录方法、结果、可追溯信息

---

"""


def ensure_worklog():
    if not WORKLOG_PATH.exists():
        WORKLOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        WORKLOG_PATH.write_text(get_template())


def append_entry(args):
    ensure_worklog()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    entry = f"""## Phase {args.phase}: {args.phase_name or '...'} — {timestamp}

### Step {args.step}: {args.step_name or '...'}
- **方法**: {args.method or 'N/A'}
- **输入**: {args.input or 'N/A'}
- **输出**: {args.output or 'N/A'}
- **关键结果**: {args.result or 'N/A'}
- **代码位置**: `{args.code or 'N/A'}`
- **SPEC 关联**: {args.spec or 'N/A'}
- **OODA 状态**: {args.ooda or 'N/A'}
- **文献验证**: {args.lit or '待验证'}
- **下一步**: {args.next_step or 'N/A'}

---

"""
    with open(WORKLOG_PATH, 'a') as f:
        f.write(entry)

    print(f"✓ Worklog 已更新: Phase {args.phase} Step {args.step}")


def show_status(args):
    if not WORKLOG_PATH.exists():
        print("Worklog 不存在。请先运行 ai4s-init.sh")
        return

    content = WORKLOG_PATH.read_text()
    phases = [l for l in content.split('\n') if l.startswith('## Phase')]
    steps = [l for l in content.split('\n') if l.startswith('### Step')]

    print(f"Worklog 状态:")
    print(f"  Phase 记录: {len(phases)}")
    print(f"  Step 记录:  {len(steps)}")
    print(f"  文件路径:   {WORKLOG_PATH}")
    print(f"  文件大小:   {WORKLOG_PATH.stat().st_size / 1024:.1f} KB")

    if phases:
        print("\n已记录的 Phase:")
        for p in phases:
            print(f"  {p}")


def gen_report(args):
    if not WORKLOG_PATH.exists():
        print("Worklog 不存在")
        return

    content = WORKLOG_PATH.read_text()
    phase_num = args.phase

    # Find all entries for this phase
    lines = content.split('\n')
    in_phase = False
    phase_lines = []

    for line in lines:
        if line.startswith(f'## Phase {phase_num}'):
            in_phase = True
        elif line.startswith('## Phase ') and in_phase:
            break
        if in_phase:
            phase_lines.append(line)

    if not phase_lines:
        print(f"Phase {phase_num} 无记录")
        return

    steps = [l for l in phase_lines if l.startswith('### Step')]
    print(f"Phase {phase_num} 报告:")
    print(f"  Step 数量: {len(steps)}")
    print()
    print('\n'.join(phase_lines))


def main():
    parser = argparse.ArgumentParser(description='AI4S Worklog Tool')
    sub = parser.add_subparsers(dest='command')

    # append
    p_append = sub.add_parser('append', help='追加 Worklog 条目')
    p_append.add_argument('--phase', required=True, help='Phase 编号 (如 02)')
    p_append.add_argument('--step', required=True, help='Step 编号 (如 02a)')
    p_append.add_argument('--phase-name', default='', help='Phase 名称')
    p_append.add_argument('--step-name', default='', help='Step 名称')
    p_append.add_argument('--method', default='', help='方法描述')
    p_append.add_argument('--input', default='', help='输入文件')
    p_append.add_argument('--output', default='', help='输出文件')
    p_append.add_argument('--result', default='', help='关键结果')
    p_append.add_argument('--code', default='', help='代码位置')
    p_append.add_argument('--spec', default='', help='SPEC 关联')
    p_append.add_argument('--ooda', default='Observe', help='OODA 状态')
    p_append.add_argument('--lit', default='', help='文献验证')
    p_append.add_argument('--next-step', default='', help='下一步')

    # status
    sub.add_parser('status', help='显示 Worklog 状态')

    # report
    p_report = sub.add_parser('report', help='生成 Phase 报告')
    p_report.add_argument('--phase', required=True, help='Phase 编号')

    args = parser.parse_args()

    if args.command == 'append':
        append_entry(args)
    elif args.command == 'status':
        show_status(args)
    elif args.command == 'report':
        gen_report(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
