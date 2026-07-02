"""
sync-entry-docs.py — Package 入口文档自动同步工具
扫描 package 内三平台 skill 目录，自动生成/更新 CLAUDE.md、AGENTS.md、GEMINI.md 的 skill list 段落。

用法:
    python sync-entry-docs.py <package-path>

示例:
    python sync-entry-docs.py E:/Development/Claude_skill_pool/package/学术脚手架
    python sync-entry-docs.py E:/Development/Claude_skill_pool/package/enterprise-use
"""

import os
import sys
import re
import yaml
from pathlib import Path


def extract_frontmatter(filepath: Path) -> dict:
    """从 SKILL.md 或 command .md 提取 frontmatter"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def scan_claude_skills(package_path: Path) -> list[dict]:
    """扫描 .claude/skills/ 和 .claude/commands/"""
    skills = []
    skills_dir = package_path / ".claude" / "skills"
    commands_dir = package_path / ".claude" / "commands"

    if skills_dir.exists():
        for item in sorted(skills_dir.iterdir()):
            if item.is_dir():
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    fm = extract_frontmatter(skill_md)
                    skills.append({
                        "name": fm.get("name", item.name),
                        "description": fm.get("description", ""),
                        "type": "skill-dir",
                    })
            elif item.suffix == ".md":
                fm = extract_frontmatter(item)
                skills.append({
                    "name": fm.get("name", item.stem),
                    "description": fm.get("description", ""),
                    "type": "skill-file",
                })

    commands = []
    if commands_dir.exists():
        for item in sorted(commands_dir.iterdir()):
            if item.suffix == ".md":
                fm = extract_frontmatter(item)
                commands.append({
                    "name": item.stem,
                    "description": fm.get("description", ""),
                })

    return skills, commands


def scan_codex_skills(package_path: Path) -> list[dict]:
    """扫描 .codex/skills/"""
    skills = []
    skills_dir = package_path / ".codex" / "skills"
    if not skills_dir.exists():
        return skills
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                fm = extract_frontmatter(skill_md)
                skills.append({
                    "name": fm.get("name", item.name),
                    "description": fm.get("description", ""),
                })
    return skills


def scan_gemini_skills(package_path: Path) -> list[dict]:
    """扫描 .gemini/skills/"""
    skills = []
    skills_dir = package_path / ".gemini" / "skills"
    if not skills_dir.exists():
        return skills
    for item in sorted(skills_dir.iterdir()):
        if item.is_dir():
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                fm = extract_frontmatter(skill_md)
                skills.append({
                    "name": fm.get("name", item.name),
                    "description": fm.get("description", ""),
                })
    return skills


def generate_skill_list_section(skills: list[dict], command_prefix: str = "/") -> str:
    """生成 markdown skill list 段落"""
    lines = []
    for s in skills:
        desc = s["description"][:80] + "..." if len(s.get("description", "")) > 80 else s.get("description", "")
        lines.append(f"- `{command_prefix}{s['name']}` — {desc}")
    return "\n".join(lines)


def update_entry_doc(filepath: Path, skill_section: str, platform_label: str):
    """更新入口文档的 skill list 段落（在标记之间替换）"""
    marker_start = f"<!-- SKILL-LIST-START -->"
    marker_end = f"<!-- SKILL-LIST-END -->"

    if filepath.exists():
        content = filepath.read_text(encoding="utf-8")
    else:
        content = f"# {platform_label} Entry\n\n{marker_start}\n{marker_end}\n"

    if marker_start in content and marker_end in content:
        pattern = re.compile(
            re.escape(marker_start) + r".*?" + re.escape(marker_end),
            re.DOTALL,
        )
        new_section = f"{marker_start}\n{skill_section}\n{marker_end}"
        content = pattern.sub(new_section, content)
    else:
        content += f"\n\n{marker_start}\n{skill_section}\n{marker_end}\n"

    filepath.write_text(content, encoding="utf-8")
    print(f"  [OK] {filepath.name} updated ({platform_label})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python sync-entry-docs.py <package-path>")
        sys.exit(1)

    package_path = Path(sys.argv[1]).resolve()
    if not package_path.exists():
        print(f"Error: {package_path} does not exist")
        sys.exit(1)

    print(f"Scanning package: {package_path.name}")
    print("=" * 50)

    # Scan all platforms
    claude_skills, claude_commands = scan_claude_skills(package_path)
    codex_skills = scan_codex_skills(package_path)
    gemini_skills = scan_gemini_skills(package_path)

    print(f"  Claude: {len(claude_skills)} skills, {len(claude_commands)} commands")
    print(f"  Codex:  {len(codex_skills)} skills")
    print(f"  Gemini: {len(gemini_skills)} skills")

    # Generate sections
    claude_section = "## Available Commands\n\n"
    if claude_commands:
        claude_section += generate_skill_list_section(claude_commands, "/")
    elif claude_skills:
        claude_section += generate_skill_list_section(claude_skills, "/")

    codex_section = "## Available Skills\n\n"
    codex_section += generate_skill_list_section(codex_skills, "$")

    gemini_section = "## Available Skills\n\n"
    gemini_section += generate_skill_list_section(gemini_skills, "")

    # Update entry docs
    print("\nUpdating entry documents:")
    update_entry_doc(package_path / "CLAUDE.md", claude_section, "Claude Code")
    update_entry_doc(package_path / "AGENTS.md", codex_section, "Codex")
    update_entry_doc(package_path / "GEMINI.md", gemini_section, "Gemini CLI")

    # Cross-platform consistency report
    print("\n" + "=" * 50)
    print("Cross-platform consistency check:")
    claude_names = {s["name"] for s in claude_skills}
    codex_names = {s["name"] for s in codex_skills}
    gemini_names = {s["name"] for s in gemini_skills}

    all_names = claude_names | codex_names | gemini_names
    issues = []
    for name in sorted(all_names):
        platforms = []
        if name in claude_names:
            platforms.append("Claude")
        if name in codex_names:
            platforms.append("Codex")
        if name in gemini_names:
            platforms.append("Gemini")
        if len(platforms) < 3:
            missing = {"Claude", "Codex", "Gemini"} - set(platforms)
            issues.append(f"  [WARN] {name}: missing in {', '.join(missing)}")

    if issues:
        print("\n".join(issues))
    else:
        print("  [OK] All skills present in all 3 platforms")

    print("\nDone.")


if __name__ == "__main__":
    main()
