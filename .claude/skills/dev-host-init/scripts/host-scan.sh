#!/usr/bin/env bash
# dev-host-init: cross-platform host environment detection (Linux / macOS / WSL / Git Bash)
# Outputs a single JSON object to stdout. Every probe silently degrades to null/false/[].
# Companion of host-scan.ps1 (Windows native). Consumed by dev-host-init Phase 2/5 rendering.

set -euo pipefail

OS_NAME="$(uname -s 2>/dev/null || echo Unknown)"
IS_MAC=0; [[ "$OS_NAME" == "Darwin" ]] && IS_MAC=1

json_str() { printf '"%s"' "${1:-}"; }
json_opt_str() { if [[ -n "${1:-}" ]]; then printf '"%s"' "$1"; else echo 'null'; fi; }

# ---------- OS & shell ----------
echo '{'
echo "  \"os\": {"
echo -n '    "name": '; json_str "$OS_NAME"; echo ","
echo -n '    "version": '; json_str "$(uname -r 2>/dev/null || echo Unknown)"; echo ","
echo -n '    "arch": '; json_str "$(uname -m 2>/dev/null || echo Unknown)"
echo '  },'
echo -n '  "shell": '; json_opt_str "${SHELL:-}"; echo ','

# ---------- hardware ----------
echo '  "hardware": {'
if [[ $IS_MAC -eq 1 ]]; then
  CPU_MODEL="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || true)"
  [[ -z "$CPU_MODEL" ]] && CPU_MODEL="$(sysctl -n hw.model 2>/dev/null || true)"
  CPU_CORES="$(sysctl -n hw.ncpu 2>/dev/null || echo 0)"
  MEM_GB=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1073741824 ))
  SWAP_GB=0
else
  CPU_MODEL="$(lscpu 2>/dev/null | awk -F': +' '/^Model name|^型号名称/{print $2; exit}' || true)"
  [[ -z "$CPU_MODEL" ]] && CPU_MODEL="$(awk -F': ' '/^model name/{print $2; exit}' /proc/cpuinfo 2>/dev/null || true)"
  CPU_CORES="$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 0)"
  MEM_GB=$(( $(awk '/^MemTotal/{print $2}' /proc/meminfo 2>/dev/null || echo 0) / 1048576 ))
  SWAP_GB=$(( $(awk '/^SwapTotal/{print $2}' /proc/meminfo 2>/dev/null || echo 0) / 1048576 ))
fi
echo -n '    "cpu_model": '; json_opt_str "$CPU_MODEL"; echo ','
echo "    \"cpu_cores\": ${CPU_CORES:-0},"
echo "    \"memory_gb\": ${MEM_GB:-0},"
echo "    \"swap_gb\": ${SWAP_GB:-0},"

# AVX2 note (x86 Linux only; macOS/ARM => null)
AVX2="$(grep -m1 -o 'avx2' /proc/cpuinfo 2>/dev/null || true)"
if [[ -n "$AVX2" ]]; then AVX2_JSON=true; else AVX2_JSON=false; fi
echo "    \"avx2\": ${AVX2_JSON},"

# GPU
echo '    "gpu": {'
if command -v nvidia-smi &>/dev/null; then
  echo '      "vendor": "nvidia",'
  echo -n '      "model": '; json_opt_str "$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)"; echo ','
  echo "      \"vram_mb\": $(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 || echo 0),"
  echo -n '      "driver": '; json_opt_str "$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)"
elif command -v rocm-smi &>/dev/null; then
  echo '      "vendor": "amd",'
  echo '      "model": "detected", "vram_mb": null, "driver": null'
elif [[ $IS_MAC -eq 1 && "$CPU_MODEL" == Apple* ]]; then
  echo '      "vendor": "apple",'
  echo -n '      "model": '; json_opt_str "$CPU_MODEL"; echo ','
  echo '      "vram_mb": null, "driver": null'
else
  echo '      "vendor": null, "model": null, "vram_mb": null, "driver": null'
fi
echo '    },'

