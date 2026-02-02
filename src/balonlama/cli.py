from __future__ import annotations

import argparse
from pathlib import Path

from .parser import extract_dimensions_from_pdf
from .report import write_csv_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PDF teknik resim balonlama ve ölçüm raporu üretimi"
    )
    parser.add_argument("pdf_path", help="Girdi PDF dosyası")
    parser.add_argument(
        "--iso-class",
        default="medium",
        choices=["fine", "medium", "coarse"],
        help="ISO 2768 tolerans sınıfı",
    )
    parser.add_argument(
        "--output",
        default="balonlama_raporu.csv",
        help="Çıktı CSV dosyası",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        raise SystemExit(f"PDF bulunamadı: {pdf_path}")

    dimensions = extract_dimensions_from_pdf(
        str(pdf_path),
        iso_class=args.iso_class,
    )
    if not dimensions:
        raise SystemExit("Ölçü bulunamadı. PDF metin katmanı boş olabilir.")

    output_path = write_csv_report(dimensions, args.output)
    print(f"Rapor oluşturuldu: {output_path}")


if __name__ == "__main__":
    main()
