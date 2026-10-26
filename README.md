# automation-data-pipeline

A reusable, production-style **data ingestion & cleaning pipeline** for CSV/Excel
files. Built to demonstrate automation skills for an Automation Specialist role.

## What it does
- Ingests CSV / Excel files from a folder (or a single path)
- Cleans: trims whitespace, normalizes column names, fixes types, drops duplicates
- Validates: required columns, non-null checks, value ranges, regex patterns
- Transforms: derived columns, filtering, aggregation
- Exports: CSV / Excel / JSON with timestamped filenames
- Logs every step with retry + error handling

## Quick start
```bash
pip install -r requirements.txt
python -m src.pipeline --input data/sample_input.csv --output out/
```

## Run tests
```bash
pytest -q
```

## Configuration
Copy `config.example.yaml` to `config.yaml` and tweak. CLI flags override config.
