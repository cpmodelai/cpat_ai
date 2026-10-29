# Air pollution: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`AP_module_prompt.md`](AP_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/plans/prompts/AP_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/plans/prompts/` is not in your checkout yet (the branch is not merged), sync first; if it is still missing, paste the whole of `AP_module_prompt.md` instead (Appendix A of the Word guide).

## Next phases

```
Go ahead with phase 1.
```
```
Go ahead with phase 2.
```
```
Go ahead with phase 3.
```
```
Go ahead with phase 4.
```
```
Go ahead with phase 5.
```

## Example follow-ups

Answer the decisions it asks for (example only: use your own decisions):

```
Decisions: B1 replicate as an issue for now and show me the effect of the fix on Egypt deaths and wel.air; B14 remove the "Transfer from OECD" option; I-d replicate as an issue. Unit damages from scenario 1 as legacy; compute 2041. Record these in the register, then go ahead with phase 1.
```

Check the units at the boundary:

```
Show me, for Egypt 2022, the emissions read from Mitigation section 15 in kt and the tonnes the module uses, pollutant by pollutant, next to the legacy 465 values.
```

Ask for an explanation:

```
Explain in plain words, with the Egypt numbers for 2030, how emissions become deaths and then the value of averted deaths in this module.
```

When a check fails:

```
check_ap.py fails on <name of the check>. Find the cause, fix the builder (not the check), rebuild and run the check again. Tell me what was wrong.
```

Before you save:

```
Show me the changes before you save them. List every file you changed and why.
```

Stop for the day, and resume later in a new session:

```
Stop here. Add the CAVEATS.md entry and the TODO items for what is left, and tell me which phase is next.
```
```
@AGENTS.md @excel_ai/plans/prompts/AP_module_prompt.md We are at phase <n>. Read the bottom of CAVEATS.md and the last report, then do phase <n> only and stop.
```

Then save to GitHub: close the workbooks and double-click `SyncRepo.bat` in the repo folder.
