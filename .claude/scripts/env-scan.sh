#!/usr/bin/env bash
# dev-env-scan: Cross-platform environment detection script
# Outputs JSON-structured environment info to stdout

set -euo pipefail

echo "{"

# OS Info
echo '  "os": {'
echo "    \"name\": \"$(uname -s 2>/dev/null || echo 'Unknown')\","
echo "    \"version\": \"$(uname -r 2>/dev/null || echo 'Unknown')\","
echo "    \"arch\": \"$(uname -m 2>/dev/null || echo 'Unknown')\""
echo '  },'

# Shell
echo "  \"shell\": \"$SHELL\","

# Languages
echo '  "languages": {'

# Node.js
if command -v node &>/dev/null; then
  echo "    \"nodejs\": \"$(node --version 2>/dev/null | tr -d 'v')\","
else
  echo '    "nodejs": null,'
fi

# Python
if command -v python3 &>/dev/null; then
  echo "    \"python\": \"$(python3 --version 2>/dev/null | awk '{print $2}')\","
elif command -v python &>/dev/null; then
  echo "    \"python\": \"$(python --version 2>/dev/null | awk '{print $2}')\","
else
  echo '    "python": null,'
fi

# Rust
if command -v rustc &>/dev/null; then
  echo "    \"rust\": \"$(rustc --version 2>/dev/null | awk '{print $2}')\","
else
  echo '    "rust": null,'
fi

# Go
if command -v go &>/dev/null; then
  echo "    \"go\": \"$(go version 2>/dev/null | awk '{print $3}' | tr -d 'go')\","
else
  echo '    "go": null,'
fi

# Java
if command -v java &>/dev/null; then
  echo "    \"java\": \"$(java -version 2>&1 | head -1 | awk -F'"' '{print $2}')\""
else
  echo '    "java": null'
fi

echo '  },'

# Package Managers
echo '  "package_managers": {'
echo -n '    "npm": '
command -v npm &>/dev/null && echo "\"$(npm --version 2>/dev/null)\"," || echo 'null,'
echo -n '    "pnpm": '
command -v pnpm &>/dev/null && echo "\"$(pnpm --version 2>/dev/null)\"," || echo 'null,'
echo -n '    "yarn": '
command -v yarn &>/dev/null && echo "\"$(yarn --version 2>/dev/null)\"," || echo 'null,'
echo -n '    "uv": '
command -v uv &>/dev/null && echo "\"$(uv --version 2>/dev/null | awk '{print $2}')\"," || echo 'null,'
echo -n '    "conda": '
command -v conda &>/dev/null && echo "\"$(conda --version 2>/dev/null | awk '{print $2}')\"," || echo 'null,'
echo -n '    "cargo": '
command -v cargo &>/dev/null && echo "\"$(cargo --version 2>/dev/null | awk '{print $2}')\"" || echo 'null'
echo '  },'

# GPU
echo '  "gpu": {'
if command -v nvidia-smi &>/dev/null; then
  GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
  GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
  DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)
  echo "    \"vendor\": \"nvidia\","
  echo "    \"model\": \"$GPU_NAME\","
  echo "    \"vram_mb\": $GPU_MEM,"
  echo "    \"driver\": \"$DRIVER\""
elif command -v rocm-smi &>/dev/null; then
  echo '    "vendor": "amd",'
  echo '    "model": "detected"'
else
  echo '    "vendor": null'
fi
echo '  },'

# Docker
echo -n '  "docker": '
command -v docker &>/dev/null && echo 'true,' || echo 'false,'

# Memory (in GB)
if [[ "$(uname -s)" == "Darwin" ]]; then
  MEM_GB=$(($(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1073741824))
else
  MEM_GB=$(($(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo 0) / 1048576))
fi
echo "  \"memory_gb\": $MEM_GB,"

# Git
echo -n '  "git": '
command -v git &>/dev/null && echo "\"$(git --version 2>/dev/null | awk '{print $3}')\"" || echo 'null'

echo "}"
