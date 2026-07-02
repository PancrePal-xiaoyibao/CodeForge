#!/usr/bin/env bash
# gitnexus-setup.sh — Install GitNexus and configure as MCP server
# Usage: bash gitnexus-setup.sh [--system|--project]

set -euo pipefail

echo "=== GitNexus MCP Setup ==="
echo "Codebase knowledge graph for AI agents"
echo "Source: https://github.com/abhigyanpatwari/GitNexus"
echo "License: PolyForm Noncommercial 1.0.0"
echo ""

# Step 1: Install GitNexus
if command -v gitnexus &>/dev/null; then
  echo "[OK] gitnexus already installed: $(gitnexus --version 2>/dev/null || echo 'detected')"
else
  echo "[INSTALL] Installing gitnexus globally..."
  if command -v npm &>/dev/null; then
    npm install -g gitnexus
  elif command -v pnpm &>/dev/null; then
    pnpm add -g gitnexus
  else
    echo "[ERROR] No npm/pnpm found. Install Node.js first."
    exit 1
  fi
  echo "[OK] gitnexus installed"
fi

echo ""

# Step 2: Determine config level
LEVEL="${1:---project}"
case "$LEVEL" in
  --system)
    if [[ "$(uname -s)" == "MINGW"* ]] || [[ "$(uname -s)" == "MSYS"* ]]; then
      CONFIG_PATH="$USERPROFILE/.claude/settings.json"
    else
      CONFIG_PATH="$HOME/.claude/settings.json"
    fi
    echo "[CONFIG] Writing MCP config to SYSTEM level: $CONFIG_PATH"
    ;;
  --project)
    CONFIG_PATH=".claude/settings.local.json"
    echo "[CONFIG] Writing MCP config to PROJECT level: $CONFIG_PATH"
    ;;
  *)
    echo "[ERROR] Unknown level: $LEVEL"
    echo "Usage: bash gitnexus-setup.sh [--system|--project]"
    exit 1
    ;;
esac

echo ""

# Step 3: Write MCP configuration
CONFIG_DIR=$(dirname "$CONFIG_PATH")
mkdir -p "$CONFIG_DIR"

if [[ -f "$CONFIG_PATH" ]]; then
  echo "[INFO] Config file exists, merging mcpServers entry..."
  # Use python for JSON merging if available
  if command -v python3 &>/dev/null; then
    python3 -c "
import json, sys
path = '$CONFIG_PATH'
with open(path, 'r') as f:
    config = json.load(f)
config.setdefault('mcpServers', {})
config['mcpServers']['gitnexus'] = {
    'command': 'gitnexus',
    'args': ['mcp'],
    'type': 'stdio'
}
with open(path, 'w') as f:
    json.dump(config, f, indent=2)
print('[OK] Merged gitnexus into existing config')
"
  else
    echo "[WARN] No python3 for JSON merge. Manual edit needed."
    echo "  Add to $CONFIG_PATH:"
    echo '  "mcpServers": { "gitnexus": { "command": "gitnexus", "args": ["mcp"], "type": "stdio" } }'
  fi
else
  cat > "$CONFIG_PATH" << 'JSONEOF'
{
  "mcpServers": {
    "gitnexus": {
      "command": "gitnexus",
      "args": ["mcp"],
      "type": "stdio"
    }
  }
}
JSONEOF
  echo "[OK] Created $CONFIG_PATH with gitnexus MCP config"
fi

echo ""

# Step 4: Index current repo
if git rev-parse --git-dir &>/dev/null; then
  echo "[INDEX] Indexing current repository..."
  gitnexus analyze
  echo "[OK] Repository indexed successfully"
else
  echo "[SKIP] Not in a git repository. Run 'gitnexus analyze' in your project root later."
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  gitnexus analyze              # Index/re-index current repo"
echo "  gitnexus query 'auth flow'    # Search the knowledge graph"
echo "  gitnexus context --symbol X   # Get callers/callees of symbol X"
echo "  gitnexus impact --file X      # Blast radius of file X"
echo "  gitnexus serve                # Start HTTP bridge for Web UI"
echo ""
echo "MCP tools available to AI agents: list_repos, query, context, impact,"
echo "detect_changes, rename, api_impact, route_map, shape_check"
