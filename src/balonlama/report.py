from __future__ import annotations

import csv
from pathlib import Path

from .models import Dimension


def write_csv_report(dimensions: list[Dimension], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "balloon_id",
            "nominal",
            "tol_min",
            "tol_max",
            "method",
            "source_text",
        ])
        for dimension in dimensions:
            writer.writerow([
                dimension.balloon_id,
                dimension.nominal,
                dimension.tol_min,
                dimension.tol_max,
                dimension.method,
                dimension.source_text,
            ])

    return path
