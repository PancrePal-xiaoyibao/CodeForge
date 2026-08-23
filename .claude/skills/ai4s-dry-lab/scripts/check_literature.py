#!/usr/bin/env python3
"""
check_literature.py — 检查 WORKLOG 中的文献验证字段

功能:
- 扫描 WORKLOG.md 文件
- 检查每个 Step 条目是否包含"文献验证"字段
- 如果缺失，输出提醒

用法:
    python check_literature.py [WORKLOG_PATH]

参数:
    WORKLOG_PATH: WORKLOG.md 文件路径 (默认: docs/WORKLOG.md)

返回:
    0: 所有条目都有文献验证
    1: 存在缺失的文献验证条目
    2: 文件不存在或读取错误

示例:
    python check_literature.py
    python check_literature.py docs/WORKLOG.md
    python check_literature.py /path/to/project/docs/WORKLOG.md
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


def find_worklog(start_path: Path = None) -> Path:
    """
    查找 WORKLOG.md 文件

    Args:
        start_path: 起始搜索路径 (默认: 当前目录)

    Returns:
        WORKLOG.md 的路径，如果未找到返回 None
    """
    if start_path is None:
        start_path = Path.cwd()

    # 常见位置
    candidates = [
        start_path / "docs" / "WORKLOG.md",
        start_path / "WORKLOG.md",
        start_path.parent / "docs" / "WORKLOG.md",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def parse_worklog_sections(content: str) -> List[Tuple[str, int, int]]:
    """
    解析 WORKLOG 中的 Step 条目

    Args:
        content: WORKLOG 文件内容

    Returns:
        列表，每个元素是 (section_title, start_line, end_line)
    """
    lines = content.split('\n')
    sections = []
    current_section = None
    current_start = 0

    for i, line in enumerate(lines):
        # 匹配 ### Step XX: 或 ## 标题
        if re.match(r'^###\s+Step\s+\d+', line) or re.match(r'^##\s+', line):
            if current_section:
                sections.append((current_section, current_start, i - 1))
            current_section = line.strip()
            current_start = i

    # 最后一个 section
    if current_section:
        sections.append((current_section, current_start, len(lines) - 1))

    return sections


def check_literature_field(content: str, start: int, end: int) -> bool:
    """
    检查指定 section 是否包含文献验证字段

    Args:
        content: WORKLOG 文件内容
        start: section 起始行
        end: section 结束行

    Returns:
        True: 包含文献验证字段
        False: 不包含
    """
    lines = content.split('\n')
    section_content = '\n'.join(lines[start:end + 1])

    # 检查是否包含文献验证相关字段
    patterns = [
        r'文献验证',
        r'Literature\s+Verification',
        r'PMID',
        r'DOI',
        r'参考文献',
        r'Reference',
    ]

    for pattern in patterns:
        if re.search(pattern, section_content, re.IGNORECASE):
            return True

    return False


def main():
    """主函数"""
    # 解析参数
    worklog_path = None
    if len(sys.argv) > 1:
        worklog_path = Path(sys.argv[1])

    # 查找 WORKLOG 文件
    if worklog_path is None:
        worklog_path = find_worklog()

    if worklog_path is None:
        print("❌ 错误: 未找到 WORKLOG.md 文件")
        print("请指定文件路径: python check_literature.py <WORKLOG_PATH>")
        sys.exit(2)

    if not worklog_path.exists():
        print(f"❌ 错误: 文件不存在: {worklog_path}")
        sys.exit(2)

    # 读取文件
    try:
        content = worklog_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ 错误: 读取文件失败: {e}")
        sys.exit(2)

    # 解析 sections
    sections = parse_worklog_sections(content)

    if not sections:
        print("⚠️ 警告: 未找到 Step 条目")
        sys.exit(0)

    # 检查每个 section
    missing_literature = []
    total_sections = len(sections)

    for section_title, start, end in sections:
        if not check_literature_field(content, start, end):
            missing_literature.append(section_title)

    # 输出结果
    print(f"📊 WORKLOG 文献验证检查报告")
    print(f"文件: {worklog_path}")
    print(f"总条目数: {total_sections}")
    print(f"缺失文献验证: {len(missing_literature)}")
    print()

    if missing_literature:
        print("⚠️ 以下条目缺少文献验证:")
        for title in missing_literature:
            print(f"  - {title}")
        print()
        print("建议: 在 WORKLOG 中添加以下字段:")
        print("  - **文献验证**:")
        print("    - 检索关键词: [PubMed/OpenAlex 检索词]")
        print("    - 找到文献: [PMID/DOI] 或 '未找到直接文献'")
        print("    - 验证结论: [一致/部分一致/矛盾]")
        print("    - 解释依据: [文献内容摘要]")
        sys.exit(1)
    else:
        print("✅ 所有条目都包含文献验证字段")
        sys.exit(0)


if __name__ == "__main__":
    main()
