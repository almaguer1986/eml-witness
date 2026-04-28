"""eml-witness — DEPRECATED.

This package has been consolidated into ``eml-cost`` as the
:mod:`eml_cost.witness` subpackage. The standalone distribution
will receive no further updates.

Migration:

    pip uninstall eml-witness
    pip install "eml-cost[witness]>=0.15.0"

    # then change your imports:
    # OLD:  from eml_witness import X
    # NEW:  from eml_cost.witness import X

This shim re-exports the public API from ``eml_cost.witness`` so
existing code keeps working while you migrate.
"""
from __future__ import annotations

import warnings as _warnings

_warnings.warn(
    "eml-witness is deprecated. Use `pip install \"eml-cost[witness]\"` "
    "instead. The functionality is now available at eml_cost.witness. "
    "This package will receive no further updates.",
    DeprecationWarning,
    stacklevel=2,
)

from eml_cost import witness as _impl  # noqa: E402

# Mirror the upstream public API so `from eml_witness import X` keeps
# working. We deliberately avoid `from eml_cost.witness import *`
# to keep `__all__` faithful to whatever the new home declares.
__all__ = list(getattr(_impl, "__all__", []))
for _name in __all__:
    globals()[_name] = getattr(_impl, _name)
del _name, _impl

# Override any upstream __version__ — this shim has its own version line.
__version__ = "0.3.0"
