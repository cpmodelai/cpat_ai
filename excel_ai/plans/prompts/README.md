# Prompts to build the modules

Prompts for GitHub Copilot (or any AI agent) to build or finish the CPAT-AI modules, following [`NORMS.md`](../../../NORMS.md) section 9 (how modules work) and section 0 (never replicate a legacy bug; always replicate a legacy issue, and track it). Each prompt works in phases, one message per phase, and stops for review after each. You only type the short **starter prompt** (`<Module>_starter_prompts.md`, which also has the follow-up prompts); the long `<Module>_module_prompt.md` is the brief Copilot reads from the repo.

| Module | Starter and follow-up prompts | Full prompt (Copilot reads it) | Guide for people (Word: the prompt, step-by-step Copilot instructions with screenshots, SyncRepo.bat) | Status |
|---|---|---|---|---|
| Transport co-benefits | [`TCB_starter_prompts.md`](TCB_starter_prompts.md) | [`TCB_module_prompt.md`](TCB_module_prompt.md) | `CPAT-AI_Prompt_TransportCobenefits.docx` | New module; two modes (`Legacy`, `Engineer`) |
| Air pollution | [`AP_starter_prompts.md`](AP_starter_prompts.md) | [`AP_module_prompt.md`](AP_module_prompt.md) | `CPAT-AI_Prompt_AirPollution.docx` | Started (v0.3 scaffold); this prompt finishes it |
| Distribution | [`Distribution_starter_prompts.md`](Distribution_starter_prompts.md) | [`Distribution_module_prompt.md`](Distribution_module_prompt.md) | `CPAT-AI_HowTo_Distribution.docx` | Built (v0.1.3); this prompt links it through `permalink_countryeditable/` and checks it on legacy 465 |

Each module also has a two-page Word **quick guide** (`CPAT-AI_<Module>_QuickGuide.docx`: how to start, the starter queries, the phases, the follow-ups), written from the starter file by `make_quick_guides.py`, small enough to e-mail. The Word guides are written by `make_prompt_guides.js` (screenshots in `img/`: the GitHub Copilot app screenshots of `other/SetupGuide.docx`, and illustrations of the prompt box and of SyncRepo.bat). Run order of the modules and how they link: `NORMS.md` 9.3-9.4.
