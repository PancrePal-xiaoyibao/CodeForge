# -*- coding: utf-8 -*-
"""
tools-catalog.py — dev-host-init 部署方式目录（问卷选项 + 命令含真实下载源）
============================================================================
被 render-now.py 引用：提供「工具 → 多个安装方式(源码/二进制/包管理器/官方安装器)」，
供 init 问卷选择与「开发工具部署计划」渲染。同时含「美术风格预设」与「自由文本配色生成」。

【脱敏】本文件只含公开下载源与通用占位（<版本>、<仓库URL>）；不出现仓库本地绝对路径、
SSH 别名、VPS IP 或任何本机专属字面量。Windows 用 %LOCALAPPDATA% 兜底、POSIX 只有 $HOME。
"""
import os, hashlib, json


# ---------- 工具部署目录：name → {windows/posix: [选项]}, note ----------
# 每个选项 {label, kind(源码/二进制/包管理器/官方安装器), cmd}
TOOL_INSTALL = {
    "codebase-memory-mcp": {
        "note": ("纯 C 实现：npm/uv/pip 渠道背后仍是下载预编译二进制，无真编译产物。"
                 "Linux 低 glibc 需用 -portable 包或源码编译（DEPLOYMENT.zh-CN.md 有实测）。"
                 "装后 `codebase-memory-mcp install -y` 自动配置 Claude/Codex 的 MCP + hook + skill。"),
        "windows": [
            {"label": "官方安装脚本（推荐）", "kind": "二进制", "cmd":
                'irm https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 | iex'},
            {"label": "源码本地编译", "kind": "源码", "cmd":
                'git clone https://github.com/DeusData/codebase-memory-mcp && cd codebase-memory-mcp '
                '&& scripts/build.sh && copy build\\c\\codebase-memory-mcp.exe %LOCALAPPDATA%\\bin\\'},
            {"label": "npm 全局", "kind": "包管理器", "cmd": "npm i -g codebase-memory-mcp"},
            {"label": "uv tool", "kind": "包管理器", "cmd": "uv tool install codebase-memory-mcp"},
        ],
        "posix": [
            {"label": "官方安装脚本（推荐）", "kind": "二进制", "cmd":
                'curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash'},
            {"label": "源码本地编译", "kind": "源码", "cmd":
                "git clone https://github.com/DeusData/codebase-memory-mcp && cd codebase-memory-mcp "
                "&& scripts/build.sh && cp build/c/codebase-memory-mcp ~/.local/bin/"},
            {"label": "npm 全局", "kind": "包管理器", "cmd": "npm i -g codebase-memory-mcp"},
            {"label": "uv tool", "kind": "包管理器", "cmd": "uv tool install codebase-memory-mcp"},
        ],
    },
    "pi（@earendil-works/pi-coding-agent）": {
        "note": "官方发布渠道以 README/官网为准；Windows 本机走 npm 已装 0.84.4。",
        "windows": [
            {"label": "npm 全局（推荐）", "kind": "包管理器", "cmd": "npm i -g @earendil-works/pi-coding-agent"},
            {"label": "官网二进制/安装器", "kind": "二进制", "cmd": "<官方文档URL> 提供 prebuilt 安装器"},
            {"label": "从源码", "kind": "源码", "cmd":
                "git clone <pi仓库URL> && cd <目录> && npm ci && npm run build && npm i -g ."},
        ],
        "posix": [
            {"label": "npm 全局（推荐）", "kind": "包管理器", "cmd": "npm i -g @earendil-works/pi-coding-agent"},
            {"label": "官网二进制/安装器", "kind": "二进制", "cmd": "<官方文档URL> 提供 prebuilt 安装器"},
        ],
    },
    "gh / GitHub CLI": {
        "note": "免密快速部署：`gh auth login`（凭据存本机，勾选 HTTPS/SSH 凭据）后一条命令做远端操作。",
        "windows": [
            {"label": "winget（包管理器）", "kind": "包管理器", "cmd": "winget install GitHub.cli"},
            {"label": "官网二进制（MSI）", "kind": "二进制", "cmd": "从 https://cli.github.com 下载 .msi"},
            {"label": "源码（go build）", "kind": "源码", "cmd": "git clone https://github.com/cli/cli && cd cli && make"},
        ],
        "posix": [
            {"label": "apt（包管理器）", "kind": "包管理器", "cmd": "sudo apt install gh   # 或 brew install gh"},
            {"label": "官网二进制", "kind": "二进制", "cmd": "curl -fsSL https://cli.github.com/install.sh | sh"},
            {"label": "源码（go build）", "kind": "源码", "cmd": "git clone https://github.com/cli/cli && cd cli && make"},
        ],
    },
    "rg / ripgrep（强烈建议）": {
        "note": "仓库全文检索依赖；缺失则 SKILL 建议 `rg --files`→回退 grep。",
        "windows": [
            {"label": "winget（包管理器）", "kind": "包管理器", "cmd": "winget install BurntSushi.ripgrep.MSVC"},
            {"label": "官网二进制（zip）", "kind": "二进制", "cmd": "从 https://github.com/BurntSushi/ripgrep/releases 下载 zip 解压到 PATH"},
        ],
        "posix": [
            {"label": "apt（包管理器）", "kind": "包管理器", "cmd": "sudo apt install ripgrep   # 或 brew install ripgrep"},
            {"label": "官网二进制", "kind": "二进制", "cmd": "从 releases 下载 static musl 包 放入 ~/.local/bin"},
        ],
    },
    "uv（Python 管理）": {
        "note": "本机已装 0.10.2；新项目 Python 用 uv venv。",
        "windows": [
            {"label": "winget（包管理器）", "kind": "包管理器", "cmd": "winget install astral-sh.uv"},
            {"label": "官方安装器（PowerShell）", "kind": "官方安装器", "cmd": "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\""},
        ],
        "posix": [
            {"label": "官方安装器", "kind": "官方安装器", "cmd": "curl -LsSf https://astral.sh/uv/install.sh | sh"},
        ],
    },
    "node（Node.js）": {
        "note": "多版本管理(源码 via nvm/fnm)、二进制(LTS 安装器)、包管理器(npm i -g)三条路由。",
        "windows": [
            {"label": "官方 LTS 安装器（二进制）", "kind": "二进制", "cmd": "winget install OpenJS.NodeJS.LTS   # 或 nodejs.org LTS .msi"},
            {"label": "nvm-windows（源码多版本）", "kind": "源码", "cmd": "winget install CoreyButler.NVMforWindows"},
        ],
        "posix": [
            {"label": "nvm（源码多版本）", "kind": "源码", "cmd":
                "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v<版本>/install.sh | bash && nvm install --lts"},
            {"label": "官方 tarball（二进制）", "kind": "二进制", "cmd": "从 nodejs.org 下载 LTS tar.xz 解压到 ~/.local"},
        ],
    },
}


