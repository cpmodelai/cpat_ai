# Transport co-benefits: starter and follow-up prompts

Short prompts to type into GitHub Copilot (Current checkout, Claude Opus, Interactive). The long instructions are in [`TCB_module_prompt.md`](TCB_module_prompt.md); Copilot reads them from the repo, so you never paste them. Send one prompt, read the report, then send the next.

## Starter (new session)

Type `@` to attach the two files, then:

```
@AGENTS.md @excel_ai/plans/prompts/TCB_module_prompt.md Follow these files. Do phase 0 only, then stop and report.
```

If `excel_ai/plans/prompts/` is not in your checkout, double-click `SyncRepo.bat` first; if it is still missing, paste the whole of `TCB_module_prompt.md` instead (Appendix A of the Word guide).

## Starter queries

One at a time, after the starter (or in a new session with the two files attached):

- Build it, starting from what already exists

```
@AGENTS.md @excel_ai/plans/prompts/TCB_module_prompt.md Build the module, starting from what already exists: the plan `excel_ai/plans/Transport_cobenefits.md`, the legacy extracts in `data_old/mvp_legacy_extracts/`, `transport_model_ref.py`, the typed values of Mitigation's tab FromTransportCB and the distribution module's patterns. Do phase 0 only, then stop and report.
```

- Check it against legacy outputs

```
Check it against legacy outputs: compare the transport co-benefits module's results for Egypt with legacy 465's cached values, year by year, both scenarios. List every difference above 0.1% with its cause: a registered bug fix, a replicated issue, or unexplained (then find the cause).
```

- Produce a short PowerPoint, following the norms of the other documents

```
Produce a short PowerPoint (about 6 slides) on the transport co-benefits module: what it does, how it links to the other modules, the results for Egypt against legacy, the bugs fixed and issues replicated (codes), open decisions. Follow the norms of the other documents: the CPAT-AI Overview deck (`excel_ai/CPAT-AI_Overview_v<version>.pptx`, builder `excel_ai/mitigation/presentation/build_deck.js`), counts taken from the register, `NORMS.md` 5. Save it as `excel_ai/CPAT-AI_TransportCobenefits_Overview_v<version>.pptx`.
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
