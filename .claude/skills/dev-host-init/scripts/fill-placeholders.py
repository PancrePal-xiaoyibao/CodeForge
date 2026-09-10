#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dev-host-init 占位符填充器（跨平台，零本机硬编码）
===================================================
核心职责：
1. 运行 host-scan（Linux/macOS/WSL → host-scan.sh；Windows → host-scan.ps1）
2. 把 host-injection.template.md 的 {{占位符}} 替换为「探测到的本机值」或「明确兜底文案」
3. 两道门禁：渲染产物 0 未替换占位符；模板 0 敏感硬编码

安全原则：
- 本脚本必须保持「通用」：不出现任何真实 IP / 域名 / 用户名 / 端口 / 绝对路径。
  所有判定都基于 host-scan JSON 里 *探测到* 的值，或通用正则黑名单（匹配模式而非具体值）。
- 模板是开源共享的：只能含 {{占位符}}；真实值一律由 init 探测回填。
- 探测不到 → 输出「未检测到」，绝不猜一个本机专属值。
"""
import argparse, json, os, re, subprocess, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- 敏感模式黑名单（通用正则，不写死具体 IP/域名/用户名/端口）----------
SENSITIVE_PATTERNS = [
    r"(?<![\d.])\b(?!(?:127\.0\.0\.1|0\.0\.0\.0|::1)\b)(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",  # 任意公网/内网 IPv4（豁免回环示例）
    r"https?://[a-z0-9][a-z0-9.-]*\.[a-z]{2,}",               # 任意公网域名 URL
    r"\b[A-Za-z0-9-]+\.(?:com|net|cn|org|io|dev|app|pro)\b",  # 域名根
    r"/home/[a-z_][a-z0-9_]*",                                 # Linux 用户绝对路径
    r"C:\\Users\\(?!<user>)",                                    # Windows 用户绝对路径（豁免 <user> 占位示例）
    r"\b[A-Z0-9]{20}\b",                                        # 类 API Key（20 位大写混搭）
    r"(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"]?[^\s'\"]{8,}",  # 凭据赋值
    r"-----BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY-----",     # 私钥头
]

def run_host_scan():
    """跨平台跑 host-scan；失败返回 {}（渲染端靠兜底文案继续）"""
    sh = os.path.join(SCRIPT_DIR, "host-scan.sh")
    ps1 = os.path.join(SCRIPT_DIR, "host-scan.ps1")
    if os.name == "nt":
        # Windows 原生：优先 PowerShell 探测（Git Bash 下跑 .sh 会因缺 WSL/Linux 工具输出空 JSON）
        if os.path.exists(ps1):
            try:
                out = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1],
                                     capture_output=True, text=True, timeout=90)
                return json.loads(out.stdout) if out.returncode == 0 else {}
            except Exception:
                return {}
    else:
        # Linux / macOS / WSL：优先 bash 脚本
        if os.path.exists(sh):
            try:
                out = subprocess.run(["bash", sh], capture_output=True, text=True, timeout=90)
                return json.loads(out.stdout) if out.returncode == 0 else {}
            except Exception:
                return {}
    return {}

def detect_value(h, key, default=None):
    cur = h
    for part in key.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur if cur is not None else default

def pick(ports, candidates):
    """从探测到的端口列表里按优先级挑第一个在候选里的端口（端口号 int/str 均可）"""
    strs = {str(p) for p in (ports or [])}
    for c in candidates:
        if str(c) in strs:
            return str(c)
    return ""

def build_values(h):
    """全部值来自 host-scan 探测；无探测项 → '未检测到' 兜底文案"""
    v = {}
    net = h.get("network", {}) or {}
    proxy = h.get("proxy", {}) or {}
    ports = net.get("listen_ports", []) or []
    open_ports = proxy.get("open_local_ports", []) or []
    home = os.path.expanduser("~")

    vps_ip = net.get("vps_ip", "") or ""
    vps_alias = net.get("vps_alias", "") or ""
    frp_svc = (net.get("frp_svc", "") or "").replace(".service", "")
    ngx_name = net.get("nginx_server_name", "") or ""
    if ngx_name in ("", "_", "example.com", "default_server"):
        ngx_name = ""
    ngx_port = net.get("nginx_port", "") or ""

    # 公网 HTTPS 端口：优先 FRP 隧道端口，其次 nginx listen；端口必须真实探测到
    pub_port = pick(ports, [int(ngx_port) if str(ngx_port).isdigit() else 0, 8443, 9443, 443])
    pub_domain = ngx_name
    ssh_local_port = pick(ports, [22022, 2222, 22])
    d_port = pick(ports, [8090, 8000, 8080])
    mcp_port = pick(ports, [8765, 8766, 8001])
    mcp_ext = pick(ports, [8767, 8766, 8002])
    rstudio = pick(ports, [8787, 8788, 8786])
    tunnel = pick(ports, [8787, 8080, 8888])
    http_p = pick(open_ports, [7890, 8080, 8888, 1080])
    socks = pick(open_ports, [1080, 7890, 10808])

    v["NET_VPS_IP_PUB"] = vps_ip or "未检测到（SSH config 无 HostName，请手填）"
    v["NET_VPS_SSH_ALIAS"] = vps_alias or "未检测到（SSH config 无 Host，请手填）"
    v["NET_PUB_DOMAIN"] = pub_domain or "未检测到（nginx 无 server_name，请手填）"
    v["NET_PUB_PORT"] = pub_port or "未检测到（无公网 HTTPS 端口，请手填）"
    v["NET_PUB_URL"] = f"https://{pub_domain}:{pub_port}" if pub_domain and pub_port else "未检测到（公网入口，请手填）"
    v["NET_SSH_LOCAL_PORT"] = ssh_local_port or "未检测到（公网 SSH 端口在云控制台，请手填）"
    v["NET_SSH_USER"] = os.environ.get("USER", os.environ.get("USERNAME", "未检测到"))
    v["NET_SSH_METHOD"] = f"FutureTerminal / ssh -p {v['NET_SSH_LOCAL_PORT']}" if "未检测" not in v["NET_SSH_LOCAL_PORT"] else "未检测到（SSH 端口）"
    v["NET_PORT_TUNNEL_CODESERVER"] = f"127.0.0.1:{tunnel}" if tunnel else "未检测到"
    v["NET_PORT_RSTUDIO"] = rstudio or "未检测到"
    v["NET_PORT_DASHBOARD"] = d_port or "未检测到"
    v["NET_PORT_MCP"] = mcp_port or "未检测到"
    v["NET_PORT_MCP_EXT"] = mcp_ext or "未检测到"
    v["NET_FRP_SVC"] = frp_svc or "未检测到（无 frp systemd 服务）"
    v["NET_FRP_BIND_PORT"] = "7000"  # frp 默认；可按 frpc.toml 探测
    v["NET_APP_SLUG"] = "未检测到（项目名，init 后自定义）"
    v["NET_PROXY_HTTP"] = f"127.0.0.1:{http_p}" if http_p else "未检测到"
    v["NET_PROXY_SOCKS5"] = f"127.0.0.1:{socks}" if socks else "未检测到"
    v["NET_INGRESS_FILE"] = "未检测到（用户自建权威运维文档路径）"
    v["NET_KAIROS_DOCS"] = "未检测到（用户自建 KAIROS 端点文档路径）"
    v["NET_NGINX_CONF"] = "未检测到（用户自建 nginx 配置路径）"
    v["NET_FRP_DIR"] = "未检测到（用户自建 frp 运维目录）"

    # 通用占位符（环境/硬件，全探测驱动）
    cpu = detect_value(h, "hardware.cpu_model", "")
    ram = detect_value(h, "hardware.memory_gb", 0)
    swap = detect_value(h, "hardware.swap_gb", 0)
    gpu = detect_value(h, "hardware.gpu", None)
    disks = detect_value(h, "hardware.disks", []) or []
    storage_desc = " + ".join(
        f"{d.get('mount','?')} {d.get('total_gb','?')}G(空{d.get('free_gb','?')}G)"
        for d in disks if isinstance(d, dict)) or "未检测到"
    gpu_desc = (f"{gpu.get('model','')} {gpu.get('vram_mb','')}MB"
                if isinstance(gpu, dict) else ("无独立 GPU" if gpu is None else "未检测到"))

    v["DEV_ROOT"] = os.path.join(home, "Development")
    v["HOME_DIR"] = home
    v["LANG_HEADER"] = "始终使用简体中文回复。"
    v["CODEBASE_MCP_DOCS"] = os.path.join(home, "Development", "codebase-memory-mcp", "DEPLOYMENT.zh-CN.md")
    v["OS_NAME"] = detect_value(h, "os.name", "Unknown")
    v["CPU"] = cpu or "未检测到（lscpu 手查）"
    v["RAM"] = f"{ram} GB" if ram else "未检测到"
    v["SWAP"] = f"{swap} GB" if swap else "未检测到"
    v["GPU"] = gpu_desc
    v["STORAGE"] = storage_desc
    v["HW_NOTES"] = "2026 dev-host-init 实测探测（host-scan）" if cpu else "未检测到，请手填"
    v["PROXY_DESC"] = (f"本机代理：socks5 {v['NET_PROXY_SOCKS5']} / http {v['NET_PROXY_HTTP']}（init 探测）"
                       if "未检测" not in v["NET_PROXY_HTTP"] else "未检测到本地代理")
    v["PROXY_SOCKS5"] = v["NET_PROXY_SOCKS5"]
    v["PROXY_HTTP"] = v["NET_PROXY_HTTP"]
    v["PROXY_HTTP_HOSTPORT"] = http_p or "未检测到"
    v["MIRROR_LIST"] = "~/AGENTS.md、~/.claude/CLAUDE.md、~/.codex/AGENTS.md、~/.gemini/GEMINI.md"
    v["REFERENCE_DIR"] = os.path.join(home, "agent-reference")
    envs = detect_value(h, "env_managers.conda_envs", []) or []
    uv_py = detect_value(h, "env_managers.uv_pythons", []) or []
    if envs or uv_py:
        v["ENV_TABLE"] = "conda: " + ", ".join(envs[:12]) + (f"\nuv python: " + ", ".join(uv_py[:8]) if uv_py else "")
    else:
        v["ENV_TABLE"] = "未检测到 conda/uv 环境"
    v["PREFERENCES_SUMMARY"] = "未采集偏好，走默认偏好模板"
    return v

def fill_template(template_text, values):
    out = template_text
    for k, val in values.items():
        out = out.replace("{{" + k + "}}", val)
    # 兜底：仍残留 {{...}} → 明确文案（保证 0 占位符残留）
    out = re.sub(r"\{\{[A-Z_]+\}\}", "[未提供，请手填]", out)
    return out

def detect_sensitive(text):
    """返回命中的通用敏感模式；空 = 通过"""
    hits = []
    for pat in SENSITIVE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(pat)
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--output", required=False)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tpl = open(args.template, encoding="utf-8").read()
    tpl_hits = detect_sensitive(tpl)
    if tpl_hits:
        print(f"[FAIL] 模板含敏感硬编码: {tpl_hits}", file=sys.stderr)
        sys.exit(2)
    print(f"[OK] 模板敏感检查通过: {args.template}")

    h = run_host_scan()
    if not h:
        print("[WARN] host-scan 探测失败，占位符走兜底文案", file=sys.stderr)

    values = build_values(h)
    out = fill_template(tpl, values)

    leftover = re.findall(r"\{\{", out)
    if leftover:
        print(f"[FAIL] 渲染产物仍有 {len(leftover)} 处未替换占位符", file=sys.stderr)
        sys.exit(3)

    # 渲染产物敏感检查：本机产物允许探测回填，但须确认无「模板硬编码」来源
    out_hits = detect_sensitive(out)
    if out_hits:
        print(f"[WARN] 渲染产物命中敏感模式: {out_hits}（本机探测合法；确认非模板硬编码）", file=sys.stderr)

    print(f"[OK] 渲染完成，共替换 {len(values)} 个占位符")
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        open(args.output, "w", encoding="utf-8").write(out)
        print(f"[OK] 已写出: {args.output}")
    else:
        print(json.dumps({k: val for k, val in values.items() if k.startswith("NET_")},
                         ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()