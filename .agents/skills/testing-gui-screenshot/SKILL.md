---
name: testing-gui-screenshot
description: How to make sure a screenshot actually shows the Zan GUI window under debug (gallery, probe, ZanIDE, any stdlib Gui app) on Windows or Linux — anchor on the launched PID, capture per-window, verify before judging. Use whenever taking a screenshot to visually verify or debug a running Zan program, when a screenshot came back showing the wrong window, or before judging pixels after a UI interaction.
---

# Capturing the RIGHT window when visually debugging a Zan GUI app

## The rule

Every screenshot must be anchored to the **PID of the process you launched**, and
captured **per-window** — never a full-screen/desktop grab that you then hunt
through. The screen shows whatever is frontmost; your debug target usually is
not. A full-screen grab routinely captures the user's editor, a terminal, the
agent harness window, or a **stale instance of the same program from a previous
run** — and pixels from the wrong window read as "the app is broken" or "the
fix works".

## Discipline, in order

1. **Record the PID at launch.** Windows: `Start-Process ... -PassThru`
   (`.Id`), or `Get-Process <name> | ? { $_.Path -like "*_scratch*" }`. Linux
   bash: `echo $!` right after the background launch, or `pgrep -f <exact
   binary path>` (match the path, the bare name is shared).
2. **Kill your previous run first.** Relaunching a probe with the same window
   title while the old process is still alive gives you two same-titled
   windows; a title-based capture then silently grabs the stale one. Kill only
   PIDs you launched (never `Stop-Process -Name ZanIDE` / `pkill zanide` — the
   user has their own instance open).
3. **Confirm the window exists before capturing.** If the launch died (log
   empty, process gone), a screenshot shows only the desktop — that is how
   "screenshot of the wrong window" happens. Windows:
   `Get-Process -Id <pid>` must be alive and have a `MainWindowTitle`; Linux:
   `wmctrl -lp` and grep your pid. Expect exactly one window; more than one is
   the stale-instance case from step 2.
4. **Capture that window, not the screen.** Recipes below. A per-window capture
   works even when the window is occluded or in the background.
5. **Verify the capture before judging any pixels.** Open the PNG and check it
   shows the target: its **title bar is visible in the image** and the state you
   meant to capture is present (the change you just made, the page you just
   opened). A shot without the target's title bar, or showing a
   terminal/desktop, is a failed capture — **discard and recapture, never
   interpret it**.
6. **One shot = one moment.** Focus and hover change pixels: a cursor left
   hovering a card renders its hover style and can masquerade as selection;
   bringing a window to front changes its active title bar. Capture *after*
   moving the synthetic cursor away from what you are judging, and prefer
   before/after pairs around a single interaction over one absolute shot.

## Windows

Use `scripts/win-shot.ps1` (in this skill's directory) — captures one window by
PID (preferred) or title regex via `PrintWindow(PW_RENDERFULLCONTENT)`, which
grabs the window's own composed surface **even if it is occluded or
background**:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill>/scripts/win-shot.ps1 `
  -ProcId 25156 -Out _scratch\shot.png        # or -Title "Zan GUI Components"
# -> CAPTURED pid=... hwnd=0x... rect=2399x1088 title='...' -> _scratch\shot.png
```

Verified behaviour (2026-09): prints what it captured so you can check the
title; `NO-WINDOW` (exit 2) when the pid has no visible window; `AMBIGUOUS`
(exit 3) listing every matching pid+hwnd+title when a title matches several
windows — **pick a PID and retry, never let it guess**. ASCII-only source,
works under PowerShell 5.1's BOM-less-ANSI reading; the title regex does match
CJK titles.

- `CopyFromScreen` (screen-rect grab) is only acceptable when you have
  independently verified the target is foreground and unoccluded for the whole
  shot; it grabs whatever overlaps that rect. Don't trust pixels from a run
  where the target lost focus.
- If your harness has app-scoped capture (e.g. ZCode computer-use:
  `get_app_state(app_ref={pid}, include_screenshot=true)`, after
  `list_windows`), that is window-scoped and background-safe — prefer it and
  skip the script. The harness's full-`screenshot` tool is a display grab: last
  resort only.

## Linux (X11)

```bash
wmctrl -lp                                   # hwnd pid host -> title
xdotool search --allpid <pid>                # hwnds of that pid
import -window <hwnd> -strip _scratch/shot.png   # ImageMagick, per-window
# fallback without ImageMagick: xwd -id <hwnd> -out _scratch/shot.xwd
```

`import -window <hwnd>` captures that window even when partially overlapped;
`import -window root` / `scrot` are display grabs — same rules as Windows'
`CopyFromScreen`.

## Zan specifics

- The window title is the first argument of the form constructor
  (`App.CreateDark("title", w, h)`, `stdlib/Gui/App.zan`) — it is known before
  launch, so title checks are exact-match-able. The gallery's window is
  `"Zan GUI Components"`.
- A Zan GUI window is a normal top-level HWND of the exe's own process —
  PID anchoring just works; there is no separate window process.
- Zan windows keep painting only while their event loop runs (e.g. the IDE
  stalls when idle) — a "blank/stale" capture of a stalled app means the app,
  not the capture, needs a nudge; see the `testing-zanide-uidriver` skill.

## Failures this skill exists for (each one has actually happened)

- Screenshotting the display and finding "the app is gone/wrong" — the app had
  failed to launch, or the grab showed the editor/terminal on top.
- Two probe instances alive with the same title; pixels judged on the stale one.
- `CopyFromScreen` of the target's rect while it was background — the PNG
  contains whichever window happened to overlap.
- Judging hover/selection state on a shot taken with the synthetic cursor still
  parked over the widget.
