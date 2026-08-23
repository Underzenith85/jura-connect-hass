"""Product-recipe construction shared by the brew button and service."""

from __future__ import annotations

from collections.abc import Mapping

from jura_connect import MachineProfile, ProductDef

PRESELECTION_TRANSLATION_KEYS = {
    "coldbrew",
    "double",
    "fakesweetfoam",
    "lightbrew",
    "powder",
    "strongcoldbrew",
    "sweetfoam",
    "xtrashot",
}


def encodable_preselections(profile: MachineProfile, product: ProductDef) -> dict[str, str]:
    """Return canonical-name -> UI-label mappings the profile can encode.

    Some machine XMLs advertise controls that J.O.E. never puts on the wire.
    Let the library planner reject those so Home Assistant does not offer a
    control that would silently do nothing.
    """
    result: dict[str, str] = {}
    for name in sorted(product.preselections):
        try:
            profile.plan_preselections(product, [name])
        except ValueError:
            continue
        # Known values stay stable so Home Assistant can translate them via
        # entity.select.brew_preselection.state. Unknown future profile values
        # still get a readable fallback instead of leaking snake_case.
        result[name] = name if name in PRESELECTION_TRANSLATION_KEYS else name.replace("_", " ").title()
    return result


def build_recipe(
    profile: MachineProfile,
    product: ProductDef,
    overrides: Mapping[str, int | str] | None = None,
    preselection: str | None = None,
) -> str:
    """Build a recipe with one optional, profile-validated preselection."""
    plan = profile.plan_preselections(product, [preselection] if preselection else ())
    return plan.product.build_recipe_hex(
        dict(overrides or {}),
        preselect_mask=plan.mask,
        preselect_bytes=plan.byte_overwrites,
    )
