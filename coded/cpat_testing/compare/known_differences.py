"""Codes where Coded CPAT departs from Excel-AI's stored values on purpose: Coded CPAT fixes an Excel-AI prototype bug
that is still open in the prototype (root NORMS 0 rule 6; bugs are never replicated, issues are). The comparison tests
leave these codes out and check that they do differ. When Excel-AI ships the fix, delete the entry: the codes must then
match again (and Coded CPAT aligns with the prototype's fix). Today there are none: every prototype bug Coded CPAT found was fixed in Excel-AI 0.9.2 and Distribution 0.1.4.

Codes without the country prefix and the scenario: 'mit.<code>' or 'distn.<code>'.
"""
KNOWN = {}                       # none: Excel-AI 0.9.2 and Distribution 0.1.4 fixed M15-M17, M19-M22 (M18 withdrawn)
BY_CODE = {code: bug for bug, codes in KNOWN.items() for code in codes}


def bug_of(code):
    """The bug that makes a full output code (e.g. 'egy.mit.gdpn.all.lcu.2') differ, or None."""
    return BY_CODE.get(code.split('.', 1)[1].rsplit('.', 1)[0])
