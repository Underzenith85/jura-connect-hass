"""Component-side brew helpers.

Only the framework-free per-product *preference* shape lives here. All brew
protocol logic — product tables, machine-definition XML decoding and the
16-byte ``@TP:`` recipe-blob construction — lives in the ``jura_connect``
backend library (``load_profile`` / ``ProductDef.build_recipe_hex``), keeping
this Home Assistant component a thin UI over that library.
"""

from __future__ import annotations

from .prefs import BREW_PARAMS, product_prefs, remember_param, selection_for_product
from .recipe import PRESELECTION_LABELS, build_recipe, encodable_preselections

__all__ = [
    "BREW_PARAMS",
    "product_prefs",
    "remember_param",
    "selection_for_product",
    "PRESELECTION_LABELS",
    "build_recipe",
    "encodable_preselections",
]
