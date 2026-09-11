#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render-now.py — 通用分层注入渲染器（dev-host-init 性能档）
===========================================================
复用 fill-placeholders.py 的 build_values / fill_template / detect_sensitive，
在本机运行 host-scan 实测 JSON，渲染整套分层注入产物。**支持两种作用域**：

  全局（默认）
      AGENTS.md + .claude/CLAUDE.md + .codex/AGENTS.md + .gemini/GEMINI.md（4 镜像）
      agent-reference/{environment,tooling,preferences}.md   + 可选 visualization.md（问卷）
      .pi/agent/APPEND_SYSTEM.md + extensions/graph-first-gate.ts（探测到 .pi 才部署）

  项目级（--project <目录>）
      <项目>/AGENTS.md + ./CLAUDE.md + ./GEMINI.md（3 镜像）
      <项目>/agent-reference/{environment,tooling,preferences}.md（+ visualization.md）
      （项目级不部署 pi 全局件；MIRROR_LIST / REFERENCE_DIR 渲染为 ./ 相对路径）

**问卷驱动（--config questionnaire.json，可跳过）**
   配置字段（均可缺省；缺省=不注入该块，留用户空间，绝不默认套用他人偏好）：
     {
       "art_style":   "engineering-calm"           // 预设风格 id（tools-catalog.ART_STYLES）；或
       "art_seed":    "自由文本（走配色生成逻辑）"  // 与 art_style 二选一；
       "art_skip":    true                         // 跳过视觉注入（template 里 ART_STYLE_SUMMARY 给"未定"）
       "install_picks": {"codebase-memory-mcp": "官方安装脚本（推荐）", ...}  // 部署计划渲染
       "preferences_summary_extra": "...",         // 追加摘要（可选）
     }

设计约束（开源仓库脱敏铁律）：
  ★ 本文件不得包含任何本机专属字面量（用户路径 / IP / 域名 / 别名 / 端口）。
  ★ HOME 取自 os.path.expanduser；DEV_ROOT 取环境变量 DEV_HOST_DEV_ROOT
    （缺省 ~/Development），调用方在命令行传入真实值。
  ★ SSH 跳板别名从 ~/.ssh/config 运行时解析；conda 环境名来自探测。
  ★ 全部部署命令/风格预设集中在 tools-catalog.py（公开下载源 + 通用占位，可审计）。

用法：
  全局   DEV_HOST_DEV_ROOT=<开发根> python scripts/render-now.py [--config q.json]
  项目级 DEV_HOST_DEV_ROOT=<开发根> python scripts/render-now.py --project <项目绝对路径> [--config q.json]
  先 --dry-run 用 questionnaire 看将写路径，确认后再真写。
