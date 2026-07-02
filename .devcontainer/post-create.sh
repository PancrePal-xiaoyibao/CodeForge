#!/usr/bin/env bash
# ============================================================================
# CodeForge Codespace / DevContainer 首次启动脚本
# 由 devcontainer.json 的 postCreateCommand 触发
# ============================================================================
set -e

echo ""
echo "🔨 ============================================================"
echo "   CodeForge Codespace Bootstrap"
echo "============================================================"
echo ""

echo "[1/4] 更新 npm..."
sudo npm install -g npm@latest || npm install -g npm@latest

echo ""
echo "[2/4] 安装 AI Coding 三剑客 (Claude Code + Codex + Gemini CLI)..."
# Claude Code — Anthropic 官方
npm install -g @anthropic-ai/claude-code || echo "  ⚠️ Claude Code 安装失败，稍后手动 npm i -g @anthropic-ai/claude-code"

# OpenAI Codex CLI
npm install -g @openai/codex || echo "  ⚠️ Codex 安装失败，稍后手动 npm i -g @openai/codex"

# Google Gemini CLI
npm install -g @google/gemini-cli || echo "  ⚠️ Gemini CLI 安装失败，稍后手动 npm i -g @google/gemini-cli"

echo ""
echo "[3/4] 部署 CodeForge skill 到用户目录..."
if [ -f "./deploy/deploy.sh" ]; then
  chmod +x ./deploy/deploy.sh
  ./deploy/deploy.sh --yes || echo "  ⚠️ 部署脚本运行失败，稍后手动 ./deploy/deploy.sh --yes"
else
  echo "  ⚠️ 未找到 deploy/deploy.sh"
fi

echo ""
echo "[4/4] 环境自检..."
echo "  Node       : $(node --version 2>/dev/null || echo 'not found')"
echo "  npm        : $(npm --version 2>/dev/null || echo 'not found')"
echo "  claude     : $(claude --version 2>/dev/null || echo 'not found (登录后可用)')"
echo "  codex      : $(codex --version 2>/dev/null || echo 'not found (登录后可用)')"
echo "  gemini     : $(gemini --version 2>/dev/null || echo 'not found (登录后可用)')"
echo "  gh         : $(gh --version 2>/dev/null | head -1 || echo 'not found')"

echo ""
echo "✅ CodeForge Codespace 初始化完成！"
echo ""
echo "下一步："
echo "  1. 登录你选择的 AI CLI（第一次运行会提示登录）"
echo "     - claude          → 用 Anthropic 账号 / API Key 登录"
echo "     - codex           → 用 OpenAI 账号 / API Key 登录"
echo "     - gemini          → 用 Google 账号登录"
echo "  2. 输入 /ai-spec  开始描述你的需求"
echo "  3. 或 /deep-research  做技术选型 / 文献调研"
echo "  4. 想接社区 Issue 干活？看 CONTRIBUTING.md"
echo ""
