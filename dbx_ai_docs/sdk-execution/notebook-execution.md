# Notebook Execution via SDK

This document covers programmatic notebook execution using the Databricks SDK, complementing CLI-based workflows with execution capabilities.

## Quick Start

```python
from databricks.sdk import WorkspaceClient
from dbx_execution import NotebookExecutor

# Create client and executor
client = WorkspaceClient()
executor = NotebookExecutor(client)

# Execute notebook
result = executor.run_notebook(
    notebook_path="/path/to/notebook",
    parameters={"param1": "value1"}
)
```

## NotebookExecutor Class

### Basic Execution

**Execute existing workspace notebook:**
```python
result = executor.run_notebook(
    notebook_path="/Users/user@company.com/my_notebook",
    cluster_id="0123-456789-abcdef",  # Optional, uses serverless if None
    parameters={"input_table": "sales_data", "output_path": "/tmp/results"},
    timeout_seconds=600
)

if result['status'] == 'SUCCESS':
    print(f"✅ Execution completed in {result['execution_time']:.1f}s")
    print(f"🔗 View results: {result['run_page_url']}")
else:
    print(f"❌ Execution failed: {result['error']}")
```

**Execute local notebook:**
```python
result = executor.run_notebook_from_local(
    local_path="./notebooks/analysis.py",
    workspace_path="/Users/user@company.com/analysis",
    parameters={"date": "2024-01-15"},
    overwrite=True
)
```

### Compute Options

**Serverless execution (recommended):**
```python
# No cluster_id specified - uses serverless compute
result = executor.run_notebook("/path/to/notebook")
```

**Existing cluster execution:**
```python
# List available clusters
clusters = executor.list_clusters()
for cluster in clusters:
    if cluster['state'] == 'RUNNING':
        print(f"Available: {cluster['cluster_name']} ({cluster['cluster_id']})")

# Use specific cluster
result = executor.run_notebook(
    notebook_path="/path/to/notebook",
    cluster_id="0123-456789-abcdef"
)
```

### Parameter Passing

**Simple parameters:**
```python
parameters = {
    "input_date": "2024-01-15",
    "environment": "prod",
    "threshold": "0.95"
}

result = executor.run_notebook(
    notebook_path="/path/to/parameterized_notebook",
    parameters=parameters
)
```

**Access parameters in notebook:**
```python
# In your Databricks notebook
dbutils.widgets.text("input_date", "2024-01-01")
dbutils.widgets.text("environment", "dev")
dbutils.widgets.text("threshold", "0.8")

input_date = dbutils.widgets.get("input_date")
environment = dbutils.widgets.get("environment")
threshold = float(dbutils.widgets.get("threshold"))
```

### Result Handling

**Check execution status:**
```python
result = executor.run_notebook("/path/to/notebook")

match result['status']:
    case 'SUCCESS':
        print("✅ Notebook executed successfully")
        print(f"⏱️ Execution time: {result['execution_time']:.1f}s")
        print(f"🔗 Run URL: {result['run_page_url']}")

        # Get notebook output if available
        output = result.get('output', {})
        if output.get('result'):
            print(f"📄 Output: {output['result']}")

    case 'FAILED':
        print(f"❌ Execution failed: {result['error_message']}")
        print(f"🔗 Debug at: {result['run_page_url']}")

    case 'TIMEOUT':
        print(f"⏰ Execution timed out after {result['timeout_seconds']}s")

    case 'ERROR':
        print(f"❌ Setup error: {result['error']}")
```

### Advanced Features

**Execution with retry:**
```python
result = executor.run_notebook_with_retry(
    notebook_path="/path/to/notebook",
    max_retries=2,
    cluster_id="0123-456789-abcdef",
    timeout_seconds=300
)
```

**Validate notebook before execution:**
```python
if executor.validate_notebook_exists("/path/to/notebook"):
    result = executor.run_notebook("/path/to/notebook")
else:
    print("❌ Notebook not found in workspace")
```

**Test execution setup:**
```python
# Test with simple notebook
success = executor.test_simple_notebook("/path/to/test_notebook")
if success:
    print("✅ Execution environment working")
else:
    print("❌ Execution environment has issues")
```

## File Format Support

**Python notebooks (.py):**
```python
result = executor.run_notebook_from_local(
    local_path="./analysis.py",
    workspace_path="/Users/user@company.com/analysis"
)
```

**Jupyter notebooks (.ipynb):**
```python
result = executor.run_notebook_from_local(
    local_path="./exploration.ipynb",
    workspace_path="/Users/user@company.com/exploration"
)
```

**SQL notebooks (.sql):**
```python
result = executor.run_notebook_from_local(
    local_path="./queries.sql",
    workspace_path="/Users/user@company.com/queries"
)
```

## Error Handling

**Common error patterns:**
```python
result = executor.run_notebook("/path/to/notebook")

if result['status'] == 'FAILED':
    error_state = result.get('error_state')

    if error_state == 'USER_CANCELLED':
        print("❌ Execution was cancelled")
    elif error_state == 'FAILED':
        print("❌ Notebook execution failed - check notebook logic")
    elif error_state == 'TIMEDOUT':
        print("❌ Execution timed out - increase timeout or optimize notebook")
    else:
        print(f"❌ Unexpected error state: {error_state}")
```

**Troubleshooting tips:**
- Check notebook syntax before uploading
- Verify cluster permissions and state
- Ensure parameters match notebook widgets
- Use shorter timeouts for testing
- Check workspace path permissions

## Integration with CLI Workflows

**Upload via CLI, execute via SDK:**
```bash
# Upload notebook using CLI
databricks workspace upload ./my_notebook.py /Users/user@company.com/my_notebook

# Execute programmatically
python -c "
from databricks.sdk import WorkspaceClient
from dbx_execution import NotebookExecutor

client = WorkspaceClient()
executor = NotebookExecutor(client)
result = executor.run_notebook('/Users/user@company.com/my_notebook')
print(f'Status: {result[\"status\"]}')
"
```

## Best Practices

1. **Use serverless compute** for most executions (simpler, auto-scaling)
2. **Set appropriate timeouts** based on notebook complexity
3. **Validate notebooks locally** before uploading and executing
4. **Use parameters** instead of hardcoded values
5. **Handle errors gracefully** with proper status checking
6. **Monitor execution** through returned URLs
7. **Test with simple notebooks** before complex workflows