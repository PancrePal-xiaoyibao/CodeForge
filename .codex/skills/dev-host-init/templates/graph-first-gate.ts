/**
 * graph-first-gate.ts — 三层代码阅读 fallback 硬闸门 + 逐轮铁律注入
 *
 * 主人钦定的硬逻辑（read 代码文件时按序判定，命中即 block）：
 *
 *   ┌─ Layer 1 图谱查询（默认起点）────────────────────────────┐
 *   │ 项目已索引 → 必须先用 codebase-memory 查询类工具：          │
 *   │ search_graph / trace_path / get_code_snippet / query_graph │
 *   │ / get_architecture / search_code                          │
 *   └──── 未索引 / 索引过期？──→ Layer 2 ↓ ────────────────────┘
 *
 *   ┌─ Layer 2 索引保障 ────────────────────────────────────────┐
 *   │ a. 项目未索引（无 .codebase-memory）→ 先 index_repository   │
 *   │ b. 索引过期（目标文件 mtime > 索引 mtime，embedding 落后）   │
 *   │    → 先 detect_changes / index_repository 更新              │
 *   │ 完成后回到 Layer 1 查图谱 —— 不允许索引完直接 read          │
 *   └────────────────────────────────────────────────────────────┘
 *
 *   ┌─ Layer 3 直读兜底（仅以下情形放行 read）───────────────────┐
 *   │ a. 本会话已有 ≥1 次图谱查询工具成功调用（tool_result 非 error）│
 *   │ b. 目标文件是本会话自己 edit/write 改过的（开发中读回）      │
 *   │ c. 非代码文件（md/json/toml...）或路径不在 PROJECT_ROOTS 下  │
 *   │ d. 全局拦截次数达 MAX_BLOCKS（防死锁最后兜底）               │
 *   └────────────────────────────────────────────────────────────┘
 *
 * 另：context 事件在每次 LLM 调用前把铁律合并进最后一条 user 消息
 *     （深拷贝不落盘、不累积、不破坏前缀 KV cache）。
 *
 * 安装：~/.pi/agent/extensions/ 全局自动加载；生效：重启 pi 或 /reload。
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { existsSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { homedir } from "node:os";

// ============================== 配置 ==============================

/** 闸门管辖的项目根目录（其下的代码文件受三层 fallback 约束；系统库/vendor 等路径放行） */
const PROJECT_ROOTS = [join(homedir(), "Development")]; // 主开发根目录，按本机实际增删

/** 视为"代码文件"的后缀（读这些才走闸门；md/json/toml 等参考文件不拦） */
const CODE_EXT =
  /\.(ts|tsx|mts|cts|js|jsx|mjs|cjs|py|pyi|rs|go|java|c|h|cc|cpp|hpp|rb|php|sql|sh|scala|kt|swift|lua|vue|svelte|r|R|jl)$/;

/** Layer 1 查询类图谱工具（后缀匹配，兼容 server 前缀形式 codebase-memory-mcp_xxx） */
const QUERY_SUFFIXES = [
  "search_graph",
  "trace_path",
  "get_code_snippet",
  "query_graph",
  "get_architecture",
  "search_code",
];

/** 同一会话 read 闸门最大拦截次数（超过后放行，MCP 不可用等死锁场景的最后兜底） */
const MAX_BLOCKS = 3;

/** 向上探测 .codebase-memory 的最大目录层数 */
const MAX_WALK = 12;

/** 索引 mtime 缓存有效期（ms）——期间内重复判定不重扫 .codebase-memory */
const IDX_MTIME_TTL = 30_000;

/** mtime 比较容差（ms），规避同秒写入抖动 */
const MTIME_EPSILON = 2_000;

// ============================== 状态 ==============================

let graphQueryOK = 0; // 本会话查询类图谱工具成功（tool_result 非 error）次数
let readBlockCount = 0; // 本会话 read 被拦截次数
const sessionEditedFiles = new Set<string>(); // 本会话 edit/write 改过的文件
const markerCache = new Map<string, string | null>(); // dir -> 所属已索引项目根（null=未索引）
const idxMtimeCache = new Map<string, { at: number; mtime: number }>();

function resetState() {
  graphQueryOK = 0;
  readBlockCount = 0;
  sessionEditedFiles.clear();
}

// ============================== 判定辅助 ==============================

function isQueryTool(name: string): boolean {
  return QUERY_SUFFIXES.some((s) => name === s || name.endsWith(`_${s}`));
}

