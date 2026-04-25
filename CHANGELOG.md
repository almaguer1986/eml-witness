# Changelog

## [0.1.0] — 2026-04-25 — Initial release

Universality-witness API composing eml-cost + eml-discover +
eml-rewrite. Single entry point `universality_witness(expr)`
returns a frozen `UniversalityWitness` dataclass with:

- `profile` — `WitnessProfile` (cost axes + fingerprint)
- `identified` — `WitnessIdentified | None` (top registry match)
- `canonical_path` — `list[WitnessTreeNode]` (rewrite sequence
  from input toward a lower-cost equivalent)
- `savings` — predicted_depth reduction along the path
- `verified_in_lean` — bool, defaults False; flips True once
  `EML_Universality.lean` lands AND the user verifies in VS
  Code lean4 extension
- `lean_url` — optional URL to the Lean source, set only when
  `verified_in_lean=True`

Plus `witness_to_dict(w)` for JSON serialisation.

### Tests

- 11 cases in `tests/test_witness.py` covering canonical sigmoid
  identification, textbook→canonical path, Pythagorean collapse,
  unknown expressions, Bessel non-EML flag, JSON round-trip,
  walk_canonical=False, explicit canonical_target, error paths,
  immutability.

### Status

Beta. mypy strict clean. No PyPI upload (per current gate);
local + GitHub only.
