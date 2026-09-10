param([string]$Compiler = '', [string]$Output = '')
$ErrorActionPreference = 'Stop'
$template = Split-Path $PSScriptRoot -Parent
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..'))
if (!$Compiler) { $Compiler = Join-Path $repo 'build/zanc.exe' }
if (!$Output) { $Output = Join-Path $repo 'build/legend-game' }
$Output = [IO.Path]::GetFullPath($Output)
if ($Output.StartsWith($template + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or $Output -eq $template) { throw 'Build output must be outside the template source directory' }
New-Item -ItemType Directory -Force -Path $Output | Out-Null
$sources = @(
    'main.zan', 'Spec.zan', 'Tables.zan', 'Data.zan', 'Game.zan',
    'Save.zan', 'Net.zan', 'Shell.zan', 'PageMap.zan', 'PageMapInner.zan',
    'PageBag.zan'
) | ForEach-Object { "$template/src/$_" }
& $Compiler @sources --auto-stdlib -o "$Output/Legend.exe"
if ($LASTEXITCODE -ne 0) { throw 'Legend compilation failed' }
foreach ($dir in @('assets', 'skins', 'data')) { Copy-Item -LiteralPath "$template/$dir" -Destination $Output -Recurse -Force }
Write-Host "Built: $Output/Legend.exe"