function underProjectRoots(p: string): boolean {
  return PROJECT_ROOTS.some((r) => p === r || p.startsWith(r + "/"));
}

/**
 * 向上探测包含 .codebase-memory 的项目根。
 * 返回 null 表示（PROJECT_ROOTS 范围内）未索引。结果按目录缓存。
 */
function findIndexedRoot(filePath: string): string | null {
  let dir = dirname(filePath);
  const walked: string[] = [];
  for (let i = 0; i < MAX_WALK; i++) {
    if (markerCache.has(dir)) {
      const hit = markerCache.get(dir)!;
      for (const d of walked) markerCache.set(d, hit);
      return hit;
    }
    if (!underProjectRoots(dir)) break; // 越过项目根边界即停
    walked.push(dir);
    if (existsSync(join(dir, ".codebase-memory"))) {
      for (const d of walked) markerCache.set(d, dir);
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  for (const d of walked) markerCache.set(d, null);
  return null;
}

/** 已索引项目的索引新鲜度：.codebase-memory 内最新文件 mtime（带 TTL 缓存） */
function indexMtime(root: string): number {
  const hit = idxMtimeCache.get(root);
  if (hit && Date.now() - hit.at < IDX_MTIME_TTL) return hit.mtime;
  let m = 0;
  try {
    for (const f of readdirSync(join(root, ".codebase-memory"))) {
      try {
        const s = statSync(join(root, ".codebase-memory", f));
        if (s.mtimeMs > m) m = s.mtimeMs;
      } catch {
        /* 单文件 stat 失败忽略 */
      }
    }
  } catch {
    /* 目录读取失败按 0 处理 */
  }
  idxMtimeCache.set(root, { at: Date.now(), mtime: m });
  return m;
}

function fileMtime(p: string): number {
  try {
    return statSync(p).mtimeMs;
  } catch {
    return 0;
  }
}

/** 未索引时给出建议的项目根（PROJECT_ROOTS 下第一级子目录） */
function suggestRepoRoot(filePath: string): string {
  for (const r of PROJECT_ROOTS) {
    if (filePath.startsWith(r + "/")) {
      const seg = filePath.slice(r.length + 1).split("/")[0];
      return join(r, seg);
    }
  }
  return dirname(filePath);
}

// ============================== 文案 ==============================

const PER_TURN_REMINDER = [
  "[system-reminder · 三层代码阅读铁律 · 每轮生效]",
  "read 代码文件前必须按序走 fallback，禁止跳层：",
  "  Layer 1 图谱查询：先用 codebase-memory MCP（search_graph / trace_path / get_code_snippet / query_graph / get_architecture / search_code）查代码结构与调用关系；",
  "  Layer 2 索引保障：项目未索引、或索引/embedding 过期（代码比索引新）时，先 index_repository 建索引 / detect_changes 检查更新，完成后回到 Layer 1 查图谱——不允许索引完直接 read；",
  "  Layer 3 直读兜底：仅当图谱确实无法满足（非代码文件、图谱查不到、本会话自己改动的文件）才直接 read。",
  "本会话内图谱查询成功一次后闸门即放行；跳过 Layer 1/2 直接 read 项目代码 = 违规，会被工具闸门拦截。",
].join("\n");

function reasonNoIndex(path: string): string {
  return [
    "⛔ 三层铁律 · Layer 2 拦截：该项目尚未建立 codebase-memory 索引。",
    "正确动作：先调用 index_repository（repo_path 建议取 " + suggestRepoRoot(path) + "；模式按规模选 full/moderate/fast）建立索引与 embedding；",
    "索引完成后回到 Layer 1 查图谱（search_graph / trace_path / get_code_snippet 等），最后才可直读。",
    "若确属一次性临时片段不值得建索引，向主人说明理由后依赖拦截上限兜底。",
  ].join("\n");
}

function reasonStaleIndex(path: string, root: string): string {
  return [
    "⛔ 三层铁律 · Layer 2 拦截：索引疑似过期——目标文件比索引新（embedding 落后于代码变更）。",
    `目标：${path}（所属已索引项目：${root}）`,
    "正确动作：先 detect_changes 检查影响范围，或 index_repository 重新索引；完成后回到 Layer 1 查图谱，最后才可直读。",
    "本会话内你自己刚改过的文件不受此拦截。",
  ].join("\n");
}

const REASON_GRAPH_FIRST = [
  "⛔ 三层铁律 · Layer 1 拦截：项目已建立 codebase-memory 索引，但本会话尚未有任何一次成功的图谱查询。",
  "必须先用查询类工具：search_graph / trace_path / get_code_snippet / query_graph / get_architecture / search_code；",
  "图谱确实无法回答后，再回来 read 具体行号（届时闸门已放行）。",
  "这是 AGENTS.md 的强制规则（先问图谱，再无细节，最后才读文件），不是可选项。读 md/json/toml 等非代码文件不受此限制。",
].join("\n");

// ============================== 扩展主体 ==============================

export default function graphFirstGate(pi: ExtensionAPI) {
  // --- 会话生命周期：重置每会话状态 ---
  pi.on("session_start", async (_event, ctx) => {
    resetState();
    if (ctx.hasUI && findIndexedRoot(join(ctx.cwd, "x"))) {
      ctx.ui.notify("codebase-memory 索引已就绪：代码探索请先走图谱（三层铁律由闸门硬性执行）", "info");
    }
  });

  // --- tool_call：记录本会话改动文件 + read 三层闸门判定 ---
  pi.on("tool_call", async (event, ctx) => {
    const name = event.toolName;

    // 记录本会话 edit/write 改过的文件（Layer 3-b 放行依据）
    if (name === "edit" || name === "write") {
      const p = (event.input as { path?: string })?.path;
      if (p) sessionEditedFiles.add(p);
      return;
    }

    if (name !== "read") return;

    const path: string = (event.input as { path?: string })?.path ?? "";

    // Layer 3-c：非代码文件、项目区外 → 不管
    if (!path || !CODE_EXT.test(path) || !underProjectRoots(path)) return;

    // Layer 3-a：本会话已有成功的图谱查询 → 直读兜底合法
    if (graphQueryOK > 0) return;

    // Layer 3-d：拦截上限 → 防死锁最后兜底
    if (readBlockCount >= MAX_BLOCKS) return;

    // Layer 3-b：本会话自己改过的文件 → 开发中读回
    if (sessionEditedFiles.has(path)) return;

    readBlockCount++;
    const root = findIndexedRoot(path);

    // Layer 2-a：未索引 → 先建索引
    if (root === null) {
      if (ctx.hasUI) ctx.ui.notify(`铁律闸门 [Layer2·未索引] #${readBlockCount}/${MAX_BLOCKS}：${path}`, "warn");
      return { block: true, reason: reasonNoIndex(path) };
    }

    // Layer 2-b：索引过期（目标文件比索引新）→ 先更新索引
    if (fileMtime(path) > indexMtime(root) + MTIME_EPSILON) {
      if (ctx.hasUI) ctx.ui.notify(`铁律闸门 [Layer2·索引过期] #${readBlockCount}/${MAX_BLOCKS}：${path}`, "warn");
      return { block: true, reason: reasonStaleIndex(path, root) };
    }

    // Layer 1：已索引、未过期、没查过图谱 → 先查图谱
    if (ctx.hasUI) ctx.ui.notify(`铁律闸门 [Layer1·图谱优先] #${readBlockCount}/${MAX_BLOCKS}：${path}`, "warn");
    return { block: true, reason: REASON_GRAPH_FIRST };
  });

  // --- tool_result：仅"查询类图谱工具成功"才解锁 Layer 3（维护类/失败均不解锁）---
  pi.on("tool_result", async (event) => {
    if (event.isError) return;
    if (isQueryTool(event.toolName)) graphQueryOK++;
  });

  // --- 逐轮注入：每次 LLM 调用前，把铁律合并进最后一条 user 消息 ---
  pi.on("context", async (event) => {
    const msgs = event.messages;
    if (!msgs || msgs.length === 0) return;

    const last = msgs[msgs.length - 1] as { role: string; content: unknown };

    if (last.role === "user") {
      msgs[msgs.length - 1] = {
        ...last,
        content: mergeContent(last.content, PER_TURN_REMINDER),
      } as (typeof msgs)[number];
    } else {
      msgs.push({
        role: "user",
        content: PER_TURN_REMINDER,
      } as (typeof msgs)[number]);
    }

    return { messages: msgs };
  });
}

/** 把提醒文本合并进 user content（兼容 string 与 block 数组两种形态） */
function mergeContent(content: unknown, reminder: string): unknown {
  if (typeof content === "string") {
    return `${content}\n\n${reminder}`;
  }
  if (Array.isArray(content)) {
    return [...content, { type: "text", text: reminder }];
  }
  return content;
}
