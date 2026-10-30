# Fix the prototype bugs M15-M22 (found by Coded CPAT), then check legacy

Written 2026-10-29 (user request). These eight prototype bugs were found while Coded CPAT (`coded/`) replicated Excel-AI number for number. **Status: done in v0.9.2 / Distribution 0.1.4** (M15-M17, M19-M22 fixed; M18 withdrawn by the user as not a bug: the legacy bus-electricity method; M17 basis decided by the user: insurance on the BEV price, ICEV maintenance and distance). The rule changed the same day: prototype bugs are never put into Coded CPAT; Python has the correct formula and the prototype is fixed to align (NORMS 0, rule 6). This file is the brief for the AI that fixes them in the prototype. The register entries are in `excel_ai/legacy/register/issues_register.py` (`OPEN_PROTO_BUGS`), listed in [`../BUGS.md`](../BUGS.md) section 2.

Read first: [`../../NORMS.md`](../NORMS.md) (section 0, the replication rule; sections 3-6 on building, checks, versions and the caveats log) and [`../mitigation/README.md`](../../mitigation/README.md) (build and check commands).

## Part 1. Fix each bug in the prototype

Every formula comes from the builder `excel_ai/mitigation/build.py`; never edit a workbook by hand. Row numbers are those of `CPAT-AI-Mitigation-Prototype_v0.9.1.xlsm`, sheet Mitigation (Distribution: `CPAT-AI-Distribution-Prototype_v0.1.3.xlsm`, sheet Distribution). The builder's row ids (`T(4555, ...)`) are the legacy rows; find a row by its variable name.

| Code | Bug | Where | Fix | Effect |
|---|---|---|---|---|
| M15 | VAT on efficient prices at the 2022 general rate in every year | Section 18: rows 8753-8768 (`vatext`) and 8943-8954 (`vat.cost`), column D; defined name `VatGen` = `Inputs!$BB$156` (`build.py`: `'VatGen'` near line 10161, the `vatext`/`vat.cost` writer near line 13503) | **User assumption 2026-10-29: VAT data run up to the final historical year (LastHistPriceYear) and are passed forward unless we know otherwise.** Make the rate a year row: VAT_WEO of the column year while it is a historical year (the `vry<year>` columns of the price block hold it), the last historical year's rate after it. Column D keeps only the consumer flag (x the household share of the oil product, Inputs column U); the formulas multiply by the year row. | Egypt: none (VAT_WEO 14% throughout). Other countries: VAT and efficient prices from 2025 at the latest rate. |
| M16 | Freight BEV feebate valued at the ICEV truck's distance | Row 4197 `trfbvfb.fre.bev` = `(0 - pivot) x rate / Million x trdkmfrei.fre.ice` | Use the freight BEV distance row (as the passenger BEV feebate, row 4138, uses `trdkmpasb.pas.bev` and the 2-3 wheeler one, row 4219, `trdkmcycb.cyc.bev`). | Engineer road model with freight feebates only. |
| M17 | Plug-in hybrid cost mixes BEV capital cost with ICEV insurance and maintenance | Row 4175 `trtcfp.pas.phv` (`build.py` near line 2265, legacy row 4555) | One basis for every PHEV cost component: PHEV purchase price where the data have one, else BEV; insurance and maintenance on that price; the distance as now. If the intended basis is unclear, ask the user (and the CPAT team) before changing it, and record the answer with the bug. | Engineer road model (PHEV choice) only. |
| M18 | Bus electricity scaled by the bus energy of every fuel | Row 4522 `trbusel.bus.ecy`, column D = `$D3816+$E3816+$F3816+$G3816` (`build.py` near line 2776, legacy row 5318) | Column D = `$G3816`, the electricity column of the base bus use, as the fuel rows 4517-4519 take their own column. | Bus electricity in the engineer road model. |
| M19 | Nominal GDP divided by a billion although WEO is in billions | Rows 7765-7766 `gdpn` (`build.py` near line 3397) | Drop `/Billion`; the unit is then LCU bn and USD bn nominal (fix the unit labels). Check every reader (none in Mitigation; look in MTOutputs and the other modules). | Output rows only. |
| M20 | World Bank gas prices read by position: LNG and Europe swapped | International prices, source WB (`build.py` `'WB'` near line 8295; `extract_data.py` `INT_SOURCES`) | Read each series by name: LNG = "Liquefied natural gas, Japan", Europe = "Natural gas, Europe". | Only with `IntEnerPricForeSource` = WB (Egypt: IMF). |
| M21 | Methane fee: marginal abatement price #DIV/0 where the curve exponent is 0 | Rows 8600-8606 `mfp` = `IF(a=0, 0, MIN(fee x gwp x on, (1/a)^(1/b)))` (`build.py` near line 13477) | `IF(a=0, 0, IF(b=0, fee x gwp x on, MIN(...)))`; the same in `check_full.py` near line 2614. | None in the current data. |
| M22 | Distribution: percentile recycling rows add a % row to amounts in local currency | Distribution 0.1.3 rows 599, 604, 609, 614, 619, 624 `hrec.<p25/p75>.<sample>` = `(pit + pui.tot + cts + tgt) / hcpc x 100` (`build.py` near line 14824) | Use the public investment amount per person of the sample (`pui.<sample>`, local currency), like `pit`, `cts`, `tgt`. | The 25th/75th percentile recycling and net rows where public investment is used. |

