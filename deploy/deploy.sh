#!/usr/bin/env bash
# ============================================================================
# CodeForge 一键部署脚本 (macOS / Linux)
# 用法: 在仓库根目录运行  ./deploy/deploy.sh
# 行为: 合并部署 .claude/.codex/.gemini 到 $HOME，并写入 .agents/skills，
#       重名文件自动备份为 *.codeforge-bak.<TIMESTAMP>
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOME_DIR="$HOME"
TIMESTAMP="$(date +%Y%m%d%H%M%S)"
YES=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        -y|--yes)
            YES=1
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--yes|-y]"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: $0 [--yes|-y]" >&2
            exit 2
            ;;
    esac
done

echo ""
echo "  ===================================================="
echo "    CodeForge - 一键部署 (macOS/Linux Bash)"
echo "  ===================================================="
echo "  Source:  $REPO_ROOT"
echo "  Target:  $HOME_DIR"
echo ""

if [[ "$YES" -eq 0 ]]; then
    read -r -p "  将合并部署 .claude/.codex/.gemini/.agents，重名文件自动备份。继续？(y/N) " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "  已取消。"
        exit 0
    fi
else
    echo "  非交互模式：已跳过确认。"
fi

merge_codeforge_dir() {
    local subpath="$1"
    local target_subpath="${2:-$subpath}"
    local src="$REPO_ROOT/$subpath"
    local dst="$HOME_DIR/$target_subpath"
    if [[ ! -d "$src" ]]; then
        echo "  [SKIP] 源不存在: $subpath"
        return
    fi
    mkdir -p "$dst"
    local bak_count=0
    for item in "$src"/*; do
        [[ -e "$item" ]] || continue
        local name="$(basename "$item")"
        local target="$dst/$name"
        if [[ -e "$target" ]]; then
            local bak="$target.codeforge-bak.$TIMESTAMP"
            mv "$target" "$bak"
            echo "    [BACKUP] $name -> $(basename "$bak")"
            bak_count=$((bak_count + 1))
        fi
        cp -r "$item" "$target"
    done
    echo "  [OK] $subpath -> $target_subpath  (备份 $bak_count 项)"
}

echo ""
echo "  正在部署..."
merge_codeforge_dir ".claude/skills"
merge_codeforge_dir ".claude/commands"
merge_codeforge_dir ".claude/agents"
merge_codeforge_dir ".claude/scripts"
merge_codeforge_dir ".codex/skills"
merge_codeforge_dir ".codex/skills" ".agents/skills"
merge_codeforge_dir ".gemini/skills"

echo ""
echo "  ===================================================="
echo "    ✅ CodeForge 部署完成！"
echo "  ===================================================="
echo ""
echo "  下一步："
echo "    1. 启动 Claude Code / Codex CLI / Gemini CLI"
echo "    2. 输入 /ai-spec  开始描述你的需求（默认主调度）"
echo "    3. 或 /deep-research  做技术选型 / 领域调研"
echo "    4. 或 /dev-env-scan  为新项目做环境画像"
echo ""
echo "  MCP 配置（可选，提升调研能力）："
echo "    参考 deploy/mcp-config.template.json"
echo ""
