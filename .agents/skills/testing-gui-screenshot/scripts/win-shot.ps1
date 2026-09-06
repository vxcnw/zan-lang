# Capture ONE top-level window by PID (preferred) or title regex, even if it is
# occluded or in the background. Uses PrintWindow(PW_RENDERFULLCONTENT), which
# grabs the window's own composed surface - unlike CopyFromScreen, which grabs
# whatever happens to be on top of that screen rect.
# Usage:  powershell -File win-shot.ps1 -ProcId 12345 -Out shot.png
#         powershell -File win-shot.ps1 -Title "Zan GUI Components" -Out shot.png
# Prints the captured HWND and title so the caller can verify WHAT was captured.
# ASCII only: PowerShell 5.1 reads BOM-less .ps1 as ANSI/GBK.
param(
  [int]$ProcId = 0,
  [string]$Title = "",
  [Parameter(Mandatory=$true)][string]$Out
)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinShot {
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc cb, IntPtr lp);
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lp);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint pid);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder sb, int max);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hWnd, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  public struct RECT { public int L, T, R, B; }
}
"@
[WinShot]::SetProcessDPIAware() | Out-Null
$found = New-Object System.Collections.ArrayList
$cb = [WinShot+EnumWindowsProc]{
  param($h, $lp)
  if (-not [WinShot]::IsWindowVisible($h)) { return $true }
  $wpid = 0
  [WinShot]::GetWindowThreadProcessId($h, [ref]$wpid) | Out-Null
  if ($ProcId -ne 0 -and $wpid -ne $ProcId) { return $true }
  $sb = New-Object System.Text.StringBuilder 512
  [WinShot]::GetWindowText($h, $sb, 512) | Out-Null
  $t = $sb.ToString()
  if ($Title -ne "" -and $t -notmatch $Title) { return $true }
  [void]$found.Add(@{ H = $h; Pid = $wpid; Title = $t })
  return $true
}
[WinShot]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
if ($found.Count -eq 0) { Write-Output "NO-WINDOW pid=$ProcId title='$Title'"; exit 2 }
if ($found.Count -gt 1) {
  Write-Output ("AMBIGUOUS {0} matches - pick a pid and retry:" -f $found.Count)
  foreach ($w in $found) { Write-Output ("  pid={0} hwnd=0x{1:X} '{2}'" -f $w.Pid, $w.H.ToInt64(), $w.Title) }
  exit 3
}
$w = $found[0]
$r = New-Object WinShot+RECT
[WinShot]::GetWindowRect($w.H, [ref]$r) | Out-Null
$wd = $r.R - $r.L; $ht = $r.B - $r.T
if ($wd -le 0 -or $ht -le 0) { Write-Output "BAD-RECT hwnd=0x{0:X}" -f $w.H.ToInt64(); exit 4 }
$bmp = New-Object System.Drawing.Bitmap $wd, $ht
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
$ok = [WinShot]::PrintWindow($w.H, $hdc, 2)  # 2 = PW_RENDERFULLCONTENT
$g.ReleaseHdc($hdc); $g.Dispose()
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
if (-not $ok) { Write-Output "PRINTWINDOW-FALSE (saved anyway - inspect the png)" }
Write-Output ("CAPTURED pid={0} hwnd=0x{1:X} rect={2}x{3} title='{4}' -> {5}" -f $w.Pid, $w.H.ToInt64(), $wd, $ht, $w.Title, $Out)
