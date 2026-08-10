#!/usr/bin/env bash
# ai4s-gate-check.sh — AI4S Dry Lab Gate 门控检查
# 用法: bash .claude/skills/ai4s-dry-lab/scripts/ai4s-gate-check.sh [phase_number|all|final]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

PHASE="${1:-all}"
PASS=0
FAIL=0
WARN=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

gate_pass() { PASS=$((PASS + 1)); printf "  \033[0;32m✓ PASS\033[0m %s\n" "$1"; }
gate_fail() { FAIL=$((FAIL + 1)); printf "  \033[0;31m✗ FAIL\033[0m %s\n" "$1"; }
gate_warn() { WARN=$((WARN + 1)); printf "  \033[0;33m⚠ WARN\033[0m %s\n" "$1"; }

echo "============================================================"
echo "AI4S Gate Check — Phase: $PHASE"
echo "============================================================"

# ── Universal Gates ──
echo ""
echo "[Universal] 基础文档检查"

[ -f "$PROJECT_ROOT/docs/SPEC-experiment.md" ] && gate_pass "SPEC-experiment.md 存在" || gate_fail "SPEC-experiment.md 缺失"
[ -f "$PROJECT_ROOT/docs/WORKLOG.md" ] && gate_pass "WORKLOG.md 存在" || gate_warn "WORKLOG.md 缺失"
[ -f "$PROJECT_ROOT/data/raw/DATA_MANIFEST.md" ] && gate_pass "DATA_MANIFEST.md 存在" || gate_warn "DATA_MANIFEST.md 缺失"
[ -f "$PROJECT_ROOT/CLAUDE.md" ] && gate_pass "CLAUDE.md 存在" || gate_warn "CLAUDE.md 缺失"

