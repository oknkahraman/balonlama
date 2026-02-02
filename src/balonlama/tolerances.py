from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IsoToleranceBand:
    minimum: float
    maximum: float
    fine: float
    medium: float
    coarse: float


ISO_2768_LINEAR_TABLE = [
    IsoToleranceBand(0.5, 3.0, 0.05, 0.1, 0.2),
    IsoToleranceBand(3.0, 6.0, 0.05, 0.1, 0.3),
    IsoToleranceBand(6.0, 30.0, 0.1, 0.2, 0.5),
    IsoToleranceBand(30.0, 120.0, 0.15, 0.3, 0.8),
    IsoToleranceBand(120.0, 400.0, 0.2, 0.5, 1.2),
    IsoToleranceBand(400.0, 1000.0, 0.3, 0.8, 2.0),
    IsoToleranceBand(1000.0, 2000.0, 0.5, 1.2, 3.0),
    IsoToleranceBand(2000.0, 4000.0, 0.8, 2.0, 4.0),
]


def apply_iso_2768(nominal: float, iso_class: str) -> tuple[float, float]:
    """Return (tol_min, tol_max) for ISO 2768 linear tolerances.

    iso_class must be one of: fine, medium, coarse.
    """
    iso_class = iso_class.lower().strip()
    if iso_class not in {"fine", "medium", "coarse"}:
        raise ValueError("iso_class must be one of: fine, medium, coarse")

    band = next(
        (
            item
            for item in ISO_2768_LINEAR_TABLE
            if nominal > item.minimum - 1e-9 and nominal <= item.maximum
        ),
        None,
    )
    if band is None:
        band = ISO_2768_LINEAR_TABLE[-1]

    tolerance_value = getattr(band, iso_class)
    return -tolerance_value, tolerance_value
