#!/usr/bin/env bash
# ocr-setup.sh — Install and configure Open Code Review (OCR) CLI
# Usage: bash ocr-setup.sh [--anthropic|--openai]

set -euo pipefail

echo "=== Open Code Review (OCR) Setup ==="
echo ""

# Step 1: Install OCR
if command -v ocr &>/dev/null; then
  echo "[OK] ocr already installed: $(ocr --version 2>/dev/null || echo 'version unknown')"
else
  echo "[INSTALL] Installing @alibaba-group/open-code-review..."
  if command -v npm &>/dev/null; then
    npm install -g @alibaba-group/open-code-review
  elif command -v pnpm &>/dev/null; then
    pnpm add -g @alibaba-group/open-code-review
  else
    echo "[ERROR] No npm/pnpm found. Install Node.js first."
    exit 1
  fi
  echo "[OK] ocr installed successfully"
fi

echo ""

# Step 2: Configure LLM
PROVIDER="${1:---anthropic}"

case "$PROVIDER" in
  --anthropic)
    echo "[CONFIG] Setting up Anthropic (Claude) as LLM backend..."
    echo ""
    echo "Please provide your Anthropic API key:"
    read -r -s API_KEY
    echo ""

    ocr config set llm.url "https://api.anthropic.com/v1/messages"
    ocr config set llm.auth_token "$API_KEY"
    ocr config set llm.model "claude-sonnet-4-20250514"
    ocr config set llm.use_anthropic true
    echo "[OK] Anthropic configured"
    ;;
  --openai)
    echo "[CONFIG] Setting up OpenAI as LLM backend..."
    echo ""
    echo "Please provide your OpenAI API key:"
    read -r -s API_KEY
    echo ""

    ocr config set llm.url "https://api.openai.com/v1/chat/completions"
    ocr config set llm.auth_token "$API_KEY"
    ocr config set llm.model "gpt-4o"
    ocr config set llm.use_anthropic false
    echo "[OK] OpenAI configured"
    ;;
  *)
    echo "[ERROR] Unknown provider: $PROVIDER"
    echo "Usage: bash ocr-setup.sh [--anthropic|--openai]"
    exit 1
    ;;
esac

echo ""

# Step 3: Test connectivity
echo "[TEST] Testing LLM connectivity..."
if ocr llm test 2>/dev/null; then
  echo "[OK] LLM connection successful!"
else
  echo "[WARN] LLM test failed. Check your API key and network."
  echo "  You can test manually with: ocr llm test"
fi

echo ""

# Step 4: Configure review language
echo "[CONFIG] Setting review comment language to English..."
ocr config set language "English"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  ocr review                    # Review working copy changes"
echo "  ocr review --from main        # Review current branch vs main"
echo "  ocr review --commit HEAD      # Review last commit"
echo "  ocr review --preview          # Dry-run: see what would be reviewed"
echo ""
echo "Custom rules: create .opencodereview/rule.json (see templates/rule.json.example)"
