# SQL Execution via SDK

This document covers SQL execution using the Databricks SDK, providing capabilities the CLI lacks for programmatic SQL operations.

## Quick Start

```python
from databricks.sdk import WorkspaceClient
from dbx_execution import SQLExecutor

# Create client and executor
client = WorkspaceClient()
executor = SQLExecutor(client)

# Execute SQL query
result = executor.execute_sql(
    query="SELECT COUNT(*) FROM sales_data",
    warehouse_id="your-warehouse-id"
)
```

## SQLExecutor Class

### Basic SQL Execution

**Execute simple query:**
```python
result = executor.execute_sql(
    query="SELECT product_id, SUM(revenue) FROM sales GROUP BY product_id LIMIT 10",
    warehouse_id="abc123def456",
    catalog="main",
    schema="analytics"
)

if result['status'] == 'SUCCESS':
    print(f"✅ Query completed in {result['execution_time']:.1f}s")
    print(f"📊 Rows returned: {result['row_count']}")

    # Access results
    for row in result['results']['data']:
        print(row)  # Dictionary with column names as keys
else:
    print(f"❌ Query failed: {result['error']}")
```

**Execute SQL from file:**
```python
result = executor.execute_sql_file(
    file_path="./queries/monthly_report.sql",
    warehouse_id="abc123def456",
    catalog="production",
    schema="reporting"
)
```

### SQL Warehouse Management

**List available warehouses:**
```python
warehouses = executor.list_warehouses()
for warehouse in warehouses:
    print(f"Warehouse: {warehouse['name']} ({warehouse['id']})")
    print(f"  State: {warehouse['state']}")
    print(f"  Size: {warehouse['cluster_size']}")
    print(f"  Clusters: {warehouse['min_num_clusters']}-{warehouse['max_num_clusters']}")
```

**Check warehouse status:**
```python
status = executor.get_warehouse_status("abc123def456")
print(f"Warehouse '{status['name']}' is {status['state']}")
print(f"Health: {status['health']}")
```

**Test warehouse connection:**
```python
if executor.test_warehouse_connection("abc123def456"):
    print("✅ Warehouse connection working")
else:
    print("❌ Warehouse connection failed")
```

### Parameterized Queries

**Using query parameters:**
```python
result = executor.execute_sql(
    query="""
    SELECT *
    FROM sales
    WHERE date >= :start_date
      AND date <= :end_date
      AND region = :region
    """,
    warehouse_id="abc123def456",
    parameters={
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "region": "US"
    }
)
```

**Parameters in SQL files:**
```sql
-- queries/filtered_sales.sql
SELECT
    product_id,
    SUM(revenue) as total_revenue,
    COUNT(*) as transaction_count
FROM sales
WHERE
    date >= :start_date
    AND category = :category
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT :limit
```

```python
result = executor.execute_sql_file(
    file_path="./queries/filtered_sales.sql",
    warehouse_id="abc123def456",
    parameters={
        "start_date": "2024-01-01",
        "category": "Electronics",
        "limit": "50"
    }
)
```

### Context Management

**Set catalog and schema context:**
```python
result = executor.execute_sql(
    query="SHOW TABLES",
    warehouse_id="abc123def456",
    catalog="production",  # Sets USE CATALOG production
    schema="analytics"     # Sets USE SCHEMA analytics
)
```

**Multiple queries with context:**
```python
queries = [
    "CREATE TABLE IF NOT EXISTS temp_results AS SELECT * FROM source_table WHERE date = CURRENT_DATE()",
    "SELECT COUNT(*) as row_count FROM temp_results",
    "DROP TABLE temp_results"
]

for i, query in enumerate(queries):
    print(f"Executing query {i+1}/{len(queries)}")
    result = executor.execute_sql(
        query=query,
        warehouse_id="abc123def456",
        catalog="workspace",
        schema="temp"
    )
    if result['status'] != 'SUCCESS':
        print(f"❌ Query {i+1} failed: {result['error']}")
        break
```

### Result Processing

**Access query results:**
```python
result = executor.execute_sql(
    query="SELECT region, SUM(revenue) as total FROM sales GROUP BY region",
    warehouse_id="abc123def456"
)

if result['status'] == 'SUCCESS':
    results = result['results']

    # Column information
    columns = results['columns']
    print(f"Columns: {columns}")

    # Row data (list of dictionaries)
    data = results['data']
    print(f"Total rows: {len(data)}")

    # Process each row
    for row in data:
        region = row['region']
        total = row['total']
        print(f"Region {region}: ${total:,.2f}")
```

