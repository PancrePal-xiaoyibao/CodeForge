#!/usr/bin/env python3
"""
validate-skills.py — CodeForge skill 元数据 / 格式合规校验器

背景
----
社区反馈：装上 CodeForge 后 Codex 拒绝加载 `ai-spec/SKILL.md`（缺必需 YAML frontmatter）。
根因是仓库长期没有元数据门禁，缺 frontmatter 的文件可以静默进入 main。
本脚本即该门禁：本地可跑，CI 也跑，任何缺元数据的 skill 会被拦下。

校验规则（对齐 Codex 官方 skill-creator/quick_validate.py 的判定门槛）
--------------------------------------------------------------------
ERROR（阻塞，退出码 1）
  1. SKILL.md 首行不是 `---`（缺 frontmatter）
  2. frontmatter 缺 `name` 或 `description`
  3. `name` 不合规：非 [a-z0-9-]、超 64 字符、以 `-` 起止、含连续 `--`
  4. `description` 为空、超 1024 字符、含 `<` `>`、或含未完成的 `[TODO:`
  5. frontmatter 含白名单外的键（Codex 允许：name/description/license/allowed-tools/metadata）
  6. 文件带 UTF-8 BOM（会挡住 `^---`，使严格解析器读不到 frontmatter）
  7. 三个镜像 skill 集合不一致（某平台缺某个 skill）
  8. `.claude/commands/*.md` 缺 `description`
  9. 文件行尾含 CR / CRLF（跨平台污染源，且首行会变成 `---` + CR 使朴素解析器失配）
     —— 例外：`*.ps1` / `*.bat` / `*.cmd` 按 .gitattributes 保留 CRLF，仅 lone CR 报错

WARN（不阻塞，仅提示）
  10. 同一 skill 三镜像正文（去 frontmatter 后）不一致 —— 仓库历史技术债，逐批收敛

用法
----
    python3 scripts/validate-skills.py            # 全量校验，失败退出码 1
    python3 scripts/validate-skills.py --quiet    # 仅输出问题
    python3 scripts/validate-skills.py --json     # 机器可读

零依赖：优先用 PyYAML；未安装时降级到内置极简 frontmatter 解析器。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 三镜像：平台 -> skills 目录
MIRRORS = {
    "codex": REPO_ROOT / ".codex" / "skills",
    "gemini": REPO_ROOT / ".gemini" / "skills",
    "claude": REPO_ROOT / ".claude" / "skills",
}
CLAUDE_COMMANDS = REPO_ROOT / ".claude" / "commands"

# Codex skill-creator/quick_validate.py 的允许键白名单
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
# Claude Code skill 侧额外允许的界面字段（仅对 .claude/ 生效）
CLAUDE_EXTRA_KEYS = {"model", "color", "tools", "argument-hint"}
NAME_RE = re.compile(r"^[a-z0-9-]+$")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
BOM = b"\xef\xbb\xbf"

# 参与行尾 / BOM 检查的文件后缀
TEXT_SUFFIXES = {".md", ".markdown", ".yaml", ".yml", ".py", ".sh", ".ps1", ".json", ".toml", ".txt"}

# 不参与校验的目录（构建产物 / 本地运行时）
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".debug", ".venv", "venv", "_archived"}

# 按 .gitattributes，这些后缀保留 CRLF（Windows 原生脚本）；其余文本文件一律 LF。
# 校验器必须尊重这条约定，否则会误报合法的 PowerShell 脚本。
CRLF_EXPECTED_SUFFIXES = {".ps1", ".bat", ".cmd"}

# 「关联 Skill」表校验：跳过表头与分隔行，数据行校验第 2 列（Skill 名）存在。
# 第 1 列就是关系词（被调用 / 可调用 / 配合…），所以不能用关系词做 skip 条件，
# 否则会把所有数据行都跳掉（写这一版时真踩过：注入错名 deep-reserch 却报绿）。
TABLE_HEADER_FIRST_CELL = "关系"
MARKDOWN_ROW_NOISE = {"-", "—", "n/a", "na", "none", "None"}


# --------------------------------------------------------------------------
# YAML 解析：优先 PyYAML，缺失时降级到极简解析器（覆盖 frontmatter 实际用法）
# --------------------------------------------------------------------------
try:
    import yaml as _yaml

    def _parse_yaml(text: str):
        return _yaml.safe_load(text)
except ImportError:  # pragma: no cover - 降级路径
    def _parse_yaml(text: str):
        """极简 frontmatter 解析：支持 `key: value` 与一层缩进嵌套（如 metadata.version）。"""
        result: dict = {}
        current_map = None
        for raw_line in text.split("\n"):
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            line = raw_line.strip()
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            if indent == 0:
                if value == "":
                    current_map = {}
                    result[key] = current_map
                else:
                    result[key] = _unquote(value)
                    current_map = None
            elif current_map is not None:
                current_map[key] = _unquote(value)
        return result

    def _unquote(v: str):
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            return v[1:-1]
        return v


# --------------------------------------------------------------------------
# 采样与解析
# --------------------------------------------------------------------------
class Issue:
    __slots__ = ("level", "path", "rule", "detail")

    def __init__(self, level: str, path: Path | str, rule: str, detail: str = ""):
        self.level = level
        self.path = str(path)
        self.rule = rule
        self.detail = detail

    def as_dict(self) -> dict:
        return {"level": self.level, "path": self.path, "rule": self.rule, "detail": self.detail}


def rel(p: Path | str) -> str:
    try:
        return str(Path(p).resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def read_text(path: Path, issues: list[Issue]) -> str:
    """读文件并检查 BOM；返回去掉 BOM 的文本（保留原始行尾，供行尾检查另行判定）。"""
    raw = path.read_bytes()
    if raw.startswith(BOM):
        issues.append(Issue("ERROR", rel(path), "bom", "文件带 UTF-8 BOM，会挡住 frontmatter 的 ^--- 匹配"))
    return raw.decode("utf-8-sig")


def check_line_endings(path: Path, text: str, issues: list[Issue]) -> None:
    """行尾检查。

    - `*.ps1` / `*.bat` / `*.cmd`：按 .gitattributes 保留 CRLF，CRLF 属预期，不报错；
      但 lone CR 仍是异常（lone CR 曾把 LaTeX 转义吃掉，见 debug-ui 案例）。
    - 其余文本文件：一律要求 LF；出现 CR 即报错（CRLF 会让 frontmatter 首行变成 `---\r`，
      使严格解析器读不到元数据）。
    """
    crlf = text.count("\r\n")
    lone = text.count("\r") - crlf
    expect_crlf = path.suffix.lower() in CRLF_EXPECTED_SUFFIXES

    if expect_crlf:
        if lone:
            issues.append(Issue("ERROR", rel(path), "line-ending",
                                f"含 lone-CR ×{lone}（该后缀允许 CRLF，但不允许孤立 CR）"))
        return

    if crlf or lone:
        parts = []
        if crlf:
            parts.append(f"CRLF×{crlf}")
        if lone:
            parts.append(f"lone-CR×{lone}")
        issues.append(Issue("ERROR", rel(path), "line-ending", "行尾非 LF（" + "、".join(parts) + "）"))


def split_frontmatter(text: str):
    """返回 (frontmatter_text | None, body)。容忍 CRLF（用归一化副本做匹配）。"""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n") and normalized.rstrip("\n") != "---":
        return None, normalized
    m = re.match(r"^---\n(.*?)\n---[ \t]*(?:\n|$)", normalized, re.DOTALL)
    if not m:
        return None, normalized
    return m.group(1), normalized[m.end():]


def validate_skill_md(path: Path, issues: list[Issue], platform: str = "codex") -> dict | None:
    """校验单个 SKILL.md，返回 frontmatter dict（解析失败返回 None）。

    platform='claude' 时 name 可选：Claude Code 的约定是「文件名 / 目录名即 skill 名」，
    官方 skill 文件只写 description。此时若缺 name，则按文件名做合规断言。
    其余平台（codex / gemini）严格执行 Codex 官方校验器门槛：name + description 必需。
    """
    text = read_text(path, issues)
    check_line_endings(path, text, issues)

    fm_text, _body = split_frontmatter(text)
    if fm_text is None:
        issues.append(Issue("ERROR", rel(path), "missing-frontmatter",
                            "缺 YAML frontmatter（首行必须是 ---）"))
        return None

    try:
        fm = _parse_yaml(fm_text)
    except Exception as exc:  # noqa: BLE001
        issues.append(Issue("ERROR", rel(path), "yaml-error", f"frontmatter YAML 解析失败：{exc}"))
        return None

    if not isinstance(fm, dict):
        issues.append(Issue("ERROR", rel(path), "yaml-not-dict", "frontmatter 不是 YAML 映射"))
        return None

    name_optional = platform == "claude"

    # 必需字段
    required_fields = ("description",) if name_optional else ("name", "description")
    for required in required_fields:
        if required not in fm:
            issues.append(Issue("ERROR", rel(path), f"missing-{required}",
                                f"frontmatter 缺必需字段 {required}"))

    # 白名单（额外允许 Claude 侧常见的 model/color 等界面字段）
    allowed = ALLOWED_KEYS | (CLAUDE_EXTRA_KEYS if name_optional else set())
    unexpected = sorted(set(fm) - allowed)
    if unexpected:
        issues.append(Issue("ERROR", rel(path), "unexpected-key",
                            "含白名单外的 frontmatter 键：" + ", ".join(unexpected)
                            + "（允许：" + ", ".join(sorted(allowed)) + "）"))

    # name 规范：缺 name 时（Claude 允许）按文件名派生做断言
    raw_name = fm.get("name")
    if raw_name is None and name_optional:
        raw_name = path.parent.name if path.name == "SKILL.md" else path.stem
    name = raw_name
    if isinstance(name, str):
        name = name.strip()
        if not NAME_RE.match(name):
            issues.append(Issue("ERROR", rel(path), "name-charset",
                                f"name '{name}' 必须为小写字母/数字/连字符"))
        elif name.startswith("-") or name.endswith("-") or "--" in name:
            issues.append(Issue("ERROR", rel(path), "name-shape",
                                f"name '{name}' 不能以连字符起止或含连续连字符"))
        if len(name) > MAX_NAME_LEN:
            issues.append(Issue("ERROR", rel(path), "name-too-long",
                                f"name 长 {len(name)}，上限 {MAX_NAME_LEN}"))
    elif "name" in fm:
        issues.append(Issue("ERROR", rel(path), "name-type", "name 必须是字符串"))

    # description 规范
    desc = fm.get("description")
    if isinstance(desc, str):
        desc = desc.strip()
        if not desc:
            issues.append(Issue("ERROR", rel(path), "description-empty", "description 为空"))
        if desc.startswith("[TODO:"):
            issues.append(Issue("ERROR", rel(path), "description-todo",
                                "description 含未完成的 TODO 占位"))
        if "<" in desc or ">" in desc:
            issues.append(Issue("ERROR", rel(path), "description-angle",
                                "description 含尖括号 < >（Codex 校验器直接判失败）"))
        if ": " in desc:
            issues.append(Issue("WARN", rel(path), "description-colon-space",
                                "description 含裸冒号+空格，未加引号时 YAML 会误解为映射"))
        if len(desc) > MAX_DESC_LEN:
            issues.append(Issue("ERROR", rel(path), "description-too-long",
                                f"description 长 {len(desc)}，上限 {MAX_DESC_LEN}"))
    elif "description" in fm:
        issues.append(Issue("ERROR", rel(path), "description-type", "description 必须是字符串"))

    return fm


# --------------------------------------------------------------------------
# 三镜像收集
# --------------------------------------------------------------------------
def collect_mirror_skills(issues: list[Issue]) -> dict[str, dict[str, Path]]:
    """返回 {platform: {skill_name: SKILL.md path}}。"""
    collected: dict[str, dict[str, Path]] = {}
    for platform, skills_dir in MIRRORS.items():
        found: dict[str, Path] = {}
        if not skills_dir.is_dir():
            issues.append(Issue("ERROR", rel(skills_dir), "mirror-missing",
                                f"{platform} 镜像目录不存在"))
            collected[platform] = found
            continue
        for item in sorted(skills_dir.iterdir()):
            if item.is_dir():
                skill_md = item / "SKILL.md"
                if skill_md.is_file():
                    found[item.name] = skill_md
            elif item.suffix == ".md" and item.name != "SKILL.md":
                # Claude 扁平镜像：.claude/skills/<name>.md
                found[item.stem] = item
        collected[platform] = found
    return collected


def body_of(text: str) -> str:
    """去 frontmatter，行尾归一化，逐行 rstrip 后比较（只比较语义正文）。"""
    _fm, body = split_frontmatter(text)
    return "\n".join(line.rstrip() for line in body.split("\n")).strip()


def check_mirrors(issues: list[Issue], quiet: bool) -> tuple[int, int]:
    mirrors = collect_mirror_skills(issues)
    codex, gemini, claude = mirrors["codex"], mirrors["gemini"], mirrors["claude"]

    all_names = sorted(set(codex) | set(gemini) | set(claude))
    sets = {"codex": set(codex), "gemini": set(gemini), "claude": set(claude)}
    for name in all_names:
        missing = [p for p, s in sets.items() if name not in s]
        if missing:
            have = next(p for p in ("codex", "gemini", "claude") if name in sets[p])
            issues.append(Issue("ERROR", f"mirror:{name}", "mirror-missing-skill",
                                f"skill 存在于 {have}，但 {'/'.join(missing)} 镜像缺失"))

    # 正文一致性规则（2026-10-15 确立，见 CONTRIBUTING.md）：
    #   - claude 与 gemini 都存“完整版”，两者必须逐字一致 → 不一致报 ERROR
    #   - codex 允许独立精简版（Overview / Workflow / Output Contract 结构，受 token 预算约束）
    #     → 与 claude/gemini 不一致不算违规，仅统计
    cg_drift = []
    codex_independent = 0
    for name in all_names:
        cb = body_of(read_text(claude[name], [])) if name in claude else None
        gb = body_of(read_text(gemini[name], [])) if name in gemini else None
        xb = body_of(read_text(codex[name], [])) if name in codex else None
        if cb is not None and gb is not None and cb != gb:
            cg_drift.append(name)
            issues.append(Issue(
                "ERROR", f"mirror:{name}", "claude-gemini-drift",
                f"claude 与 gemini 正文必须一致（两者都是完整版）："
                f"claude={len(cb.splitlines())}行、gemini={len(gb.splitlines())}行",
            ))
        elif xb is not None and xb != cb and xb != gb:
            codex_independent += 1

    if not quiet:
        print(f"  [mirror] 三镜像 skill 集合：codex={len(codex)} gemini={len(gemini)} claude={len(claude)}"
              f"；claude↔gemini 不一致 {len(cg_drift)} 个；codex 独立精简版 {codex_independent} 个（允许）")
    return len(all_names), len(cg_drift)


def check_claude_commands(issues: list[Issue], quiet: bool) -> int:
    if not CLAUDE_COMMANDS.is_dir():
        return 0
    count = 0
    for path in sorted(CLAUDE_COMMANDS.glob("*.md")):
        count += 1
        text = read_text(path, issues)
        check_line_endings(path, text, issues)
        fm_text, _ = split_frontmatter(text)
        if fm_text is None:
            issues.append(Issue("ERROR", rel(path), "missing-frontmatter",
                                "Claude command 缺 frontmatter（至少需要 description）"))
            continue
        try:
            fm = _parse_yaml(fm_text)
        except Exception as exc:  # noqa: BLE001
            issues.append(Issue("ERROR", rel(path), "yaml-error", f"frontmatter 解析失败：{exc}"))
            continue
        if not isinstance(fm, dict) or "description" not in fm:
            issues.append(Issue("ERROR", rel(path), "missing-description",
                                "Claude command 的 frontmatter 缺 description"))
    if not quiet:
        print(f"  [commands] 校验 .claude/commands/*.md：{count} 个")
    return count


def check_text_hygiene(issues: list[Issue], quiet: bool) -> int:
    """全仓扫 BOM / 行尾（覆盖 .md/.yaml/.py/.sh/.ps1 等文本文件）。"""
    count = 0
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        # SKILL.md / commands 已在专项检查里报过，避免重复
        if path.name == "SKILL.md" or CLAUDE_COMMANDS in path.parents:
            continue
        count += 1
        text = read_text(path, issues)          # 顺带报 BOM
        check_line_endings(path, text, issues)
    if not quiet:
        print(f"  [hygiene] 扫描文本文件：{count} 个（BOM / 行尾）")
    return count


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def check_skill_refs(issues: list[Issue], all_names: set[str], quiet: bool) -> int:
    """校验各 skill 的「关联 Skill」表：引用的名字必须是真实 skill（或显式标注）。

    触发背景：`api-first-modular` 曾被写成 `api-first`、`code-debugger` 被写成 `debug`，
    三镜像各自漂移，路由表指向不存在的 skill，属于一类“静默失效”缺陷。

    约定（与 CONTRIBUTING.md 「关联 Skill 无悬空引用」一致）：
      - 外部 skill：名字后加 `（外部）` / `(external)`，跳过存在性校验
      - 非 skill 的沉淀库 / 产物：整个名字写成 `—（…，非 skill）` 或 `-`，跳过
    """
    checked = 0
    mirrors = collect_mirror_skills([])
    for platform, table in sorted(mirrors.items()):
        for _name, path in sorted(table.items()):
            text = read_text(path, [])
            _fm, body = split_frontmatter(text)
            m = re.search(r"^##\s*关联\s*Skill.*?$", body, re.M)
            if not m:
                continue
            rest = body[m.end():]
            stop = re.search(r"^##\s", rest, re.M)
            if stop:
                rest = rest[: stop.start()]
            for line in rest.split("\n"):
                s = line.strip()
                if not s.startswith("|"):
                    continue
                cells = [c.strip() for c in s.strip("|").split("|")]
                if len(cells) < 2:
                    continue
                relation, ref = cells[0], cells[1]
                if relation == TABLE_HEADER_FIRST_CELL or set(relation) <= set("-: "):
                    continue
                if ref in MARKDOWN_ROW_NOISE or "（外部）" in ref or "(外部)" in ref:
                    continue
                checked += 1
                for target in re.split(r"\s*/\s*", ref):
                    target = target.strip()
                    if not target or target in MARKDOWN_ROW_NOISE:
                        continue
                    if not NAME_RE.match(target) and not target.startswith("scrna-"):
                        # 含中文 → 作者已用自然语言描述非 skill 目标，视为声明，跳过
                        continue
                    if target not in all_names:
                        issues.append(Issue(
                            "ERROR", rel(path), "dangling-skill-ref",
                            f"「关联 Skill」表引用了不存在的 skill：{target!r}"
                            "（若为外部 skill 请加“（外部）”；若为沉淀库/产物请写“—（…，非 skill）”）",
                        ))
    if not quiet:
        print(f"  [skill-refs] 校验「关联 Skill」引用：{checked} 条")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description="CodeForge skill 元数据 / 格式合规校验")
    parser.add_argument("--quiet", action="store_true", help="仅输出问题")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    parser.add_argument("--warn-as-error", action="store_true", help="把 WARN 也视为失败")
    args = parser.parse_args()

    issues: list[Issue] = []
    quiet = args.quiet or args.json          # --json 时也静默进度行，否则 JSON 前混入文本导致解析失败
    if not quiet:
        print("CodeForge skill 合规校验")
        print("=" * 62)

    mirrors = collect_mirror_skills(issues)
    skill_count = 0
    for platform, table in sorted(mirrors.items()):
        for name, path in sorted(table.items()):
            skill_count += 1
            validate_skill_md(path, issues, platform=platform)

    total_skills, drift = check_mirrors(issues, quiet)
    cmd_count = check_claude_commands(issues, quiet)
    text_count = check_text_hygiene(issues, quiet)
    all_skill_names = set(mirrors["codex"]) | set(mirrors["gemini"]) | set(mirrors["claude"])
    ref_count = check_skill_refs(issues, all_skill_names, quiet)

    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    if args.json:
        print(json.dumps({
            "skills_scanned": skill_count,
            "mirror_skills": total_skills,
            "commands_scanned": cmd_count,
            "skill_refs_checked": ref_count,
            "text_files_scanned": text_count,
            "errors": [i.as_dict() for i in errors],
            "warnings": [i.as_dict() for i in warns],
            "ok": not errors and not (args.warn_as_error and warns),
        }, ensure_ascii=False, indent=2))
    else:
        if errors or warns:
            print()
        for level, group in (("ERROR", errors), ("WARN", warns)):
            for i in group:
                detail = f" — {i.detail}" if i.detail else ""
                print(f"  [{level}] {i.path}  ({i.rule}){detail}")
        if not args.quiet:
            print()
            print("=" * 62)
            print(f"  skill 检查 {skill_count} 个 | command {cmd_count} 个 | 文本文件 {text_count} 个")
            print(f"  关联 Skill 引用 {ref_count} 条；claude↔gemini 正文不一致 {drift}/{total_skills} 个")
            if not errors:
                print(f"  ✅ 无阻塞问题（{len(warns)} 条提示）")
            else:
                print(f"  ❌ {len(errors)} 条阻塞问题，{len(warns)} 条提示")

    if errors:
        return 1
    if args.warn_as_error and warns:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