# ── Phase-specific Gates ──
check_phase() {
    local ph="$1"
    echo ""
    echo "[Phase $ph] 专项检查"

    case "$ph" in
        01)
            local manifest="$PROJECT_ROOT/data/raw/DATA_MANIFEST.md"
            if [ -f "$manifest" ]; then
                grep -q '✅' "$manifest" && gate_pass "DATA_MANIFEST 包含已验证数据" || gate_warn "DATA_MANIFEST 无已验证标记"
            fi
            ;;
        02)
            local h5ad_files=$(find "$PROJECT_ROOT/data/processed/scrna" -name '*.h5ad' 2>/dev/null | wc -l)
            [ "$h5ad_files" -gt 0 ] && gate_pass "scRNA-seq 处理数据: $h5ad_files H5AD 文件" || gate_fail "scRNA-seq 无处理数据输出"

            local scripts=$(find "$PROJECT_ROOT/scripts/02_scrna_analysis" -name '*.py' 2>/dev/null | wc -l)
            [ "$scripts" -gt 0 ] && gate_pass "Phase 2 脚本: $scripts 个" || gate_warn "Phase 2 无分析脚本"
            ;;
        03)
            local spatial_files=$(find "$PROJECT_ROOT/data/processed/spatial" -name '*.h5ad' 2>/dev/null | wc -l)
            [ "$spatial_files" -gt 0 ] && gate_pass "空间数据: $spatial_files H5AD 文件" || gate_fail "空间分析无处理数据输出"

            local coloc_csv=$(find "$PROJECT_ROOT/results/tables" -name '*colocalization*' 2>/dev/null | wc -l)
            [ "$coloc_csv" -gt 0 ] && gate_pass "共定位分析: $coloc_csv CSV 文件" || gate_warn "共定位分析未输出"
            ;;
        04)
            local cross_csv=$(find "$PROJECT_ROOT/results/tables" -name '*cross*' -o -name '*comparison*' -o -name '*conservation*' 2>/dev/null | wc -l)
            [ "$cross_csv" -gt 0 ] && gate_pass "跨物种比较: $cross_csv CSV 文件" || gate_warn "跨物种比较未输出"
            ;;
        05)
            local fig_count=$(find "$PROJECT_ROOT/results/figures" -name 'Fig*.png' 2>/dev/null | wc -l)
            [ "$fig_count" -ge 5 ] && gate_pass "可视化输出: $fig_count 张 Figure" || gate_fail "可视化输出不足 (需要≥5, 实际 $fig_count)"

            local pdf_count=$(find "$PROJECT_ROOT/results/figures" -name 'Fig*.pdf' 2>/dev/null | wc -l)
            [ "$pdf_count" -ge 5 ] && gate_pass "PDF 输出: $pdf_count 个" || gate_warn "PDF 输出不足"
            ;;
        06)
            local mouse_files=$(find "$PROJECT_ROOT/data/processed" -path '*mouse*' -name '*.h5ad' 2>/dev/null | wc -l)
            [ "$mouse_files" -gt 0 ] && gate_pass "小鼠空间数据: $mouse_files 文件" || gate_warn "小鼠空间数据未输出"
            ;;
        07)
            local lr_csv=$(find "$PROJECT_ROOT/results/tables" -name '*lr*' -o -name '*communication*' -o -name '*cellchat*' 2>/dev/null | wc -l)
            [ "$lr_csv" -gt 0 ] && gate_pass "细胞通讯: $lr_csv CSV 文件" || gate_warn "细胞通讯未输出"
            ;;
        final)
            echo ""
            echo "[Final] 交付物检查"

            local md_report=$(find "$PROJECT_ROOT/results/reports" -name '*.md' ! -name '_*' 2>/dev/null | wc -l)
            [ "$md_report" -gt 0 ] && gate_pass "MD 报告: $md_report 个" || gate_fail "MD 报告缺失"

            local docx_report=$(find "$PROJECT_ROOT/results/reports" -name '*.docx' 2>/dev/null | wc -l)
            [ "$docx_report" -gt 0 ] && gate_pass "DOCX 报告: $docx_report 个" || gate_fail "DOCX 报告缺失"

            local fig_png=$(find "$PROJECT_ROOT/results/figures" -name 'Fig*.png' 2>/dev/null | wc -l)
            local fig_pdf=$(find "$PROJECT_ROOT/results/figures" -name 'Fig*.pdf' 2>/dev/null | wc -l)
            [ "$fig_png" -ge 5 ] && gate_pass "Figure PNG: $fig_png 张" || gate_fail "Figure PNG 不足"

            local tables=$(find "$PROJECT_ROOT/results/tables" -name '*.csv' 2>/dev/null | wc -l)
            [ "$tables" -gt 0 ] && gate_pass "统计表格: $tables 个 CSV" || gate_warn "统计表格缺失"

            [ -f "$PROJECT_ROOT/docs/SPEC-visualization.md" ] && gate_pass "可视化 SPEC 存在" || gate_warn "可视化 SPEC 缺失"

            # Worklog coverage
            if [ -f "$PROJECT_ROOT/docs/WORKLOG.md" ]; then
                local phases_logged=$(grep -c '## Phase' "$PROJECT_ROOT/docs/WORKLOG.md" 2>/dev/null || echo 0)
                gate_pass "Worklog 覆盖: $phases_logged 个 Phase"
            fi
            ;;
    esac
}

# Run checks
if [ "$PHASE" = "all" ]; then
    for p in 01 02 03 04 05 06 07; do
        check_phase "$p"
    done
    check_phase "final"
elif [ "$PHASE" = "final" ]; then
    check_phase "final"
else
    check_phase "$PHASE"
fi

# Summary
echo ""
echo "============================================================"
TOTAL=$((PASS + FAIL + WARN))
echo "Gate Check 结果: ${GREEN}$PASS PASS${NC} | ${RED}$FAIL FAIL${NC} | ${YELLOW}$WARN WARN${NC} | 共 $TOTAL 项"
if [ "$FAIL" -eq 0 ]; then
    echo -e "状态: ${GREEN}通过 ✓${NC}"
else
    echo -e "状态: ${RED}未通过 — $FAIL 项需要修复${NC}"
fi
echo "============================================================"

exit $FAIL
