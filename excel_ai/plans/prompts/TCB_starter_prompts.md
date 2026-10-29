# Transport co-benefits: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`TCB_module_prompt.md`](TCB_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/plans/prompts/TCB_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/plans/prompts/` is not in your checkout yet (the branch is not merged), sync first; if it is still missing, paste the whole of `TCB_module_prompt.md` instead (Appendix A of the Word guide).

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
Decisions: B-c replicate as an issue (legacy uses 100% of the after-tax wage); B-d fix as a bug; B-e replicate as an issue. D5: gasoline and diesel only. D7: charts of vehicle-km, deaths, congestion and road damage; skip the historical scatter. D8: import the whole Tran_Elast table. Record these in the register, then go ahead with phase 1.
```

Ask for an explanation:

```
Explain in plain words, with the Egypt numbers for 2030, how the Legacy and Engineer modes differ and why legacy is inconsistent.
```

When a check fails:

```
check_tcb.py fails on <name of the check>. Find the cause, fix the builder (not the check), rebuild and run the check again. Tell me what was wrong.
```

Before you save:

```
Show me the changes before you save them. List every file you changed and why.
```

When it found something you did not expect:

```
Is this a legacy bug or a legacy issue under NORMS.md section 0? Show me the legacy cells. If unsure, treat it as an issue, replicate it and register it.
```

Stop for the day, and resume later in a new session:

```
Stop here. Add the CAVEATS.md entry and the TODO items for what is left, and tell me which phase is next.
```
```
@AGENTS.md @excel_ai/plans/prompts/TCB_module_prompt.md We are at phase <n>. Read the bottom of CAVEATS.md and the last report, then do phase <n> only and stop.
```

Then save to GitHub: close the workbooks and double-click `SyncRepo.bat` in the repo folder.
