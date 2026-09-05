$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

# SkinBuilder is a pure Gui stdlib program (stdlib widgets + Chart component
# only), so the static Win32 GUI runtime is enough -- same recipe as
# scripts/build_charts.ps1. zanc auto-includes the Chart component sources by
# namespace when the tool `using Gui.Component.Chart;`s them.

Write-Output "[1/2] Building native GUI runtime (Win32, static, mingw ABI)..."
clang --target=x86_64-w64-windows-gnu -O2 -DZAN_GUI_STATIC `
    -c src\runtime\gui_runtime.c -o build\zan_gui_skinbuilder_gnu.o
if ($LASTEXITCODE -ne 0) { throw "RUNTIME_COMPILE_FAILED" }
llvm-ar rcs build\libzan_gui_skinbuilder_gnu.a build\zan_gui_skinbuilder_gnu.o
if ($LASTEXITCODE -ne 0) { throw "RUNTIME_LIB_FAILED" }

Write-Output "[2/2] Compiling and linking skinbuilder.exe..."
$files = @()
$files += (Get-ChildItem stdlib\Gui\*.zan).FullName
$files += (Get-ChildItem stdlib\Gui\Widget\*.zan).FullName
$files += (Get-ChildItem stdlib\Gui\Component\Chart\*.zan).FullName
$files += (Get-ChildItem tools\skinbuilder\*.zan).FullName

$zanArgs = @()
$zanArgs += $files
$zanArgs += @("-o", "build\skinbuilder.exe", "--subsystem", "windows")
$zanArgs += @("--libpath", "build", "--link-lib", "zan_gui_skinbuilder_gnu")
$zanArgs += @("--link-lib", "ws2_32", "--link-lib", "mswsock")
$zanArgs += @("--link-lib", "psapi", "--link-lib", "advapi32")
$zanArgs += @("--link-lib", "dwmapi", "--link-lib", "gdi32", "--link-lib", "imm32")
$zanArgs += @("--link-lib", "user32", "--link-lib", "rpcrt4")

& build\zanc.exe @zanArgs
if ($LASTEXITCODE -ne 0) { throw "ZANC_COMPILE_FAILED" }

Write-Output "SKINBUILDER_BUILD_OK build\skinbuilder.exe"
