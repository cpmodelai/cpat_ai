"""Codes where Coded CPAT departs from Excel-AI's stored values on purpose: Coded CPAT fixes an Excel-AI prototype bug
that is still open in the prototype (root NORMS 0 rule 6; bugs are never replicated, issues are). The comparison tests
leave these codes out and check that they do differ. When Excel-AI ships the fix, delete the entry: the codes must then
match again (and Coded CPAT aligns with the prototype's fix). Bugs without an entry change nothing for Egypt's
scenarios 1-2 (M15 VAT rate of the year, M16 freight BEV feebate distance, M20 World Bank gas series, M21 methane fee
cap); M17 is replicated until the prototype's fixed version.

Codes without the country prefix and the scenario: 'mit.<code>' or 'distn.<code>'.
"""
KNOWN = {
    'M19': ['mit.gdpn.all.lcu', 'mit.gdpn.all.usd'],                     # Coded CPAT = Excel-AI x 1e9 (WEO is in bn)
    'M22': [f'distn.{v}.{p}.dec.{s}' for v in ('hrec', 'hnet') for p in ('p25', 'p75') for s in ('ove', 'urb', 'rur')],
}
BY_CODE = {code: bug for bug, codes in KNOWN.items() for code in codes}


def bug_of(code):
    """The bug that makes a full output code (e.g. 'egy.mit.gdpn.all.lcu.2') differ, or None."""
    return BY_CODE.get(code.split('.', 1)[1].rsplit('.', 1)[0])