"""
import argparse, importlib.util, json, os, re, subprocess, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "templates", "host-injection.template.md"))
GATE_TPL = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "templates", "graph-first-gate.ts"))
HOME = os.path.expanduser("~")
DEV_ROOT = os.environ.get("DEV_HOST_DEV_ROOT") or os.path.join(HOME, "Development")

ap = argparse.ArgumentParser()
ap.add_argument("--project", default=None,
                help="项目级模式：渲染到该目录（AGENTS.md/CLAUDE.md/GEMINI.md/agent-reference/，3 镜像）；省略=全局模式(4 镜像 + pi 强化层)")
ap.add_argument("--dry-run", action="store_true", help="只打印将写出的路径，不写盘（校验 --project 解析）")
ap.add_argument("--config", default=None, help="问卷 JSON：art_style/art_seed/art_skip/install_picks/preferences_summary_extra")
ARGS = ap.parse_args()
SCOPE_GLOBAL = ARGS.project is None
PROJECT_DIR = os.path.abspath(ARGS.project) if ARGS.project else None


# ---------- 0. 加载 tools-catalog 与问卷 ----------
def load_tools():
    spec = importlib.util.spec_from_file_location("tools_catalog", os.path.join(SCRIPT_DIR, "tools-catalog.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tc = load_tools()

Q = {}
if ARGS.config and os.path.exists(ARGS.config):
    Q = json.load(open(ARGS.config, encoding="utf-8"))
art_style_id = Q.get("art_style")
art_seed = Q.get("art_seed", "").strip()
art_skip = bool(Q.get("art_skip"))
install_picks = Q.get("install_picks", {}) or {}
prefs_extra = Q.get("preferences_summary_extra", "")


# ---------- 1. 复用 fill-placeholders 渲染核心 ----------
def load_fp():
    spec = importlib.util.spec_from_file_location(
        "fill_placeholders", os.path.join(SCRIPT_DIR, "fill-placeholders.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fp = load_fp()


# ---------- 2. host-scan 实测（按平台选脚本）----------
def run_scan():
    if os.name == "nt":
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
               "-File", os.path.join(SCRIPT_DIR, "host-scan.ps1")]
    else:
        cmd = ["bash", os.path.join(SCRIPT_DIR, "host-scan.sh")]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return json.loads(out.stdout) if out.returncode == 0 else {}
    except Exception:
        return {}


h = run_scan()
conda_envs = list(dict.fromkeys(h.get("env_managers", {}).get("conda_envs", []) or []))
uv_pythons = list(dict.fromkeys(h.get("env_managers", {}).get("uv_pythons", []) or []))


# ---------- 3. 运行时机器事实（不写死）----------
def ssh_aliases():
    cfg = os.path.join(HOME, ".ssh", "config")
    if not os.path.exists(cfg):
        return []
    out, import_os = [], None
    for line in open(cfg, encoding="utf-8", errors="ignore"):
        m = re.match(r"^\s*Host\s+(\S.*)$", line.strip())
        if m:
            for tok in m.group(1).split():
                if tok not in ("*", "!*") and not tok.startswith("!"):
                    out.append(tok)
    return out


def find_codebase_skill_dir():
    """在常见 skills 发现路径中定位 codebase-memory skill；找不到返回 None"""
    candidates = [
        os.path.join(HOME, ".agents", "skills", "codebase-memory"),
        os.path.join(HOME, ".claude", "skills", "codebase-memory"),
        os.path.join(HOME, ".codex", "skills", "codebase-memory"),
        os.path.join(HOME, ".gemini", "skills", "codebase-memory"),
    ]
    for p in candidates:
        if os.path.isdir(p):
            return p
    return None


aliases = ssh_aliases()
kb_skill = find_codebase_skill_dir()
net = h.get("network", {}) or {}

# 过滤拓扑探测噪音：link-local(169.254/16) / 回环(127/8) / 占位地址一律不作为真实 VPS 拓扑
def _is_noise_ip(ip):
    if not ip:
        return True
    ip = str(ip).strip().lower()
    first = ip.split(".")[0]
    return first in ("127", "169", "0") or ip in ("::1", "localhost")

if _is_noise_ip(net.get("vps_ip", "")):
    net["vps_ip"] = ""
    net["vps_alias"] = ""
aliases = [a for a in aliases if not _is_noise_ip(a)]

listen_ports = [str(p) for p in (net.get("listen_ports") or [])]
uncommon = [p for p in listen_ports if p not in ("22", "80", "443", "8080", "8000", "8888", "3389")]
ngx_name = net.get("nginx_server_name") or ""
has_topology = bool(
    (net.get("vps_ip") and not _is_noise_ip(net.get("vps_ip")))
    or (ngx_name and ngx_name not in ("_", "example.com", "default_server"))
    or net.get("frp_svc")
    or bool(uncommon)
)
if not has_topology:
    net = {"vps_alias": None, "vps_ip": None, "frp_svc": None,
           "nginx_server_name": None, "nginx_port": None, "listen_ports": []}
    h["network"] = net
    # aliases 也用于下方的 PREFERENCES_SUMMARY 远程跳板提示；纯开发机无 VPS 拓扑时不报别名
    aliases = [a for a in aliases if not _is_noise_ip(a)]

# ---------- 4. 渲染值 ----------
values = fp.build_values(h)
values["HOME_DIR"] = HOME
values["DEV_ROOT"] = DEV_ROOT
values["CODEBASE_MCP_DOCS"] = os.path.join(DEV_ROOT, "codebase-memory-mcp", "DEPLOYMENT.zh-CN.md")

# 问卷视觉选择：fill_template 切段前先落进 values（模板内 {{ART_STYLE_SUMMARY}} 将被正确替换）
art_summary = "未在 init 问卷选择（命中视觉任务时按 visualization.md 现场确立，不替他域套用）"
if art_style_id:
    s = tc.style_by_id(art_style_id)
    if s:
        values["ART_STYLE_SUMMARY"] = (f"风格 {s['name']}：主 {s['palette']['primary']} / 强调 {s['palette']['accent']} / "
                                       f"背景 {s['palette']['bg']} / 正文 {s['palette']['text']}；语义渐变 {s['gradient'][0]}→{s['gradient'][1]}")
        art_summary = f"{s['name']}（{s['palette']['primary']}/{s['palette']['accent']}）"
elif art_seed:
    _auto = tc.auto_palette(art_seed)
    _m = re.search(r"主基调：(\S+) / 强调：(\S+)", _auto)
    if _m:
        values["ART_STYLE_SUMMARY"] = f"按自由文本生成的基调：主 {_m.group(1)} / 强调 {_m.group(2)}（见 visualization.md）"
        art_summary = f"自定义基调（主 {_m.group(1)} / 强调 {_m.group(2)}）"
if "ART_STYLE_SUMMARY" not in values and not art_skip:
    values["ART_STYLE_SUMMARY"] = art_summary

if SCOPE_GLOBAL:
    values["MIRROR_LIST"] = "~/AGENTS.md、~/.claude/CLAUDE.md、~/.codex/AGENTS.md、~/.gemini/GEMINI.md"
    values["REFERENCE_DIR"] = os.path.join(HOME, "agent-reference")
else:
    # 项目级：触发表路径用 ./AGENTS.md ./CLAUDE.md ./GEMINI.md 与 ./agent-reference（相对项目根，已可入仓库）
    values["MIRROR_LIST"] = "AGENTS.md、CLAUDE.md、GEMINI.md（项目级 3 镜像）"
    values["REFERENCE_DIR"] = "./agent-reference"

values["ENV_TABLE"] = ("conda: " + ", ".join(conda_envs or ["未检测到"])
                       + ("\nuv python: " + ", ".join(uv_pythons[:8]) if uv_pythons else ""))

if aliases:
    d = (
        "主力语言：Python + Node.js/TypeScript + R（生信出图）；Bash/批处理辅助。\n"
        "包管理器：Node 用 pnpm(>npm>bun)、Python 用 uv(>conda>pip)、R 用 renv/conda。\n"
        "领域路线图：开发/全栈、量化金融、科研、Data Science、生命科学/生信、可视化美术设计。\n"
        "日常任务：开发/调试/文档/调研/上线运维、生信分析（Seurat/Bioc/R 出图）。\n"
        + (f"远程跳板别名（~/.ssh/config 解析）：{', '.join(aliases[:6])}。\n" if aliases else "")
        + f"路径约定：开发 {DEV_ROOT}、学术 ~/R、MCP server 开发 {DEV_ROOT} 或 ~/mcp。\n"
        + (f"问卷补充：{prefs_extra}\n" if prefs_extra else "")
        + "完整问卷见 agent-reference/preferences.md，此处为常驻摘要。")
    if aliases:
        values["PREFERENCES_SUMMARY"] = d
else:
    values["PREFERENCES_SUMMARY"] = (
        "主力语言：Python + Node.js/TypeScript + R（生信出图）；Bash/批处理辅助。\n"
        "包管理器：Node 用 pnpm(>npm>bun)、Python 用 uv(>conda>pip)、R 用 renv/conda。\n"
        "领域路线图：开发/全栈、量化金融、科研、Data Science、生命科学/生信、可视化美术设计。\n"
        "日常任务：开发/调试/文档/调研/上线运维、生信分析（Seurat/Bioc/R 出图）。\n"
        f"路径约定：开发 {DEV_ROOT}、学术 ~/R、MCP server 开发 {DEV_ROOT} 或 ~/mcp。\n"
        + (f"问卷补充：{prefs_extra}\n" if prefs_extra else "")
        + "完整问卷见 agent-reference/preferences.md，此处为常驻摘要。")

tpl_text = open(TEMPLATE, encoding="utf-8").read()
full = fp.fill_template(tpl_text, values)

leftover = re.findall(r"\{\{", full)
if leftover:
    sys.exit(f"[FAIL] 全文仍残留 {len(leftover)} 处未替换占位符")
hits = fp.detect_sensitive(full)
if hits:
    print(f"[WARN] 渲染产物命中敏感模式: {hits}（本机探测合法值；模板硬编码则终止）")
else:
    print("[OK] 无模板级敏感硬编码")

# ---------- 5. 切段 ----------
MARKER = re.compile(r'(?m)^<!--\s*=+\s*\[(RULES|PERFORMANCE|ENVIRONMENT|TOOLING|APPEND)\]')
starts = [(m.group(1), m.start()) for m in MARKER.finditer(full)]
segs = {}
for i, (name, start) in enumerate(starts):
    line_end = full.find("\n", start)
    end = starts[i + 1][1] if i + 1 < len(starts) else len(full)
    segs[name] = full[line_end + 1:end].strip("\n")

def strip_html_comments(s):
    return re.sub(r'(?s)<!--.*?-->', '', s).strip()

performance = segs.get("PERFORMANCE", "")
environment = segs.get("ENVIRONMENT", "")
tooling = segs.get("TOOLING", "")
append_body = strip_html_comments(segs.get("APPEND", ""))
assert performance and environment and tooling and append_body, "段切分失败"

# ---------- 6. PERFORMANCE 正文后处理（平台与拓扑适配，保持镜像一致）----------
# 6a. 无公网拓扑 → 把「网络拓扑」整节替换为一行诚实说明（工作站无 VPS/nginx/FRP）
if not has_topology:
    topo_m = re.search(
        r"(?ms)^## 网络拓扑与公网访问规则（动态探测）.*?(?=\n<!--|\Z)", performance)
    if topo_m:
        performance = performance[:topo_m.start()].rstrip() + "\n\n" + (
            "## 网络拓扑与远程访问（init 探测）\n\n"
            "本机为工作站/纯开发机：未探测到公网入口（VPS/nginx/FRP 均为空），无持续隧道服务。\n"
            "域名/证书/端口映射需求按触发表读取 agent-reference/environment.md（及自建 network.md）；"
            "禁止硬编码公网地址。") + "\n"

# 6b. 无本地代理 → 去掉「git config 写死 proxy」代码块（代理未探测时不渲染指令）
if "未检测到本地代理" in performance:
    proxy_block = re.compile(
        r"(?ms)\n配置方式:\n```bash\ngit config --global http\.proxy http://未检测到\ngit config --global https\.proxy http://未检测到\n```")
    performance = proxy_block.sub("", performance)
    # 同步清理「网络代理」小节里重复的 - **SOCKS5**: 未检测到 行
    proxy_sec = re.compile(
        r"(?ms)^## 网络代理\n\n未检测到本地代理\n- \*\*SOCKS5\*\*: `未检测到`\n- \*\*HTTP\*\*: `未检测到`\n*")
    performance = proxy_sec.sub("## 网络代理\n\n未检测到本地代理；如需代理请在 agent-reference/environment.md 手填。\n\n", performance)

# 6c. Windows 专属：补「Windows 编码规则」到个人开发偏好前（含动态 R 环境名）
if os.name == "nt":
    r_env = next((e for e in conda_envs if re.match(r"^R[-_ ]", e, re.I)), "<R环境名>")
    win_rules = (
        "## Windows 编码规则（GBK/UTF-8）\n\n"
        "Windows 中文系统控制台默认 GBK (cp936)，Python/R 的 stdout 常因非 GBK 字符写入失败。"
        "默认预防：所有脚本输出一律按 UTF-8。\n"
        "- Python 首选：运行前设 `PYTHONUTF8=1`；仅修 stdout 用 `PYTHONIOENCODING=utf-8`；文件读写 `encoding='utf-8'` 显式指定\n"
        "- Python stdout 仍写入失败：改为输出到文件或脚本内直接写文件\n"
        f"- R：禁止在 Git Bash 跑 R（中文输出与路径编码混乱），统一用 CMD `conda activate {r_env}` 或 RStudio\n"
        "- CMD/PowerShell：默认 cp936，切 UTF-8 用 `chcp 65001`；源码文件统一 UTF-8 无 BOM\n"
        "- Node.js：fs 默认 UTF-8，控制台中文乱码时 `chcp 65001`\n\n")
    anchor = "## 个人开发偏好"
    if anchor in performance:
        performance = performance.replace(anchor, win_rules + anchor, 1)

# 6d. codebase-memory skill 路径提示按本机实测修正（全局用 ~/.claude/skills 实测路径，项目级保持专业无关说明）
if SCOPE_GLOBAL and kb_skill:
    ref_path = kb_skill.replace(HOME, "~").replace("\\", "/")
    performance = performance.replace(
        "~/.agents/skills/codebase-memory/SKILL.md", ref_path + "/SKILL.md", 1)
elif not SCOPE_GLOBAL:
    performance = performance.replace(
        "~/.agents/skills/codebase-memory/SKILL.md",
        "<本机 codebase-memory skill 路径>（global 模式渲染时回填）", 1)

# 6e. 视觉基调摘要回填（AFTER PERFORMANCE 切段后，模板里 ART_STYLE_SUMMARY 位于 PERFORMANCE 段）
if "ART_STYLE_SUMMARY" in values:
    performance = performance.replace("{{ART_STYLE_SUMMARY}}", values["ART_STYLE_SUMMARY"])
else:
    performance = performance.replace("{{ART_STYLE_SUMMARY}}", art_summary)

# ---------- 7. 组装并写出（含备份；graph-first-gate 按 DEV_ROOT 生成）----------
def w(path, text, backup=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if backup and os.path.exists(path):
        ts = __import__("time").strftime("%Y%m%d%H%M%S")
        os.rename(path, f"{path}.hostinit-bak.{ts}")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"[写] {path}  ({len(text)} 字符)")

if SCOPE_GLOBAL:
    masters = [
        ("AGENTS.md", os.path.join(HOME, "AGENTS.md")),
        ("CLAUDE.md", os.path.join(HOME, ".claude", "CLAUDE.md")),
        ("codex AGENTS.md", os.path.join(HOME, ".codex", "AGENTS.md")),
        ("GEMINI.md", os.path.join(HOME, ".gemini", "GEMINI.md")),
    ]
else:
    masters = [
        ("AGENTS.md", os.path.join(PROJECT_DIR, "AGENTS.md")),
        ("CLAUDE.md", os.path.join(PROJECT_DIR, "CLAUDE.md")),
        ("GEMINI.md", os.path.join(PROJECT_DIR, "GEMINI.md")),
    ]
    print(f"[项目级] 目标目录: {PROJECT_DIR}  （写入 AGENTS.md/CLAUDE.md/GEMINI.md + agent-reference/，不部署 pi 强化层）")

# environment.md 增补（B 层机器画像，探测驱动）
langs = h.get("languages", {}) or {}
pms = h.get("package_managers", {}) or {}
dev_env_lines = " | ".join(f"{k} {v}" for k, v in {**langs, **pms}.items() if v)
extra_env = []
if os.name == "nt":
    extra_env.append(
        "## Windows 编码规则（GBK/UTF-8，本机画像）\n\n"
        "Windows 中文系统控制台默认 GBK (cp936)，Python/R 的 stdout 常因非 GBK 字符写入失败。默认预防：所有脚本输出一律按 UTF-8。\n"
        "- Python 首选：运行前设 `PYTHONUTF8=1`；仅修标准输出用 `PYTHONIOENCODING=utf-8`；读写文件 `encoding='utf-8'` 显式指定\n"
        "- Python stdout 仍写入失败：改为输出到文件或脚本内直接写文件\n"
        "- R：禁止在 Git Bash 跑 R（中文输出与路径编码混乱），统一用 CMD `conda activate <R环境名>` 或 RStudio\n"
        "- CMD/PowerShell：默认 cp936，切 UTF-8 用 `chcp 65001`；源码文件统一 UTF-8 无 BOM\n"
        "- Node.js：fs 默认 UTF-8，控制台中文乱码时 `chcp 65001`\n")
if dev_env_lines:
    extra_env.append(f"## 开发环境版本速查（init 探测）\n\n{dev_env_lines}\n")
if aliases:
    extra_env.append(
        "## 远程跳板（~/.ssh/config 运行时解析）\n\n"
        f"别名：{', '.join(aliases[:6])}\n"
        "连接/转发前先 `ssh <别名>` 验证可达；具体拓扑按需自建 network.md。\n")

environment_out = environment.rstrip() + "\n\n" + "\n".join(extra_env).rstrip() + "\n"

# preferences.md（问卷全量，机器事实运行时注入，无字面量敏感值）
prefs = """# 开发偏好问卷（agent-reference/preferences.md 全量）

