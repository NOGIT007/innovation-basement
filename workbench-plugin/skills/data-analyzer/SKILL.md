# Multi-Format Data Analyzer

**Version:** 1.0.0
**Author:** Kenneth Kusk
**Based on:** CSV Data Summarizer by coffeefuelbump

## Description

Intelligent data analysis skill that automatically processes CSV, JSON, and Parquet files with database-backed analytics. Designed for financial reconciliation, inventory analysis, and multi-dataset operations.

## Capabilities

### Supported Formats
- **CSV** - Comma-separated values
- **JSON** - JSON records or arrays
- **Parquet** - Columnar format for large datasets

### Intelligent Features
- **Automatic file detection** - Scans input folder and identifies relationships
- **Smart database selection** - Chooses DuckDB or SQLite based on workload
- **Schema analysis** - Inspects data structure before processing
- **SQL-powered analytics** - Runs reconciliation and analytical queries
- **Visual insights** - Generates correlation heatmaps and distributions
- **Comprehensive reporting** - Single markdown file with embedded images

## Database Selection Logic

### DuckDB (Primary Choice)
Selected when:
- Total dataset size > 10MB
- Row count > 100,000
- Parquet format detected
- Multiple files requiring joins
- Complex analytical queries needed
- Financial reconciliation workflows

**Ideal for:** Financial P&L analysis, inventory reconciliation, order/purchase matching, multi-period comparisons

### SQLite (Fallback)
Selected when:
- Small datasets < 1MB
- Simple single-table operations
- Row count < 100,000
- Basic lookups without aggregations

## Usage

### 1. Setup
```bash
# Install dependencies
uv pip install -r requirements.txt
```

### 2. Add Files
Place data files in the `input/` folder:
```
.claude/skills/data-analyzer/input/
├── financial_2024_q1.csv
├── inventory_current.json
└── orders_history.parquet
```

### 3. Run Analysis
```bash
cd .claude/skills/data-analyzer
python analyze.py
```

### 4. View Results
Find the analysis report in `/Users/kennetkusk/Documents/Output/{topic}/analysis/` folder:
- Markdown file with timestamp
- Embedded base64 images (no separate files needed)
- SQL query results
- Schema documentation

## Behavior Guidelines

### Automatic Execution
- **NO user prompts** - Analyzes immediately upon invocation
- **Intelligent defaults** - Detects file relationships automatically
- **Single response** - Delivers complete analysis at once

### File Relationship Detection
The analyzer intelligently determines how to process multiple files:

**Combined Analysis** (creates multi-table database):
- Files share common column names (e.g., `order_id`, `product_id`)
- Similar naming patterns (e.g., `sales_jan.csv`, `sales_feb.csv`)
- Time-series partitions requiring consolidation

**Separate Analysis** (independent processing):
- Unrelated datasets with no common structure
- Different domains (e.g., HR data + Sales data)
- No matching columns or naming patterns

### Analytical Queries

Automatically executes:
- **Row counts** - Total records per table
- **Null analysis** - Missing data detection per column
- **Duplicate detection** - Identifies duplicate keys
- **Numeric summaries** - Min, max, avg, sum for numeric columns
- **Categorical distributions** - Top values and frequencies
- **Cross-table reconciliation** - Compares matching columns across files

### Visualizations

Generates and embeds:
- **Correlation heatmaps** - Numeric column relationships
- **Distribution histograms** - Value frequency analysis
- **Time-series plots** - Temporal trends (if date columns exist)

## Dependencies

- `pandas>=2.0.0` - Data manipulation
- `matplotlib>=3.7.0` - Visualization
- `seaborn>=0.12.0` - Statistical graphics
- `duckdb>=0.9.0` - Analytical database (OLAP)
- `pyarrow>=14.0.0` - Parquet file support

## Output Format

### Markdown Report Structure
```markdown
# Data Analysis Report

## 📁 Input Files
- File names, formats, sizes

## 🔗 File Relationship Analysis
- Combined vs separate strategy
- Reasoning

## 🗄️ Database Selection
- DuckDB or SQLite
- Selection rationale

## 📋 Data Schema
- Table structures
- Column types, nulls, uniqueness
- Potential keys

## 📊 Analytical Queries
- SQL queries with results
- Reconciliation findings
- Data quality checks

## 📈 Visualizations
- Embedded base64 images
- No separate file management needed

## ✅ Summary
- Total rows, columns
- Database used
- Queries executed
```

## Use Cases

### Financial Reconciliation
```
input/
├── bank_transactions.csv
├── accounting_ledger.csv
└── invoice_records.json
```
**Result:** Multi-table analysis identifying discrepancies, matching transactions, detecting duplicates

### Inventory Analysis
```
input/
├── current_stock.csv
├── purchase_orders.parquet
└── sales_history.json
```
**Result:** Cross-table reconciliation showing inventory flow, order fulfillment rates, stock levels

### Time-Series Analysis
```
input/
├── sales_q1_2024.csv
├── sales_q2_2024.csv
├── sales_q3_2024.csv
└── sales_q4_2024.csv
```
**Result:** Combined dataset with temporal trends, quarterly comparisons, growth analysis

## Prohibited Behaviors

**NEVER:**
- Ask "What would you like to do with this data?"
- Request user input for analysis preferences
- Split analysis into multiple responses
- Create separate image files (use embedded base64 only)
- Process files outside the `input/` directory
- Overwrite existing output reports (use timestamps)

## Required Actions

**ALWAYS:**
- Scan input folder automatically
- Detect file relationships intelligently
- Select appropriate database
- Execute comprehensive analytical queries
- Generate single markdown report with embedded images
- Save output with timestamp
- Provide clear summary of findings

## Example Invocation

**User:** "Analyze my financial data"

**Claude:** *Automatically loads skill, scans input folder, detects CSV and JSON files, creates DuckDB database, runs reconciliation queries, generates report*

"✅ Analysis complete! Report saved to: /Users/kennetkusk/Documents/Output/{topic}/analysis/analysis_report_20241109_143022.md

Found 3 files totaling 45.2MB. Used DuckDB for analytical processing. Executed 12 queries including duplicate detection and cross-table reconciliation. Report includes correlation heatmaps and distribution analysis with embedded visualizations."

## Notes

- Designed for financial operations: reconciliation, variance analysis, audit trails
- Optimized for multi-file workflows common in accounting and inventory management
- Database remains in-memory (not persisted after analysis)
- All outputs use markdown with base64-encoded images for portability
- Timestamps prevent overwriting previous analyses

## Version History

**1.0.0** (2024-11-09)
- Initial release with DuckDB/SQLite support
- Multi-format file loading (CSV, JSON, Parquet)
- Intelligent relationship detection
- Schema analysis and documentation
- SQL-powered reconciliation queries
- Embedded base64 visualizations
- Single markdown report output
