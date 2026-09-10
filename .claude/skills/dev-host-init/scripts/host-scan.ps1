#Requires -Version 5.1
# dev-host-init: host environment detection (Windows native PowerShell)
# NOTE: runtime-verified on Windows only (dev environment has no pwsh).
# Outputs a single JSON object to stdout, same schema as host-scan.sh.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File host-scan.ps1

[CmdletBinding()] param()
$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Test-Cmd($name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }
function Get-Ver($exe, $arg, $regex) {
    if (-not (Test-Cmd $exe)) { return $null }
    $out = & $exe $arg 2>$null | Select-Object -First 1
    if ($out -and $out -match $regex) { return $Matches[1] }
    return $null
}

# ---------- OS & shell ----------
$osName = "Windows"
$osVer = (Get-CimInstance Win32_OperatingSystem).Version
$arch = $env:PROCESSOR_ARCHITECTURE

# ---------- hardware ----------
$cpuObj = Get-CimInstance Win32_Processor | Select-Object -First 1
$cpuModel = if ($cpuObj) { "$($cpuObj.Name.Trim()) ($($cpuObj.NumberOfCores)C/$($cpuObj.NumberOfLogicalProcessors)T)" } else { $null }
$cpuCores = if ($cpuObj) { [int]$cpuObj.NumberOfLogicalProcessors } else { 0 }
$cs = Get-CimInstance Win32_ComputerSystem
$memGB = [math]::Round($cs.TotalPhysicalMemory / 1GB)
$pf = Get-CimInstance Win32_PageFileUsage | Select-Object -First 1
$swapGB = if ($pf) { [math]::Round($pf.AllocatedBaseSize / 1024) } else { 0 }

$gpuObj = Get-CimInstance Win32_VideoController | Select-Object -First 1
$gpu = if ($gpuObj) {
    $vramMb = if ($gpuObj.AdapterRAM) { [math]::Round($gpuObj.AdapterRAM / 1MB) } else { $null }
    [ordered]@{ vendor = ($gpuObj.Name -split ' ')[0]; model = $gpuObj.Name; vram_mb = $vramMb; driver = $gpuObj.DriverVersion }
} else {
    [ordered]@{ vendor = $null; model = $null; vram_mb = $null; driver = $null }
}

$disks = @(Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 -or $_.Free -gt 0 } | ForEach-Object {
    $total = [math]::Round(($_.Used + $_.Free) / 1GB)
    $free = [math]::Round($_.Free / 1GB)
    [ordered]@{ mount = "$($_.Name):"; total_gb = $total; free_gb = $free }
})

# ---------- languages ----------
$lang = [ordered]@{
    nodejs = Get-Ver node '--version' 'v?([\d.]+)'
    python = Get-Ver python '--version' '([\d.]+)'
    rust   = Get-Ver rustc '--version' 'rustc ([\w.]+)'
    go     = Get-Ver go 'version' 'go version go([\w.]+)'
    java   = Get-Ver java '-version' '"([\w.]+)"'
    dotnet = Get-Ver dotnet '--version' '([\d.]+)'
    r      = Get-Ver R '--version' 'R version ([\w.]+)'
}

# ---------- package managers ----------
$pm = [ordered]@{}
foreach ($m in 'npm','pnpm','yarn','bun','uv','conda','cargo','pip','winget','scoop','choco') {
    $v = Get-Ver $m '--version' '([\d][\w.]*)'
    $pm[$m] = if ($v) { $v } elseif (Test-Cmd $m) { 'installed' } else { $null }
}

# ---------- env managers ----------
$condaEnvs = @()
if (Test-Cmd conda) {
    $condaEnvs = @(conda env list 2>$null | Where-Object { $_ -and $_ -notmatch '^#' } | ForEach-Object { ($_ -split '\s+')[0] } | Where-Object { $_ })
}
$uvPythons = @()
if (Test-Cmd uv) {
    $uvPythons = @(uv python list 2>$null | Where-Object { $_ } | ForEach-Object { ($_ -split '\s+')[0] } | Where-Object { $_ -and $_ -notmatch '^-' } | Select-Object -First 10)
}