**Export results to DataFrame:**
```python
import pandas as pd

result = executor.execute_sql(
    query="SELECT * FROM sales WHERE date >= '2024-01-01'",
    warehouse_id="abc123def456"
)

if result['status'] == 'SUCCESS' and result['results']['data']:
    df = pd.DataFrame(result['results']['data'])
    print(f"DataFrame shape: {df.shape}")
    print(df.head())
else:
    print("No data returned")
```

### Advanced SQL Operations

**Execute complex analytical query:**
```python
analytical_query = """
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', sale_date) as month,
        product_category,
        SUM(revenue) as monthly_revenue,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM sales
    WHERE sale_date >= '2024-01-01'
    GROUP BY 1, 2
),
ranked_categories AS (
    SELECT
        month,
        product_category,
        monthly_revenue,
        unique_customers,
        ROW_NUMBER() OVER (PARTITION BY month ORDER BY monthly_revenue DESC) as revenue_rank
    FROM monthly_sales
)
SELECT *
FROM ranked_categories
WHERE revenue_rank <= 5
ORDER BY month, revenue_rank
"""

result = executor.execute_sql(
    query=analytical_query,
    warehouse_id="abc123def456",
    catalog="analytics",
    schema="reporting",
    timeout_seconds=600  # Longer timeout for complex queries
)
```

**Data quality checks:**
```python
quality_checks = [
    ("Row Count", "SELECT COUNT(*) as count FROM target_table"),
    ("Null Check", "SELECT COUNT(*) as nulls FROM target_table WHERE important_column IS NULL"),
    ("Duplicate Check", "SELECT COUNT(*) - COUNT(DISTINCT id) as duplicates FROM target_table"),
    ("Date Range", "SELECT MIN(date_column) as min_date, MAX(date_column) as max_date FROM target_table")
]

for check_name, query in quality_checks:
    result = executor.execute_sql(query, warehouse_id="abc123def456")
    if result['status'] == 'SUCCESS':
        data = result['results']['data'][0] if result['results']['data'] else {}
        print(f"{check_name}: {data}")
    else:
        print(f"❌ {check_name} failed: {result['error']}")
```

### Error Handling

**Handle common SQL errors:**
```python
result = executor.execute_sql(query, warehouse_id="abc123def456")

if result['status'] == 'FAILED':
    error_msg = result['error'].lower()

    if 'table or view not found' in error_msg:
        print("❌ Table doesn't exist - check catalog/schema/table name")
    elif 'permission denied' in error_msg:
        print("❌ Access denied - check Unity Catalog permissions")
    elif 'syntax error' in error_msg:
        print("❌ SQL syntax error - check query structure")
    elif 'timeout' in error_msg:
        print("❌ Query timeout - optimize or increase timeout")
    else:
        print(f"❌ SQL error: {result['error']}")

elif result['status'] == 'TIMEOUT':
    print(f"⏰ Query timed out after {result['timeout_seconds']}s")
    print("Consider: optimizing query, adding LIMIT, or increasing timeout")
```

## Integration Patterns

**Combine with notebook execution:**
```python
# Execute SQL to prepare data
sql_result = executor.execute_sql(
    query="CREATE OR REPLACE TABLE temp_analysis_data AS SELECT * FROM raw_data WHERE date = CURRENT_DATE()",
    warehouse_id="abc123def456"
)

if sql_result['status'] == 'SUCCESS':
    # Run notebook that uses the prepared data
    from dbx_execution import NotebookExecutor
    notebook_executor = NotebookExecutor(client)
    notebook_result = notebook_executor.run_notebook(
        notebook_path="/path/to/analysis_notebook",
        parameters={"source_table": "temp_analysis_data"}
    )
```

**CLI + SDK workflow:**
```bash
# Use CLI for workspace setup
databricks workspace upload ./query.sql /Shared/queries/daily_report.sql

# Execute via SDK for programmatic control
python -c "
from databricks.sdk import WorkspaceClient
from dbx_execution import SQLExecutor

client = WorkspaceClient()
executor = SQLExecutor(client)

# Download and execute
import tempfile
with tempfile.NamedTemporaryFile(suffix='.sql', delete=False) as f:
    content = client.workspace.download('/Shared/queries/daily_report.sql')
    f.write(content)
    f.flush()

    result = executor.execute_sql_file(f.name, 'warehouse-id')
    print(f'Query status: {result[\"status\"]}')
"
```

## Best Practices

1. **Always specify warehouse_id** - required for SQL execution
2. **Use parameters** for dynamic queries instead of string formatting
3. **Set appropriate timeouts** - complex queries may need longer timeouts
4. **Handle large result sets** - consider LIMIT clauses for exploratory queries
5. **Use catalog/schema context** to avoid fully qualified names
6. **Test queries interactively** before automating
7. **Monitor warehouse costs** - larger warehouses cost more
8. **Cache results** when possible to avoid re-execution
9. **Use descriptive error handling** for better debugging