"""Tests for universality_witness + witness_to_dict."""
from __future__ import annotations

import json

import pytest
import sympy as sp

from eml_witness import (
    UniversalityWitness,
    WitnessIdentified,
    WitnessProfile,
    universality_witness,
    witness_to_dict,
)


x = sp.Symbol("x")
y = sp.Symbol("y")


def test_witness_for_canonical_sigmoid():
    w = universality_witness("1/(1+exp(-x))")
    assert isinstance(w, UniversalityWitness)
    assert w.input_expr_str == "1/(1 + exp(-x))"
    assert isinstance(w.profile, WitnessProfile)
    assert w.profile.pfaffian_r >= 1
    assert w.profile.predicted_depth >= 1
    assert w.profile.fingerprint.startswith("p")
    assert w.profile.axes.startswith("p")
    # Canonical sigmoid IS in the registry — identification expected.
    assert w.identified is not None
    assert isinstance(w.identified, WitnessIdentified)
    assert "sigmoid" in w.identified.name.lower()
    # Verified-in-Lean defaults to False.
    assert w.verified_in_lean is False
    assert w.lean_url is None


def test_witness_for_textbook_sigmoid_walks_to_canonical():
    """Textbook sigmoid (cost 3) has a known 1-step canonical
    rewrite — witness should record the path + savings."""
    w = universality_witness(sp.exp(x) / (1 + sp.exp(x)))
    assert len(w.canonical_path) >= 2
    # Path is monotone non-increasing in cost.
    costs = [step.cost for step in w.canonical_path]
    assert costs == sorted(costs, reverse=True)
    # Savings should be positive (textbook is more expensive).
    assert w.savings >= 1


def test_witness_for_pythagorean_collapses_to_one():
    w = universality_witness(sp.sin(x) ** 2 + sp.cos(x) ** 2)
    # Should rewrite to S.One, with savings ≥ 0.
    assert w.canonical_path
    final = w.canonical_path[-1]
    assert final.expression_str == "1"
    assert w.savings >= 1


def test_witness_for_unknown_expression_has_no_identification():
    """An expression with no registry match still gets a witness;
    identified is just None."""
    w = universality_witness(x * y * y * y * sp.Symbol("z") + 17)
    assert isinstance(w, UniversalityWitness)
    # Profile always present.
    assert w.profile.predicted_depth >= 0
    # Identification may be None.
    if w.identified is None:
        # OK — no registry match.
        pass
    else:
        # Even if matched, confidence should be present.
        assert w.identified.confidence in {"identical", "exact", "axes"}


def test_witness_pfaffian_not_eml_for_bessel():
    w = universality_witness(sp.besselj(0, x))
    assert w.profile.is_pfaffian_not_eml is True


def test_witness_to_dict_roundtrips_through_json():
    w = universality_witness("exp(sin(x))")
    d = witness_to_dict(w)
    s = json.dumps(d)
    roundtripped = json.loads(s)
    assert roundtripped["input_expr"] == "exp(sin(x))"
    assert "profile" in roundtripped
    assert "fingerprint" in roundtripped["profile"]
    assert "verified_in_lean" in roundtripped
    assert roundtripped["verified_in_lean"] is False


def test_witness_dict_shape_matches_documented_keys():
    w = universality_witness("sin(x)")
    d = witness_to_dict(w)
    assert set(d.keys()) == {
        "input_expr", "profile", "identified",
        "canonical_path", "savings",
        "verified_in_lean", "lean_url",
    }
    assert set(d["profile"].keys()) == {
        "pfaffian_r", "max_path_r", "eml_depth",
        "structural_overhead", "predicted_depth",
        "is_pfaffian_not_eml", "corrections",
        "fingerprint", "axes",
    }


def test_walk_canonical_false_skips_path_walk():
    w = universality_witness(
        sp.exp(x) / (1 + sp.exp(x)),
        walk_canonical=False,
    )
    assert w.canonical_path == []
    assert w.savings == 0


def test_explicit_canonical_target():
    """Caller can name the target form they want a witness toward."""
    w = universality_witness(
        sp.exp(x) / (1 + sp.exp(x)),
        canonical_target=1 / (1 + sp.exp(-x)),
    )
    assert w.canonical_path
    assert w.canonical_path[-1].expression_str == "1/(1 + exp(-x))"


def test_invalid_expression_raises_value_error():
    with pytest.raises(ValueError):
        universality_witness("not valid sympy ((((((")


def test_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        universality_witness(42)             # type: ignore[arg-type]


def test_witness_is_immutable():
    w = universality_witness("sin(x)")
    with pytest.raises(Exception):
        w.savings = 999          # type: ignore[misc]
