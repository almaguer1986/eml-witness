"""Shim sanity test — verify the deprecation re-export works."""
import pytest


def test_shim_imports_with_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="eml-witness is deprecated"):
        import eml_witness
    assert hasattr(eml_witness, "__version__")
    assert eml_witness.__version__ == "0.3.0"
