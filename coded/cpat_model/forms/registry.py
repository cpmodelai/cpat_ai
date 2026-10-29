"""The forms registry: FORMS[form][slot] = function."""

SLOTS = ('fuel_demand', 'electricity_demand', 'service_price')
FORMS = {}
DEFAULT_FORM = 'CPAT'


def register(form, slot_name):
    assert slot_name in SLOTS, slot_name

    def deco(fn):
        FORMS.setdefault(form, {})[slot_name] = fn
        return fn
    return deco


def slot(slot_name, inputs=None):
    form = DEFAULT_FORM
    if inputs is not None and 'ModelForm' in inputs.values and inputs.values['ModelForm']:
        form = inputs.values['ModelForm']
    if form not in FORMS or slot_name not in FORMS[form]:
        raise NotImplementedError(f'ModelForm {form!r} has no {slot_name} equation yet (only CPAT is built)')
    return FORMS[form][slot_name]
