---
name: zan-development
description: The fixed workflow for writing or changing Zan code with the Zan SDK — orient, look the API up, edit, compile, run — plus the language facts and the exact commands. Use it for any Zan coding task.
---

# Writing Zan code

## 0. Orient (one call)

MCP connected: `zan_start_here` → layout, entry point, build/test commands,
which optional tools this installation actually has.
No MCP: read `AGENTS.md` and `docs/AI_ONBOARDING.md` at the SDK root.

## 1. Locate before you read

* `search_text(query)` for a symbol or string; `find_files(pattern)` for a name.
  Both answer with `path:line`, which is the address you edit at.
* `read_file(path, from_line, max_lines)` — the numbered window around that
  line, not the file. (`offset`/`limit` reads bytes, for binaries.)

Reading a whole tree "to understand the project" is what `zan_start_here` and
the symbol index exist to replace — and reading the same window twice is worse
still: a tool result stays true until you change it, so use the one you have
instead of asking again.

## 2. Look up every API you are about to call

```
zan_api_search("File.ReadAllText")   → static string ReadAllText(string path)
zan_api_search("Http")               → the surface of the HTTP client/server
zan_example()                        → catalog of shipped, build-verified programs
zan_example("server-mvc")            → files of one of them, verbatim
```

Copy the shape from an example; adapt names, not structure. Guessing a
signature that "should" exist is the top cause of a broken build here.

Without MCP the same index is a file: `knowledge/symbols.json` next to the SDK
(one JSON record per line: name, kind, file, line, sig) — grep it.

## 3. Language facts that decide whether it compiles

* Static types, C#-like syntax, **ARC** — no GC and no manual free.
* Static members are reached through the class: `Foo.Bar()`, including inside
  `Foo` itself.
* Nullability is enforced: `x.Get("k").Put(...)` is an error when `Get` may
  return null. Store it, check for null, then use it (or use `?.`).
* `await` only inside an `async` member; the scheduler is real, not cooperative
  sugar.
* Platform-specific code: `#if WINDOWS` / `#else`; native symbols via
  `[DllImport("crt", EntryPoint = "...")]`.
* Strings concatenate with `+`; `Convert.ToString(n)` for numbers.

## 4. Edit

`edit_file(path, old, new)` (MCP) replaces an exact snippet in place — the
default, because it needs the snippet and not the file. `old` must occur once,
so extend it with neighbouring lines until it is unique; the call refuses a
fuzzy match rather than guessing. `write_file(path, content)` is for a new file
or a wholesale replacement.

Make the whole change in one call per site — edit, re-read, edit the next line
is how a five-minute fix becomes twenty. Match the surrounding style; prefer
extending an existing class over adding a parallel one.

## 5. Compile — every time, before any claim

```
zan_build_project()            # whole project, structured diagnostics
zan_compile(content)           # one snippet in an isolated dir
```

Direct:

```
<ZAN_SDK>/toolchain/zanc <entry.zan> --auto-stdlib -o build/app
<ZAN_SDK>/toolchain/zanc <entry.zan> --auto-stdlib --publish -o app   # release
<ZAN_SDK>/toolchain/zanc <entry.zan> --auto-stdlib --check-leaks -o build/app
```

Read `diagnostics[]` (file, line, column, message) and fix from the first one
down: later errors are usually fallout.

## 6. Run / test

`run_command("build/app")`, or the project's own test entry point if it has one
(`zan_start_here` reports it when present). In the SDK repo itself the tiers are
`scripts/test.ps1 smoke | standard | full` — take the smallest tier that covers
the change.

## 7. Evidence discipline (the anti-rework rules)

Two real projects (a 420-file gateway port, a 634-file WinForms port) lost days
to the loops below. These rules are what closed them.

**Success must leave an artifact on disk.** A claim of "the repro passed" or
"the server responded" is false until a log file with content, a screenshot, or
a marker file proves it. One project burned hours on 8 repro variants whose
logs were all empty — the "success" was assumed, then "fixes" were built on it.
Before you treat a run as evidence, check the log is non-empty; before you fix
based on a failure, make sure the failure is the one you think.

**Compile after every coherent unit — not in batches.** A 600-file port that
compiles only once per batch spends a whole unverified epoch per batch; when a
build breaks there, every edit since the last green build is suspect at once.
Compile per module/window and fix forward immediately. If a build is blocked by
a file you must not touch (concurrent session, frozen stdlib), surface the
blocker and stop changing that batch — do not "keep editing, compile later."

**One command template, kept correct.** In one session `zanc` failed 4 times in
a row with `cannot open file 'src/App.zform'` because the working directory had
drifted to `build/`. Commands that compile your project are project assets:
keep the exact working form in the project's AGENTS.md/README and always paste
it, including the `cd`, instead of retyping it from memory. Same for tool
quirks: a `File has not been read yet` error is a full wasted round trip — read
the window first, then edit.

**Search the file, not the memory of the name.** 5 consecutive greps for a
class that turned out to be named differently is 5 lost rounds. `find_files`
for the file name first, read it, and take the API shapes you need from a
sibling file that already does the same thing.

**Claiming a compiler defect has a price tag.** If code compiles silently but
is wrong (e.g. an `int` returned from a stdlib call assigned to an object
variable, then dereferenced — crashes with a poison-value pointer), the defect
itself is in scope: reduce it to a minimal snippet with `zan_compile` and
report it. Do not spend session hours tiptoeing around an unreported defect;
each later session re-pays the same discovery cost.

## 8. Report

State the command you ran and what it printed. Separate "compiled", "ran" and
"not verified". Never present an unverified change as working.

## Traps

* Do not invent APIs — look them up (step 2). A stdlib method's real return
  type is part of the API: check it before assigning to anything but `var`
  (assigning an `int` to an object variable once crashed a port on its first
  request — silent at compile time, poison-value pointer at runtime).
* Do not hard-code hosts, ports, credentials or business limits: they belong in
  the project config (`config/app.json` for server projects), read at run time.
* Do not hand-draw GUI widgets: use the standard library's components
  (`zan_example("gui-window")`, `zan_example("gui-form-components")`).
* Do not leave probes in the project: `_scratch/` for throwaway work, `build/`
  for output.
* If the compiler itself looks wrong, reduce it to a minimal snippet with
  `zan_compile` and report the snippet — do not contort the code around it.
