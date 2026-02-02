from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Dimension:
    balloon_id: int
    nominal: float
    tol_min: float
    tol_max: float
    method: str
    source_text: str