For each fix:

1. Change the builder (and its independent recalculation where one exists: `check_full.py`, `transport_model_ref.py`, `distribution_ref.py`), keeping the codes of the rows.
2. Build (`python build.py`, then the Distribution prototype) and run `python check_quick.py`; a full check (`check_full.py`) once all are done. Report every change of stored values (Egypt, scenarios 1-6) in the caveats log: which codes moved, and why.
3. Register the fix: move the item from `OPEN_PROTO_BUGS` to `MVP_BUGS` in `issues_register.py` (title, `found / fixed in` = `v0.9.1 (Coded CPAT) / v<new version>`, what happened, fix), then `python make_documentation.py` (BUGS.md, ISSUES.md, tracker, bugs document, Word documentation). Release as NORMS section 5 (new version; Mitigation and Distribution).
4. **Tell Coded CPAT** (NORMS 0, rule 6): add one line per fixed bug to `coded/TODO.md` ("Excel-AI v<version> fixed M<n>: Coded CPAT to follow"), so the replication changes in the same release. Do not change `coded/` yourself unless asked.

## Part 2. Check whether each bug is in legacy CPAT as well

Legacy: `CPAT 1.0pre_465_NoPropData.xlsb` (mitigation; the extracts in `data_old/mvp_legacy_extracts/` and `excel_ai/legacy/`) and the legacy distribution sheets. The prototype's builder comments give the legacy row of most prototype rows (`T(<legacy row>, ...)`, "legacy row ..." in the row notes).

For each of M15-M22:

1. **Does legacy have the same defect?** Find the legacy cells that compute the same quantity and compare the formula. M15: how legacy applies VAT in its efficient-price block; M16-M18: the engineer road model (legacy rows 4555, 5318 and the freight feebate rows); M19: legacy nominal GDP rows; M20: legacy `Prices_int` World Bank rows; M21: the methane block; M22: the legacy distribution percentile rows (if legacy has them; the prototype may have added them).
2. **If legacy has it:** look in the register for an existing legacy bug (`BUGS.md` section 1, `Tracking_Legacy_Bugs_v<version>.xlsx` tab Bugs, `Legacy_CPAT_Bugs_v<version>.docx`; search by row, variable and title).
   - Already registered: add the cross-reference (`SEE_ALSO` in `register.py`, both ways), and record whether legacy 465 fixed it (the check of the CPAT team's fixes: `excel_ai/legacy/fixes/check465/`; column "Legacy 465" in `BUGS.md`).
   - Not registered: register a new legacy bug (`L`, next free number) with its cell-level fix plan (`excel_ai/legacy/fixes/data`; NORMS 0 rule 3), priority and effect, cross-referenced to the M item. Check legacy 465 for whether it is fixed there.
3. **If legacy does not have it** (the prototype introduced it): say so in the M item's description ("not in legacy: introduced in v<version>").
4. Regenerate the register documents (`python make_documentation.py`) and log the result in `CAVEATS.md` (one entry: per bug, in legacy yes/no, registered as L<n> or new, fixed in 465 yes/no).

## Done when

- All eight fixed in the builder, built, quick and full checks PASS, released; `BUGS.md` lists M15-M22 as fixed.
- Part 2 answered for every bug and registered.
- `coded/TODO.md` has one line per fixed bug for Coded CPAT to follow.
- Committed and pushed to `main` (fast-forward; merge `origin/main` first if it moved).
