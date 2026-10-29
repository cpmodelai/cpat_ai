# Distribution: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`Distribution_module_prompt.md`](Distribution_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/plans/prompts/Distribution_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/plans/prompts/` is not in your checkout yet (the branch is not merged), sync first; if it is still missing, paste the whole of `Distribution_module_prompt.md` instead (Appendix A of the Word guide).

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

## Example follow-ups

Look at one result:

```
For Egypt, the live scenario, show me the total effect by decile (overall, urban, rural) and the Gini change, next to legacy 465's cached values, with the reason for each difference.
```

Check a legacy bug in the register:

```
Show me register item <code>: the legacy cells, what legacy computes, what the module computes and the effect on deciles 1 and 10. Is it a bug or an issue under NORMS.md section 0?
```

Change a distribution setting (the formula source is excel_ai/mitigation/build.py):

```
<describe the change>. Change it in excel_ai/mitigation/build.py, rebuild the prototype, rebuild the module, run check_distribution.py and show me the result.
```

When a check fails:

```
check_distribution.py fails on <name of the check>. Find the cause, fix the builder (not the check), rebuild and run the check again. Tell me what was wrong.
```

Before you save:

```
Show me the changes before you save them. List every file you changed and why.
```

Resume later in a new session:

```
@AGENTS.md @excel_ai/plans/prompts/Distribution_module_prompt.md We are at phase <n>. Read the bottom of CAVEATS.md and the last report, then do phase <n> only and stop.
```

Then save to GitHub: close the workbooks and double-click `SyncRepo.bat` in the repo folder.
