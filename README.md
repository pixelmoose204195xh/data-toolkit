# data-toolkit

A personal collection of practical utilities for cleaning, transforming, and inspecting everyday datasets.

## Features

- Load and export common data formats
- Clean missing, duplicate, and inconsistent values
- Filter, sort, and transform records
- Generate quick dataset summaries
- Combine reusable operations into repeatable workflows

## Install

```bash
git clone https://github.com/your-username/data-toolkit.git
cd data-toolkit
python -m pip install -e .
```

## Usage

```python
from data_toolkit import load_data, summarize

data = load_data("data/example.csv")
print(summarize(data))
```

This is a personal project built around the data tasks I use most often.