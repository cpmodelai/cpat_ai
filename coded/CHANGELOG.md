# Changelog: Coded CPAT

One row per release, newest last (root `NORMS.md` 5b). The version is `<Excel-AI version>p<Python version>` (D14): the Python version of the replication of that Excel-AI version. Full notes: `../CAVEATS.md`. Git tag: `coded-v<version>`.

| Version | Date | Description | Max abs diff against Excel-AI |
|---|---|---|---|
| 0.9.1p0.1 | 2026-10-29 | First release. Replicates Excel-AI 0.9.1 (mitigation, every Mitigation sheet section incl. the road engineer model, welfare and efficient prices) and Distribution 0.1.3, readable first (one function per equation of the equation list); one entry point `cpat_model.run` for the command line (`run_model.py`), the Shiny app and the tests; reruns compute only changed scenarios (one country, two scenarios 0.8 s). Excel-AI prototype bugs are not replicated: M15, M16, M19, M20, M21, M22 fixed in Python (M17 follows the prototype's fix; M18 withdrawn). | Egypt, scenarios 1-2, 2022-2041: every output code within 1e-9 (relative above 1) except the known differences of the bugs fixed in Python: `gdpn` (x 1e9, M19) and 12 distribution percentile rows of group 2 (M22) (`cpat_testing/compare/known_differences.py`) |
