# Distribution: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`Distribution_module_prompt.md`](Distribution_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/core/prompts/Distribution_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/core/prompts/` is not in your checkout, double-click `SyncRepo.bat` first; if it is still missing, paste the whole of `Distribution_module_prompt.md` instead (Appendix A of the Word guide).

## Starter queries

One at a time, after the starter (or in a new session with the two files attached):

- Review what already exists (the module is built)

```
@AGENTS.md @excel_ai/core/prompts/Distribution_module_prompt.md The module exists (v0.1.3). Review it against `NORMS.md` section 9 and its README, run `check_distribution.py`, and report what is missing. Do phase 0 only, then stop and report.
```

- Run a scenario end to end

```
Change the live carbon price in the mitigation prototype to <x> USD/tCO2 in <year>, update the distribution module from it, and show me the effect by decile and the Gini change against the current values.
```

- Check it against legacy outputs

```
Check it against legacy outputs: compare the distribution module's results for Egypt with legacy 465's cached values, decile by decile in the analysis year (overall, urban, rural), and the MTOutputs distribution results. List every difference above 0.1% with its cause: a registered bug fix, a replicated issue, or unexplained (then find the cause).
```

- Produce a short PowerPoint, following the norms of the other documents

```
Produce a short PowerPoint (about 6 slides) on the distribution module: what it does, how it links to the other modules, the results for Egypt against legacy, the bugs fixed and issues replicated (codes), open decisions. Follow the norms of the other documents: the CPAT-AI Overview deck (`excel_ai/CPAT-AI_Overview_v<version>.pptx`, builder `excel_ai/mitigation/docs/presentation/build_deck.js`), counts taken from the register, `NORMS.md` 5. Save it as `excel_ai/CPAT-AI_Distribution_Overview_v<version>.pptx`.
```

- Check that every bug found is in the registers

```
Check that every bug and issue you found is in the register (`excel_ai/bugs_and_legacy/register/issues_register.py`, `make_legacy_fixes.py`), with its code, legacy cells and cross-references; regenerate `excel_ai/core/BUGS.md`, `excel_ai/core/ISSUES.md` and the tracker, and list what you added.
```

- Adjust what you do not like or what is missing

```
I found I don't like format (x) / you are lacking output (y): please adjust. Change the builder, not the built workbook; rebuild, rerun the check and show me the result.
```

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
@AGENTS.md @excel_ai/core/prompts/Distribution_module_prompt.md We are at phase <n>. Read the bottom of CAVEATS.md and the last report, then do phase <n> only and stop.
```

Then save to GitHub: close the workbooks and double-click `SyncRepo.bat` in the repo folder.
