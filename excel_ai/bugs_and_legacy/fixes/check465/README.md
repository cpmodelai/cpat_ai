# Legacy CPAT 1.0pre_465: the CPAT team's bug fixes, checked

`CPAT 1.0pre_465_NoPropData.xlsb` (in `../../workbooks/`) is the latest legacy file from the CPAT team (2026-10-22). The team marked 62 of our legacy bugs (and the issues I18, I29) as fixed. Each fix was checked cell by cell against the bug's cell plan (baseline cell, filled range, policy copy) on 2026-10-22. (Until v0.8.3 these files and a second copy of the legacy file were in `excel_ai/bugsfixed/`, retired in v0.8.4.)

| File | What it is |
|---|---|
| `FixedBugsToConfirm.txt` | The team's list, split into **Confirmed fixed** (52) and **Fixed with caveats** (12: 8 bugs with caveats, L62 and L63 not fixed, and the issues I18 and I29), with the caveat of each |
| `legacy465_check.json` | The same result for code: read by the register (`../../register/register.py`) |

Where the result shows (v0.8.4): column "Legacy 465" of every legacy bug in `Legacy_CPAT_Bugs_v<version>.docx` (section 2; the fixed bugs in Appendices A and B), the tracker `Tracking_Legacy_Bugs_v<version>.xlsx` (tab Bugs: column Fixed = Solved, In progress, No; column Legacy 465) and `BUGS.md`.
