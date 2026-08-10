# OODA 循环在干实验研究中的应用指南

## 概述

OODA（Observe-Orient-Decide-Act）是 John Boyd 提出的决策循环模型，本指南将其适配为干实验（计算生物学/生物信息学）研究的标准认知框架。

## 与传统科学方法的映射

| 科学方法 | OODA 对应 | 干实验实现 |
|---------|----------|----------|
| 观察/数据收集 | **Observe** | 运行脚本、加载数据、QC、初步可视化 |
| 文献调研/假设评估 | **Orient** | PubMed 检索、结果与已知对比、意外发现标记 |
| 假设形成/修正 | **Decide** | 继续推进/修正参数/回退重做/标记新发现 |
| 实验/验证 | **Act** | 执行分析、生成输出、Gate Check |

## 干实验中的典型 OODA 循环

### 循环 1: 数据 QC

```
Observe: 加载 H5AD，计算 QC 指标
  → 18,269 cells after filtering (69% retention)
Orient: 与文献对比 QC 阈值
  → PMID:39567783 使用类似阈值，合理
Decide: QC 参数合理，继续
Act: 进入 Phase 2b (CD34 filtering)
```

### 循环 2: 细胞类型鉴定

```
Observe: Leiden 聚类得到 13 个 cluster
  → Cluster 7: 191 cells, highest CMC score (0.272)
Orient: 检查 marker gene 表达
  → CD34+/PDGFRA+/PECAM1- ✓
  → CAV1, ELN, RSPO3 高表达 ✓
  → 文献: 与大鼠筋膜 CMC (Huang 2025) 核心标记一致
Decide: Cluster 7 确认为 CMC 候选
  → 标记为新发现，需要空间验证
Act: 进入 Phase 3 (spatial mapping)
```

### 循环 3: 意外发现处理

```
Observe: 空间共定位显示 CMC 富集于 smooth muscle zone
  → enrichment fold = 1.46-2.11x
Orient: 与文献对比
  → 已知 telocytes 位于 subepithelial zone
  → CMC 定位不同 → 支持非 telocyte 论点
  → 但需要更多证据
Decide: 标记为关键发现，追加验证
  → 更新 SPEC: 增加空间定位详细分析
Act: 执行 Phase 3c (colocalization) + 检索更多文献
```

### 循环 4: 矛盾处理

```
Observe: CD34 表达检测率在 Visium spots 中仅 0.9-3.4%
Orient: scRNA-seq 中 CD34 阳性率约 15-20%
  → 矛盾原因：Visium spot 含 10-30 cells，信号稀释
  → 使用 label transfer 而非直接基因检测
Decide: 方法调整 — 使用反卷积而非直接检测
Act: 修改 03b 脚本，改用 label transfer 方法
```

## 收敛判断标准

研究线收敛的条件：

1. **目标覆盖**: SPEC 中所有 P0 目标 (G1-Gn) 有对应结果
2. **文献锚定**: 关键结果至少 1 次文献验证（PMID/DOI）
3. **无未解决矛盾**: 不存在"与文献矛盾且未解释"的发现
4. **可视化确认**: 与研究者讨论确认可视化方案
5. **Gate 通过**: 所有 Gate Check 项目通过

## 发散/收敛控制

### 发散信号（需要扩展分析）

- 发现 SPEC 未覆盖的新细胞类型/基因
- 跨物种比较发现意料之外的保守性/差异
- 空间定位与预期不一致

### 收敛信号（可以收紧范围）

- 多个独立分析线指向相同结论
- 文献验证充分，无重大矛盾
- 可视化方案已确认，不追加新 Figure

### 控制 Agent 行为

- 发散时：自动标记为"新发现"，写入 Worklog，等待研究者确认
- 收敛时：自动运行 Gate Check，准备进入下一 Phase
- 不自动决定发散/收敛 — 必须在 Decide 阶段与研究者确认
