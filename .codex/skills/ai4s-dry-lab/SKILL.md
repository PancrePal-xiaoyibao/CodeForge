---
name: ai4s-dry-lab
description: AI4S 端到端干实验自动化研究引擎。自启动检查+追溯入职(半路加入也能补齐历史)+强制Worklog(W1)+输出目录README(W2)+强制文献验证(W3)+强制脚本日志(W4)+分层记忆注入+SPEC驱动+OODA循环+Gate门控。适用于scRNA-seq/空间转录组/跨物种比较等计算生物学项目。
version: 2.2.0
---

# AI4S Dry Lab — 端到端干实验自动化研究引擎

## 设计哲学

从计算生物学项目实践中提炼。核心设计原则：

1. **SPEC 驱动**：研究方案是北极星，所有分析可追溯到 SPEC 目标
2. **Worklog 追溯**：每一步操作都有记录
3. **OODA 循环**：Observe-Orient-Decide-Act 假设驱动闭环
4. **Gate Control**：线性门控验证交付物完整性
5. **Human-in-the-loop**：关键决策必须与研究者确认
6. **【强制】实验记录不可跳过** — 任何改动、测试、运行必须先写 WORKLOG
7. **【强制】输出目录必须带解释文档** — 每个结果目录含 README_文件说明.md，逐图逐表引用代码解释
8. **【强制】文献验证不可跳过 (W3)** — 每个关键结果必须有文献支撑，WORKLOG 和 README 必须包含文献检索记录

适用场景：scRNA-seq、空间转录组、多组学、跨物种比较、论文级可视化。
不适用于：湿实验设计、临床数据分析、非生物学领域。

---

## 自启动协议 (Auto-Bootstrap Protocol)

skill 激活时自动检查任务容器套件，有则改之无则加勉，保证任何时候都能进入工作状态。
即使半路加入已有项目，也能扫描理解全部历史工作，反向填充所有容器文档。

### 任务容器套件（5 个核心文件 + 硬件配置）

| # | 文件 | 作用 | 缺失时动作 |
|---|------|------|-----------|
| 0 | `HARDWARE_CONFIG.md` | 硬件资源限制（防止资源耗尽） | 自动探测系统硬件 → 生成 |
| 1 | `docs/SPEC-experiment.md` | 研究方案（北极星） | 新项目→从模板创建；已有项目→追溯构建 |
| 2 | `docs/WORKLOG.md` | 实验记录（W1 强制） | 新项目→从模板创建；已有项目→反向填充 |
| 3 | `docs/STATE.md` | 状态检查点（记忆锚点） | 始终创建，从项目实际状态生成 |
| 4 | `docs/SPEC-visualization.md` | 可视化方案 | 从模板创建（可后续填充） |
| 5 | `data/raw/DATA_MANIFEST.md` | 数据清单 | 从模板创建 |

### 硬件感知协议 (Hardware Awareness Protocol) — Advisory 模式

自动探测硬件、生成 HARDWARE_CONFIG.md、警告资源超限，但不阻塞执行。
探测内容：CPU cores, RAM, GPU, max_workers, future.globals.maxSize。
所有分析脚本开头应读取此配置，不要直接使用 detectCores()。

### 激活时自动检测流程

```
/ai4s-dry-lab 激活
  │
  ├─ 0. 【硬件感知检查】(Advisory 模式)
  │     ├─ 检查 HARDWARE_CONFIG.md → 存在则读取，不存在则探测生成
  │     ├─ 将硬件限制写入 STATE.md 的 Hardware 段
  │     └─ 脚本请求超限 → ⚠️ WARNING（不阻塞执行）
  │
  ├─ 1. 读取 docs/STATE.md
  │     ├─ 存在 → 恢复上下文（Phase/Step/OODA位置）→ 跳到第4步
  │     └─ 不存在 → 继续
  │
  ├─ 2. 检测项目状态
  │     ├─ 空项目 → 全新项目初始化
  │     └─ 非空项目 → 触发追溯入职协议
  │
  ├─ 3. 追溯入职协议 (Retroactive Onboarding)
  │     ├─ 扫描项目结构 → 识别脚本/输出/数据
  │     ├─ 读取每个脚本 → 理解功能、输入输出映射
  │     ├─ 反向构建 SPEC → 反向填充 WORKLOG → 生成输出 README → 生成 STATE.md
  │     └─ 呈现摘要给研究者确认 → 确认后进入正常循环
  │
  └─ 4. 进入正常 OODA 循环
        ├─ 读 SPEC 目标 → 读 STATE 位置 → 读 WORKLOG 尾部
        └─ 开始下一轮 Observe → Orient → Decide → Act
```

追溯入职详细步骤见 `references/onboard-protocol.md`。

---

## 分层记忆架构 (Layered Memory Architecture)

解决长链路问题：科研任务跨越多轮对话/context 压缩，通过分层设计保证核心规则和状态永不丢失。

| 层 | 载体 | 内容 | 更新频率 |
|----|------|------|---------|
| L1 规则层 | SKILL.md 本体 | 不可妥协规则、流程 | 版本化 |
| L2 状态层 | docs/STATE.md | 当前 Phase/Step/OODA 位置、待办 | 每轮更新 |
| L3 日志层 | docs/WORKLOG.md | 全部实验记录 | 每步追加 |
| L4 沉淀层 | 输出目录 README + self.opt | 结果解释、经验 | 产出时 |
| L5 文献层 | 文献检索记录 | 每结果对应文献 | W3 强制 |