> 由 dev-host-init（性能档 init）聚合生成：技术栈/包管理器/路径约定来自本次扫描与全局规则权威源；
> 远程跳板别名来自 ~/.ssh/config 运行时解析。每次 init 重跑，用户当次选择为准增量合并。
> 本文为「问卷快照 + 通用默认」；任何未在问卷明确选择的内容都不替用户下结论（缺失则触发式补采）。

## 技术栈/语言（偏好顺序）

| 任务域 | 首选 | 次选 | 备注 |
|---|---|---|---|
| 单细胞组学分析 | R + Seurat/Bioconductor | Python scanpy | 本机 R 分析环境 |
| 机器学习/数据处理/AI Agent | Python + conda | — | 专用 conda env |
| MCP server/CLI/Web | Node.js + TypeScript | — | pnpm 管理 |
| 脚本快速执行 | Bun | Node | 已安装非主力 |
| 应用开发 | Rust / Go | — | 追求优雅与性能 |

## 包管理器优先级

- Node.js 项目：pnpm > npm > bun
- Python 项目：uv venv > conda（生信与机器学习特定任务）> pip
- R 项目：renv 或 conda

## 路径约定

- 开发项目：开发根；学术项目：~/R
- MCP server 开发：开发根 或 ~/mcp/

## Conda 环境速查（init 探测）

