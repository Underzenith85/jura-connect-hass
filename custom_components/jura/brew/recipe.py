"""Product-recipe construction shared by the brew button and service."""

from __future__ import annotations

from collections.abc import Mapping

from jura_connect import MachineProfile, ProductDef

PRESELECTION_LABELS: dict[str, str] = {
    "coldbrew": "Cold Brew",
    "double": "Double",
    "fakesweetfoam": "Sweet Foam",
    "lightbrew": "Light Brew",
    "powder": "Ground Coffee",
    "strongcoldbrew": "Strong Cold Brew",
    "sweetfoam": "Sweet Foam",
    "xtrashot": "Extra Shot",
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
        result[name] = PRESELECTION_LABELS.get(name, name.replace("_", " ").title())
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
