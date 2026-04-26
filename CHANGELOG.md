# Changelog

## [0.1.1] — 2026-04-25 — Audit fixes (deep freeze + targeted exception handling)

### Changed
- **`UniversalityWitness.canonical_path` is now `tuple[WitnessTreeNode, ...]`**
  (was `list[...]`). The previous list field made the supposedly
  "frozen" dataclass shallowly mutable in place — callers could
  `.append()` to the path. Tuples close that hole. CHANGED API
  signature; consumers iterating with `for step in w.canonical_path`
  are unaffected.
- Replaced bare `except Exception` blocks in
  `universality_witness()` with targeted `(ImportError,
  AttributeError, RecursionError)` (best-rewrite import) and
  `(ValueError, RecursionError, AttributeError)` (path walk) so
  real failures surface instead of silently masking as "no path".

### Tests
- 12 cases — `test_walk_canonical_false_skips_path_walk` updated
  to assert `()` not `[]`. `test_witness_is_immutable` tightened
  to catch `dataclasses.FrozenInstanceError` specifically and to
  assert the tuple invariant on `canonical_path`.

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
