"""The comparison harness works on the reference itself (every code equals itself) and finds a difference."""
from cpat_testing.compare.compare import compare, reference, summary


def test_reference_matches_itself_and_flags_a_change():
    ref = reference()
    sample = ref.loc[[c for c in ref.index if c.startswith('egy.mit.infl.') or c.startswith('egy.mit.defl.')]]
    rep = compare(sample, ref=ref)
    assert len(rep) == 4 and rep['first_bad'].isna().all()
    changed = sample.copy()
    changed.loc['egy.mit.infl.1', 2030] *= 1 + 1e-6
    assert summary(compare(changed, ref=ref)).loc['infl', 'failing'] == 1
