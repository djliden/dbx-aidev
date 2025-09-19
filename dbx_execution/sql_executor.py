"""SQL execution on Databricks via SDK."""

import time
from typing import Any, Dict, List, Optional

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementParameterListItem

from .utils import format_execution_time, safe_get_error_message


class SQLExecutor:
    """Execute SQL on Databricks workspace using statement execution API."""

    def __init__(self, client: WorkspaceClient):
        self.client = client

    def execute_sql(self, query: str, warehouse_id: str,
                   catalog: Optional[str] = None, schema: Optional[str] = None,
                   parameters: Optional[Dict[str, str]] = None,
                   timeout_seconds: int = 300) -> Dict[str, Any]:
        """Execute SQL query and return results.

        Args:
            query: SQL query to execute
            warehouse_id: SQL warehouse ID
            catalog: Optional catalog name
            schema: Optional schema name
            parameters: Optional query parameters (for parameterized queries)
            timeout_seconds: Max time to wait for completion

        Returns:
            Dictionary with execution results
        """
        try:
            # Prepare parameters if provided
            statement_params = None
            if parameters:
                statement_params = [
                    StatementParameterListItem(name=k, value=v)
                    for k, v in parameters.items()
                ]

            # Execute statement
            print(f'🚀 Executing SQL query on warehouse {warehouse_id}')
            if catalog or schema:
                context_msg = f" (catalog: {catalog or 'default'}, schema: {schema or 'default'})"
                print(f'📍 Context{context_msg}')

            start_time = time.time()

            response = self.client.statement_execution.execute_statement(
                statement=query,
                warehouse_id=warehouse_id,
                catalog=catalog,
                schema=schema,
                parameters=statement_params,
                wait_timeout='30s'  # Initial wait before polling
            )

            # Poll for completion
            return self._wait_for_sql_completion(response.statement_id, timeout_seconds, start_time)

        except Exception as e:
            print(f'❌ Failed to execute SQL: {e}')
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def execute_sql_file(self, file_path: str, warehouse_id: str,
                        catalog: Optional[str] = None, schema: Optional[str] = None,
                        parameters: Optional[Dict[str, str]] = None,
                        timeout_seconds: int = 300) -> Dict[str, Any]:
        """Execute SQL from local file.

        Args:
            file_path: Path to .sql file
            warehouse_id: SQL warehouse ID
            catalog: Optional catalog name
            schema: Optional schema name
            parameters: Optional query parameters
            timeout_seconds: Max time to wait for completion

        Returns:
            Dictionary with execution results
        """
        try:
            with open(file_path, 'r') as f:
                query = f.read()

            print(f'📄 Executing SQL from file: {file_path}')
            return self.execute_sql(
                query=query,
                warehouse_id=warehouse_id,
                catalog=catalog,
                schema=schema,
                parameters=parameters,
                timeout_seconds=timeout_seconds
            )

        except FileNotFoundError:
            print(f'❌ SQL file not found: {file_path}')
            return {
                'status': 'ERROR',
                'error': f'File not found: {file_path}'
            }
        except Exception as e:
            print(f'❌ Failed to read SQL file: {e}')
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def list_warehouses(self) -> List[Dict[str, Any]]:
        """List available SQL warehouses.

        Returns:
            List of warehouse information dictionaries
        """
        try:
            warehouses = self.client.warehouses.list()
            warehouse_info = []

            for warehouse in warehouses:
                warehouse_info.append({
                    'id': warehouse.id,
                    'name': warehouse.name,
                    'state': warehouse.state.value if warehouse.state else 'UNKNOWN',
                    'cluster_size': warehouse.cluster_size,
                    'min_num_clusters': warehouse.min_num_clusters,
                    'max_num_clusters': warehouse.max_num_clusters
                })

            return warehouse_info

        except Exception as e:
            print(f'❌ Failed to list warehouses: {e}')
            return []

    def get_warehouse_status(self, warehouse_id: str) -> Dict[str, Any]:
        """Get status of specific SQL warehouse.

        Args:
            warehouse_id: SQL warehouse ID

        Returns:
            Warehouse status information
        """
        try:
            warehouse = self.client.warehouses.get(warehouse_id)
            return {
                'id': warehouse.id,
                'name': warehouse.name,
                'state': warehouse.state.value if warehouse.state else 'UNKNOWN',
                'health': warehouse.health.value if warehouse.health else 'UNKNOWN'
            }
        except Exception as e:
            print(f'❌ Failed to get warehouse status: {e}')
            return {'error': str(e)}

    def _wait_for_sql_completion(self, statement_id: str, timeout_seconds: int,
                                start_time: float) -> Dict[str, Any]:
        """Wait for SQL statement completion and return results."""
        while time.time() - start_time < timeout_seconds:
            try:
                # Get statement status
                statement = self.client.statement_execution.get_statement(statement_id)
                status = statement.status.state.value

                if status == 'SUCCEEDED':
                    execution_time = time.time() - start_time
                    print(
                        f'✅ SQL executed successfully! '
                        f'({format_execution_time(execution_time)})'
                    )

                    # Get results
                    results = self._get_statement_results(statement_id)

                    return {
                        'status': 'SUCCESS',
                        'statement_id': statement_id,
                        'execution_time': execution_time,
                        'row_count': len(results.get('data', [])),
                        'results': results
                    }

                elif status in ['FAILED', 'CANCELED']:
                    error_msg = safe_get_error_message(statement.status.__dict__)
                    print(f'❌ SQL execution {status.lower()}: {error_msg}')
                    return {
                        'status': status,
                        'statement_id': statement_id,
                        'error': error_msg
                    }

                elif status in ['PENDING', 'RUNNING']:
                    print(f'⏳ SQL execution in progress... ({status})')
                    time.sleep(5)
                else:
                    print(f'❓ Unknown SQL execution state: {status}')
                    break

            except Exception as e:
                print(f'❌ Error checking SQL status: {e}')
                break

        print(f'⏰ SQL execution timed out after {timeout_seconds} seconds')
        return {
            'status': 'TIMEOUT',
            'statement_id': statement_id,
            'timeout_seconds': timeout_seconds
        }

    def _get_statement_results(self, statement_id: str) -> Dict[str, Any]:
        """Get results from completed SQL statement."""
        try:
            # Get result metadata
            statement = self.client.statement_execution.get_statement(statement_id)

            # Get result data if available
            if statement.manifest and statement.manifest.total_row_count > 0:
                result_data = self.client.statement_execution.get_statement_result_chunk_n(
                    statement_id=statement_id,
                    chunk_index=0
                )

                # Convert to readable format
                columns = (
                    [col.name for col in statement.manifest.schema.columns]
                    if statement.manifest.schema
                    else []
                )
                data = []

                if result_data.data_array:
                    for row in result_data.data_array:
                        data.append(dict(zip(columns, row)))

                return {
                    'columns': columns,
                    'data': data,
                    'total_row_count': statement.manifest.total_row_count
                }
            else:
                return {
                    'columns': [],
                    'data': [],
                    'total_row_count': 0
                }

        except Exception as e:
            print(f'⚠️ Warning: Could not retrieve result data: {e}')
            return {
                'columns': [],
                'data': [],
                'error': str(e)
            }

    def test_warehouse_connection(self, warehouse_id: str) -> bool:
        """Test connection to SQL warehouse with simple query."""
        print(f'🧪 Testing warehouse connection: {warehouse_id}')
        result = self.execute_sql('SELECT 1 as test', warehouse_id, timeout_seconds=60)
        return result.get('status') == 'SUCCESS'