# ---------- 美术风格预设（描述性，不唯一于任何领域） ----------
ART_STYLES = [
    {"id": "engineering-calm", "name": "工程冷静 · 深海蓝灰",
     "desc": "低饱和蓝灰主色 + 冷感强调青/钛，克制、专业、可读性优先；适合前后端/基建/CLI 工具/监控面板。",
     "palette": {"primary": "#4A6572", "accent": "#1BA1C6", "bg": "#F4F7F8", "text": "#24303A"},
     "gradient": ["#4A6572", "#1BA1C6"]},
    {"id": "academic-muted", "name": "科研学术 · 暖纸古蓝",
     "desc": "米白纸底 + 古蓝/暗红点缀，克制的数据可视化色；适合论文/报表/生信/文献综述/学术海报。",
     "palette": {"primary": "#A4443C", "accent": "#3A5A78", "bg": "#FAF7F0", "text": "#333A40"},
     "gradient": ["#F0EDE4", "#A4443C"]},
    {"id": "warm-human", "name": "温暖人文 · 焦糖暖橙",
     "desc": "柔和奶油底 + 焦糖/珊瑚暖色，人文感强；适合内容站/社区/教育/医疗/非营利向界面与 PPT。",
     "palette": {"primary": "#C2703D", "accent": "#D98E73", "bg": "#FFF6EE", "text": "#3D3028"},
     "gradient": ["#FFF6EE", "#C2703D"]},
    {"id": "dark-premium", "name": "暗黑高级 · 墨黑鎏金",
     "desc": "近黑底 + 极光强调（金/青），NV 级高级感；适合开发者工具/仪表盘/深色主题产品。",
     "palette": {"primary": "#E3B341", "accent": "#35E0E0", "bg": "#14161B", "text": "#E9EDF2"},
     "gradient": ["#14161B", "#E3B341"]},
    {"id": "nature-fresh", "name": "自然生态 · 苔绿雾松",
     "desc": "低饱和苔绿 + 陶土/雾蓝语义，透气的自然感；适合生物/医药/环保/健康类应用与图表。",
     "palette": {"primary": "#5E8875", "accent": "#C79A6B", "bg": "#F5F7F2", "text": "#2E4038"},
     "gradient": ["#F5F7F2", "#5E8875"]},
    {"id": "art-vivid", "name": "艺术活力 · 钴蓝朱红",
     "desc": "高饱和钴蓝 + 朱红/橙黄点缀，年轻有张力；适合创意/平面设计/插画/营销/品牌物料与演示。",
     "palette": {"primary": "#2E5CB8", "accent": "#E2583E", "bg": "#FAFAF5", "text": "#1D2233"},
     "gradient": ["#FAFAF5", "#2E5CB8"]},
]


