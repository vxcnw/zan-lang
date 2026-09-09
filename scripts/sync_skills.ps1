# sync_skills.ps1 — 三份 skills 副本的漂移报告与全局同步。
#
# skills 有三份副本（见 AGENTS.md 规则 13）：
#   1. 工作区 .agents\skills\          —— 活源（LF 换行），zan-lang 仓库内 zcode 自动优先
#   2. tools\ai_pack\skills\           —— 发布变体（人工维护的措辞适配：去仓库专属节、
#                                         description 尾加"仓库内同名项目级版本优先"提示）
#   3. C:\Users\QQ\.agents\skills\     —— 发布包的字节副本，zcode 在仓库外使用
# publish_ide.ps1 再把 2 复制进 dist\ai\skills\ 随 SDK 发布。
#
# 用法：
#   scripts\sync_skills.ps1             # 漂移报告（1 vs 2，忽略 CRLF 差异）
#   scripts\sync_skills.ps1 -SyncGlobal # 把 2 字节复制到 3（发布变体同步到全局）
#
# 报告只定位漂移，不自动合并：工作区→发布包的移植需要人工措辞适配
# （剥离仓库专属节、适配仓库内路径引用），机器自动覆盖会毁掉变体。

param([switch]$SyncGlobal)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$ws   = Join-Path $root '.agents\skills'
$pack = Join-Path $root 'tools\ai_pack\skills'
$globalDir = Join-Path $env:USERPROFILE '.agents\skills'

function Read-TextLf($path) {
    if (-not (Test-Path $path)) { return $null }
    return ((Get-Content $path -Raw -Encoding UTF8) -replace "`r`n", "`n")
}

if ($SyncGlobal) {
    if (-not (Test-Path $pack)) { throw "pack missing: $pack" }
    New-Item -ItemType Directory -Force -Path $globalDir | Out-Null
    Get-ChildItem $pack -Directory | ForEach-Object {
        $dst = Join-Path $globalDir $_.Name
        if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
        Copy-Item $_.FullName $dst -Recurse -Force
        Write-Output "SYNC_GLOBAL $($_.Name) -> $dst"
    }
    exit 0
}

# ---- 漂移报告：工作区(1) vs 发布包(2)，逐 skill 逐文件 ----
$wsSkills  = Get-ChildItem $ws  -Directory | ForEach-Object Name
$packSkills = Get-ChildItem $pack -Directory | ForEach-Object Name
$drift = 0
foreach ($s in ($wsSkills + $packSkills | Sort-Object -Unique)) {
    $wsDir  = Join-Path $ws $s
    $packDir = Join-Path $pack $s
    if (-not (Test-Path $packDir)) {
        Write-Output "ONLY_WS   $s  (发布包没有此 skill —— 决定是否要随 SDK 发布)"
        $drift++
        continue
    }
    if (-not (Test-Path $wsDir)) {
        Write-Output "ONLY_PACK $s  (工作区没有此 skill —— 疑似只在发布侧维护，检查是否该回移)"
        $drift++
        continue
    }
    $wsFiles  = @(Get-ChildItem $wsDir -Recurse -File | ForEach-Object { $_.FullName.Substring($wsDir.Length + 1) })
    $packFiles = @(Get-ChildItem $packDir -Recurse -File | ForEach-Object { $_.FullName.Substring($packDir.Length + 1) })
    foreach ($f in (@($wsFiles) + @($packFiles) | Sort-Object -Unique)) {
        $a = Read-TextLf (Join-Path $wsDir $f)
        $b = Read-TextLf (Join-Path $packDir $f)
        if ($null -eq $b) { Write-Output "MISSING   $s/$f  (发布包缺此文件)"; $drift++; continue }
        if ($null -eq $a) { Write-Output "EXTRA     $s/$f  (发布包多出此文件)"; $drift++; continue }
        if ($a -ne $b)    { Write-Output "VARIANT   $s/$f  (预期内的变体差异或未移植的更新 —— 人工比对)" ; $drift++ }
    }
}
if ($drift -eq 0) { Write-Output 'IN_SYNC: 工作区与发布包逐文件一致（忽略 CRLF）' }
else { Write-Output "`n$drift 处差异。规则 13：验证过的 skill 更新必须同一提交同步到发布包，然后 -SyncGlobal。" }