# disks: mount,total_gb,free_gb — real filesystems only, max 5
echo '    "disks": ['
DF_OUT="$(df -l -k 2>/dev/null | awk 'NR>1 && $1 !~ /^(tmpfs|devfs|devtmpfs|map|overlay|squashfs|proc|sysfs|cgroup|udev)/ && $6 !~ /^\/(dev|proc|sys|run)(\/|$)/ {print $6" "$2" "$4}' | head -5 || true)"
FIRST=1
while read -r mnt total avail; do
  [[ -z "${mnt:-}" ]] && continue
  [[ $FIRST -eq 1 ]] || echo ','
  FIRST=0
  echo "      {\"mount\": $(json_str "$mnt"), \"total_gb\": $((total/1048576)), \"free_gb\": $((avail/1048576))}"
done <<< "$DF_OUT"
echo ''
echo '    ]'
echo '  },'

# ---------- languages ----------
echo '  "languages": {'
echo -n '    "nodejs": '; command -v node &>/dev/null && json_str "$(node --version 2>/dev/null | tr -d v)" || echo 'null'; echo ','
if command -v python3 &>/dev/null; then echo -n '    "python": '; json_str "$(python3 --version 2>/dev/null | awk '{print $2}')"
elif command -v python &>/dev/null; then echo -n '    "python": '; json_str "$(python --version 2>/dev/null | awk '{print $2}')"
else echo -n '    "python": null'; fi; echo ','
echo -n '    "rust": '; command -v rustc &>/dev/null && json_str "$(rustc --version 2>/dev/null | awk '{print $2}')" || echo 'null'; echo ','
echo -n '    "go": '; command -v go &>/dev/null && json_str "$(go version 2>/dev/null | awk '{print $3}' | tr -d go)" || echo 'null'; echo ','
echo -n '    "java": '; command -v java &>/dev/null && json_str "$(java -version 2>&1 | head -1 | awk -F'"' '{print $2}')" || echo 'null'; echo ','
echo -n '    "dotnet": '; command -v dotnet &>/dev/null && json_str "$(dotnet --version 2>/dev/null)" || echo 'null'; echo ','
echo -n '    "r": '; command -v R &>/dev/null && json_str "$(R --version 2>/dev/null | head -1 | awk '{print $3}')" || echo 'null'
echo '  },'

# ---------- package managers ----------
echo '  "package_managers": {'
for pm in npm pnpm yarn bun uv conda cargo pip; do
  case $pm in
    pip) VER="$(pip --version 2>/dev/null | awk '{print $2}' || true)" ;;
    *)   VER="$($pm --version 2>/dev/null | awk '{print $NF}' | head -1 || true)" ;;
  esac
  # keep only plausible version tokens (digits or x.y.z-ish)
  if [[ -n "$VER" && "$VER" =~ [0-9] ]]; then echo "    \"$pm\": $(json_str "$VER"),"
  else echo "    \"$pm\": null,"; fi
done
# brew (macOS/linuxbrew)
echo -n '    "brew": '; command -v brew &>/dev/null && json_str "$(brew --version 2>/dev/null | head -1 | awk '{print $2}')" || echo 'null'
echo '  },'

# ---------- env managers ----------
echo '  "env_managers": {'
echo -n '    "conda_envs": ['
if command -v conda &>/dev/null; then
  FIRST=1
  while read -r e; do
    [[ -z "$e" ]] && continue
    [[ $FIRST -eq 1 ]] || printf ', '
    FIRST=0; printf '"%s"' "$e"
  done < <(conda env list 2>/dev/null | grep -v '^#' | awk 'NF{print $1}' || true)
fi
echo '],'
echo -n '    "uv_pythons": ['
if command -v uv &>/dev/null; then
  FIRST=1
  while read -r e; do
    [[ -z "$e" ]] && continue
    [[ $FIRST -eq 1 ]] || printf ', '
    FIRST=0; printf '"%s"' "$e"
  done < <(uv python list 2>/dev/null | awk 'NF && $1!~"^-"{print $1}' | head -10 || true)
fi
echo ']'
echo '  },'

