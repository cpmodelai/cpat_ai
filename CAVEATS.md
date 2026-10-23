# CAVEATS - log of completed tasks

Log of every completed task in this repo: what was asked, what went in, what came out, and what the next person must know before building on it. One entry per completed task (or per workbook version increment). **Newest entry at the bottom.** Earlier entries may be edited to keep the log accurate (fix stale paths, mark a caveat resolved with the date and where, correct a mistake); the record of a task is not deleted. Paths in older entries are as they were at the time: the Egypt folders (`egypt/`, `egypt+mitigation/`) were removed on 2026-10-09 (commit f070c20; in git history) and `excel_ai_new/` is today's `excel_ai/` (README, "Removed folders").

The rule that every finished task gets an entry here, and the other bookkeeping that goes with it (workbook version log, task inventory, `TODO.md`), is in [`NORMS.md` section 6](NORMS.md#6-task-completion-caveats-log-and-bookkeeping). Repo map and key documents: [`README.md`](README.md).

## Entry template

Copy the block below to the end of the file and fill it in. Keep it short; point to the task spec, report or yaml notes for detail rather than repeating them.

```markdown
## YYYY-MM-DD - <task id / short name> (<version or increment, if any>)
- **Task:** what was asked and what was done (one or two sentences).
- **Inputs:** files, sheets/ranges, data sources, specs and prior versions used.
- **Outputs:** files created or changed (paths), version numbers, documents updated.
- **Caveats:** placeholders, assumptions, known gaps, deferred items, regression differences that were explained rather than zero, decisions still open. Write "None" only if there genuinely are none.
```

## Caveats recorded before this log existed

Earlier work was logged in the task documents themselves; they remain the detailed record:

- Kernel increments v0.3-v0.11 (Tasks E, A, B, C, K, D-scaffold, H, L): `notes` under `TASK-1` in `egypt/instructions/instructions-egypt.yaml` (removed 2026-10-09; in git history before commit f070c20) and each workbook's `Settings` version log.
- Process semi-elasticities (Task D): `egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` section 4 (in git history before commit f070c20).
- Gap list for the Egypt kernel: `egypt/instructions/EgyptTaskReference.md` (in git history before commit f070c20).
- LAMBDA/VBA distribution workbook: [`excel_ai/distribution/LESSONS_LEARNED.md`](excel_ai/distribution/LESSONS_LEARNED.md); Python Distribution module gaps vs Excel: [`excel_ai/distribution/README.md`](excel_ai/distribution/README.md).

---

## Entries

## 2026-10-02 - TASK-D: IPCC-based process semi-elasticities (values ready, not applied)
- **Task:** Derive documented, IPCC-based process-emission semi-elasticities ("half-elasticities") for the eight CBAM products of the industry kernel, to replace the undocumented v0.8 `Manual inputs` E40:F47 values. Values are final; applying them to a kernel increment is queued as `TODO.md` T1.
- **Inputs:** IPCC AR6 WGIII Ch. 11 (Table 11.3 technology costs) and Ch. 12 (Table 12.3 2030 potentials) in `_research/`; CBAM Implementing Regulation (EU) 2023/1773 and guidance documents in `_research/`; kernel convention from `CPAT_Industry_Kernel_Egypt_v0.8.xlsx` (`Manual inputs` D38:F47) and the v0.9 layout (`Manual inputs` rows 53-60, selector `E50`); earlier method note in `egypt+mitigation/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md` and `egypt+mitigation/InitialResultsAndIssues/Methodological Note.txt`.
- **Outputs:** `egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` (drop-in spec, sections 2.3 maps onto v0.9+); `egypt+mitigation/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse_Report.md` and `.docx` (derivation report, Appendix D = drop-in table); `egypt+mitigation/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse.xlsx` (live derivation, sheet `CPAT_v0.8_Table`); `TASK-D` entry in `instructions/instructions-egypt.yaml`; `EgyptTaskReference.md` item 1b marked partly done; `TODO.md` T1.
- **Caveats:** (1) Not applied: v0.9-v0.11 rows 53-60 hold placeholder anchors, so process response in those versions still equals v0.8. (2) Values are for process emissions only; v0.8 used one table for both fuel ER (rows 352-359) and process ER (363-370) - the applying task must separate them or accept the proxy explicitly. (3) The kernel books DRI reductant and SMR feedstock CO2 as `fp`, so `np` is ~0 for DRI-EAF and ammonia; the response then acts through `fp`. (4) AN assumes an unabated N2O baseline (`K36` = 0.97); use 0.3292 instead of 0.7210 if Egyptian nitric-acid plants are already abated. (5) Urea's own `np` is negative and floored at 0; the 11.6 % applies to embedded NH3 CO2 and is not applied separately. (6) Same values used for Egypt and non-Egypt. (7) IPCC supplies costs and potentials, not elasticities; the 2030 vs long-run split rests on labelled deployment assumptions. (8) USD2019 basis (100 USD2019 ~ 122 USD2024) versus the kernel's nominal/2024 price path - deflate or note when applying.

## 2026-10-02 - Docs: task-completion norm, caveats log and cross-references
- **Task:** Make the task-completion process explicit: every finished task is appended to this file (task, inputs, outputs, caveats), and `README.md`/`NORMS.md` reference the norms, processes and key documents.
- **Inputs:** `README.md`, `NORMS.md`, `TODO.md` (per-task conventions), `instructions/instructions-egypt.yaml`, `instructions/context-egypt.md`, `egypt+mitigation/EgyptTaskReference.md`, `egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`, `excel_ai_new/distribution/*.md`, current folder listing.
- **Outputs:** `CAVEATS.md` (new, this file); `NORMS.md` (new "Key documents" table and section 6 "Task completion: caveats log and bookkeeping"; legacy workbook path corrected to `excel_ai_original\`); `README.md` (layout block, "When a task is done", "Key documents", folder sections brought up to date with the current tree).
- **Caveats:** (1) Only Task D is back-filled above; caveats for kernel increments v0.3-v0.11 stay in the yaml `TASK-1` notes and the workbook `Settings` logs. (2) Not changed here and still stale: `TODO.md` header says the latest mainline is v0.9 (disk and yaml say v0.11, with `build_stream2_v2.py`/`..._Stream2_v2.xlsx` also present); `instructions/context-egypt.md` key-files table points at the v0.3 prototype and at `egypt+mitigation/Methodology/` (the methodology note now sits in `egypt+mitigation/InitialResultsAndIssues/`); the yaml, context file and TASK-D spec still write the legacy folder as `original_excel_ai/` although the folder on disk is `legacy/workbooks/`. (3) Working-tree reorganisation (`excel_ai_new/standalone-final/` -> `standalone_initial_prototypes/`, legacy folder rename, `NORMS.md`/`TODO.md`/`_research/` untracked) is uncommitted; nothing was committed in this task.

## 2026-10-02 - T2: merge Stream 2 (Tasks F, I, J) into the mainline (v0.12)
- **Task:** Integrate the Stream-2 branch (v0.7 -> `Stream2_v1/v2/v3` = Task F energy CO2, Task I output-based rebate, Task J revenue fund) with the mainline v0.11 (Tasks A-E, H, K, L, D-scaffold) into one workbook, v0.12.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.11.xlsx`; branch `Old\CPAT_Industry_Kernel_Egypt_v0.7branch_Stream2_v3.xlsx` (reference); builders `build_stream2_v1.py`, `build_stream2_v2.py`, `build_stream2_v3.py` (imported, not modified).
- **Outputs:** `excel_ai_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v0.12.xlsx` and `build_v0_12.py`. New sheets Data_EF, Emissions_Industry, Rebate_Industry, Fund_Industry; Check sections F, I, J appended after row 1516; Settings version-log row v0.12. v0.11 and the three branch workbooks moved to `Old\`. Updated `TODO.md` (T2 ticked, header), `NORMS.md`, yaml, `context-egypt.md`, `EgyptTaskReference.md`.
- **Regression:** for every bundle (LEGACY, 1A, 2A, 2B, 3A, 3B, 3C) all Check "Max |" summaries are 0, except the comparison rows 2-4, 584/585 and 1381, which are compared with v0.11 instead. LEGACY, 1A, 2A, 2B and 3A are identical to v0.11 (Mitigation_Industry and Check rows 1-1516, max abs diff 0). Only 3B (theta = 1, rebate) and 3C (phi = 1, fund) change, by design. No error values on any sheet.
- **Caveats:**
  1. **Fund_Industry process abatement adapted.** It now uses the v0.9 per-category ERmax form: wm = Q x cov x max(EF, 0) x ERmax / 1000, wp = wm x e^(-beta P), with 16 rows (np/no). The branch used the v0.7 single-beta form. The fund is still calibrated on the block curves, and the fuel side is unchanged. Fund 3C results therefore differ from the branch file.
  2. **`+o4` added to the process price term.** It is in o118-o125 (np and no) and in o15/o16. In v0.11, o15/o16 are still in the v0.7 form (beta.np from E363:E370 for both np and no, no ERmax), which is inconsistent with o118 (v0.9). This is pre-existing and was not changed here.
  3. **Task F check (d) re-pointed.** It used block o1 (row 645), which cascades to the year row (o29), not to a price. In the branch the check never bound because output was exogenous. Under Task H (v0.10), 2027 scenario-2 coal/gas CO2 is about 3e-6 Mt above scenario 1 at a zero explicit price. The check now conditions on o2 + o3 (rows 646/647). Block o1 itself is unchanged and stays a label cascade.
  4. **Rebate is counted on two paths.** Task I's rebate uses EU benchmark x obrrb, while Task H's output response (v0.10) deducts min(obrrb, price) x covered EF. Task I's ppin is kept as a memo so the rebate does not enter output twice; the two bases are not reconciled.
  5. **ssc rows now hold 1 in every bundle.** Data_Prices `egy.mit.ssc.<sector>.2` is 1 for all bundles (ssc_fund default); it has no effect while shp.<fuel>.ind.2 = 0 (phi = 0).
  6. **Ex-post shortfall in 3C.** In 3C the ex-post shortfall is negative (e.g. -152 USD mn in 2030): actual o155 revenue is below F, because F is phi x pre-fund revenue rev0. This is the Stream-2 design that avoids circularity.
  7. **T1 still not applied.** Rows 53-60 remain placeholders.

## 2026-10-02 - Task G: IPPU replacement and fuel-CO2 reconciliation (v0.13)
- **Task:** Task G (EgyptTaskReference 5.1/5.2). Replace CPAT's proportional IPPU row with the block's process emissions to remove the double count, and reconcile block product fuel CO2 with sector energy CO2. Produces v0.13.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.12.xlsx`. Legacy `excel_ai_original\CPAT 1.0pre_456_NoPropData.xlsb`, Mitigation rows 7566-7570 / 13883-13887 (IPPU co2/ch4/n2o/fga/tot) and 6590 (ind CO2), values stored. CPAT method: IPPU(t) = IPPU(t-1) x ind CO2(t)/ind CO2(t-1) from 2024.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.13.xlsx` and `build_v0_13.py`. Manual inputs rows 84-95: switch E85 `IppuOther` NONE (default) / CPAT, plus a per-product "fp counted as IPPU" flag (E88:E95; ammonia = 1). New sheet `IPPU_Industry`: CPAT IPPU; CPAT-method IPPU; block np/no/proc; fp as IPPU; non-block remainder; kernel IPPU = block + non-block; double-count correction; sector fuel-CO2 reconciliation. Check section Task G after row 1827 (summary D1831). v0.12 moved to `Old\`.
- **Regression:** for all bundles, every Check "Max |" row is 0 (Task G identities included), and all prior sheets are identical to v0.12 (max diff 0). There are no error values. The IppuOther = CPAT switch test passes. 2030 s2, kernel vs CPAT-method IPPU (Mt): LEGACY 87.67 vs 82.79; 1A/3A 84.75 vs 85.27; 2A/2B 86.74 vs 85.27; 3B 86.99 vs 86.29; 3C 80.01 vs 81.91. Non-block 50.75 in all.
- **Caveats:**
  1. **Report-only.** Kernel IPPU is not yet fed into a national GHG total; this needs the CPAT links (Task M). There is no calibration to CPAT.
  2. **Non-block baseline.** Non-block IPPU in s1 = CPAT IPPU - block. Under NONE it is held at s1 in s2; under CPAT it follows CPAT's s2/s1 ratio.
  3. **CPAT-method s2 is an approximation.** It reproduces CPAT exactly only in s1. In s2 it applies CPAT's rule to the kernel's own industrial energy CO2 change, with the non-kernel sectors (omn, ftr) held at baseline.
  4. **fp flag judgement.** Only ammonia SMR feedstock fp is booked as IPPU (IPCC 2B1; CPAT mch energy CO2 = 0). DRI reductant fp stays in energy.
  5. **Reconciliation gap (Info rows).** Block fuel CO2 net of fp-as-IPPU exceeds kernel sector energy CO2 in every year for cem, nfm and mch, and in 11 (s1) / 16 (s2) years for irn. Cement is about 13.5 Mt (50 Mt clinker x 0.2883) against 9.5 Mt in 2022. Block fuel EFs or CPAT sector energy balances need review; not resolved here.
  6. **Data source.** CPAT values come from the legacy xlsb (as in Task F), not from the Egypt csv run.
  7. **T1 still not applied** (rows 53-60 are placeholders).

## 2026-10-02 - Task M: links to main CPAT and Table 2 assembly (v0.14)
- **Task:** Task M (EgyptTaskReference 5.6). Link the kernel to CPAT national outputs (GHG for coverage %, revenue, deaths avoided, recycling) and assemble Table 2 in the kernel, porting the TASK-2b rebuild composition. Produces v0.14.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.13.xlsx`; `egypt+mitigation\AdHocRebuild\cpat_outputs_egypt_2022_2041.csv` (CPAT runs EG1-EG4, 32 codes); rebuild method `MethodologyNote_v0.1.md`, `build_adhoc_rebuild_v0_1.py` (Results).
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.14.xlsx` and `build_v0_14.py`. New sheets `CPAT_National` (csv stored) and `Table2_Industry`: A bundle -> run mapping (D6:D12; 1A/2A EG1, 2B EG2, 3A-3C EG3, LEGACY '-') + active bundle, scope (Scenarios L), summary year; B CPAT series of the mapped run + deltas; C kernel series; D Table 2 columns J K L M N O P Q R T U AR per year; E live summary row + stored 2030 snapshot of all bundles with rebuild v0.1 K. Check section Task M after row 1857. v0.13 moved to `Old\`.
- **Method (deltas only):** K = dGHG_CPAT + (dIPPU_kernel - dIPPU_CPAT) + (dInd_kernel - dInd_CPAT); dInd_kernel = d energy CO2 of the kernel sectors + non-kernel industry change (All sectors: non-kernel baseline x CPAT run's ind2/ind1 - 1; Industry only: 0). J = (All sectors: CPAT energy CO2; Industry only: encov x kernel-sector energy CO2 + flag x block process baseline) / CPAT GHG baseline. P = gross - rebates (Rebate_Industry) - fund F (Fund_Industry); gross = All: CPAT six-fuel carbon-tax receipts + cptraj x encov x (dInd_kernel - dInd_CPAT) + block process revenue; Industry only: cptraj x encov x kernel-sector energy CO2 (policy) + process revenue. Q = CPAT deaths avoided x dEnergy CO2 (kernel composition) / dEnergy CO2 (CPAT). AR = CPAT dNet new revenue - CPAT carbon-tax receipts + P. M/N/O/T/U = block cbcov/cbintch/cbobchu/emrt over baseline emis/cbqch.
- **Regression:** every Check "Max |" row is 0 for all bundles (Task M included), all prior sheets identical to v0.13 (max diff 0), no error values; live row = stored snapshot.
- **2030 results (kernel / rebuild v0.1):** K Mt 1A -27.7/-31.6, 2A -25.7/-27.7, 2B -27.1/-29.3, 3A -9.7/-18.0, 3B -6.6/-12.8, 3C -17.3/-22.4. J % 63.0, 57.3, 57.3, 8.5, 8.5, 8.5. P $bn 6.90, 6.27, 6.24, 0.91, 0.00, -0.37. Q 1441, 1441, 1497, 278, 241, 397. AR $bn 11.10, 10.47, 10.67, 2.67, 1.76, 1.39.
- **Caveats:**
  1. **T1/T3 not done.** TODO T4 asked for Task M after T1/T3; built now on request. Process semi-elasticities are still placeholders, so K, N, T change once T1 is applied.
  2. **Data vintage.** The csv runs differ from the CPAT values stored in the kernel (xlsb; 2030 baseline IPPU 85.97 vs 87.67, industrial energy CO2 88.97 vs 75.38). Only deltas within one source are composed; J mixes csv GHG with kernel-sector levels.
  3. **Smaller K than the rebuild,** mainly for 3x: the kernel's own industry response replaces CPAT's (no kappa, D_obr, F_fund add-ons); kernel-sector energy CO2 is smaller than kappa x CPAT industry CO2 (J 8.5 % vs 14 %).
  4. **Negative P in 3C (-0.37).** Fund F = phi x block revenue (CBAM products), which exceeds kernel-sector carbon revenue because block fuel CO2 > sector energy CO2 (Task G reconciliation gap). Left unclamped.
  5. **LEGACY** is not a Table 2 bundle: national-linked columns are 0; block metrics shown as is.
  6. **Recycling effects:** the csv has no recycling outputs; reported as revenue use (Scenarios K) + AR only.
  7. **Run mapping** is a stored input (Table2_Industry D6:D12); EG3 prices kappa = 0.54 of industry, so its dGHG residual (non-industry) is that run's.
  8. **Snapshot** rows are stored at default Manual inputs; Check compares live = snapshot only in 2030.

## 2026-10-02 - TASK-EF: Egypt CBAM emission factors split four ways (v0.1, values ready, not applied)
- **Task:** A transparent, auditable derivation of Scope 1 emission factors for the eight kernel CBAM goods, split into fuel combustion (fc), fuel-based process/reductant (fp), non-fuel process CO2 (np) and non-CO2 (no).
- **Inputs:** IPCC 2006 Vol.2 Table 2.2 and Vol.3 Tables 2.4, 3.1, 3.3, 4.1, 4.10 and 4.15; CBAM Implementing Regulation (EU) 2023/1773 and its default-value conventions; `Manual inputs` H30:K37 and S:V of kernel v0.12/v0.13; Egypt plant information (Tier C/D).
- **Outputs:** `egypt+mitigation/EmissionFactors/EGY_CBAM_EF_v0.1.xlsx`, `build_ef_v0_1.py`, `recalc_and_check.py` (0 errors, 14 checks OK) and `EGY_CBAM_EF_Methodology_v0.1.md`; `TASK-EF` in `instructions/instructions-egypt.yaml`; `EgyptTaskReference.md` section 1; `TODO.md` T5.
- **Caveats:**
  1. Not applied to the kernel. Adoption is queued as T5.
  2. Conventions differ from the kernel:
     - urea np = 0 under the CBAM rule, against the kernel's -0.733 (the `urea_conv` switch reproduces the kernel);
     - AN keeps HNO3 as a precursor (own 0.112, against the kernel's folded-in 0.97);
     - DRI-EAF is rebuilt from a carbon balance (0.609, against 0.730).
  3. Egypt-specific inputs are Tier C/D and carry VERIFY flags: ammonia GJ/t, the nitric-acid N2O abatement share, Egyptalum PFC rates, the kiln fuel mix, DRI gas use and the EISCO BF closure. Egypt portals (UNFCCC, CDM, GNR, IEA) were not reachable.
  4. Clinker fc 0.314 (> 0.2883) widens the v0.13 cement fuel-CO2 reconciliation gap.
  5. EU default values are copied from the kernel, not re-verified.

## 2026-10-02 - Integrated Egypt methodology document (v1.0)
- **Task:** Bring the whole Egypt thread into one main methodology document. The EF derivation is Appendix A and the process semi-elasticity work (Task D) is Appendix B.
- **Inputs:**
  - `README.md`, `instructions/context-egypt.md`, `CAVEATS.md`, `TODO.md`, `NORMS.md`, `EgyptTaskReference.md`, `instructions/instructions-egypt.yaml`;
  - `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` and the `ProcessEmissions_CarbonPriceResponse_Report.md` report;
  - `AdHocRebuild/MethodologyNote_v0.1.md`;
  - `EmissionFactors/EGY_CBAM_EF_Methodology_v0.1.md`;
  - the `InitialResultsAndIssues/` docx files (Technical note, MajorIssues, EgyptResultsInitial, MACC audit trail);
  - kernel v0.13 (`Manual inputs` H30:K37 and rows 53-60).
- **Outputs:** `egypt+mitigation/EGYPT_Methodology_v1.0.md` and `.docx`. The docx is generated from the md by a python-docx script, which is not in the repo. Pointers added in `README.md` (Key documents, egypt folder), the `NORMS.md` Key documents table, the `instructions/context-egypt.md` key files, `EgyptTaskReference.md`, and `TASK-METHOD` in `instructions/instructions-egypt.yaml`.
- **Caveats:**
  1. The document describes the current state. The Table 2 results come from the TASK-2b rebuild, which uses kernel EFs, not EF v0.1, and has open flags: kappa(EG3) = 0.54, and eps_Q, P_EU and sigma are placeholders.
  2. Kernel v0.13 still holds the Task D placeholders (T1 not applied), so the App. B values are not yet live.
  3. App. B.5 recommends routing beta to fp for DRI, BF and ammonia, together with np/no. This is a recommendation, not implemented.
  4. The earlier MACC audit-trail docx (ammonia 85 %, AN 89 % at $100) is treated as superseded by Task D.
  5. If the md is edited, regenerate the docx or the two will drift.

## 2026-10-02 - T1 + T5: Task D semi-elasticities and Egypt CBAM EF v0.1 applied (kernel v0.15, AdHoc rebuild v0.2)
- **Task:** Apply the updated emission factors (TASK-EF v0.1) and the IPCC process-emission semi-elasticities (Task D, TODO T1) to both the kernel prototype and the TASK-2b ad hoc rebuild.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.14.xlsx`; `egypt+mitigation\EmissionFactors\EGY_CBAM_EF_v0.1.xlsx` (Products D:G); `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` and `ProcessEmissions_CarbonPriceResponse.xlsx` (IPCC central ER at $100); `AdHocRebuild\AdHocCalculations_Rebuild_v0.1.xlsx` builder.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.15.xlsx` + `build_v0_15.py` (Manual inputs H30:K37 EFs, M35/M36 embedded NH3, S:V memo, AD/AE sources; E50 = IPCC; rows 53-60 ERmax / P* = 100 / ER*; Check section T1/T5 at row 1881; Settings log row 42). `AdHocRebuild\AdHocCalculations_Rebuild_v0.2.xlsx` + `build_adhoc_rebuild_v0_2.py`, `recalc_and_check_adhoc_v0_2.py` (report `_v0_2_report.txt`), `MethodologyNote_v0.2.md/.docx`, new switch `Inputs!EFSet` (EGY_EF_V01 default / PROTOTYPE). v0.14 moved to `Old\`.
- **Regression:** kernel: every Check "Max |" row 0 for all 7 bundles, no error values (stored Task J v2 table and Task M Table 2 snapshot refilled; baseline-independent rows unchanged except via EFs). AdHoc: ALL PASSED; PROTOTYPE FULL/NOPHASE = v0.11 132/132 (EFSet forced PROTOTYPE); REBUILD = Python mirror 534/534; check 8 (E_base 61.16) is n/a unless EFSet = PROTOTYPE (E_base 2030 now 62.42 Mt).
- **2030 K (Mt):** kernel v0.15 1A -29.8, 2A -25.8, 2B -27.1, 3A -11.8, 3B -8.6, 3C -23.9 (v0.14 -27.7/-25.7/-27.0/-9.7/-6.6/-17.3); rebuild v0.2 -31.8/-27.8/-29.3/-18.2/-12.7/-22.6 (v0.1 -31.6/-27.7/-29.3/-18.0/-12.8/-22.4).
- **Caveats:**
  1. **Bug fixed (kernel):** EF-category rows o15/o16 (Mitigation_Industry 260/261, 659/660) applied the np beta to no and ignored ERmax; now np = F x (1 - exp(-E x P)), no = H x (1 - exp(-G x P)), as in o118-o125. Latent while the placeholders were equal.
  2. **AN:** HNO3 N2O folded into AN own no (0.79 x 1.2588 = 0.9944); ER at $100 = N2O-weighted blend of unabated 0.7210 and abated 0.3292 at the EF workbook's 50 % abatement share: (3.5 x 0.7210 + 1.25 x 0.3292) / 4.75 = 0.6179.
  3. **Urea np = 0** (CBAM rule; was -0.733, floored to 0 in the process factor anyway). Ammonia/urea beta = 0: routing the CCS lever to fp (EF App. B.5) is not implemented.
  4. **Aluminium:** combined ER 0.2164 applied to both np (anode CO2) and no (PFC) instead of the non-additive split 0.1282 / 0.1078.
  5. **P* = 100 in USD2019,** no deflation to the kernel price unit. Fuel ER (rows 40-47) and the fund path unchanged; 3C fund shadow price 2028 falls 72.4 -> 44.5 $/t because the higher beta buys more abatement per dollar.
  6. **Cement fc 0.2883 -> 0.3136** widens the Task G block-vs-sector fuel CO2 gap (info rows in Check still non-zero counts).
  7. **EF VERIFY list** (EF App. A.6) still open; values not final.
  8. Table 2 snapshot rebuild column now "Rebuild v0.2 K"; Task M not otherwise redesigned (T3 and the EG3 full-coverage re-run still pending).

## 2026-10-02 - AdHoc rebuild v0.3: P* deflation and EG3 full-coverage approximation
- **Task:** Build `AdHocCalculations_Rebuild_v0.3.xlsx` without modifying v0.2. Added `PStar=122` for IPCC beta sets and made `KappaMode=SCALE` the default to approximate full industrial coverage for EG3 bundles 3A/3B/3C.
- **Inputs:** `AdHocCalculations_Rebuild_v0.2.xlsx`, `build_adhoc_rebuild_v0_2.py`, `recalc_and_check_adhoc_v0_2.py`, `MethodologyNote_v0.2.md`, `cpat_outputs_egypt_2022_2041.csv`, `prototype_v0_11_results.json`, Egypt EF v0.1 and Task-D IPCC ER100 values.
- **Outputs:** `egypt+mitigation\AdHocRebuild\AdHocCalculations_Rebuild_v0.3.xlsx`, `build_adhoc_rebuild_v0_3.py`, `recalc_and_check_adhoc_v0_3.py`, `recalc_and_check_adhoc_v0_3_report.txt`, `MethodologyNote_v0.3.md` and `.docx`. Verification passed: PROTOTYPE FULL/NOPHASE 132/132 each; REBUILD Python mirror 588/588; no Excel errors.
- **Caveats:** `KappaMode=SCALE` is an approximation of a full-coverage EG3 run pending a CPAT re-run. CPAT fuel receipts are scaled by 1/kappa; CPAT delta net new revenue itself is not independently re-run. `PStar=122` has Medium confidence and applies only to IPCC beta sets; PROTOTYPE keeps /100.

## 2026-10-02 - Worked example results workbook (v0.1, quick draft)
- **Task:** One-example-per-level walkthrough of the ad hoc Table 2 rebuild v0.3 (parameters -> CPAT inputs -> clinker in 1A -> 8-product block -> national 1A metrics -> 3A/3B/3C variants), with a column noting where the main version (kernel v0.15) differs.
- **Inputs:** `AdHocCalculations_Rebuild_v0.3.xlsx` (Inputs, Results), `cpat_outputs_egypt_2022_2041.csv` (2030), `MethodologyNote_v0.3.md`, `EGYPT_Methodology_v1.1.md` section 5.1.
- **Outputs:** `egypt+mitigation\AdHocRebuild\ExampleResults_v0.1.xlsx` (sheets Example, Inputs, Block), builder `build_example_results_v0_1.py`. All 30 check values match v0.3 to 4 dp (max diff 5e-5); no Excel errors.
- **Caveats:** Quick draft for iteration. Inputs copied as values (not linked to v0.3). Only REBUILD / NOPHASE / SCALE / EGY_EF_V01 shown. Kernel column quotes v0.15 headline values and method differences only; kernel steps are not recomputed.

## 2026-10-03 - Kernel v0.16: run-2 fixes (P* deflation, EG3 1/kappa scaling, block fuel CO2 reallocation, 3C fund fixed point)
- **Task:** Apply the four user-agreed fixes to the final prototype (decisions recorded in the session; mirrors AdHoc rebuild v0.3 for items 1-2) and refresh the `Egypt Final results` deliverables.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.15.xlsx`; `egypt+mitigation\AdHocRebuild\rebuild_v0_3_K2030.json` (rebuild v0.3 K for the Table 2 comparison column).
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.16.xlsx` + `build_v0_16.py`: Manual inputs F/J 53-60 P* = 122 (Check T1/T5 ER rows use 122); `Table2_Industry` row 54 kappa, rows 59-60 block fuel CO2 reallocation (ek1' = sum max(block, sector)), row 64 non-kernel response /kappa, rows 84/91 coverage and gross revenue at kappa = 1 for Industry only, row 94 deaths /kappa, row 96 AR; `Fund_Industry` rows 425-433 stored fund R* per bundle (fixed point R = post-abatement block payments o155, secant per year, tol 1e-9), row 329 reads it; new Check section; Table 2 rebuild column "Rebuild v0.3 K". `Egypt Final results\`: kernel v0.16, rebuild v0.3, MethodologyNote_v0.3, ResultsComparison_Table2_v0.3, EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx (built by `AdHocRebuild\make_results_page_v0_3.py`), EGYPT_Methodology_v1.2, EGYPT_FinalCaveats_v1.1; superseded files in `Egypt Final results\Old\`.
- **Regression:** every Check "Max |" row 0 for all 7 bundles, no error values; 3C fund fixed point residual 5e-12 (5 iterations); other bundles have no fund.
- **2030 (kernel v0.16 / v0.15):** K 1A -29.0/-29.8, 2A -25.5/-25.8, 2B -26.7/-27.1, 3A -21.1/-11.8, 3B -17.4/-8.6, 3C -32.9/-23.9 Mt; J 3A-3C 18.5/8.6 %; P 1A 6.89, 3A 1.88/0.89, 3B 0.98/-0.02, 3C 0.73/-0.47 $bn; Q 3A 816/278, 3B 746/239, 3C 985/366. Rebuild v0.3 K -31.4/-27.8/-29.3/-25.1/-19.6/-30.6.
- **Caveats:**
  1. 1/kappa scaling is a linear approximation of a full-coverage EG3 CPAT run (non-kernel industry responds at CPAT's average priced-industry rate).
  2. 3C fund = block's own post-abatement payments; non-block industry revenue (0.73 $bn) stays in P. The rebuild sends all industrial revenue to the fund (P = 0): convention difference.
  3. Reallocation removes the block-above-sector excess (cement 19.05 vs 10.91 Mt in 2030) from non-kernel industry; the underlying CPAT energy-balance mismatch is not resolved.
  4. Data-vintage mix remains (stored industry CO2 75.4 vs csv 89.0 Mt): about 1.9 Mt of the prototype-rebuild K gap at kappa = 1, about 3.5 Mt for EG3.
  5. fp routing (ammonia/urea beta = 0) and the block fuel-intensity channel remain unimplemented (kept as caveats).
  6. The stale `EgyptResultsInitial_UpdatedResults_tracked.docx` (v0.1) may still be open in Word; move it to `Egypt Final results\Old\` if it remains in place.

## 2026-10-02 - Repo tidy: final deliverables vs Old/ (no model changes)
- **Task:** Tidy the Egypt output and working folders so only the final deliverables sit at top level; everything else moved to `Old/`. The prototype kernel v0.16 (not the ad hoc rebuild) is treated as the final model.
- **Inputs:** `Egypt Final results\`, `egypt+mitigation\`, `excel_ai_new\standalone_working_version\`.
- **Outputs:** `Egypt Final results\` and `egypt+mitigation\` now both hold the identical final set at top level (hash-checked): `CPAT_Industry_Kernel_Egypt_v0.16.xlsx`, `EGYPT_Methodology_v1.2`, `EGYPT_FinalCaveats_v1.1`, `ResultsComparison_Table2_v0.3`, `EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx` (+ `EgyptTaskReference.md` in the working folder). Moved to `Egypt Final results\Old\`: rebuild v0.3, MethodologyNote_v0.3, `CAVEATS.md` snapshot; exact duplicates of files already in `Old\` removed. Moved to `egypt+mitigation\Old\`: `AdHocRebuild\`, `EmissionFactors\`, `InitialResultsAndIssues\`, `ProcessEmissions_CarbonPrice_Response\`, TASK-2a/TASK-D specs, Methodology v1.0/v1.1, ResultsSummary v1.0, kernel v0.1. `standalone_working_version\`: builders other than `build_v0_16.py` moved to `Old\`, `__pycache__` deleted; `build_v0_16.py` paths updated (adds `Old\` to `sys.path`, reads v0.15 and `rebuild_v0_3_K2030.json` from their `Old\` locations; imports verified). Removed an empty stray root folder named `EGYPT_FinalCaveats_v1.1.md\`. Paths updated in `README.md`, `NORMS.md`, `TODO.md`, `instructions\context-egypt.md`.
- **Caveats:**
  1. `EGYPT_Methodology_v1.2` Appendix C (file map) and earlier entries in this log / `instructions-egypt.yaml` still cite pre-tidy paths; prefix `Old\` for anything not in the final set.
  2. `egypt+mitigation\EGYPT_ResultsSummary_v1.0.docx` was locked (open in Word); a copy is in `Old\`, delete the top-level one once closed.

## 2026-10-02 - Repo tidy follow-up
- **Task:** Resolve both caveats of the previous entry.
- **Inputs:** EGYPT_Methodology_v1.2.md/.docx.
- **Outputs:** Appendix C paths now point to Old\ in the .md and .docx (table text only, formatting kept), copied to both Egypt folders; locked egypt+mitigation\EGYPT_ResultsSummary_v1.0.docx removed (copy in Old\).
- **Caveats:** Earlier log entries and instructions-egypt.yaml still cite pre-tidy paths (historical record).

## 2026-10-02 - Updated results text v0.4 (final prototype values)
- **Task:** Put the final prototype (kernel v0.16) numbers into the tracked-changes results text; v0.3 carried the ad hoc rebuild values.
- **Inputs:** Egypt Final results\Old\EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx; kernel v0.16 2030 values from ResultsComparison_Table2_v0.3.md.
- **Outputs:** EgyptResultsInitial_UpdatedResults_v0.4_tracked.docx in both Egypt folders (builder egypt+mitigation\Old\AdHocRebuild\make_results_page_v0_4.py); tracked changes still relative to the original text; Table 2 checked against v0.16 (P, K, J, N, O, Q). References updated in README, FinalCaveats v1.1, Methodology v1.2, ResultsComparison v0.3. v0.3 moved to Old\.
- **Caveats:** O uses NOPHASE (as Table 2); the prototype's default FULL roughly doubles it. 2A/2B intensity shows 0% because the prototype holds block fuel intensity fixed (stated in the text). Narrative re-ranked: 3C now has the largest cut (32.9 Mt), 2B the largest health gain (1,473). Methodology v1.2 section text still describes the rebuild-based results page.

## 2026-10-02 - CBAM carve-out of Table 2 (v0.1)
- **Task:** Original CPAT run results everywhere except the CBAM block; block from kernel v0.16 with growth matched to CPAT sectors. 3A-3C use EG3 as run (no 1/kappa).
- **Outputs:** EGYPT_CarveOut_Table2_v0.1.md/.docx in both Egypt folders; builder egypt+mitigation\Old\AdHocRebuild\make_carveout_v0_1.py with kernel extracts carveout_kernel_*_2030.json (Excel COM, Settings!B10 per bundle).
- **Result (2030 K, Mt):** 1A -36.1, 2A -31.7, 2B -33.4, 3A -21.5, 3B -17.8, 3C -31.9.
- **Caveats:** K = CPAT dGHG - r x block + kernel block change, with r = CPAT industry energy CO2 % change (also CPAT's IPPU %). Non-CBAM IPPU (about 50 Mt) keeps CPAT's response; prototype v0.16 held it fixed (main cause of its low 1A). Growth rescaled 2024-2030: irn x0.976, cem x1.001; mch (mining & chemicals = fertilisers) x1.157 and nfm x0.956 follow total CPAT industry because CPAT sector energy is 0 for Egypt. M/N/O kept from v0.16 (O NOPHASE). Deaths scaled by block fuel adjustment. 1A remains 5.5 Mt below the original: about 2.7 Mt was the original's process double count, the rest is the block responding less than CPAT's industry average (fuel intensity fixed). Tracked doc v0.4 not updated to the carve-out.

## CBAM carve-out v0.2 (CPAT fuel-intensity response), updated text v0.5, Methodology v1.3 (2026-10-03)

- **Task:** Final Table 2 = original CPAT runs everywhere; only the CBAM block replaced, using CPAT's own emissions-intensity reduction plus the CBAM output/process adjustment, with no double counting.
- **Method:** K = dGHG_CPAT - r*B + dB. CPAT's implied block change (r*B) removed in full; dB = kernel output response + kernel process abatement (where charged) + CPAT fuel-intensity response (1+r)^(1/3)-1 (s_int = 1/3, Methodology section 3): EG1 -4.9%, EG2 -5.1%, 3A-3C use -4.9%. N/O = kernel v0.16 plus the fuel-intensity term (O x0.8 NOPHASE; 3B x1.0). Check: the N formula reproduces kernel N to within 0.2 pt with i_f = 0.
- **Results 2030 (1A/2A/2B/3A/3B/3C):** K -37.4/-33.1/-34.8/-22.8/-19.1/-33.0; P 6.9/6.3/6.2/1.5/0.6/0.4; N -5.8/-2.1/-2.3/-5.8/-5.8/-23.1; O -24.0/-12.2/-12.3/-24.0/-5.1/-36.2; Q 1,501/1,456/1,517/552/491/646; J 63/57/57/14/14/14.
- **Outputs:** EGYPT_CarveOut_Table2_v0.2.md/.docx (builder Old\AdHocRebuild\make_carveout_v0_2.py); EgyptResultsInitial_UpdatedResults_v0.5_tracked.docx (make_results_page_v0_5.py, tracked relative to the original; rankings rechecked); EGYPT_Methodology_v1.3 (new section 5.0). Both Egypt folders identical. v0.4 text, carve-out v0.1 and Methodology v1.2 moved to Old\. References updated in README, NORMS, TODO, context-egypt.md, FinalCaveats v1.1, ResultsComparison v0.3.
- **Caveats:**
  1. The 3B rebate and the 3C fund are not re-solved for the lower block fuel payments (under 0.05 $bn).
  2. O on NOPHASE, not yet confirmed by the user.
  3. 3A-3C use EG3 as run (54% industry coverage), so their non-block industry cut is diluted.
  4. The CPAT intensity share (1/3) is the CPAT efficiency/fuel-switch split; it is not product-specific.

## CBAM obligations on FULL convention: carve-out v0.3, updated text v0.6 (2026-10-03)

- **Task:** Report CBAM obligations (O) on the FULL convention (EU CBAM factor 0.485 in 2030, full credit for the domestic price; kernel headline) instead of NOPHASE.
- **Method:** O = kernel v0.16 FULL value + 0.59 x the fuel-intensity change in N ((48.5 - 20)/48.5); 3B x1.0. NOPHASE kept as a memo row. All other values as in carve-out v0.2.
- **Results 2030 O FULL (1A/2A/2B/3A/3B/3C):** -44.2/-22.9/-23.0/-44.2/-5.0/-53.1 (NOPHASE -24.0/-12.2/-12.3/-24.0/-5.1/-36.2).
- **Outputs:** EGYPT_CarveOut_Table2_v0.3.md/.docx (make_carveout_v0_3.py); EgyptResultsInitial_UpdatedResults_v0.6_tracked.docx (make_results_page_v0_6.py; O cells and O narrative only); Methodology v1.3 section 5.0 edited in place. v0.5 text and carve-out v0.2 moved to Old\. Both Egypt folders identical; references updated.
- **Caveats:**
  1. The FULL percentages are not like-for-like with the original Table 2, which used NOPHASE; the comparison table shows both.
  2. The results text does not state the convention explicitly; add a footnote to Table 2 if needed.

## Egypt finalisation: final set docx-only, FinalCaveats v1.2, convention note (2026-10-03)

- **Task:** Finalise the Egypt deliverables, archive the old versions and the .md files, and tie off loose ends.
- **Final set (top level of both `Egypt Final results\` and `egypt+mitigation\`, hash-identical):** EGYPT_CarveOut_Table2_v0.3.docx (final Table 2), EgyptResultsInitial_UpdatedResults_v0.6_tracked.docx, EGYPT_Methodology_v1.3.docx, EGYPT_FinalCaveats_v1.2.docx, CPAT_Industry_Kernel_Egypt_v0.16.xlsx. The working folder also keeps EgyptTaskReference.md (workflow tracker, per NORMS).
- **Changes:**
  - FinalCaveats v1.2 adds section F (carve-out caveats F1-F7) and updates items 8-9.
  - The results text v0.6 now says obligations are "under the 2030 CBAM phase-in" (tracked).
  - The .md sources and ResultsComparison_Table2_v0.3 moved to Old\. make_carveout_v0_3.py now writes its md to Old\.
  - References updated in README, NORMS, TODO, context-egypt.md and instructions-egypt.yaml (FINAL note under TASK-1).
- **Caveats:**
  1. The egypt+mitigation\Old copy of FinalCaveats v1.1 was restored from the Egypt Final results\Old copy, which has the older file references (superseded anyway).
  2. The kernel xlsx could not be hash-checked because it is open in Excel.

## Kernel v0.17: CBAM carve-out in the kernel (2026-10-03)

- **Task:** Put the final Table 2 (CBAM carve-out v0.3, O on FULL) into the kernel with live formulas.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.17.xlsx` + `build_v0_17.py` (Excel COM, from v0.16). New sheet `CarveOut_Table2`:
  - A: inputs (live links to Table2_Industry, Manual inputs, CPAT_National, Emissions/IPPU_Industry);
  - B: rates r and i_f;
  - C: block by sector (mch, irn, nfm, cem; growth factors);
  - D: carve-out;
  - E: Table 2 columns for the active bundle (Settings!B10);
  - F: stored 6-bundle snapshot and a live-vs-stored check.
  - Also: a Check sheet section, a pointer in Table2_Industry B112, and a Settings version row. No other formulas changed.
- **Copies:** in both `Egypt Final results\` and `egypt+mitigation\` (hash-identical). v0.16 and `build_v0_16.py` moved to `Old\`.
- **Verification:** each bundle set active in turn, CalculateFull. Live = stored within 0.006 (largest in 3A-3C J: kappa 0.537 is rounded in the script). Kernel N rebuilt from the block table is within 0.19 pt.
- **Fix:** Methodology v1.3 section 5.0 and FinalCaveats v1.2 section F had symbols (minus, delta, times, section sign, kappa, CO2 subscript) saved as "?" (encoding slip in the earlier edit). Repaired, and both docx regenerated.
- **References updated:** README, TODO, context-egypt.md, instructions-egypt.yaml, Methodology (5.0, 6, App. C, version log), FinalCaveats header.
- **Caveats:**
  1. The NOPHASE memo uses the stored v0.16 NOPHASE O per bundle (hard input, rounded to 0.1), not a live convention switch.
  2. With Settings!B10 = LEGACY the carve-out sheet shows n/a; pick a bundle from 1A to 3C.

## 2026-10-04 - Tracked results text v0.7 (terminology; author Stephen Stretton)
- `EgyptResultsInitial_UpdatedResults_v0.7_tracked.docx` (both Egypt folders) built from v0.6 by `egypt+mitigation/Old/AdHocRebuild/make_results_page_v0_7.py`; v0.6 moved to `Old/`.
- Fixes: 3C CBAM obligation cut 30% -> 53% (summary paragraph, missed in v0.6); 3B "undermines both revenue and CBAM relief" -> "raises less revenue and delivers the smallest CBAM relief"; 3C "forgoes revenue and health benefits" -> "raises less revenue and yields smaller health benefits than broad-based pricing"; added note that EG3 prices only about half of industrial energy CO2 (14% coverage, not about 21%).
- Terminology standardised: "industrial abatement rebate", "CBAM-sector emission intensity", "CBAM-sector emissions", "national GHG emissions"; en-dashes in numeric ranges.
- All tracked changes and docProps (creator/lastModifiedBy) of the final .docx files now attributed to Stephen Stretton; Lelia Croitoru's comments kept. References v0.6 -> v0.7 updated (README, instructions, Methodology/FinalCaveats md; docx regenerated).
- Consistency check: final numbers identical across tracked text, CarveOut v0.3, Methodology v1.3 §5.0 and kernel v0.17 snapshot; both folders hash-identical. Not verified by opening in Word (automation hung); XML validated.


## 2026-10-04 - Egypt final v1.0 release (Stephen Stretton)

- All final deliverables relabelled v1.0 and placed identically (hash-checked) at the top of `Egypt Final results\` and `egypt+mitigation\`: CPAT_Industry_Kernel_Egypt_v1.0.xlsx (= v0.17 relabelled, no formula changes), EGYPT_CarveOut_Table2_v1.0, EgyptResultsInitial_UpdatedResults_v1.0_tracked, EGYPT_Methodology_v1.0, EGYPT_FinalCaveats_v1.0. Numbers unchanged (2030 K: -37.4/-33.1/-34.8/-22.8/-19.1/-33.0 Mt).
- Proofread: tracked text fixes (double spaces, punctuation, "CBAM obligations", "trade-offs", 3C label, table-header units), all revisions and docProps by Stephen Stretton. Methodology: final-status header, §5 pointer to §5.0, coverage row in §5.0, kernel v0.17/v1.0 rows, file map updated.
- Md sources in `Old\` (both folders); earlier drafts and md (Methodology v1.3, FinalCaveats v1.2, CarveOut v0.3, text v0.7, kernel v0.17) archived in `Old\Superseded\` and `standalone_working_version\Old\`.
- Not validated by opening in Word (Word COM hangs in this environment); XML checked. Open items unchanged: full-coverage EG3 CPAT run; 3B published deaths (345) untraced; 3B rebate and 3C fund not re-solved.


## 2026-10-05 - Egypt results text v1.1: single scenario term (Stephen Stretton)

- Reviewer comment: the chapter mixed "policy options", "families", "bundles", "choices" and "designs" for the scenarios. `EgyptResultsInitial_UpdatedResults_v1.1_tracked.docx` (builder `egypt+mitigation\Old\AdHocRebuild\make_results_page_v1_1.py`) makes 22 minimal tracked replacements, all by Stephen Stretton, so that every reference to 1A-3C uses "scenario(s)" (for example "Policy bundle" -> "Policy scenario", "The second family" -> "The second set of scenarios", "The six bundles" -> "The six scenarios"). Uses that do not refer to scenarios are kept: "Revenue Recycling Option", "recycling options/choice(s)", "policy design". No numbers changed.
- v1.0 text archived in `Old\Superseded\` (both folders); v1.1 copied to both folders (hash-identical). Methodology and FinalCaveats v1.0 updated only to point to the v1.1 text file. Not opened in Word (COM hangs); XML checked.


## 2026-10-05 - Table 2 workbook with live CBAM obligations (Stephen Stretton)

- New `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx` (both Egypt folders; builder `egypt+mitigation\Old\AdHocRebuild\make_table2_cbam_xlsx.py`, data `kernel_products_2030.json` from `extract_kernel_products_2030.py`). Rows J, P, K, M, N, Q are hard-coded from the CBAM carve-out v1.0. Row O is computed live by product: obl = max(0, CBF x P_EU x EI - S x d), weighted by 2024 EU exports.
- Inputs are on the Assumptions sheet: EU price in 2030 (USD 100, placeholder kept from the initial analysis); convention (default **Full implementation, CBF = 1**, as in the initial table; alternative 2030 phase-in, CBF = 0.485); deduction scaled by CBF (No); net the 3C fund (No).
- Product-level O reproduces the kernel's O exactly (all six scenarios). It differs from the carve-out v1.0 linear shortcut by <= 0.4 pt. Default O: 1A -24.3, 2A -12.5, 2B -12.6, 3A -24.3, 3B -5.4, 3C -36.6 (2030 phase-in: -44.4/-23.1/-23.2/-44.4/-5.4/-53.4). Sensitivities: net the 3C fund -> 3C -20.7; P_EU 120 -> 1A -21.2; P_EU 80 -> 1A -29.1.
- **Pending:** the v1.0/v1.1 docx (CarveOut, tracked text, Methodology, Caveats) still quote O on the 2030 phase-in convention. Update them once the convention is agreed.


## 2026-10-06 - CBAM obligations restated as CBAM-product intensity change (Stephen Stretton)

- Table 2 row O is now the change in CBAM obligations per tonne exported = export-weighted change in embedded (fuel + process) emission intensity of CBAM products only (2024 EU export weights). The Egyptian carbon-price deduction is not applied, so the EU price and phase-in cancel. Final O: 1A -5.4, 2A -2.6, 2B -2.7, 3A -5.4, 3B -5.4, 3C -20.7% (was FULL -44.2/-22.9/-23.0/-44.2/-5.0/-53.1).
- Updated: `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx` (O live, deduction variants as memo rows only); results text **v1.2** tracked (`make_results_page_v1_2.py`; O cells, range "3 to 21%", 1A/3A 5%, 2A/2B 3%, 3C 21%, 3B sentence); CarveOut, Methodology §5.0, FinalCaveats F5/item 9; README and instructions references. v1.1 text and `EGYPT_CBAM_ObligationNote_v0.1` (deduction-based) moved to `Old\Superseded\`.
- Not changed: kernel v1.0 sheet `CarveOut_Table2` still reports O on FULL (the workbook governs). The user's `Egypt Final results\EGYPT_Methodology_v1.1 - Edited.docx` and the renamed note in `CBAM Guess - Needs Carolyn Input\` were left untouched and still quote the old O.

## 2026-10-07 - All Egypt deliverables aligned at v1.3

- Methodology v1.3 is built from the author's edited master (`EGYPT_Methodology_v1.1 - Edited.docx`, archived in `Egypt Final results/Old/`). Edits: §2 output and §4.5 now define Table 2 O as intensity-only (export-weighted, no deduction); the kernel's deduction-based Task L obligation and the NOPHASE/FULL/SCALED conventions are kept only as a memo; the P_EU/CBF parameter row and the glossary entry are marked memo-only; "bundle" changed to "scenario" (as in the tracked text). The edited master has no Markdown source, so it was edited directly in Word XML.
- CBAM obligation note rewritten to v1.3 (intensity-only; source `egypt+mitigation/Old/EGYPT_CBAM_ObligationNote_v1.3.md`, via pypandoc).
- CBAM workbook, CarveOut, FinalCaveats, tracked text and kernel are all at v1.3; content is unchanged apart from version references and "scenario" terminology. Kernel v1.3 `CarveOut_Table2`: column M80:M85 stores the intensity-only O; row 71 is relabelled as the FULL deduction memo (live O is still FULL there; the workbook governs).
- v1.0/v1.2 copies archived (FIN `Old/`, WRK `Old/Superseded/`). FIN and WRK copies are byte-identical. README, instructions and EgyptTaskReference now point to v1.3.

## 2026-10-08 - Egypt folder reorganisation and doc consistency fixes
- **Task:** merged `Egypt Final results/`, `egypt+mitigation/` and `instructions/` into a single root folder `egypt/` (`final/`, `supporting/`, `archive/`, `instructions/`); fixed documentation inconsistencies (latest kernel is v1.3 everywhere; legacy folder is `legacy/workbooks/`; methodology master is the edited `.docx`).
- **Inputs:** the three old folders (byte-identical duplicates found by hash; the two folders held the same v1.3 deliverables and mirrored archives).
- **Outputs:** `egypt/` (new `README.md`); duplicates removed, one copy of each file kept; tracked `__pycache__` files removed; path references updated in README, NORMS, TODO, AGENTS, the instructions yaml/context, the TASK-D/TASK-2a specs and the Python builders (`egypt/supporting/AdHocRebuild/*`, `excel_ai_new/standalone_working_version/Old/build_v0_14-17.py`). Entries above this one still quote the old paths: map `Egypt Final results\`/`egypt+mitigation\` to `egypt\final\`, `Old\` and `Old\Superseded\` to `egypt\archive\` or `egypt\supporting\`.
- **Caveats:** builders were not re-run (they need Excel COM on Windows); path edits are untested. Final CBAM workbook/note renamed to `..._v1.3_NeedsCarolynConfirmation` (from the `CBAM Guess - Needs Carolyn Input/` folder name). Two variants that differed were kept with `_alt1` (FinalCaveats v1.0, Methodology v1.0 md) and the pre-edit Methodology v1.3 renamed `_preedit`, all in `egypt/archive/`; the two `CAVEATS.md` copies from the old `Old/` folders are `egypt/archive/CAVEATS_snapshot_*.md`. `extract_kernel_products_2030.py` still points at the (now archived) v1.0 kernel and old Windows root. Historical versions in `egypt/archive/` were left with their original path text.

## 2026-10-04 - Decisions: 3B rebate scope and O convention (no model change)
- **Task:** resolved the two open TODO T4 decisions on the user's instruction (Stephen Stretton): the 3B rebate goes to all covered industry (`Inputs!ThetaOther` = 1, P approx. 0); the CBAM obligation O is on the FULL convention (CBAM factor phase-in, domestic carbon price deducted in full). NOPHASE (CBF = 1) is kept as a memo only.
- **Inputs:** `TODO.md` T4; `build_v0_11.py` / `build_v0_17.py` convention definitions; CAVEATS 2026-10-03 kernel v0.17 entry (kernel already reports O on FULL).
- **Outputs:** `TODO.md` T4 item updated; this entry. No workbook, builder or yaml changes.
- **Caveats:** decisions only, not yet applied. The AdHoc rebuild defaults (`ThetaOther`, convention) must be set to these values in a new builder version and re-verified with `recalc_and_check_adhoc.py` (Windows/Excel COM). Any Table 2 numbers built under `ThetaOther` = 0 or NOPHASE are superseded once that is done.

## 2026-10-04 - AdHoc rebuild v0.4 builder and verifier drafted (not built, not run)
- **Task:** applied the 2026-10-04 decisions to the AdHoc rebuild defaults: `Conv` = FULL (NOPHASE kept as a memo) and `ThetaOther` = 1. `ThetaOther` is forced to 0 in PROTOTYPE mode so the v0.11 reproduction is unchanged. No formula changes.
- **Inputs:** `build_adhoc_rebuild_v0_3.py`, `recalc_and_check_adhoc_v0_3.py`; CAVEATS 2026-10-04 decisions entry.
- **Outputs:** `egypt/supporting/AdHocRebuild/build_adhoc_rebuild_v0_4.py` and `recalc_and_check_adhoc_v0_4.py` (docstrings, defaults, ReadMe version log; the verifier now saves with Conv = FULL). v0.3 files untouched. Both compile (`py_compile`).
- **Caveats:** drafted on Linux. `AdHocCalculations_Rebuild_v0.4.xlsx` has NOT been built, and the verifier (Excel COM, Windows) has NOT been run. Run `python build_adhoc_rebuild_v0_4.py` then `python recalc_and_check_adhoc_v0_4.py` and check the report. Still to do after a clean run: MethodologyNote v0.4 and ResultsComparison_Table2 v0.4 (results change with ThetaOther = 1 and FULL), the yaml / `EgyptTaskReference.md` / `context-egypt.md` bookkeeping, and whether the final Table 2 deliverables need regenerating.

## 2026-10-04 - T3 builder drafted (kernel v1.4, not built, not run)
- **Task:** drafted `build_v1_4.py` for T3: move 2024 production, growth, EU exports and pre-policy prices out of `Mitigation_Industry` (both blocks) into a new `Manual inputs` section and link them. Values are read from the workbook, so no number should change.
- **Inputs:** `CPAT_Industry_Kernel_Egypt_v1.3.xlsx` (layout and values inspected read-only with openpyxl: both blocks identical, rows 97-108 of `Manual inputs` empty); TODO T3 spec (corrected: the spec's row 62 and v0.9 references are stale).
- **Outputs:** `excel_ai_new/standalone_working_version/build_v1_4.py`; TODO T3 note. No workbook produced.
- **Caveats:** drafted on Linux, never run; Excel COM needed. New section at `Manual inputs` rows 98-108 (title 98, header 100, products 101-108); links F/G/I rows 276-283 and 675-682, G rows 288-295 and 687-694; total exports (column H, blank placeholder) deliberately not linked. The builder aborts without saving unless the max abs difference over pre-existing cells is 0 and the new Check literal count is 0, then writes the version-log row and moves v1.3 to `Old/`. Check sheet rows 595-1020 hold CPAT values that equal the literals (e.g. 5100); they are comparison data, left as is. Pending after a clean run: yaml (TASK-T3 + TASK-1 notes), `EgyptTaskReference.md`, `context-egypt.md`, the kernel path references in other documents (still say v1.3), tick T3.

## 2026-10-04 - AdHoc rebuild v0.4 built and verified; housekeeping and reconciliation (no model change)
- **Task:** (1) resolves the entry "AdHoc rebuild v0.4 builder and verifier drafted (not built, not run)": v0.4 was built and verified on Windows (`recalc_and_check_adhoc_v0_4_report.txt`: ALL PASSED; PROTOTYPE 132/132 for FULL and NOPHASE, REBUILD 588/588 against the Python mirror). (2) Wrote `MethodologyNote_v0.4` (current method only), `ResultsComparison_Table2_v0.4` and `VersionNotes_AdHocRebuild.md` (change history, kept out of the methodology). (3) Added NORMS section 7 and an AGENTS.md rule: methodology and version notes are always separate documents. (4) Reconciled stale pointers in README, `instructions-egypt.yaml` (TASK-2a, 2b, D, EF, QUEUE statuses), `context-egypt.md`, `EgyptTaskReference.md` (current-status table at the top) and `TODO.md` (header, T4, Final steps plan). (5) Archived superseded AdHoc files to `egypt/archive/AdHocRebuild/` (workbooks, builders and verifiers v0.1-v0.2; methodology notes and comparisons v0.1-v0.3; make_carveout v0.1-v0.2; make_results_page v0.3-v0.6 and v1.0). Files still needed by live scripts stay in `supporting/AdHocRebuild/` (rebuild v0.3 workbook/builder for the example-results builder; make_results_page v0.7, v1.1, v1.2; make_carveout_v0_3).
- **Inputs:** CAVEATS 2026-10-04 decisions; v0.4 workbook and report; v1.3 kernel and final documents (read-only checks).
- **Reconciliation findings:** (a) The final numbers agree across `EGYPT_CarveOut_Table2_v1.3.md`, the Table 2 CBAM-calc workbook and the kernel `CarveOut_Table2` stored snapshot (K, P, Q, J, N, T checked). (b) The two 2026-10-04 decisions are in the rebuild only, not the final Table 2: final 3B still has the block-only rebate (P 0.64, K -19.1), and final row O is the intensity-only measure, so the FULL decision affects the kernel/rebuild memo only. (c) The CBAM-calc workbook's "Full implementation" (CBF = 1) is what the kernel calls NOPHASE. (d) The v1.3 kernel's Settings title and last log row say v1.0 (no v1.1-v1.3 rows). (e) `EGYPT_FinalCaveats_v1.3` still names rebuild v0.3; the Methodology docx carries before/after material. (f) The CBAM-calc workbook's Table 2 rows are hard-coded.
- **Caveats:** no model or deliverable changed. `.docx` versions of the new notes were produced with `md_to_docx.py` and not opened in Word. The final-steps plan in `TODO.md` lists the decisions needed (D1-D4) before the single confirmation workbook is built.

## 2026-10-04 - Decisions applied everywhere: 3B rebate to all covered industry, one CBAM convention, single confirmation workbook (final set v1.5; builders drafted, not run)
- **Task:** (D1) apply the 3B rebate decision to the final Table 2 and every document; (D2) apply one CBAM convention consistently; (D3) put the single confirmation workbook inside the kernel; (D4) keep EG3 as run for 3A-3C.
- **Method for 3B (new; review it):** `make_carveout_v0_4.py`. In non-block covered industry the output share (1 - s_int = 2/3) of CPAT's response (fuel + proportional IPPU, NB = dInd + dIPPU - r x block) is removed from K (+7.2 Mt); its fuel part enters the deaths adjustment; the rebate tau x (kappa x IND1 - block post-policy fuel) = USD 0.33bn is deducted from revenue, with no feedback onto CPAT receipts. Result, 3B: K -19.1 to -12.0 Mt, P 0.6 to 0.3 $bn, Q 491 to 330; all other scenarios and columns unchanged. 3B net revenue is 0.3, not 0, because EG3 prices only 54% of industry.
- **CBAM convention (D2, interpretation):** Table 2 row O stays the CBAM-product intensity change (EU price and phase-in cancel). The deduction-based memo obligation is on FULL (2030 phase-in, CBAM factor 0.485) with NOPHASE (no phase-in, factor 1) as the other memo, under those names in the kernel, rebuild and documents. The old workbook label "Full implementation" (CBF = 1) was NOPHASE.
- **Outputs:** `egypt/final/` v1.5 documents: `EGYPT_Methodology_v1.5.docx` (3B scope, new section 4.7, history removed), `EGYPT_CarveOut_Table2_v1.5`, `EGYPT_FinalCaveats_v1.5`, `EGYPT_CBAM_ObligationNote_v1.5_NeedsCarolynConfirmation`, `EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx`, `EGYPT_VersionNotes_v1.5` (new, change history), md sources in `md_sources/`. Builders/scripts in `egypt/supporting/AdHocRebuild/`: `make_carveout_v0_4.py` (+ `carveout_v1_5_results.json`), `make_results_page_v1_5.py`, `edit_methodology_v1_5.py`, `check_final_documents.py`. Kernel builders (`excel_ai_new/standalone_working_version/`): `build_v1_4.py` (T3) then `build_v1_5.py` (3B rule, `Manual inputs` E112, `CarveOut_Table2` section G, new sheet `Table2_Final`). The v1.3 document set and the CBAM-calc workbook (with its script and data) are in `egypt/archive/`.
- **Verification:** `check_final_documents.py`: every Table 2 figure printed in the carve-out note and the results text equals the independent Python mirror (15 rows, 0 failures). The kernel builders have NOT been run (Excel COM, Windows). `build_v1_5.py` refuses to save unless the live kernel equals the mirror, the stored snapshot, the live row O and the printed figures, and the regression over all other cells is 0.
- **Caveats:** (1) `egypt/final/` documents say kernel v1.5, which exists only after `build_v1_5.py` has run (until then `final/` holds kernel v1.3). (2) The new `.docx` files were generated with pandoc / python-docx and not opened in Word. (3) The kernel's prototype composition (`Table2_Industry`, `Rebate_Industry`) still rebates the CBAM block only (reference). (4) The row O definition is still pending Carolyn's confirmation. (5) The 3B non-block rule is an application of CPAT's usage/efficiency split, not a CPAT re-run. (6) Open as before: true full-coverage EG3 run, EF VERIFY list, fp routing.

## 2026-10-04 - `egypt-final/` simplified hand-over folder
- **Task:** new top-level folder `egypt-final/` with a plain, version-free set of the final Egypt deliverables: `1_Summary.docx` (2 pages, plain language), `2_Results_Table.docx`, `3_Methodology.docx` (simplified rewrite), `Egypt_Model.xlsx`, `Egypt_CBAM_Obligations.xlsx`.
- **Inputs:** `egypt/final/` (kernel v1.3, Table 2 carve-out, CBAM calc workbook, methodology v1.3, caveats).
- **Outputs:** the five files above. Nothing in `egypt/` was changed or moved.
- **Caveats:** the two workbooks are byte copies renamed; internal sheet text (ReadMe/Settings version log, builder names) still carries version labels, because Linux cannot recalculate or rebuild them. The three Word files are new text; numbers were copied from `EGYPT_CarveOut_Table2_v1.3.md` and the methodology v1.3 and not independently recomputed. The CBAM-bill workbook is still pending Carolyn's confirmation (stated in the summary). Page counts checked via LibreOffice (summary 2 pages).

## 2026-10-04 - Kernel v1.4 (T3) and v1.5 (3B decision, Table2_Final) built and verified on Windows
- **Task:** resolves the entries "T3 builder drafted" and the v1.5 caveat that the builders had not been run. `build_v1_4.py` and `build_v1_5.py` were run by the user (commits "Minor changes", "Rebuilt to v1.5").
- **Checked after the pull (read-only, openpyxl on the saved v1.5):** sheets include `Table2_Final`; Settings log has rows v1.4 and v1.5; `Manual inputs` E112 = 1 and rows 101-108 hold the T3 values; Check section v1.4 literal count = 0 and v1.5 printed-vs-workbook mismatches = 0 (`Table2_Final` D42 = 0). Final Table 2 stored values: 3B K -11.976, P 0.315, Q 329.8, J 13.921 (others unchanged from v1.3: 1A K -37.39, 2A -33.08, 2B -34.83, 3A -22.77, 3C -33.04). Section D memo: FULL -44.2/-22.9/-23.0/-44.2/-5.0/-53.1, NOPHASE -24.0/-12.2/-12.3/-24.0/-5.1/-36.2.
- **Outputs:** `egypt/final/CPAT_Industry_Kernel_Egypt_v1.5.xlsx` (= `excel_ai_new/standalone_working_version/` copy); v1.4 in `Old/`; v1.3 in `Old/` and `egypt/archive/`.
- **Caveats:** the builders' own printed regression output was not available to me, so the "regression 0" gate is inferred from the fact that they saved (they abort otherwise). 3B coverage J is 13.921 in the kernel (live kappa) against 13.916 in the documents (rounded to 14); no printed figure changes. Still open: the `egypt-final/` hand-over folder (built from v1.3, shows the old 3B numbers), Word check of the new .docx files, Carolyn's confirmation of row O, EG3 full-coverage run, EF VERIFY list.

## 2026-10-04 - `egypt-final/` updated to v1.5 (3B rebate to all covered industry)
- **Task:** brought the hand-over folder in line with the final set v1.5. `update_egypt_final_v1_5.py` (in `egypt/supporting/AdHocRebuild/`) edited the three Word files in place and replaced the model workbook.
- **Changes:** 3B figures in all three documents (K -19.1 to -12.0 Mt, -3.2 to -2.0% of GHG, revenue 0.6 to 0.3 USD bn, deaths 491 to 330); 3B described as free allowances for all covered industry; new row in the "how the cut is built" table (+7.2 Mt) and a note; a 3B paragraph in the methodology; pointers to the CBAM calculation now say `Egypt_Model.xlsx`, sheet `Table2_Final`. `Egypt_Model.xlsx` = kernel v1.5 (byte copy of `egypt/final/`). `Egypt_CBAM_Obligations.xlsx` removed (retired; its content is in `Table2_Final`).
- **Caveats:** the Word files were edited with python-docx and not opened in Word; the summary was 2 pages before and gained one sentence (page count not re-checked, LibreOffice does not open files in this environment). The 3B column of "how the cut is built" shows rounding (-21.5 + 6.1 - 3.7 + 7.2 = -11.9 against -12.0). The workbook still carries version labels internally (Settings log).

## 2026-10-04 - `egypt-final/simple/Egypt_Simple.xlsx` (plain-words workbook)
- **Task:** a very small workbook for a non-specialist reader: sheet "How it works" (five plain steps), "Results" (six scenarios; final cut built live from four visible lines; CBAM bill as before/after index), "Try it" (one example product, yellow cells = the seven material parameters, green = worked out), and a hidden sheet "Other parameters" holding everything else. Builder: `egypt/supporting/AdHocRebuild/build_simple_workbook.py` (openpyxl, formulas).
- **Inputs:** `carveout_v1_5_results.json` (same source as the v1.5 documents).
- **Caveats:** simplified picture only; the Results numbers are typed from the full model (kernel v1.5), only the sums and the "Try it" example are live. The "Try it" example (cement clinker, USD 20) uses rounded inputs (process saving 6.5%, fuel saving 4.9%) and is illustrative, not a reproduction of the kernel. Not recalculated in Excel here (checked the formulas in Python: final cut equals K for all six scenarios; example gives -5.9% emissions per tonne, -12.4% total).

## 2026-10-04 - Output elasticity: evidence note and recommendation (no model change)
- **Task:** looked for a better basis for the uniform output elasticity -0.5 (`Manual inputs` rows 66-73). Wrote `egypt/supporting/OutputElasticity_Note_v0.1.md/.docx`.
- **Findings:** only cement matters (3.6 of the 3.8 Mt output-channel cut in 1A, because the carbon cost is 15% of the clinker price). Evidence for cement: demand elasticity about -0.02 to -0.16, pass-through 20-40%; steel demand -0.2 to -0.3, pass-through very wide (about 0.5 central); EU ETS firm studies find no detectable output fall. Recommended: cement -0.10 (range -0.03 to -0.30), steel and fertilisers -0.40, aluminium -0.50 (unchanged). Effect (approximate, outside the kernel): 1A cut -37.4 to -34.5 Mt, 3A -22.8 to -19.9, 3C -33.0 to -30.1; 3B unchanged.
- **Caveats:** values are judgements from sourced components (Low-Medium confidence), from web search summaries; the papers could not be opened (egress blocked). Nothing in the kernel or deliverables changed. Decision pending: apply cement -0.10 (kernel rebuild, new carve-out numbers, document updates) or keep -0.5 as a documented placeholder.

## 2026-10-08 - Final set v1.6: product-specific output elasticities (documents on mirror numbers; kernel builder and rebuild v0.5 drafted, not run)
- **Task:** apply cement -0.10 and the full recommended set (steel and fertilisers -0.40, aluminium -0.50; was -0.5 for all) per `OutputElasticity_Note_v0.1`, everywhere. Decisions: full set; one pass with approximate numbers; rebuild v0.5 included; set labelled v1.6.
- **New numbers (mirror, `make_carveout_v0_5.py`), 2030 K Mt old to new:** 1A -37.4 to -34.7; 2A -33.1 to -31.9; 2B -34.8 to -33.7; 3A -22.8 to -20.0; 3B -12.0 unchanged; 3C -33.0 to -30.8. Deaths: 1A 1,501 to 1,440; 2A 1,456 to 1,431; 2B 1,517 to 1,492; 3A 552 to 509; 3C 646 to 607. Revenue 3A 1.5 to 1.6; others within rounding. N 1A/3A -5.8 to -5.7, 2B -2.3 to -2.2, 3C -23.1 to -23.0; T (block emissions) 1A/3A -11.6 to -7.2, 2A -4.7 to -2.9, 2B -4.8 to -3.0, 3C -27.8 to -24.3. O (row O), J, M unchanged.
- **Mirror method:** emissions scale linearly with output, so the stored kernel block rows (policy rows 773-788, product outputs 675-682) and the block process revenue / 3C fund items are rescaled per product by (1 + dp)^eps_new / (1 + dp)^-0.5 and the carve-out arithmetic is rerun. Approximations: the 3C fund shadow price is not re-solved; kernel N is shifted by the change in the output weights; O is unchanged.
- **Outputs:** documents v1.6 in `egypt/final/` (methodology, carve-out note, final caveats, CBAM obligation note, tracked results text, version notes; v1.5 set in `egypt/archive/`), `egypt-final/` (three Word files; `simple/Egypt_Simple.xlsx` with cement default -0.1), scripts `make_carveout_v0_5.py`, `make_documents_v1_6.py`, `edit_methodology_v1_6.py`, `update_egypt_final_v1_6.py`, `build_v1_6.py` (kernel), `build_adhoc_rebuild_v0_5.py` and `recalc_and_check_adhoc_v0_5.py` (rebuild).
- **Verification:** `check_final_documents.py` (printed figures = mirror: 15 rows, 0 failures). Kernel v1.6 and rebuild v0.5 have NOT been built or run (Excel COM). `egypt/final/` still holds kernel v1.5 and `egypt-final/Egypt_Model.xlsx` is still v1.5 until `build_v1_6.py` runs; the documents state v1.6 numbers that come from the mirror.
- **Caveats:** the exact kernel numbers can differ from the mirror (largest expected for 3C, whose fund is re-solved in the kernel); the builder saves anyway, prints "DOCUMENTS MUST BE REGENERATED" if the printed figures differ, and the documents are rebuilt from `carveout_v1_6_results_live.json` (TODO, Final steps). Rebuild v0.5 notes and results are not written yet. Elasticity values are judgements (Low-Medium confidence); citations unverified against the papers.

## 2026-10-08 - Final set v1.6 finalised on the live kernel results
- **Task:** after `build_v1_6.py` and the rebuild v0.5 run (both on Windows, user), regenerated every document from `carveout_v1_6_results_live.json`, finalised the supporting notes and tidied the final folder.
- **Live kernel against mirror:** K, P, Q, T and O agree to rounding; the printed figures that changed are N for 1A/3A (-5.74 mirror to -5.79 live, still printed -5.8), 2B (-2.26, printed -2.3) and 3C (-23.10, printed -23.1), 3C deaths 606 (mirror 607), 3C K -30.82. Kernel `Table2_Final` mismatch count 0; `check_final_documents.py` 15 rows, 0 failures; kernel coverage J is 13.921 (live kappa) against 14 printed.
- **Outputs:** `egypt/final/` (v1.6): kernel, methodology, carve-out note, final caveats, CBAM obligation note, tracked results text, version notes (md sources in `md_sources/`); `egypt-final/` three Word files, `Egypt_Model.xlsx` (= kernel v1.6) and `simple/Egypt_Simple.xlsx` from the live numbers. Final caveats sections A-D now use the rebuild v0.5 and prototype v1.6 figures and no history wording (NORMS section 7). Rebuild notes: `MethodologyNote_v0.5`, `ResultsComparison_Table2_v0.5` (shortened: tables plus qualitative reasons; the old numeric decomposition of the prototype gap was dropped because it could not be recomputed outside Excel); v0.4 notes archived.
- **Caveats:** the new .docx files were generated with pandoc / python-docx and not opened in Word; row O still needs Carolyn's confirmation; evidence-note citations unchecked against the papers; the rebuild/prototype figures in the final caveats are as of the v0.5 / v1.6 runs.

## 2026-10-08 - TODO.md simplified
- **Task:** rewrote `TODO.md` to open work only: three checks for the user (Word check, Carolyn's confirmation of row O, citation check), seven modelling items (full-coverage EG3 run, EF VERIFY list, fp routing, block fuel-intensity channel, fuel-CO2 reconciliation, aligning the kernel's own composition with the 3B decision, items under review) and a short conventions list. Completed T1-T5, D1-D4 and the v1.4-v1.6 steps were removed (history is in this log). README and yaml pointers to TODO updated.
- **Caveats:** none.

## 2026-10-08 - Evidence check, EG3 full-coverage preparation, kernel-increment specs (no model change)
- **Task:** worked through the open modelling list as far as possible without Excel or CPAT.
- **Citations (`OutputElasticity_Note_v0.2`, replaces v0.1 in the archive):** checked by search summaries: EC / CE Delft-Oeko 2016 pass-through (cement 20-40%, steel 55-85%, correcting the earlier "about 0.5"), Ganapati-Shapiro-Walker 2020 (about 0.59 average), Colmer et al. 2025 (14-16% emission cut, no detectable output fall), cement demand (aggregate -0.02 to -0.04, median industry-level -0.10; the -0.16 attribution unconfirmed). Single-source: GTAP Armington values. Not found: a steel demand study and a numeric fertiliser demand elasticity. All fetches of the papers were blocked by the network policy. Methodology (parameter table) and `egypt-final` methodology text corrected for steel pass-through; recommended values unchanged.
- **Methodology wording:** Section 3 and the channel table said the proportional IPPU row "is removed"; now: removed for the CBAM block, kept for non-block IPPU. Typo fixed.
- **EG3 full coverage:** `EG3_FullCoverage_RunSpec_v0.1` (CPAT settings, acceptance check kappa about 1, export, regeneration, statements to rewrite); `cpat_run_constants.py` (reproduces every constant behind the final Table 2 from the csv); `make_carveout_v0_6.py` (mirror on a new csv; reproduces v1.6 on the current csv to 0.006); `build_v1_7.py` (kernel refresh of `CPAT_National`, stored snapshots and `Table2_Final`; drafted, not run). Indicative effect on the final Table 2 (1/kappa proxy): 3A -20.0 to about -29 Mt, 3B -12.0 to -15, 3C -30.8 to -40.
- **Kernel increments:** `KernelIncrements_Spec_v0.1`: fp routing about -0.3 Mt (optional), block fuel-intensity channel (none; double-counting risk with the carve-out; not recommended), 3B alignment of the kernel's own composition (reference sheet; label instead). No builders written for these three.
- **Caveats:** the indicative EG3 numbers are a proxy, not a CPAT result; `build_v1_7.py` has not been run and needs the new csv; the text of `Manual inputs` F66:F68 in the kernel still carries the old steel pass-through wording.

## 2026-10-05 - Kernel v1.7: CPAT_National linked to the new CPAT_Results sheet
- **Task:** in the user's `egypt/final/CPAT_Industry_Kernel_Egypt_v1.7.xlsx` (v1.6 plus a new raw CPAT export sheet `CPAT_Results`, runs EG1-EG5, 6,420 rows), replaced the stored values of `CPAT_National!L6:AE133` (2022-2041) with `=INDEX(CPAT_Results!$A:$AD,MATCH($H6&"_"&$C6,CPAT_Results!$F:$F,0),MATCH(L$5,CPAT_Results!$1:$1,0))` (key = CPAT code & "_" & run in `CPAT_Results` column F; year from row 5). Source column F and the section A band text updated. Done by Excel COM; `build_v1_7.py` was not used.
- **Verification:** all 128 keys found; 2,560 linked cells equal `CPAT_Results` exactly, no errors. 16 keys occur twice in `CPAT_Results` (co2.tot, rev.new.usd); the duplicates are identical, the first is used.
- **Caveats:** the new export changes the baselines as well as EG3 (about 2,060 of 2,560 cells differ from v1.6 in EG1, EG2, EG3 and EG4; e.g. `egy.air.mort` by about 31,000), so the new run is not an EG3-only replacement. EG5 is in `CPAT_Results` but not used. `CarveOut_Table2` (42 cells, from D22/D23: `Table2_Industry!G31/G32 & "|" & run` not found in `CPAT_National`) and `Table2_Final` (16 cells) show #N/A / #DIV/0!; these errors were already present in the v1.7 file before the links and are unchanged. Stored snapshots, documents and `egypt-final/` not refreshed.

## 2026-10-08 - Mitigation copy-paste prototype (v0.1)
- **Task:** first build of a copy-pasteable replacement for the CPAT mitigation module, price -> fuel use only, design 2 (scenario > year across; block > subsector > fuel down; per-block parameter sets on the left picked by scenario number). Goal, spec and decisions agreed in conversation (README in the folder).
- **Inputs:** legacy `CPAT 1.0pre_456_NoPropData.xlsb` (`Elasticities` rows 138-282 by income group; `Mitigation` rows 980-1009 EFs and unit conversions); `CPAT_PriceModule_Data_1.xlsx` `DomesticPrices` (221 countries, 2021-2024); kernel v1.6 `Data_Energy` (legacy Mitigation rows 583-602) and `Data_Macro` (legacy row 2446); CPAT public documentation (github.com/cpmodel/cpat_public, Mitigation 3.3.3 and 3.3.5); `coded` `ec.py` (subsector groupings, coal/gas price rule).
- **Outputs:** `excel_ai_new/mitigation/`: `CPAT_Mitigation_CopyPaste_v0.1.xlsx`, `build_v0_1.py`, `extract_data_v0_1.py`, `check_v0_1.py`, `check_report_v0.1.md`, `data/*.csv`, `README.md`. Checks (LibreOffice recalculation): 0 errors; one R1C1 formula per block across 128 rows x 2 groups; copied group = source group (diff 0) and copied group with carbon price 0 = baseline (diff 0); independent Python recomputation max relative diff 5e-15. Result: $20/t from 2027 lowers total fuel use by 10.7 % in 2027-2030 (Egypt's low, subsidised prices make the relative price rise large).
- **Caveats:** (1) The CPAT documentation tables (Figures 54, 57) differ from the legacy workbook: the workbook applies the developing-country adjustment to the usage elasticity (LIC/LMIC/UMIC = HIC - 0.1), not to the efficiency elasticity as the docs say, and several base values differ (e.g. residential gas income elasticity 0.3 vs 0.6). Legacy values used (user decision). (2) Simplifications vs CPAT: no per-capita GDP adjustment of income elasticities (user decision), no Covid factor, no shadow prices or additional efficiency gains, no self-generated renewables, jet fuel or road biofuel split, no electricity; pre-tax prices flat at the 2022 supply cost (growth 0 %, REVIEW); base tax = retail - supply cost (includes excise, subsidies and VAT) held constant. (3) Assumptions to review: EF sector for foo and srv = res, for transport subsectors = rod, for oen = ind; elasticity sector for foo and oen = ind (as `coded`); IIASA EFs without the Egypt inventory adjustment (0.93) for the tax base; carbon price taken as $/tCO2 in the same (2022 current) dollars as prices. (4) Base-year energy use, GDP growth and EFs are Egypt only; other countries return #N/A. (5) Built with openpyxl, not Excel COM (NORMS/TODO convention); verified in LibreOffice, not yet opened in Excel. (6) Years start after the key and parameter columns, not in column K (NORMS 1.1 deviation, noted in the ReadMe). (7) Not yet compared with legacy CPAT results (bucket 4).

## 2026-10-08 - Mitigation copy-paste prototype (v0.2)
- **Task:** revise v0.1 after review: lookups separated from formulas (new `Inputs` sheet, one row per fuel|subsector, elasticities expanded to that taxonomy); four parameter columns D:G, hidden by default, between Sector and Description; parameters global (scenario-specific parameter sets and scenario numbers removed; scenarios differ only in the carbon price); base year 2022 in column L as in legacy Mitigation; 2023-2034 plain formulas and 2035 named LAMBDAs (`PRETAX`, `TAX`, `POSTTAX`, `FUELUSE`, orange) that can be dragged back over the row.
- **Inputs:** v0.1 (`Old/`), `data/*.csv` (unchanged), `excel_ai_new/distribution/LESSONS_LEARNED.md` (LAMBDA encoding), kernel v0.1b LAMBDA (encoding pattern).
- **Outputs:** `excel_ai_new/mitigation/CPAT_Mitigation_CopyPaste_v0.2.xlsx`, `build_v0_2.py`, `check_v0_2.py`, `check_report_v0.2.md`, README; v0.1 files moved to `Old/`; Settings version log row added. Checks: one R1C1 formula per block for base year, plain years and the LAMBDA year; LAMBDA encoding (`_xlfn.LAMBDA`, every parameter `_xlpm.`); LAMBDA bodies expanded and plain formula dragged into 2035 both match the independent Python recomputation (5e-15); scenario-copy test diff 0; regression vs v0.1 diff 0 on all 14,336 block cells.
- **Caveats:** (1) LibreOffice 24.2 cannot evaluate LAMBDA, so the 2035 column was verified by expansion, not by Excel; LESSONS_LEARNED warns that hand-encoded LAMBDA names can be stripped by some Excel builds - if Excel shows a repair prompt or #NAME? in 2035, drag 2034 forward (or re-create the names in Name Manager from the ReadMe). Not yet opened in Excel. (2) Further NORMS 1.1 deviation: Description..Output Code move to H:K and Input Code, Note and Helper are dropped. (3) All v0.1 caveats on simplifications and assumptions still apply.

## 2026-10-08 - Mitigation copy-paste prototype (v0.3)
- **Task:** full CPAT output codes with country and scenario, repeated for each scenario: column A now holds the variable code (`gdp.pos.pct`, `cptraj`, `sp`, `tax`, `atp`, `ener`, `ener.chk`, `ener.ref`, `ener.pct`); Description, Unit and Source (H:J) are looked up from a new `Variables` sheet; each scenario group starts with a code column (K for scenario 1, base year 2022 still in L) that builds `country.mit.<variable>[.<subsector>.<fuel>][.<suffix>].<scenario>` (e.g. `egy.mit.ener.rod.gso.e.1`, as legacy row 5430). The scenario number sits at the top of the code column; scenario 1 is typed and every later group is previous + 1, so a pasted group numbers itself.
- **Inputs:** v0.2 (`Old/`); legacy Mitigation output codes (rows 2498 `sp...a.N`, 5416 `atp...e.N`, 5430 `ener...e.N`, 2446 `gdp.pos.pct.N`; `cptraj.N` from the CPAT outputs csv).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.3.xlsx`, `build_v0_3.py`, `check_v0_3.py`, `check_report_v0.3.md`, README; v0.2 files moved to `Old/`; Settings version log row. Checks: one formula per label column and per code column (542 rows), expected codes for 8 sample cells, pasted groups number themselves (3, 4), regression vs v0.2 diff 0, all v0.2 checks still pass.
- **Caveats:** (1) Codes follow the legacy pattern but use the subsector where legacy prices use the price sector (`egy.mit.sp.ind.coa.a.1`) and legacy `atp` is in $/liter for liquids while ours is $/GJ; `tax` and the totals/check codes (`ener.chk`, `ener.ref`, `ener.pct`, `...rod.all...`) are new, not legacy. (2) Labels for total rows rely on the `all` rows added to Mapping (rows 21 and 32). (3) All v0.1/v0.2 caveats still apply; still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.4)
- **Task:** roll up the sections: a row outline groups each block's rows under its band row (+/- on the band; summary row above), blocks collapsed by default, totals grouped but open.
- **Inputs:** v0.3 (`Old/`).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.4.xlsx`, `build_v0_4.py`, `check_v0_4.py`, `check_report_v0.4.md`, README; v0.3 files moved to `Old/`; Settings version log row. Checks: outline levels and collapsed state per block, all v0.3 checks, regression vs v0.3 diff 0.
- **Caveats:** (1) openpyxl drops `sheetFormatPr/@outlineLevelCol`; the builder adds it after saving (`fix_outline_levels`) so the hidden D:G column group gets its button - v0.2/v0.3 lacked it. (2) Copying a scenario group or dragging across includes collapsed (hidden) rows, which is intended; a filtered view would not. (3) Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.5)
- **Task:** white text in the green bands; a white summary line directly under each band, visible when the block is rolled up (the +/- now sits on that line): fuel use = total fuel use (`egy.mit.ener.all.all.e.N`); tax = policy carbon price (new variable `cptraj.ref`, repeating row 7); pre-tax and after-tax price = no total (prices are not additive, line left empty with a note). The totals section's own grand-total row is dropped (it duplicated the fuel-use summary line); its check row now tests totals by subsector and by fuel against the summary line.
- **Inputs:** v0.4 (`Old/`).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.5.xlsx`, `build_v0_5.py`, `check_v0_5.py`, `check_report_v0.5.md`, README; v0.4 files moved to `Old/`; Settings version log. Checks: all earlier checks, white bold band text, summary lines equal the carbon price and the sum of the 128 fuel-use rows, outline under the summary lines, regression vs v0.4 diff 0.
- **Caveats:** (1) Every block is one row taller (band + summary line + 128 rows + blank), so all row numbers below row 9 shift by 1-4 against v0.4. (2) Bug found and fixed: the builders v0.3 and v0.4 wrote earlier version-log rows with the current version number (shipped v0.3 shows the v0.2 row as 0.3; v0.4 shows the v0.2 and v0.3 rows as 0.4); v0.5 hard-codes each row's version. Old workbooks are left as shipped. (3) `cptraj.ref` and the totals-section codes are new, not legacy. (4) Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.6, bucket 6a: MTInputs and carbon price)
- **Task:** policy inputs per scenario. New sheet `MTInputs`: the template (`templates/MTInputs_template.xlsx`, legacy row structure, names, units, `NameOfParameter`) copied cell by cell into A:H, plus one *Used for calculation* column per scenario from column J (number row 5, auto-numbered; name row 6; Scenario ID and name rows 10/12 link to them). `Mitigation` gets a scenario-number row (5), the scenario name from MTInputs (row 6), a carbon-tax band with lookup rows for `CPIntro`, `CPLevelStart`, `CPLevelTarget`, `CPOutro`, `ExtendCarbonPriceBeyondOutro` (rows 9-13, rolled up) and the carbon price trajectory as a formula (row 14, as legacy rows 2248/2251), replacing the typed carbon prices. Decisions: MTInputs columns A:H unchanged; scenario columns from J; ETS left out for now; `MCovOen` = FALSE.
- **Inputs:** v0.5 (`Old/`); `templates/MTInputs_template.xlsx`; legacy Mitigation rows 2188-2252 and 8579-8582 (carbon tax settings and trajectory).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.6.xlsx`, `build_v0_6.py`, `check_v0_6.py`, `check_report_v0.6.md`, README; v0.5 files moved to `Old/`. Checks: MTInputs A:H = template (0 cells differ, D:E hidden); a scenario with the legacy Egypt settings (2026, 0 -> 50 by 2030, Linear*) reproduces legacy row 8582 (0, 12.5 ... 50, 62.5 ... 112.5); copied MTInputs columns and Mitigation groups number and name themselves; scenario 4 with zero carbon price in MTInputs = scenario 1; regression vs v0.5 diff 0 (blocks and carbon price); all earlier checks pass.
- **Caveats:** (1) Scenario columns start from the template's *Used for calculation* values (an Egypt run: carbon tax 0 -> 50 by 2030 from 2026), overridden for our scenarios: scenario 1 carbon price 0, scenario 2 $20 from 2027 (`CPOutro` 2030, start = target), `MCovOen` FALSE in both; overrides are in red. (2) Only the carbon-tax parameters are used so far; coverage still comes from `Mapping` (oen 0) until bucket 6b switches to the `MCov*` switches. (3) Nominal vs real (`NomorReal`), the exponential option (`CTaxTrajectoryType`) and CPI conversion (legacy row 2249) are not implemented: the trajectory is the real, linear path. (4) Lookup ranges cover MTInputs scenario columns J:AZ (41 scenarios). (5) Rows below 8 shift by 7 against v0.5. (6) Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.7, bucket 6b: policy wedges, legacy section layout)
- **Task:** (1) legacy CPAT visual structure: numbered sections 1. Policies, 3. Power sector (placeholder), 5. Transport, 6. Buildings, 7. Industrial, 8. Other energy use, 11. Results; within a sector section subsector > variable > fuel (as legacy rows 5538-5560), with a total fuel-use line per sector and per subsector. (2) Policy wedges per fuel x subsector: `ctxnew` (carbon price x EF x MTInputs fuel and sector coverage `MCov*`), `ntx` (fuel price reform path / GJ per unit), `nce` (total new policy), `tax` = base tax + `nce`, and the feebate shadow price `shp` (calculated, not yet used in fuel use). Section 1 reads all inputs from MTInputs by row and scenario number and computes the carbon price, fuel price reform and feebate paths. (3) The carbon-price line repeated under the tax block (v0.5-v0.6, `cptraj.ref`) is removed. Decisions: no ETS yet; `MCovOen` FALSE.
- **Inputs:** v0.6 (`Old/`); `templates/MTInputs_template.xlsx` (rows 18-47, 53-82, 140-169, 265); legacy Mitigation section layout (rows 2174-2447, 4302, 5538-5560, 5665-5690, 6063-6087) and codes (`ctxnew` row 2510, `ntx` 2512, `nce` 2514, `shp` 2377).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.7.xlsx`, `build_v0_7.py`, `check_v0_7.py`, `check_report_v0.7.md`, README; v0.6 files moved to `Old/`; Settings version log. Checks: one formula per variable (base, plain years, 2035) across 128 rows x 2 scenarios, per D:G column, Section-1 inputs and paths, labels and codes; values vs independent Python recomputation (5e-15) for scenarios 1-2 and test scenarios 5 (legacy carbon tax = legacy row 8582), 6 (fuel price reform), 7 (feebates: shadow price non-zero, fuel use unchanged); copied scenarios = source; regression vs v0.6 on 1,094 shared output codes (max diff 1e-15); outline levels; MTInputs = template.
- **Caveats:** (1) Fuel price reform and feebate paths are assumed linear from start to target year and flat afterwards; the legacy formulas could not be read (values are zero in the Egypt run). Fuel price reform increases are in the MTInputs price units ($/GJ, $/liter, $/bbl) and converted with the GJ-per-unit factors; electricity rows are read but unused. (2) Feebate sector for food & forestry and services = residential, other energy use = industry (assumptions). (3) Biomass has no carbon-tax switch in MTInputs; its coverage row is a typed FALSE (biomass EF is 0 anyway). (4) `ctxnew`, `ntx` and `shp` pick a Section-1 row by position (`INDEX(range, position)`); positions come from Inputs (data step). (5) The shadow price is not yet in the fuel-use equation; ETS, subsidy phase-out, price liberalisation, methane fee and CBAM process emissions are not implemented. (6) Power sector is a placeholder section. (7) Row numbers change completely against v0.6 (codes are stable). (8) Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.8: shadow price on the efficiency margin)
- **Task:** feed the feebate shadow price into fuel use as legacy CPAT: the efficiency term uses `((atp + shp)/(atp_prev + shp_prev))^eps_F` (all ^(1+eps_U)), the usage term `atp` only (`coded` `ec.py`, legacy rows 2374-2419). Section 1 gains shadow prices by sector ($/tCO2: power, transport, residential, industry = feebate path; legacy rows 2345-2349) and the share of the shadow price impacting efficiency by subsector (`ssc` = feebate coverage x adjustment 1.0; legacy rows 2403-2419; `coded` default for feebates). `shp` = sector shadow price x EF x `ssc`; `FUELUSE` LAMBDA takes the shadow prices (10 arguments). User decisions: one default for all paths (linear continuation after the target year; the carbon price keeps its MTInputs switch); feebate grouping as the legacy main grouping (buildings = res, foo, srv -> residential rate); biomass carbon-tax coverage TRUE like the other fuels (EF 0); positional INDEX picks accepted but kept rare.
- **Inputs:** v0.7 (`Old/`); `coded/cpat_model/components/energy_consumption/ec.py` and `policies/shadow_prices.py`; legacy Mitigation rows 2345-2420.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.8.xlsx`, `build_v0_8.py`, `check_v0_8.py`, `check_report_v0.8.md`, README; v0.7 files moved to `Old/`; the MTInputs template path in `Old/build_v0_6.py`, `Old/build_v0_7.py` and `build_v0_8.py` now searches upward (archived builders run from `Old/`; output unchanged). Checks: all v0.7 checks; shadow-price paths uniform; feebate test: fuel use matches Python (5e-15) and falls only in subsectors with feebate coverage and a non-zero rate (road -11.1 %, iron & steel -12.3 % in 2035 at 10 -> 50 / 5 -> 25 USD/tCO2 from 2027 to 2030, continuing linearly); regression vs v0.7 on 2,322 shared codes diff 0 (intended change: biomass coverage switch).
- **Caveats:** (1) The scenario columns copy the template's feebate coverage switches (TRUE for most industrial subsectors and other energy use); with zero feebate rates they have no effect. (2) Other energy use takes the industry feebate rate (legacy groups it under 'oth'). (3) Elasticity grouping unchanged: food & forestry uses industry elasticities (as `coded` EC_SECTORS) although it sits in the buildings section - open question for the user. (4) Regulations (MTInputs rows 247-250 adjustments) and ETS are not yet shadow-price sources; additional policy-induced efficiency gains (rows 242-245) not yet in the fuel-use equation. (5) Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.9: domestic price projection in real terms)
- **Task:** Implement in one step the legacy domestic price projection, and write out the real/nominal assumptions explicitly. The user decided not to track values after 2030, and to keep one index only if it matches legacy up to 2030.
- **Changes:**
  - New section 2 (12 price fuels) with:
    - `gp` (international prices: MTInputs source and High/Low adjustment, country gas market);
    - `sp` (data to 2024, then fixsp + floating part x gp ratio);
    - `txo` (data, then the legacy pass-through rule);
    - `rpb` = (sp + txo)(1 + VAT).
  - Top rows `infl` (US CPI index) and `defl` (US GDP deflator index), both = 1 in ResultsYear 2026.
  - `NomorReal` in section 1: a nominal carbon price is multiplied by `infl`.
  - Per subsector: `atp` = max(rpb + nce(1 + VAT), 0.01); `sp` and `tax` removed.
  - New sheets `Inputs_prices` (data step), `Prices_int` and `PriceAssump`; Settings C8-C12.
  - LAMBDAs `SUPPLYCOST` and `OTHERTAX` replace `PRETAX` and `TAX`; `POSTTAX` now takes the VAT rate.
- **Index decision:** The CPI and deflator indices differ before 2030 by up to 1.2% (2022: 1.137 vs 1.124; 2030: 0.918 vs 0.929). One index would not reproduce legacy, so both are kept: CPI for domestic data and nominal inputs, deflator for international prices (as legacy).
- **Inputs:** v0.8 (`Old/`); `coded/cpat_model/components/prices/prices.py`, `domestic_prices.py` and `international_prices.py`; legacy Mitigation rows 452/455/456/467/725 and 633-695; legacy `Prices_int` regional assumptions; `extract_data_v0_2.py` -> `data/prices_int.csv`, `weo_us.csv`, `price_assumptions.csv`.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.9.xlsx`, `build_v0_9.py`, `check_v0_9.py`, `check_report_v0.9.md`, `extract_data_v0_2.py`, `PriceProjection_Method_v0.2.md` (assumptions A1-A10), README. v0.8 files, method note v0.1 and `extract_data_v0_1.py` moved to `Old/`.
- **Checks:**
  - Every new block has one R1C1 formula, with history and projection in the same formula.
  - gp, sp, txo, rpb and all subsector variables match an independent Python recomputation from the CSVs (max relative diff 1e-14). This covers scenarios 1-2; price source IMF-WB* with High adjustment and a nominal carbon price; and global price controls None and Manual.
  - Pass-through 0 keeps rpb at its 2024 value.
  - Regression vs v0.8: 1,286 shared non-price codes diff 0. atp, ener and sp change by intent.
- **Results (Egypt):**
  - Baseline fuel use: 49.7 Mtoe (2022), 62.5 (2023), 68.9 (2024), 78.8 (2027), 105.3 (2030). In v0.8 it was 55.4 (2027) and 60.7 (2030).
  - $20/t from 2027: -17.5% (2027) and -30.1% (2030) against the baseline. In v0.8 it was -10.7% in 2027.
- **Caveats:**
  1. Legacy rules are copied as they are, including two quirks:
     - (a) pass-through 0.5 or 0.8 makes `txo` jump in the first projected year;
     - (b) other oil products have pass-through 1 hardcoded but keep their negative fixed tax. Their retail price falls with the oil price: 3.79 $/GJ (2024), 0.23 (2030), 0.01 floor from 2031. Baseline oop fuel use therefore rises 10x by 2030 (3.0 to 29.2 Mtoe) and explodes after it. This drives most of the higher baseline and the large carbon-price effects (other manufacturing, fuel transformation, navigation). Proposed fix pending user decision.
  2. Real prices fall sharply from 2022 to 2024 in the data (devaluation; gasoline 15.1 to 8.4 $/GJ real), so modelled fuel use jumps +26% in 2023 and +10% in 2024. Legacy also models from the 2022 base year.
  3. Historical oil-product retail prices follow legacy (sp + txo; Egypt VAT rate on oil products is blank = 0), so they are 14% below the dataset `rp`, which includes VAT.
  4. Margins and production costs (2022 nominal) are converted with `infl(2022)`; `coded` applies no conversion. To check in bucket 5.
  5. ResultsYear and price controls are global (scenario 1 column). Source, adjustment and NomorReal are per scenario.
  6. Scenario 1 takes the template's *Used for calculation* source `IMF` (the legacy default is `IMF-WB*`).
  7. The legacy NoPropData price forecasts are #N/A, and data vintages differ, so the projected prices cannot yet be validated against legacy numbers.
  8. Still not opened in Excel.

## 2026-10-08 - Mitigation copy-paste prototype (v0.10: other oil products, VAT assumption)
- **Task (user decisions):** (1) Treat other oil products like the other oil products. (2) Make an assumption for Egypt's VAT rate. (3) Mark changed data clearly in a bright colour.
- **Changes:**
  - Other oil products: pass-through and margin now come from the IMF dataset (Egypt: 0 and 7.95 $/bbl) instead of the legacy hardcodes 1 and 0.
  - VAT rate: the dataset rate where filled; otherwise the general rate `VAT_WEO` (Egypt 14%) for residential coal and gas and the all-sector oil products, and 0 for power, industry (credited to firms) and biomass (informal).
  - The changed cells in `Inputs_prices` (VAT consumer flag, VAT assumption, oop pass-through and margin) are bright yellow with red bold text; the ReadMe and the method note (A10, A11) say so.
- **Evidence for the VAT assumption:** the Egypt dataset's own retail prices imply it: rp = (sp + txo) x 1.14 for residential gas, gasoline, diesel, LPG, kerosene and other oil products, and rp = sp + txo for power and industry.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.10.xlsx`, `build_v0_10.py`, `check_v0_10.py`, `check_report_v0.10.md`, `PriceProjection_Method_v0.3.md`, README. v0.9 files and method note v0.2 moved to `Old/`.
- **Checks:** PASS. The price chain and fuel use match the independent Python recomputation (5e-15), and the bright marking is checked. Regression vs v0.9: 1,300 unaffected codes diff 0; 646 price and fuel-use codes change by intent.
- **Results (Egypt):**
  - Other oil products: retail price held at 4.32 $/GJ from 2024 (v0.9: 0.23 in 2030). Their fuel use is 4.9 Mtoe in 2030 (v0.9: 29.2).
  - Gasoline retail price 9.58 $/GJ (v0.9: 8.40, without VAT).
  - Baseline total 74.1 Mtoe (2027) and 81.0 (2030).
  - $20/t from 2027: -15.1% in 2027 and 2030.
- **Caveats:**
  1. The VAT rule is an assumption. It reproduces Egypt's data but is not a statement of Egyptian tax law: petroleum products may be under a schedule tax rather than standard VAT. The fiscal split between VAT and excise does not affect fuel use, but it will matter for revenue.
  2. The VAT assumption applies to any country with blank dataset rates. Check it per country.
  3. The legacy `txo` jump at pass-through 0.5 or 0.8 is still copied.

## 2026-10-09 - Mitigation copy-paste prototype (v0.11: ETS, shadow prices, existing taxes and subsidies, 2040, LAMBDA right column)
- **Task (user decisions):**
  1. Food & forestry takes the buildings elasticities. Services is used, because legacy groups food & forestry with services as Commercial.
  2. Differences with legacy go in a new tab.
  3. Existing taxes and subsidies, (a) ready for revenue and (b) as an input for a later per-fuel policy.
  4. ETS and feebates with sectoral shadow prices; the ETS is as effective as a carbon tax.
  5. Complete the prices section and prepare revenues.
  6. Separate column blocks for history and projection. The LAMBDA (which may hold the IF) goes in the right column of every calculated row.
  7. Extend to 2040 with LAMBDAs for the baseline and the policy scenario.
- **Changes:**
  - Horizon 2022-2040.
  - Section 1:
    - New ETS inputs: MTInputs rows 84-92 and coverage rows 99-115.
    - Effective ETS coverage `etsc`.
    - ETS permit price `ets.p` = the carbon price path once the ETS applies.
    - Auctioned share `ets.a`: linear, constant after the target year.
    - Regulation shadow prices `reg`: placeholder 0.
    - `shps` = feebates + regulations.
  - Subsectors:
    - New variable `ets` = permit price x EF x effective coverage.
    - `ctxnew` x (1 - ETS coverage), so there is no double pricing.
    - `nce` = ctxnew + ets + ntx.
  - Section 2 adds, per price fuel:
    - `vat`: VAT payment before new policies;
    - `etx` = max(txo, 0): existing tax;
    - `esub` = max(-txo, 0): existing consumer subsidy;
    - `esubpu`: the subsidy per MTInputs price unit.
  - Section 12 Revenues: band with the revenue recipe and the rows it uses.
  - Sheet `LegacyDiff` (second tab, 21 rows).
  - 19 named LAMBDAs; every calculated row calls one in 2040. `SUPPLYCOST` and `OTHERTAX` hold the history/projection IF. Plain blocks: history 2022-2024 and projection 2025-2039, with no switch.
  - Method note v0.4.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.11.xlsx`, `build_v0_11.py`, `check_v0_11.py`, `check_report_v0.11.md`, `PriceProjection_Method_v0.4.md`, README. v0.10 files and method note v0.3 moved to `Old/`.
- **Checks:** PASS.
  - One R1C1 formula per variable and column block.
  - The right column has a LAMBDA on exactly the calculated rows (data lookups and sums stay plain).
  - Python recomputation matches for three variants (LAMBDA expanded; 2039 dragged; LAMBDA copied back over whole rows) and for test scenarios 5-9 and price controls None/Manual.
  - ETS test (scenario 9: power and industry in the ETS, same price): nce, atp and fuel use equal the carbon-tax scenario exactly, and the cement carbon tax is 0.
  - Regression vs v0.10, 2022-2035: 1,902 codes diff 0. Only food & forestry fuel use and its aggregates change (food & forestry 2027: 1,740 to 1,441 ktoe).
- **Results (Egypt):**
  - Baseline 73.8 Mtoe (2027), 92.1 (2035), 104.4 (2040).
  - $20/t: -14.9% throughout.
  - Existing consumer subsidies, 2024 ($/GJ real): gas power 6.2, residential 12.4, industry 4.6; gasoline 13.4 (0.47 $/liter); diesel 15.0 (0.56 $/liter); LPG 18.2; kerosene 12.6; other oil products 11.2 (68 $/bbl).
- **Caveats:**
  1. ETS price is not cap-based: the cap needs emissions (next buckets). Users set the expected permit price through the carbon price inputs.
  2. The full permit price enters the price whatever the auction share: free allocation keeps the marginal incentive.
  3. The existing tax/subsidy split is by sign of txo. Legacy splits into fixed tax, fixed subsidy and floating part, with the same totals.
  4. Changing the last historical year (Settings C10) now also needs the history/projection blocks re-dragged; the LAMBDA column adapts by itself.
  5. 2031-2040 compute but are not a legacy target.
  6. Feebates are revenue-neutral; revenue is not yet calculated.

## 2026-10-09 - Mitigation copy-paste prototype (v0.12: revenues)
- **Task (user):** Revenues, with existing taxes and subsidies and new revenues as separate calculations.
- **Changes:** Three new variables per subsector and fuel, in USD million real 2026 (Settings C13 = 0.041868 PJ/ktoe):
  - `rtx` = fuel use x PJ/ktoe x (existing tax `etx` + VAT `vat` of the price fuel);
  - `rsub` = fuel use x PJ/ktoe x existing subsidy `esub` (cost, positive);
  - `rnew` = fuel use x PJ/ktoe x (`ctxnew` + `ntx` + `ets` x auctioned share + `nce` x VAT rate). Feebates are revenue-neutral.

  Each has a plain block plus a 2040 LAMBDA (`REVENUE`, `NEWREVRATE`). Section 12 shows totals and splits by sector section for each, `rnet` = rtx - rsub, `rtot` = rnet + rnew, `rtot.ref` (scenario 1) and `rtot.chg` (fiscal effect). LegacyDiff gains a revenue-structure row (22 rows).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.12.xlsx`, `build_v0_12.py`, `check_v0_12.py`, `check_report_v0.12.md`, README. v0.11 files moved to `Old/`.
- **Checks:** PASS.
  - Revenue rows: one formula per block, with a LAMBDA in 2040.
  - Per-row revenues and section-12 totals match the independent Python recomputation (5e-15) in all variants and test scenarios, including ETS auction shares in scenario 9.
  - Sector splits sum to totals; no new revenue in scenario 1.
  - Regression vs v0.11: 2,390 shared codes diff 0.
- **Results (Egypt, USD million real 2026):**

  | | Existing taxes | Existing subsidies | New revenue | Fiscal effect vs baseline |
  |---|---|---|---|---|
  | Baseline 2022 | 1,952 | 27,875 | - | - |
  | Baseline 2030 | 1,919 | 29,036 | - | - |
  | $20/t, 2027 | 1,529 | 26,058 | 3,818 | +8,533 |
  | $20/t, 2030 | 1,656 | 24,372 | 4,168 | +8,568 |

  The $20/t effect is mostly subsidy savings from lower use of subsidised fuels.
- **Caveats:**
  1. Subsidies are price-gap subsidies against supply cost (IMF method), not budget outlays.
  2. Excludes power and electricity, including gas to power. Gas for power has a subsidy of 6.2 $/GJ but no power fuel use yet.
  3. No producer subsidies, no GDP feedback, and existing taxes on fuels only.
  4. Revenue in years after 2030 is not a legacy target.

## 2026-10-09 - Mitigation copy-paste prototype (v0.13: CO2 emissions)
- **Task (user):** Emissions next, CO2 first.
- **Changes:**
  - New variable `co2` per subsector and fuel = fuel use (ktoe) x 0.041868 PJ/ktoe x EF (tCO2/GJ, IIASA, `EF_GHG`; biomass 0), in MtCO2. It has a plain block and the 2040 LAMBDA `EMISSIONS`.
  - Section 13: total, by sector section, by fuel, scenario 1 reference, and change vs scenario 1 in MtCO2 and %.
  - LegacyDiff gains an emissions row (23 rows).
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.13.xlsx`, `build_v0_13.py`, `check_v0_13.py`, `check_report_v0.13.md`, README. v0.12 files moved to `Old/`.
- **Checks:** PASS.
  - `co2`: one formula per block, with a LAMBDA in 2040.
  - Per-row CO2 and the section-13 total match the independent Python recomputation (5e-15) in all variants and test scenarios.
  - Sectors and fuels sum to the total; biomass is 0; there is no change vs scenario 1 before 2027.
  - Regression vs v0.12: 3,196 shared codes diff 0.
- **Results (Egypt, MtCO2, fuel combustion excluding power):**

  | Year | Baseline | $20/t from 2027 |
  |---|---|---|
  | 2022 | 134.8 | 134.8 |
  | 2024 | 188.9 | 188.9 |
  | 2027 | 203.5 | 172.5 (-15.2%) |
  | 2030 | 222.3 | 188.6 (-15.2%) |
  | 2040 | 287.5 | 244.0 (-15.1%) |
- **Caveats:**
  1. 2022-2024 rises +40%. Fuel use in 2023-2024 is modelled from the 2022 base with the large real price falls in the data (devaluation; gasoline -44% real), not taken from energy balances. This is likely too high against observed emissions. Options: use observed energy use for 2023-2024 when available, or start the response from the last price year.
  2. No inventory adjustment of EFs.
  3. No power sector (gas and oil to power are a large share of Egypt's CO2).
  4. No process emissions, CH4, N2O or local pollutants yet.
  5. The ETS price is still not cap-based. Emissions now exist, so a cap can be added next.

## 2026-10-09 - Check: does legacy CPAT show the 2022-2024 jump? (no model change)
- **Source:** a real legacy CPAT run for Egypt, `egypt/supporting/AdHocRebuild/cpat_outputs_egypt_2022_2041.csv` (EG1 baseline, CPAT Outputs sheet, proprietary data), compared with v0.13 scenario 1 (MtCO2, energy-related).
- **Findings:**

  | Sector | Run | 2022 | 2023 | 2024 | 2027 | 2030 |
  |---|---|---|---|---|---|---|
  | Residential | legacy | 15.8 | 17.4 | 22.3 | 23.3 | 24.7 |
  | Residential | v0.13 | 13.9 | 19.0 | 22.3 | 23.3 | 24.6 |
  | Industry | legacy | 59.6 | 58.9 | 69.8 | 80.2 | 89.0 |
  | Industry | v0.13 | 64.3 | 80.3 | 87.2 | 95.4 | 106.2 |
  | Transport | legacy | 53.0 | 57.3 | 48.1 | 72.8 | 116.4 |
  | Transport | v0.13 | 53.4 | 67.4 | 74.8 | 79.8 | 86.3 |

  - Residential: legacy shows the same jump (+41% by 2024), and the trajectories coincide from 2024.
  - Industry: legacy +17% by 2024; v0.13 +36%.
  - Transport: legacy falls in 2024 and then rises steeply; v0.13 rises early and more slowly.
  - Total energy CO2 incl. power: legacy +10% (210.9 to 232.3).
- **Caveats:**
  1. The legacy run used different price data (proprietary vintage; its 2023-2024 prices are not in the NoPropData file).
  2. Sector groupings may differ: legacy industry may exclude fuel transformation; v0.13 industry includes it.
  3. Legacy transport may include dynamics not modelled here.
  4. To confirm in bucket 5 with the legacy price inputs.

## 2026-10-09 - Mitigation copy-paste prototype (v0.14: corrected Egypt price block)
- **Task (user):** The user supplied "the whole price block for Egypt, with correct data" (`Egypt_Price_Data.xlsx`, legacy Prices_dom layout, 2019-2024, plus info columns on sources, reliability and last data year).
- **Changes:**
  - File stored as `data/source/Egypt_Price_Data_2026-10-09.xlsx`.
  - `update_prices_egypt_v0_1.py` replaces the Egypt rows of `data/prices_dom.csv` for the shared columns and adds 2019-2020. Non-Egypt rows are byte-identical; the extra info columns are not used.
  - 291 changed or added cells are listed in `data/prices_dom_changes.csv` and marked bright yellow with red text in the `Prices_dom` sheet.
  - VAT rule: the dataset rate wherever the cell is filled (explicit 0 included); the v0.10 VAT_WEO assumption applies only to blank cells.
  - LegacyDiff gains an "Egypt price data" row (24 rows).
- **What the correction changes:**
  1. Supply costs and retail prices: changes within rounding, except 2024 gas (-1%) and some coal values.
  2. Excise and other taxes of gas and oil products: retail price = supply cost + txo, with VAT rates explicitly 0 (only residential coal 14%). Any VAT sits inside txo, so the v0.10 VAT assumption would have counted VAT twice; under the new rule it no longer applies to Egypt.
  3. Electricity supply costs are now filled (not used yet).
- **Checks:** PASS.
  - Prices, taxes, fuel use, revenue and CO2 match the independent Python recomputation from the updated CSV, including the VAT blank/explicit rule.
  - All 291 changed cells are marked with the new values; no other country is marked.
  - Regression vs v0.13: 1,648 codes that do not depend on Egypt prices diff 0; 1,836 price-dependent codes change by intent.
- **Results (Egypt):**

  | | v0.13 | v0.14 |
  |---|---|---|
  | Baseline CO2 2022 / 2024 / 2030 (Mt) | 134.8 / 188.9 / 222.3 | 134.8 / 187.5 / 220.7 |
  | $20/t effect on CO2 | -15.2% | -13.9% (no VAT on new policies for gas and oil products) |
  | Existing tax revenue 2022 (USD m) | 1,952 (mostly assumed VAT) | 25 |
  | Existing subsidies 2022 (USD m) | 27,875 | 26,077 |
  | $20/t fiscal effect 2030 (USD m) | +8,568 | +7,683 |
- **Caveats:**
  1. The 2022-2024 jump in fuel use and CO2 remains: the corrected block has the same large real price falls. The gap to the legacy run in industry and transport therefore has other causes (to investigate in bucket 5).
  2. Other oil products keep the legacy retail-price rule (sp + txo); the dataset rp is 14% higher for them.
  3. 2019-2020 are stored but not used (history starts 2021).

## 2026-10-09 - Mitigation copy-paste prototype (v0.15: layout)
- **Task (user):**
  - Group columns B:C and I:K.
  - Row grouping at the bottom rather than the top.
  - Mitigation as the first tab, at 75% zoom.
  - Open rolled up.
- **Changes:**
  - Columns: B:C (fuel, sector) and I:K (unit, source, scenario-1 code column) at outline level 1, hidden. The parameter columns D:G sit between them and are nested at level 2, so expanding level 1 shows B:C and I:K and level 2 adds D:G. Adjacent same-level groups would merge in Excel.
  - Rows: summaryBelow, so the + button sits below each group. Every grouped row is hidden on open, and the collapsed flag is on the row after each group.
  - Mitigation is the first and active tab, at zoom 75%.
  - ReadMe roll-up text and version log updated.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.15.xlsx`, `build_v0_15.py`, `check_v0_15.py`, `check_report_v0.15.md`, README. v0.14 files moved to `Old/`.
- **Checks:** PASS, including the scenario-copy tests. Regression vs v0.14: 3,484 codes diff 0. New layout checks: column levels, rolled-up rows and collapsed flags, first tab, zoom.
- **Caveats:**
  1. Grouping I:K also hides scenario 1's output-code column (K) when rolled up. Scenario 2's code column (Z) stays visible.
  2. With the + buttons below, a subsector's variables expand from the button on the next subsector's heading line (Excel convention for summary rows below).
  3. Not yet opened in Excel.

## 2026-10-09 - Mitigation copy-paste prototype (v0.16: layout)
- **Task (user):**
  - One level of column grouping, not nested; combine the early column groups.
  - Group 2030-2039 for both scenarios.
  - Two beiges: the darker one for the base year; a lighter one for areas that are copy-pasteable within themselves but not draggable to white or the other beige. Apply the lighter one to the LAMBDA formulae and the historical price range.
  - A blank column between scenarios.
- **Changes:**
  - Column groups at one level, all rolled up: B:G (fuel, sector, parameters), I:K, and 2030-2039 in each scenario group.
  - Light beige `EEECE1` (Excel tan, lighter than the base-year `DDD9C4`) on the right-column LAMBDA cells of every calculated row (dark red text kept) and on the 2023-2024 history block of `sp` and `txo`.
  - Each scenario group now ends with a blank spacer column (group width 21). Scenario 2 is `AF:AZ`; copy a whole group, spacer included, to add a scenario.
  - ReadMe colours and roll-up text, README "Add a scenario" and the version log updated.
- **Outputs:** `CPAT_Mitigation_CopyPaste_v0.16.xlsx`, `build_v0_16.py`, `check_v0_16.py`, `check_report_v0.16.md`, README. v0.15 files moved to `Old/`.
- **Checks:** PASS, including the scenario-copy tests with the spacer column (groups 3-9). Regression vs v0.15: 3,484 codes diff 0. New layout checks: one outline level; the 20 grouped year columns; spacer columns empty; light-beige LAMBDA and history blocks (base year darker, projection white).
- **Caveat:** Not yet opened in Excel.

## 2026-10-09 - CPAT-AI-Mitigation-MVP v1.00 (rename) and overview deck
- **Task (user):**
  - A very short PowerPoint (about 7 slides, pitch and user guide combined) explaining in simple terms the purpose, scope and definition of the Excel. Styled like the Excise Diagnostic user guide and the Excise-Fiscal proposal; screenshots from the workbook where possible.
  - Rename the prototype CPAT-AI-Mitigation-MVP-vX.XX and upgrade to v1.0.
- **Changes:**
  - Workbook renamed `CPAT-AI-Mitigation-MVP-v1.00.xlsx`. `build_v1_00.py` (NAME, VERSION 1.00; sheet titles and version log), `check_v1_00.py`, `check_report_v1.00.md`. Content as v0.16.
  - The uploaded v0.16 was byte-identical to ours (no user edits to merge).
  - The folder name `mitigation/` and the v0.x file names in `Old/` are kept.
- **Deck:** `presentation/CPAT-AI-Mitigation-MVP_Overview_v1.0.pptx`, 7 slides:
  1. Title, with the rolled-up overview.
  2. Purpose and scope: AI-generated Excel; main mitigation equations; more readable. Definition, in scope, not yet, and the section chain.
  3. Four problems and four fixes: readability; fixed rows -> scenarios left to right; sector/fuel-specific quantities -> left parameter section; scenarios -> copy a block plus an MTInputs lookup.
  4. Scenarios side by side, with three steps to add one and the MTInputs screenshot.
  5. The left section (B:C, D:G).
  6. Two formula styles: direct formulas vs LAMBDA with IF, both draggable.
  7. Next steps: store data, charts and scenario settings in CPAT; collect outputs for many scenarios in an updated MTOutputs (outputs, not inputs, for now); power, other gases, legacy check. Also a "getting started" box.
- **Built by:** `presentation/build_deck_v1_0.js` (pptxgenjs; theme navy 1E2761 / teal 0F7B6C / amber E08A1E / gold D4A24C, Cambria headings, Calibri body, 13.33 x 7.5 in as the Excise decks). Screenshots are rendered from the real workbook by `presentation/make_screenshots_v1_0.py`: LibreOffice recalculation with LAMBDAs expanded, values copy of one sheet, selected cells showing formula text, PDF -> PNG.
- **Checks:** workbook PASS; regression vs v0.16: 3,484 codes diff 0. Deck passes `validate.py`; every slide rendered and inspected (no overflow or overlap).
- **Caveats:**
  1. Screenshots come from LibreOffice, not Excel (fonts and gridlines differ slightly).
  2. The formula screenshot shows the road-gasoline rows only.
  3. pptxgenjs is not a repo dependency: install it (`npm install pptxgenjs`) to rebuild the deck.

## 2026-10-09 - CPAT-AI-Mitigation-MVP v1.01: MTOutputs and Charts
- **Task:** User offline, "press on". First item of the agreed next steps: store results per scenario (slide 7 of the overview deck).
- **Changes:**
  - New sheet `MTOutputs` (second tab): 23 key indicators per scenario block, read from Mitigation by output code.
    - Indicators: fuel use total and by sector, CO2 total and by sector with change vs scenario 1, the revenue components and fiscal effect, carbon and ETS price, retail prices of gasoline, diesel and residential gas, and road-gasoline after-tax price.
    - Lookup: the scenario's code column is the first cell of Mitigation row 5 holding the scenario number; the year columns are read by offset.
    - Adding a scenario: copy the last block below (its number = previous + 1). Adding an indicator: a code stem in column B plus the row formulas.
  - New sheet `Charts`: 4 line charts (CO2, fuel use, fiscal effect, carbon price), one series per scenario block.
  - ReadMe, README and version log updated.
- **Outputs:** `CPAT-AI-Mitigation-MVP-v1.01.xlsx`, `build_v1_01.py`, `check_v1_01.py`, `check_report_v1.01.md`. v1.00 files moved to `Old/`.
- **Checks:** PASS.
  - MTOutputs as shipped: 874 cells equal the Mitigation cell of their code.
  - With blocks 3-9 added by copying alongside the scenario-copy tests: 3,933 cells equal, block numbers 1-9.
  - Charts reference the right rows.
  - Regression vs v1.00: 3,484 Mitigation codes diff 0.
- **Caveats:**
  1. Charts need a new series added by hand after adding a scenario block.
  2. MTOutputs search area on Mitigation is A1:ZZ5000 (room for about 30 scenario groups).
  3. The overview deck still shows v1.00 screenshots (no MTOutputs slide).
  4. Not yet opened in Excel.

## 2026-10-09 - Legacy cached baseline vs MVP; ETS cap design options (no model change)
- **Task:** User offline, "press on". Investigate the 2022-2024 fuel-use jump against legacy, and plan the cap-based ETS price.
- **Finding:** `CPAT 1.0pre_456_NoPropData.xlsb` keeps the cached results of its last full run with real data. That gives fuel use and after-tax prices for all 16 subsectors x 8 fuels, and CO2 by subsector. `legacy_compare_v0_1.py` extracts them (`data/legacy_cached_baseline.csv`) and compares them with MVP v1.01 scenario 1 in `legacy_comparison_v0_1.md`.
- **Results:**
  1. The 2022 base year matches exactly (fuel use, e.g. road gasoline 7,577.3 ktoe).
  2. Legacy prices show no devaluation drop: road gasoline 0.612 / 0.612 / 0.604 $/liter in 2022-2024 against the corrected data's 0.600 / 0.411 / 0.335. So the legacy run used an older price vintage.
  3. With the last historical price year set to 2022 (prices held), the mean absolute gap in fuel use by subsector and fuel for 2023-2030 falls from 45.6% to 17.3%, and the 2030 total from +41.3% to +8.0%.
  4. Legacy has a 2023 dip of about -20% in every sector, which matches its note "sets baseline 2022 and 2023 emissions to equal estimates" (legacy Mitigation row 475). The MVP has no such calibration.
  5. Remaining price differences: legacy residential gas 5.5-6.2 vs 2.3-4.6 $/GJ; coal; legacy other oil products 15 $/bbl from 2025.
- **ETS cap:** `ETS_Cap_Design_Options_v0_1.md`. The legacy method is semi-elasticity based with iteration. In the MVP it would create a circular reference through scenario 1. Four options; recommended A: baseline covered emissions as a refreshed data row, with the current rule kept as override.
- **ETS algorithm (legacy):** `ETS_Legacy_Algorithm_v0_1.md`. Legacy has a fast closed-form price estimate (reduction left / (covered semi-elasticity × effectiveness), effectiveness auctioned 1.0, OBA 0.5) plus a VBA damped log-space goal seek on an override row. The auctioned part acts as a price wedge; the OBA part acts as a shadow price on efficiency only. The cached legacy run is not converged (max error 0.33). The MVP still treats the ETS as fully effective. The proposed benchmark design (OBR share from benchmarks, same split afterwards) is not built yet.
- **Decisions for the user:**
  1. Which price vintage and last historical year to use. The corrected data imply the jump is a real consequence of the devaluation under CPAT's method.
  2. Whether to add legacy's 2023 calibration to emission estimates.
  3. Which ETS option to build.

## 2026-10-09 - Check: legacy treatment of regulated prices (no model change)
- **Question (user):** Does legacy have functionality that keeps regulated prices flat for an economy like Egypt's, based on the pass-through numbers, which would explain the difference?
- **Answer:** No extra mechanism. Legacy uses the same rule as the MVP: chosen = bucketed pass-through, with Egypt values coal 1, gas 0, gasoline/diesel/LPG/kerosene 0, other oil products 1 (MVP 0 by user decision), biomass 1. The floating subsidy is set at its 2024 level, so with pass-through 0 the retail price stays at its 2024 value from 2025 (legacy gasoline 0.6036 $/liter flat). Price-control phase-out is off; there is no fuel subsidy override.
- **The difference is the historical price data.** Legacy's block has no devaluation fall: gasoline 0.612 / 0.612 / 0.604 $/liter real in 2022-2024, against the corrected 0.600 / 0.411 / 0.335. Residential gas 6.24 / 5.81 / 5.54 against 4.63 / 3.21 / 2.33 $/GJ. The MVP's fuel use responds to that 2022-2024 fall; legacy's prices barely move (and legacy calibrates 2023 emissions to estimates).
- **Details and options:** appended to `excel_ai_new/mitigation/legacy_comparison_v0_1.md`.

## 2026-10-09 - Reality check: Egypt gasoline prices 2022-2024 (no model change)
- **Question (user):** Did Egypt's gasoline prices really fall like that?
- **Answer:** Yes, in US dollars.
  - The official 92-octane price rose from about EGP 8.9/liter (2022 average) to 10.3 (2023) and 13.1 (2024).
  - The pound averaged about 19.2, 30.7 and 45.4 per USD over the same years.
  - So the USD price fell from about 0.47 to 0.34 and 0.29 $/liter nominal (-38%). The corrected block falls 0.528 -> 0.376 -> 0.316 (-40%, average over grades).
  - Legacy's block rises (0.54 -> 0.57). The corrected data are right; legacy's price vintage is stale.
- **Details and sources:** `excel_ai_new/mitigation/legacy_comparison_v0_1.md`. Exchange rates are from secondary compilers; the official IMF/World Bank series is still to be pulled.

## 2026-10-09 - CPAT-AI-Mitigation-MVP v1.02: new ETS with cap, benchmarks, volatility, goal seek
- **Task (user):** "The ETS is split into a shadow price and a carbon tax near equivalent piece. We can update old model with a volatility dependent effectiveness. Anyway, implement ETS then as you wish."
- **Built** (`excel_ai_new/mitigation/build_v1_02.py`, method `ETS_Method_v0_1.md`):
  - **Cap.** Baseline covered emissions use option A of `ETS_Cap_Design_Options_v0_1.md`. The data rows `bco2` hold scenario 1's CO2 by ETS sector; the build fills them from a LibreOffice recalculation, and check row `bco2.chk` = 0. The cap follows MTInputs 85-87. There is no circular reference.
  - **Price.**
    - Fast estimate: LN(cap/baseline) / (effective semi-elasticity × volatility adjustment). This is the log form; legacy's is linear.
    - Or the override row `ets.ovr` (MTInputs `D_ETSPriceOverride` = Yes; a blank cell takes the carbon price path, the v1.01 behaviour).
    - `ets_goalseek_v0_1.py` replaces the legacy VBA. It uses the same damped log-space step on the workbook's `ets.next` proposal and writes a CSV for pasting into `ets.ovr`.
  - **Benchmarks** by sector group (pow, tra, res, ind; typed rows, assumption 1.0 → 0.8) replace the auction share. OBR share = benchmark.
    - The permit price splits into a tax-equivalent wedge in `atp`, × (1 − OBR).
    - The OBR part, × OBR, is a shadow price on the efficiency margin, like feebates.
    - Revenue is the permit price on the auctioned part.
  - **Volatility adjustment** = (1 + policy risk × impact) / (1 + volatility × impact), from MTInputs 95-97 and a Settings table (legacy ETS+LTS). It equals legacy's 1/1.1 at Medium and scales the tax-equivalent price and the fast estimate.
  - Section 13 adds CO2 by ETS sector, covered emissions, cap, gap and next price. MTOutputs adds covered CO2 and the cap. LegacyDiff is updated.
- **Checks** (`check_report_v1.02.md`, PASS):
  - Scenarios 1-2 are unchanged against v1.01 (3,476 codes, diff 0).
  - The cap-based ETS test matches Python to 1e-14.
  - ETS with a blank override, volatility Zero, policy risk 0 and benchmarks 0 equals the carbon tax exactly.
  - Goal seek: the fast estimate misses the cap by at most 2.9%. After 12 iterations the gap is 0.46%. Prices go 2030 26.6 → 24.6 and 2035 54.3 → 52.5 $/tCO2 (cap −2% → −15% on iron & steel and cement).
- **Caveats:**
  - Power is not modelled, so covered power emissions are 0.
  - Benchmarks are relative to current intensity, with output proxied by fuel use (OBR share = benchmark).
  - Semi-elasticities are legacy's Egypt sector values (fast estimate only).
  - VAT on new policies applies to the tax-equivalent ETS cost.
  - The `bco2` data must be refreshed (rebuild, or paste scenario 1's `co2.sec`) when the baseline changes; `bco2.chk` shows it.
  - Goal-seek convergence is slow (about 12% error reduction per iteration), as with legacy's damping.
  - MTInputs rows 90-92 (auction proportion) are no longer read.

## 2026-10-09 - CPAT-AI-Mitigation-MVP v1.03: multiple scenarios (definitions, VBA batch run, stored results, comparison)
- **Task (user):**
  - Store results as values so multiple scenarios can be kept: the baseline, which should not change, and the scenarios.
  - Put a table of scenario definitions in MTInputs, one column per scenario, and add combined packages. No High/Low international price sensitivity, because it deviates from legacy.
  - Write a VBA macro that cycles through the definitions, runs the ETS goal seek when the ETS is on, and stores the results as values.
  - Add a comparison tab for one year.
  - The user chose an embedded .xlsm.
- **Built** (`excel_ai_new/mitigation/build_v1_03.py`, `Scenarios_Method_v0_1.md`):
  - **MTInputs:** J = baseline, K = live policy scenario, L-N = definitions with a Run? flag in row 4:
    - 3: $20 carbon price;
    - 4: Package A, carbon tax $10 → $50 by 2030 + feebates on transport and industry;
    - 5: Package B, ETS on power and industry (cap −5% → −20% by 2035) + carbon tax $25 elsewhere.
  - **VBA module CPATScenarios** (`CPATScenarios_v0_1.bas`): RunAllScenarios, StoreBaseline, StoreLiveScenario, SolveETSLive, ClearStoredScenarios. The ETS goal seek ports `ets_goalseek_v0_2.py`.
  - **StoredResults:** values only, 25 MTOutputs rows per scenario ID.
  - **ScenarioCompare:** one year, baseline + 8 scenario slots; levels, differences and % differences.
  - **`vba_project_v0_1.py`** writes the VBA project without Excel: MS-OVBA compression, dir/PROJECT/PROJECTwm streams, encrypted protection fields (checked by decrypting legacy's), and a compound file writer. It embeds the project as an .xlsm.
  - StoredResults ships filled by a Python emulation of the macro.
- **Checks** (`check_report_v1.03.md`, PASS):
  - Mitigation is unchanged against v1.02.
  - Stored baseline and definition 3 equal the recalculated MTOutputs blocks.
  - Definitions 4 and 5 equal the independent Python recomputation (5 at its stored ETS prices). Package B meets its cap within 0.49%: ETS price $41 (2030), $77 (2035), $147 (2040).
  - ScenarioCompare equals StoredResults.
  - **The embedded macro runs in LibreOffice:** RunAll stored the same four blocks as the emulation (max relative difference 8e-15) in 27 s, and restored column K and the override row.
- **Caveats:**
  - **The VBA project has not been opened in Excel.** It is tested only with oletools and LibreOffice. If Excel rejects it or shows an empty project, import `CPATScenarios_v0_1.bas` and save as .xlsm.
  - The macro needs macros enabled. Excel may warn about files from the internet (unblock in file Properties).
  - The batch runs one policy scenario at a time through Mitigation group 2. Stored indicators are the MTOutputs rows.
  - The Package A result is driven by assumptions: the carbon price continues linearly after 2030 (template switch) and feebates continue linearly. CO2 is −31% vs baseline in 2030.
  - LibreOffice saves booleans as `=TRUE()` in .xlsx, which affects only the test's comparison.

## 2026-10-09 - CPAT-AI-Mitigation-MVP: documentation completed, advanced-features deck, hand-over folder
- **Task (user):**
  - Complete the documentation.
  - Adjust the team deck on AI and the MVP if visible; otherwise write a short 4-slide deck on the MVP's advanced features.
  - Update the reference .md files, then commit and push everything to main.
- **Deck:**
  - The only deck in the repo is the generated v1.0 overview; `excel_ai_new/working_version/` holds an identical copy. No separate team deck is visible.
  - New 4-slide deck written: `presentation/CPAT-AI-Mitigation-MVP_AdvancedFeatures_v1.0.pptx`. Slides:
    1. what is new in v1.01-v1.03;
    2. the cap-based ETS and its two channels, with the Package B price path;
    3. the scenario table and the RunAllScenarios macro;
    4. ScenarioCompare, CO2 by scenario in 2030, quality numbers and next steps.
  - Screenshots and chart data come from the v1.03 workbook (`make_screenshots_advanced_v1_0.py`); the deck is built by `build_deck_advanced_v1_0.js` (pptxgenjs).
  - Validation passed; visual check in LibreOffice.
- **Documentation:**
  - `CPAT-AI-Mitigation-MVP_Documentation_v1.03.docx` (25 pages) now has appendices:
    - A: differences with legacy CPAT, read from sheet LegacyDiff;
    - B: version log, from Settings;
    - C: verification summary, from `check_report_v1.03.md` (all sections, Overall PASS);
    - D: presentations.
  - Reference .md files updated:
    - folder README: deck and appendices;
    - root README: key documents, the mitigation line and the new `working_version/` line;
    - NORMS key documents: MVP row;
    - AGENTS: the MVP builds on Linux with openpyxl + LibreOffice, an exception to the Excel COM rule.
  - `make_screenshots_v1_0.py` now finds the archived v1.00 builder in `Old/`.
  - The check report's goal-seek heading now names `ets_goalseek_v0_2.py` (label only).
- **Hand-over folder** `excel_ai_new/working_version/`:
  - added the v1.03 .xlsm, the Word documentation, the advanced-features deck and the .bas module;
  - kept the v1.0 overview deck;
  - moved v1.00 to `working_version/Old/`.
- **Caveats:**
  - The decks' screenshots are LibreOffice renders, so fonts may differ slightly from Excel.
  - If a separate team deck on AI exists outside the repo, it was not updated. Share it to have the new slides merged in.
  - The VBA project still needs its first run in Excel (see the v1.03 entry).

## 2026-10-10 - CPAT-AI-Mitigation-MVP v1.04: first-run test for Excel (CheckBatchRun, sheet MacroCheck)
- **Task (user):** "Go for it", the open item being the macro's first run in Excel. Excel is not available in this Linux environment, so the run itself is left to the user. This version makes that run a one-click, self-reporting test.
- **Built** (`build_v1_04.py`, module `CPATScenarios_v0_2.bas`):
  - Macro **CheckBatchRun**:
    1. checks the 12 lookups the macros rely on (MTInputs scenario columns and parameter rows, Mitigation rows by code and the scenario-2 columns, MTOutputs blocks);
    2. compares the host's own recalculation of the baseline with the stored baseline. Excel evaluates the LAMBDA column natively; LibreOffice needed it expanded;
    3. reruns RunAll, including the ETS goal seek, and compares every stored value with the value stored before.
  - The report goes to the new sheet **MacroCheck** (Result PASS / CHECK / FAIL, 1e-6 relative tolerance). Its first-run checklist (unblock, enable macros, run, fallback import) is in `Scenarios_Method_v0_1.md`.
  - The v0.1 macros are unchanged; Mitigation is unchanged.
  - Deck updated to `CPAT-AI-Mitigation-MVP_AdvancedFeatures_v1.1.pptx` (the next step names the test).
  - Word documentation `..._v1.04.docx`; `working_version/` refreshed (v1.03 files to `working_version/Old/`).
- **Checks** (`check_report_v1.04.md`, PASS):
  - Regression vs v1.03: 3,642 codes, difference 0.
  - CheckBatch run in LibreOffice: Result PASS; 12 lookups found; baseline difference 4.4e-15; 1,900 stored cells after the batch rerun, largest relative difference 7.6e-15; 27 s.
  - Negative test with the row code ets.ovr broken: Result FAIL naming exactly that lookup, returned −1, no run.
- **Caveats:**
  - Still not run in Excel. The MacroCheck report from that first run is the evidence to look for.
  - LibreOffice's VBA layer reports itself as "Microsoft Excel 11.0" in the report's Started line, so that line names the host but does not prove Excel.
  - In Excel, small differences against the LibreOffice-computed stored values are possible but expected below 1e-6. Anything larger shows as CHECK, with a count.

## 2026-10-10 - CPAT-AI-Mitigation-MVP v1.05: power generation costs and electricity prices (section 3)
- **Task (user):** plan the prices part of power (generation costs and downstream electricity prices), with simplifications that match the existing model; lay out the interactions (generation mix, systemic cost of renewables); write a method note with pseudocode; then build it following the legacy outline and sub-table letters.
- **Method note:** `PowerPrices_Method_v0_1.md`:
  - interactions I1-I8 and simplifications S1-S7;
  - method by legacy sub-table (A, B, C, D, E, F, G, J) with pseudocode;
  - workbook layout, interim data, validation and open decisions.
- **Data:** `extract_power_v0_1.py` reads legacy Mitigation rows 2950-3935, locating each row by table id and label. It writes `data/power_tech.csv`, `power_paths.csv`, `power_params.csv` and `legacy_power_reference.csv`.
  - Correction found while validating: the legacy B2 capital cost is the base-year cost. It already includes the capex time factor of 2022 (1.05 for wind and solar), so `cax0` is divided by that factor.
- **Built** (`build_v1_05.py`):
  - **Mitigation section 3**, with legacy sub-tables in legacy order:
    - A: inputs;
    - B: amortised fixed cost of the stock, with vintage averages;
    - C: levelised fixed cost of new plants;
    - D: variable cost and new policy cost per kWh;
    - E: generation cost by type and the averages;
    - G: residential and industrial electricity prices, subsidy gap and revenues;
    - J: storage cost of variable renewables.
  - Sheet `Inputs_power` (one row per type, with derived constants; one row per end-user group) and data sheets `PowerTech`, `PowerPaths`, `PowerParams`.
  - 14 new LAMBDAs, 44 in all.
  - 3 new MTOutputs indicators: residential and industrial price, and the average generation cost.
  - 7 new LegacyDiff rows; the version log is updated.
- **Checks** (`check_report_v1.05.md`, PASS):
  - **Method = legacy:** the Python reference, fed with legacy inputs, reproduces 80 cached legacy rows (A13, B2, B6, B8, C3, C7, D4, E3, J, G1/G2 supply cost and price), 2022-2040. Largest relative difference: 5.6e-17.
  - **Workbook = Python** for all 28 power variables in every scenario test (carbon tax, ETS, fuel price reform, price source, price controls), and in the stored packages (ID 5 is the ETS on power).
  - One formula per power block; the right column calls a LAMBDA (1,669 rows).
  - Regression vs v1.04: 3,642 codes, difference 0. The macro tests still pass.
- **Results (Egypt, real 2026 $/kWh):**
  - The average generation cost is about 0.069.
  - Residential price before policy: 0.061 (2022) and 0.042 (2030). Industrial: 0.064 and 0.049.
  - A $20 carbon price adds about 0.009 $/kWh in 2027 and raises about USD 1.8 bn a year.
  - The VRE share rises from 5% to 28% by 2040. Storage then adds about 0.011 $/kWh to wind and solar.
- **Caveats:**
  - Generation shares, investment shares and consumption are **interim data** from the legacy baseline run. A policy scenario therefore changes power prices only through fuel and carbon costs, not through its own generation mix, until the engineer model exists. Power emissions are still 0, so a cap that covers power cannot be met by power.
  - Fuel prices are spot prices from section 2. Legacy uses a 5-year moving average.
  - Historical electricity prices come from the corrected Egypt block: 0.054 $/kWh nominal residential in 2022, VAT 0. Legacy used 0.112 including 15.6% VAT.
  - Power revenues value the ETS at the tax-equivalent price. They are not yet in the section 12 totals.
  - The coal implicit cost and the extra shadow price are not built (both are 0 for Egypt).
  - Open decisions are in section 8 of the method note.

## 2026-10-10 - CPAT-AI-Mitigation-MVP v1.06: power engineer model; legacy bugs report
- **Task (user):** "Build the power model. Align except for bugs, and report both bugs and improvements in new human readable word doc."
- **Legacy reading:**
  - The legacy .xlsb was converted to .xlsx with LibreOffice so its formulas could be read (named ranges come through as `#NAME?`; their values were taken from the cached cells).
  - For each row, the formulas were compared across all year columns.
  - `extract_power_v0_2.py` adds the engineer-model inputs (A4 plant data, retirement, investment permission, scale-up rates, demand by subsector, balance shares, dispatch and investment parameters). It also writes `legacy_engineer_reference.csv`: cached inputs and results of the baseline and the carbon-tax run (rows +6331).
- **Python reference** `power_model_ref_v0_1.py`:
  - covers H demand, I dispatch, J storage, K retirement and capacity, L investment, plus the price chain;
  - with the bugs switched on (and the legacy demand shock), it reproduces 208 legacy rows of both runs, 2022-2040, to 2e-13;
  - each of the 10 bugs is a switch (`FIXES`).
- **Bugs** (details and effects in `PowerModel_BugsAndImprovements_v1_0.docx`):
  1. services demand grows with the industrial multiple from 2024 (row 3731);
  2. the autonomous-efficiency exponent uses eps_F instead of eps_U;
  3. the income factor on the GDP elasticity is applied twice, anchored to 2023 ($M3686);
  4. the long-term storage allocation is applied twice;
  5. investment USD uses the capital cost at factor 1;
  6. the investment logit is normalised by non-permitted types;
  7. early coal retirement mixes nameplate and effective MW;
  8. the effective coal retirement is uncapped;
  9. the feebate rebate is x 1.22;
  10. the capacity check uses last year's plan.
  - Plus 2 minor defects: a stray `$G4291` and a total-row multiplier on an empty cell.
  - With all fixes, on the legacy Egypt inputs: 2040 generation +12.6% in the baseline and +9.2% in the carbon-tax run; 2040 power CO2 +10.8%.
- **MVP corrections of v1.05:**
  - VAT on the power policy term (legacy row 3614 applies it);
  - LT storage allocation applied once;
  - VRE share includes other renewables.
  - None of the three affects Egypt numbers.
- **Built** (`build_v1_06.py`):
  - **Section 3 now has legacy H, I, K and L**:
    - D6 shadow price and rebate, D9 levelised variable cost, E1 investment cost;
    - the interim rows of v1.05 (generation shares, investment shares, consumption) are now modelled;
    - 33 named LAMBDAs added;
    - the look-ahead rows `dsum` and `lvc` are plain formulas in every column.
  - **Power CO2 enters section 13** (total, by fuel, ETS sector power).
  - Inputs_power gains plant, demand-group and subsector tables; new data sheet PowerDemand.
  - Settings C19 switches the 2023-2024 demand shock (off by default).
  - 5 MTOutputs indicators; LegacyDiff rows; version log.
  - Method note `PowerModel_Method_v0_1.md`. Price note corrected (VAT, LT allocation, VRE share).
- **Checks** (`check_report_v1.06.md`):
  - legacy test: 208 rows x 2 runs;
  - the workbook equals the Python reference (all fixes) for every power row in every scenario test (carbon tax, fuel price reform, feebates, price source, ETS with power, price controls);
  - power properties hold;
  - regression vs v1.05: 3,484 codes unchanged (388 intended changes: power block and CO2 including power);
  - macro tests pass.
  - The shipped-file check now allows LibreOffice errors in the power block and the section-13 CO2 rows, because D9 looks ahead to the LAMBDA column. The expanded variant checks their values.
- **Caveats:**
  - **2023 jump:** MVP electricity demand jumps +22% in 2023 (generation 220 to 269 TWh), and investment surges in 2023-2025 (scale-up limits leave some need unplaced; gas then runs harder). The cause is the corrected Egypt electricity prices, which fall in USD (0.075 to 0.054 $/kWh, devaluation), and demand responds to that fall. The fuel blocks show the same jump (+25% fuel use). This is the open price-vintage decision in TODO. The legacy demand shock (Settings C19) largely offsets it.
  - **Earlier power response:** investment looks ahead (D9 includes future carbon prices), so power changes before a carbon price starts, as in legacy.
  - **ETS with power:** an ETS covering power now has power emissions in its cap. The Package B ETS price is about $124/t in 2027 (the goal seek converges within 17 iterations).
  - **Demand not linked to sectors:** electricity demand (H) is its own block, not linked to the sector fuel blocks. Electricity is not yet a fuel there.
  - **Features not built:** PPAs, manual capacity and investment, planned coal retirement data, elasticity-model power demand, and a carbon price on power use (all off or 0 for Egypt).
  - **Not run in Excel:** not yet opened in Excel. The MINIFS function (`_xlfn.MINIFS`) requires Excel 2019 or later, which the LAMBDAs already require.

## 2026-10-11 - CPAT-AI-Mitigation-MVP v1.07: short formulas, planned retirement, demand memo lines, power indicators

- **Task (user):**
  - "Accept the dip. Keep sectoral policies separate. Add planned retirement. Keep all formulae short - lambdas can have more complexity. Add memo lines for sectoral demand. Add power indicators."
- **Decisions recorded:**
  - The 2023 power-demand jump is accepted. It comes from the USD electricity prices after the devaluation; Settings C19 stays 0.
  - Sector policies stay separate from power demand. Electricity is shown as memo lines only, not as a fuel in the sector blocks.
  - Both decisions are in LegacyDiff and TODO.
- **Built** (`build_v1_07.py`):
  - **Short formulas:** every cell formula has at most 100 characters, LAMBDA calls included. The longest is 99, across 110,473 formulas. The rule is in NORMS section 3. Tools used:
    - 53 defined names for data tables and fixed ranges;
    - helper rows: carbon-price path years and nominal factor; ETS on, volatility, impact, cap change, log ratio; policy rates by sector `ctr`, `etr`, `shpx`; `gp.src`, `gp.adj`, `gpn`; `txf`; `ecmin`, `ecshr`;
    - helper columns in Inputs_prices (data by year), MTOutputs and ScenarioCompare; Settings rows 20-25;
    - new fuel-use parameters: AEEI factor and efficiency exponent (Inputs);
    - the LAMBDA `ROWLABEL` for column H;
    - history lookups moved into the SUPPLYCOST, OTHERTAX and POWERPRICE LAMBDAs.
    - There are now 85 LAMBDAs.
  - **Planned retirement for every type:**
    - PowerTech gains a `planned_retirement` switch and PowerPaths gains `pret|<type>` rows (`extract_power_v0_3.py`).
    - Retirement = MIN(planned retirement or the rate-based retirement, + early coal retirement, capacity).
    - Python reference: `power_model_ref_v0_2.py`.
  - **Memo lines `eldem`:**
    - electricity demand by subsector in each sector block, and by sector in section 11;
    - demand by demand group in H.
  - **Power indicators:** 18 more MTOutputs indicators (51 in all) and 6 power charts (10 in all).
  - Method note `PowerModel_Method_v0_2.md`; Documentation v1.07; `ets_goalseek_v0_3.py`, `legacy_compare_v0_2.py`.
- **Checks** (`check_report_v1.07.md`, Overall PASS):
  - formula length;
  - regression vs v1.06: 4,404 shared codes, max difference 0;
  - planned retirement switched on for gas and oil = Python reference, and retirement = the data;
  - memo lines add up;
  - legacy test 208 rows × 2 runs;
  - macro tests;
  - Package B goal seek converges within 17 iterations.
- **Caveats:**
  - **No planned-retirement data for Egypt.** The legacy file has none, so every switch is No and the results are unchanged. Enter data in PowerPaths and set the switch in PowerTech.
  - **Name clash found during the build.** A defined name must not equal a LAMBDA name, ignoring case: `ETSSemi` collided with `ETSSEMI` and gave #NAME?. It was renamed to `SemiEl`, and the builder now asserts against such clashes.
  - **Column H uses a LAMBDA (ROWLABEL).** Without LAMBDA support (LibreOffice, Excel before 365) the descriptions show errors. The check accepts this, as it does for the right column. Output codes stay plain formulas.
  - **The shipped-file check now also allows LibreOffice errors in the memo lines.** They read power demand, which depends on the D9 look-ahead.
  - **Memo grouping.** In the memo by sector, food & forestry counts under buildings, as in the sector blocks. The legacy demand groups put it with industry.
  - **Not run in Excel yet.**

## 2026-10-11 - CPAT-AI-Mitigation-MVP v1.08: works without LAMBDA; combined deck v2.0; documentation refresh

- **Task (user):**
  - "Main functionality should work without lambdas. If formulae become too long break up. Do and test."
  - Then: finalise, redo the PowerPoint and the documentation for the whole project. The integrated AI-tools deck is not in the repository, so the deck is one simple combined deck of the MVP, based on the existing MVP decks.
- **Built** (`build_v1_08.py`):
  - **No LAMBDA in cells.** Every cell holds a plain formula of at most 100 characters (longest 99), the right column (2040) included.
  - **Column H** reads the member labels from a table on Mapping (sector|fuel key) instead of the LAMBDA ROWLABEL.
  - **The 84 named LAMBDAs are an optional library.** New sheet `Lambdas` gives the LAMBDA formula of each calculated row (as text). The right column is no longer light beige.
  - Method notes renewed so they describe the current state: PriceProjection v0.5, Scenarios v0_2, PowerPrices v0_2, PowerModel v0_3.
  - Documentation v1.08.
- **Deck:** `presentation/CPAT-AI-Mitigation-MVP_v2.0.pptx`.
  - 11 slides, built by `build_deck_v2_0.js` from `make_screenshots_v2_0.py` (screenshots and stored-scenario data of v1.08).
  - It replaces the Overview v1.0 and Advanced features v1.1 decks, which moved to `presentation/Old/`.
- **Checks** (`check_report_v1.08.md`, Overall PASS):
  - no cell calls a LAMBDA;
  - the shipped file recalculated by LibreOffice has zero error values in all 29 sheets;
  - values equal the Python recomputation as shipped, and also with each row's LAMBDA from sheet `Lambdas` copied over the whole row;
  - regression vs v1.07: 4,630 shared codes, max difference 0;
  - macro tests and the ETS goal seek pass.
- **Caveats:**
  - **Excel 2019 or later still needed** for MINIFS (power dispatch and investment). LAMBDA is no longer required.
  - **New sector|fuel pairs need a label.** A new pair on Mitigation (e.g. a new fuel) needs a row in the member-label table on Mapping, or its description shows #N/A. The table has 20 spare rows in its defined name.
  - **Deck charts render slightly differently in LibreOffice.** The deck was checked in LibreOffice renders; in the CO2 chart there the year labels are dense.
  - **The integrated AI-tools deck (user guide for Claude and GitHub Copilot) was not found in this repository** and was not redone.
  - **Not run in Excel yet.**

## 2026-10-11 - CPAT-AI-Mitigation-MVP v1.09: existing carbon pricing; power in the main thread; full consistency check

- **Task (user):** "Do a full check for consistency. One could now bring in existing carbon pricing data; ensure power is fully linked up with revenues and energy use and emissions built into the main thread."
- **Built** (`build_v1_09.py`, data step `extract_ecp_v0_1.py`):
  - **Existing carbon pricing.**
    - New sheet `ECP`: the legacy ECP data (carbon tax rate, ETS permit price by year 2021-2025; sector and fuel coverage; 52 countries) and the values of the country in Settings C4 (real prices, coverage of the last data year). Egypt has no entries, so all values are 0.
    - Section 1 reads MTInputs 208-214: `ExistingCTApply`, `ExistingCTGrowth`, `ExistingETSApply`, `ExistingETSGrowth`, `CTaxComplimentaryToETS`. Prices used = data x switch, growing after the last data year; the level embedded in the price data is held after the last historical price year.
    - Per subsector and fuel: `xcp` (level) and `xcpd` (change against the price data). `xcpd` enters the after-tax price and existing-tax revenue; `rxcp` is a revenue memo. Power: `xck` in the variable cost.
    - `CTaxComplimentaryToETS` = Yes: the new carbon tax covers 1 - existing ETS sector coverage (legacy rows 2270-2288).
  - **Power in the main thread.**
    - Section 11: generation fuel use of coal, gas, oil and biomass (row `ener.pow`) is in the total and in the fuel rows.
    - Section 12: power rows in every total: fuel taxes and subsidies on generation, change in existing carbon pricing, electricity VAT (also on the passed-through policy cost) and subsidy gap, new policies with the ETS at the permit price (new sub-table M by generation type). This fixes the power ETS revenue (it was valued at the tax-equivalent price, about 10% high).
    - Section 13 already had power CO2 (v1.06); new check row `co2.chk`.
  - **Consistency fixes found by the review:**
    - stale texts in the workbook (section 12 and 13 notes said "no power", PowerPaths title said interim data, data-sheet sources named old extractors, method-note names);
    - method notes renewed to the current state: PriceProjection v0.6 (with existing carbon pricing, 5b), PowerPrices v0_3 (interim data text removed, revenues and section 12), PowerModel v0_4, Scenarios v0_3 (58 indicators);
    - `ets_goalseek_v0_4.py` and `legacy_compare_v0_3.py` import v1.09;
    - folder and root README (sections, variables, indicator count, files), TODO.
  - MTOutputs: 58 indicators (adds fuel use of power, revenues of power, existing carbon pricing revenue and prices). Deck `presentation/CPAT-AI-Mitigation-MVP_v2.1.pptx` (from v1.09) and documentation v1.09.
- **Checks** (`check_report_v1.09.md`): Overall PASS.
  - 133,331 formulas in 30 sheets, none over 100 characters, no LAMBDA calls, zero LibreOffice errors.
  - Values equal the independent Python recomputation (fuel and revenue totals with power, power revenues by type) in every scenario test.
  - Existing carbon pricing with non-zero test data (shipped scenarios, growth, switched off, complementary carbon tax) equals Python; `xcpd` = 0 up to 2024.
  - Regression vs v1.08: 4,592 shared codes, max difference 0 outside the intended changes (fuel and revenue totals, their reference and change rows).
  - New consistency section: check rows and identities in every column, file references in the workbook texts, versions, no stale texts, one current method note each.
- **Caveats:**
  - **Fuel and revenue totals now include power.** The totals of v1.09 are not comparable with v1.08. Fuel use 2022 is 86.4 Mtoe, of which 36.7 Mtoe is power generation. Revenue totals add power: in 2022 USD 14.4 bn of subsidies on the gas and oil used for generation and a USD 6.2 bn electricity subsidy gap.
  - **The electricity subsidy gap is signed** (negative when the tariff is above the modelled supply cost). Fuel subsidies are positive parts only. The two do not overlap: the supply cost already uses the subsidised fuel price.
  - **Existing carbon pricing simplifications** (listed in LegacyDiff):
    - one ETS per country (national, else the regional EU ETS; DEU and AUT keep only their national ETS);
    - a single carbon tax rate (legacy fuel-specific rates `ecr.<fuel>` are not used);
    - coverage of the last data year (coverage carried forward over blank years);
    - existing ETS revenue at the full permit price (free allocation not used);
    - existing and new ETS add up where both cover a sector.
  - **Only the change against the price data enters prices.** The IMF retail prices already contain the existing carbon pricing of their year, so the level is a memo (`xcp`, `rxcp`). Coverage differences within a price fuel cannot be in the price data, so `xcpd` uses the embedded level of the same subsector and fuel.
  - **Not run in Excel yet.**

## 2026-10-11 - CPAT-AI-Mitigation-MVP v2.2: one version number; register of bugs, issues and upgrades; quick start

- **Task (user):** "Make sure we have consistent human readable bug list and potential issues or upgrades list in word format. Update all versions to 2.2. Check for consistency. Add quick start guide / intro at beginning of word document. Include guide to structure of repo."
- **Built:**
  - **One version number.** Every current file of `excel_ai_new/mitigation/` has version 2.2: the workbook `CPAT-AI-Mitigation-MVP-v2.2.xlsm`, `build_v2_2.py`, `check_v2_2.py`, the data-step and helper scripts, `CPATScenarios_v2_2.bas`, the method and background notes, the Word documents and the deck `presentation/CPAT-AI-Mitigation-MVP_v2.2.pptx`. The previous versions are in `Old/` (and `presentation/Old/`). Results are unchanged.
  - **Register of bugs, issues and upgrades.** `issues_register_v2_2.py` is the single source. It feeds `CPAT-AI-Mitigation-MVP_BugsIssuesUpgrades_v2.2.docx` (`make_issues_doc_v2_2.py`) and the appendices of the documentation. IDs:
    - L1-L16: legacy CPAT bugs, with the effect of each power fix computed when the document is built;
    - M1-M9: bugs of earlier MVP versions, all fixed;
    - I1-I14: known issues;
    - LD<#>: the LegacyDiff rows of type Not yet, Simplification or To check;
    - U1-U16: upgrades by priority.
    - It replaces `PowerModel_BugsAndImprovements_v1_0.docx` (now in `Old/`).
  - **Word documentation v2.2** opens with `QuickStart_v2_2.md`: what the MVP is, a quick start in seven steps, how to rebuild, a guide to the repository (top level, `excel_ai_new/`, the MVP folder) and to the workbook sheets. Appendix E lists the register by ID, appendix F the upgrades by priority.
- **Consistency fixes:**
  - LegacyDiff: the row "Existing ETS and existing carbon taxes: Not modelled" removed (modelled since v1.09); the formula-structure row described the v1.07 LAMBDA right column. The sheet now points to the register.
  - Notes and scripts naming old versions (ETS note: ets_goalseek_v0_2; VBA module comment; script headers).
  - `legacy_comparison` was the v1.01 note and its script wrote another file name. It is re-run on v2.2: mean absolute difference to legacy 45.6% with prices to 2024, 17.3% with prices to 2022 (unchanged, cause I4).
  - **Repository guide:** the root README described `egypt/`, `egypt-final/` and `excel_ai_new/standalone_working_version/`. These were removed on 2026-10-09 (commit f070c20); the kernel working version is in `excel_ai_new/old/standalone_working_version/`. The root README layout is corrected; `NORMS.md`, `TODO.md` and `AGENTS.md` got a note at the top (their Egypt paths are kept for reference).
- **Checks** (`check_report_v2.2.md`, Overall PASS):
  - regression vs v1.09: 5,556 shared codes, max difference 0;
  - every current versioned file of the folder carries 2.2 (27 files);
  - register IDs unique, all 17 LegacyDiff rows of the listed types included;
  - no stale texts, file references valid, all earlier checks as v1.09.
- **Caveats:**
  - **Tool scripts were renamed, not rewritten.** Their headers say so. Old cross-references inside `Old/` still use the old names.
  - **The Egypt material is no longer in the repository.** NORMS, TODO and AGENTS still describe the Egypt workflow; decide whether to delete those parts.
  - **Not run in Excel yet** (I1).

## 2026-10-12 - CPAT-AI-Mitigation-MVP v2.3: last year 2041 as the LAMBDA year; legacy moving-average fuel prices for power; Egypt parts removed from NORMS, TODO, AGENTS

- **Task (user):** "Delete the Egypt parts from NORMS, TODO and AGENTS. For moving average prices, we go what is in legacy. Please note that the LAMBDA functions should be a full year as part of the flow. Let's go with 2041, which will be our last year."
- **Built:**
  - **Repository documents.** The Egypt parts are deleted from `NORMS.md` (key documents, reference implementation, EGY flag rule, working-version folder, task-inventory step, superseded copies), `TODO.md` (Egypt checks and modelling sections, kernel conventions) and `AGENTS.md`.
  - **Horizon 2041, the LAMBDA year** (`build_v2_3.py`):
    - the last year is 2041 (legacy horizon of the power block); power data re-extracted to 2041 (`extract_power_v2_3.py`; 2022-2040 unchanged);
    - every calculated cell of 2041 calls its named LAMBDA (light beige, dark red text) and feeds the results like any year;
    - 2022-2040 keep plain formulas of at most 100 characters.
    - NORMS section 3 records the rule.
  - **Fuel prices for power as legacy (A18):** new row `fpp` = centred 5-year moving average (years t-2 .. t+2 within 2022-2041, blanks ignored as legacy) of the price before new policies. Settings C21 `SpotPow` = Yes gives spot prices (legacy option). `vbc` uses `fpp`.
  - **Levelised variable cost window to 2041** as legacy (closes I9/U12 of v2.2).
  - **Hosts without LAMBDA support** (Excel before 365, LibreOffice) still calculate 2022-2040:
    - `tvcx` = IFERROR(tvc, last year's tvc) feeds the D9 window;
    - `fpp` averages with AGGREGATE (errors skipped), so the 2041 prices are left out of 2039-2040 there.
  - **Consistency:** the total rows were labelled "All subsectors" although they include power since v1.09; the label is now "All sectors" (M10). Register updated: I2, I9, I10 rewritten; moving average and window upgrades closed.
  - **VBA year count (M11).** The macros had 19 years as a constant; found by the check and set to 20, and the builder now asserts it.
  - Every current file renumbered to 2.3 (previous versions in `Old/`); documentation, register and deck v2.3; legacy comparison re-run (unchanged: 45.6% / 17.3%).
- **Checks** (`check_report_v2.3.md`): Overall PASS.
  - 139,801 formulas; 4,888 cells call a named LAMBDA, all in 2041; plain formulas at most 99 characters.
  - In LibreOffice (no LAMBDA support) errors only in 2041 (5,184 cells); price and subsector rows 2022-2040 identical to the LAMBDA host; power within 0.01%.
  - Values (LAMBDA year expanded) equal the Python recomputation with moving-average fuel prices and the window to 2041, in every scenario test.
  - Regression vs v2.2: 3,854 shared codes, 0 outside the intended power changes.
  - Macro batch run and CheckBatchRun in LibreOffice match the stored results (1.7e-14).
- **Caveats:**
  - **2041 needs Excel 365.** Elsewhere 2041 shows errors (Mitigation and the 2041 column of MTOutputs). The power look-ahead there uses last year's values for 2041, so power results 2022-2040 differ slightly from Excel 365 (size in the check report). Stored results are the Excel 365 values.
  - **Results changed against v2.2** for power and everything that includes it (fuel use, CO2 and revenue totals, electricity prices, the ETS baseline). Price and subsector rows are unchanged.
  - **Not run in Excel yet** (I1).

## 2026-10-13 - CPAT-AI-Mitigation-MVP v2.4: labelled parameters, one outline level, years in row 1, no hard-coded constants, subsidies negative

- **Task (user):** "In mitigation. Can you make sure that all the numbers in columns D-G of mitigation are labelled (often twice, including at top of each tab). Please avoid double grouping - two levels. Could you put years in row 1? It will be obvious that they are years. Could you avoid hard coding any constants. They need to be looked up. Could you adopt the norm of subsidies as negative?"
- **Built** (`build_v2_4.py`; every current file renumbered to 2.4, previous versions in `Old/`):
  - **Labels for D:G.** A label row sits above every block of rows: column H names the variable, D:G the name of each parameter, looked up from `Variables` G:J (320 label rows; they replace the blank separator rows). In section 1 the sub-heading rows carry the labels (two new sub-headings: OBR share, shadow price on the efficiency margin). Row 1 of D:G says "Param n: see label row". Interpretation: "top of each tab" was read as "top of each block"; the labels also stay in `Variables`.
  - **One level of row groups.** Subsector headings and their electricity memo line are visible; each subsector's variables form one group (no nesting).
  - **Years in row 1** of every scenario group; row 4 is empty (rows 5-9 unchanged, so the macros and defined names still find them).
  - **No hard-coded constants on Mitigation:**
    - MTInputs rows are looked up on a new table on `Mapping` (121 keys: by NameOfParameter, or by label below its MTInputs heading for the unnamed rows) instead of typed row numbers;
    - new sheet `Constants`: named constants `HoursYr`, `kWperMW`, `USDperM`, `MWyMkWh` (= 8.76, a formula), `PriceFloor` (0.01), used in Mitigation formulas, the LAMBDAs and `Inputs_power`; and 77 policy assumptions without an MTInputs row, looked up by key (biomass coverage, regulations placeholder, ETS benchmarks, ETS groups and semi-elasticities, feebate sector positions, High/Low international price factors, power scale factors);
    - new data sheet `BaselineCO2` for the baseline CO2 by ETS sector (written by the build; the `bco2` rows look it up).
  - **Subsidies negative:** `esub` = min(txo, 0), `esubpu`, `rsub`, `prsub`, `sgap` = price before VAT - supply cost, `rgap`; `rnet` = `rtx` + `rsub` (same value as before). Labels, notes, ReadMe, LegacyDiff (two new rows: sign of subsidies, constants and row pointers), register (I6 rewritten; I15, I16 new) and the method notes follow.
  - NORMS section 3 records the five rules.
- **Checks** (`check_report_v2.4.md`): Overall PASS.
  - New section 8b: years in row 1; 2,136 rows with D:G values, every used column labelled; no typed number below the top rows and no numeric constant in a Mitigation formula; all 121 MTInputs rows found = the template rows; `BaselineCO2` complete.
  - One level of row groups; 143,195 formulas, at most 99 characters; errors in LibreOffice only in 2041.
  - Regression vs v2.3: 5,592 shared codes, max difference 1e-11, with the subsidy rows compared as new = -old (98 non-zero). All scenario tests, ETS goal seek (18 iterations), macro runs and CheckBatchRun as before. Legacy comparison unchanged (45.6% / 17.3%).
- **Caveats:**
  - **Allowed in formulas besides 0 and 1:** AGGREGATE function codes, text lengths in LEFT(switch, n), the choice codes 1/2/3 of the price adjustment, the factor 2 and the square in the long-term storage cost (legacy functional form). The scenario number of group 1 (row 5) and the ETS override row remain typed inputs.
  - **Subsidy rows changed sign:** outputs stored with v2.3 or earlier have the opposite sign in these rows (I15).
  - **A new block needs its label row** (copy it with the block; new variables need labels in Variables G:J) (I16).
  - **Not run in Excel yet** (I1).
  - **Repository layout changed on main during this task** (commit 2554550: everything Excel-side moved into `excel_ai/`, root documents included; CSV and .bas line endings converted to LF). v2.4 was replayed onto that layout; the legacy-workbook paths of `extract_data_v2_4.py`, `extract_ecp_v2_4.py`, `extract_power_v2_4.py` and `legacy_compare_v2_4.py` and the repository guide in `QuickStart_v2_4.md` follow it. The repository README (`excel_ai/README.md`) and the method notes still name `excel_ai_new/` in places (descriptive text, not used by any script).

## 2026-10-13 - CPAT-AI-Mitigation-MVP v2.5: price section as a build-up by fuel and sector

- **Task (user):** reorder section 2 into a price build-up by fuel (outer) and sector (inner), in the existing format, reusing the existing rows; one meaning per parameter column, with only parameters that depend on fuel and sector; the fixed part of the supply cost as its own row (12 extra rows accepted); new policies stay in the subsector blocks (their reordering is the next step, option B).
- **Built** (`build_v2_5.py`; every current file renumbered to 2.5):
  - Section 2: 8 fuel heading rows (visible when rolled up; they and the section sub-heading name D:G), then per price fuel a block of 9 rows: `spf` fixed part of the supply cost (new: base-year value, then constant), `sp`, `txf`, `txo`, `etx`, `esub`, `vat`, `rpb` (visible), `esubpu`. 116 rows (was 104).
  - D:G mean the same in every block: D pass-through, E VAT rate, F GJ per price unit, G international price position (kept as a parameter: fuel-only, and the supply-cost formula would exceed 100 characters with a Mapping lookup). Price position and the last historical values are no longer parameters.
  - `txf` is now the excise and other taxes before the floor (txo_L x pcc + the legacy floating part), computed year by year from the change in the supply cost; `txo` applies the legacy floor with its own last historical value, read from its row at the column number in row 4 (new helper row, = COLUMN() + LastHist - year).
  - History lookups by price code (defined names IPKey, IPsp, IPtxo); other sections find a price by block position (Inputs_prices `pos`, now the block position). LAMBDAs SUPPLYCOST, OTHERTAX, FLOATTAX take the price code.
- **Checks** (`check_report_v2.5.md`): Overall PASS. Regression vs v2.4: 5,568 shared codes, max difference 1e-10, apart from the redefined `txf` (24 codes, intended); new codes `spf`. All scenario tests, the ETS goal seek (18 iterations) and the macro runs as before; legacy comparison unchanged.
- **Caveats:**
  - **No blank rows between the sector blocks of a fuel** (the fuel heading rows separate the fuels), to keep the row count down.
  - **Row 4 is a helper row** (column number of the last historical price year); copying a scenario group copies it with the group.
  - **`txf` changed meaning**: outputs stored with v2.4 or earlier hold the floating part only.
  - **Not run in Excel yet** (I1).

## 2026-10-13 - CPAT-AI-Mitigation-MVP v2.6: formatting (price parameter tables, one group per section, tab groups)

- **Task (user):** price blocks with a little table of settings at the top and the international reference price and fixed part as rows outside the build-up; spacing between build-ups as in legacy; no grey or beige in the parameter columns; few row groups, each section ending with its aggregate row (the only row shown rolled up); names not bold; tab groups MAIN, INPUTS, REF (and DATA); merging the input tabs later.
- **Built** (`build_v2_6.py`; every current file renumbered to 2.6):
  - Section 2: per fuel a heading row and a blank row; per fuel | sector a block of 13 rows: heading row naming D:G, parameter row `pset` (D pass-through, E VAT rate, F GJ per price unit, G international price position), `gpi` international reference price (new, time series), `spf`, the 8 build-up rows (no parameters of their own; they refer to the block's parameter row, so a block copies as a whole), blank row.
  - One row group per section; its last row is the summary shown rolled up: carbon price (moved to the end of section 1), power generation fuel use (new row `pet`, end of section 3), sector fuel use, total fuel use, total revenue, total CO2 (moved to the ends of their sections, after the notes). Section 2 shows its band only.
  - Names in A:C never bold; no fill colour in D:G outside the bands; the band of section 1 no longer carries a D label.
  - Tabs: MAIN->> (Mitigation, MTOutputs, StoredResults, ScenarioCompare, MTInputs, Charts, Settings), INPUTS->> (Inputs, Inputs_prices, Inputs_power, Mapping, Constants), REF->> (MacroCheck, ReadMe, LegacyDiff, Lambdas, Variables), DATA->>.
- **Checks** (`check_report_v2.6.md`): Overall PASS. Regression vs v2.5: 5,616 shared codes, max difference 0; new codes `pset`, `gpi`, `pet`. New checks: one group per section with only the band and summary row visible, tab order, names not bold, plain D:G. The first run failed one old tab-order expectation in the format check (fixed).
- **Caveats:**
  - **Section 2 grew to about 190 rows** (parameter tables and spacing); rolled up it shows its band only.
  - **Input tabs not merged yet** (agreed as a later step).
  - **Not run in Excel yet** (I1).

## 2026-10-13 - CPAT-AI-Mitigation-MVP v2.7: Excel repair error fixed, macro buttons, formatting

- **Task (user):** Excel asked to repair the file ("Removed Records: Formula from /xl/worksheets/sheet2.xml part"); buttons on ScenarioCompare to run the macros; short light-green section headings; dark green title just "Mitigation Module"; summary rows at 0 dp; default column width 10.14 (76 px); variable names in column A light green.
- **Built** (`build_v2_7.py`; every current file renumbered to 2.7):
  - **Repair error cause:** the defined names `BCO2Key`, `BCO2Val`, `BCO2Year` (baseline CO2, v2.4) begin with `BCO2`, a valid cell reference (column BCO, row 2). Excel cannot parse the 2,040 `bco2` formulas on Mitigation (sheet2.xml) that use them and removes them on repair; LibreOffice accepts them, so the checks did not see it. Renamed to `BaseCO2Key`, `BaseCO2Val`, `BaseCO2Year`; the check now fails on any defined name that begins like a cell reference.
  - Six buttons on ScenarioCompare (columns N-P): Run all scenarios, Store baseline, Store live scenario, Solve ETS (live scenario), Clear stored scenarios, First-run test. Drawing shapes assigned to the macros, added after the VBA project is embedded.
  - Title "Mitigation Module" (version in the Settings log, ReadMe and file name); section headings at most 30 characters; summary rows `#,##0`; default and year column width 10.14; column A of variable rows light green (E2EFDA).
- **Checks** (`check_report_v2.7.md`): Overall PASS; regression vs v2.6 max difference 0.
- **Caveats:**
  - **Buttons not tested in Excel** (drawing shapes with macro links, written without Excel; LibreOffice opens the file). If a button does not run its macro, assign it by right-click > Assign Macro, or use Alt+F8.
  - **No 2042 power look-ahead column**: in Excel 365 the 2041 values are already complete (the levelised window, which the user asked not to extend, and the fuel-price moving average are the only look-ahead parts); open until the user re-checks 2041 in v2.7 (formulas removed by the repair could explain the unreliable 2041 numbers seen in v2.6).
  - **Not run in Excel yet** (I1).

## 2026-10-13 - CPAT-AI-Mitigation-MVP v2.7 (rebuilt): the real cause of the Excel repair error, 2041 power, formatting

- **Task (user):** the v2.7 test copy still gave "Removed Records: Formula from /xl/worksheets/sheet2.xml part", and power generation fuel use fell from 60,690 in 2040 to 0 in 2041; variable names should be lighter text, not a green fill; bold only on summary and total rows; MTInputs and Settings are input sheets.
- **Cause:** seven named LAMBDAs had parameter names that Excel reads as cell references: `y1` (cell Y1) in PATH, PATHYEARS, CAPCHANGE and ETSCAP; `co2` (cell CO2) in PNEWREV; `c` (R1C1 column) in LOWEST3; `tco2_kwh` (begins like cell TCO2) in KWHPOLICY. Excel removed the 90 cells of 2041 (column AE of Mitigation, the LAMBDA year) that call them, including LOWEST3 in the power dispatch, so 2041 power and everything downstream read 0. LibreOffice accepts these names, so the checks did not see it, and the earlier v2.7 entry wrongly put the repair error down to the `BCO2*` defined names alone (renaming those was harmless and is kept). Not a missing look-ahead year.
- **Fixed:** parameters renamed (`start_yr`, `target_yr`, `emissions`, `x`/`y`/`z`, `intensity`); the check fails on any LAMBDA parameter or defined name that reads as a cell reference (A1, or R1C1 such as `r`, `c`); new rule in NORMS.md.
- **Formatting:** column A of variable rows in light green text (`70AD47`), no fill; bold only on the section summary rows (values, not names); tab order MAIN->> Mitigation, MTOutputs, StoredResults, ScenarioCompare, Charts; INPUTS->> MTInputs, Settings, Inputs, Inputs_prices, Inputs_power, Mapping, Constants.
- **Caveats:**
  - **Still not opened in Excel by me**: a remaining formula Excel cannot parse would show the same message. The no-VBA test copy is the quick test.
  - **The 2042 look-ahead column** stays off until 2041 has been checked in Excel with this build.

## 2026-10-13 - Repository documents split by project; visual style guide from the legacy sheet

- **Task (user):** the repository holds two projects (AI-coded Excel, AI-coded Python), so give each its own documents; a root README that says clearly what is for whom; extend the visual guide: subsections should follow the legacy conventions (sub-heading fonts, borders, white space and empty rows); add the adjustments still needed to the TODO.
- **Inputs:** root `README.md`, `AGENTS.md`, `NORMS.md`, `excel_ai/plans/TODO.md`; legacy `Mitigation` sheet styles (fonts, fills, borders, blank rows) read from an xlsx conversion of `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb`.
- **Outputs:**
  - `README.md` (root): "Who reads what" table (Excel users, Excel builders, Python developers, AI agents, anyone finishing a task), repository layout by project, how the projects relate.
  - `NORMS.md` (root): rules for every task only (sections 6 and 7, numbers kept); Excel sections 1-5 moved (git mv) to `excel_ai/NORMS.md`, which gains section 2 "Visual style guide" (2.1 colours, 2.2 fonts, 2.3 borders, 2.4 white space) and fixed paths (`excel_ai_new/` -> `excel_ai/`).
  - New `excel_ai/README.md` (Excel folder map), `coded/README.md` (Python layout, conventions, getting started), `coded/TODO.md`.
  - `AGENTS.md` routes to the project documents; `excel_ai/plans/TODO.md` gains the style-alignment item (eight differences between the mitigation MVP and the legacy style); the mitigation QuickStart repository guide follows the new layout.
- **Caveats:**
  - **Legacy title band fill is `00AE49`**, not the `00B050` NORMS and the MVP use; listed in the TODO, not changed yet.
  - **Style differences not applied to the workbook yet** (TODO item): sub-section headings, header-row borders, block top borders, blank rows around bands, font size 9 vs 10-11, italic codes and notes, boxed parameter tables. Where the legacy and a user rule differ (bold, blank rows between price blocks), the user rule wins.
  - **`coded/TODO.md` holds one item** (port the mitigation MVP logic); Python open work was not tracked before.
  - Older CAVEATS entries and `Old/` files still cite `NORMS.md` sections 1-5 at the root and `excel_ai_new/`; the root README explains both.

## 2026-10-14 - CPAT-AI-Mitigation-MVP v2.7: equation list (complete mathematical description)

- **Task (user):** a complete mathematical description of the model: an equation list plus the list of modifications and adjustments against legacy CPAT; to be built before the non-CO2 GHG work.
- **Inputs:** the shipped workbook `CPAT-AI-Mitigation-MVP-v2.7.xlsm` (Mitigation formulas, scenario 1, 2022-2041), the variable dictionary, `LEGACY_DIFFS` and the LAMBDA library of `build_v2_7.py`, the register (`issues_register_v2_7.py`).
- **Outputs:** `make_equations_v2_7.py` -> `Equations_v2_7.md`: section A, 210 variables in model order, each with its equation by year range (cell references as variable codes `code[f,s](t)`, parameters `<label>` with their own lookups, rows and years with the same equation shown once; 2041 as the LAMBDA call), description, legacy reference and the changes that touch it; section B, the 42 LegacyDiff rows and the register's legacy and MVP bugs with the equations they touch; section C, the LAMBDA library; section D, an index. The check regenerates it and fails if a variable of the dictionary has no equation (`check_report_v2.7.md`: PASS); appendix G of the Word documentation; README and QuickStart list it. No workbook change.
- **Caveats:**
  - **Generated, not edited:** the text is as exact as the formulas but terse; positional lookups read `X[<price position>]`, sums over the sector blocks read `SUMIFS(block{...},SecVar,...)` (explained in the notation).
  - **The change-to-equation links (section B) are a hand-made map** in `make_equations_v2_7.py` (`MODS`); new LegacyDiff rows need an entry there.
  - **Method notes stay** for the narrative; the equation list is the reference for what the workbook computes.

## 2026-10-14 - Excel encoding lessons in the norms; plan to install the MVP's LAMBDAs by macro

- **Task (user):** fold the distribution workbook's lessons into the norms and draft the switch of the mitigation MVP to the distribution approach (LAMBDAs installed by a macro, not encoded in the file).
- **Inputs:** `excel_ai/distribution/LESSONS_LEARNED.md`; the MVP's repair errors (v2.4-v2.8: cell-like names, cell-like LAMBDA parameters, MAXIFS without its `_xlfn.` prefix found before shipping).
- **Outputs:** `excel_ai/NORMS.md` section 3b (nine rules: let Excel encode LAMBDA and newer functions, names Excel cannot read, one namespace, no silent error handling, arrays, pattern scans, round-trip of generated code, unique table headers, design in Python and encoding tested in Excel); the earlier Excel-names rule now points there. `excel_ai/mitigation/LambdaInstall_Plan_v2_8.md`: the switch (shipped file without LAMBDA encoding, 2041 plain; InstallLambdas / RemoveLambdas macros with an in-Excel self-test on MacroCheck; checks; cost; decisions).
- **Caveats:**
  - **Not built**: the plan waits for the user's decisions (section 8 of the plan); the MVP still writes its LAMBDAs into the file.
  - **The current LAMBDAs use `year` as a parameter**, which rule 2 now discourages; renaming is part of the plan.

## 2026-10-14 - CPAT-AI-Mitigation-MVP v2.8: non-CO2 GHGs and methane

- **Task (user):** start on non-CO2 GHGs and methane (first item of the legacy gap list), after the equation list; the plan's six decisions were not answered, so the proposals were applied as defaults.
- **Inputs:** legacy Mitigation sections 9, 13-15 and key inputs 7-8 (formulas from the xlsx conversion, cached values from the xlsb); legacy sheets GHGs, CH4Inputs, EF_PM, UNPop and the energy balance rows (`extract_ghg_v2_8.py` -> data/ghg_inventory.csv, ch4_inputs.csv, ef_nonco2.csv, population.csv, energy_balance.csv); MTInputs rows 184-189, 207, 239, 240.
- **Outputs:** every current file renumbered to 2.8 (v2.7 in Old/); `build_v2_8.py`: section 14 "GHG emissions" (drivers; methane by source: allocation of the inventory, activity, abatement by the methane fee along the CH4Inputs curves, emissions; combustion CH4 by sector; calibration of energy CH4 to the inventory; flaring CO2; the inventory categories by gas, inventory while it has the year and projected after; totals by gas and category; summary line total GHGs excluding LULUCF), the methane fee in section 1, a `ch4` row in every sector block, methane fee revenue in section 12 (in total revenue), data sheets GHGs, CH4Inputs, EF_NonCO2, UNPop, Balances, 15 LAMBDAs; `GHG_Method_v2_8.md`; register L18-L21 (legacy bugs fixed), I17-I18; LegacyDiff rows 43-48; legacy comparison with a GHG table; equation list, Word documentation, deck, working_version. Check (`check_report_v2.8.md`): Overall PASS; regression vs v2.7 max abs diff 0 on 5,666 codes; section 14 and the ch4 rows equal an independent Python recomputation in every scenario test; new scan: newer Excel functions carry the `_xlfn.` prefix.
- **Caveats:**
  - **Defaults applied without the user's answer**: non-energy methane grows and is abated (legacy: constant); flaring as CO2 (legacy: added to CH4); industrial processes follow only increases of industrial energy CO2 (legacy); production of oil, gas, coal held at the base year; energy N2O with energy CO2; no effect of the methane fee on producer prices; the fee keeps rising after the target year (legacy); one fee for every source.
  - **Population from UN WPP**, not the legacy growth path (L20): agriculture, waste and other are lower than legacy after 2030.
  - **Egypt's inventory breaks after 2021** (I17): calibration to 2024 may understate energy methane by about 19 Mt CO2e.
  - **Energy CO2 without inventory adjustment** (I18): GHG totals start below the inventory (2022: 414.6 vs 442 Mt CO2e excluding LULUCF).
  - **Combustion CH4 factors** from the GAINS base and final values only (paths stripped in the NoPropData file); the calibration factor is 0.25 for Egypt.
  - **Industrial processes are lower than legacy from 2024** (57.2 vs 66.5 Mt CO2e in 2024, 94.9 vs 119.2 in 2040), although both follow industrial energy CO2; not yet explained (the comparison note does not cover it).
  - **Not in MTOutputs or the charts yet**; local pollutants not built.
  - **The first full check found six names that read as cell references, 295 over-long formulas, a typed column number, missing labels and a whole-row test gap**; all fixed before release (the checks did their job).

## 2026-10-14 - CPAT-AI-Mitigation-MVP v2.9: local air pollutants
- **Task (user):** "Scope out then do local air pollutants".
- **Inputs:** legacy Mitigation pollutant rows (factor paths 1052-1663, forcing 7459-7530), legacy sheets EF_PM (GAINS), the GWP table of the pollutants and the GAINS region mapping (`extract_ghg_v2_9.py` -> data/gwp_pollutants.csv, gains_region.csv).
- **Outputs:** every current file renumbered to 2.9 (v2.8 in Old/); `build_v2_9.py`: section 15 "Local air pollutants" (factor-path weight `ap.w`; PM2.5, NOx, SO2, VOC, BC, OC, CO by subsector and power generation, sector and pollutant totals, total PM2.5 as the summary line; forcing memo `apf` with the GWP100 of the GAINS region), base and final factors in Inputs and Inputs_power, data sheets GWP_AP and GainsRegion, LAMBDAs EFWEIGHT and POLLUTANT; `AirPollutants_Method_v2_9.md`; register L22; LegacyDiff rows 48-51; equation list, Word documentation, deck, working_version. Check (`check_report_v2.9.md`): Overall PASS; regression vs v2.8 max abs diff 0 on 6,126 codes; section 15 equals an independent Python recomputation; 164,896 formulas, none over 100 characters.
- **Caveats:**
  - **Factor mapping is an assumption**: services take the residential factors, rail the road factors, industry and other energy use the manufacturing factors (legacy: zero where GAINS has no match).
  - **Navigation included** in the totals (legacy omits it, L22), so totals are above legacy where navigation burns fuel.
  - **Linear factor path** between the GAINS base and final factors to EFEndYear (the year-by-year paths are stripped in the NoPropData file), as for combustion CH4.
  - **Not built**: the split into the air-pollution module sectors, primary organic matter, other PM2.5, ammonia; no pollutant indicators in MTOutputs or the charts yet; no pollutant table in the legacy comparison note yet. Against the legacy cached forcing (Mitigation rows 7516-7522), 2022 is close: total -17.5 vs -16.3 Mt CO2e; CO 4.86 vs 4.86, BC 11.0 vs 10.8, VOC 2.26 vs 2.27, OC -4.37 vs -4.32, NOx -5.65 vs -5.54, SO2 -25.6 vs -24.3. By 2040 they diverge (BC 17.9 vs 12.2, total -18.5 vs -20.9) with the different fuel paths and factor paths.
  - **Forcing is net negative** for Egypt (about -17.5 Mt CO2e in 2022) because OC, SO2 and NOx cool; it is a memo and not in the GHG totals.

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.0: air-pollution sectors, GHG and pollutant outputs, legacy pollutant tables
- **Task (user):** "Do it 123": (1) split the pollutants into the air-pollution module sectors with primary organic matter and other PM2.5; (2) GHG and pollutant indicators in MTOutputs and the charts; (3) pollutant tables in the legacy comparison.
- **Inputs:** legacy Mitigation rows 6693-7446 (air-pollution sectors, POM = 1.3 x OC, other PM2.5) and 7516-7522 (forcing), cached values from the xlsb.
- **Outputs:** every current file renumbered to 3.0 (v2.9 in Old/; 3.0 follows 2.9 as 2.0 followed 1.09); section 15 rows `aps` (seven sectors per pollutant, POM, other PM2.5), constant PomPerOC, LAMBDA OTHERPM; MTOutputs +10 indicators (68), four new charts (14); register L23; LegacyDiff rows 51-53; legacy comparison with three pollutant tables; `GDP_Plan_v3_0.md` (plan for the next item, decisions open). Check: Overall PASS; regression vs v2.9 max abs diff 0 on 6,436 codes; 168,861 formulas, none over 100 characters.
- **Caveats:**
  - **L23 has no effect on the legacy Egypt numbers**: the legacy total formula leaves out services and food & forestry, but they emit zero in the legacy run (its total equals the sum of its sectors). My first draft of the comparison note said otherwise; corrected before release.
  - **MVP pollutants are above legacy from 2024** (PM2.5 2040: 128.6 vs 93.1 kt), mainly through road fuel use (the known fuel-use gap, `legacy_comparison_v3_0.md`); 2022 matches closely (90.8 vs 89.2 kt).
  - **Food split not built** (zero share for Egypt); no ammonia from combustion (none in legacy either).
  - **Sum-type sector rows** (other power plants, ground level road/other, other, food & forestry) are differences or sums of section 15 rows, so their 2041 cells do not call a LAMBDA (same rule as the other totals).

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.1: GDP effects
- **Task (user):** plan GDP effects, then "Go with recommendations" (fix the level-into-growth bug, new-policy revenue, endogenous effects on by default, all income-group multipliers with low/high).
- **Inputs:** legacy Mitigation section 17 (rows 8028-8290), section 11 (1766-1779), rows 2176-2184 and 2442-2446; legacy sheet Multipliers rows 90-203 (cached values); legacy row 465 (baseline GDP, USD bn) -> `extract_gdp_v3_1.py`, data/multipliers.csv, data/gdp_level.csv.
- **Outputs:** every current file renumbered to 3.1 (v3.0 in Old/); section 16 "GDP effects" (inputs from MTInputs 197-201, 226, 263, 267; fiscal space, impulses and 19 lag rows; multiplier key; GDP effect by revenue use; level factor; post-policy GDP), row 7 GDP growth after the feedback; sheet Multipliers (5 groups x base/low/high x 8 instruments x lags 0-19); 8 LAMBDAs; MTOutputs +3 rows, one chart; register L24; LegacyDiff rows 54-57; `GDP_Method_v3_1.md`; check with an iterated Python recomputation (the whole model on the growth path). Check: Overall PASS; scenario 1 vs v3.0 max abs diff 1e-16 on 3,283 codes; scenario 2 changes as intended; 171,283 formulas, none over 100 characters.
- **Caveats:**
  - **No legacy benchmark**: the legacy GDP-effect rows are stripped to 0 in the NoPropData file; the numbers rest on the legacy multipliers and our own formulas, checked only against our Python copy.
  - **Methane fee revenue is not in the fiscal space** (would make 2022-2023 circular through the GHGYear allocation); subsidy-reform savings are not counted either.
  - **Scenario-1 lookups changed** (co2.ref, ghg.ref, rtot.ref, fis.ref end at their own column) to keep Excel free of circular references; values unchanged. A dependency search of scenarios 1-2 found no cycle, but Excel itself has not opened v3.1 yet.
  - **The first full check failed** on a too-short Variables range (269 variables, range 260), a formula pushed to 101 characters by 9 new section-1 rows (inputs moved to section 16) and a sanity test that GDP effects invalidate; all fixed before release.
  - **Scenario 2 results move**: GDP about +0.3% by 2040, so fuel use, emissions and revenue of every policy scenario differ slightly from v3.0.

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.2: CO2 calibration; documentation tidy
- **Task (user):** calibrate energy CO2 to the inventory ("Go with recommendations": GHGYear 2024, EFs everywhere, on by default); then "Tidy up the repo and make documentation and deck more concise and readable. Separate code equations from implementation details. Emphasise legacy side bug fixes needed."
- **Outputs:** every current file renumbered to 3.2 (v3.1 in Old/); Settings C27-C30 and `EFCalib` (inventory / scenario-1 energy CO2 with uncalibrated EFs in GHGYear; Egypt 0.960) on every CO2 EF, raw CO2 row on sheet BaselineCO2 written by the build; `CO2Calibration_Method_v3_2.md`; register I18 resolved; LegacyDiff row 57. Documentation: new `Equations_v3_2.md` (the model in 95 equations, mathematics only); the generated formula listing renamed `Formulas_v3_2.md` (implementation reference); new `LegacyBugFixes_v3_2.md` (23 legacy bugs by priority, 7 high, generated by `make_legacy_fixes_v3_2.py` from the register); method notes tightened (implementation detail removed); README, QuickStart, TODO rewritten short; Word documentation reordered (quick start, equations, legacy fixes, methods; formula listing and register table no longer pasted in); deck 11 → 10 slides with a legacy-fixes slide; finished plans (GDP, calibration, LAMBDA install, ETS cap options) and deck images v2.3-v3.1 moved to Old/. Check: Overall PASS; scenario-1 fuel use and prices vs v3.1 max abs diff 0 on 3,086 codes; 171,287 formulas, none over 100 characters.
- **Caveats:**
  - **The calibration factor is static data** (BaselineCO2 row raw, refreshed by the build); after a change of country or base data, rebuild, as for the ETS baseline. It assumes scenario-1 fuel use does not depend on the EFs (true for Egypt: no carbon price and no existing pricing).
  - **2022 stays below the 2022 inventory** (215.8 vs 252.2 Mt) because of the 2021-2022 inventory break (I17).
  - **Equations_v3_2.md was drafted by a subagent** from the generated formulas and the method notes and spot-checked, not checked line by line; a few rules are stated at the level confirmed (inventory projection rules, scenario-1 methane shares, electricity consumption split). The first full v3.2 check failed on one formula of 114 characters (Settings C29), split before release.
  - **Legacy bug priorities** (high / medium / low) are my judgement from the register's effects; L24's effect is not visible in the NoPropData file (rows stripped).

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.3: no country-specific terms outside the reference tables
- **Task (user):** "We can't have hard coded terms here. Nothing is Egypt specific except reference tables."
- **Inputs:** legacy sheet ETS+LTS rows 80-256 (semi-elasticities of 175 countries) -> `extract_ets_v3_3.py`, `data/ets_semi.csv`; an audit of the builder, check, Python references, extract scripts and the equations note for Egypt values.
- **Outputs:** every current file renumbered to 3.3 (v3.2 in Old/).
  - **Semi-elasticities:** the ETS values typed for Egypt (`ETS_SEMI`) are replaced by sheet ETSSemi, looked up by the country code (Constants ets.semi).
  - **Keyed tables:** country column and `country|item` keys on the power tables, the energy balance and BaselineCO2; the lookups use `CtryCode`.
  - **One setting:** `COUNTRY` in the builder is the default of Settings C4.
  - **Scripts:** the check, the power reference and legacy_compare take the country from the build (income group, GAINS region, country name from the data); the extract scripts name their source country once (`SRC_ISO`).
  - **Documents:** Equations_v3_3.md uses named symbols for constants and the base year (no Egypt values); QuickStart has an "Another country" section.
  - **Check:** PASS; the regression against v3.2 shows a maximum difference of 0 on 6654 output codes.
- **Caveats:**
  - **Only Egypt has full data.** Several tables hold Egypt rows only: energy use, WEO GDP, CO2 and non-CO2 emission factors, the power tables and the energy balance. Another country gets #N/A until its rows are added. The legacy NoPropData file has no other country for these tables.
  - **BaselineCO2 is still model output stored as values,** now under the country key. For another country, rebuild with its code or paste its scenario-1 values. A live formula would be circular.
  - **Data and reference files are still tied to Egypt:** the legacy reference run (legacy_*.csv; its country is read from the codes) and the source files of the extract scripts (`SRC_ISO`). `update_prices_egypt_v3_3.py` is an Egypt data step by design.
  - **Not changed:**
    - The check's independent recomputation still writes a few unit constants and legacy defaults as literals: 41.868, 2039 and the OBR effectiveness 0.5.
    - The Inputs_prices formula `pccb` uses thresholds 0.25 and 0.5.

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.4: no literals in formulas; CO2 calibration switch off by default
- **Task (user):** "Fix the remaining literals too. If you can't do calibration in general please have a switch and turn it off as default."
- **Outputs:** every current file renumbered to 3.4 (v3.3 in Old/).
  - **New named constants** on sheet Constants:
    - pass-through buckets (PassLo, PassHi, PassMid, PassManual);
    - GJperkWh;
    - CapAvgShr (half the WACC in amortised capex);
    - TieBreak (dispatch tie breaker).
  - **The check reads every constant from the build:** `const_values()`, Settings C13-C15 and the ETS volatility table. Its recomputation no longer repeats 41.868, 2039, 0.5, 29.8, the GHG elasticities and so on.
  - **The literal scan now covers the formulas of every sheet,** not just Mitigation.
  - **CO2 calibration:** an input switch on Settings C27, default No (EFCalib = 1).
  - **Check:** PASS. Regression vs v3.3: max diff 0 on the 3,086 unaffected codes. CO2 and everything priced by it returns to uncalibrated (v3.1) levels.
- **Caveats:**
  - **Turning the calibration off changes results:** energy CO2 returns to the uncalibrated level (Egypt 2024: 297.2 instead of 285.3 Mt), and policy scenarios change slightly.
  - **Literals still allowed in formulas:** function codes, text lengths and the functional form of the storage cost (listed in the check).
  - **Unit conversions:** 1000 and 1e6 remain in the check's Python.
  - **Legacy defaults kept as data:** the ETS volatility table and the GHG elasticities. The GHG elasticities were backed out of the Egypt legacy run.
  - **Workflow:** the version check now allows files of the next version (work in progress on the transport model, v3.5).

## 2026-10-14 - CPAT-AI-Mitigation-MVP v3.5: engineer road transport model
- **Task (user):** code up the engineer transport model from the methodology note and legacy, starting with a plan; "Go with recommendations"; then "Go with suggestions and always try to match existing except where there are bugs". The user also asked for a document on the bugs and the decisions against legacy.
- **Inputs:**
  - Methodology note: `data/source/Transportation_methodology.docx`.
  - Legacy:
    - Mitigation key inputs 15 (rows 2015-2171) and section 5 (rows 4302-5378 and the policy copy);
    - sheets Transport1-3, Dashboard and Manual inputs.
  - Defined names had to be recovered from the xlsb binary, because the xlsx copy lost them (`tools/xlsb_*.py`).
- **Outputs:**
  - **Plan and survey:** `Transport_Plan_v3_5.md`, `Transport_Legacy_Survey_v3_5.md`.
  - **Data and reference:**
    - data extraction `extract_transport_v3_5.py` (all countries);
    - Python reference `transport_model_ref_v3_5.py`, which reproduces the cached legacy engineer run (both scenarios, 2022-2041, about 1,091 series) to 4e-14, with 17 bug switches.
  - **Workbook:**
    - Mitigation section 5b (855 rows, 80 LAMBDAs);
    - five data sheets;
    - MTInputs rows 418-479 (transport policies, all off);
    - switch `TrModel` (MTInputs row 340), default Elasticity.
  - **Documents:**
    - `Transport_vs_Legacy_v3_5.md` (bugs and decisions, generated from the reference);
    - `Transport_Method_v3_5.md`, `Transport_Workbook_Notes_v3_5.md`;
    - Equations section 4b;
    - register L25-L41, so LegacyBugFixes now lists 40 bugs;
    - a deck slide.
  - **Check:** PASS. Section 5b matches the reference to 4e-14. Engineer test scenarios (carbon tax, EV subsidy, distance tax, feebates, charging subsidy) match it to 5e-14 and pass the direction tests. Regression vs v3.4 is 0 on every shared code.
- **Caveats:**
  - **The engineer model is off by default.** All v3.5 results equal v3.4 until a scenario sets `TrModel` = Engineer. The legacy Egypt run also uses the elasticity approach, so there is no legacy benchmark for the engineer results with Egypt's real policy path, only the cached engineer run that legacy computes alongside.
  - **The fixes change the Egypt engineer baseline a lot:** road fuel in 2035 falls from 40,398 to 26,533 ktoe with legacy inputs. The two-sided ownership calibration (L27) does most of it.
  - **Range anxiety is legacy's stored per-country values,** solved in another vintage. The Egypt 2025 passenger EV share is 0.09% calculated against 0.15% actual. The goal seek is open.
  - **Large calibration factors for Egypt** (distance × 2.67, then gasoline × 1.23) point to weak Transport1 data.
  - **Kept as legacy:** freight distance in the TCO (floored at 50,000 km) and the data years of vehicle VAT, customs and import shares.
  - **The ownership decline limit (10% a year) is a placeholder.**
  - **Deviations in the inputs from the MVP** (listed in LegacyDiff):
    - 2-3 wheelers pay the gasoline price including new policies;
    - VAT on vehicles is VAT_WEO (Egypt 0.14, legacy run 0.1531).
  - **Phases 3-4 were built by a subagent;** I verified the check log and the regression.
  - **One check was narrowed:** the scenario-copy test now skips row `tr.pol`, a scenario-number flag.
  - **The externality sheet and mode shift are not built.**

## 2026-10-15 - CPAT-AI-Mitigation-MVP v3.6: consolidated tabs
- **Task (user):** consolidate tabs and move the reference group to the end:
  - the three Inputs tabs into one;
  - Settings, Constants and Mapping into one;
  - version log, ReadMe and LegacyDiff into a new tab "Version Log and Reference";
  - Variables, Lambdas and MacroCheck into one;
  - every macro button except Run all scenarios onto the reference tab.

  The user also asked about rebuild time and the Excel repair error.
- **Outputs:**
  - **Merge step:** `merge_tabs` in `build_v3_6.py` runs as the last step of the build. It:
    - stacks the blocks of each merged tab top to bottom, with three blank rows between them;
    - re-points every formula and defined name (openpyxl tokenizer; row offset per block);
    - writes the tab map `CPAT-AI-Mitigation-MVP-v3.6_tabs.json`.
  - **Scripts:** the check and the document scripts read the old blocks through `B.tab(wb, old_name)`.
  - **Tabs:**
    - **Inputs** = Inputs, Inputs_prices, Inputs_power.
    - **Settings** = Settings, Constants, Mapping.
    - **Version Log and Reference** = the version log (moved from Settings), ReadMe, LegacyDiff.
    - **Lambdas, Variables, Check** = Lambdas, Variables, MacroCheck.
  - **Order:** MAIN, INPUTS, DATA, then REF last.
  - **Macro:** constants `SH_CHECK` and `CHK_FIRST` are written by the build. MacroCheck is the last block, because the macro clears 300 rows below its report.
  - **Validation:** a quick build with and without the merge, recalculated in LibreOffice, gave identical values in all 564,458 cells.
- **Caveats:**
  - **Formulas now point at the merged tabs,** for example `Settings!$B$38` for a constant. Defined names keep the formulas readable as before.
  - **Texts in the workbook and the method notes still name the old sheets.** They now mean the table of that name; the ReadMe explains this.
  - **One LAMBDA body named a sheet:** POWERPRICE read Inputs_power directly. It now uses the defined names PwRpHist and PwRpYear, and the build asserts that no LAMBDA names a merged sheet.
  - **Build time:** the full build takes about 19 minutes. Most of it is the LibreOffice recalculation for the baseline CO2 and the batch emulation; the quick build takes 1 minute.
  - **The repair error is still unexplained.** The scan finds none of the known causes; the repair log text from Excel is needed.

## 2026-10-15 - Main prototype moved to the top of excel_ai/; duplicate files deleted
- **Task:** move the main prototype up a level, on every release; delete old files no longer needed.
- **Outputs:**
  - `CPAT-AI-Mitigation-MVP-v3.6.xlsm` moved from `excel_ai/working_version/` to `excel_ai/` (identical to the master in `mitigation/`).
  - New rule in `excel_ai/NORMS.md` section 5: every release puts the current workbook at the top of `excel_ai/` and removes the previous one there.
  - Deleted (all recoverable from git history): `working_version/Old/` (230 files, 77 MB, each byte-identical to a file in `mitigation/Old/` or `presentation/Old/`); `working_version/CPAT-AI-Mitigation-MVP-v2.6.2.xlsm` (superseded); in `standalone_initial_prototypes/`, the distribution pseudocode docx and standalone v0.4 workbook (identical to the copies in `distribution/`); `distribution/standalone/Old/CPAT_Distribution_Standalone_Egypt_v04b.xlsx` (identical to the current v0.4).
  - Path text updated in `QuickStart_v3_6.md` (both copies), the deck builder and the READMEs.
- **Caveats:**
  - The QuickStart path fix edits a shipped v3.6 note in place (text only, no method change).
  - Other `Old/` archives were kept: they are the version history the norms require. Duplicate PDFs in `_research/` were kept because notes may cite either path.

## 2026-10-15 - v3.6 variants without macros and without LAMBDAs; cause of the Excel repair error
- **Task (user):** versions of the v3.6 MVP without macros and without LAMBDAs, quickly. The user sent Excel's repair log ("Removed Records: Formula from /xl/worksheets/sheet2.xml").
- **Inputs:** `excel_ai/CPAT-AI-Mitigation-MVP-v3.6.xlsm`; Excel 365 via COM on the user's machine.
- **Outputs:**
  - `excel_ai/mitigation/make_variants_v3_6.py`. It edits the file package (zip) of the shipped workbook, so charts and styles stay as they are. It writes three files next to the source in `excel_ai/`:
    - `..._noMacros.xlsx`: VBA project removed; the buttons stay as plain shapes with no macro.
    - `..._noLambdas.xlsm`: the 7,206 cells that call a named LAMBDA get the body with the arguments substituted (recursively); the 194 LAMBDA names are removed; Excel recalculates on open. The longest expanded formula is 182 characters.
    - `..._noMacros_noLambdas.xlsx`: both.
  - **Cause of the repair error:** sheet2 is `Mitigation`. Excel 365 rejects cell formulas that call the named LAMBDAs **SCALE** and **SHARE** (found by bisection over the 193 LAMBDAs called there, opening each test file in Excel). With only those two expanded, the file opens with no repair and the other 191 LAMBDAs work.
  - **Check (Excel):** both no-LAMBDA files open without a repair log. The fully expanded file and the file with only SCALE/SHARE expanded (the other LAMBDAs live) give identical values after a full recalculation: 168,102 numbers on Mitigation, 3,290 on MTOutputs and 612 on ScenarioCompare, with 0 differences and 0 error values.
- **Caveats:**
  - **These are derived files, not a new version:** the in-workbook version log still says v3.6. The shipped v3.6 .xlsm itself still triggers the repair. The fix (rename SCALE and SHARE in the builder) is a TODO item for v3.7.
  - **Likely reason:** Excel reserves these names (new built-in function names). Not confirmed against Microsoft documentation.
  - **noMacros still has the macro sheet blocks** (MacroCheck report, button shapes); Run all scenarios is not available there, so StoredResults and ScenarioCompare keep what the build stored.
  - **LibreOffice is not installed on this machine,** so the variants were checked in Excel only, not with `check_quick_v3_6.py`.
  - **The Lambdas sheet block** still documents the LAMBDAs as text in the no-LAMBDA files.

## 2026-10-15 - Bug-fix and verification procedure for the main CPAT workbook (example bug L1)
- **Task:** designed a repeatable procedure and a paste-in VBA macro for fixing a bug in legacy CPAT and confirming nothing else broke, using legacy bug L1 (services electricity demand uses the industrial multiple from 2024) as the worked example. The macro locates rows by label, checks that CPAT still has the bug as registered, applies the fix as a drag (baseline) and a paste (policy), tests drag-ability, baseline-to-policy copy-paste, formula diff of the whole sheet, an independent recomputation, past years, error cells and totals, and writes a `FixLog` sheet. It never saves.
- **Inputs:** `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (read only; all runs on a scratch copy), `mitigation/LegacyBugFixes_v3_6.md` (L1), `excel_ai/NORMS.md` sections 3 and 3b.
- **Outputs:** `excel_ai/legacy/bugfix_procedure/BugFixProcedure.md`, `excel_ai/legacy/bugfix_procedure/FixL1_ServicesElectricity.bas`.
- **Caveats:**
  - **Tested only on the NoPropData file** (Excel 365, via COM on a copy); the macro's preflight is the check that the user's current CPAT still has the bug as registered. The user's newer CPAT was not available.
  - **T5 gives REVIEW on this file:** 72 cells in column M (2023) in the fiscal-multiplier tables (rows 14399-14592 and similar) change; their columns are lags, not years. Why the multipliers respond to electricity demand is not established.
  - **The fix itself is not applied to any shipped file.** Effect on the NoPropData copy: services electricity 2041 +30.8% (baseline), +16.1% (policy); 3,979 rows change. Legacy team still has to make the change (register L1).
  - No scenario-shift test is run by the macro (manual step 5 in the procedure).
  - During testing, all running Excel processes were force-closed once while a hung automation instance was being cleared; an unsaved session of the user's own Excel could have been affected. The legacy original itself was only ever opened read-only; the test runs used a copy in the session scratch folder. An Excel lock file `~$CPAT 1.0pre_456_NoPropData.xlsb` in `legacy/workbooks/` belongs to a copy opened by someone else at 16:03; it is untracked and not part of this task.
## 2026-10-15 - CPAT-AI-Mitigation-MVP v3.7: defaults as legacy; replication rule and lists
- **Task (user):**
  - apply the recommended decisions, matching legacy as much as possible;
  - put the bugs and issues first;
  - rule: never replicate a legacy bug, always replicate a legacy issue and track it;
  - two lists, `BUGS.md` and `ISSUES.md`, each with a bugs part and an issues part.
- **Inputs:**
  - v3.6 and its register;
  - `Sector_Equations_Survey_v3_6.md` (legacy fuel-use equations);
  - `legacy_comparison_v3_6.md`;
  - the MTInputs template (legacy ETS auctioned share, rows 90-92).
- **Outputs:**
  - **Version:** every current file renumbered to 3.7 (v3.6 in `Old/`).
  - **Model:**
    - last historical price year 2022 (`LAST_HIST`, Settings C10), as legacy;
    - ETS benchmarks 1.0 flat: nothing auctioned, the legacy default.
  - **Rule:** `excel_ai/NORMS.md` section 0 (bug vs issue, what to replicate, exceptions only by user decision), with pointers in the root `NORMS.md` (section 6, item 3), `AGENTS.md` and both READMEs.
  - **Lists:** `make_replication_lists_v3_7.py` writes `NotReplicated_v3_7.md` and `Replicated_v3_7.md`, copied to `excel_ai/BUGS.md` and `excel_ai/ISSUES.md`.
  - **Register:**
    - legacy bugs L42-L48 from the survey (now 47 bugs);
    - issues I19-I30;
    - `ISSUE_STATUS` (severity, status, next step), `ISSUE_LEGACY` (replicated / not replicated / MVP), `BUGS_REPLICATED` (L14), `LD_REPLICATED`.
  - **Bugs list:** `LegacyBugFixes_v3_7.md` has a column "In the MVP".
  - **Workbook:** LegacyDiff rows "ETS allocation" and "Fuel-use equation" updated (the shock named, effect large); version-log row 3.7.
  - **Check:** `check_v3_7.py` tests that every issue has a severity and a status.
  - **Documents:** legacy comparison re-run (shipped = prices to 2022); Formulas, Transport_vs_Legacy and the Bugs/Issues/Upgrades Word file regenerated.
  - **Copies:** `working_version/` and the workbook at the top of `excel_ai/` replaced.
  - **Quick check:** PASS. 8,622 shared codes; 2,488 change against v3.6, all through prices from 2023 and the ETS benchmarks.
  - **Legacy comparison:** fuel use is on average 17.3% from legacy over 2023-2030 (45.6% with 2024 prices); total GHGs 2040 are 647 Mt CO2e against 641 for legacy (v3.6: 724).
- **Caveats:**
  - **Some 2022 values change (212 codes).** Power fuel prices are a centred average over t-2 to t+2, so 2022 sees the 2023-2024 prices. 2022 power investment, the subsidy gap, revenue totals and the energy CH4 calibration factor (calibrated in 2024) follow.
  - **ETS goal seek, definition 5 (I30).** With all permits free the ETS works at half effectiveness. Prices reach about 134 $/t in 2030 and 230 $/t in 2035, and the goal seek oscillates between years: the worst gap is 6.2% after 20 iterations (stored results). Not fixed.
  - **Not yet replicated (queued in TODO):**
    - the 2023-2024 fuel-use shock (I22), the largest gap to legacy fuel use;
    - jet fuel (I19);
    - the MTInputs auctioned share (I21);
    - the income factor (I23);
    - the BiomassNormal switch (I24);
    - zero pollutant factors (I27);
    - existing carbon pricing in full (I7).
  - **Bug L14 is still replicated** (no effect for Egypt): queued to be fixed.
  - **Classification is a first pass.** The 45 LegacyDiff departures in `BUGS.md` 2b are not yet each reviewed; some may be issues to replicate.
  - **Two documents not rebuilt.** The Word documentation and the deck need the full check report, which runs only on request.
  - **pyxlsb installed** in the session to run the legacy comparison.

## 2026-10-15 - BUGSandISSUES: consolidated bugs and issues table with replication status (v3.7)
- **Task:** one workbook with a single table of every legacy bug, tracked issue and LegacyDiff departure, and a column saying whether the prototype replicates it.
- **Inputs:** `excel_ai/BUGS.md`, `excel_ai/ISSUES.md` (generated from `issues_register_v3_7.py`), `mitigation/LegacyBugFixes_v3_7.md`.
- **Outputs:** `mitigation/BUGSandISSUES_v3_7.xlsx` (sheets ReadMe and BUGSandISSUES, 123 rows), `mitigation/make_bugs_issues_sheet_v3_7.py`.
- **Caveats:**
  - Built by parsing the two generated Markdown lists, not from the register: the builder needs Python 3.12 (nested f-strings) and this machine has 3.10. The sheet is therefore only as current as those lists; regenerate them first at each release.
  - Upgrades (U) and bugs found and fixed in the prototype itself (M) are not in the sheet; they stay in the Word register.
  - Not added to the release routine yet (it is not run by `make_replication_lists`).

## 2026-10-15 - BUGSandISSUES as a Word document (v3.7)
- **Task:** the consolidated bugs-and-issues table with replication status, in Word form.
- **Inputs:** `mitigation/BUGSandISSUES_v3_7.xlsx` (see the entry above).
- **Outputs:** `mitigation/BUGSandISSUES_v3_7.docx` (landscape A4: rule, summary, then one table per kind; 123 rows), `mitigation/make_bugs_issues_docx_v3_7.py`.
- **Caveats:** same source and limits as the xlsx (built from the generated Markdown lists; no upgrades, no MVP-found bugs). Needs `python-docx`, which was installed on this machine for the task. Layout checked by exporting to PDF from Word; pages 1-3 viewed, not every page.

## 2026-10-15 - v3.7 rebuild with SCALE/SHARE renamed; Excel step in the quick check; build tools on the Windows machine
- **Task (user):** build v3.7 with the LAMBDAs SCALE and SHARE renamed and an Excel repair check; then tidy up.
- **Outputs:**
  - Builder: `SCALE` → `SCALEBY`, `SHARE` → `SHAREOF`; version-log row 3.7. `check_quick_v3_7.py` step 4 opens the built file in Excel (macros off, alerts off), fails if Excel cannot open it without a repair or writes a repair log, then fully recalculates with LAMBDAs live and fails on any error value. It is skipped where there is no Excel.
  - Build tools installed on the user's Windows machine: conda env `cpat312` (Python 3.12, openpyxl, pyxlsb, pywin32) and LibreOffice (winget).
  - Built `mitigation/CPAT-AI-Mitigation-MVP-v3.7.xlsm`. Quick check PASS (134 s): Excel opens it with no repair and 0 error values; 8,622 output codes vs v3.6, 0 change (max abs diff 9.9e-10, recalculation noise).
- **Caveats:**
  - **A second session built its own v3.7 in parallel** (commits 7f6609d, a457f62) and merged this rename into it. This build loaded the builder before that merge, so the committed v3.7 workbook lacks that session's v3.7 defaults. The rebuild (as v3.8) is the first TODO item.
  - **`excel_ai/CPAT-AI-Mitigation-MVP-v3.7.1.xlsm` is the user's Excel-repaired copy of the parallel session's v3.7** (which still had SCALE and SHARE, so it opened with errors). It opens cleanly, but the repair deleted the 258 Mitigation cells that called SCALE or SHARE: columns AE and BA, the LAMBDA year 2041. Every other formula is kept, and 2022-2040 are unaffected. Replace it with v3.8.
  - **The Excel check needs Windows with Excel:** a Linux or cloud build cannot confirm the fix.
  - **`soffice --version` hangs on its first run on Windows;** headless conversion works.
## 2026-10-15 - v3.7: merge of the local additions; LAMBDAs SCALE and SHARE renamed
- **Task:** merge the user's local commits (v3.6 variants, bug-fix procedure, cause of the Excel repair error) with v3.7.
- **Outputs:**
  - **Builder:** the LAMBDAs SCALE and SHARE renamed SCALEBY and SHAREOF on top of the v3.7 changes. The local commit had started from an earlier copy of the v3.7 files, so its renumbered files were not taken; its real changes were applied on top: the renames, the Excel open test in `check_quick_v3_7.py`, and the doc text.
  - **Version log:** 3.7 row names both changes.
  - **Register:** I29 (repair prompt) resolved.
  - **Rebuilt:** quick check PASS. Values equal to the first v3.7 build (max abs diff 0 on 8,622 codes).
  - **Regenerated:** Formulas, the Word register, the replication lists; workbook copied to the top of `excel_ai/`.
- **Caveats:**
  - **Repair fix not yet confirmed in Excel.** The Excel test is skipped on Linux (no Excel). Run `check_quick_v3_7.py` on Windows.
  - **The legacy workbook changed in the local commit 6a2e567.** `legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` went from 15,585,630 to 15,574,005 bytes, and `Backup of CPAT 1.0pre_456_NoPropData.xlk` (the original size) was added. The original should be read-only. Not touched here; the user decides whether to restore it.
  - **Extra workbooks at the top of `excel_ai/`.** The v3.6 variants sit there next to v3.7, against the one-workbook rule. Kept until v3.7 is confirmed in Excel.
  - **ETS goal seek of definition 5 unchanged** (I30): worst gap 6.2%.

## 2026-10-15 - Merge with the Windows v3.7 build (supersedes parts of the entry above)
- **Task:** merge the user's commits 15f1e5d-d1e51bd (Windows build of v3.7, repaired v3.7.1, BUGSandISSUES workbook and Word file, v3.8 TODO) with this session's rebuild.
- **Outputs:**
  - The user's workbooks and file moves kept:
    - `mitigation/CPAT-AI-Mitigation-MVP-v3.7.xlsm` is the Windows build (pre-merge builder, Excel-checked);
    - `excel_ai/CPAT-AI-Mitigation-MVP-v3.7.1.xlsm` stays at the top;
    - v3.6 variants and the earlier v3.7 copy are in `excel_ai/old/`.
  - This session's Linux rebuild from the merged builder (v3.7 defaults + SCALEBY/SHAREOF) was not kept, so that no two different files carry v3.7. It is in commit de6a268. Its result: quick check PASS; values equal to the first v3.7 build with the defaults.
  - TODO: the v3.8 item notes that the merged builder is verified on Linux.
- **Caveats:**
  - **The entry above says the rebuilt workbook was copied to the top of `excel_ai/`;** that copy was replaced by the user's layout in this merge.
  - **v3.8 (bump + build + Excel step on Windows) is still to do;** the TODO puts it first.

## 2026-10-15 - CPAT-AI-Mitigation-MVP v3.8: rebuild from the merged builder
- **Task (user):** build v3.8 in the cloud: the TODO item "Rebuild as v3.8".
- **Inputs:** the merged `build_v3_7.py`, which has the v3.7 defaults (prices to 2022, ETS benchmarks 1.0) and the LAMBDAs renamed SCALEBY and SHAREOF.
- **Outputs:**
  - **Version:** every current file renumbered to 3.8 (v3.7 in `Old/`); version-log row 3.8.
  - **Workbook:** `CPAT-AI-Mitigation-MVP-v3.8.xlsm` built (26 min).
  - **Quick check:** PASS. 8,622 codes; 2,488 change against the Windows v3.7 build, all through the defaults that build lacked.
  - **Values:** equal to the Linux v3.7 build with the defaults (max abs diff 0).
  - **Regenerated:** LegacyBugFixes, the replication lists, Transport_vs_Legacy, Formulas, the Word register, BUGSandISSUES (xlsx and docx; python-docx installed for it).
  - **Copies:** v3.8 at the top of `excel_ai/` (v3.7.1 moved to `excel_ai/old/`); `working_version/` replaced.
- **Caveats:**
  - **The Excel step of the quick check was skipped (no Excel in the cloud).** Run `check_quick_v3_8.py` on Windows to confirm that Excel opens the file without a repair.
  - **ETS goal seek, definition 5 (I30):** still 6.2% from the cap.
  - **Two documents not rebuilt:** the Word documentation and the deck need the full check (on request).

## 2026-10-15 - Assessment of the legacy mitigation results rows; issue I31
- **Task (user):**
  - add the price-mixing problem as a major issue;
  - assess every results row of legacy Mitigation (in the scenario blocks and in the results area), organised, with a strategy to fix them.
- **Inputs:** legacy `CPAT 1.0pre_456_NoPropData.xlsb` (cached values, baseline and carbon tax, read with pyxlsb); `Downstream_Survey_v3_8.md`, `Sector_Equations_Survey_v3_8.md`, the method notes and the register.
- **Outputs:**
  - Register: I31 (major, not replicated): legacy average prices are unit values reported as price changes. TODO item for v3.9 (price indices).
  - `mitigation/Results_Assessment_v3_8.md`:
    - cross-cutting problems S1-S8;
    - a health scan of every results row (error values, zero rows; scenario rows zero in both runs);
    - a section-by-section table (what each holds, legacy quality, MVP status, strategy code);
    - fix options and a recommended order (v3.9-v3.16).
- **Caveats:**
  - **The scan reads cached values only.** A row with no error value can still be wrong. Formulas were not re-read for this note; the bug lists come from the earlier surveys.
  - **Block D was scanned only for sections 11-17,** to separate policy rows from rows that are always zero.
  - **The strategy is a proposal.** Option (1 fix legacy, 2 rebuild in the MVP, 3 both), increment size and dropping the cross-check tests are the user's decisions.

## 2026-10-15 - Results layout rules (NORMS 3c) and the placement plan for legacy's post-processing
- **Task (user):**
  - write the four agreed rules into the norms;
  - put the price indices in the price section as a memo after the price build-up, with the decomposition;
  - plan how legacy's post-processing results slot into the scenario calculations, keeping the section numbering and mostly at the end, in coherent sections.
- **Outputs:**
  - `excel_ai/NORMS.md` section 3c, with five rules:
    - results belong to the scenario, and output sheets only select and compare;
    - differences live in the model only where the model uses them (`.ref`, `.chg`, `.pct`);
    - the definitions of differences (% only for strictly positive quantities; price changes as indices; ratios from summed levels; periods from summed levels; scenario 1 as reference);
    - large modules on own sheets with the same column-group geometry;
    - section numbering.
  - `Results_Assessment_v3_8.md` section 6:
    - memo blocks in sections 2, 3, 13, 16;
    - new sections 17 Prices and carbon pricing, 18 Fiscal results, 19 Energy and emissions results, 20 Welfare and externalities, 21 External balance and targets, 22 Hand-offs;
    - output-sheet rows;
    - version order v3.9-v3.15.
  - I31 next step and TODO updated (section 2 memo on after-tax prices incl. new policies); TODO item for the plan.
- **Caveats:**
  - **The MVP's sections 11-16 already differ from legacy's numbers** (e.g. MVP 12 Revenues = legacy 16). They are kept, and new sections 17+ have no legacy number.
  - **The section 2 memo reads rows further down** (after-tax prices in sections 5-8, fuel use in section 11). That is allowed: it is not circular, but it is not in reading order.
  - **The plan is not built.** v3.9 starts with the section 2 memo.

## 2026-10-15 - Results placement plan consolidated (NORMS 3c rules 5-6; plan section 6)
- **Task (user):** write the consolidated plan into the plan and the norms:
  - revenue consolidated in section 12;
  - energy and emissions reports in 11, 13, 14;
  - external balance in section 16;
  - new sections 17-18 only;
  - modules reading Mitigation rows directly, with section 15 and the Distribution inputs shaped for the modules.
- **Outputs:**
  - `excel_ai/NORMS.md` 3c:
    - rule 5 (section layout: existing sections grow by memos and lettered sub-blocks; new sections 17 Carbon pricing and 18 Welfare and externalities only; dependency order);
    - new rule 6 (modules read Mitigation directly; no hand-off block; module-only transformations on the module sheet).
  - `Results_Assessment_v3_8.md` section 6 rewritten:
    - all sections, legacy and MVP, with the additions per section;
    - header rows (GDP level moved up; exchange rate, nominal GDP);
    - module sheets and what each reads;
    - output sheets;
    - order v3.9-v3.16.
  - TODO item updated.
- **Caveats:**
  - **The plan is not built.**
  - **One cross-sheet read back into `Mitigation`:** section 18 will read the module sheets' unit damages. It is not circular (the modules do not read section 18).
  - **Section 16 is renamed only when 16b is built** ("GDP effects and external balance").

## 2026-10-15 - Norms for names, copy-paste and overnight runs; plan v3.9-v3.17 with questions
- **Task (user):**
  - put the formatting upgrade first;
  - list every question up to v3.17 with recommendations;
  - set a token-saving, no-hang procedure with quick checks and half-way builds;
  - write lists of names, keywords and cell references for LAMBDA safety, and the copy-paste rules, into the norms.
- **Outputs:**
  - `excel_ai/NORMS.md`:
    - 3d names, keywords and cell references: reserved names, cell-like names, one namespace, the form of new names, no sheet names in LAMBDA bodies, `_xlfn.`/`_xlws.`/`_xlpm.`, formula keywords;
    - 3e copy-paste ability (across years, down a block, across scenarios);
    - 3f overnight runs: per-version steps with half-way quick builds, timeouts, one LibreOffice job at a time, full check at checkpoints, failed steps reverted, unanswered questions defaulted and recorded.
  - `mitigation/excel_reserved_names.txt` (Excel functions, reserved defined names, SCALE and SHARE).
  - `mitigation/Plan_v3_9_to_v3_17.md`: order, procedure, Q1-Q50 with recommendations.
  - TODO item.
- **Caveats:**
  - **Version numbers shift by one.** v3.8 is released, so formatting is v3.9 and the chain ends at v3.17.
  - **Seven LAMBDA parameters equal Excel function names** (`base`, `growth`, `price`, `rate`, `share`, `value`, `year`). Excel accepted them in the v3.7 Windows test; they are grandfathered, and new ones are not allowed.
  - **The reserved-name list is from knowledge of Excel 365 (2026),** not read from Microsoft. SCALE and SHARE are not listed functions, so the list grows whenever Excel rejects a name.
  - **Nothing is built yet;** the run waits for the user's answers.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.9: style guide (overnight run, step 1)
- **Task:** plan v3.9, Q1-Q10: formatting to NORMS 2.
- **Outputs:**
  - **Builder:**
    - two blank rows before each section band and one after; one between blocks; two before a sub-section;
    - sub-section headings on their own row in column B, bold underlined;
    - header (label) rows bold with a thin bottom border;
    - top border on each price block; thin borders on parameter cells;
    - Arial 10;
    - legacy band (number in A, title in B 12 pt bold) and title fill `00AE49`;
    - codes italic, notes italic grey, helper row grey;
    - column B no longer rolls up.
  - **Names and length:** defined name `PwTie` keeps the second investment round within 100 characters after the rows moved.
  - **Checks:** `check_quick` tests reserved names (NORMS 3d) and the style (bands, headings, header rows, font) and reads a quick build with `QUICK=1`. NORMS 2.1 title fill and 2.4 visible column B; NORMS 3f `pkill -x`.
  - **Quick check on the full build:** PASS, 0 change on all 8,622 codes (layout only). The workbook is at the top of `excel_ai/`; `working_version/` is refreshed.
- **Caveats:**
  - **Row numbers moved throughout Mitigation;** codes are unchanged.
  - **Parameter boxes are per-cell thin borders,** not an outline around each group.
  - **Bands and fonts follow the new style on the output sheets, but their layout is unchanged.**

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.10: average prices and price indices (overnight run, step 2)
- **Task:** plan v3.10, Q11-Q16; issue I31.
- **Outputs:** memo at the end of section 2, with one block for each of the 8 fuels, electricity and all energy:
  - spending and fuel use;
  - average price (unit value, as legacy F5b);
  - spending at scenario 1 quantities and the Laspeyres price index against scenario 1;
  - spending at base-year quantities and the time index;
  - mix effect = unit-value ratio / price index.

  Also:
  - helper row 10: position of scenario 1's column of the year;
  - defined names `SecVar`, `SecFuel` and `PwCG`; the latter keeps the power `gmin` row within 100 characters after the rows moved;
  - LAMBDAs FUELSPEND, FUELQTY, SPENDSUM, ALLSPEND, MIXEFFECT;
  - 11 MTOutputs rows;
  - PriceProjection method section 7;
  - full check: `check_results_memos` (independent Python recomputation, every scenario group).
- **Check:** quick check PASS; 160 new codes; 0 change on the 8,622 v3.9 codes. The memo equals a Python recomputation to 8e-15.
- **Results:** carbon tax 2030 against the baseline (Laspeyres):
  - coal +26%, gas +21%, gasoline +8%, diesel +13%, electricity +13%, all energy +14%;
  - mix effect about 1 per fuel and 1.013 for all energy.

  Legacy's unit-value "price change" for gas (+71%) also differs through legacy's baseline and bugs, not only the mix.
- **Caveats:**
  - **Sums cover the 16 subsectors (final use).** Fuels burnt for power generation are not in the fuel averages. Legacy weights coal and gas over power too: recorded under I31.
  - **The all-energy unit value is in USD m per ktoe** (only its ratios are used).
  - **The road engineer model (when switched on)** feeds road fuel use into `ener`, so the weights follow it.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.11: fuel-use shock 2023-2024 and jet fuel (overnight run, step 3)
- **Task:** plan v3.11, Q17-Q20; issues I19 and I22 (now replicated), new I32 and I33.
- **Outputs:**
  - **Energy demand shock as legacy** (legacy row 483: Egypt -20.81% in 2023, +9.24% in 2024). It applies to fuel use and to power demand, through one switch (Settings C19, default 1 = on, as legacy), via header row 11. This reverses the 2026-10-11 acceptance of the 2023 power-demand jump.
  - **Jet fuel `jfu` as a fuel of its own, used in domestic aviation only** (707 ktoe in 2022, legacy Data_Energy):
    - its price is the kerosene price (`PRICE_FUEL_OF`, Mapping column I);
    - CO2 and pollutant factors are the jet factors.
- **Check:**
  - full build PASS;
  - 534 new codes and 1,906 changed values against v3.10 (intended: every result moves).
- **Results:** gap to the legacy cached baseline (`legacy_comparison_v3_11.md`, prices to 2022):

  | Measure | v3.10 | v3.11 |
  |---|---|---|
  | Mean absolute % difference, subsector by fuel 2023-2030 | 17.3% | 9.9% |
  | Total fuel use 2030 | +8.0% | -6.7% |

  Transport fuel use in 2030 is now 19,830 ktoe (legacy 20,541).
- **Caveats:**
  - **ETS goal seek of definition 5 stops at a worst gap of 0.040** after 20 iterations (I30).
  - **CO2 calibration stays off and in 2024** (user rule v3.4), while legacy uses Yes* and 2021. This is why legacy CO2 in 2022 is about 7% below the MVP (I32, accepted exception).
  - **The data step (`extract_data`) rewrites every data file and loses the corrected Egypt prices** (I33). Only its jet-fuel rows were kept.
  - **`legacy_compare` counts the jet-fuel rows that legacy lacks** (outside aviation) as zero.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.12: section 15 as the air-pollution input table (overnight run, step 4)
- **Task:** plan v3.12, Q21-Q22; new issues I34 and I35 (both replicated).
- **Outputs:** the section 15 hand-off now has the layout of the legacy input table (rows 15859-15961):
  - one block per module sector, plus all sectors;
  - the ten pollutants in legacy order;
  - new CH4 rows `aps.<sec>.ch4`;
  - a total `aps.all.<p>` for every pollutant.

  Units stay kt (legacy: tonnes).
- **Check:**
  - full build, then quick check: PASS;
  - 30 new codes, 0 change;
  - totals equal the section 15 pollutant totals;
  - CH4 total = combustion + fuel supply + agriculture and waste methane;
  - every non-CH4 value matches the legacy input table, e.g. gas plants' NOx is 104,502 t in both.

  The Python recomputation in `check_v3_12.py` is extended; it runs in the full check after v3.13.
- **Decision to confirm (Q21, NORMS 3f).** The plan's recommendation was combustion CH4 only. Legacy's table holds methane sources instead:
  - extraction methane under "other";
  - agriculture and waste methane under "food & forestry";
  - zero combustion CH4.

  Taken: the legacy allocation plus combustion CH4, with all fossil fuel supply methane under "other". CH4 is 2,117 kt in 2022 against legacy's 1,936 kt (I34).
- **Caveats:**
  - **Fuels with no GAINS factor emit nothing, in legacy too (I35, major, open).** Examples are residential LPG, mining diesel, food & forestry diesel and other manufacturing LPG. Food & forestry shows about 1 t of NOx in both models. This is not a units bug, as first suspected.
  - **Quick builds skip the baseline-CO2 data refresh,** so `bco2` codes differ in quick mode only.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.13: header GDP rows and 12d fiscal reports; full check (overnight run, step 5)
- **Task:** plan v3.13, Q23-Q29; first full check since v3.8; bug M12.
- **Outputs:**
  - **Header rows 12-14:**
    - `gdp.usd` moved up from section 16, code unchanged;
    - `gdp.lcu`, real GDP in local currency (legacy row 464, through `extract_gdp`);
    - `xr`, the exchange rate implied by real GDP (14.34 EGP per USD).
  - **12d fiscal reports:**
    - revenue by fuel net of subsidies: final use, electricity, generation fuels;
    - a check row, `rfu.chk` = 0;
    - base erosion `rbe`;
    - six % of GDP rows via LAMBDA GDPSHARE;
    - 5 MTOutputs rows.
  - Method note `ResultsSections_Method_v3_13.md`.
- **Check:**
  - quick check PASS; 48 new codes, 0 change;
  - 12d equals a Python recomputation (920 cells).
- **Full check.** The script had drifted since v3.8 and is now updated:
  - jet fuel and the fuel-use shock in the Python recomputation;
  - column B outline;
  - the LAMBDA row list;
  - band and bold tests for the v3.9 style;
  - regression now against the previous version.

  The independent recomputation matches every scenario (66,180 cells, 1e-13).
- **Bug M12 (MVP, since v3.6):** the formula texts on sheet Lambdas still named the merged sheets `Inputs_power` / `Inputs_prices`, so copied in they gave `#REF!`. `merge_tabs` now re-points them.
- **Remaining full-check FAILs:** only the ETS goal seek (I30, known and open): test scenario 3 has a gap of 0.038 and stored scenario 5 a gap of 0.040.
- **Decisions to confirm (NORMS 3f):**
  - no nominal GDP: the legacy file has no NGDP or NGDPD, so it waits for WEO data;
  - producer subsidies and price-control losses are not built (no data / no legacy revenue row);
  - fuel expenditures stay in the section 2 memo.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.14: sub-blocks 11b, 13b, 14b (overnight run, step 6)
- **Task:** plan v3.14, Q30-Q33.
- **Outputs** (method in `ResultsSections_Method_v3_14.md` sections 3-5):
  - **11b:** energy change against scenario 1 by fuel, sector group, power and total, plus % change.
  - **13b:**
    - CO2 change by fuel and sector group;
    - grid emission intensity, tCO2/MWh: 0.41 in 2022 (legacy 0.38);
    - Kaya identity as legacy F14 (baseline GDP, total CO2, total fuel use). Its levels and its indices against the base year multiply exactly to the CO2 index.
  - **14b:** GHG change by inventory category and gas; energy GHGs including the forcing of the local pollutants.
  - New LAMBDA SAFEDIV.
  - 9 MTOutputs rows.
- **Check:**
  - full build PASS; 132 new codes, 0 change;
  - the Python recomputation of every new row in every scenario group matches to 7e-12.
- **Found during the step:**
  - **LAMBDA name clash, fixed before release.** The new ratio LAMBDA was first called INTENSITY, a name the road model already uses, and the road version silently won. The build now asserts that no LAMBDA name is defined twice.
  - **Missing parentheses in the plain grid-intensity formula, fixed.**
- **Decisions (to confirm):**
  - no energy-balance matrix rows (Q30);
  - Kaya energy = total fuel use including power fuels (Q31); legacy's primary-energy row is broken;
  - broad sectors = inventory categories, so no allocation data (Q32);
  - NDC later (Q33).
- **Caveats:** Kaya population is the MVP's UN series (111.7 mn in 2022 against legacy's 103.6 mn; bug L20 fixed), so GDP per capita is lower than in legacy.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.15: section 17 Carbon pricing (overnight run, step 7)
- **Task:** plan v3.15, Q34-Q36; new issue I36 (replicated).
- **Outputs:** new section 17 (method in `ResultsSections_Method_v3_15.md` section 6). It has:
  - the implicit carbon price by fuel and economy-wide: revenue net of subsidies per tCO2, legacy F5d;
  - the effective carbon rate (legacy row 16662) and the effective carbon tax (row 16137);
  - CO2 covered by the carbon tax in each of the 17 coverage sectors;
  - coverage shares by sector group, for the tax and the ETS (legacy rows 16150-16157).

  Also 4 MTOutputs rows.
- **Check:**
  - full build PASS; 72 new codes, 0 change;
  - the Python recomputation matches (1,440 cells, 6e-15).
- **Results (Egypt):**
  - implicit carbon price of fossil fuels in 2022: -179 USD/tCO2 (subsidies);
  - effective carbon rate -207 (legacy -122: different price data);
  - carbon-tax coverage in the carbon tax scenario, 2030: 99.8% (legacy 98.8%).
- **Decisions (to confirm):**
  - biomass is left out of the implicit price (Q34);
  - the effective carbon rate follows legacy, VAT and subsidies included (Q35, I36);
  - coverage is computed exactly from the fuel switches and sector rates (Q36).

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.16: 16b External balance (overnight run, step 8)
- **Task:** plan v3.16, Q37-Q39; legacy bugs L49 and L50 (not replicated).
- **Outputs** (method in `ResultsSections_Method_v3_16.md` section 7):
  - **Data:** energy trade balance and share traded from legacy rows 741-743, through `extract_gdp` into sheet WEO.
  - **Change in net energy imports by fossil fuel and group:** change in use (11b) x supply price (section 2) x import share.
  - **Trade balance:** baseline, scenario and % of GDP.
  - **Renamed:** section 16 is now "GDP effects and external balance".
  - 3 MTOutputs rows.
- **Check:**
  - full build PASS; 38 new codes, 0 change;
  - Python recomputation 760 cells, 5e-15.
- **Results (Egypt):**
  - energy trade balance 2022: -6.7 bn USD;
  - carbon tax 20 USD, 2030: net energy imports -1.2 bn USD.
- **Legacy bugs found and not replicated:**
  - **L49:** oil without the share traded, so the oil effect is about twice too large.
  - **L50:** the current account is `#NAME?`, the policy rows lag one column (2022 shows the 2021 balance), and the sign looks reversed.
- **Decisions (to confirm):**
  - supply prices value the trade (coal and gas: industry price);
  - no current-account level until WEO BCA data are added (Q38).

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.17: section 18 Welfare and externalities, climate part; full check; documentation and deck (overnight run, step 9, last)
- **Task:** plan v3.17, Q40-Q45.
- **Outputs:** new section 18 (method in `ResultsSections_Method_v3_17.md` section 8):
  - SCC options and selection as legacy. Ricke national and global values come from the new data sheet `SCC` (680 rows); the manual path from legacy row 17683; settings in Settings rows 32-42.
  - Climate damages (SCC x GHG excl. LULUCF) and damages avoided, national and global.
  - Tax wedges and efficiency costs of energy by fuel (trapezoid, LAMBDA TRAPEZOID).
  - Efficiency costs of the methane fee: area under the abatement curves (MFEEPRICE, MFEECOST). Tested with a fee of 50 USD/tCO2e.
  - Welfare summary.
  - 6 MTOutputs rows.
- **Check:**
  - full build PASS; 102 new codes, 0 change;
  - section 18 equals the Python recomputation (2,040 cells, 3e-13).
  - **Full check:** every section passes except three items:
    - ETS goal seek, test scenario 3: gap 0.038 (I30, known);
    - stored scenario 5: gap 0.040 (I30, known);
    - the D:G label test on the 16b rows: the share traded had no label. Fixed and rebuilt; the layout test then passed (`check_report_v3.17.md` predates the fix).
- **Found during the step:**
  - **The build's sheet-order list silently dropped the new SCC sheet.** The build now asserts that the list covers every sheet.
  - **A section 18 reference counted the helper-row position from the wrong column.** It gave `#REF!` and was caught by the quick check.
- **Results (Egypt, carbon tax 20 USD, 2031):**
  - climate damages avoided 1.9 bn USD (SCC 78);
  - efficiency gain 1.3 bn USD (subsidised use falls);
  - national welfare +3.2 bn USD (0.4% of GDP).
- **Decisions (to confirm):**
  - SCC defaults as legacy (target-consistent 75 USD in 2030, 4% a year);
  - the efficiency costs use the tax wedge = revenue net of subsidies per unit, power fuels included;
  - co-benefits come with the modules (Q42).
- **Documentation:**
  - the Word documentation now includes the results-sections note;
  - the deck gains a slide on the results sections and new next steps.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v3.18: Kaya on total primary energy supply (user request)
- **Task:** the user asked for the Kaya identity on total primary energy supply: power inputs plus primary electricity (renewables and nuclear). Legacy does the same (row 18880).
- **Outputs:**
  - new row `kaya.tpes` = fuel use (section 11, power fuels included) + `pe` of nuclear, wind, solar, hydro and other renewables (section 3);
  - energy intensity and carbon intensity now use it.
- **Check:**
  - Egypt 2022 TPES 89,470.6 ktoe and energy intensity 163.5747 equal legacy exactly;
  - the Kaya identity holds (`kidx.chk` = CO2 index);
  - only the Kaya rows change.
- **Correction:** the v3.14 note said legacy's primary-energy row was broken. It is not: the -97% bug is in legacy's separate "simplified Kaya" row 18931.
- **Caveat (I37, replicated):** the legacy efficiencies of wind (1.004), solar (1.026) and hydro (0.937) are not exactly 1 (physical energy content convention), about 0.1% of TPES.
- **Process:** the version bump stopped on a file that is not UTF-8. It was completed in place, and `bumpv.py` now passes such bytes through.

## 2026-10-16 - Legacy CPAT bug-fix plans, cell by cell (`legacy_bugfix_plans/`)
- **Task (user):** manual fix plans for legacy CPAT with, for each bug, the cell and the exact new formula, legacy as reference: engineer power model, engineer road model, all other mitigation bugs; Word documents; kept in their own folder and added to main; then this log entry and a tidy-up of main.
- **Inputs:** `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (sheet Mitigation; converted with LibreOffice, defined names and cached values read from the .xlsb); register v3.8 (bug IDs L1-L48); `power_model_ref_v3_8.py` and `transport_model_ref_v3_8.py` (fix switches and effects); `Transport_Legacy_Survey_v3_8.md`, `Sector_Equations_Survey_v3_8.md`.
- **Outputs:** `legacy_bugfix_plans/`: three Word plans and PDFs (power engineer L1-L12, 20 cells; road engineer L25-L41, 51 cells; other mitigation L13-L24, L42-L48, N1, N2, 79 cells), the fixes as JSON, the legacy defined-names map, generator scripts, README. Tidy-up: README repo map lists the folder; `excel_ai/plans/TODO.md` legacy bug item updated (49 bugs as in v3.18, link to the plans, follow-ups); folder README points to the v3.18 register.
- **Caveats:**
  - **New formulas are built by exact text substitution of the legacy formula and bracket-checked; nothing was recalculated in Excel.** Effects come from the Python legacy models (power, road), cached values and the register.
  - **L15 and L18 do not reproduce in this file;** L22 needs inserted rows; L43's policy rows are edited by hand (the policy block is +6,331 rows up to about row 6070, +6,317 after, while those rows point to drivers at +6,331).
  - **N1 and N2 are new and not in the register;** confirm before applying (TODO follow-up).
  - **The road-model fixes change only the engineer run** (the legacy Egypt run uses TrModel = Elasticity).
  - **Made from the legacy file before commit d82efd0 restored the original;** the Mitigation formulas (A:AF, rows 1-15000) of the restored original are identical, including every cell in the plans.
  - **L49 and L50 (balance of payments, v3.16):** covered since 2026-10-16 (v4.0 release entry below).
  - **Preamble paths:** fixed on 2026-10-16 (v4.0 release entry below), when the append-only rule was lifted.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v4.0: release renumbering, repository tidy-up, L49-L50 fix plans
- **Task (user):** release v3.18 as 4.0 (all files incl. workbook, Word documents and decks; no rebuild); lift the append-only rule of this log and tidy it; check the overarching files and unarchived old versions; clarify the root and Excel READMEs; add L49 and L50 to the legacy bug-fix plans; push to main.
- **Inputs:** v3.18 files of `excel_ai/mitigation/` (incl. `presentation/`), `excel_ai/working_version/`, the top of `excel_ai/`; legacy workbook rows 735-745 and 18165-18225 for L49-L50.
- **Outputs:**
  - **v4.0:** every current v3.18 file of `mitigation/` and `presentation/` copied as v4.0, the v3.18 masters in `Old/`; `working_version/` renamed to v4.0; top of `excel_ai/`: `CPAT-AI-Mitigation-MVP-v4.0.xlsm` and `CPAT-AI-Mitigation-MVP_Overview_v4.0.pptx` (v1.0 deck to `excel_ai/old/`). Only file names, title labels ("CPAT-AI-Mitigation-MVP v4.0"), `VERSION = '4.0'` and file references changed; history notes ("added in v3.18") kept. `build_v4_0.py` has a version-log row 4.0.
  - **Archived:** `Plan_v3_9_to_v3_17.md` and the deck's v3.10-v3.17 image and data files (`presentation/img/Old/`).
  - **Append-only lifted:** `NORMS.md` section 6, `AGENTS.md`, `README.md`, `excel_ai/NORMS.md`, `excel_ai/README.md`; earlier entries may now be corrected, not deleted. This log's preamble links fixed (Egypt documents in git history, distribution docs in `excel_ai/distribution/`).
  - **READMEs:** root: repository name, current release, a row for fixing legacy CPAT, `CLAUDE.md`, `SyncRepo.bat` (at the root, not in `excel_ai/`), `bugfix_procedure/`; Excel: release, deck names, `bugfix_procedure/`, `old/` contents.
  - **Fix plans:** `legacy_bugfix_plans/Legacy_CPAT_BugFix_OtherMitigation.docx` (and PDF, JSON) now has L49 (row 18181: oil x share traded $H742) and L50 (WEO codes `<iso>.bca.a`, `<iso>.bca_ngdpd.a`; `WEO_upd` instead of the empty name `WEO`; no column lag; rows 18215-18219 relabelled as trade balance). All register bugs L1-L50 are covered; script `tools/gen_bop.py`.
- **Caveats:**
  - **The v4.0 workbook is the v3.18 file renamed (not rebuilt):** its Settings version log, title cell and `_tabs.json` content still say 3.18 until the next build with `build_v4_0.py`. The Word documents and decks were relabelled by text replacement in their XML; a few historical "v3.18" mentions remain on purpose.
  - **The branch `claude/legacy-bugfix-plan` could not be deleted from this session** (the git service refuses branch deletion); it is fully merged and can be deleted on GitHub.
  - **L50's current account** needs WEO data to the end of the horizon; years beyond the WEO data return #N/A.

## 2026-10-16 - CPAT-AI-Mitigation-MVP v4.1: rolled-up sections, price blocks with new policies, copy-paste across scenarios (user request)
- **Task (user):** every section rolled up by default to its summary row, reordering so the summary comes last (12d fiscal reports before total revenue, 13b before total CO2, likewise 11b, 14b, 16b); a second summary row only where useful (the change against scenario 1); summary rows for Carbon pricing and Welfare; section 0 numbered and rolled up below the frozen rows; notes not italic; one spacer row instead of two; price blocks: settings (four rows, incl. the subsidy per unit) in italic, full retail price incl. new taxes and subsidies in bold, the existing build-up ending with the price before new policies, then the new taxes and subsidies weighted by subsector, total new policy last; check copy-pasteability between scenarios (also pasting a third scenario from column BD), differences always against scenario 1; write the norms.
- **Inputs:** v4.0 builder and checks (`mitigation/Old/*_v4_0.*`).
- **Outputs:**
  - `mitigation/build_v4_1.py`, `check_quick_v4_1.py`, `check_v4_1.py` and the v4.1 file set (v4.0 masters in `Old/`); workbook `CPAT-AI-Mitigation-MVP-v4.1.xlsm` (also at the top of `excel_ai/`); version-log row 4.1.
  - **Layout:** section 0 (rows 1-5 frozen: years, title, band 0, scenario name, scenario number; rows 6-13 roll up; GDP growth in row 14 is its summary); every section's group ends with its summary row; second summary rows: `echg.all` (11), `rtot.chg` (12), `co2.chg` (13), `ghg.chg` (14); new summary rows `rpe` (2, average retail energy price, all energy), `ecr` (17, effective carbon rate, moved), `wel.usd` (18, moved); sub-blocks 11b, 12d, 13b, 14b, 16b inside their sections before the notes and summary; one blank row before every band and sub-heading; notes upright dark grey.
  - **Price blocks (section 2):** new rows `rpn` (full retail price), `pnq` (fuel use of the subsectors priced by the block), `pctx`, `pets`, `pntx`, `pxcd` (new carbon tax, ETS, excise, change in existing carbon pricing, weighted), `pvatn` (VAT on new policies and floor, residual), `pnce` (total new policy = `rpn - rpb`); new LAMBDAs `BLOCKQTY`, `BLOCKAVG`; new name `SecPar` (column D of sections 5-8). `rpb` relabelled "before new taxes and subsidies".
  - **Copy-paste:** the scenario number is a formula (`COUNTIF` of the code-column headers from `$K$1`), the code-column header is the same in every group; groups 1 and 2 are identical in relative form (quick check, new test); differences against scenario 1 were already copy-pasteable (`INDEX($K x:<col> x, <col>$10)`).
  - **Norms:** `excel_ai/NORMS.md` 2.2 (notes), 2.4 (one blank row), new 2.5 (sections, roll-up, summary rows), 2.6 (price blocks), 3e (full copy-pastability, differences). Method notes: `PriceProjection_Method_v4_1.md`, `ResultsSections_Method_v4_1.md`. Quick check: new tests (one blank row, rolled-up view = bands and summaries, notes not italic, section 0, group copy test). Full check: Python recomputation of the new price-block rows (`price_blocks`).
  - Test script `mitigation/check_paste_v4_1.py` (on request).
- **Check (full build):**
  - quick check PASS: no formula over 100 characters, no literals, no error cells after recalculation, one blank row before every band and sub-heading, rolled-up view = bands and summary rows only, groups 1 and 2 identical in relative form;
  - **0 of 9,740 shared output codes change against v4.0** (max abs diff 1e-11); 194 new codes (the new price-block rows and summary rows);
  - **copy-paste:** group 2 pasted as groups 3 and 4 (code columns BC and BY, years from BD and BZ) with no edit: 0 error cells; group 4 numbers itself 4 and runs MTInputs definition 4 (Package A), and equals the stored batch result of definition 4 on all 2,090 stored values (difference 0); its difference rows equal its level minus scenario 1's (5e-10). The full check (`check_v4_1.py`) was not run (on request only); it now recomputes the new price-block rows in Python.
- **Caveats:**
  - **Word documentation, register, deck not regenerated:** the `.docx` files named v4.1 hold the v4.0 content, and the deck stays v4.0 (regenerated with the next full check).
  - **Second summary rows** (changes against scenario 1) are shown for 11-14 only, as an exception the user allowed; section 2's summary (`rpe`) repeats the all-energy unit value of the price memo.
  - **Price-block averages use each scenario's own quantities** (unit values, as the user allowed); they are not price indices.
  - **Header rows moved** (section 0): scenario name row 4, shock factor row 6 (one-digit row keeps the fuel-use formula within 100 characters), GDP growth row 14; anything outside the builder that typed old header rows needs updating (none found in the repository).
  - Not yet checked in Excel on Windows (no Excel in the cloud).

## 2026-10-16 - CPAT-AI-Mitigation-MVP v4.2: Cover, divider contents, tab title bars, reference tabs, constants to mappings (user request)
- **Task (user, queued during v4.1):** Check and Variables before Lambdas, Lambdas condensed (row lists, build-up order) and its purpose explained; tab Version Log, About, and Diff with the wide column C, the difference number in column E, register code / bug or issue / status columns; About table edited, with a category column and the name as first entry; version table incl. the 4.0 bump and no version tags in headings; dark green title bar and light green sub-heading bars of one width on every tab; divider tabs with a table of contents and the legacy counterpart of each tab; a Cover tab as legacy (colours); remove purposeless light green shading; named constants restructured (semi-elasticities are data, feebate positions are mappings); data tabs split into mitigation data and other data, documenting legacy similarity; norms.
- **Outputs:** v4.2 file set (v4.1 masters in `Old/`), workbook at the top of `excel_ai/`; `excel_ai/NORMS.md` 2.1 (light green = inputs only), 1.4 (Cover first), new 2.7 (tabs other than Mitigation); quick check: title-bar / sub-bar width, header fills, Cover first.
  - **Tabs:** `Cover` (contents with legacy counterpart, cell colours, tab colours, abbreviations; as the legacy Cover); dividers `MAIN->>`, `INPUTS->>`, `DATA_MITIGATION->>` (23 tabs with a legacy data tab: Yes or Partly), `DATA_OTHER->>` (6 tabs with none: PriceAssump, BaselineCO2, GWP_AP, GainsRegion, TransportParams, TransportPaths), `REF->>`, each with its table of contents; tab colours by group.
  - **`Version Log, About, and Diff`:** columns A-D for the log; About = category (About, Layout, Assumptions, Algorithm, Use, Version notes), topic, text (27 entries, rewritten; the old per-version notes are in the log); differences: Type, Area, This model (C, wide), Legacy CPAT, # (E), Why, Effect, Register code, Bug or issue, Status (from the register `issues_register`: L codes fixed, I codes their status, LD rows open or replicated, decisions accepted).
  - **`Check, Variables, Lambdas`:** MacroCheck first (its block keeps the 300 rows the macro clears), then Variables, then Lambdas: one line per formula pattern (variable, LAMBDA, formula of the first row, Mitigation rows such as `93-106`, count, members, section), about 990 lines for 2,100 rows, sorted by row (build-up order). **Purpose:** both: it documents for readers which LAMBDA replaces each row's plain formulas, and the full check copies each formula back over its rows (the "LAMBDA library everywhere" test), so it is kept machine-readable (rows as a list, formula of the first row).
  - **Constants:** the ETS benchmark group and feebate sector positions and the ETS semi-elasticity group of each coverage sector moved from Constants to a Mapping table (`CovKey`, `CovEtsPos`, `CovFbPos`, `CovSemiPos`); the semi-elasticities are read from the data tab ETSSemi where used (Mitigation obr rows, column E).
  - **Styling:** row 2 of every tab a dark green title bar with what the tab is for; blocks of consolidated tabs and MTOutputs blocks with light green bars of the same width; table headers bold with a bottom border, no fill; light green kept on inputs only (mapping tables cleared).
- **Check (full build):** quick check PASS incl. the new tab tests (title and sub-heading bars of equal width on every restyled tab, no header with the input fill, Cover first); 0 error cells after recalculation; **0 of 9,934 output codes change against v4.1** (max abs diff 1e-11). The full check was not run (on request); it now reads the condensed Lambdas sheet and the new VersionLog columns.
- **Caveats:**
  - Mitigation, MTInputs and Prices_dom keep their legacy layouts (not restyled); MacroCheck has no sub-heading bar (its first rows are the macro's report area).
  - Data tabs were split by dividers and documented, not merged into Settings (the user asked for documentation first).
  - Word documentation, register and deck not regenerated (v4.0 content); the Lambdas sheet changed format, so `presentation/make_screenshots` needs an update before the next deck.

## 2026-10-17 - Coded CPAT: the old coded (now coded_increment) merged into the new coded (user request)
- **Task (user):** the new `coded` (commit 741696e) is the main Python project; check that it works, plan the merge and carry out the plan: bring in the distribution module and the pandas updates of the old project (`coded_increment`), then remove it.
- **Inputs:** `coded/` (new layout: `mitigation/`, `data_read/`, `indicators/`, `cpat_shiny/`, sample data `data/dummy`), `coded_increment/` (old layout `components/`, `inputs/`; distribution module; data gitignored), `excel_ai/distribution/data_standardized/CPAT_DistributionalData.xlsx`.
- **Outputs:**
  - **New project fixed (commit 68114f9):** the policies, GHGs and CH4 loaders read the CSVs under `DATA_PATH` (were hard-coded to a missing `data/new_data_pkl`); pandas copy-on-write fixes (writes through `.iloc` not `.values`: phaseouts x3, carbon-price trajectory x2; numeric zero coverage columns; float zero `ctxnew` frames); tests updated to the new import paths (they had not been, so none ran); `requirements.txt` completed; typo `calcualte_power_year`.
  - **Distribution brought in:** `cpat_model/distribution/` (9 files), `distribution_inputs.py`, `scenario_results.py` (now also carries `power`), 34 distribution constants in `constants.py`, the 8 `distn_*` tables in `InputData`, `run_model.py` (`run_distribution`; `run_model()` returns `(scenario_results, distributions)`), tests in `cpat_testing/model/distribution/`.
  - **Data:** `coded/data/dummy/distn_*.csv` (11 files, 12 MB, Egypt) from `excel_ai/distribution/scripts/build_distribution_model_data.py`, whose paths were fixed (repository root, lowercase `distribution`, output folder `data/dummy` or an argument).
  - **Docs:** `coded/README.md`, `coded/TODO.md` (new), developer guide (layout table, distribution in the run, data note, pandas 2/3), docstring template; `excel_ai/distribution/README.md` paths and a section on running inside the model; root README; price method note path. `coded_increment/` deleted (its older Sisepuede guide is superseded by the developer guide).
- **Check:**
  - before: the new project's model failed (missing pickles) and its tests did not collect; the increment's distribution tests needed data not in the repository;
  - after: **48/48 tests pass on pandas 2.2.3 / numpy 2.2.0 and on pandas 3.0.5 / numpy 2.5.3** (35 existing, 12 distribution, 1 new); `run_model.py` runs end to end on both, also with FutureWarnings as errors;
  - **mitigation results identical** to the original new code (rp, emissions, generation, fuel use, carbon price, both scenarios) and between pandas 2.2 and 3.0 (difference 0);
  - **distribution results identical** to the old code: Egypt, Excel's 2030 carbon-tax price changes, with and without deadweight losses, 36 tables, 2,246 numbers, difference 0, on both pandas versions; the Shiny app loads and serves its page.
- **Caveats:**
  - **Fixed while wiring the run (the old project's end-to-end run had the same errors):** electricity prices of projected years now come from the power model (`power.demand.rp_demand`; `EnergyPrices.ele_prices['rp']` holds history only), oil products take their all-sector price (they have no residential price), and each country's Distribution gets its own rows (`country_view`; HH_Elast and GDPRatios hold several countries).
  - **Open, not fixed (TODO):** carbon-pricing revenue from a run is USD million but used as local currency, so recycling effects from a run are far too small; `national_totals=None`; the electricity price is the power model's simplified one; other oil products sit at the 0.01 price floor in the sample data.
  - The `data/dummy` folder now also holds real Egypt distribution data (the name is the new project's).
  - **Environment (user decision 2026-10-17):** `environment.yml` and `requirements.txt` pinned to Python 3.12 (as `cpat312`), pandas 2.2.3, numpy 2.2.0, matplotlib 3.9.2 (3.8.0 predates numpy 2); tested on Python 3.12.3 (48/48, run, app, results identical) and also on 3.13 with pandas 2.2.3 and 3.0.5. The old pins (Python 3.11.9, pandas 2.1.4, numpy 1.26.4) were not tested.

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.3: LAMBDA test group; plan for the distribution module (user request)
- **Task (user):** new norm: instead of the LAMBDA year (2041 of every scenario group), a full third scenario group with the LAMBDAs from the first to the last year, none in groups 1 and 2, so the LAMBDAs are tested with their IFs inside; a simple test instead of full tests: where two groups run the same scenario number, row sum vs row sum, 1 against 2 and 2 against 3, no errors. Then plan the distribution module (find the prototype).
- **Outputs:**
  - `build_v4_3.py` (`lambda_test_group`): groups 1 and 2 plain in every year (2041 takes the 2040 formula); group 3 (code column BC, years BD:BW) is group 2 pasted, runs the scenario number of the group on its left, and calls the row's LAMBDA in every year (base year too, unless it is data); codes end in `L`. The spacer column of each group tests the group on its right when both run the same scenario (row sum minus row sum; largest absolute difference in the spacer's row 4); rows whose spacer cell a model formula reads (power look-ahead, the centred moving average of fuel prices) stay blank.
  - `check_quick_v4_3.py`: LAMBDA group test after the LibreOffice recalculation (LAMBDAs expanded).
  - Norms: `excel_ai/NORMS.md` section 3 (LAMBDA test group replaces the LAMBDA year), 3d, 3e.
  - Plan: `excel_ai/distribution/PLAN_Distribution_in_MVP.md` (prototype found in `excel_ai/distribution/standalone/`, v0.4; its remaining error located).
- **Check (quick check, full build):** see the v4.3 version-log row; LAMBDA group 3 equals group 2 on all 4,996 row sums (largest relative difference 4e-16), in-sheet test 0, no error values; groups 1 and 2 identical in relative form; shared output codes unchanged against v4.2.
- **Caveats:**
  - The LAMBDA group is tested in LibreOffice with the LAMBDA calls expanded; Excel 365 itself (live LAMBDAs) is still to be confirmed on Windows.
  - The full check (`check_v4_3.py`) still assumes the LAMBDA year and blank spacers; not run, to be adapted (TODO).
  - The spacer test leaves the rows read by look-ahead formulas blank (price blocks and power levelised-cost rows); their LAMBDAs are covered through the rows that use them.
  - Word documentation, register and deck still hold the v4.0 content.

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.4: distribution module prototype; scenario capacity; standalone v0.5 (user request)
- **Task (user):**
  - Distribution only to 2030; one analysis year with three scenario groups, deciles across, outputs as legacy; build the prototype and update the norms.
  - Norm: the user can paste up to five policy scenarios.
  - Keep the standalone tool and fix it.
  - Push v4.3 to main (done: 3696156).
- **Outputs:**
  - `build_v4_4.py`: sheet Distribution (13 columns per group: code, basket, deciles 1-10, spacer; groups 1-2 plain, group 3 the LAMBDA test group); data tabs HHSurvey, HH_Elast, IO_GTAP, ASPIRE, WHOCooking, GDPRatios and DistMapping under the divider DATA_DISTRIBUTION->>; MTOutputs distribution block (legacy rows 911-1033 and their codes); scenario definition 6.
  - `extract_distn_v4_4.py` (data/distn_*.csv), `distribution_ref_v4_4.py` (Python reference), `Distribution_Method_v4_4.md`.
  - `check_quick_v4_4.py`: Distribution checks. `check_paste_v4_4.py`: Mitigation and Distribution groups 4-7.
  - Norms: NORMS 1.1b (Distribution layout), 3c rule 4 (single-year module exception), 3e (scenario capacity).
  - Standalone: `distribution/standalone/CPAT_Distribution_Standalone_Egypt_v0.5.xlsx` (NET_EFFECT basket = total recycled / total consumption).
- **Checks:**
  - Python reference on legacy's cached Egypt inputs reproduces legacy's cached outputs: effects, recycling, net effect and compensation to 4e-4 (the cache's rounding); Gini changes to 7e-6.
  - Two simplifications verified on the cache: indirect prices (k(s) cancels: 59 sectors to 4e-16, categories to 3e-6) and the Gini as fixed weights.
  - Quick check (quick build): PASS. Distribution group 2 equals the reference fed with the sheet's inputs (505 values, 6e-13); its LAMBDA group equals group 2; no error values; Mitigation output codes unchanged against v4.3 (bco2 rows only, as every quick build).
  - Paste test before the change: groups 4-6 worked; scenario 6 failed for want of a definition (added).
  - Full build: quick check PASS; Mitigation output codes identical to v4.3 (9934 shared, 0 change); Distribution as above.
  - Paste test (groups 4-7 of Mitigation and Distribution, scenarios 3-6): PASS. No error values; scenarios 3, 4 and 6 equal StoredResults (0); every difference row = level - scenario 1 (8e-10).
  - Scenario 5 (new ETS) is reported, not compared: the batch macro runs the ETS goal seek, a pasted group the fast estimate (largest difference in ets.p).
- **Caveats:**
  - Legacy bugs fixed (method note section 3) change Egypt's legacy numbers a little (targeted transfer deciles 1-4 up to 0.13 points; urban and rural compensation shares now sum to 100).
  - Not modelled: ASPIRE-targeted and poverty-line transfers, median flags (support check in section 1).
  - ScaleGTAP = No uses economy-wide fuel price changes.
  - Revenue = Mitigation's new-policy revenue.
  - Distribution data for Egypt only (as legacy NoPropData).
  - The standalone fix is tested in Python only (no Excel here); the file recalculates on opening.
  - The LAMBDAs are tested in LibreOffice with the calls expanded.


## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.5: data tabs aligned with legacy; all-country readiness (user request)
- **Task (user):** check the data tabs:
  - order them as legacy (grouped by module) with similar names, format and content, without undoing better norms;
  - check that the model would work with the full all-country tables (about eight were cut to Egypt because the proprietary data cannot be shared);
  - put Egypt-only tables alone on their tab or at the bottom;
  - check how far legacy tables can be copied in, and align where possible.

  User interface: later.
- **Outputs:**
  - `build_v4_5.py` (v4.4 copied to `Old/`):
    - Data tabs grouped as legacy: DATA_MITIGATION, DATA_DISTN, DATA_TRAN, DATA_OUTPUT, then DATA_OTHER.
    - 16 tabs hold the legacy table unchanged (header row 3, data from A4, legacy column letters; key formula column right where legacy has no unique key): Balances, EnergyCons, GHGs, CH4Inputs, UNPop, EF_GHG, SCC, EF_PM, IO_GTAP, HHSurvey, HH_Elast, ASPIRE, WHOCooking, GDPRatios, Transport1, Transport2. Prices_dom keeps the legacy header rows (paste legacy rows 4+ at A1; ranges widened to 142+ columns).
    - Named ranges sized for all countries.
    - Base-year fuel use and power demand from Balances through legacy's flow mapping (Mapping J-M; MTInputs BalancesOrConsumption, Settings C31); EnergyCons is the alternative. PowerDemand and EF_NonCO2 dropped (EF_PM, legacy codes).
    - CO2 emission factors selected from the legacy EF_GHG table as legacy rows 980-1011, on a new Inputs block (Inputs_ef): country, else World Bank region (Settings C43, CtryReg), else world; legacy's row references; jet fuel IEA (constant EFJetIEA); biomass 0. GWP_AP dropped (GWP100 read from EF_GHG).
    - GHG inventory column codes on Mapping (GHGCol, by position as legacy). CH4Inputs source codes now LOWER(LEFT(tier3,3)): oil, coa, liv, ric, tot.
  - `extract_legacy_tables_v4_5.py` (new): `data/legacy_<Tab>.csv`, verbatim from the legacy file.
  - `extract_distn_v4_5.py` trimmed to the mappings; `distribution_ref_v4_5.py` reads the legacy tables.
  - `check_allcountry_v4_5.py` (new, on request): clones every Egypt row of every data tab as a dummy country (XEG) at the bottom of its table; outputs must equal Egypt's.
  - `DataTabs_v4_5.md` (tab by tab: legacy source, layout, countries, copy-in route).
  - NORMS 1.5 (new) and 2.7 items 6-7; QuickStart "Another country"; READMEs; TODO.
- **Checks:**
  - Legacy tables against the previous CSVs: identical values (SCC, UNPop, CH4Inputs, GHGs, Transport1, Transport2, GWP100). The EF selection reproduces Egypt's factors exactly.
  - Quick check (quick build): PASS. Mitigation output codes unchanged against v4.4 (only the bco2 rows of every quick build); Distribution = Python reference (5.4e-13); both LAMBDA groups = group 2.
  - Full build: quick check PASS; all 9,934 Mitigation output codes identical to v4.4 (largest difference 1e-9); Distribution = Python reference (5.4e-13); LAMBDA groups = group 2. Paste test (groups 4-7): PASS; scenarios 3, 4 and 6 equal StoredResults (0); scenario 5 (new ETS) reported, not compared.
  - All-country test (quick build): PASS. 626 Egypt rows cloned as XEG in 27 tabs, appended below each table; no error values; 164,962 output values of Mitigation and Distribution identical to Egypt's (max difference 0). The ghg.h row (a row number of the GHGs table) is compared as found / not found.
- **Caveats:**
  - Still from legacy's cached Egypt run, so a converter is needed for other countries (TODO): PowerTech, PowerPaths, PowerParams, WEO GDP rows (legacy Mitigation rows 415-467); BaselineCO2 is derived by the build.
  - Own layouts kept (all countries, converters exist): Countries, ECP, Prices_int, Elasticities, ETSSemi, Transport3, TransportParams, TransportPaths, Multipliers, PriceAssump, GainsRegion.
  - GHGs now includes Zimbabwe 2021 (legacy row 947; the old extract stopped at 946). The Python references still read the old CSVs (same values).
  - In the LibreOffice conversion, legacy rows 980-1010 show `IFNA(U)` (world only); the cached values show the real rule (country, region, world), which is what was built.
  - Our Egypt Prices_dom values differ from legacy NoPropData (the earlier documented Egypt price update), so do not paste legacy's Egypt rows over them unless that update is to be undone.

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.6: legacy tabs at legacy addresses; country data steps (user request: align more fully)
- **Task (user):** once v4.5 was done, align more fully, going with the recommendations without further questions.
- **Outputs:**
  - `build_v4_6.py`:
    - Countries, Elasticities, ETS+LTS, Multipliers, Prices_int and ECP are legacy tabs kept at their legacy cell addresses from row 3; Transport3 from row 5 (`data/legacy_<Tab>_cells.csv`).
    - WEO is the legacy table (header row 3, data from A4).
    - ETSSemi, GainsRegion and PriceAssump are dropped; their values are read from the legacy tabs.
    - New Inputs blocks that do what legacy Mitigation computes for the selected country (NORMS 1.5 rule 2c):
      - Inputs_ela: the country's column of Elasticities;
      - Inputs_mult: median ± sd by group, instrument and lag;
      - Inputs_macro: WEO series extended as legacy rows 417-467, plus the energy trade balance and share traded (rows 741-743) from Balances;
      - Inputs_pint: international price series as rows 633-695;
      - Inputs_ecp: ECP of the country, one ETS per country, coverage carried forward.
  - Register: L51 (coal trade balance valued at the oil price) fixed.
  - NORMS 1.5 rules 2b and 2c; `DataTabs_v4_6.md`; the clone test renames in place on tabs kept at legacy addresses.
- **Checks:**
  - Quick check on the full build: PASS. Against v4.5, 10 output codes change, all intended:
    - xtb coal and its totals: about 0.61 bn USD a year (L51 fix);
    - trgdl 2022: the WEO 2021 growth of 3.25 % instead of 0. Transport fix B2, already in the builder, now takes effect, because the old WEO copy had no 2021 value.
  - Paste test: PASS.
  - All-country test (quick build): PASS (0 errors, 164,962 values identical).
  - The new macro series reproduce the legacy cached Egypt rows to 1e-15 (GDP in USD and LCU, deflators, trade balances of gas and oil, shares traded).
- **Caveats:**
  - Lookups into the tabs kept at legacy addresses use legacy addresses and legacy row numbers (as legacy does), so the pasted legacy tab must keep its layout.
  - IEA price series: "NA" where the source has no value, as legacy; averages over only "NA" give "NA" (legacy: #DIV/0!).
  - Power data still came from legacy's cached Egypt run in v4.6; v4.7 follows.
## 2026-10-17 - Coded CPAT: export of the proprietary tables to the legacy layout (user request)
- **Task:** a script that turns the four proprietary tables in the Coded CPAT data form (energy use, domestic prices, household survey, IO_GTAP) into one workbook in the legacy CPAT sheet layout, ready to copy-paste into legacy.
- **Inputs:** `coded/data/dummy/` (`energy_consumption.csv`, `prices_dom.csv`, `distn_hh_survey.csv`, `distn_io_gtap.csv`) or `REAL_DATA_PATH`; legacy `CPAT 1.0pre_456_NoPropData.xlsb` sheets `EnergyCons`, `Prices_dom`, `HHSurvey`, `IO_GTAP` (header layouts) and `Mitigation` rows 578-603 (how `EnergyCons` is read: key `LOWER(country)&".mit.enc."&fuel`, columns E:V by letter, Consumption mode only).
- **Outputs:** `coded/legacy_export/export_to_legacy.py`, `legacy_layouts.json`, `README.md`; tests `coded/cpat_testing/legacy_export/test_export_to_legacy.py`; `coded/README.md` layout row; `pyxlsb` in `dev-requirements.txt`; `.gitignore` for `CPAT_LegacyData*.xlsx` except the dummy export next to the legacy workbook (unchanged): `excel_ai/legacy/workbooks/CPAT_LegacyData_dummy.xlsx` (exactly the four tabs), `CPAT_LegacyData_dummy_csv/` (the same four tabs as CSVs) and `CPAT_LegacyData_dummy_ReadMe.md` (paste ranges, gaps); all dummy countries. Tests: 9 (suite 57 pass). Checks: headers equal the legacy layouts; every exported value equals the CSV (to openpyxl's 16 significant digits); `HHSurvey` (132 rows) and `IO_GTAP` (11 rows) reproduce the legacy workbook cell for cell (Egypt; within 1e-15, as `data_standardized` rounds to 16 decimals).
- **Caveats:**
  - Energy goes to `EnergyCons` (legacy Consumption mode), not the IEA flow-level `Balances` sheet, which cannot be rebuilt from the sector-level CSV. `ren` and `total_energy_use` are not exported (legacy computes them); `wav`, `neu` blank; the Year column is a parameter (default 2022).
  - 48 legacy `Prices_dom` columns are not in `prices_dom.csv` (source/reliability flags, `taxa`, `sub.or`, production, spot prices) and are left blank; `countrycode_weo` = ISO code.
  - Not tested by pasting into legacy Excel (no Excel here). In the NoPropData file some lookups into the stripped sheets are shrunk to row 1 (e.g. Mitigation AA583) and need widening; the full workbook has them.
  - The mitigation CSVs in `dummy/` are randomised, so the dummy export is a format sample only.

## 2026-10-17 - Docs: dummy legacy-data files in README and NORMS; consistency check (user request)
- **Task:** documented the new dummy legacy-data files next to the legacy workbook and checked that they agree with the Coded CPAT dummy data, with the workbook as master.
- **Inputs:** `excel_ai/legacy/workbooks/CPAT_LegacyData_dummy.xlsx`, `CPAT_LegacyData_dummy_csv/`, `CPAT_LegacyData_dummy_ReadMe.md`; `coded/data/dummy/` (`energy_consumption.csv`, `prices_dom.csv`, `distn_hh_survey.csv`, `distn_io_gtap.csv`); legacy `CPAT 1.0pre_456_NoPropData.xlsb`.
- **Outputs:** `NORMS.md` new section 8 (legacy data files: which file is read-only, which is master, how to check consistency); `README.md` (current release v4.6, layout of `legacy/workbooks/` and `coded/`, new "Loading data into legacy CPAT" row, data flow back to legacy); `excel_ai/README.md`, `coded/README.md`, `AGENTS.md` (pointers to section 8). No data file changed.
- **Checks:** re-running `export_to_legacy.py` on `data/dummy/` reproduces the committed workbook (0 cell differences on all four tabs) and the four CSVs byte for byte; `cpat_testing/legacy_export` 9 pass (incl. `HHSurvey` and `IO_GTAP` against the NoPropData workbook).
- **Caveats:**
  - Nothing differed, so the "workbook is master" rule was not exercised.
  - The dummy `Prices_dom` rows for Egypt differ from the Egypt rows cached in the NoPropData workbook (randomised dummy data; NoPropData also has EGY2025, which the dummy lacks). `EnergyCons` is empty in the NoPropData file. If dummy data that match the NoPropData Egypt values are wanted, that is a separate task.

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.7: power data from the legacy Power, CoC and GHGs tabs (user request: align more fully)
- **Task (user):** finish aligning the data tabs with legacy, going with the recommendations. The last tables copied from legacy's cached Egypt run (PowerTech, PowerPaths, PowerParams) are now computed from the legacy tabs.
- **Outputs:**
  - `build_v4_7.py`:
    - Power, CoC and GHGs are legacy tabs at legacy addresses (NORMS 1.5 rule 2b). GHGs keeps a key column (BA, rows 8-947) and adds the 2023-2024 emission shocks (rows 1201-1388).
    - The power data of the country is a data step on Inputs (rule 2c), formulas only, reproducing legacy Mitigation section 4 (`PowerData_Chain_v4_7.md`):
      - Inputs_pset: the power settings of MTInputs scenario 1 and derived values (defined names Ps...);
      - Inputs_ptech: by generation type, country else world parameters, efficiency and generation from Balances, WACC from CoC (by income group), capacity factors;
      - Inputs_ppath: capex time factors, storage, income factor, fuel price shocks, prices;
      - Inputs_ppar: parameters.
    - PowerTech, PowerPaths and PowerParams are dropped; their names point to the Inputs blocks, so the power model is unchanged.
  - Register: I38 (legacy's stored run, see below). L52-L56 are legacy bugs the power data step still copies, status "Kept as legacy in v4.7, queued to be fixed" (NORMS 0, BUGS_REPLICATED).
  - Docs: `DataTabs_v4_7.md` (power rows, layout counts, power data step), NORMS 1.5 rules 2b and 2c, `QuickStart_v4_7.md` (Another country: all public tables hold every country), READMEs, TODO (converter item done; fixes of L52-L56 queued).
- **Checks:**
  - The Inputs power blocks reproduce `data/power_*.csv` (legacy's cached Egypt values) to 1e-12, except the wind and solar capex time factors for 2039-2041.
  - Quick check (full build): PASS, 0 error values. Against v4.6, 503 output codes change, all from 2039 on (on the quick build, the first differing year was 2039 or 2040 for every code): new capacity and investment of solar, wind and gas, then power fuel use and emissions (largest: new solar investment, up to 149 MW a year).
  - Paste test: PASS (groups 4-7 equal StoredResults, 2,200 values each, scenario 5 with the new ETS included).
  - All-country test (quick build): PASS (617 rows cloned in 25 tabs; 0 errors; 164,962 values identical).
- **Build (user rule 2026-10-17):** no ETS goal seek in the build. It took 22 of the build's 27 LibreOffice recalculations; the full build now takes about 20 minutes instead of about 70. A new ETS (definition 5) is stored at the workbook's own price estimate; RunAllScenarios in Excel still goal-seeks the cap. The paste test now also compares definition 5.
- **Caveats:**
  - I38: legacy's stored Mitigation values of the wind and solar capex time factors for 2039-2041 (wind 0.920, 0.915, 0.909) disagree with the cached Power cells they reference (0.923, 0.920, 0.918), apparently a stale cache in the distributed file. The MVP follows the Power tab, so its results depart from legacy's stored run from 2039. Recheck against a fresh legacy run.
  - L52-L54 change Egypt's power results once fixed (renewables take the world parameters; actual capacity factors never used; hydro investment from the first year); L55-L56 do not affect Egypt. Queued (TODO).
  - `data/power_*.csv` now only gives the layout and the technology classes (price code, VRE, dispatch) and is the reference the data step is compared with.
  - The quick check of the v4.8 draft ran LibreOffice while the first v4.7 full build was also running it, breaking the one-job rule. That build was stopped anyway (goal seek dropped); the v4.7 full build that was kept ran alone.

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.8: Distribution readability (user request)
- **Task (user):** make the Distribution sheet readable: per section the green band, a summary row and a visible blank row, with one row group per section (not two); hide the parameter columns and narrow the others; change the default zoom; format the scenario number at the top as on Mitigation.
- **Outputs:**
  - `build_v4_8.py` (sheet Distribution, as Mitigation, NORMS 2.5):
    - one row group per section, the summary row last;
    - summaries, all overall: analysis year (section 0, moved to row 12), options check, revenue, three new rows (average indirect price change of the consumption categories and average fuel price factor, both weighted by budget shares; energy budget share), then total effect, total consumption, recycling gain and net effect after recycling;
    - sections 6-9 list urban and rural first, overall last;
    - columns C:G and I:K in one column group each, rolled up;
    - narrower columns (deciles 9, descriptions 44), with totals in local currency shown in bn and population in m (values unchanged);
    - zoom 75;
    - row 4-5 labels bold and the basket cell of row 5 in the base colour, as Mitigation.
  - Docs: NORMS 1.1b, `Distribution_Method_v4_8.md`, READMEs, TODO (build-speed plan).
- **Checks:** quick check (full build) PASS: 0 output codes change against v4.7; the Distribution LAMBDA group equals group 2 (342 rows) and group 2 equals the Python reference (505 values). Paste test PASS. Full build 19 minutes.
- **Caveats:**
  - The three new summary rows add output codes (`dprw.cat`, `facw.ene`, `bsh.ene`; not in MTOutputs or legacy).
  - Survey code rows moved from 11-12 to 10-11 (formulas name them; lookups unchanged).
  - The column cut-off for faster recalculations (user message cut off) is still to confirm (TODO).

## 2026-10-17 - CPAT-AI-Mitigation-MVP v4.9: full build as fast as possible (user request)
- **Task (user):** do the full build as quickly as possible and optimise further; speed comes first (the builds give no errors); update the norms.
- **Outputs:**
  - `build_v4_9.py` and the new `lo_session_v4_9.py`; NORMS (excel_ai) "Build speed" (7 rules) and the LibreOffice rule (parallel sessions only with their own profile); README, TODO.
  - Full build about 19 minutes (v4.8) → about 2.2-2.9 minutes (≈7-8x; v4.6 took about 70). Measured stage by stage (the build now prints its stage times), then:
    - one LibreOffice session per worker process over UNO: the recalculation copy is loaded once, each run writes its inputs (MTInputs definition column copied into the live column; BaselineCO2) and recalculates in memory (`calculateAll`, about 17 s), and only MTOutputs blocks 1-2 are read. Before, each run had a save, reload, LAMBDA expansion, file conversion and reload (about 155 s);
    - the 5 runs are shared among 3 parallel sessions (4 or 5 sessions gave no gain on 4 cores); session 1 reports scenario 1's CO2, from which the baseline CO2 is set for all; the tabs are merged meanwhile;
    - the recalculation copy is written from the workbook in memory, without the LAMBDA test group of Mitigation and without Distribution (nothing stored reads them);
    - generation 105 s → about 30-40 s: `ws.max_column` was computed per row (a scan of every cell, 5,597 times), and group 3's copy of group 2 now uses a column shifter (10x faster than openpyxl's Translator, identical on all 108,220 formulas).
- **Checks:**
  - The v4.9 workbook equals v4.8 cell by cell (2,981,694 cells, values and styles), apart from version strings and the version-log row; StoredResults and BaselineCO2 equal to 1e-14.
  - Quick check PASS: 0 output codes change against v4.8. Paste test not rerun: the scenario groups and stored results are identical to v4.8's, which passed.
- **Caveats:**
  - A first ordering (merge the tabs before rebuilding StoredResults) left the StoredResults header fill unstyled; the quick check caught it, and `style_tabs` now restyles that tab after the rebuild.
  - Threads with pyuno serialise (GIL), so the sessions run as spawned processes. A script that imports the builder and calls `main()` must be guarded by `if __name__ == '__main__'`, or each spawned worker reruns it.
  - The quick check (about 3 minutes) and the paste test (about 5) still use file conversions; moving them to sessions is in TODO.

## 2026-10-18 - Check speed: quick check and paste test on LibreOffice sessions (TODO "Check speed"; tooling only, workbook v4.9 unchanged)
- **Task (user):** the next TODO step, as promised: the quick check and the paste test on the fast LibreOffice sessions.
- **Outputs:**
  - `lo_session_v4_9.py`:
    - `start_values`: recalculate a file in a spawned session and read the used ranges of the sheets named; error cells come from LibreOffice's own query;
    - `expanded_zip`: the LAMBDA-expanded copy written from the file's XML (about 11 s; no openpyxl load and save), optionally with a copy-paste of columns written into the XML;
    - `uno` imported lazily: a spawned child that imports uno while it re-imports the parent's main module fails ("pyuno runtime is not initialized").
  - `check_quick_v4_9.py`: LibreOffice recalculates while the structure checks run; it prints its stage times.
  - `check_paste_v4_9.py`: the paste is written into the XML; the stored results are read meanwhile.
  - NORMS (excel_ai) "Build speed" rule 8; README; TODO.
- **Checks:**
  - Quick check 197 → 95 s: PASS, the same lines as before. Differences of 1e-16 to 6e-10, because the values no longer round-trip through 15-digit file text.
  - Paste test 309 → 206 s: PASS, groups 4-7 equal StoredResults (2,200 values each).
  - Same inputs as before:
    - the XML expansion gives the same formulas as variant 'expand' (all 422,845);
    - the XML paste gives the same cells as openpyxl's Translator paste (all 574,168).
  - The full build still runs (2 min 48 s) with identical StoredResults and BaselineCO2.
- **Caveats:**
  - Pasting with UNO `copyRange` was tried and dropped:
    - with automatic calculation on, it recalculates after each paste (197 s for 4 groups);
    - with it off, it leaves error values in a pasted group.
  - Loading the full expanded workbook in LibreOffice (about 60 s, parsing) is now the critical path of both checks. The all-country test still uses file conversions (TODO).
  - The checks were changed in place in v4.9 (tooling only): the workbook and the build are unchanged.

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.10: no legacy bug replicated (user rule: bugs are never replicated)
- **Task (user):** stick to the rule, fix every legacy bug the prototype still copied, update the reference information, and say whether bugs and issues are then cleanly split.
- **Outputs:**
  - `build_v4_10.py` fixes the six bugs that were kept as legacy and queued:
    - L14: the floating excise applies (1 - pass-through) once;
    - L52: every generation type takes the country parameters where they exist;
    - L53: the actual capacity factor (base-year output / installed capacity, Power rows 358-1635 over F:AC) is used inside the CFOverride bounds, else the studies value;
    - L54: hydro invests from the base year only above a 50% generation share (new constant HydInvShare);
    - L55: country rows are looked up in the country block, Power rows 112-294;
    - L56: countries without CoC risk data take the default WACC, flagged (PsCoCData).
  - New names: PowACtry, PowAPre, PowIC, PowICKey, PowICYr, CoCC. New MTInputs settings on Inputs_pset: PsCFMinVRE, PsCFMinOth, PsCFMax.
  - `check_v4_10.py`: the full check's price reference follows the L14 fix.
  - Register: the six entries read "Fixed in v4.10"; BUGS_REPLICATED is empty. The replication lists say so; "none" replaces an empty table.
  - Docs: Equations E21, PriceProjection A10, DataTabs, PowerData_Chain (v4.10 note), TODO, READMEs.
- **Effect for Egypt** (quick check against v4.9: 1,793 output codes change, all from the power fixes; L14, L55 and L56 have no effect for Egypt):
  - capacity factors gas 0.566 → 0.385, wind 0.30 → 0.44, solar 0.18 → 0.35, hydro 0.43 → 0.59;
  - base-year gas capacity 35 → 52 GW, the installed capacity;
  - solar fixed O&M 15 → 11.831 $/kW/y;
  - hydro investment from 2030;
  - 2030: industrial electricity use +1.9%, baseline CO2 +1.3%, CO2 cut of the policy scenario 19.6 Mt instead of 22.4.
- **Checks:**
  - Quick check (full build) PASS: 0 error values.
  - Paste test PASS.
  - All-country test PASS: 165,028 values identical, the new installed-capacity rows included.
  - Full build 2 min 41 s.
- **Caveats:**
  - The bug side is clean: 55 legacy bugs, none replicated.
  - The issue side is not clean yet, because of departures from legacy with no user decision behind them:
    - 12 legacy issues not replicated: 3 accepted by user decision (I6, I20, I32), 9 open, queued to be replicated (I7, I14, I21, I23, I24, I25, I26, I27, I31);
    - 44 LegacyDiff departures: 11 user decisions, 4 data updates, 29 neither (13 simplifications, 8 features not built, 3 assumptions, 2 methods, 2 design, 1 to check);
    - by the rule, each needs a user decision (exception) or replication.
  - The capacity-factor bounds (CFOverride, MTInputs scenario 1) now act, so a user's change to them changes power results.

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.11: bug / issue split, user decisions
- **Task (user):** decisions on the 38 departures from legacy: LD6 is a bug; LD47 needs a new legacy file; LD36 goes with legacy, as an issue; I27 is a bug; I31 may need two options for Distribution (legacy or new); LD3 is a data issue; LD53 sticks to legacy (the structure of the processed Balances); I24 goes to TODO. Explanations asked for I7/LD38, I21, LD5, LD46, LD62, LD44 and I23.
- **Outputs:**
  - `build_v4_11.py`:
    - CO2 calibrated to the inventory as legacy: switch Settings C27 on; inventory energy CO2 of the year before the base year over the base-year estimate (Egypt 0.930; I32 replicated, LD57 now the same as legacy);
    - food & forestry split into food and forestry/agriculture as legacy: Inputs columns fdk, fdt, fsh from the Balances info_ flows (helper Settings C44, BalInfo); block apfd (food fuel use); memo rows ap.<pollutant>.fod / .fag, not in the totals; zero for Egypt (LD53).
  - LegacyDiff relabelled: LD6 bug L57 (new), LD8 bug L15, LD49 bug L58 (new; was I27, removed from the issues); LD17, LD26, LD30, LD32, LD42 same as legacy; LD3, LD47 data.
  - Full check reference (`check_v4_11.py`) follows the new calibration.
  - Docs: CO2Calibration_Method (rewritten), GHG_Method, AirPollutants_Method, QuickStart, READMEs; TODO "Bug / issue split" with the open items.
- **Checks:**
  - Quick check (full build) PASS: 0 error values. Against v4.10, 1,862 output codes change (CO2 everywhere; in policy scenarios, prices and quantities through the lower carbon cost per unit of fuel) and 46 are new (food rows).
  - Paste test PASS. Full build 2 min 34 s.
- **Caveats:**
  - Legacy's calibration carries Egypt's 2021-2022 inventory break (I17) into every year: calibrated energy CO2 is 211 / 183 / 204 Mt in 2022-2024, against inventory values of 252 / 267 / 285. This is legacy behaviour, now replicated by user decision.
  - After v4.11: 57 legacy bugs (none replicated); 10 issues not replicated (2 accepted, 8 open); 34 LegacyDiff departures, of which 16 are user decisions (10) or data (6) and 18 are open (8 simplifications, 8 not built, 1 assumption, 1 to check).
  - I35 (fuels with no GAINS factor emit nothing) is the same kind of problem as L58 but is still classified as an issue: question to the user.

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.12: the remaining legacy features of the bug / issue split, input rule
- **Task (user):** "Yes and Yes": the listed departures go back to legacy and I35 becomes a bug; I7/LD38 replicate legacy with multiple schemes; I21 on hold ("running ahead of ourselves"); new rule: the main inputs are on MTInputs, policy inputs elsewhere should mostly be bugs, not extensions; I23 agreed; LD5 to classify as bug or issue and apply the rule; LD62 realign with legacy and note as an issue; LD44 OK (already bug L19).
- **Outputs:**
  - `build_v4_12.py`:
    - I23: fuel use raises GDP growth to eps_Y x the income factor, as legacy row 2433 (Mitigation row 14 = (1 + g)^incf - 1; FUELUSE unchanged);
    - I35 -> legacy bug L59: a fuel its GAINS subsector has no factor for takes the nearest GAINS match (LPG: natural gas of the same subsector; food & forestry: construction; else manufacturing); Inputs columns efxs, efxf, efok, efs, eff; names NCCtry, NCSub, NCFuel;
    - LD5 classified as an issue (legacy means VAT on the household part only; firms reclaim it): replicated as I39: new legacy tab OilProductShares (after UNPop), VAT rate of gasoline, diesel, LPG, kerosene x household share (Inputs_prices column osh); legacy bug L60 (VAT payment divided by 1 + the full rate) fixed;
    - LD62: road biofuels as legacy (bioethanol and other biofuels follow gasoline, biodiesel diesel; Balances or EnergyCons; LAMBDA BIOSPLIT) and the feebate CO2 per liter x the fossil share (E2146:E2147); the questionable part noted as replicated issue I40;
    - LD46: methane fee switch per source on Settings rows 47-51 (legacy Manual inputs J196-J200: biomass No, the others Yes) in abatement and revenue (FEEREV now one SUMPRODUCT); the fee path only in policy scenarios (scenario number > 1, legacy row 2238);
    - I7/LD38: existing carbon pricing as legacy: Inputs_ecp looks every code up in its own legacy block of ECP (carbon tax single and fuel rates with the single-price flag, national ETS, EU ETS where EU ETS? = Yes or Both), coverage by data year (blank = 0), tables by ECP sector | fuel; section 1 rows xct.c (data column), xct.p, xets.p (factors); Inputs ecpk, xcp0 replace ctc, etc; the ECP sector of the price fuel as legacy; legacy bugs L61-L65 fixed;
    - LegacyDiff rows 5, 21, 38, 46, 49, 53, 62 updated; version log 4.12.
  - Register: L59-L65 added; I7, I23, I35 removed from the issues; I39, I40 added (replicated, accepted); I21 on hold under the input rule; U11 done.
  - `check_v4_12.py` (full check reference): income factor, L59 fallback, VAT x household share, biofuel split, methane fee switches and policy-only fee. Not run (on request).
  - NORMS 4: the input rule. Docs: PriceProjection (5b rewritten, VAT share), GHG, AirPollutants (rules and new results), Transport, Equations (E17, E18, E30, E38, E69, T17-T18), DataTabs, QuickStart, Sector_Equations_Survey D3, READMEs, TODO; register documents regenerated; working_version refreshed.
- **Checks:**
  - Quick check (full build) PASS: 0 error values; formulas within 100 characters. Against v4.11, 1,692 output codes change, 8 new (xct.c and road biofuel parameter rows), 8 gone (xct.d, xct.p0, xets.d, xets.p0).
  - Egypt effects: fuel use outside power +0.1% in 2025, -0.9% in 2040 (income factor below 1 after 2028), energy CO2 -0.9% in 2040, total GHG -0.7%; local pollutants up from 2022 (NOx +11%, black carbon +8%, PM2.5 +5%, SO2 +5%, CO +1%), combustion CH4 +20% (energy CH4 after calibration +1-2%). Existing carbon pricing, VAT share, biofuels and the methane fee: none for Egypt (no existing pricing, VAT 0 on oil products, no road biofuels, fee 0 in the shipped scenarios).
  - Paste test PASS (groups 4-7 equal their stored results, max relative difference 1.1e-13). Full build 2 min 39 s.
- **Caveats:**
  - The first fallback tried for I35 (same fuel, nearest subsector) gave residential LPG the construction LPG factors (off-road engines, CO 27 kt/PJ) and multiplied residential CO by four; the rule shipped maps LPG to natural gas of the same subsector. The fallback rules are a judgement: check them with the GAINS team.
  - My earlier note to the user said the income factor raises fuel use by 1-2% by 2040; it lowers it (-0.9% in 2040), as the sector survey (D3) had it.
  - Legacy's national ETS rows are stubs in the NoPropData file (`IFNA(0)`), so the national lookup follows legacy's J-column ranges and the regional rows' formulas; the existing carbon pricing has no country to test it on in the shipped data, and the full check's ECP test (`check_ecp`) still writes to the pre-v4.6 ECP layout (TODO).
  - After v4.12: 64 legacy bugs (none replicated); 8 legacy issues not replicated (2 accepted: I6, I20; 6 open: I14, I21 on hold, I24, I25, I26, I31); 29 LegacyDiff departures (10 decisions, 6 data, 8 not built, 4 simplifications, 1 assumption, 2 to check, of which one is kept as legacy).

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.13: residential biomass and additional efficiency gains as legacy
- **Task (user):** "do 1": I24 (residential biomass, legacy switch BiomassNormal) and LD21 (additional policy-induced efficiency gains, MTInputs 242-245); road engineer model not to be fixed now; plan the power engineer features (separate file).
- **Outputs:**
  - `build_v4_13.py`: Settings C53 = MTInputs `BiomassNormal` (scenario 1, name BioNormal): residential biomass has eps_Y = 0 unless Yes (legacy row 5567). New variable row `aef` in every subsector block: (1/(1 + alpha + additional efficiency of the group))^(1 + eps_U), groups as legacy (road vehicles: road, rail, aviation, navigation; residential; industrial: the rest), the three MTInputs inputs read by scenario in section 1 (LAMBDA AEEIFACTOR); FUELUSE takes it; Inputs column aeef replaced by aeg. LegacyDiff 21 same as legacy, 62 corrected to "Not yet" (the elasticity road branch of the biofuels is not as legacy; parked with the road model). Version log 4.13.
  - Register: legacy bug L66 (other energy use fossil rows without the additional efficiency); I24 removed. Full check reference updated (not run). Docs: Equations E69, Sector_Equations_Survey D4/D7, TODO, READMEs.
- **Checks:** quick check (full build) PASS: 294 new codes (the aef rows and three inputs), 193 change, all through residential biomass (Egypt: -47 ktoe in 2030, -103 in 2040; PM2.5 -1.5 kt in 2040; CO2 unchanged, biomass EF 0). Paste test PASS. Full build 2 min 53 s.
- **Caveats:**
  - The additional efficiency inputs are 0 in every shipped scenario, so the new rows equal the old AEEI factor; only the full check reference (not run) exercises non-zero values.
  - Power demand still takes AdditionalEfficiencyPower (MTInputs 242) from scenario 1, like the other power settings: in the power plan.
  - BiomassNormal is read from scenario 1 (a structural assumption, like BalancesOrConsumption); a scenario that changes it has no effect.
  - In v4.12 I had labelled LegacyDiff 62 "same as legacy"; only the engineer branch is.

## 2026-10-18 - Plan of the power engineer features (no model change)
- **Task (user):** "plan out the features for Power engineer" (instead of fixing the road engineer model).
- **Outputs:** `excel_ai/mitigation/PowerFeatures_Plan_v4_13.md`: 14 features with their legacy rows and inputs, class (bug, legacy feature, departure), Egypt effect and size; five releases P1-P5; six decisions for the user. TODO and README point to it.
- **Checks:** from a read-only survey of the legacy power block (rows 2731-4301) by a subagent; the claims the plan leans on most (next-year demand row 4027 = this year's demand; MaximumGasCF ignored) re-checked in the legacy formula dump.
- **Caveats:** not verified: the intended source of legacy's demand feebate (blank row 2255), the all-manual lag, the GoalSeekCoal data, El Dabaa and retirement data for Egypt. I8 is reclassified in the plan as a likely legacy bug; the register still lists it as a replicated issue until the user decides.

## 2026-10-18 - Power engineer plan: user decisions recorded (no model change)
- **Task (user):** decisions on the plan: next-year demand is a bug; every MTInputs power input per scenario; manual capacity needed (from 'Manual inputs', which now comes in as the second input source; no Egypt data); no demand-side power feebate (covered by the rebating of power prices); no elasticity power model; coal implicit cost with a switch defaulting to legacy. "Define the plan, but do NOT do it."
- **Outputs:** `PowerFeatures_Plan_v4_13.md` sections 2-4 (decisions, releases P1-P5, points to settle when building); TODO item updated. Nothing built.
- **Caveats:** the register still lists I8 as a replicated issue; it becomes a legacy bug when P1 is built. Per-scenario technical power inputs (P2) run against the shared scenario-1 baseline (plan section 4).

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.14: power capacity for next year's demand (legacy bug L67)
- **Task (user):** "This is definitely a bug. Please fix it" (I8: new capacity sized for this year's demand although it comes online next year).
- **Outputs:**
  - `build_v4_14.py`: investment need = next year's required generation - capacity after retirements (2041: this year's, the spacer column being blank); LAMBDA NEEDNEXT; LegacyDiff 23 and version log 4.14.
  - `power_model_ref_v4_14.py`: fix 'nextyear' (block H computed for the next year before block K7); with no fixes it still reproduces legacy.
  - Register: L67 added (was I8, removed from the issues); U9 done. Docs: Equations E63, PowerFeatures plan (P1 item done), TODO, READMEs; register documents regenerated.
- **Checks:** quick check (full build) PASS, no circular reference (next year's demand reads this year's and last year's power prices only); LAMBDA test group equal to group 2. Against v4.13: 1,774 codes change. Egypt scenario 1: investment moves one year earlier (the 2024 rebound after the 2023 shock is bought in 2023), total capacity +4% in 2030 and 2040, gas generation -2% (2030) and -4% (2040), power CO2 -1% and -4%. Reference with legacy inputs: capacity +3%, gas -3%, wind and solar +4-6%. Paste test PASS. Full build 2 min 43 s.
- **Caveats:**
  - Base year: 2023 demand is below 2022 (shock -20.8%), so no investment is needed in 2022 and 2023 capacity is 2.7% lower than before; power CO2 2023 is 2% higher.
  - 2041 has no next year in the model: it sizes on its own demand, as legacy did every year.

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.15: the calls replicated as legacy (LD37, LD55, LD56), I21, I31; full check repaired
- **Task (user, overnight):** "On the calls, please replicate legacy for now, noting issues. On I21 just go with the MTInputs auctioned share. We'll add benchmarks later. I31 use legacy as default." Also "do the repairs" (the full check).
- **Inputs:** read-only survey of the legacy revenue, GDP, multiplier, average-price and ETS blocks (subagent; rows checked in the legacy formula dump; legacy GDP row 14605 reproduced to 5e-18 from cached values); the legacy Multipliers tab (`data/legacy_Multipliers_cells.csv`) and Manual inputs J260:U268.
- **Outputs:**
  - `build_v4_15.py`: ETS benchmarks = 1 - MTInputs D_ETSAuctStart / D_ETSAuctTarget (rows 90-91, per scenario; LAMBDA FREESHARE; the typed Constants rows gone; I21). Section 2 memo: pav.leg, pav.lidx, pav.idx per fuel and the legacy weights of coal and gas (pavl.qr, qi, qp, pp; LAMBDAs SUBQTY, SUMOF, PWFUELPRICE, LEGAVG, PICKINDEX); Settings C54 PavMethod (Legacy* default); MTOutputs mit.pav.idx (I31). Per-pair rows rex (new excise revenue) and rvt (VAT revenue); block 12e total revenue by policy, legacy rows 8016-8027, with a check row (LD37). GDP: fis.rev = rnet + rnew (total revenue, as legacy rev.new.usd), impulse = change in USD over this year's GDP from GDPStartYear (MTInputs 236; LAMBDA IMPULSE) (LD55). Multipliers: sources est (country tables of the legacy Multipliers tab, exact match, income group as fallback; CIT and WAGE income group) and man (new sheet **Manual inputs**, legacy addresses J261:U268), both with the income group's spread; Settings B55:C58 source table (LD56). LegacyDiff 7, 37, 55, 56, 58 updated; version log 4.15.
  - Register: legacy bugs L68-L73, L75-L80 (L74 kept free); issues I41-I47; I21 and I31 replicated; distribution bugs D1-D8 and issues DI1-DI10 (from Distribution_Method) now in the register. `make_legacy_fixes`: priorities and fixes of L68-L80.
  - `check_v4_15.py`: existing carbon pricing recomputed from the legacy ECP cells (`ecp_tables`, as Inputs_ecp); `check_ecp` writes its test data into the legacy ECP blocks (with an EU coverage case); LAMBDA test group 3, the spacer test cells and 5b rows without a LAMBDA recognised in the formula-length, shipped-file, uniformity, spacer and beige tests; I21, LD37 (rex, rvt, 12e explicitly), LD55, LD56 (est, man; test scenarios 7 and 8 use Manual and Estimated) and I31 (legacy averages from the cells) recomputed. `check_quick_v4_15.py`: QC_DUMP env var writes the new output codes.
  - New: `make_bugfix_book_v4_15.py` -> `CPAT_BugFix_Procedure_and_Register_v4_15.docx` (procedure + every bug by type with the cell plans + issues + reference table). Docs: GDP, ETS, PriceProjection (section 7), ResultsSections (12e) method notes; TODO; READMEs; register documents regenerated; working_version and the top-folder workbook updated.
- **Checks:** quick check (full build) PASS: 690 new codes, 1,205 change; scenario 1 only in fis.rev and fis.ref (redefined); scenario 2 through the GDP feedback: fiscal space 2030 0.75% of GDP (was 0.55%), GDP effect 2040 +0.39% (was +0.25%). 12e: total = rtot exactly; Egypt 2030 carbon tax 4.2 bn USD, existing taxes and subsidies -10.3 bn, electricity subsidy gap -10.0 bn. Reported gas price index 2030 1.294 (legacy weights) against 1.198 Laspeyres. Paste test PASS. Full check: run started on the v4.15 build in a scratch copy (result in the next entry).
- **Caveats:**
  - I43 (revenue-use shares 0 before CPIntro) and I47 (methane fee left out of the fiscal space, GHGYear circularity) are not replicated; transport revenues and renewable subsidies are 0 rows in 12e (I46: road engineer and power features parked); producer subsidies of oil, coal and gas come with v4.16.
  - The legacy GDP benchmark (policy rows 14584-14607) is from a run with a different carbon price path (to about 175 $/t in 2041), so it is not compared.
  - Benchmarks by sector (output-based) are deferred by the user; one auctioned share applies to every sector group, as legacy.
  - The register is keyed to the 456 legacy file; the new 459 file (some bugs fixed) is not reconciled yet (TODO).

## 2026-10-18 - CPAT-AI-Mitigation-MVP v4.16: phase-outs, producer subsidies and regulations as separate policy lines (LD18, LD19, LD9)
- **Task (user, overnight):** "For subsidy and price control phase out and producer subsidies, make sure these are separate policy lines, not meshed with the pre-policy price build up. They will need to be by sector and fuel. Add in regulations as shadow prices, add producer subsidies."
- **Inputs:** legacy Mitigation rows 2205-2262 (phase-out factors), 2547-2600 (producer and consumer subsidy rows), 222-262 (scenario table), 2371 (regulation share); MTInputs rows 214-251.
- **Outputs:**
  - `build_v4_16.py`: section 1 lines by sector and fuel: phase-out switches and factors (po.*, pof.ps/cs/pc), consumer subsidy factors csi/csf and price-control factors pci/pcf by price code, producer subsidy factors psi/psf and producer subsidies pros by fuel (IMF data to the last historical year, then held) (LD18, LD19). Price blocks: txo split into a fixed part txfx (pass-through x txo of the last historical year) and a floating part txfl; the reform wedges pcsw = -(1-csf) x MIN(txfx,0) and ppcw = -(1-pcf) x txfl are separate lines after the price before new taxes, not in the pre-policy build-up. Sectors: csw, pcw (the block's wedges) in the price with policies; revenue rsr (reform) by pair, rpsu (producer subsidies, negative) in the totals, 12e and the fiscal space. Regulations: the legacy scenario table on Mapping (ScnName, ScnExpl, ScnAdj, ScnCov), main-scenario row scn, explicit pricing cp.exp and cpx, coverage regc and shadow price reg by sector, added to the shadow prices; feebate shadow price x SPPEffAdjFeebates (LD9). LAMBDAs SCNROW, EXPLICIT, REGADJ, REGCOVER, REGSHADOW, PHASEON, PCON, PICKSCEN, PHASESHARE, PHASEOUT, INCLFACTOR, PRODSUB, SUBREFORM, PCREFORM, BLOCKWEDGE, FIXEDPART. LegacyDiff 9, 18 Same; 19 Simplification. Transport feebates read reg.rod (prototype bug M13).
  - Register: legacy bugs L81-L89 (L87 high: regulations never act in legacy), issues I48 (replicated: the price-control factor uses the consumer shares, as legacy), I49; make_legacy_fixes priorities and fixes; bugfix book with L83, L84, L88 under power.
  - Fixes found on the way: `fis.rev` now adds its parts (rnet + rnew + rsr + rpsu): the v4.15 form rtot - rmf referenced the methane fee and LibreOffice reported a circular reference on a full recalculation (the shipped StoredResults of v4.16's first build were blank after 2028 in power; caught by the paste test). `rev.chk` back to rtx, rsub, rnew (100-character limit; rsr is in rfu.chk). The full check's soffice conversion uses its own profile.
  - Docs: PriceProjection 6b, Scenarios 2b, GDP method; register documents, bugfix book, Documentation docx, Formulas regenerated; READMEs, working_version, top-folder workbook.
- **Checks:** quick check (full build) PASS: 0 shared output codes change (every new line is off or 0 in the shipped scenarios: Egypt producer subsidies are 0 in the data, the phase-out switches are No, the main scenario sets no regulation); 1,246 new codes, 14 gone (the old zero rows reg, shps, ssc.adj). Paste test PASS (stored results equal the pasted groups to 6e-14). Full check: running on the v4.16 build in a scratch copy (result with v5.0).
- **Caveats:**
  - Electricity phase-outs are not modelled (rsr of power is 0); power stays parked as the user asked.
  - I48 is replicated (price-control factor with the consumer shares); I49 not replicated (see register).
  - The Python power reference of the full check lacks the v4.10 fixes L52-L56 (actual capacity factors, country parameters), so its power and revenue rows will differ from the workbook until it reads the workbook's data step.

## 2026-10-18 - CPAT-AI-Mitigation-MVP v5.0: consolidated release (user: "bump everything to v5.0 when done. Make sure everything is consistent.")
- **Task (user):** "Also bump everything to v5.0 when done. Make sure everything is consistent." and "do a full rebuild at the end".
- **Inputs:** v4.16 (previous entry).
- **Outputs:** every versioned file renamed v4_16 -> v5_0 / v4.16 -> v5.0 (builder, checks, references, method notes, register scripts, documents; v4.16 copies in `Old/`); VERSION 5.0 and a version-log row; the title lines of the method notes and references read v5.0 (surveys and plans keep the version they were written for); `working_version/` and the top-folder workbook at v5.0; root and `excel_ai` READMEs at v5.0 (the root README said v4.6). New legacy file noted in the READMEs: `CPAT 1.0pre_459_NoPropData.xlsb` (a few bugs fixed by the CPAT team, one transport bug not), `CPATMasterProcessesCodesAndDefaults.xlsx` (master list of codes; may be inaccurate; alignment planned) and `Tracking issues.xlsx`; the only data-table subfolder there, `CPAT_LegacyData_dummy_csv/`, is our own dummy export (coded/legacy_export), not data of the 459 file. All documents regenerated, among them `CPAT_BugFix_Procedure_and_Register_v5_0.docx` (procedure; bugs by type: engineer power, engineer transport, other mitigation, distribution, prototype; issues; appendix table of 199 codes in code order). `check_v5_0.py`: optional `CHECK_CACHE` dir reuses LibreOffice results of identical files; the price-block rows weighted from the sheet (rpn, pnq, pctx, ...) are left to the price-block test instead of the pairwise comparison (the comparison raised a KeyError on them, also in v4.15).
- **Checks:** full rebuild (FORCE=1) then quick check PASS: 12,196 output codes, 0 change against v4.16 (same model). Paste test PASS (stored results equal the pasted groups to 6e-14). Full check: running on the v5.0 build (result in the next entry).
- **Caveats:** the register and the MVP are keyed to the 456 legacy file; the 459 file is not reconciled yet (TODO).

## 2026-10-18 - Team tracker kept with our codes (user: "I put a bug tracker in legacy folder. You could edit that by adding extra rows and extra columns. Continue to use our codes")
- **Task (user):** the bug list Word document and the other documents need a full update; the tracker `legacy/workbooks/Tracking issues.xlsx` may be edited (rows, columns), with our codes.
- **Inputs:** the tracker (sheet BUGSandISSUES = our register export of v3.18, not edited by the team; the team's sheets CPAT_issues, Mit+Disn_DeepDive, MT_issues, Slicer_issues); a mapping of the 93 team items to our codes (subagent, checked against the legacy formulas where cells were cited).
- **Outputs:** `update_tracker_v5_1.py` (run at every release; idempotent): BUGSandISSUES refreshed from the register, 216 rows (new codes appended; retired codes kept and marked with where they went, e.g. I8 -> L67), columns L-R added (type, code group, version settled, cell-level plan, status in the 459 file, related team items, updated); the team sheets keep their content and get "CPAT-AI code(s)" and "CPAT-AI note" (93 items mapped; DeepDive's second table keyed "Dist n", its general concerns "General n"). Mapping kept with the register: `mitigation/data/tracker_mapping.json`. New register codes from the team items: L95 (power-demand efficiency term on the net-exports row 3719), L96 (mislabelled parameter and fuel rows), L97 (unused iron & steel memo rows), D9 (rural rows labelled Urban; oil vs oop) — all Low, no value effect (L90-L94 are reserved for the residential leakage work of v5.1). NORMS: the tracker is editable; the 459 file and the master code list are read-only. Register documents regenerated (Word bug list, register docx, LegacyBugFixes).
- **Checks:** the tracker update run twice on a copy (same result, no duplicated columns); register modules import; documents regenerate.
- **Caveats:** the mapping of CPAT_issues is by substance; 21 in-scope items have no code (16 were fixed in legacy before 456). CPAT_issues 48 (transport impacts with transport exempted, High) and the MTInputs 182-183 units are TODO leads. The tracker will be refreshed again at the v5.1 release (new codes L90-L94).

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.1: residential LPG/kerosene exemption and residential leakage to biomass
- **Task (user):** "After all this is done, consider doing next: the residential exemption and leakage rows; ..." (first of four items).
- **Inputs:** read-only survey of legacy rows 1782-1795, 2257-2288, 5540-5593 and MTInputs 18, 49-51, 268, 298-301, 312-313, 325-326 (spec in the session notes; NoPropData IFNA stubs identified: the "hard 0 start" of L48 is not legacy logic).
- **Outputs:**
  - `build_v5_1.py`: per scenario, Section-1 row AlwaysExemptResLPGKer (MTInputs 268) with factor rows exf.all / exf.res, Inputs column exg; ctxnew, ets and ntx of residential LPG and kerosene multiply by the factor (LAMBDAs CARBONTAX, ETSCOST, NEWEXCISE gain exempt_fac; shadow price kept) (I50, replicated). Section 6b "Residential leakage to biomass" (rows lkt, lkp, lkd, lkb, lkz, lkc, lkcb, lks; LAMBDAs EXEMPTFACTOR, LEAKTAX, LEAKSHARE, LEAKCHANGE, LEAKBIOMASS, LEAKCUM): only the most-used cooking fuel (WHOCooking) leaks, share MIN(r^(sigma e_b/e_m/lag) - 1, 1), fossil change -F_prev e_m p (I51, replicated as legacy; user decision open), biomass + useful-energy equivalent (L90 fixed), exempt fuels do not leak (L91), kerosene with its own rows (L45 fixed); fuel use = elasticity model + cumulative change (ROADSWITCH gains the leak term). Settings C59 BioLeak (MTInputs 325, global), C61:C64 cookstove efficiencies (MTInputs 298-301), C65 CookFuel; ResBioSubst = Elasticities C131; constant ResSubstLag 1. LegacyDiff 65, 66 (Same), 67 (exemption phase-out of uncovered fuels and sectors, D8 split: not yet). Docs: Equations (4a), Sector survey (D8, D9, D16), PriceProjection 5.
  - `check_v5_1.py`: exemption and leakage recomputed (_recompute_once), 6b in uniformity and compare, exemption and leakage test scenarios with an energy-balance invariant; aef recomputed (compare used to crash); compare reports missing series.
  - Register: L45 fixed; L48 text corrected; new L90-L94 (L90, L91 fixed; L92-L94 not built), I50, I51. All documents, the Word bug list and the team tracker regenerated (224 rows). TODO item (1) ticked; MTInputs appendix plan (item 4) written.
- **Checks:** quick check (full build) PASS: 12,196 shared codes, 0 change against v5.0, 42 new. Paste test PASS (5.7e-14). On-switch tests (scratch copies): leakage on, $20 scenario, 2027: 1.55% of residential LPG leaks, LPG -25.4 ktoe, biomass +71.0 ktoe (useful energy conserved to 5e-15), CO2 -0.07 Mt, workbook = Python to 6e-15, LAMBDA group = group 2; exemption on: residential LPG/kerosene price = scenario 1, their new-policy revenue 0 (residential LPG 144 USD m in 2027), CO2 +0.76 Mt; both on: exempt fuels do not leak. Full check: sections 0-3 no FAIL; section 4 residential rows and 6b match; the whole-group comparisons still FAIL on the pre-existing power rows (reference lacks L52-L56) and transport 5b 2041 (about 9%) — the repair of the full check is in progress on a scratch copy.
- **Caveats:** both switches off by default (Egypt unchanged). The D8 initially-exempt demand split (ExemptMostCook in Mitigation) and the ExemptPhaseout phase-out are not built (LegacyDiff 67). The full check does not yet pass as a whole (see above).

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.2: the whole legacy 'Manual inputs' tab, inputs held elsewhere remapped onto it
- **Task (user):** "bringing in the whole of the Manual inputs from Legacy and remapping what is elsewhere into there" (third of four items; done before the power features because the power plan's P3 is this tab and the power reference is being repaired).
- **Inputs:** read-only survey of the legacy tab (17 blocks, rows 5-378; who reads each, switches), `data/legacy_ManualInputs_cells.csv` (2,874 legacy cells, new `manual` mode of `extract_legacy_tables_v5_2.py`).
- **Outputs:**
  - `build_v5_2.py`: sheet 'Manual inputs' holds every legacy cell at its legacy address (paste-compatible from row 3); block bars with a note of what reads each block or "Not read: feature not built"; legacy formulas within the sheet kept, those reading other legacy tabs replaced by the MVP equivalent or typed as the legacy default.
  - Remapped (values unchanged): ETS goal seek E10:E12 (names ETSMaxIterations, ETSStartFreshContinue, ETSErrorTolerance; read by the VBA SolveETS and ets_goalseek; MVP values 20 / Continue / 0.005 kept, legacy 30 / Continue / 0.001 noted; CheckBatch checks 15 lookups); price controls J167:J180 (Inputs_prices pcc by code; constant PassManual removed); methane fee scope J196:J200 (names MFeeBio..MFeeWst; Settings C47:C51 show them); manual international prices J221:AF225 (Inputs_pint Manual rows from 2026); fuel economy of new BEVs J375:AC377 (section 5b trfen; TransportPaths rows dropped); non-energy GHG elasticities K325:M327 (Constants ghg.el removed; L102 fixed); manual SCC row 237 (scc.man; names SCCManVal, SCCManYear; L103 fixed).
  - `check_v5_2.py` reads the new cells (independent recomputation from the typed values). LegacyDiff rows 68-73; VersionLog 5.2. Docs: DataTabs (Manual inputs section), QuickStart (where inputs live), ETS, PriceProjection, GHG, Transport methods, ResultsSections (scc.man), plans marked.
  - Register: L98-L106 (L102, L103, L106 fixed; L98, L99, L100, L101, L104, L105 not applicable in the MVP), I52, I53 (open, user decisions when the features are built). All documents, the Word bug list and the team tracker (236 rows) regenerated; TODO: Manual inputs ticked, electricity price controls (J178:J179, possibly dead in legacy) added as a lead.
- **Checks:** quick check (full build) PASS: 12,238 shared codes, 2 change: scc.all.man (scenarios 1-2; the manual SCC now from 'Manual inputs' row 237, 50 $/t in 2025 + 4% a year, instead of the legacy row-17683 path; the shipped scenarios use the Target source, so no result changes). Paste test PASS (5.7e-14). Remap tests on scratch copies (each value changed and restored): J167 0.8 -> 0.5 moves coal-power pcc to 0.5 only; J196 No -> Yes with a methane fee turns the biomass CH4 abatement on (2030 0 -> 0.47); a doubled manual oil price doubles gp oil 2028 only; a BEV fuel economy change moves trfen; K327 0.15 -> 0.30 moves agriculture N2O 2035 28.70 -> 30.28. ETS settings: the VBA in LibreOffice matches the Python goal seek (2 iterations, StartFresh). Full check: the touched sections match; its pre-existing FAILs remain (power reference, transport 5b 2041, CheckBatch stored ID 5 = the ETS goal seek of definition 5 against the build's emulation), repair in progress.
- **Caveats:** blocks of features not built (process emissions/CBAM, manual domestic prices, additional excise, other methane inputs, Distribution pass-through, manual GDP, PM2.5 apportionment, manual elasticities, manual non-energy effort, manual power capacity) are placed but not read; manual power capacity comes with the power features.

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.3: full check repaired and passing; MacroCheck at the bottom of its tab
- **Task:** repair the full check (overnight request "do the repairs"; task #25) and run it; user: "I think the macros table belongs at the bottom of its tab - there's lots of white space below it!"
- **Inputs:** the v5.0 full check run in a scratch copy (subagent), its diffs ported onto v5.2/v5.3.
- **Outputs:**
  - `power_model_ref_v5_3.py`: `mvp_data()`, an independent Python data step with the v4.10 fixes (L52 country parameters, L53 actual capacity factors within the CFOverride bounds, L54 hydro start, L55 country block), from `legacy_Power_cells.csv` and `legacy_Balances.csv`; `engine()` takes it (`inp['data']`); the legacy test is unchanged (9.6e-14).
  - `check_v5_3.py`: power inputs from `power_data()`; missing recomputations added (aef, S15 apfd/ap food rows, WEO 2021 growth for the road model, trade balance with L51 fixed); stale expectations updated (planned retirement on Inputs_ptech/ppath, previous version found in Old/, rpb label, bold rows by design, phase-out rows in scenario 4 = 1, scenario 7 at its own GDP path, no legacy average for jfu/bio, CheckBatch lookups 15); compare robust (missing series reported); diagnostics (Lambdas texts naming merged sheets, macro differences per stored ID); LibreOffice timeout 3600 s (CHECK_LO_TIMEOUT); optional CHECK_CACHE. Judgement call (for the user to review): the carbon-price direction test now checks the VRE share of the investment logit (never lower) and power CO2; the VRE generation share is a memo (with the fixed power data, $20 lowers it in 2041 from 0.394 to 0.387 while power CO2 falls: less new investment, existing gas runs more; workbook = reference).
  - `build_v5_3.py`: prototype bug M14 fixed (21 LAMBDA-library texts of the power pollutant rows named the merged-away sheet Inputs_power; merge_tabs re-points the Lambdas texts of an appended block); the Check tab now holds Variables, Lambdas, then MacroCheck last (user request; the VBA report row is set from the tab map: 2015); VersionLog 5.3.
  - `CPATScenarios_v5_3.bas` CheckBatch and the check's macro test: new-ETS definitions (stored by the build at the fast estimate, no goal seek, user rule 2026-10-17) are reported as a memo, not compared.
  - Register: M14; I30 extended (goal seek: worst gap 0.0265 after 20 iterations, prices oscillating; the macro in LibreOffice reaches 2,132 $/t in 2030 and still misses the cap). The v4.0 deck files moved to `presentation/Old/` (content of v4.0; the hand-over copy stays at the top of `excel_ai/`).
- **Checks:** quick check (full build) PASS, 0 change on 12,238 codes against v5.2; paste test PASS. Full check (`check_report_v5.3.md`, assembled from three runs: the one-process run reached its time limit in 5b): every section PASS — 0-4b, 5 scenario tests, 5a leakage, 5c ECP, 6-11d, 12 (definitions, VBA, stored results, ScenarioCompare, macro RunAll), 13 first-run test (Result PASS, 15 lookups, 5.7e-14; negative test OK) and 14 consistency — except **5b ETS goal seek (I30)**.
- **Caveats:** the goal seek of a new ETS does not converge (I30): a user running RunAllScenarios on definition 5 gets oscillating prices. The full check needs about 2.5 hours and more memory than one process gets with other LibreOffice jobs running; run it in sections when the machine is busy.

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.4: power features P1, P2, P4 (plan PowerFeatures)
- **Task (user):** "consider doing next: ... the power features in the plan" (second item; decisions of 2026-10-18 in PowerFeatures_Plan section 2).
- **Inputs:** the plan, the read-only legacy power survey, the v5.3 Python power reference with the MVP data step.
- **Outputs:**
  - P1: final deficit to gas (Settings C45 PwDeficitGas, default No as legacy's typed E4248; row dgas); MaximumGasCF caps gas (row gmx; gas no longer borrows the coal cap; same default 0.9); LongTermStorageFor100pcVRE scales the long-term storage (rows stm, ltu).
  - P2: every MTInputs power input read per scenario: 62 Section-1 rows "Power sector settings" and sub-table A0 in section 3 (cfu, nuu, wac, dlf, kwh, cap0, invs, perm, start, rate, rr, rns, wsel, wfx, dlfr, scat, scv, erf, spot, ctf, ...); the power formulas re-pointed from scenario-1 values; Inputs_pset kept as the scenario-1 view with a note. EarlyRetirementInBaseline now applies in scenario 1 only, as legacy F3993 (no effect at the default).
  - P4: PPAs (ppa, glg, ppr; Yes or Yes*, I54); renewable subsidies (rnsp, rns, prrns; own start year MTInputs row 482 RenSubsidyAddStartYear, L107; revenue by type, L108; nominal used as real, I55); power revenue rebate (rbs, rreb; without the VAT never collected, L110); electricity excise (exs carbon-based with the base-year grid intensity, I56; manual excise from 'Manual inputs' J161:AF162 when AdditionalExcise is on; pex, rpex, rexs, rexm; revenue = the excise in the price, L111). Capex decline Low / Vhigh fall back to the older series (L109). 30 new LAMBDAs; Python reference `engine()` with every new input; check section 5d (power features, test groups 1-9 vs Python, all OK).
  - Register: L107-L111, I54-I58, and I59 (electricity fuel price reform not applied to electricity prices) and I60 (no end-user price floor at MinPostSubsidyPowerPrice), queued for v5.5. LegacyDiff 21, 28, 34 updated, 74-79 added. Documents, the Word bug list and the team tracker (250 rows) regenerated; READMEs, TODO.
- **Checks:** quick check (full build) PASS: 12,238 shared codes, 0 change (max 1.5e-10), 468 new. Paste test PASS (5.7e-14). Full check sections (`check_report_v5.4.md`): 0, 2, 3, 4 (1.24e-11), 4b, 5, 5d, 7, 8, 8b, 9, 10, 11b, 11c, 12a, 14 PASS. Test groups: MaximumGasCF 0.6 lowers the gas maximum 49,630 -> 32,660 MWy; PPAs share 0.5 phases out 2031-2035, coal generation 819 vs 89.6 MWy; renewable subsidies raise wind + solar capacity 2041 52,754 -> 53,085 MW (cost -1,777 USD m); rebate brings the residential price back to 0.0571 $/kWh (rebate -1,890 USD m); electricity excise 0.0076 $/kWh carbon-based, revenue 1,586 + 2,113 (manual) USD m; deficit to gas 1,458-1,761 MW a year with tight scale-up limits.
- **Caveats:** P3 (manual capacity and investment, El Dabaa possible through 'Manual inputs' 342-371) and P5 (coal implicit cost, memo tables) next (v5.5), with I59 and I60. User to confirm: I58 (Yes* accepted for PowerRebates, RenewableSubsidyHydro, AdditionalExcise) and the L109 fallback.

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.5: cell-level fix plans for the 15 engineer-power bugs (register and documents; model unchanged)
- **Task (user):** "add as a todo to generate cell plans for the bugs starting engineer power", then "OK add the 15 engineer cell plans".
- **Inputs:** the legacy .xlsb (read-only), the register and fixes (v5.4), the MVP fixes as reference.
- **Outputs:** `legacy_bugfix_plans/data/fixes_power_engineer.json` + 15 plans (L52-L56, L67, L83, L84, L88, L95, L107-L111; 14 "fix", L107 "needs input row"; the power document now 27 bugs, 57 entries), rendered `Legacy_CPAT_BugFix_PowerEngineer.docx` and PDF; tools: `dec.py` decodes formulas straight from the .xlsb (needs pyxlsb2), `chkplans.py` checks every plan against it, `gen_pow2.py`, `h.py`, `dumpo.py`, `arr.py`; `pol.py` (array cells) and `render.js` (multi-line formulas, other statuses) fixed. Register: L87 and L50 texts corrected from the .xlsb; new legacy bug L112 (policy copies of the shadow-price rows 8708-8719 keep $D$2369 and L$2375: the regulation term of the policy run reads the baseline carbon price; to confirm in Excel). TODO: power plans ticked; new item on formula texts truncated by the LibreOffice conversion. VersionLog 5.5; documents, Word bug list (with the new plans) and team tracker (251 rows) regenerated.
- **Checks:** `chkplans.py` (run independently): 57 plan entries, 0 differ from the .xlsb. Quick check (full build) PASS, 0 change on 12,706 codes; paste test PASS.
- **Caveats:** **the LibreOffice .xlsx conversion of the legacy file truncates 23,115 Mitigation formula texts** (`_xlfn.IFNA`, `XLOOKUP` first argument dropped, `LET` garbled): the plans L48 and L50 were built from such texts and must be redone; register entries and surveys quoting such cells from the .xlsx are to be audited (TODO). Nothing recalculated in Excel; effects from the MVP and the register.
## 2026-10-19 - Legacy CPAT bug-fix plans: engineer power, batch 2 (`legacy_bugfix_plans/`) - superseded by the v5.5 power plan on main; files removed in the merge

- **What:** cell-level fix plans for the 15 engineer-power bugs of the v5.4 register that had none: L52, L53, L54, L55, L56, L67, L83, L84, L88, L95, L107, L108, L109, L110, L111 (37 cells). `Legacy_CPAT_BugFix_PowerEngineer_2.docx` (PDF in `pdf/`), `data/fixes_power_engineer_2.json`, generator `tools/gen_pow54.py`. Keyed to `CPAT 1.0pre_456_NoPropData.xlsb` (formulas read from a LibreOffice conversion, defined names recovered from the .xlsb).
- **Choices to confirm:** L52 uses the test of the fossil rows (country value if > 0, else world); L55 searches Power!A112:A294 (country block) first; L56 sends a country without CoC data to the default WACC 0.075 (NA() fallback, read through Mitigation's IFERROR) instead of Sri Lanka; L88 power reads rows 2377/2380 (feebate + regulation) and adds the regulation term to oil; L108 also fixes row 7900 (other renewables multiplied biomass generation) and adds a biomass row 7901; L110 books the rebate before VAT in row 3663 (prices unchanged); L111 counts the excise in the price (change since 2024 x pass-through in projection years); L107 needs a new MTInputs input row; L109 fallback as the MVP (older series, else Medium).
- **Caveats:** nothing recalculated (Excel or Python); effects from the register. The Word register document is not regenerated. Next: other mitigation (45 bugs), then distribution (9).

## 2026-10-19 - Legacy CPAT bug-fix plans: other mitigation batch 2 and distribution (`legacy_bugfix_plans/`)

- **What:** cell-level plans for the remaining 54 register bugs: 45 other-mitigation (`Legacy_CPAT_BugFix_OtherMitigation_2.docx`, `data/fixes_other_mitigation_2.json`, 152 cells) and D1-D9 (`Legacy_CPAT_BugFix_Distribution.docx`, `data/fixes_distribution.json`, 54 cells). Every legacy bug of the register now has a plan. Generators `tools/gen_A.py`-`gen_E.py` (made by five parallel agents on one shared dump), helpers `tools/q.py`, `tools/dec.py`.
- **Found:** the LibreOffice .xlsx conversion turns formulas with IFNA into constants; `dec.py` reads the .xlsb directly; all 144 Mitigation "formula now" cells of the batch match the .xlsb. Consequences: L92 does not reproduce; the old plan L48 is a no-op on L5564:L5570; L86 = extend the names _manual_codes/_manual_prices (as L100). New unregistered findings (L2555, rows 5587/5588, Elasticities H53/H54, Multipliers D44): see the README.
- **To confirm (MVP choice taken):** L64 (C1717 = "all"?), L79 (covered emission share instead of new subsector price rows), L75 (mapping of the revenue report rows), L87 (feebate part *$F$90), L89 (services stay on the residential price), L94 (single phase-in rule), L96, L97, L103 (typed SCC path lost unless copied to Manual inputs), L104 (delete the name), D1 (decile 1), D3 (drop the ASPIRE test vs. swap the flag).
- **Caveats:** nothing recalculated; effects from the register. NoPropData stubs (GAINS factors, rows 8280-8287) prevent checking L58, L59 and L68 in this file.

## 2026-10-19 - Register: issues I61-I63; team tracker item 48 done

- **What:** user request: the parked engineer road model follow-ups (I61), the partial-adjustment fuel-use model (I62, was upgrade U12) and demand on real local-currency prices (I63) registered as Major, Open issues (legacy side: replicated). Team tracker lead item 48 marked done (user). `ISSUES.md` and `Replicated_v5_5.md` regenerated (`make_replication_lists_v5_5.py`).
- LD47 (GAINS combustion factor paths) and LD3 (blank VAT cells): registered as Major, Open data issues I64 and I65 (user decision; not bugs under NORMS section 0, as no legacy formula is wrong); next step: data requests. Legacy side "not replicated": the MVP's fills are kept (as before). Word register, deck and team tracker not regenerated.

## 2026-10-19 - User decisions on the open choices (bug-fix plans and issues)

- **Fix plans** (`legacy_bugfix_plans/`, documents re-rendered): L64 coverage rows only (C1717 stays); L79 covered emission share (subsector prices = upgrade); L87 feebate part kept, apply with L112; L89 road only (services stay on the residential price); L94 the rule of rows 2259-2265; L75 mapping kept, row 17162 left empty with a note, ask the CPAT team; L69 check in Excel when applying; L86/L100 accepted incl. the manual electricity price rows; L96 relabel in place; L97 memo rows kept, M5667 = (M2446) (no clearing); L103 copy the typed SCC path into Manual inputs J237:AC237 first; L104 delete the name; D1 decile 1 capped too (Q2562 = MIN($Q$2552,Q2560)); D3 test $I$214 (current spending's flag) instead of $I$213; L109 fallback accepted, ask the CPAT team for the series.
- **Register:** I58 reclassified as legacy bug L113 (fixed in the MVP since v5.4); I55 reclassified as legacy bug L114 (the MVP still copies it: BUGS_REPLICATED, to fix in v5.6); I51 and I56 accepted as legacy; I52 and I53 replicate legacy when built; I64 and I65 MVP fills kept. Lists regenerated. The Word register document and team tracker are not regenerated.

## 2026-10-19 - Bug-fix plans: L48 and L50 redone, L112 and L115-L117 planned, register documents regenerated

- **What:** L48 and L50 redone from the .xlsb (`legacy_bugfix_plans/tools/gen_redo.py`): L48 = income factor in M5568:M5570 and the starred-Yes test in L5546:L5547 only (the exemption split L5564:L5570 already exists; the old start-row edits are dropped); L50 = codes and WEO -> WEO_upd, legacy's carry-forward kept. Audit: every plan's "formula now" (362 cells, all sheets) checked against the .xlsb; only L48 and L50 differed. Register: L48 retitled; L92 marked not reproduced (I1784 reads MTInputs F312, ExemptMostCook); LD58 and the surveys no longer call rows 8280-8287 stubs (live formulas, 0 in the baseline). L112 planned (rows 8708-8719: $D$8700, L$8706). New bugs: L115 (Mitigation 2555 reads the LPG ETS row 1720 instead of 1715; Medium), L116 (Elasticities H53/H54; Low), L117 (Multipliers D44; Low), planned. The kerosene rows 5587/5588 are part of L45.
- **Regenerated:** LegacyBugFixes, replication lists (and working_version copies, which had been left stale earlier today), BugsIssuesUpgrades, BUGSandISSUES (.docx, .xlsx), CPAT_BugFix_Procedure_and_Register_v5_5.docx, team tracker `Tracking issues.xlsx`, plan documents.
- **Not done:** sending to the CPAT team (the user's call).

## 2026-10-19 - CPAT-AI-Mitigation-MVP v5.6: power P3 and P5, I59, I60, L114, exemption phase-out, MTInputs appendix

- **What (section 4 of the open list, in plan order):** power P3 (manual capacity and investment from 'Manual inputs' 349-371; rows mancap, mani, needm; legacy bug L118 registered and fixed: logit investment sized on the need net of manual investment) and P5 (coal implicit cost rows cics, cicl, cic from GoalSeekCoal (new legacy data tab, 85 countries, not Egypt) or the Manual option; in dispatch and investment; in tariffs unless Settings C66 PwCoalICTariff = No; memo rows fce, cik, swi, swd); I59 (electricity fuel price reform in the manual excise of policy scenarios) and I60 (end-user price floor) replicated; L114 fixed (renewable subsidy inputs nominal to real); exemption phase-out of uncovered fuels and sectors (section-1 rows ExemptPhaseout, YearPha, ExemptPhaseoutPeriod, exph; ctcov = 1 if covered, else exph; LegacyDiff 67 part a); MTInputs appendix blocks A-D (global rows below the power rows; TransportParams, Settings and Constants read them; TransmissionCostShare read in the levelised cost); I25 traced: the MVP floored the growth of process emissions at 0, legacy does not (floor removed); I26 checked: energy N2O as legacy, production held at the base year registered as I66; MIT_MAX 9000 (VBA MIT_MAX_ROW too).
- **Checks:** quick check PASS: 12,706 shared codes, 98 new, 29 changed (process emissions of scenario 2, the I25 floor; max 8.44 Mt CO2e). On-switch test in LibreOffice (scenario 2): nuclear Manual with 2,400 MW from 2030 builds 2,400 MW in 2029 and then replaces retirements; coal implicit cost Manual 0.01 -> 0.03 $/kWh by 2030; exemption phase-in 0.2 (2027) to 1 (2031); additional renewable subsidy deflated (0.0098 in 2027). Full check and paste test not run (user: rudimentary checks only).
- **Not done (TODO, section 4 still open):** the initially exempt residential split (12b), the appendix scenario rows (2c, 2d) and Settings C27, C36-C39, LD20, I66, distribution options, 12d follow-ups, results blocks E-G, I31 remaining parts; then section 5.

## 2026-10-19 - v5.6 continued: items 1-7 of the ordered list

- **What:** Settings C27 (EFsAdjustmentAnnexI, as legacy E7534) and C36-C39 (SCC sources, Ricke parameters in the legacy texts) read MTInputs; scope rows per scenario after the power rows (CTaxCoversBiomass, ConsSubPhaseScope_*, PriceCtrlPhaseScope_*, ProdSubPhaseScope_*; Constants rows removed); I66 replicated (fuel production for supply methane: world demand, methane-fee price response; inventory-year activity = base production, avoiding a loop; Egypt oil and gas +4,968 ktoe by 2041); initially exempt residential demand (12b, section 6b rows lkxp, lkxe, lkxr, lkx, lkxa; share on Settings C83 from HHSurvey); nominal GDP rows gdpn (12d; WEO NGDP, NGDPD); I31 found complete; LD20: Europe gas shift to LNG (Inputs_pint nga.eus, legacy rows 699, 706), the ad-valorem flag is unused in legacy. MT_LAST 512 in the VBA.
- **Checks:** quick check PASS (12,706 shared codes, 150 new, 55 changed: the I25 process-emission growth and the I66 production growth). On-switch: ExemptMostCook Yes, bottom 4 deciles: 33% of LPG initially exempt, +38-44 ktoe of LPG against full response under the $20 scenario while the phase-in rises (0.2 in 2027 to 1 in 2031). Full check and paste test not run (rudimentary checks only, user).
- **Open:** items 8 (results blocks E-G: NDC comparison, memos 3 and 16a, air-pollution and transport-externality module sheets) and 9 (distribution: ASPIRE-targeted and poverty-line transfers, sectoral ranking and charts; standalone tool dropped); section 5.

## 2026-10-19 - v5.7: item 8 A+B (NDC comparison, GDP memo rows)

- **What:** section 14c NDC comparison (sheets NDCs and GHGHist from legacy; MTInputs NDCs, NDCTargetYear, Conditionality; five NDC types; targets incl. LULUCF, index, reduction against scenario 1, share achieved, distance to target); comparison only, no NDC goal seek (user). Section 16 memo rows: growth effect by revenue use (gdpg), by year of the reform (gdpy, one shifted row instead of legacy's twelve, to keep scenario groups copy-paste identical), change in GDP level. Section 3 memo (F6) already covered by v5.6 rows. Legacy bugs L119-L123 fixed and registered; issues I67 (China CO2 hard-coded in legacy), I68 (reference years outside the historical data give N/A).
- **Checks:** quick check PASS (no existing output changed; new codes only). Legacy comparison (Egypt, cached .xlsb): same NDC (BAU, 2030, -27%, excl. LULUCF) and method; target 344.3 Mt CO2e against legacy 355.7 (the known baseline GHG difference: BAU 471.7 against 487.2). Legacy's cached policy scenario is not the MVP's scenario 2, so the share achieved (21% against 51%) is not comparable. Only Egypt's BAU type was checked against legacy values; Fixed, Historical and Intensity are tested by construction only.
- **Open:** items 8 C (transport externalities) and D (air pollution; data tabs in the MVP workbook), item 9, section 5.

## 2026-10-19 - v6.0: consolidated release (distribution as legacy, I43, I33, I47 intensities)

- **What:** consolidated release of v5.0-v5.7. Distribution matches legacy: ASPIRE and poverty-line transfers, median flags, chart outputs (urban and rural, Lorenz, horizontal), production-sector prices and top-20 ranking, 11 charts. Distribution bugs D10-D31 are fixed; the user accepted the fixes of D11, D13 and D15. Also: I43 replicated (revenue uses count impulses from CPIntro), I33 (corrected Egypt prices kept by the data step), I68 in part (WEO real GDP 2000-2040), I14 accepted. Methane intensities use base-year data activity as legacy (I47); the fee revenue stays out of the fiscal space because it is circular.
- **Checks:** quick check PASS, 0 error values after a full recalculation (`calculateAll`; a plain load hides Err:522, now in NORMS). Distribution switch tests match the specification (cash, poverty line 6.85, median flags, fallback; Lorenz baseline equals legacy). Full check: sections 0-4 PASS with 0 FAIL. Section 5 crashed when a LibreOffice process was killed by mistake; the full check was then run on v6.1, which changes no output against v6.0.
- **Not done:** ETS goal-seek runs (NORMS 5; the user tests I30).

## 2026-10-20 - v6.1: I49, I47, I68, I46; parked items dropped

- **What:** I49 producer subsidies now enter the supply cost as legacy (rows `psd`, `psu`, block row `psp`). This also fixes legacy bugs L124 (residential gas read the oil subsidy) and L125 (a per-liter value added to the per-barrel price of other oil products). I47 counts the methane fee in the fiscal space on the stored scenario-1 activity of gas and biomass use (sheet BaselineCO2 rows dg, bm; `ch4.emf`, `ch4.revf`, check `ch4b.chk`). I68: NDC reference years 2021-2024 come from the GHGs inventory (`ndc.hc`, `ndc.hv`). I46 is closed: renewable subsidies have been in revenue since v5.4, and transport is dropped. The user dropped I28, I61, I62 and I63, plus the air-pollution co-benefits (I69) and transport externalities (I70) modules.
- **Checks:** quick check PASS, 0 error values after a full recalculation, 0 change on 12,992 output codes against v6.0 (Egypt: no producer subsidy data, no methane fee). Functional test with non-zero inputs (scratch, LibreOffice): producer subsidies move the coal, gas and oil supply costs as the formula requires (residual 0). A methane fee of 50 in groups 2-3 reaches the fiscal space with no circular reference (0 error cells): ch4.revf 2,194 against ch4.rev 2,194 in 2022, 2,774.5 against 2,774.3 in 2037. Reference year 2021 reads 332.3 Mt from the inventory.
- **Caveat:** the fiscal-space fee uses scenario-1 gas and biomass activity, so it differs slightly from the reported fee revenue (rmf) when a policy changes gas or biomass use. Legacy uses the scenario's own activity and avoids the loop only through bug L67.

## 2026-10-20 - v6.2: reforms as separate wedges, L67 without look-ahead, circular references removed

- **What (user decisions 2026-10-20):**
  - **Subsidy reforms are always separate from the before-tax build-up.** The producer subsidy phase-out is a wedge: `ppsw` per price block, `psw` per subsector, x pass-through, with its VAT in `rsr`. The supply cost keeps the existing producer subsidy.
  - **Units fix:** `psp` is now $/GJ. In v6.1 the oil value was per price unit; Egypt is unaffected (no producer-subsidy data).
  - **Legacy bug L67, fixed your way:** next year's required generation is estimated as this year's x (1 + growth from last year), in the MVP, the Python reference and the legacy cell plan (L4027 `=L3752*IFERROR(L3752/K3752,1)`).
    - Legacy Egypt inputs: capacity 77.9 GW in 2030 and 109.6 GW in 2040, against 75.2 and 107.3 in legacy and 77.3 and 109.5 when next year is read directly.
    - The need follows the 2023-2024 demand shock: 4.3 GW in 2024, 0 in 2025.
  - **Methane fee (I47):** it enters the fiscal space on the stored scenario-1 gas and biomass activity, so the fiscal space reads no fuel use (your rule: no vulnerability to circular references, close to legacy).
  - **New high-priority issues:** I62 (partial adjustment, reinstated) and I71 (fuel use on total GDP: population takes the income elasticity).
- **Finding:** the v6.0 circular reference was not the power look-ahead.
  - The price-block averages (`rpn`, `pnq`) used ranges that ran 44 rows past the subsector blocks into section 11, including the scenario-1 lookup `ener.ref`.
  - Bounded in v6.2 (names `PVar`, `PPar`).
  - The power fuel-price average now reads one row (`fpn`) instead of five years of the price-block area.
  - NORMS records the four rules.

## 2026-10-20 - Policy taxonomy covering the FTT policies (plan)

- **Task:** list the policies of FTT and propose a CPAT policy taxonomy that includes all of them. Done as a plan: `excel_ai/mitigation/PolicyTaxonomy_Plan_v6_2.md` (10 families, family.instrument codes, a representation tag per instrument, CPAT rows and FTT variables side by side).
- **Inputs:** open-source stand-alone FTT, `github.com/cpmodel/FTT_StandAlone` commit 8cf4bfd (`Utilities/titles/VariableListing.csv`, `ftt_source/ftt_core/`, `ftt_source/Power/ftt_p_phase_out.py`, the LCOE/LCOT/LCOH functions); `templates/MTInputs_template.xlsx`; `Transport_Method_v6_2.md`, `PowerFeatures_Plan_v6_2.md`, `Scenarios_Method_v6_2.md`; `coded/cpat_model/constants.py`.
- **Outputs:** the plan above and its Word copy `excel_ai/mitigation/PolicyTaxonomy_Plan_v6_2.docx` (pandoc, landscape); item in `excel_ai/plans/TODO.md`. No workbook or code changed.
- **Caveats:** FTT here is the stand-alone version (power, passenger road, freight, residential heat, industrial heat); E3ME-FTT steel, hydrogen and agriculture modules are not covered. 9 FTT instruments are new to CPAT; most are technology-specific and need technology shares that CPAT has only in the engineer power model (road model dropped, I61), so outside power they are shadow-price or exogenous-path approximations. Decisions open: plan section 5.
- **Robustness to circular references (user 2026-10-20: power upgrades as legacy bugs, GDP and methane as recommendations):**
  - **L126 fixed:** the fuel price for power is a trailing 5-year average (t-4 .. t, over row `fpn`, the scenario's own years only); legacy averages t-2 .. t+2.
  - **L127 (latent):** the levelised variable cost may read the future only because its inputs are exogenous; the quick check enforces this.
  - **`ghg.k`:** it read scenario 1's GHGYear (2024) cells in every year; it now reads stored scenario-1 values (sheet BaselineCO2 rows ch4c, ch4sup).
  - **LAMBDA group test:** moved from the spacer column, which sat inside running ranges and the next group's reads, to sheet `LambdaTest`, which nothing reads.
  - **New quick-check tests:** no formula reads a later year except `mani` (data), `dsum` and `lvc`; no parameter cell reads a later model row that is not data; the levelised cost reaches no fuel use, GDP or power quantity row.
  - **Issues I72-I74:** recommendations to the CPAT team on GDP timing, bounded scenario-1 lookups and methane calibration bases.
- **Checks:** quick check PASS: 0 error values after a full recalculation, the LAMBDA group equals group 2 (1.8e-16), the three robustness tests pass.
  - **Functional test with non-zero inputs:** producer subsidies with a phase-out to half from 2030, and a methane fee of 50 in groups 2-3. No error cell. The wedge equals the expected value; the before-tax price and supply cost are unchanged by the phase-out; `ch4.revf` tracks `ch4.rev`.
- **Results against v6.1** (L67 and L126 together):
  - Baseline 2030: CO2 232.0 Mt (231 in v6.1), power CO2 95.7 Mt (94.5), investment 10.8 bn USD (9.0; same level by 2040).
  - $20 carbon price (scenario 3): the 2030 CO2 cut against baseline is 16.1 Mt (18.0 in v6.1), about 10% smaller, because the power fuel price now lags.

## 2026-10-20 - Housekeeping: status, I62/I71 as legacy issues, open-work lists

- **Task (user 2026-10-20):** I62 and I71 are legacy issues, high priority for the CPAT team but not for the MVP; status is 80% complete for Excel-AI-CPAT and 40% for the Python part; clean up the open-work lists.
- **Register:**
  - I62 and I71 are now Accepted, replicated as legacy, and passed to the CPAT team as recommendations (with I72-I74).
  - I52 and I53 are Accepted on a condition: replicate legacy only if ETS coverage by Dashboard groups or manual domestic prices are ever built.
  - Upgrades: U3, U8, U9, U11 and U12 removed (done, decided, or duplicating I62); U1, U2 and U4 rewritten.
  - Regenerated: BUGSandISSUES (xlsx, docx), the Word register, the replication lists and the team tracker.
- **TODO:**
  - `excel_ai/plans/TODO.md` now lists only open work, grouped as "with the user", "next for the AI" and "later".
  - `coded/TODO.md` carries the 40% status.
- **Decks:**
  - The v6.2 overview deck's "Next" card now lists U4 and U2 in place of I62 and I71.
  - The overarching deck is now `Presentations/AIClimate-FiscalTools_v2.6.pptx` (folder `Presentations - Overarching/` until 2026-10-20), with v2.5 moved to `Old/`:
    - slide 5 shows 80% (1a) and 40% (1b), with the bars resized and the footer dated 20 October for 1a and 1b;
    - slide 31 has the same figures;
    - the other slides are unchanged.

## 2026-10-20 - Excel repair "Named range from /xl/workbook.xml" fixed

- **Problem (user 2026-10-20):** Excel repairs v6.2 (and earlier versions, at least back to v5.7) on open: "Repaired Records: Named range from /xl/workbook.xml part".
- **Cause:** the comment of the LAMBDA name FUELUSE was 305 characters long, and Excel allows at most 255. A scan of all 737 names found nothing else:
  - names: none invalid, none looking like a cell reference, no duplicates, none with a bad sheet scope;
  - formulas: none over 8,192 characters, no missing `_xlfn` prefixes, no undeclared `_xlpm` parameters, no #REF!.
- **Fix:**
  - `build_v6_2.py`: the FUELUSE note is shortened to 227 characters, and the build now asserts that every name comment is at most 255.
  - The shipped `CPAT-AI-Mitigation-MVP-v6.2.xlsm` is patched in its package; only that comment changed.
  - The variants are regenerated with `make_variants_v6_2.py`: `_noMacros.xlsx`, `_noLambdas.xlsm` and `_noMacros_noLambdas.xlsx`.
- **Caveat:** not confirmed in Excel. The cloud has no Excel; the user to confirm on Windows.

## 2026-10-20 - v6.3: release with the Excel repair fix; cell plans L113-L125 and D10-D31

- **Task (user 2026-10-20):** bump everything to v6.3 to reflect the fix of the Excel repair on open.
- **Bump:** every `_v6_2` script and note copied to `_v6_3`, with v6.2 in `Old/` (and `presentation/Old/`). The top-level v6.2 workbook, its variants and the overview deck moved to `excel_ai/old/`. READMEs and TODO point to v6.3. The version log has a 6.3 row.
- **Build v6.3:** quick check PASS (288 s). The name scan is clean: no comment over 255, no invalid or duplicate name. Variants: `_noMacros.xlsx`, `_noLambdas.xlsm` (111,991 LAMBDA cells expanded) and `_noMacros_noLambdas.xlsx`. Model results unchanged from v6.2 (only a name comment and the version log differ).
- **Full check:** run on v6.3. The v6.2 run was stopped at section 5 because its file moved to `Old/`.
- **Cell-level fix plans (two agents):**
  - **L113-L125** (`fixes_other_mitigation_2.json`, now 60 entries; the Word plan and PDF): 8 bugs with cell edits.
    - L123 is not reproduced in the .xlsb (the reading came from the LibreOffice copy).
    - L124 has the same cells as the L82 plan.
    - L122 corrected: J18465 holds non-CO2, so non-CO2 is counted twice and LULUCF is missed.
    - Two new legacy findings are in TODO, to confirm.
  - **D10-D31** (`fixes_distribution.json`, 69 new entries; the Word plan and PDF):
    - 21 bugs with cell plans;
    - D16 not planned (the survey variable's definition needs confirming);
    - D24 needs inserted rows;
    - D25 and D31 are widened to two similar errors found while planning.
  - All "now" formulas are checked against the .xlsb. Nothing is recalculated in Excel.
- **Two new legacy bugs (user 2026-10-20), already fixed in the MVP:**
  - **L129 (Medium):** the baseline renewable subsidy is counted twice. Rows 2785-2788, 2947-2951 and 7897-7900 add L2743 + L2745, and L2745 already includes L2743. It only bites when MTInputs 354 is not zero. The MVP has one row, `rnsp`.
  - **L130 (Low):** the intensity NDC rows use different base years. The conditional row cuts the target-year BAU intensity; the unconditional row cuts the reference-year intensity. The MVP's `ndc.hi` uses the reference year for both.
  - Registers, the Word documents and the team tracker are regenerated.
- **TODO next (not built, user 2026-10-20):** LAMBDAs in the second column group instead of the third; two scenarios by default to cut file size, still extensible by copy-paste.
- **Price build-up style (user rule 2026-10-20, NORMS 2.6):**
  - Rows outside the build-up are in italics: the parameter and input rows, the memo splits of txo, and the fuel-use weights.
  - The post-tax price `rpn` moved to the last row of each block. Its values are bold, with a thin top and a thick (medium) bottom border across the whole row.
  - v6.3 rebuilt: quick check PASS (169 s); variants regenerated; the name scan is clean.
  - Results unchanged: only the row order within the price blocks moved.
- **Full check (v6.3 before the style change):** sections 0-4b had no FAIL (formula length, recalculation, uniformity, LAMBDA encoding, values against Python, power against legacy). The run was stopped at the 30-minute background limit inside section 5 (scenario tests), and is rerun with a longer limit.

## 2026-10-20 - Plan: separating the Excel tools from their database

- **Task (user 2026-10-20):** a simple way to keep the global data out of the Excel tools, (a) for WB and IMF CPAT team members and (b) for other users; whether loading by country is quick and costs time per table; a version for the Global Fiscal Indicators dashboard (`new-ai-tools`).
- **Outputs:**
  - `excel_ai/mitigation/DataSeparation_Plan_v6_3.md`: a database of CSVs pre-split by country, with a manifest; a `LoadCountryData` macro that fills the existing data tabs for one country (layouts, formulas and checks unchanged); `_Linked` and one-country variants; routes for the team (a synced SharePoint folder) and for others (country packs, a public folder, Power Query later); speed costs; v6.3 steps.
  - The dashboard version was written for `new-ai-tools/TaxMacroFiscalDashboard/` and is kept for now as `excel_ai/mitigation/DataSeparation_Plan_Dashboard.md` (this session cannot push to `new-ai-tools`; move it there). It keeps the cross-section embedded, because the scores need all countries, and adds the series by country through Power Query.
  - `excel_ai/plans/TODO.md`: new item for v6.3.
- **Caveats:**
  - Plan only; nothing is built.
  - The size breakdown of v6.2 is measured: the model sheet is 5.3 MB and the data tabs about 6 MB of the 12.8 MB.
  - The load times are typical figures, not measurements. Step 1 of the plan is a benchmark on a WB/IMF laptop.
  - Which tables are restricted by licence is still to be confirmed by the user.

## 2026-10-20 - Data workbook of the dummy data; plan updated (Power Query, version selector, dashboard)

- **Task (user 2026-10-20):** one xlsx holding all the data in `coded/data/dummy`; extend the plan: only the biggest and possibly proprietary tables of the prototype link to the online data, by query; a selector for the data version (dummy, real, real with dummy proprietary tables); Egypt works out of the box; a simple dashboard on ScenarioCompare. Only the file now; the rest after this branch is brought up to date with main.
- **Outputs:**
  - `coded/data/CPAT_Data_dummy.xlsx` (9 MB): README, Index, the 38 CSVs as `c_` tables, and the four MVP-layout `L_` tables (EnergyCons, Prices_dom, HHSurvey, IO_GTAP). Every table is an Excel table with a header in row 1 and a country filter column where it has countries (named `ISO3` at first, which clashed with `iso3` in Excel; renamed `FilterISO3`, see the next entry).
  - Builder: `coded/legacy_export/build_data_workbook.py` (README section added). Works for any version folder.
  - Plan: section 7 of `excel_ai/mitigation/DataSeparation_Plan_v6_3.md`. It supersedes sections 2-6 where they differ: Power Query instead of the loader macro, with a `SetupDataLinks` macro creating the queries.
  - `.gitignore`: `CPAT_Data_*.xlsx` is ignored except the dummy workbook.
  - `excel_ai/plans/TODO.md` item updated.
- **Checks:**
  - Every cell equals its CSV (numbers to 1e-14).
  - The `L_` tables equal `CPAT_LegacyData_dummy_csv/` cell for cell.
  - The file opens in LibreOffice.
- **Caveats:**
  - Power Query, the SharePoint refresh and the speed are untested; the cloud has no Excel and no access to the user's SharePoint.
  - The licence classes and the MVP tab of each table in the Index are proposals.
  - Only four tables exist in the MVP layout. WEO, GDPRatios, HH_Elast and GHGs need converting. Balances and Transport1-2 have no dummy data.
  - Header cells were made unique for Excel tables. In ghgs.csv, the two header rows are joined ("1. Energy | CO2"). Changes are listed in the Index.

## 2026-10-20 - Excel repair of CPAT_Data_dummy.xlsx fixed; a lint for every workbook written by code

- **Problem (user 2026-10-20):** Excel repaired 7 tables of `coded/data/CPAT_Data_dummy.xlsx` (table4, 5, 13-16, 21). The user reports that such repairs happen often.
- **Cause:** those 7 tables already had a column `iso3`, and the builder added a filter column `ISO3`. Excel compares table column names case-insensitively, so it treated them as duplicates. openpyxl and LibreOffice accept them.
- **Fix:**
  - The filter column is now `FilterISO3`; the builder asserts that no source header has that name.
  - `CPAT_Data_dummy.xlsx` is rebuilt: same 42 tables and 144,429 rows.
  - The plan's query text and the README are updated.
- **Lint, for every workbook written by code:** `excel_ai/shared/excel_lint.py` checks the package for the Excel-only faults.
  - It found exactly the 7 tables in the user's repair log, and nothing else in that file.
  - It also finds the FUELUSE comment fault (more than 255 characters) in `Old/CPAT-AI-Mitigation-MVP-v6.1.xlsm`.
  - Clean: the rebuilt data workbook, the MVP v6.2, `CPAT_LegacyData_dummy.xlsx` and the dashboard `Global_fiscal_indicators_v1.2.xlsx` (new-ai-tools).
  - `build_data_workbook.py` runs it and fails on a problem.
- **Norms:**
  - `excel_ai/NORMS.md` has a new section 3g: lint before shipping, what is checked, and the procedure when Excel still repairs a file (read the named part, add a rule the same day).
  - Rule 3b.8 now says the comparison is case-insensitive.
  - The root `NORMS.md` points every project to it.
- **Caveats:**
  - The rebuilt file has not been opened in Excel here; the user to confirm.
  - The MVP builder and its variants do not call the lint yet (TODO, with the next version).
  - Neither do the dashboard builder or the other repositories.

## 2026-10-20 - CPAT-AI management decks; folder renamed to Presentations

- **Task:** a high-level CPAT-AI briefing for managers. It is a series of decks, also in new-ai-tools (`Presentations/CPAT-AI/`, merged in cpmodel/new-ai-tools#1).
- **Inputs:**
  - the v6.3 bug and issue register (`excel_ai/BUGS.md`, `ISSUES.md`, `mitigation/issues_register_v6_3.py`);
  - the READMEs, QuickStart and Scenarios method v6.3;
  - the new-ai-tools slide kit (`Presentations/Sebastian-2026-10-20/kit.py`, AIClimate-FiscalTools v2.5 theme).
- **Outputs:**
  - `Presentations - Overarching/` is renamed `Presentations/`.
  - `Presentations/CPAT-AI/` holds `CPAT-AI_0_Management_Overview.pptx` (12 slides) and four topic decks (1 progress and differences, 2 legacy bugs and issues, 3 process and repository, 4 next steps and discussion).
  - The build script is in new-ai-tools (`Presentations/CPAT-AI/build_cpat_ai_decks.py`).
- **Caveats:**
  - CPAT-AI recalculation timings are TBC on the slide (legacy: more than 5 s, as stated by the user). Time them in Excel.
  - Three legacy descriptions on the "What is different" slide are summaries to confirm: scenarios copied in by macro, long nested formulas, data selected inside the calculation sheets.
  - Counts are from v6.3:
    - 159 legacy bugs (128 mitigation, 31 distribution);
    - 62 legacy issues (52 mitigation, 10 distribution).

## 2026-10-20 - v6.4: dashboard on ScenarioCompare (every macro button, charts of the stored scenarios)

- **Task (user 2026-10-20):** make ScenarioCompare a dashboard: every macro button on it (the user could not find them: since v3.6 five of the six were on the reference tab), with charts, and charts for copied scenarios too.
- **Build (`build_v6_4.py`, release v6.4):**
  - **Buttons:** all six macro buttons (Run all scenarios, Store baseline, Store live scenario, Solve ETS (live scenario), Clear stored scenarios, First-run test) are top right on ScenarioCompare (N1:S6, two across, two rows high, no text inset, so the labels fit). None are left on `Version Log, About, and Diff`. `add_macro_buttons` now appends the shapes to the sheet's chart drawing when there is one.
  - **Slots fill themselves:** row 6 takes the next stored ID after the slot on its left (`SMALL` / `COUNTIF` on SRScen). So every stored scenario shows, up to 8 besides the baseline, and a definition copied on MTInputs shows once RunAllScenarios has stored it. A typed ID still overrides a slot. Shipped: IDs 1, 3, 4, 5, 6.
  - **Charts:** 8 line charts right of the table, below the buttons: CO2 from fuel combustion, GHGs excl. LULUCF, fuel use, carbon price, net total revenue, GDP effect, residential electricity price and VRE share. Each shows the baseline (dashed) and the 8 slots over 2022-2041, with the slot's ID as the legend label.
  - **Chart data:** they read a chart-data block at the bottom of the tab (rows 370-544). It has one block per chart, with years down and slots across, looked up in StoredResults like the levels (one formula per block). An empty slot reads `#N/A`, which Excel leaves out of a line chart.
- **Checks:**
  - **Accepted #N/A:** the quick, paste and full checks accept `#N/A` only inside the chart-data values (`cmp_chart_area`, `cmp_na_only`).
  - **New full-check test:** `check_compare` also tests that the slots equal the stored IDs in order, that the chart data equal StoredResults (max rel diff 0), that empty slots read `#N/A`, and that each block uses one formula. It was run on its own: PASS.
  - **Quick check:** PASS. 13,396 output codes, 0 changes against v6.3 (model results unchanged).
  - **Render:** checked in LibreOffice (PDF of the tab): the buttons show their labels and the charts show their lines.
  - **Not run:** the full check.
- **Bump:**
  - Every `_v6_3` script and note was copied to `_v6_4`, with the version references bumped.
  - Variants: `_noMacros.xlsx`, `_noLambdas.xlsm` and `_noMacros_noLambdas.xlsx`.
  - The workbook was copied to the top of `excel_ai/`, and `working_version/` has the v6.4 notes.
  - Regenerated: the replication lists, the registers (BUGSandISSUES .xlsx/.docx, BugsIssuesUpgrades, BugFix book) and the team tracker.
  - Documents updated: Scenarios_Method (ScenarioCompare, section 5), QuickStart (buttons, the stale tab names), the ExcelReview checklist (steps 13-14: buttons, charts) and the READMEs.
- **Caveats:**
  - **Not yet moved:** the v6.3 files are not yet in `Old/` / `excel_ai/old/`. The move was refused by this session's permission settings and waits for the user. Until then, `check_quick_v6_4.py` also finds the last release in the folder root. *Resolved 2026-10-20 (user: try again): v6.3 scripts, notes, workbook and documents moved to `Old/` (and `presentation/Old/`), the top-level v6.3 workbook to `excel_ai/old/`, the v6.3 copies in `working_version/` removed; the root fallback of `check_quick_v6_4.py` taken out. The v6.3 overview deck stays at the top until the v6.4 deck is built.* Not regenerated: `PolicyTaxonomy_Plan_v6_4.docx` (v6.3 copy only), `Formulas_v6_4.md` and the deck (with the full check).
  - **LibreOffice draws empty slots as lines at 0:** LibreOffice draws the `#N/A` of empty slots as flat lines at 0; Excel leaves them out. The legend still lists the empty slots as "-". To check in Excel (checklist step 14). Not confirmed in Excel: buttons, charts, and no repair prompt with the merged drawing.
  - **Charts tab unchanged:** the Charts tab (MTOutputs, live column groups) is unchanged. A group pasted on Mitigation still needs a series added there by hand. The dashboard covers scenarios once they are stored (RunAllScenarios for definitions, StoreLiveScenario for the live scenario).
  - **Paste test FAIL, older than this release:** `check_paste_v6_4.py` FAILs, with identical numbers on v6.3. No error values, but the pasted scenarios 3-6 differ from StoredResults by up to 2.9e-3 relative. It is in TODO.
- **Data-separation plan integrated (user 2026-10-20, after merging main):**
  - Retargeted as `DataSeparation_Plan_v6_4.md` (the v6.3 copy is in `Old/` since the moves of 2026-10-20; `coded/legacy_export` points to the v6.4 plan).
  - The separation now targets v6.5, since v6.4 is the dashboard release.
  - Section 7.6 records the dashboard built in v6.4, and what is still to add in v6.5: data version and refresh time in the heading, headline tiles, and the burden by decile. The decile rows must first be stored by RunAllScenarios.
  - TODO and the dashboard note point to the v6.4 plan.
  - No change to the workbook or to the data workbook.

## 2026-10-20 - Word documentation consolidated in `documentation/`, decks in `Presentations/`

- **Task (user 2026-10-20):** tidy up the documentation, starting with the human-readable (Word) documents. Plan first, then implement quickly, by copying rather than restructuring. Word goes in a root folder `documentation/`, decks in `Presentations/`.
- **Plan and index:** `documentation/README.md` (step 1 done; step 2, the restructuring, is listed there and in TODO).
- **Outputs:**
  - **`documentation/CPAT-AI-Mitigation-MVP_Documentation_v6.4.docx` (196 pages):** regenerated by `make_docs_v6_4.py`. The last one was v5.5. Changes to the generator:
    - it gained the Distribution and Data-tabs notes;
    - the title takes the version;
    - with no v6.4 full check, the verification appendix uses the last full-check report (`Old/check_report_v6.2.md`) and says so.
    - The run also regenerated `Formulas_v6_4.md`, which was stale; its copy in `working_version/` is replaced.
  - **`documentation/CPAT-AI-Mitigation-MVP_BugsAndIssues_v6.4.docx` (155 pages):** the bug-fix book, the BugsIssuesUpgrades register and BUGSandISSUES, appended as they are (docxcompose: 781 paragraphs, 259 tables, equal to the sum of the sources).
  - **Copies:** the Distribution pseudocode, the CBAM guide and the elasticities note.
  - **Moves:** the FY27 work plan from `Presentations/` to `documentation/`; the MVP overview deck (v6.3) from `excel_ai/` to `Presentations/`.
  - **`documentation/make_documentation.py`** rebuilds all of this at each release.
  - **Pointers:** NORMS (excel_ai 5: documents and decks at the root) and the READMEs (root, excel_ai, mitigation).
- **Caveats:**
  - **Duplication:** the originals stay where they are. The generated Word files are rebuilt in `mitigation/`, and code refers to the standalone ones by path. So each document exists twice until step 2.
  - **Overlap within the bugs-and-issues document:** its three parts overlap. They are appended, not merged.
  - **Not copied:** the five `legacy_bugfix_plans` Word plans (their content is in part 1 of the bugs-and-issues document) and `Transportation_methodology.docx` (a data source).
  - **Checks:** both consolidated files open in LibreOffice (converted to PDF). They are not opened in Word yet.

## 2026-10-20 - Documentation step 2: one register, generators write to `documentation/`, fewer notes

- **Task (user 2026-10-20):** do step 2 of the documentation plan, the restructuring. It runs in parallel with another agent's code work, so the builder and the checks were not touched.
- **One register:**
  - `make_bugfix_book_v6_4.py` now writes `documentation/CPAT-AI-Mitigation-MVP_BugsAndIssues_v6.4.docx`: 79 pages, against 155 for the three registers appended.
  - It already held every bug (with cell plans), the prototype bugs, the issues and every LegacyDiff departure. It gained a summary, the effect of each power fix (computed from `power_model_ref`; equal to the old register's table), the upgrades by priority, the improvements made, and the upgrades in the reference table.
  - Retired: `make_issues_doc_v6_4.py`, `render_docx_v6_4.js`, `make_bugs_issues_docx_v6_4.py` and their Word outputs.
  - The register as data stays (`issues_register`, `BUGSandISSUES_v6_4.xlsx`, the team tracker; both regenerated, the tracker note pointing to the new file).
- **Generators write to `documentation/`:**
  - `make_docs_v6_4.py` writes the MVP documentation there. Its project-folder copy is gone.
  - The standalone Word files (Distribution pseudocode, CBAM guide, elasticities note) now live only in `documentation/`. The references are updated, including comment and doc lines in `coded/`.
  - `documentation/make_documentation.py` now runs the two generators.
- **Markdown:**
  - `mitigation/` went from 38 to 29 notes. The eight plans are now `Plans_v6_4.md`, and the three legacy reviews are `Reviews_and_Surveys_v6_4.md`. Each section keeps its text, with its former file name in the title.
  - References are updated (TODO, READMEs, register, `coded/legacy_export`); the replication lists are regenerated.
  - `excel_ai/working_version/` is retired, and NORMS 5 updated.
- **Caveats:**
  - **Builder not edited:** `build_v6_4.py` (not edited, to stay clear of the parallel work) still names the retired BugsIssuesUpgrades file in three workbook texts and cites `MTInputs_Appendix_Plan` and `PowerFeatures_Plan` by name, which are now sections of `Plans_v6_4.md`. This is in TODO, for the next build. The full check's stale-reference test may flag these.
  - **Notes still separate:** the notes the builder or checks cite stay separate for the same reason.
  - **Not opened in Word:** the documents are checked in LibreOffice only (they convert to PDF).

## 2026-10-20 - v6.5 (MVP): first linked data table (Balances), data-source dropdown, one update button; plan for the rest

- **Task (user 2026-10-20):** connect the big data tables so CPAT holds one country; sources local, repository, shared drive; a dropdown; one button; Egypt out of the box; lighter and faster. Second message: do it fast as an MVP with one table (Balances), and a plan for the rest; few tests.
- **Inputs:** `build_v6_4.py`, `CPATScenarios_v6_4.bas`, `coded/legacy_export/build_data_workbook.py`, `data/legacy_Balances.csv`, the SharePoint Share link from the user, plan section 7 of `Plans_v6_4.md`.
- **Outputs:**
  - `excel_ai/mitigation/build_v6_5.py`, `CPATScenarios_v6_5.bas`, `CPAT-AI-Mitigation-MVP-v6.5.xlsm` (and the hand-over copy in `excel_ai/`). New sheet DataLinks (dropdown `DataSource`: Embedded (default), Dummy - local file, Dummy - SharePoint; source table; linked-tab table with one row, Balances <- `L_Balances`). Macro `UpdateDataTables` (buttons on DataLinks and ScenarioCompare) writes the Power Query text with the path and country as literals, creates `q_Balances` and its table at Balances!A3 on first use, refreshes it, recalculates once. Macros `CalculationOn`/`CalculationOff` (button on ScenarioCompare). Version-log row 6.5.
  - `build_data_workbook.py`: adds `L_Balances` (the MVP's Egypt Balances rows). `coded/data/CPAT_Data_dummy.xlsx` rebuilt (43 tables) and committed again.
  - `Plans_v6_5.md` (section 1.8: what was built, the tables to link in order, lighter and faster, the first Excel test, the three places, fast rebuild); `Plans_v6_4.md` to `Old/`; references updated. v6.4 workbook to `Old/`.
- **Checks:** build ran (5.5 min, LibreOffice); `excel_lint` clean on both workbooks; StoredResults identical to v6.4 (620 rows, max abs diff 0). Quick check, full check, paste test and variants not run (user: skimp tests).
- **Caveats:**
  - **Power Query not tested:** it cannot run on Linux. The macro has never run in Excel; the first refresh is the user's test (plan 1.8.4).
  - **SharePoint:** the Share link gets `download=1` appended; it may still be refused, then paste the direct path (File > Info > Copy path) into DataLinks D12. The SharePoint file must be replaced by the new dummy workbook (it has no `L_Balances` before).
  - **L_Balances is not dummy data:** it is the Egypt table of the public legacy file, so a refresh gives the shipped results.
  - **No size gain yet:** Balances is small. The size and speed gains (one country in the all-country tabs, two scenario groups, manual calculation) are planned in 1.8.2-1.8.3, not built.
  - **Embedded cannot be restored by the macro** after an update (reopen the shipped file).
  - **Scripts other than the builder and the module are still v6_4** (checks, documents, variants); no `_noMacros`/`_noLambdas` variants of v6.5.
- **Follow-up (user 2026-10-20, same day):** VBA compile error fixed (the three DataLinks constants sat after the first procedures; moved to the declarations at the top). DataLinks is now the second tab (after Cover) and the workbook opens on it; C8 shows the folder the workbook is saved in (`CELL("filename")`), C9 the file or URL the last update read; the source table moved to rows 12-14. The local search also tries `<folder>\data\`, `<folder>\coded\data\` and `..\data\`. The build copies the workbook to the repository root (the hand-over copy; the `excel_ai/` copy is removed). Rebuilt, lint clean; not run in Excel.

## 2026-10-20 - Data workbook: Python format and CPAT format, with a converter

- **Task (user 2026-10-20):** a script in `data` that converts the data workbook between the Python format (as now) and the CPAT format, checked against CPAT itself; `CPAT_Data_dummy` renamed `..._python.xlsx`, and a new `..._cpat.xlsx`.
- **Inputs:** `coded/data/dummy/*.csv` (38 tables); the legacy data sheets of `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (header rows, cell positions, WEO and WDI code lookups); `legacy_export/export_to_legacy.py` and `build_data_workbook.py`.
- **Outputs:**
  - `coded/data/convert_data_workbook.py`: `to-cpat` (Python workbook or CSV folder -> CPAT workbook) and `to-python` (CPAT workbook -> Python workbook, optionally the CSVs). `--rebuild-layouts` re-reads `data/cpat_layouts.json` from the legacy file.
  - `coded/data/dummy/CPAT_Data_dummy_python.xlsx`: the former `data/CPAT_Data_dummy.xlsx` (removed from the repository earlier the same day), same content, rebuilt; `build_data_workbook.py` now writes `CPAT_Data_<version>_python.xlsx` into the data folder.
  - `coded/data/dummy/CPAT_Data_dummy_cpat.xlsx`: 17 legacy data sheets with the legacy names, header rows and cell positions (EnergyCons, Prices_dom, HHSurvey, IO_GTAP, WEO, WDI, UNPop, GDPRatios, GHGs, CH4Inputs, OilProductShares, EF_GHG, CalVal, Air_Data, HH_Elast, ASPIRE, WHOCooking); 21 `py_` sheets (tables of the multi-table legacy tabs, carried in the Python layout); 3 `pyx_` sheets (the Python cells legacy has no place for: WEO Scale, energy `ren` and `total_energy_use`, six CH4 columns); README and Index (data range to paste, columns left blank, Python column order).
  - `export_to_legacy.py` reads the CSVs with `float_precision='round_trip'`. `CPAT_LegacyData_dummy.xlsx`, `_csv/` and `_ReadMe.md` are regenerated: values now equal the CSV text (they were up to 8e-13 relative off, pandas' default parser); no other change.
  - Tests: `cpat_testing/data/test_convert_data_workbook.py` (6; whole suite 63 pass). `.gitignore`, `legacy_export/README.md`, `coded/README.md`, `coded/TODO.md`, `excel_ai/plans/TODO.md` and `Plans_v6_4.md` (paths, gap note) updated.
- **Checks:** Python workbook -> CPAT -> Python: every c_ and L_ sheet identical, values and types. CSV -> CPAT -> CSV: every table equal to 16 significant digits, same rows and order. Every key the converter builds (UNPop, EF_GHG, Air_Data, CH4Inputs, OilProductShares, GHGs, GDPRatios, HH_Elast, ASPIRE, WHOCooking) is found in the legacy sheet. The WEO and WDI keys not found there are series or countries legacy lacks; CalVal matches only Egypt, because NoPropData strips the rest. Excel lint clean; opens in LibreOffice.
- **Caveats:**
  - **Code renames (assumption):** WEO indicators BCA_BP6, BCA_GDP_BP6, ENDA and PCPI_PCH are written as the legacy series BCA, BCA_NGDPD, XDC_USD.PA_RT and PCPIPCH (taken to be the same series under the IMF data API codes); WDI `enda` is `XDC_USD.PA_RT.A`. To be confirmed by the team.
  - **Partial legacy sheets:** WDI fills only the second block (header row 265; the urban-growth block is blank); EF_GHG holds only the CO2 factors (no GWP/GTP rows); Air_Data holds only density and NetCV; GHGs holds only the inventory (UNFCCC category and fugitive memo blank; the shocks block stays in `py_ghg_adjustments`); legacy columns the CSVs lack are blank (listed per sheet in the Index).
  - **Derived columns:** WEO/WDI "last year" is the last year with data; EnergyCons Year is 2022.
  - **Not converted yet:** the 21 `py_` tables (ECP, Power, Prices_int, Elasticities, Mapping blocks and tables with no legacy sheet): `coded/TODO.md`. The legacy-layout sheets are not `L_` Excel tables with `FilterISO3`, so Power Query (plan section 7) still reads only the four `L_` tables of the Python workbook.
  - **Precision:** openpyxl writes 16 significant digits, so a CSV -> workbook step loses up to about 1e-16 relative, and a whole float comes back as an integer (`5.0` -> `5`). The Index MD5 of the CSVs then differs after `to-python`. The model's CSV loaders still use pandas' default parser (`coded/TODO.md`).
  - **Not opened in Excel**, only in LibreOffice; no paste into the full legacy workbook tried.

## 2026-10-20 - All data in the root `data/`, with the conversion scripts; NORMS section 8

- **Task (user 2026-10-20):** merge with `main`; the overarching data folder is `data/` at the root: move all data there, mostly in subfolders, with the conversion scripts; update the norms.
- **Inputs:** the previous entry's branch, merged with `main` (v6.5 MVP: DataLinks, `L_Balances`).
- **Outputs (moves, history kept with `git mv`):**
  - `coded/data/dummy/` -> `data/dummy/` (Coded CPAT inputs; `coded/config.py` and `.env` now default to `../data/dummy`, resolved from `coded/`, so any working directory works).
  - The data workbooks -> `data/workbooks/` (`CPAT_Data_dummy_python.xlsx`, now with `L_Balances`, 43 tables; `CPAT_Data_dummy_cpat.xlsx`). `main`'s `coded/data/CPAT_Data_dummy.xlsx` is replaced by the `_python` file.
  - `excel_ai/legacy/workbooks/CPAT_LegacyData_dummy*` -> `data/legacy_dummy/` (values unchanged; the ReadMe names the new script path).
  - `excel_ai/mitigation/data/` -> `data/mvp_legacy_extracts/` (the 23 `os.path.join(HERE, 'data'...)` paths in the MVP scripts point there).
  - `excel_ai/distribution/data_*` (5 stages) -> `data/distribution/` (`scripts/common.module_dir`, `build_distribution_model_data.py`, `standalone/extract_egypt.py`).
  - `coded/legacy_export/` and `coded/data/*.py|json` -> `data/scripts/`; their tests -> `data/tests/` (15; `pytest tests` from `data/`). New `data/README.md` (folders, formats, scripts, rules; replaces `legacy_export/README.md`).
  - Root `NORMS.md` section 8 now covers all data: everything in `data/` by subfolder, new data go there, exceptions, dummy-only commits, rebuild every format when the dummy data change. `AGENTS.md`, `README.md`, the project READMEs, TODOs, `Plans_v6_5.md`, `DataTabs_v6_4.md`, the distribution docs and `.gitignore` follow.
  - MVP source: `CPATScenarios_v6_5.bas` looks for `CPAT_Data_dummy_python.xlsx` in `<repo>/data/workbooks/`; `build_v6_5.py` label to match.
- **Checks:** Coded CPAT 48 tests and `data/tests` 15 pass; `run_model.py` runs; `power_model_ref_v6_4.py` and `distribution_ref_v6_4.py` run from the new data folder; every file name the MVP scripts open exists in `data/mvp_legacy_extracts/`; the distribution `module_dir` folders exist.
- **Caveats:**
  - **Shipped v6.5 workbook not rebuilt** (no in-place edit of a shipped version; the MVP is being worked on in parallel): its DataLinks still look for `CPAT_Data_dummy.xlsx` in the old folders, so type the full path of `data/workbooks/CPAT_Data_dummy_python.xlsx` in DataLinks until the next build. The SharePoint copy keeps its own name.
  - **MVP full build and checks not run** after the move (only the reference scripts above); the next `build_v<n>.py` run is the test. Old/ scripts and `excel_ai/old/` keep their old paths.
  - **Not moved:** the legacy workbook and the team's reference files (`excel_ai/legacy/workbooks/`, the reference model), test fixtures (`coded/cpat_testing/model/data_expected/`), `legacy_bugfix_plans/data/` (fix-plan JSON, not data), `excel_ai/old/`. The distribution pipeline scripts stay in `excel_ai/distribution/scripts/`: they also build the distribution workbook.

## 2026-10-21 - v6.6 (MVP): speed - shipped with values, manual calculation, two scenario groups

- **Task (user 2026-10-20, overnight plan, release 1 of 4):** ship with calculated values and no recalculation on open, with a button to turn recalculation on and one to recalculate; replace OFFSET with INDEX and COUNTIFS; three scenario groups down to two on Mitigation and Distribution (group 2 = the live scenario in LAMBDAs).
- **Outputs:** `CPAT-AI-Mitigation-MVP-v6.6.xlsm` (and the root copy), `build_v6_6.py`, `CPATScenarios_v6_6.bas`; v6.5 files to `Old/`. The `_v6_4` scripts import `build_v6_6`. `check_quick_v6_4.py`, `lo_session_v6_4.py` adapted.
  - **Values in the file:** the build recalculates the final workbook in LibreOffice (LAMBDAs expanded) and writes every formula's value (395,465) into the file; `calcPr` manual, `calcId` 191029 (Excel 365), no full calculation on load, no recalculation on save. Macros `RecalculateNow` (timed, CalculateFull) and `ToggleRecalculation`; `RunAll` restores the calculation mode it found (was: automatic).
  - **Two groups:** group 1 baseline (plain formulas), group 2 live scenario calling the LAMBDAs (v4.3-v6.5: a third LAMBDA test group and sheet LambdaTest, dropped). Formulas 568k -> 404k; SUMPRODUCT 13.8k -> 7.7k; OFFSET 440 -> 0 (TRAILAVG, LAGVALUE now INDEX on the row from column A); the CH4/air-pollutant factor check `efok` is a key MATCH with a wildcard (was COUNTIFS); DataLinks C8 written by the macro (was the volatile CELL("filename")).
- **Checks:** quick check all OK except the tab order (Cover, DataLinks, MAIN: v6.7 merges DataLinks into Cover). Output codes against v6.4 (whose group 2 was plain): 13,396 codes, max abs diff 7e-15, so the LAMBDA group gives the plain results; Distribution group 2 (LAMBDAs) against the Python reference 5e-13. Build 2.8 min.
- **Caveats:** values come from LibreOffice; Excel shows them until the first recalculation (booleans as 1/0). Manual calculation is application-wide in Excel (the toggle says so). The LAMBDA test is now the regression against the last release plus the Distribution reference (a plain twin of group 2 in the check was tried and dropped: history cells error in LibreOffice for reasons unrelated to the LAMBDAs). The remaining 2,503 COUNTIFS are on ScenarioCompare (rebuilt in v6.7). Not opened in Excel.

## 2026-10-21 - v6.7 (MVP): the dashboard - front tabs, Live/Stored switch, charts, renames

- **Task (user 2026-10-20, overnight plan, release 2 of 4):** ScenarioCompare the dashboard at the front; Cover and DataLinks merged (status first, every user entry on ScenarioCompare); MTInputs renamed ScenarioDefinition in the front group; a Live/Stored switch (MTOutputs renamed LiveOutputs, StoredResults StoredOutputs) with lookups robust to reordering; short names as legend IDs; Charts tab deleted; 4-5 key indicators with absolute and % comparison; one comparison chart; time series with the chart beside each table and an indicator dropdown in the title; scenarios with no results left out of the charts; core and other buttons; blank scenarios grouped; StoredOutputs sorted (like variables together); no indices in the charts.
- **Outputs:** `CPAT-AI-Mitigation-MVP-v6.7.xlsm` (and the root copy), `build_v6_7.py`, `CPATScenarios_v6_7.bas`; v6.6 files to `Old/`. `check_quick_v6_4.py` (front-tab order, new test: every stored scenario has values). Sheet references renamed in the `_v6_4` checks.
  - **ScenarioCompare:** Results from (Stored / Live), year, data source and the source paths (from DataLinks); scenario slots 1-10 from ScenarioDefinition (ID, short name, name); key table (energy CO2, GHG, revenue % of GDP, GDP effect, net welfare: level, difference, % difference for the levels); bar chart (energy CO2 vs Base); four time-series blocks (default CO2, GHG, revenue, GDP effect) whose title is a dropdown of the indicator list (every LiveOutputs indicator except the price and Kaya indices). Every value: `INDEX(SCVal, MATCH(country.stem.ID, SCCode, 0), year column)` where SCVal, SCCode, SCYear are names with `CHOOSE(switch, LiveOutputs, StoredOutputs)`; so any row order works (the build ships StoredOutputs sorted by stem, then ID). No result = #N/A (hidden by a conditional format; a gap in the charts).
  - **Charts:** built with the scenarios that have stored results, short-name legends at the bottom, baseline dashed grey, one colour per slot, no axis titles, titles linked to the block's indicator (with cached text). Macro `RefreshDashboard` (run by Recalculate now, Run stored scenarios, the store macros, and its own grey button) rebuilds the series from the chart configuration table and hides the rows of slots without results.
  - **Buttons:** core (green): Recalculate now, Recalculation on/off, Run stored scenarios, Update data tables; others (grey): Store baseline, Store live scenario, Solve ETS, Clear stored, Sort stored outputs, Group blank scenarios, Refresh dashboard charts, First-run test.
  - **ScenarioDefinition:** short names row 2 (Base, CP20, CP20-b, PkgA, PkgB, CP50); blank scenario columns P:AZ grouped and collapsed (macro `GroupBlankScenarios` as part of Run stored scenarios). Legacy rows unchanged. `StoreScenario` deletes an ID's rows wherever they are and appends (StoredOutputs may be sorted); `SortStoredOutputs` after every store.
  - **Fixed (v6.6 regression):** the build's batch copy blanked "the LAMBDA test group", which became the live group in v6.6, so v6.6 shipped scenarios 3-6 with empty stored results; the new quick-check test catches it.
  - **Formula length:** the longer sheet name pushed 21 scenario-1 lookups over 100 characters: names SDBase and SDParam. The MVP build now runs the Excel lint (it caught a name, SD1Val, that reads as a cell).
- **Checks:** quick check PASS (output codes against v6.5 unchanged, 7e-15); Excel lint clean; macros SortStoredOutputs, GroupBlankScenarios, RefreshDashboard run without error in LibreOffice (chart behaviour only testable in Excel).
- **Caveats:** the key table's 5th indicator is net welfare (% of GDP), not household burden: distribution results are not stored per scenario. CP20 (ID 2, the live scenario) has no stored results by design (Stored shows 1, 3-6; Live shows 1-2). LibreOffice previews re-evaluate cells and show 0 where Excel shows the stored #N/A/blank. The full check (`check_v6_4.py`) still tests the v6.4 dashboard layout: updated in v7.0.

## 2026-10-22 - v7.0 (MVP): release - every file at 7.0, full rebuild, checks repaired

- **Task (user 2026-10-20, overnight plan, release 3 of 4):** commit the full version upgrade, full rebuild and check with adjustments, every document at 7.0.
- **Outputs:** every current `_v6_4`/`_v6_5`/`_v6_7` script and note renamed `_v7_0` (old copies in `Old/`); `CPAT-AI-Mitigation-MVP-v7.0.xlsm` (now in `Old/`, superseded by v7.1); references updated in 69 files; documents regenerated (Formulas, replication lists, register, BUGSandISSUES, tracker).
- **Fixes found by the rebuild and the checks:**
  - **Check recalculation:** since v6.6 the shipped file is in manual calculation; LibreOffice left the formulas of an openpyxl copy uncalculated, and its recalculation on load gives wrong trailing averages of the power fuel prices (fpp, then swi, swd: up to 31%). `check_v7_0.py` now copies the file in automatic calculation and recalculates in a UNO session (calculateAll), as the build does.
  - **Batch:** the first definition of each LibreOffice session was stored 5e-5 off (first calculateAll after loading); the batch worker now calculates once after loading. Paste test: every pasted group equals its stored results (1e-12).
  - **Python reference:** the end-user power price floor (sheet since v5.6) was missing; the methane calibration (ghg.k) now uses the stored baseline, as the sheet (v6.2, I47), also in the tests that change a global setting.
  - **Check layout:** check_charts and check_compare rewritten for the v6.7 dashboard; uniformity and LAMBDA checks for two groups (group 2 = the LAMBDA group); quick check's baseline of the last release recalculated with its LAMBDAs expanded; paste test numbering.
- **Checks:** quick check PASS (13,396 output codes equal v6.7); paste test PASS; full check: sections 0-5 OK after the fixes; the last full run was interrupted (container pause) and is rerun after v7.1.
- **Caveats:** results unchanged from v6.7. The LibreOffice load-recalculation fault matters only to checks (Excel and the build use full recalculations).

## 2026-10-22 - v7.1 (MVP): nine data tabs linked to the data workbook

- **Task (user 2026-10-21, release 4 of 4):** link the relevant tables to the database (the data workbook), going ahead with the recommendations; test on the repository version.
- **Outputs:** `CPAT-AI-Mitigation-MVP-v7.1.xlsm` (and the root copy), `build_v7_1.py`, `CPATScenarios_v7_1.bas` (v7.0 ones to `Old/`), `check_links_v7_1.py` and `check_links_report_v7.1.md`; `data/scripts/build_data_workbook.py` adds `L_WEO`, `L_GDPRatios`, `L_HH_Elast`, `L_UNPop` through the CPAT-format converters; both data workbooks rebuilt.
  - **Links:** Balances, EnergyCons, Prices_dom, HHSurvey, IO_GTAP, HH_Elast (rows of the country); WEO, GDPRatios, UNPop (all rows: US CPI, regional fallbacks). Cover's link table has a Rows column (country / all).
  - **Macro:** `RefreshLink` loads the query in a staging sheet and copies by column name (any column order; header row and formula columns of the tab stay; missing columns reported; no rows = shipped data kept); the query table no longer sits on the tab.
- **Checks:** quick check PASS (output codes equal v7.0). Link test: A. identity (a data workbook from the MVP's own tabs, columns reversed, extra column, other countries' rows) gives back every cell of the nine tabs; B. the dummy data workbook: every link finds its table and every MVP column; after the dummy-price fix, all nine links leave the model without error values.
- **Caveats:**
  - **Dummy prices fixed (user 2026-10-22: invert negative prices):** the dummy `prices_dom.csv` had negative retail prices (8 for Egypt, e.g. `mit.rp.die.all` 2022 = -0.13), which gave #NUM! in the transport cost ratio (trbvu) and the price blocks. Negative `mit.rp.*` inverted (139 cells) and, as the MVP prices from supply cost + margin + tax, the tax `mit.txo.*` inverted where that sum was negative (400 cells: some fake subsidies became fake taxes). Both data workbooks and the legacy dummy rebuilt; data tests 15 and Coded CPAT tests 48 pass; the nine links now leave the model without error values.
  - **Not tested in Excel:** Power Query does not run in LibreOffice; the copy is emulated in Python exactly as the macro does it. First test in Excel: `Plans_v7_0.md` 8.4.
  - **Not linked:** GHGs, EF_GHG, CH4Inputs, Elasticities, Prices_int, OilProductShares, Transport1-2 (their MVP layout needs a converter).

## 2026-10-22 - v7.1 (MVP) fix: "Variable not defined" in StyleSeries (dashboard charts)

- **Task (user 2026-10-22):** Excel stopped at `s.Format.Line.Visible = msoTrue` (Variable not defined); check the VBA for similar issues.
- **Cause:** `msoTrue`, `msoLineDash`, `msoLineSolid` are Office-library constants; the embedded VBA project references only the Excel library and stdole, so under `Option Explicit` they are undefined (since v6.7, macro `RefreshDashboard`). LibreOffice Basic does not report them, so the macro run of the check passed.
- **Fix:** module constants `MSO_TRUE` (-1), `MSO_LINE_SOLID` (1), `MSO_LINE_DASH` (4) in `CPATScenarios_v7_1.bas`; v7.1 rebuilt (results unchanged, quick check PASS).
- **Sweep and new check:** every identifier of the module checked against its declarations, VBA keywords and built-ins, Excel object-model names and the xl/vb constants used (all real); no other undefined name. The quick check now runs this scan (`vba_names`); on the v7.0 module it reports the three Office constants.
- **Caveat:** the scan finds undefined names only; other Excel-only compile errors (wrong argument types, a member that does not exist) still show only in Excel (Debug > Compile VBAProject).

## 2026-10-22 - Norms: lessons register for LAMBDA and VBA issues; the norm to update the norms

- **Task (user 2026-10-22):** update the norms, add the norm to update norms in future, and apply it retrospectively to every LAMBDA and VBA issue found.
- **Outputs:**
  - Root `NORMS.md` section 6b (new): every bug class found (by a check or by the user) gets, in the same task, a norm, a check that fails on the old file, a look-back for other instances, a register row and a "Norm:" line in its CAVEATS entry.
  - `excel_ai/NORMS.md`: 3h (new) VBA modules embedded by the build (only Excel and VBA names; declarations first; no silent errors and restore the calculation mode; no volatile cells for macros; round-trip of generated strings; Excel-only behaviour listed as untested; Power Query via a staging sheet); 3i (new) testing LAMBDAs and values without Excel (expand LAMBDAs for both releases, two `calculateAll`, automatic calculation first, the LAMBDA group tested by results, tests by group number); 3j (new) lessons register: 17 LAMBDA and VBA issues from the distribution workbook to v7.1, each with its norm and check.
  - QuickStart: first-run step asks for Debug > Compile VBAProject.
- **Norm:** this entry is the norm itself (root 6b; Excel 3h-3j).
- **Caveats:** the register is built from CAVEATS and LESSONS_LEARNED; issues fixed before v1.07 without a CAVEATS entry may be missing. Two checks named in the register are review-only (volatile cells for macros; Excel compile, done by the user).

## 2026-10-21 - User document: AC
- **Task:** Update local `main` to the latest `origin/main` and add a Word document named for the user with the user's name as its content.
- **Inputs:** `users/Readme.txt`; user-provided name `AC`.
- **Outputs:** `users/AC.docx`; local `main` fast-forwarded to `efd90ae`.
- **Caveats:** None.

## 2026-10-22 - v7.1 (MVP) fix: stored results of the batch recalculated twice

- **Found by:** the full check (stored IDs 4 and 5 against the independent Python recomputation: 2.4e-3 and 1.1e-4).
- **Cause:** one LibreOffice `calculateAll` after copying a definition into the live column leaves small differences (the v7.0 fix covered only the first run after loading).
- **Fix:** `lo_session_v7_0.Session.calc` runs `calculateAll` twice (the build's batch, the checks, the value sessions); v7.1 rebuilt. Stored IDs 4 and 5 now equal Python (1.4e-11, 1.5e-13); live output codes unchanged (quick check PASS, 0 change); paste test PASS. The shipped StoredOutputs values of IDs 3-6 change by up to 2.4e-3 relative.
- **Norm:** `excel_ai/NORMS.md` 3i.2 sharpened (every recalculation is two `calculateAll`), register 3j row updated.

## 2026-10-22 - Documentation consolidated; one core deck; speed and size measured by the user

- **Task (user 2026-10-22):** one folder for decks, documents and bugs, with the bug-fix plans as a subfolder; drop the overlap between the documentation and the register; check the decks are current (e.g. bug counts); one core presentation; a clean top level. User measurements: recalculation about 5 s (legacy about 10 s); file about 10 MB as .xlsb, 12-13 MB expected with all country data and the remaining modules (legacy over 21 MB).
- **Outputs:**
  - `documentation/` holds everything: the core deck, the Documentation, the register; `bugfixes/` (was `legacy_bugfix_plans/`), `presentations/` (other decks; `Old/`: overview v6.3, management briefing), `more/`, `research/` (was `_research/`), `Old/`. `templates/` moved to `excel_ai/templates/` (build finds it). Top level: the root notes, the workbook, `coded`, `data`, `excel_ai`, `documentation`, `users`. References updated.
  - Documentation docx no longer repeats the register: chapters "Legacy CPAT: bug fixes needed" and the road model's "bugs and decisions" and appendices LegacyDiff and upgrades removed; a pointer chapter instead.
  - Core deck `documentation/CPAT-AI-Mitigation-MVP_Overview_v7.1.pptx` (17 slides): the MVP overview merged with the management briefing; counts from the register (159 bugs: 128 mitigation, 31 distribution; 62 issues: 52 and 10; the v6.3 overview said 126); v7.0+ names; status, speed and size (user's measurements), linked data; what remains.
  - Replication lists and LegacyBugFixes keep the v7_0 note names (the generators wrote `_v7_1` names).
- **Caveats:** the deck's speed and size figures are the user's Excel measurements, not reproduced here. The AI and climate fiscal tools deck (v2.6) stays in `presentations/` as a separate deck.

## 2026-10-22 - Codes increment R0-R9 (v7.2): MVP codes follow the CPAT code protocol

- **Task (user 2026-10-22):** go through the codes TODO (`excel_ai/plans/TODO_Codes.md`, plan `Codes_Remediation_Plan_v7_1.md`) step by step, with quick checks, a commit per step.
- **Inputs:** the crosswalk `data/mvp_legacy_extracts/codes_crosswalk_v7_1.csv` (only evidenced rows applied), the protocol (CodesMap sheet Protocol, C1-C11), v7.1 as the release to compare against.
- **Outputs:**
  - Rename map `data/mvp_legacy_extracts/code_renames_v7_2.csv` (kinds variable, codevar, codeend, member, row; ~260 rows): R1 no model letters; R2 power (`gen_mwy`, `nid`, `rec`, `xac`); R3 prices (`ps`, `etsnew`, `pbc`, `fadtx`, `cs`, `inc.ela.adj`, `tcp`); R4 transport (`stockcalc`, `shrcalc`, `shract`, `pass`/`fre`/`motor`/`all` `.vkt`/`.own`, `fecon`, `tot.rod`; members `pass`, `motor`); R5 emissions (`em.*`, `<pol>.tot`, `<gas>.tot`); R6 fiscal (`rev.usd.tot`, `rev.sr.usd`, `wel.*`, `gdp.pct.tot`); R7 150 total rows `tot`, power totals `<var>.pow.tot`, the 18 copy rows carry no code (0 duplicates, was 17); R8 LiveOutputs alias column (v7.1 stem) and macro `UpgradeStoredCodes`; R9 checks, `legacy_compare`, register I75 and L131-L133, protocol checks C1/C5/C7/C10 in `check_quick`.
  - Mechanism (`build_v7_2.py`): Mitigation columns A-C keep the internal members (lookups, LAMBDAs and `MTRowKey` read them; only column A takes variable renames); the code formula reads the code variable (Variables column L, `VCode`) and the pair's code slots (Mapping column G, `MSlot`); the 512 rows the map codes on its own read a row-code table (Mapping I-J, `RowKey`/`RowCode`); at most 96 characters. A full LibreOffice recalculation takes 31.8 s (v7.1: 30.5 s); a first design with one 6,700-row code table took 51 s and timed out the CheckBatch test.
  - `check_codes_v7_2.py`: every cell of v7.2 equals v7.1 through the map; the 272,860 numbers of Mitigation and LiveOutputs recalculated equal v7.1; the codes the workbook computes equal the map's; alias column checked.
- **Caveats:**
  - The full check found a silent FAIL in v7.0/v7.1: section 2 required 7 leakage variables (12 since v6.x); fixed, and unlogged conditions now log FAIL lines.
  - Open (TODO_Codes): crosswalk rows marked review (R3, R5 `ch4.em`, `co2.sec`, `apf.all.all`; R6 `rnew`, `rsub`, `gdp.*`...); C6 vocabularies; legacy MTOutputs code as a second alias; `coded` `ele` -> `ecy` (changes the shared data); the protocol's single-letter qualifiers (`fpr.s`, `etsb.t`) stay.
  - `ap.all.<pol>` is `em.tot.<pol>` (a total, C5), not the crosswalk's `em.all.<pol>`; `ap.<sector>.<pol>` keeps the crosswalk's `em.<sector>.all.<pol>`; `aps.all.<pol>` keeps its old code (it would equal `ap.all.<pol>`).

## 2026-10-22 - Other-mitigation bug plan split into sections (`excel_ai/legacy/bugfixes/`)
- `Legacy_CPAT_BugFix_OtherMitigation.docx` now holds both batches (82 entries) in 10 sections by model area (macro/GDP, prices and subsidies, GHG and pollutants, regulations and feebates, ETS and carbon pricing, fuel use, NDC, balance of payments, revenue, manual inputs), each with its own summary table and cell plans; sections ordered roughly by priority, bugs High/Medium/Low within. Codes unchanged. The `_2` docx and pdf were removed (content merged).
- Built by `tools/render_other.js` from `data/cfg_other_sections.json`; the fix JSONs are unchanged. Section assignment and the order within a priority are judgement calls.
- **Caveats:** the summary row of L124 and L66 reads "None: not reproduced" because their fixes sit under L82 and L43 (duplicate entries), as before.

## 2026-10-22 - One register, Word and JSON, with every cell plan (`documentation/`)
- `documentation/CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.docx` was missing the cell plans of other-mitigation batch 2 and of distribution (D1-D31): `make_bugfix_book_v7_0.py` read only three of the five plan files, so 91 bugs showed "Cell plan: not written yet". It now reads all five; only L129 and L130 have no plan yet. L126, L127 (power plan) are typed as engineer power.
- Section 3.3 (other mitigation) follows the 10 areas of `excel_ai/legacy/bugfixes/data/cfg_other_sections.json` in rough priority order, one table and set of cell plans per area (L129 added to prices, L130 to NDC); N1, N2 sit in their area.
- New `documentation/CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.json`: the whole register (legacy, distribution and prototype bugs with their cell plans, issues, LegacyDiff, upgrades), written by the same script.
- The separate Word and PDF plans in `excel_ai/legacy/bugfixes/` were removed (duplicates of section 3); their JSON sources and tools stay. README pointers updated (the root README still named the retired v6_3 register).
- **Caveats:** `BUGSandISSUES_v7_0.xlsx` stays, because `update_tracker_v7_0.py` fills the CPAT team's tracker from it. `LegacyBugFixes_v7_0.md` and `make_legacy_fixes_v7_0.py` still name the v6.4 register file (regenerate at the next release).

## 2026-10-22 - Bugs and issues register renamed v7.1.5 (`documentation/`)
- `CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.5.docx` and `.json` replace the v7.1 files (same content, regenerated; user asked for a new version number so the update is visible). The register now has its own version, `REGISTER_VERSION` in `issues_register_v7_0.py`; the workbook stays v7.1. References updated (READMEs, QuickStart, deck builder, make_docs, update_tracker); the title page states the register version and date.

## 2026-10-22 - Clean-up and restructure; v8.0 (prototype naming, stable names, few documents)

- **Task (user 2026-10-22):** a total rethink of the repository and its documents, after v7.2 reached main: no `documentation/` folder, no `cpat_` prefix, the three main files at the top of `excel_ai/`, short lists `BUGS.md`/`ISSUES.md`, history dropped, versioned and `_latest` copies, few and simple documents; the mitigation MVP renamed a prototype.
- **Outputs:**
  - Layout: `excel_ai/` (workbook, bug-fix register, register spreadsheet, deck as `_latest`; `releases/` with the `_v<n>` copies from v7.2; `mitigation/` sources and checks; `legacy/` legacy workbooks, fix-plan sources and tools, surveys, finished codes work; `plans/` one file per open plan and the TODO; `shared/`, `templates/`), `data/`, `coded/`, `other/`. Git history reset to one commit (`2fb1c31`); `Old/` folders and earlier variants deleted.
  - v8.0: `CPAT-AI-Mitigation-Prototype`; scripts and notes with stable names; one NORMS (sections 0-8; section 5 rewritten); `CHANGELOG.md`; documents: a 5-page Documentation (`docs/Documentation.md`) and a Methods volume (13 method notes merged into 6 chapters + distribution, equations and data tabs appendices).
  - Checks: data tests 15 pass, Python tests 48 pass, quick check PASS (0 change vs v7.2), paste test PASS, full check PASS (sections 0-13 in the run; section 14 rerun after its version rule was rewritten for stable names).
- **Caveats:**
  - Seven old session branches remain on GitHub with the old history (deleting them was refused by the permission system): delete them on GitHub to drop the history there.
  - `LegacyBugFixes.md` stays as an intermediate source of the register spreadsheet; the replication lists and the register are regenerated from `issues_register.py`.
  - The method chapters are mechanical merges of the notes (one section per former note); their text is not yet rewritten for flow.

## 2026-10-22 - Legacy fixes in CPAT 1.0pre_465 checked (`excel_ai/bugsfixed/`)
- **Task (user 2026-10-22):** confirm the bugs the CPAT team marked fixed in `CPAT 1.0pre_465 - No Prop Data.xlsb`; split `FixedBugsToConfirm.txt` into "Confirmed fixed" and "Fixed with caveats"; mark each heading of the bug register `CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.5_fixedbugs.docx` in red.
- **Inputs:** the 465 and 456 legacy workbooks (converted to xlsx with LibreOffice; formulas that use defined names cross-checked with pyxlsb2, because LibreOffice drops those names); the cell plans of the register (formula now, new formula, fill range, policy copy). Rows were matched between 456 and 465 by their labels and codes.
- **Outputs:** `FixedBugsToConfirm.txt` (52 confirmed, 12 with caveats; moved up from caveats: L11, L57, L83, L90, L124, L125; moved down: L62, L63, L84, L87, L95, L115, I18, I29); the docx headings carry red "CONFIRMED / FIXED WITH CAVEATS / NOT FIXED in 465" marks and a red note where there is a caveat, plus a red summary under "Legacy version" in section 1. The sections of the checked bugs are moved whole out of sections 3 and 4: confirmed fixes to a new Appendix C (last), fixes with caveats to a new Appendix B (headings become Heading 2). `legacy465_check.json` holds the results; `update_tracker.py` writes them to the new column S "Status in legacy 465" of `legacy/workbooks/Tracking issues.xlsx` (codes not in the list: "Not marked fixed"). That rerun also brought the tracker up to date with the register (v8.0 wording "prototype", method references, cell-plan flags, 4 new codes).
- **Caveats:**
  - Not fixed in 465: L62 (L1760:AE1762 unchanged) and L63 (lookup still stops at ECP row 403).
  - L115 changed to the wrong row (K$1735, existing carbon tax fuel rate for biomass, instead of K$1715).
  - L95 cleared row 3719, but P2823:AE2823 and M2836:AE2836 (and the policy copies on $M10035) still read it: the additional power-demand efficiency now drops out there.
  - L45 kerosene leg (M5588, M5590) not as planned; L16 only in L1868; L87 dropped the E2189="Yes" test; L84 option text unchanged; L56 still Sri Lanka; L109 real Low/Vhigh series still missing.
  - Formula text was compared, not results: nothing was recalculated (no Excel on Linux). From about row 5590 down, 465 rows sit 15 rows above the 456 rows the register quotes.
  - The register itself (`issues_register.py`, `BUGS.md`) is not updated with "fixed in legacy 465"; that is the next step (register section 2.7).

## 2026-10-22 - Modules M1-M3: v8.1 and the standalone Distribution v1.0

- **Task (user 2026-10-22):** modular CPAT: Distribution, air pollution and transport co-benefits become modules; first consistent money units (M1), the prototype's exports (M2) and the standalone Distribution module (M3, the priority). One scenario at a time; no interaction with the batch runs.
- **Inputs:** the prototype v8.0; plan `excel_ai/plans/Modules.md`.
- **Outputs:**
  - Prototype v8.1 (`excel_ai/releases/CPAT-AI-Mitigation-Prototype_v8.1.xlsm`, `_latest`): one money-unit vocabulary (NORMS section 3); section 15 moved to the end; section 19 Exports to modules, 19a Distribution (plain copies, defined name `ExportDistn`); tab `FromMitigation`, Distribution's only Mitigation input. Quick check PASS (0 change vs v8.0), paste test PASS.
  - Distribution module v1.0 (`excel_ai/distribution/`; `excel_ai/CPAT-AI-Distribution-Prototype_latest.xlsm`, `releases/..._v1.0.xlsm`): cut from the built prototype (tabs Cover, ScenarioDefinition with only the distribution rows shown, FromMitigation as values, Distribution, Settings, the distribution data tabs; 66 of 768 names kept); VBA `CPATDistribution.bas` (UpdateFromMitigation, RecalculateNow, ToggleRecalculation). `check_distribution.py` PASS: Distribution equals the prototype's (25,190 cells); FromMitigation equals 19a through the macro's row mapping; end to end (live carbon price 60 instead of 20, prototype recalculated, module updated and recalculated: 0 differences, 4,670 values moved); VBA scan; lint.
- **Caveats:**
  - The macro UpdateFromMitigation is tested by a Python emulation of its copy, not run in Excel (Excel 365 review, TODO section 5). It opens the mitigation workbook read-only with macros off and the calculation manual, or uses it as it stands if it is open.
  - 41 Settings formulas that read dropped tabs (country lists, GHG and WEO lookups) are values of Egypt; the module's data tabs have no data-workbook link yet.
  - The module's ScenarioDefinition keeps every row (hidden but the distribution ones) so that the row numbers Distribution reads stay those of the prototype.
  - v8.1 is not on main yet (quick and paste checks only; a full check before main).

## 2026-10-22 - Interim register spreadsheet with the legacy 465 bug-fix status (`excel_ai/bugsfixed/`)
- **Outputs:** `excel_ai/bugsfixed/CPAT-AI_BugsAndIssues_interim_fixedbugs.xlsx`, a copy of `CPAT-AI_BugsAndIssues_latest.xlsx` with Status set from `legacy465_check.json` (the cell-by-cell check above): 52 "Confirmed fixed in legacy 465", 10 "Fixed with caveats in legacy 465", 2 "Not fixed in legacy 465" (L62, L63), the check's note in a new column L; all 64 refs matched; other rows keep their v8.0 status; ReadMe note added.
- **Caveats:**
  - Edited copy, not regenerated: the statuses are not in `issues_register.py`, so `make_documentation.py` does not carry them; add them to the register when the 465 fixes are accepted.

## 2026-10-22 - Bug fix plan: cell references moved to legacy 465 (`excel_ai/bugsfixed/`)
- **Task (user 2026-10-22):** update the cell references of the bug fix plan (`CPAT-AI-Mitigation-MVP_BugsAndIssues_v7.1.5_fixedbugs.docx`) from legacy 456 to the latest legacy file, CPAT 1.0pre_465; revenue section first.
- **Inputs:** 456 and 465 workbooks; row map built by aligning the rows of both files on their labels and codes (formula digits ignored). Mitigation: rows 1-5666 unchanged, rows 5667-5677, 5727-5728, 5856, 5880 and 8404 deleted, then -11, -13, -14 (rows 5881-8403) and -15 (8405 on); MTInputs rows 329-330 deleted, -2 from 331. The policy block now sits a uniform +6,316 below the baseline (456: +6,331 above row ~5667, +6,317 below).
- **Outputs (step 1, revenue):** section 3.3.9 (L70, L71, L72, L73, L75, L85) and L128: every reference in the legacy-cells, what-legacy-does, fix, note and cell-plan fields remapped; each "Formula now" checked against the 465 cell (all 18 cells hold the bug; L128 is already fixed in 465). Red note under the 3.3.9 heading.
- **Outputs (step 2, everything else):** all other L and N bug sections (130 sections in all, about 300 references changed), the legacy rows quoted in the issues (only text that speaks of legacy), section 2 (the copy-paste protocol now says +6,316 throughout; the L1 worked example and preflight line) and red notes: section 1 (what changed between 456 and 465), 3.4 (Distribution rows unchanged), L97 (the CPAT team deleted the iron & steel memo rows 5667-5677 and 5727-5728, so M5667 is gone). The L108 and L70 notes that said a pasted policy copy points 14 rows off now say a paste works (uniform offset).
- **Check:** of 326 plan cells, 187 still hold the bug at the new address, 110 are already fixed in 465, 25 are labels or values, 4 are new cells; 34 differ: bugs fixed differently in 465 (L2/L95, L16, L57, L87, L90, L112, L115, L45, L48, L56), L94 (rows changed by the L48 fix), L97 (deleted), and cells the LibreOffice conversion mangles or did not load (L50 arrays, L58/L59 nested IFNA: the bug is still there in the xlsb; L76, L101, L116, L117 on Multipliers and Elasticities: unchanged).
- **Caveats:** the Effect and In-the-prototype fields are left as they are (they quote values and prototype rows, not legacy rows). The register's sources (`issues_register.py` "Where in legacy", the JSON cell plans in `excel_ai/legacy/bugfixes/data/`, `BUGS.md`) still quote 456 rows: regenerating the register from them would bring the 456 references back.

## 2026-10-21 - Codes map for the prototype and the CPAT code protocol (logged 2026-10-23)
- **Task (user):** update the legacy codes map for the prototype, find where the prototype's codes differ from legacy, define the code protocol, and plan the remediation (carried out as R0-R9 on 2026-10-22, entry above).
- **Inputs:** `CPATMasterProcessesCodesAndDefaults.xlsx` (CodesAndLookups), legacy 456 (Mitigation, MTOutputs), MVP v7.1.
- **Outputs:** `excel_ai/legacy/codes/` (`make_codes_map_v7_1.py`, `CPAT_CodesMap_v7_1.xlsx` with protocol C0-C11, the plan, `TODO_Codes.md`); `data/mvp_legacy_extracts/codes_crosswalk_v7_1.csv`; NORMS fuel-code list corrected (`nga`, `ecy`).
- **Caveats:** user decisions: legacy variable names, self-consistent protocol structure, no model letters, `tot` for totals and `all` for unused slots, N2O `n2o.tot` and NOx `nox.tot` (legacy `nox.tot` holds N2O, its NOx row is coded `oc.tot.`). Leftovers are in `excel_ai/plans/TODO.md` section 4.

## 2026-10-23 - Tracking issues.xlsx: BUGS and ISSUES-OTHER tabs, status in legacy first (`excel_ai/legacy/workbooks/`)
- **Task (user 2026-10-23):** in the CPAT team's tracker, a divider AI-FOUND->>, then BUGS and ISSUE/OTHER tabs with the same columns, then a divider PRIOR->> before the team's own sheets; bugs focus on the status in legacy, Closed struck through, filtered to Open.
- **Outputs:** `update_tracker.py` now writes sheets AI-FOUND->>, BUGS (legacy bugs L, D: 162), ISSUES-OTHER (I, DI, M, LD: 147; Excel does not allow "/" in a sheet name), PRIOR->>, then CPAT_issues, CPAT-MT, Mit+Disn_DeepDive, MT_issues, Slicer_issues, CPAT_dev. The old BUGSandISSUES sheet is replaced (a rerun reads its rows back from the two new sheets). Same 20 columns in both; column B "Status in legacy" (bugs: Closed (fixed in 465) / Open (fixed with caveats in 465) / Open (marked fixed, not fixed in 465) / Open; others: Closed (resolved, dropped, retired, prototype bug fixed) / Open (accepted: as legacy, LegacyDiff)), C the 465 check note. Conditional formatting: rows whose B starts with "Closed" in grey strikethrough; the saved filter on B (not equal Closed*) hides them (52 bugs, 66 others).
- **Caveats:** "Open" for a bug means legacy still has it as far as we know: only the bugs the CPAT team marked fixed were checked in 465. The status of issues is the register's status, not a legacy check.

## 2026-10-23 - v8.2: register refresh to legacy 465, documents, tidy-up
- **Task (user 2026-10-23):** after the tracker restructure, the register refresh (sources moved from legacy 456 to the latest file, 465), then update all documents and tidy up to a full new version.
- **Inputs:** `CPAT 1.0pre_456_NoPropData.xlsb`, `CPAT 1.0pre_465 - No Prop Data.xlsb` (rows of both matched on labels and codes), `excel_ai/bugsfixed/legacy465_check.json` (the check of the CPAT team's fixes).
- **Outputs:**
  - Row map `excel_ai/legacy/bugfixes/data/rowmap_456_465.json` and tool `excel_ai/legacy/bugfixes/tools/remap_465.py` (JSON plans, Python string literals, text files; reports deleted rows). Applied to the four mitigation fix-plan files (cell, now, new, fill, policy, where, why, ref, note; effects untouched), `issues_register.py` and `make_legacy_fixes.py` (string literals; every change reviewed: all legacy rows; comments untouched). Plan check against 465: of 350 plan cells with a formula 187 still hold the bug, 111 are already fixed, 23 differ as explained in the register (bugs fixed differently, L94 changed by L48, L97 deleted, conversion artefacts L50/L58/L59). Notes on the old uneven policy offset (L43, L66, L70, L108) reworded: in 465 the policy block is +6,316 everywhere, so a paste works; L107 notes the CPAT team's own fix (Dashboard L57).
  - Register v8.2 (`make_bugfix_book.py`): every bug has a "Status in legacy" row (red when the CPAT team fixed it) and a red mark on its heading; the 52 confirmed fixes move whole to Appendix C (last), the 8 with caveats and the 2 not fixed to Appendix B; section 1 says what moved between 456 and 465; protocol 2.1 (+6,316), the L1 example (run on 456; 465 rows given), code ranges computed; JSON export with `legacy_465` per bug. I18 and I29 (prototype issues on the team's list) stay in section 4.
  - `BUGS.md`, `LegacyBugFixes.md`: column "In legacy 465"; register spreadsheet: column "Status in legacy 465" (and its version from version.json, was a fixed 7.0); tracker refreshed (v8.2).
  - Release v8.2 (workbook formulas unchanged; version-log row): `CPAT-AI-Mitigation-Prototype_v8.2.xlsm` and `_latest`, register `_v8.2.docx` and `_latest`, deck `_v8.2.pptx` and `_latest` (new screenshots v82_*; the legacy-bugs slide gives the 465 counts; stale note on the 459 file fixed), Documentation and Methods rebuilt. Checks: excel_lint clean; quick check PASS, 0 change in 13,396 output codes vs v8.1; paste test PASS (on the first v8.2 build; the second build changed only the version-log text).
  - Tidy-up: `excel_ai/bugsfixed/README.md`; the hand-edited register copy (`..._v7.1.5_fixedbugs.docx`) and the interim spreadsheet retired (the regenerated register and spreadsheet carry the same 465 results); old deck images v80_* removed; NORMS legacy-file table (465 added, 459 superseded, tracker tabs), TODO (465 done; follow-ups for the CPAT team and the data extracts), READMEs, CHANGELOG, `Data_request.md`, `BugFixProcedure.md` (465 note, stale link), `bugfixes/README.md`.
- **Caveats:**
  - Counts: the team marked 62 bugs fixed: 52 confirmed, 8 with caveats, 2 not fixed (L62, L63); the "12 with caveats" of `FixedBugsToConfirm.txt` also hold the prototype issues I18 and I29.
  - The prototype's data extracts (`extract_*.py`), `build.py` (LegacyDiff texts) and the Methods chapters still quote 456 rows on purpose (the prototype was built and checked against 456); the Documentation and the Methods volume say so. Moving them is a TODO item, after the numerical check on 465 (U2).
  - Distribution bugs (D1-D31) keep their rows: the Distribution sheet did not move. Nothing was recalculated in Excel (formula text compared).
