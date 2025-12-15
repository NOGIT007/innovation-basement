"""
Multi-Format Data Analyzer with Intelligent Database Selection
Supports CSV, JSON, Parquet with DuckDB/SQLite backend for financial analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import duckdb
import sqlite3
from pathlib import Path
import json
import base64
from io import BytesIO
from typing import List, Dict, Tuple, Optional
import re


class DataAnalyzer:
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.db_conn = None
        self.db_type = None
        self.files_info = []
        self.visualizations = []

    def scan_input_files(self) -> List[Dict]:
        """Scan input directory for CSV, JSON, and Parquet files"""
        supported_formats = {'.csv', '.json', '.parquet', '.pq'}
        files = []

        for file_path in self.input_dir.iterdir():
            if file_path.suffix.lower() in supported_formats:
                files.append({
                    'path': file_path,
                    'name': file_path.stem,
                    'format': file_path.suffix.lower().replace('.', ''),
                    'size': file_path.stat().st_size
                })

        return sorted(files, key=lambda x: x['name'])

    def load_file_to_dataframe(self, file_info: Dict) -> pd.DataFrame:
        """Load file into pandas DataFrame based on format"""
        path = file_info['path']
        fmt = file_info['format']

        if fmt == 'csv':
            return pd.read_csv(path)
        elif fmt == 'json':
            return pd.read_json(path)
        elif fmt in ['parquet', 'pq']:
            return pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def analyze_schema(self, df: pd.DataFrame, table_name: str) -> Dict:
        """Analyze dataframe schema and characteristics"""
        schema = {
            'table_name': table_name,
            'rows': len(df),
            'columns': len(df.columns),
            'column_info': [],
            'total_size_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'has_dates': False,
            'numeric_cols': [],
            'categorical_cols': [],
            'potential_keys': []
        }

        for col in df.columns:
            col_info = {
                'name': col,
                'dtype': str(df[col].dtype),
                'null_count': int(df[col].isnull().sum()),
                'null_pct': float(df[col].isnull().sum() / len(df) * 100),
                'unique_count': int(df[col].nunique()),
                'sample_values': df[col].dropna().head(3).tolist()
            }

            # Detect numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                schema['numeric_cols'].append(col)
                col_info['min'] = float(df[col].min()) if not df[col].isnull().all() else None
                col_info['max'] = float(df[col].max()) if not df[col].isnull().all() else None

            # Detect categorical columns
            if df[col].dtype == 'object' and df[col].nunique() < len(df) * 0.5:
                schema['categorical_cols'].append(col)

            # Detect potential keys (high uniqueness)
            if df[col].nunique() / len(df) > 0.95:
                schema['potential_keys'].append(col)

            # Detect date columns
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    pd.to_datetime(df[col], errors='coerce')
                    schema['has_dates'] = True
                    col_info['is_date'] = True
                except:
                    pass

            schema['column_info'].append(col_info)

        return schema

    def detect_file_relationships(self, files_info: List[Dict]) -> Dict:
        """Analyze if files should be combined or analyzed separately"""
        if len(files_info) <= 1:
            return {'strategy': 'single', 'groups': [files_info]}

        # Load small samples to detect relationships
        samples = {}
        for file_info in files_info:
            df = self.load_file_to_dataframe(file_info)
            samples[file_info['name']] = df.head(100)

        # Check for common column patterns
        all_columns = {name: set(df.columns) for name, df in samples.items()}

        # Look for matching patterns in names (e.g., orders_2024, inventory_2024)
        name_patterns = {}
        for name in all_columns.keys():
            base_name = re.sub(r'[_\-]\d{4}|\d{4}[_\-]', '', name)
            base_name = re.sub(r'[_\-](jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', '', base_name, flags=re.IGNORECASE)
            if base_name not in name_patterns:
                name_patterns[base_name] = []
            name_patterns[base_name].append(name)

        # Check for common join keys
        common_columns = set.intersection(*all_columns.values()) if len(all_columns) > 1 else set()
        potential_join_keys = [col for col in common_columns if 'id' in col.lower()]

        if potential_join_keys:
            return {
                'strategy': 'combined',
                'reason': f'Found common join keys: {", ".join(potential_join_keys)}',
                'join_keys': potential_join_keys,
                'groups': [files_info]
            }
        elif any(len(names) > 1 for names in name_patterns.values()):
            # Multiple files with similar names - likely time series or partitions
            return {
                'strategy': 'combined',
                'reason': 'Similar file naming patterns detected',
                'groups': [files_info]
            }
        else:
            return {
                'strategy': 'separate',
                'reason': 'No clear relationships detected',
                'groups': [[f] for f in files_info]
            }

    def select_database(self, schemas: List[Dict], has_parquet: bool) -> str:
        """Intelligently select DuckDB or SQLite"""
        total_rows = sum(s['rows'] for s in schemas)
        total_size_mb = sum(s['total_size_mb'] for s in schemas)
        multiple_tables = len(schemas) > 1
        has_analytics = any(len(s['numeric_cols']) > 3 for s in schemas)

        # Decision criteria
        use_duckdb = (
            total_size_mb > 10 or          # Larger datasets
            total_rows > 100000 or          # Many rows
            has_parquet or                  # Parquet format
            multiple_tables or              # Multi-file analysis
            has_analytics                   # Analytical workload
        )

        if use_duckdb:
            reason = []
            if total_size_mb > 10: reason.append(f"large dataset ({total_size_mb:.1f}MB)")
            if total_rows > 100000: reason.append(f"many rows ({total_rows:,})")
            if has_parquet: reason.append("Parquet format")
            if multiple_tables: reason.append("multiple tables")
            if has_analytics: reason.append("analytical workload")
            return 'duckdb', f"Selected DuckDB for: {', '.join(reason)}"
        else:
            return 'sqlite', f"Selected SQLite for small, simple dataset ({total_size_mb:.1f}MB, {total_rows:,} rows)"

    def create_database(self, db_type: str) -> None:
        """Create database connection"""
        self.db_type = db_type

        if db_type == 'duckdb':
            self.db_conn = duckdb.connect(':memory:')
        else:
            self.db_conn = sqlite3.connect(':memory:')

    def load_data_to_db(self, file_info: Dict, table_name: str) -> None:
        """Load data into database"""
        df = self.load_file_to_dataframe(file_info)

        if self.db_type == 'duckdb':
            self.db_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        else:
            df.to_sql(table_name, self.db_conn, if_exists='replace', index=False)

    def execute_analytical_queries(self, schemas: List[Dict]) -> List[Dict]:
        """Run analytical SQL queries for insights and reconciliation"""
        results = []

        for schema in schemas:
            table = schema['table_name']
            queries = []

            # Basic counts
            queries.append({
                'name': f'{table}: Row Count',
                'sql': f'SELECT COUNT(*) as total_rows FROM {table}'
            })

            # Null analysis
            if any(col['null_count'] > 0 for col in schema['column_info']):
                null_cols = [col['name'] for col in schema['column_info'] if col['null_count'] > 0]
                for col in null_cols[:5]:  # Limit to 5
                    queries.append({
                        'name': f'{table}: Nulls in {col}',
                        'sql': f'SELECT COUNT(*) as null_count FROM {table} WHERE "{col}" IS NULL'
                    })

            # Duplicate detection
            if schema['potential_keys']:
                key_col = schema['potential_keys'][0]
                queries.append({
                    'name': f'{table}: Duplicate {key_col}',
                    'sql': f'SELECT "{key_col}", COUNT(*) as count FROM {table} GROUP BY "{key_col}" HAVING COUNT(*) > 1 LIMIT 10'
                })

            # Numeric aggregations
            for col in schema['numeric_cols'][:5]:  # Limit to 5
                queries.append({
                    'name': f'{table}: {col} Summary',
                    'sql': f'SELECT MIN("{col}") as min, MAX("{col}") as max, AVG("{col}") as avg, SUM("{col}") as total FROM {table}'
                })

            # Categorical distributions
            for col in schema['categorical_cols'][:3]:  # Limit to 3
                queries.append({
                    'name': f'{table}: Top {col} Values',
                    'sql': f'SELECT "{col}", COUNT(*) as count FROM {table} GROUP BY "{col}" ORDER BY count DESC LIMIT 5'
                })

            # Execute queries
            for query in queries:
                try:
                    if self.db_type == 'duckdb':
                        result_df = self.db_conn.execute(query['sql']).fetchdf()
                    else:
                        result_df = pd.read_sql_query(query['sql'], self.db_conn)

                    results.append({
                        'name': query['name'],
                        'sql': query['sql'],
                        'result': result_df
                    })
                except Exception as e:
                    results.append({
                        'name': query['name'],
                        'sql': query['sql'],
                        'error': str(e)
                    })

        # Cross-table reconciliation if multiple tables
        if len(schemas) > 1:
            # Try to find matching columns for reconciliation
            table_cols = {s['table_name']: [c['name'] for c in s['column_info']] for s in schemas}
            common_cols = set.intersection(*[set(cols) for cols in table_cols.values()])

            if common_cols:
                for col in list(common_cols)[:2]:  # Limit to 2
                    tables = list(table_cols.keys())
                    if len(tables) >= 2:
                        queries.append({
                            'name': f'Cross-table: {col} comparison',
                            'sql': f'SELECT "{col}", COUNT(*) as count FROM {tables[0]} GROUP BY "{col}" LIMIT 5'
                        })

        return results

    def create_visualization(self, df: pd.DataFrame, chart_type: str, title: str) -> str:
        """Create visualization and return base64 encoded image"""
        plt.figure(figsize=(10, 6))

        if chart_type == 'correlation' and len(df.select_dtypes(include='number').columns) > 1:
            numeric_df = df.select_dtypes(include='number')
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0, square=True)
            plt.title(title)
        elif chart_type == 'distribution':
            numeric_cols = df.select_dtypes(include='number').columns[:4]
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            axes = axes.flatten()
            for idx, col in enumerate(numeric_cols):
                axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
                axes[idx].set_title(f'{col}')
                axes[idx].grid(True, alpha=0.3)
            plt.suptitle(title)

        plt.tight_layout()

        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()

        return f"data:image/png;base64,{image_base64}"

    def generate_markdown_report(self, files_info: List[Dict], schemas: List[Dict],
                                 relationship_info: Dict, db_info: Tuple[str, str],
                                 query_results: List[Dict]) -> str:
        """Generate comprehensive markdown report with embedded images"""
        md = []

        # Header
        md.append("# Data Analysis Report")
        md.append(f"\n*Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        md.append("---\n")

        # Files Overview
        md.append("## 📁 Input Files\n")
        for file in files_info:
            size_mb = file['size'] / 1024 / 1024
            md.append(f"- **{file['name']}.{file['format']}** ({size_mb:.2f} MB)")
        md.append("")

        # Relationship Detection
        md.append("## 🔗 File Relationship Analysis\n")
        md.append(f"**Strategy:** {relationship_info['strategy'].upper()}")
        md.append(f"\n**Reason:** {relationship_info['reason']}\n")

        # Database Selection
        md.append("## 🗄️ Database Selection\n")
        db_type, db_reason = db_info
        md.append(f"**Database:** {db_type.upper()}")
        md.append(f"\n**Rationale:** {db_reason}\n")

        # Schema Documentation
        md.append("## 📋 Data Schema\n")
        for schema in schemas:
            md.append(f"### Table: `{schema['table_name']}`\n")
            md.append(f"- **Rows:** {schema['rows']:,}")
            md.append(f"- **Columns:** {schema['columns']}")
            md.append(f"- **Size:** {schema['total_size_mb']:.2f} MB")

            if schema['potential_keys']:
                md.append(f"- **Potential Keys:** {', '.join(schema['potential_keys'])}")

            md.append("\n#### Column Details\n")
            md.append("| Column | Type | Nulls | Unique | Sample Values |")
            md.append("|--------|------|-------|--------|---------------|")

            for col in schema['column_info']:
                sample = ', '.join([str(v)[:20] for v in col['sample_values'][:2]])
                md.append(f"| {col['name']} | {col['dtype']} | {col['null_count']} ({col['null_pct']:.1f}%) | {col['unique_count']} | {sample} |")

            md.append("")

        # SQL Query Results
        md.append("## 📊 Analytical Queries\n")
        for result in query_results:
            md.append(f"### {result['name']}\n")
            md.append(f"```sql\n{result['sql']}\n```\n")

            if 'error' in result:
                md.append(f"❌ **Error:** {result['error']}\n")
            else:
                md.append(result['result'].to_markdown(index=False))
                md.append("")

        # Visualizations
        if self.visualizations:
            md.append("## 📈 Visualizations\n")
            for viz in self.visualizations:
                md.append(f"### {viz['title']}\n")
                md.append(f"![{viz['title']}]({viz['image_data']})\n")

        # Summary
        md.append("## ✅ Summary\n")
        total_rows = sum(s['rows'] for s in schemas)
        total_cols = sum(s['columns'] for s in schemas)
        md.append(f"- **Total Rows:** {total_rows:,}")
        md.append(f"- **Total Columns:** {total_cols}")
        md.append(f"- **Database Used:** {db_type.upper()}")
        md.append(f"- **Queries Executed:** {len(query_results)}")

        return "\n".join(md)

    def analyze(self) -> str:
        """Main analysis workflow"""
        # Step 1: Scan files
        files_info = self.scan_input_files()
        if not files_info:
            return "❌ No files found in input directory"

        # Step 2: Detect relationships
        relationship_info = self.detect_file_relationships(files_info)

        # Step 3: Analyze schemas
        schemas = []
        for file_info in files_info:
            df = self.load_file_to_dataframe(file_info)
            schema = self.analyze_schema(df, file_info['name'])
            schemas.append(schema)

        # Step 4: Select database
        has_parquet = any(f['format'] in ['parquet', 'pq'] for f in files_info)
        db_type, db_reason = self.select_database(schemas, has_parquet)

        # Step 5: Create database and load data
        self.create_database(db_type)
        for file_info in files_info:
            self.load_data_to_db(file_info, file_info['name'])

        # Step 6: Execute analytical queries
        query_results = self.execute_analytical_queries(schemas)

        # Step 7: Create visualizations
        for file_info in files_info:
            df = self.load_file_to_dataframe(file_info)

            # Correlation heatmap
            if len(df.select_dtypes(include='number').columns) > 1:
                viz_data = self.create_visualization(df, 'correlation',
                                                     f'Correlation Heatmap: {file_info["name"]}')
                self.visualizations.append({
                    'title': f'Correlation Heatmap: {file_info["name"]}',
                    'image_data': viz_data
                })

            # Distribution plots
            if len(df.select_dtypes(include='number').columns) > 0:
                viz_data = self.create_visualization(df, 'distribution',
                                                     f'Distributions: {file_info["name"]}')
                self.visualizations.append({
                    'title': f'Distributions: {file_info["name"]}',
                    'image_data': viz_data
                })

        # Step 8: Generate report
        report = self.generate_markdown_report(
            files_info, schemas, relationship_info,
            (db_type, db_reason), query_results
        )

        # Step 9: Save report
        output_file = self.output_dir / f"analysis_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_file.write_text(report)

        return f"✅ Analysis complete! Report saved to: {output_file}"


if __name__ == "__main__":
    import sys

    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"

    analyzer = DataAnalyzer(input_dir, output_dir)
    result = analyzer.analyze()
    print(result)
