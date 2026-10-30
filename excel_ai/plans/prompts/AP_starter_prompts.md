# Air pollution: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`AP_module_prompt.md`](AP_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/plans/prompts/AP_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/plans/prompts/` is not in your checkout, double-click `SyncRepo.bat` first; if it is still missing, paste the whole of `AP_module_prompt.md` instead (Appendix A of the Word guide).

## Starter queries

One at a time, after the starter (or in a new session with the two files attached):

- Build it, starting from what already exists

```
@AGENTS.md @excel_ai/plans/prompts/AP_module_prompt.md Build the module, starting from what already exists: the v0.3 scaffold in `excel_ai/air_pollution/`, the extracts in `data_old/air_pollution/legacy_459/`, `Equations_v1_0.md`, the plan `excel_ai/plans/Air_pollution.md` and the distribution module's patterns. Do phase 0 only, then stop and report.
```

- Check it against legacy outputs

```
Check it against legacy outputs: compare the air pollution module's results for Egypt with legacy 465's cached values, year by year, both scenarios. List every difference above 0.1% with its cause: a registered bug fix, a replicated issue, or unexplained (then find the cause).
```

- Produce a short PowerPoint, following the norms of the other documents

```
Produce a short PowerPoint (about 6 slides) on the air pollution module: what it does, how it links to the other modules, the results for Egypt against legacy, the bugs fixed and issues replicated (codes), open decisions. Follow the norms of the other documents: the CPAT-AI Overview deck (`excel_ai/CPAT-AI_Overview_v<version>.pptx`, builder `excel_ai/mitigation/presentation/build_deck.js`), counts taken from the register, `NORMS.md` 5. Save it as `excel_ai/CPAT-AI_AirPollution_Overview_v<version>.pptx`.
```

- Check that every bug found is in the registers

```
Check that every bug and issue you found is in the register (`excel_ai/mitigation/issues_register.py`, `make_legacy_fixes.py`), with its code, legacy cells and cross-references; regenerate `excel_ai/BUGS.md`, `excel_ai/ISSUES.md` and the tracker, and list what you added.
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
