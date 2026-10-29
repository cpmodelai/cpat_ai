# Coded CPAT: developer guide

The developer guide is now the **Coded CPAT documentation** (the website's Coded CPAT tab, `docs/index.html#coded`), written in [`../guide/`](../guide/) and generated into a Quarto book by `docs/CPAT_coded_documentation_qmd/make_qmd.py`:

- **Part I, what you need to know:** quick start; the database (format and where it is); scenarios and inputs; results; editing the model; testing (with the current test status).
- **Part II, how it works:** architecture; the mitigation blocks; the distribution module; the app; versions and releases.
- **Appendices:** both equation lists, every database table, every input, every variable, the Excel-AI bugs and known differences, the spec, the Python norms, the plan, a glossary.

Edit the chapters in `coded/cpat_documentation/guide/`; then `python make_qmd.py` (add `--tests` to rerun the tests and update the status) and `quarto render` in `docs/CPAT_coded_documentation_qmd/`.
