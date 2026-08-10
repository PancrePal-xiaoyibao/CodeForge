# 可视化方案 SPEC — 论文级别图表设计

**版本**: v1.0
**日期**: {YYYY-MM-DD}
**关联**: SPEC-experiment.md

---

## 1. 叙事逻辑链

```
Figure 1: [发现/鉴定] — 核心结果展示
    ↓
Figure 2: [分子特征] — 深入刻画
    ↓
Figure 3: [空间定位] — 组织学验证
    ↓
Figure 4: [跨物种保守性] — 进化意义
    ↓
Figure 5: [与已知类型区分] — 新颖性论证
    ↓
Figure 6: [功能通讯] — 生物学功能
    ↓
Figure 7: [综合总结] — 收敛论证
```

---

## 2. 设计系统

### 2.1 颜色方案

| 用途 | 颜色 | HEX | 说明 |
|------|------|-----|------|
| CMC 高亮 | | | 核心标记色 |
| Human | | | 人样本色 |
| Mouse | | | 小鼠样本色 |
| Rat | | | 大鼠样本色 |
| 背景 | | | 非目标细胞 |
| Other | | | 对比对照组 |

### 2.2 字体

| 元素 | 字号 | 字重 |
|------|------|------|
| Figure title | 12pt | bold |
| Panel title | 9-10pt | bold |
| Axis label | 8pt | normal |
| Tick label | 6-7pt | normal |
| Legend | 7pt | normal |
| Panel label | 12pt | bold |

### 2.3 尺寸规范

| 项目 | 规格 |
|------|------|
| 输出 DPI | 300 |
| 格式 | PNG + PDF |
| 标准 Figure | 11-14 inch 宽 |

---

## 3. Figure 详细定义

### Figure 1: [标题]

**叙事定位**: Results 第一节，核心发现

**布局**: X 行 × Y 列

| Panel | 内容 | 数据源 | 绘图方法 |
|-------|------|--------|---------|
| A | | | |
| B | | | |
| C | | | |

**精确坐标**（fig.add_axes）:
- Panel A: [left, bottom, width, height]
- Panel B: ...

### Figure 2: [标题]

（同上结构）

---

## 4. Supplementary Figures

| Figure | 内容 | 说明 |
|--------|------|------|
| S1 | QC 统计 | 数据质量保证 |
| S2 | 聚类分辨率 | 参数选择依据 |
| S3 | 全部 marker | 完整基因表达 |

---

## 5. 数据源映射

| Figure | 需要的数据文件 | 对应 Phase |
|--------|---------------|-----------|
| Fig1 | data/processed/scrna/*.h5ad | Phase 2 |
| Fig2 | results/tables/*.csv | Phase 2 |
| Fig3 | data/processed/spatial/*.h5ad | Phase 3 |
| Fig4 | results/tables/*cross*.csv | Phase 4 |
| Fig5 | data/processed/scrna/*.h5ad | Phase 2 |
| Fig6 | results/tables/*communication*.csv | Phase 7 |
| Fig7 | results/tables/*.csv | Phase 7 |

---

## 6. 与论文 Results 章节对应

| Results 章节 | 对应 Figure | 核心结论 |
|-------------|------------|---------|
| 3.1 | Fig1 | |
| 3.2 | Fig2 | |
| 3.3 | Fig3 | |
| 3.4 | Fig4, Fig5 | |
| 3.5 | Fig6, Fig7 | |
