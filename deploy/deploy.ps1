# ============================================================================
# CodeForge 一键部署脚本 (Windows PowerShell)
# 用法: 在仓库根目录运行  .\deploy\deploy.ps1
# 行为: 合并部署 .claude/.codex/.gemini 到 %USERPROFILE%，并写入 .agents/skills，
#       重名文件自动备份为 *.codeforge-bak.<TIMESTAMP>
# ============================================================================
#requires -Version 5.1
[CmdletBinding()]
param(
    [Alias('y')]
    [switch]$Yes
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
$HomeDir   = $env:USERPROFILE
$Timestamp = Get-Date -Format 'yyyyMMddHHmmss'

$env:PYTHONUTF8 = 1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ''
Write-Host '  ====================================================' -ForegroundColor Cyan
Write-Host '    CodeForge - 一键部署 (Windows PowerShell)' -ForegroundColor Cyan
Write-Host '  ====================================================' -ForegroundColor Cyan
Write-Host "  Source:  $RepoRoot"
Write-Host "  Target:  $HomeDir"
Write-Host ''

if (-not $Yes) {
    $confirm = Read-Host '  将合并部署 .claude/.codex/.gemini/.agents，重名文件自动备份。继续？(y/N)'
    if ($confirm -notmatch '^[yY]') {
        Write-Host '  已取消。' -ForegroundColor Yellow
        exit 0
    }
}
else {
    Write-Host '  非交互模式：已跳过确认。' -ForegroundColor Yellow
}

function Merge-CodeForgeDir {
    param(
        [string]$SubPath,
        [string]$TargetSubPath = $SubPath
    )
    $src = Join-Path $RepoRoot $SubPath
    $dst = Join-Path $HomeDir $TargetSubPath
    if (-not (Test-Path $src)) {
        Write-Host "  [SKIP] 源不存在: $SubPath" -ForegroundColor DarkGray
        return
    }
    if (-not (Test-Path $dst)) {
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
    }
    $bakCount = 0
    Get-ChildItem $src -Force | ForEach-Object {
        $target = Join-Path $dst $_.Name
        if (Test-Path $target) {
            $bak = "$target.codeforge-bak.$Timestamp"
            Move-Item $target $bak -Force
            Write-Host "    [BACKUP] $($_.Name) -> $(Split-Path -Leaf $bak)" -ForegroundColor Yellow
            $bakCount++
        }
        Copy-Item $_.FullName $target -Recurse -Force
    }
    Write-Host "  [OK] $SubPath -> $TargetSubPath  (备份 $bakCount 项)" -ForegroundColor Green
}

Write-Host ''
Write-Host '  正在部署...' -ForegroundColor Cyan
Merge-CodeForgeDir '.claude\skills'
Merge-CodeForgeDir '.claude\commands'
Merge-CodeForgeDir '.claude\agents'
Merge-CodeForgeDir '.claude\scripts'
Merge-CodeForgeDir '.codex\skills'
Merge-CodeForgeDir '.codex\skills' '.agents\skills'
Merge-CodeForgeDir '.gemini\skills'

Write-Host ''
Write-Host '  ====================================================' -ForegroundColor Green
Write-Host '    ✅ CodeForge 部署完成！' -ForegroundColor Green
Write-Host '  ====================================================' -ForegroundColor Green
Write-Host ''
Write-Host '  下一步：' -ForegroundColor Cyan
Write-Host '    1. 启动 Claude Code / Codex CLI / Gemini CLI'
Write-Host '    2. 输入 /ai-spec  开始描述你的需求（默认主调度）'
Write-Host '    3. 或 /deep-research  做技术选型 / 领域调研'
Write-Host '    4. 或 /dev-env-scan  为新项目做环境画像'
Write-Host ''
Write-Host '  MCP 配置（可选，提升调研能力）：'
Write-Host '    参考 deploy/mcp-config.template.json'
Write-Host ''