def style_by_id(sid):
    return next((s for s in ART_STYLES if s["id"] == sid), None)


def palette_text(style, task_hint=""):
    c = style["palette"]
    lines = [
        "## 配色基调（init 问卷生成；可随时在 agent-reference/visualization.md 自调）", "",
        f"- 风格：{style['name']} — {style['desc']}",
        f"- 主基调：{c['primary']} / 强调：{c['accent']} / 背景：{c['bg']} / 正文：{c['text']}",
        f"- 语义渐变：{style['gradient'][0]} → {style['gradient'][1]}",
    ]
    if task_hint:
        lines.insert(1, f"> 任务提示：{task_hint}\n")
    return "\n".join(lines)


def auto_palette(seed_text):
    """自由文本 → 初始配色提案（确定性、零网络、零随机）。

    规则：从种子取稳定哈希映射到离散「色相族」，叠加 CBDR 明暗对比与可读性建议。
    不是"智能设计器"，只是无手调基础下保证不刺眼、有记忆点的人类可改起点。
    """
    if not seed_text:
        return ""
    b = hashlib.sha256(seed_text.encode("utf-8")).digest()
    fams = [
        ("深海蓝",   "#1A4B6E", "#2E86AB", "#A8D8EA"),
        ("暮紫",     "#3D348B", "#6A5AE0", "#D0C4F0"),
        ("暖橙焦糖", "#B2501F", "#E8853D", "#F6D9B8"),
        ("苔绿",     "#4F7A5B", "#7BA58B", "#CCE0D2"),
        ("朱红",     "#A62A2A", "#E2574B", "#F6CDCB"),
        ("金棕",     "#A87C2C", "#D4A940", "#F0E2C0"),
        ("青瓷",     "#2F6D6D", "#4E9E9E", "#C3E5E5"),
        ("雾灰高级", "#46494D", "#7E8A93", "#D9E0E4"),
    ]
    name, dark, mid, light = fams[b[0] % len(fams)]
    accent = "#E2B341" if b[1] % 2 else "#E2574B"
    bg = "#FAF8F4" if b[2] % 2 else "#F4F6F8"
    text = "#232A30"
    return (
        "## 配色基调（由你的自由文本生成的初始提案；喜欢就留，不喜欢在 visualization.md 改）\n\n"
        f"- 种子：`{seed_text[:40]}{'…' if len(seed_text) > 40 else ''}`\n"
        f"- 主基调：{dark} / 强调：{accent} / 背景：{bg} / 正文：{text}\n"
        f"- 语义渐变：{light} → {mid} → {dark}（分类可用 {name} 系做主线，语义冷暖可再加一极）\n"
        "- 建议：正文对比度优先（深底浅字或浅底深字）；类别色 ≥6 时拉开色相，避免接近色混淆。\n")


# ---------- 渲染：目录 JSON / 部署 TODO / 触发表 ----------
def catalog_for_platform():
    kind = "windows" if os.name == "nt" else "posix"
    out = {}
    for name, spec in TOOL_INSTALL.items():
        opts = spec.get(kind, [])
        out[name] = {"options": [o["label"] for o in opts],
                     "kinds": [o["kind"] for o in opts],
                     "commands": {o["label"]: o["cmd"] for o in opts},
                     "note": spec.get("note", "")}
    return out


def render_install_todo(picks):
    """picks: {工具名: 选项label} → '## 开发工具部署计划' Markdown；空则返回 ''"""
    if not picks:
        return ""
    kind = "windows" if os.name == "nt" else "posix"
    lines = ["## 开发工具部署计划（本次 init 问卷选择）", ""]
    for name, label in picks.items():
        spec = TOOL_INSTALL.get(name, {})
        opts = spec.get(kind, [])
        cmd = next((o["cmd"] for o in opts if o["label"] == label), None)
        note = spec.get("note", "")
        lines.append(f"### {name} — {label}")
        if cmd:
            lines.append(f"```bash\n{cmd}\n```")
        lines.append("")
    lines.append("> 确认执行前请先逐条核对命令源的版本/Linux-dist 差异；不可逆源先 dry-run。")
    return "\n".join(lines).strip()


def viz_trigger_table():
    return ("| 科研配色、可视化、图表风格或你建的领域参考 | agent-reference/visualization.md |\n"
            "| 需要一类风格/趋势速查或你的历史参考 | 自建 agent-reference/patterns.md |")


def catalog_json():
    return json.dumps(catalog_for_platform(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    if "--catalog" in sys.argv:
        print(catalog_json())
    elif "--auto-demo" in sys.argv:
        print(auto_palette("前端 Vue 仪表盘，深色科技感"))
    else:
        print(render_install_todo({"codebase-memory-mcp": "官方安装脚本（推荐）",
                                   "rg / ripgrep（强烈建议）": "winget（包管理器）"}))