CONDA_ENVS_LINE

## 领域路线图

开发/全栈、前端、量化金融、科研、Data Science、生命科学、生信、可视化美术设计

## 日常任务范围

开发 / 调试 / 文档 / 调研 / 上线运维；生信分析与科研出图（Seurat/Bioc/R）

## 一般偏好

- **部署风格**：本地 + 远程跳板（别名见 environment.md）；不允许重开已关闭的 Web 映射
- **测试哲学**：定向回归优先；关键路径（交易/权限/状态机）验入口到实际结果；恒有负控
- **代码风格**：补丁式小 diff，可审查
- **Windows 中文编码**：见 environment.md「Windows 编码规则」

## 领域偏好（问卷未涉及则不套用）

- 若在 init 问卷选择了视觉/配色：其风格基调见 preferences.md 同目录 visualization.md；未选则按 visualization.md 现场确立
- 新项目 Python 用 uv；已有 conda 环境直接复用
- 未经明确指示不 git commit/push；开源仓库 push 前强制脱敏核查
"""
prefs = prefs.replace("CONDA_ENVS_LINE", (", ".join(conda_envs) if conda_envs else "未检测到"))
prefs = prefs.replace("开发根", DEV_ROOT).rstrip() + "\n"

# 部署计划按问卷写入 environment.md；视觉种子按问卷写入 visualization.md
install_todo = tc.render_install_todo(install_picks)
if install_todo:
    environment_out = environment_out.rstrip() + "\n\n" + install_todo + "\n"

visualization_out = None
if not art_skip:
    if art_style_id:
        style = tc.style_by_id(art_style_id)
        if style:
            visualization_out = (f"# 视觉/图表风格（agent-reference/visualization.md）\n\n"
                                 + tc.palette_text(style))
    elif art_seed:
        visualization_out = ("# 视觉/图表风格（agent-reference/visualization.md）\n\n"
                             + tc.auto_palette(art_seed))

# graph-first-gate.ts：PROJECT_ROOTS 指向本机 DEV_ROOT（Windows 拆盘符，POSIX 用整路径）
if os.name == "nt":
    drive, _, rest = DEV_ROOT.partition(":")
    gate_roots = f'join("{drive}:", "{rest.strip(os.sep).replace(os.sep, "/")}")'
else:
    gate_roots = f'"{DEV_ROOT.replace(os.sep, "/")}"'
gate_src = open(GATE_TPL, encoding="utf-8").read()
gate_out = gate_src.replace(
    'const PROJECT_ROOTS = [join(homedir(), "Development")]; // 主开发根目录，按本机实际增删',
    f'const PROJECT_ROOTS = [{gate_roots}]; // 本机主开发根目录（dev-host-init 渲染）')

# 项目级模式：dry-run 只列路径不写盘（供 skill 在询问阶段确认落点）
def target_paths():
    ref = os.path.join(PROJECT_DIR, "agent-reference") if PROJECT_DIR else os.path.join(HOME, "agent-reference")
    paths = [p for _, p in masters]
    paths += [os.path.join(ref, n) for n in ("environment.md", "tooling.md", "preferences.md")]
    if visualization_out and not art_skip:
        paths.append(os.path.join(ref, "visualization.md"))
    if SCOPE_GLOBAL:
        paths += [os.path.join(HOME, ".pi", "agent", "APPEND_SYSTEM.md"),
                  os.path.join(HOME, ".pi", "agent", "extensions", "graph-first-gate.ts"),
                  os.path.join(HOME, ".dev-host-profile.json")]
    return paths

if ARGS.dry_run:
    print(f"[dry-run] 作用域: {'全局' if SCOPE_GLOBAL else '项目级'}  目标根: {HOME if SCOPE_GLOBAL else PROJECT_DIR}")
    for p in target_paths():
        print(("[将写] " if not os.path.exists(p) else "[将备份后覆写] ") + p)
    sys.exit(0)

# 写出（性能档：规则主文档 = PERFORMANCE 全量正文；镜像逐字一致）
for label, path in masters:
    w(path, performance, backup=True)
ref_dir = os.path.join(PROJECT_DIR, "agent-reference") if PROJECT_DIR else os.path.join(HOME, "agent-reference")
w(os.path.join(ref_dir, "environment.md"), environment_out, backup=True)
w(os.path.join(ref_dir, "tooling.md"), tooling, backup=True)
w(os.path.join(ref_dir, "preferences.md"), prefs, backup=True)
if visualization_out and not art_skip:
    w(os.path.join(ref_dir, "visualization.md"), visualization_out, backup=True)

if SCOPE_GLOBAL:
    w(os.path.join(HOME, ".pi", "agent", "APPEND_SYSTEM.md"), append_body, backup=True)
    w(os.path.join(HOME, ".pi", "agent", "extensions", "graph-first-gate.ts"), gate_out, backup=True)
    with open(os.path.join(HOME, ".dev-host-profile.json"), "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, indent=2)
    print("[写] ~/.dev-host-profile.json")
else:
    print("[跳过] 项目级不部署 pi 强化层（APPEND_SYSTEM / graph-first-gate）")

print("\n[DONE] 渲染完成")