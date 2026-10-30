"""Switchable demand equations (D4): the scenario input ModelForm chooses the form that fills each slot.

A block calls `slot(name, inputs)` and gets the function of the chosen form; it never calls a form directly.
Only the CPAT form (Excel-AI) is built (spec section 7).
"""
from cpat_model.forms.registry import SLOTS, slot, register  # noqa: F401
from cpat_model.forms import cpat  # noqa: F401,E402  (registers the CPAT form)
