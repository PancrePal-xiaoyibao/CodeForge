#!/usr/bin/env bash
# ai4s-init.sh — AI4S Dry Lab 项目初始化
# 用法: bash .claude/skills/ai4s-dry-lab/scripts/ai4s-init.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
TEMPLATES="$SCRIPT_DIR/../templates"

echo "============================================================"
echo "AI4S Dry Lab — 项目初始化"
echo "============================================================"
echo "项目根目录: $PROJECT_ROOT"
echo ""

# 1. 创建标准目录结构
echo "[1/5] 创建目录结构..."
mkdir -p "$PROJECT_ROOT/docs"
mkdir -p "$PROJECT_ROOT/data/raw"
mkdir -p "$PROJECT_ROOT/data/processed/scrna"
mkdir -p "$PROJECT_ROOT/data/processed/spatial"
mkdir -p "$PROJECT_ROOT/data/processed/cross_species"
mkdir -p "$PROJECT_ROOT/scripts/01_data_acquisition"
mkdir -p "$PROJECT_ROOT/scripts/02_scrna_analysis"
mkdir -p "$PROJECT_ROOT/scripts/03_spatial_analysis"
mkdir -p "$PROJECT_ROOT/scripts/04_cross_comparison"
mkdir -p "$PROJECT_ROOT/scripts/05_visualization"
mkdir -p "$PROJECT_ROOT/results/figures"
mkdir -p "$PROJECT_ROOT/results/tables"
mkdir -p "$PROJECT_ROOT/results/reports"
echo "  ✓ 目录结构已创建"

# 2. 复制模板文件（仅在不存在时）
echo ""
echo "[2/5] 初始化文档模板..."

init_doc() {
    local src="$1"
    local dst="$2"
    local desc="$3"
    if [ -f "$dst" ]; then
        echo "  ⊙ $desc 已存在，跳过"
    else
        cp "$src" "$dst"
        echo "  ✓ $desc 已创建: $dst"
    fi
}

init_doc "$TEMPLATES/SPEC-experiment.md" "$PROJECT_ROOT/docs/SPEC-experiment.md" "实验方案 SPEC"
init_doc "$TEMPLATES/SPEC-visualization.md" "$PROJECT_ROOT/docs/SPEC-visualization.md" "可视化方案 SPEC"
init_doc "$TEMPLATES/WORKLOG.md" "$PROJECT_ROOT/docs/WORKLOG.md" "实验记录"

# 3. 创建 DATA_MANIFEST.md（仅在不存在时）
echo ""
echo "[3/5] 检查数据清单..."
if [ -f "$PROJECT_ROOT/data/raw/DATA_MANIFEST.md" ]; then
    echo "  ⊙ DATA_MANIFEST.md 已存在"
else
    cat > "$PROJECT_ROOT/data/raw/DATA_MANIFEST.md" << 'MANIFEST'
# 数据源说明文档 (Data Manifest)

**生成日期**: $(date +%Y-%m-%d)
**用途**: 供研究人员逐一核对数据来源、分组、质量，确认数据选择无误后再进入正式分析

---

## 一、数据集总览

| # | 数据集 | 类型 | 物种 | 细胞数 | 文件大小 | 下载状态 |
|---|--------|------|------|--------|---------|---------|
| | | | | | | |

---

## 二、各数据集详细信息

（待填写）

---

## 三、文件清单

（待填写）
MANIFEST
    echo "  ✓ DATA_MANIFEST.md 已创建"
fi

# 4. 创建 .gitignore（仅在不存在时）
echo ""
echo "[4/5] 检查 .gitignore..."
if [ -f "$PROJECT_ROOT/.gitignore" ]; then
    echo "  ⊙ .gitignore 已存在"
else
    cat > "$PROJECT_ROOT/.gitignore" << 'GITIGNORE'
# Data files (large)
data/raw/**/*.h5ad
data/raw/**/*.h5
data/raw/**/*.tar.gz
data/raw/**/*.zip
data/raw/**/*.mtx
data/raw/**/*.tiff
data/raw/**/*.tif
data/processed/**/*.h5ad

# Python
.venv/
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
GITIGNORE
    echo "  ✓ .gitignore 已创建"
fi

# 5. 检查项目状态
echo ""
echo "[5/5] 项目状态检查..."
echo ""
echo "  目录结构:"
echo "    docs/           $(ls "$PROJECT_ROOT/docs/" 2>/dev/null | wc -l) 文件"
echo "    data/raw/       $(find "$PROJECT_ROOT/data/raw" -maxdepth 2 -name '*.h5ad' -o -name '*.h5' -o -name '*.tar*' 2>/dev/null | wc -l) 数据文件"
echo "    scripts/        $(find "$PROJECT_ROOT/scripts" -name '*.py' 2>/dev/null | wc -l) 脚本"
echo "    results/        $(find "$PROJECT_ROOT/results" -type f 2>/dev/null | wc -l) 输出文件"

echo ""
echo "============================================================"
echo "初始化完成！"
echo ""
echo "下一步:"
echo "  1. 编辑 docs/SPEC-experiment.md 定义研究方案"
echo "  2. 填写 data/raw/DATA_MANIFEST.md 记录数据来源"
echo "  3. 运行 /ai4s-lab next 开始第一个 Phase"
echo "============================================================"