# ---------- proxy ----------
$proxyPorts = @()
foreach ($p in 1080, 7890, 7897, 8118, 10808, 8888) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $task = $client.ConnectAsync('127.0.0.1', $p)
        if ($task.Wait(500) -and $client.Connected) { $proxyPorts += "$p" }
    } catch { } finally { $client.Dispose() }
}

# ---------- network topology (init 时探测) ----------
$net = [ordered]@{
    vps_alias = $null; vps_ip = $null; frp_svc = $null
    nginx_server_name = $null; nginx_port = $null
    listen_ports = @()
}
# SSH config (OpenSSH): 解析 Host / HostName
$sshCfg = Join-Path $env:USERPROFILE '.ssh\config'
if (Test-Path $sshCfg) {
    $lines = Get-Content $sshCfg -ErrorAction SilentlyContinue
    $inBlock = $false
    foreach ($line in $lines) {
        if ($line -match '^\s*Host\s+') {
            if (-not $inBlock -and -not $net.vps_alias) {
                $net.vps_alias = ($line -replace '^\s*Host\s+', '').Trim() -split '\s+' | Select-Object -First 1
                $inBlock = $true
            } elseif ($inBlock) { break }
        } elseif ($inBlock -and $line -match '^\s*HostName\s+(.+)$') {
            $net.vps_ip = $Matches[1].Trim(); break
        }
    }
}
# frp service / nginx: Windows 无 systemctl & 通常无 nginx，留 null
# 端口扫描 (回环 listen)
$scanPorts = 22, 80, 443, 1080, 7890, 8787, 8765, 8767, 8090, 8000, 8080, 8443, 22022, 2222
foreach ($p in $scanPorts) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $task = $client.ConnectAsync('127.0.0.1', $p)
        if ($task.Wait(300) -and $client.Connected) { $net.listen_ports += "$p" }
    } catch { } finally { $client.Dispose() }
}

# ---------- codebase-memory-mcp ----------
$cbCli = Test-Cmd 'codebase-memory-mcp'
$cbCfg = $false
foreach ($f in "$env:USERPROFILE\.claude.json", "$env:USERPROFILE\.claude\settings.json", "$env:USERPROFILE\.codex\config.toml", "$env:USERPROFILE\.gemini\settings.json") {
    if (Test-Path $f) {
        if (Select-String -Path $f -Pattern 'codebase-memory' -Quiet -ErrorAction SilentlyContinue) { $cbCfg = $true; break }
    }
}
if ($cbCli) { $cbCfg = $true }

# ---------- output ----------
$out = [ordered]@{
    os = [ordered]@{ name = $osName; version = $osVer; arch = $arch }
    shell = 'powershell'
    hardware = [ordered]@{
        cpu_model = $cpuModel
        cpu_cores = $cpuCores
        memory_gb = $memGB
        swap_gb = $swapGB
        avx2 = $null
        gpu = $gpu
        disks = $disks
    }
    languages = $lang
    package_managers = $pm
    env_managers = [ordered]@{ conda_envs = $condaEnvs; uv_pythons = $uvPythons }
    proxy = [ordered]@{
        env_http = $env:HTTP_PROXY
        env_https = $env:HTTPS_PROXY
        open_local_ports = $proxyPorts
    }
    network = $net
    codebase_mcp = [ordered]@{ cli_available = $cbCli; mcp_configured = $cbCfg }
    tools = [ordered]@{
        git = (Get-Ver git '--version' 'git version ([\w.]+)')
        gh = (Test-Cmd gh)
        rg = (Test-Cmd rg)
        docker = (Test-Cmd docker)
    }
}

$out | ConvertTo-Json -Depth 6
