# Balonlama ve Ölçüm Raporu

Bu proje, PDF teknik resimlerinden ölçü metinlerini yakalayıp otomatik balon numarası atayan ve ölçüm raporu (CSV) üreten bir Python aracıdır. Sistem, metinde açık tolerans varsa otomatik algılar; tolerans yoksa ISO 2768 (fine/medium/coarse) sınıfına göre tolerans uygular.

> Not: Bu ilk sürüm PDF içindeki metin katmanını okur. Görsel balon çizimi veya OCR destekli ölçü tespiti bu iskelette yer almamaktadır.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Kullanım

```bash
balonlama input.pdf --iso-class medium --output rapor.csv
```

Parametreler:
- `--iso-class`: `fine`, `medium`, `coarse` (varsayılan: `medium`)
- `--output`: Çıktı CSV dosyası (varsayılan: `balonlama_raporu.csv`)

## Çıktı

CSV sütunları:
- `balloon_id`: Balon numarası
- `nominal`: Nominal ölçü
- `tol_min`: Minimum tolerans (negatif değer)
- `tol_max`: Maksimum tolerans (pozitif değer)
- `method`: `explicit` (metinden) veya `iso_2768`
- `source_text`: Kaynak metin
