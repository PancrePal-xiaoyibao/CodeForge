---
name: loop-engineer
description: Loop 系统工程师 — 从用户需求出发，设计并开发完整的多 skill 联动 package。扫描现有 skill 资产，识别可复用与缺失项，逐一开发后组包，编写主调度 skill 平滑层。也可用于对已有 package 进行联动完整性审计（格式合规+主调度逻辑+入口文档同步+命名一致性）。当用户说"我需要一个 XX 系统/loop/agent 包"、"帮我设计一个多技能联动方案"、"检查 package 联动完整性"时触发。不适用于单个 skill 开发。
---

# Loop Engineer — 需求驱动的系统化 Skill Package 工程师

## Overview

Loop Engineer 是 skill-governor 的上层调度者。从用户需求出发，设计完整的多 skill 联动体系：盘点现有资产、识别缺口、逐一补齐、组包联调、编写平滑层，最终交付完整 package。

**两种工作模式：**
- **模式 A: 新建 Package** — 完整执行 Phase 0 → Phase 5 全流程
- **模式 B: 审计已有 Package** — 执行 Phase 1 资产盘点 + Phase 5 验证 checklist，输出诊断报告

## Workflow

### Phase 0: 需求理解与 OODA 映射
1. 接收用户需求，提炼能力模块清单
2. 映射 Observe/Orient/Decide/Act 四槽位 + 修正面
3. 获得用户确认

### Phase 1: 资产盘点与 Gap 分析
1. 扫描现有 skill 列表
2. 生成 Gap 报告（可复用 / 需适配 / 需新建）
3. **【必须】识别主调度 Skill** — 每个 package 必须有且仅有一个主调度节点
4. **【必须】Package 定位输出** — 目的 + 主调度名 + 子 skill 职责
5. Gate: 用户确认

### Phase 2: 缺失 Skill 开发
- 对每个缺失 skill 走 skill-governor 全流程（三镜像同步）
- Gate: 缺失列表清零

### Phase 3: 组包
1. 创建 package 三平台目录
2. 复制所有相关 skill
3. 路径验证

### Phase 4: 平滑层与主调度
1. 确定主调度 skill（可复用已有 / 新建 orchestrator / 加前置分诊）
2. 编写主调度 SKILL.md（能力索引 + 路由逻辑表 + 数据流 + 回流机制）
3. 上下文传递与错误回退

### Phase 5: 验证与交付

**5.1 三平台格式合规检查** — Codex/Claude/Gemini 格式 + description 语义一致

**5.2 主调度逻辑检查** — 有主调度 / 路由表完整 / 无歧义 / 有回流机制

**5.3 入口文档同步检查** — CLAUDE.md / AGENTS.md / GEMINI.md 列出所有 skill 且命名一致

**5.4 命名一致性检查** — command 名可追溯到 skill 名，无混淆或重复

**5.5 联动路径检查** — 引用路径存在 / scripts 有效 / 接口对齐 / 无孤立文件

**5.6 README 生成/更新** — 架构图 + 清单 + 主调度说明 + 部署 + 示例

Gate: 用户确认 → commit

## Output Contract

完成时必须产出：Gap Analysis Report（含主调度识别）、完整 Package 目录（三平台）、主调度 Skill（含路由表+回流机制）、平滑层、入口文档（CLAUDE.md/AGENTS.md/GEMINI.md）、Package README。

## Resources

| 文件 | 用途 | 何时加载 |
|------|------|----------|
| skill-governor | 单 skill 开发规范 | Phase 2 |
| 项目 README | 现有 skill 清单速查 | Phase 1 |

## 关联 Skill（网络调度协议）

| 关系 | Skill | 场景 |
|------|-------|------|
| 被调用 | ai-spec | 需要设计多 skill 联动系统时 |
