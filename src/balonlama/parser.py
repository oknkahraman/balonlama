from __future__ import annotations

import re
from typing import Iterable

import pdfplumber

from .models import Dimension
from .tolerances import apply_iso_2768


DIMENSION_PATTERNS = [
    re.compile(
        r"(?P<nominal>\d+(?:[\.,]\d+)?)\s*±\s*(?P<tol>\d+(?:[\.,]\d+)?)"
    ),
    re.compile(
        r"(?P<nominal>\d+(?:[\.,]\d+)?)\s*\+?(?P<plus>\d+(?:[\.,]\d+)?)\s*/\s*-?(?P<minus>\d+(?:[\.,]\d+)?)"
    ),
    re.compile(
        r"(?P<nominal>\d+(?:[\.,]\d+)?)\s*\+?(?P<plus>\d+(?:[\.,]\d+)?)\s*-\s*(?P<minus>\d+(?:[\.,]\d+)?)"
    ),
]


def _to_float(raw: str) -> float:
    return float(raw.replace(",", "."))


def _find_matches(text: str) -> Iterable[re.Match[str]]:
    for pattern in DIMENSION_PATTERNS:
        yield from pattern.finditer(text)


def _parse_match(match: re.Match[str]) -> tuple[float, float, float]:
    groups = match.groupdict()
    nominal = _to_float(groups["nominal"])

    if "tol" in groups and groups["tol"] is not None:
        tol = _to_float(groups["tol"])
        return nominal, -tol, tol

    plus = _to_float(groups["plus"])
    minus = _to_float(groups["minus"])
    return nominal, -minus, plus


def extract_dimensions_from_text(
    text: str, iso_class: str, start_balloon: int = 1
) -> list[Dimension]:
    dimensions: list[Dimension] = []
    seen = set()
    balloon_id = start_balloon

    for match in _find_matches(text):
        nominal, tol_min, tol_max = _parse_match(match)
        key = (nominal, tol_min, tol_max, match.group(0))
        if key in seen:
            continue
        seen.add(key)
        dimensions.append(
            Dimension(
                balloon_id=balloon_id,
                nominal=nominal,
                tol_min=tol_min,
                tol_max=tol_max,
                method="explicit",
                source_text=match.group(0).strip(),
            )
        )
        balloon_id += 1

    if not dimensions:
        return []

    return dimensions


def extract_dimensions_from_pdf(
    pdf_path: str, iso_class: str, start_balloon: int = 1
) -> list[Dimension]:
    dimensions: list[Dimension] = []
    balloon_id = start_balloon
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if not text.strip():
                continue

            explicit = extract_dimensions_from_text(text, iso_class, balloon_id)
            if explicit:
                dimensions.extend(explicit)
                balloon_id = explicit[-1].balloon_id + 1

            tokens = re.findall(r"\d+(?:[\.,]\d+)?", text)
            for token in tokens:
                nominal = _to_float(token)
                key = (nominal,)
                if key in {(d.nominal,) for d in dimensions}:
                    continue
                tol_min, tol_max = apply_iso_2768(nominal, iso_class)
                dimensions.append(
                    Dimension(
                        balloon_id=balloon_id,
                        nominal=nominal,
                        tol_min=tol_min,
                        tol_max=tol_max,
                        method="iso_2768",
                        source_text=token,
                    )
                )
                balloon_id += 1

    return dimensions
