# data-toolkit

A small, practical command-line toolkit I use to inspect, clean, and convert everyday datasets.

## Features

- Preview CSV and JSON files without opening a spreadsheet
- Summarize columns, missing values, and inferred data types
- Filter, select, rename, and sort fields
- Convert between CSV, JSON, and JSON Lines
- Stream large files with low memory usage
- Produce readable terminal output or machine-friendly results

## Install

Requires Python 3.10 or newer.

    git clone https://github.com/your-username/data-toolkit.git
    cd data-toolkit
    python -m pip install .

## Usage

Inspect a dataset:

    data-toolkit inspect data/customers.csv

Select columns and remove incomplete rows:

    data-toolkit clean data/customers.csv \
      --select name,email,country \
      --drop-missing email \
      --output build/customers.csv

Convert CSV to JSON Lines:

    data-toolkit convert data/customers.csv build/customers.jsonl

View all commands and options:

    data-toolkit --help