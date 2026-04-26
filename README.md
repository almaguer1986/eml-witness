# eml-witness — ARCHIVED

> **🗄  This package is archived as of 2026-04-25 (E-129 consolidation).**
>
> The functionality has been folded into the main `monogate` package
> as of `monogate 2.4.0+`. New users should install:
>
> ```bash
> pip install monogate[witness]
> ```
>
> and use:
>
> ```python
> from monogate.witness import universality_witness
> # or, equivalently (via lazy alias on the package root):
> from monogate import universality_witness
> ```
>
> The standalone `eml-witness` PyPI / GitHub package is **frozen at
> 0.2.0** and will receive no further updates. Existing installs
> continue to work, but please migrate to `monogate[witness]` for
> ongoing improvements.
>
> See [monogate's CHANGELOG entry for 2.4.0](https://github.com/almaguer1986/monogate/blob/master/python/CHANGELOG.md#240--2026-04-25--universality-witness--cli--jupyter-folded-in)
> for details.

---

# eml-witness (historical)

Universality witnesses for elementary functions over the EML
routing tree. A *witness* is a finite, structured certificate
that an expression admits an EML routing tree — composed of the
expression's Pfaffian profile, its closest registry match (if
any), and a rewrite path to a lower-cost equivalent (if one
exists).

```python
from eml_witness import universality_witness

w = universality_witness("1/(1+exp(-x))")
print(w.profile.predicted_depth)       # 2
print(w.identified.name)               # 'sigmoid (canonical)'
print(w.verified_in_lean)              # False (until Lean lands)
```

Serialise to JSON:

```python
from eml_witness import witness_to_dict
import json
print(json.dumps(witness_to_dict(w), indent=2))
```

## Lean integration

`verified_in_lean` defaults to `False` and is the link to the
formal half of the universality story. It will flip to `True`
once `EML_Universality.lean` lands in the `monogate-lean`
repository AND the user has personally verified the file via
the VS Code lean4 extension (per the project's
`feedback_lean_writing_protocol_2026_04_25` rule).

When verified, the upstream consumer can patch the witness
post-construction:

```python
w = universality_witness("sin(x)")
w_verified = dataclasses.replace(
    w,
    verified_in_lean=True,
    lean_url="https://github.com/almaguer1986/monogate-lean/blob/main/MonogateEML/Universality.lean",
)
```

## Why a separate package?

The witness API composes three other packages:

| Provided by | Used for |
|---|---|
| `eml-cost` | profile (analyze + fingerprint + fingerprint_axes) |
| `eml-discover` | identification |
| `eml-rewrite` | canonical path + best-rewrite walk |

Putting it as a leaf-level package keeps the dependency story
clean: the eml-* substrate stays unchanged, and downstream
clients (`eml-explore`, `eml-jupyter`, `eml-vscode`,
`eml-discover-server`) can pull witness-shaped data through
one entry point.

## Status

Beta. v0.1.0. Patent pending.