# ---------- proxy ----------
echo '  "proxy": {'
echo -n '    "env_http": ';  json_opt_str "${http_proxy:-${HTTP_PROXY:-}}";  echo ','
echo -n '    "env_https": '; json_opt_str "${https_proxy:-${HTTPS_PROXY:-}}"; echo ','
echo -n '    "open_local_ports": ['
FIRST=1
for port in 1080 7890 7897 8118 10808 8888; do
  if timeout 1 bash -c "echo > /dev/tcp/127.0.0.1/$port" 2>/dev/null; then
    [[ $FIRST -eq 1 ]] || printf ', '
    FIRST=0; printf '"%s"' "$port"
  fi
done
echo ']'
echo '  },'
  # ---------- network topology (init 时探测) ----------
  echo '  "network": {'
  # SSH alias -> VPS IP (解析 ~/.ssh/config)
  vps_ip=""; vps_alias=""
  if [ -f "$HOME/.ssh/config" ]; then
    vps_alias=$(awk '/^Host /{a=$2} a!="" && /HostName /{print a; exit}' "$HOME/.ssh/config" 2>/dev/null)
    vps_ip=$(awk '/^Host /{a=$2} a!="" && /HostName /{print $2; exit}' "$HOME/.ssh/config" 2>/dev/null)
  fi
  echo -n '    "vps_alias": '; json_opt_str "${vps_alias}"; echo ','
  echo -n '    "vps_ip": '; json_opt_str "${vps_ip}"; echo ','
  # FRP systemd service
  frp_svc=$(systemctl list-units --type=service --all 2>/dev/null | awk '/frpc|frp/{print $1; exit}' | head -1 || true)
  echo -n '    "frp_svc": '; json_opt_str "${frp_svc}"; echo ','
  # nginx server_name / port (本机已装时)
  ngx_name=""; ngx_port=""
  if [ -d /etc/nginx ]; then
    ngx_name=$(grep -rhoE 'server_name[[:space:]]+[^;]+' /etc/nginx/sites-available /etc/nginx/conf.d 2>/dev/null \
      | awk '$2 != "_" && $2 != "example.com" && $2 != "default_server" {print $2; exit}')
    ngx_port=$(grep -rhoE 'listen[[:space:]]+[0-9]+' /etc/nginx/sites-available /etc/nginx/conf.d 2>/dev/null | awk '{print $2; exit}')
  fi
  echo -n '    "nginx_server_name": '; json_opt_str "${ngx_name}"; echo ','
  echo -n '    "nginx_port": '; json_opt_str "${ngx_port}"; echo ','
  # 端口扫描 (回环 listen, 含本机服务端口)
  scan_ports="22 80 443 1080 7890 8787 8765 8767 8090 8000 8080 8443 22022 2222"
  echo -n '    "listen_ports": ['
  FIRST=1
  for port in $scan_ports; do
    if timeout 1 bash -c "echo > /dev/tcp/127.0.0.1/$port" 2>/dev/null; then
      if [ $FIRST -eq 1 ]; then FIRST=0; else printf ','; fi
      printf '"%s"' "$port"
    fi
  done
  echo ' ]'
  echo '  },'

# ---------- codebase-memory-mcp ----------
echo '  "codebase_mcp": {'
if command -v codebase-memory-mcp &>/dev/null; then CB_CLI=true; else CB_CLI=false; fi
echo "    \"cli_available\": ${CB_CLI},"
CB_CFG=0
for f in "$HOME/.claude.json" "$HOME/.claude/settings.json" "$HOME/.codex/config.toml" "$HOME/.gemini/settings.json"; do
  if [[ -f "$f" ]] && grep -q 'codebase-memory' "$f" 2>/dev/null; then CB_CFG=1; break; fi
done
[[ $CB_CLI == true ]] && CB_CFG=1
if [[ $CB_CFG -eq 1 ]]; then echo '    "mcp_configured": true'; else echo '    "mcp_configured": false'; fi
echo '  },'

# ---------- tools ----------
echo '  "tools": {'
echo -n '    "git": '; command -v git &>/dev/null && json_str "$(git --version 2>/dev/null | awk '{print $3}')" || echo 'null'; echo ','
echo -n '    "gh": '; command -v gh &>/dev/null && echo true || echo false; echo ','
echo -n '    "rg": '; command -v rg &>/dev/null && echo true || echo false; echo ','
echo -n '    "docker": '; command -v docker &>/dev/null && echo true || echo false
echo '  }'
echo '}'