## AI4S Dry Lab 规则

1. 一切工作从读取 SPEC 开始
2. 任何代码改动先写 WORKLOG（W1）
3. 任何结果目录必须有 README_文件说明.md（W2）
4. 任何关键结果必须有文献验证（W3）
5. 任何脚本运行必须有日志（W4）
6. 关键决策征求研究者确认

## 不可妥协规则（Inviolable Rules）

1. **不做无 SPEC 的分析** — 没有目标的分析是无底洞
2. **不跳过文献验证** — 干实验结论必须有文献支撑
3. **不隐瞒失败** — 失败必须写入 WORKLOG，禁止静默重跑
4. **不虚报完成** — 无输出验证的"完成"是造假
5. **不无限调参** — 同一问题最多 3 轮尝试，之后必须改变策略或询问研究者
6. **不做湿实验决策** — 不提供临床/湿实验建议
7. **不忽略硬件限制** — 资源超限必须警告
8. **不擅自扩大范围** — 超 SPEC 的分析必须征得研究者同意

---

## OODA 循环引擎（含强制记录点）

```
Observe（观察）→ Orient（定向）→ Decide（决策）→ Act（行动）
      ↑                                                 │
      └────────────── 回到 Observe（带新证据）────────────┘
```

### Observe — 观察当前状态
- 读取 STATE.md 当前阶段、WORKLOG 最近记录
- 查看数据/输出目录变化
- **强制记录点**：观察结果写入 WORKLOG

### Orient — 定向分析
- 对照 SPEC 目标，判断当前位置与目标的差距
- 检查假设是否需要修正
- **强制记录点**：定向结论写入 STATE.md

### Decide — 决策
- 明确下一步行动（代码/分析/验证）
- 评估资源限制（HARDWARE_CONFIG.md）
- **强制记录点**：决策及理由写入 WORKLOG

### Act — 执行
- 运行脚本（必须带日志，W4）
- 验证输出（数值、可视化）
- **强制记录点**：结果写入 WORKLOG + 输出目录 README

## Gate Check 门控系统

线性门控验证交付物完整性，见 `scripts/ai4s-gate-check.sh`：

| Gate | 检查内容 | 通过条件 |
|------|---------|---------|
| G1 | SPEC 存在且可追溯 | docs/SPEC-experiment.md 存在 |
| G2 | WORKLOG 最新 | 最近操作有记录 |
| G3 | 输出 README 齐全 | 每个结果目录有 README_文件说明.md |
| G4 | 文献验证完成 | 关键结果有文献引用 |
| G5 | 脚本日志存在 | 每个脚本运行有日志 |

## 核心产出物

1. **SPEC-experiment.md** — 研究方案（北极星文档）
2. **WORKLOG.md** — 完整实验记录（时间线）
3. **STATE.md** — 当前状态检查点
4. **结果目录 + README_文件说明.md** — 逐图逐表解释
5. **文献验证记录** — 关键结果的文献支撑

## 项目目录规范

```
project-root/
├── HARDWARE_CONFIG.md          # 硬件配置
├── docs/
│   ├── SPEC-experiment.md      # 研究方案
│   ├── SPEC-visualization.md   # 可视化方案
│   ├── WORKLOG.md              # 实验记录
│   └── STATE.md                # 状态检查点
├── data/
│   ├── raw/                    # 原始数据 + DATA_MANIFEST.md
│   └── processed/              # 处理数据
├── scripts/                    # 分析脚本
├── results/                    # 输出（每目录带 README）
└── literature/                 # 文献与验证记录
```

## 轻量级验证脚本

| 脚本 | 用途 | 用法 |
|------|------|------|
| `scripts/ai4s-init.sh` | 初始化任务容器套件 | `bash scripts/ai4s-init.sh` |
| `scripts/ai4s-worklog.py` | 快速追加 WORKLOG 条目 | `python scripts/ai4s-worklog.py "内容"` |
| `scripts/ai4s-gate-check.sh` | Gate 门控验证 | `bash scripts/ai4s-gate-check.sh` |
| `scripts/check_literature.py` | 文献验证检索记录 | `python scripts/check_literature.py` |
| `scripts/log_skill_call.py` | skill 调用日志 | `python scripts/log_skill_call.py` |

## 研究生命周期

```
文献调研 → SPEC 设计 → 数据获取 → 分析循环(OODA) → 结果验证 → 可视化 → 论文撰写
   │        │            │            │              │          │          │
   └────────┴──Gate G1───┴──G2────────┴──G3──────────┴──G4───────┴──G5──────┘
```

## 质量标准

- **可追溯**：任何结论可回溯到 SPEC + 代码 + 数据 + 文献
- **可复现**：脚本+数据+环境记录齐全
- **可验证**：关键结果有 Gate 证据和文献支撑
- **诚实**：失败和不确定性如实记录

## 关联 Skill

| 关系 | Skill | 场景 |
|------|-------|------|
| 前置 | deep-research | 文献调研与方案设计 |
| 配合 | dev-env-scan | 硬件与环境探测 |
| 配合 | code-review | 分析脚本质量门 |
| 配合 | goal-driven-development | 里程碑证据化执行 |
| 后续 | extract-research-framework | 研究方法论沉淀复用 |
