"""Phase 5.0: Coded CPAT's distribution module against the independent recomputation written for Excel-AI
(excel_ai/mitigation/checks/distribution_ref.py), given the same inputs from mitigation (scenario 2, Egypt)."""
from cpat_testing.compare.check_recomputations import distribution


def test_distribution_matches_distribution_ref():
    rows, worst, _ = distribution()
    missing = [k for k, d in rows if d is None]
    assert not missing, missing
    assert worst < 1e-9, [r for r in rows if r[1] >= 1e-9]
