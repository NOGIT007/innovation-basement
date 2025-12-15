# Multi-Format Data Analyzer

Intelligent data analysis skill with database-backed analytics for CSV, JSON, and Parquet files.

## Quick Start

### 1. Install Dependencies

```bash
cd .claude/skills/data-analyzer
uv pip install -r requirements.txt
```

### 2. Add Your Data Files

Place files in the `input/` folder:

```bash
.claude/skills/data-analyzer/input/
├── your_data.csv
├── more_data.json
└── big_data.parquet
```

### 3. Run Analysis

```bash
python3 analyze.py
```

The analysis report will be generated in `/Users/kennetkusk/Documents/Output/{topic}/analysis/` with a timestamp.

## Supported Formats

- **CSV** - Comma-separated values
- **JSON** - JSON records or arrays
- **Parquet** - Columnar format for large datasets

## Features

### Intelligent Database Selection

The analyzer automatically chooses the best database:

**DuckDB** (for most cases):
- Large datasets (>10MB)
- Many rows (>100K)
- Parquet files
- Multiple tables requiring joins
- Complex analytical queries

**SQLite** (fallback):
- Small datasets (<1MB)
- Simple operations
- Few rows (<100K)

### Automatic File Relationship Detection

The analyzer intelligently determines how to process files:

- **Combined**: Files with matching columns or naming patterns
- **Separate**: Unrelated datasets with different structures

### Comprehensive Analysis

- Schema documentation with data types and sample values
- Data quality checks (nulls, duplicates)
- Numeric summaries (min, max, avg, sum)
- Categorical distributions
- Cross-table reconciliation
- Correlation heatmaps
- Distribution visualizations

### Single Markdown Report

All results in one file with:
- Embedded base64 images (no separate image files)
- SQL query results in tables
- Complete schema documentation
- Timestamped filename

## Example Use Cases

### Financial Reconciliation

```
input/
├── bank_transactions.csv
├── accounting_ledger.csv
└── invoices.json
```

Automatically detects matching columns and runs reconciliation queries.

### Inventory Analysis

```
input/
├── current_stock.csv
├── purchase_orders.parquet
└── sales_history.json
```

Cross-table analysis showing inventory flow and fulfillment rates.

### Time-Series Data

```
input/
├── sales_q1_2024.csv
├── sales_q2_2024.csv
├── sales_q3_2024.csv
└── sales_q4_2024.csv
```

Combines quarterly data for temporal trend analysis.

## Output Structure

Reports include:

1. **File Overview** - Names, formats, sizes
2. **Relationship Analysis** - How files are connected
3. **Database Selection** - Which DB was chosen and why
4. **Schema Documentation** - Complete data dictionary
5. **Analytical Queries** - SQL results with insights
6. **Visualizations** - Embedded charts and graphs
7. **Summary** - Key statistics and findings

## Test Files

Two sample files are included in `input/`:

- `financial_transactions.csv` - Bank transactions with categories
- `inventory_stock.json` - Product inventory with pricing

Run the analyzer on these to see how it works!

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- duckdb >= 0.9.0
- pyarrow >= 14.0.0

## Notes

- Database operates in-memory (not persisted)
- All visualizations embedded as base64 in markdown
- Previous reports are preserved (timestamped filenames)
- Designed for financial operations and reconciliation workflows

## Version

1.0.0 - Initial release (2024-11-09)
