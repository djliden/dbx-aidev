"""Notebook execution on Databricks workspace."""

import time
from typing import Any, Dict, List, Optional

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import NotebookTask, SubmitTask

from .utils import format_execution_time, safe_get_error_message


class NotebookExecutor:
    """Execute notebooks on Databricks workspace."""

    def __init__(self, client: WorkspaceClient):
        self.client = client

    def run_notebook(self, notebook_path: str, cluster_id: Optional[str] = None,
                    parameters: Optional[Dict[str, str]] = None,
                    timeout_seconds: int = 300) -> Dict[str, Any]:
        """Run a notebook on Databricks and return results.

        Args:
            notebook_path: Path to notebook in workspace
            cluster_id: Cluster ID to run on (if None, uses serverless)
            parameters: Notebook parameters
            timeout_seconds: Max time to wait for completion

        Returns:
            Dictionary with execution results
        """
        try:
            # Create task configuration
            task = SubmitTask(
                task_key='notebook_task',
                notebook_task=NotebookTask(
                    notebook_path=notebook_path,
                    base_parameters=parameters or {}
                )
            )

            # Add cluster config if provided, otherwise use serverless
            if cluster_id:
                task.existing_cluster_id = cluster_id
                print(f'🚀 Starting notebook execution on cluster {cluster_id}')
            else:
                print('🚀 Starting notebook execution on serverless compute')

            if parameters:
                print(f'📝 Parameters: {parameters}')

            # Submit the run
            run_response = self.client.jobs.submit(tasks=[task])
            run_id = run_response.run_id
            print(f'📋 Run ID: {run_id}')

            # Poll for completion
            return self._wait_for_completion(run_id, timeout_seconds)

        except Exception as e:
            print(f'❌ Failed to execute notebook: {e}')
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_notebook_from_local(self, local_path: str, workspace_path: str,
                               cluster_id: Optional[str] = None,
                               parameters: Optional[Dict[str, str]] = None,
                               timeout_seconds: int = 300,
                               overwrite: bool = False) -> Dict[str, Any]:
        """Upload local notebook and execute it.

        Args:
            local_path: Path to local notebook file
            workspace_path: Target path in workspace
            cluster_id: Cluster ID to run on (if None, uses serverless)
            parameters: Notebook parameters
            timeout_seconds: Max time to wait for completion
            overwrite: Whether to overwrite existing notebook

        Returns:
            Dictionary with execution results
        """
        try:
            # Upload notebook first
            print(f'📤 Uploading notebook: {local_path} -> {workspace_path}')

            with open(local_path, 'rb') as f:
                content = f.read()

            self.client.workspace.upload(
                path=workspace_path,
                content=content,
                overwrite=overwrite,
                format=self._detect_notebook_format(local_path)
            )

            print('✅ Notebook uploaded successfully')

            # Execute the uploaded notebook
            return self.run_notebook(
                notebook_path=workspace_path,
                cluster_id=cluster_id,
                parameters=parameters,
                timeout_seconds=timeout_seconds
            )

        except Exception as e:
            print(f'❌ Failed to upload and execute notebook: {e}')
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    def get_notebook_output(self, run_id: int) -> Dict[str, Any]:
        """Get output from notebook execution.

        Args:
            run_id: Job run ID

        Returns:
            Dictionary with notebook output
        """
        try:
            run_output = self.client.jobs.get_run_output(run_id)

            if run_output.notebook_output:
                return {
                    'result': run_output.notebook_output.result,
                    'truncated': run_output.notebook_output.truncated
                }
            else:
                return {'result': None, 'truncated': False}

        except Exception as e:
            print(f'⚠️ Could not retrieve notebook output: {e}')
            return {'error': str(e)}

    def list_clusters(self) -> List[Dict[str, Any]]:
        """List available clusters for notebook execution.

        Returns:
            List of cluster information dictionaries
        """
        try:
            clusters = self.client.clusters.list()
            cluster_info = []

            for cluster in clusters:
                cluster_info.append({
                    'cluster_id': cluster.cluster_id,
                    'cluster_name': cluster.cluster_name,
                    'state': cluster.state.value if cluster.state else 'UNKNOWN',
                    'node_type_id': cluster.node_type_id,
                    'num_workers': cluster.num_workers
                })

            return cluster_info

        except Exception as e:
            print(f'❌ Failed to list clusters: {e}')
            return []

    def validate_notebook_exists(self, notebook_path: str) -> bool:
        """Check if notebook exists in workspace.

        Args:
            notebook_path: Path to notebook in workspace

        Returns:
            True if notebook exists, False otherwise
        """
        try:
            self.client.workspace.get_status(notebook_path)
            return True
        except Exception:
            return False

    def _wait_for_completion(self, run_id: int, timeout_seconds: int) -> Dict[str, Any]:
        """Wait for run completion and return results."""
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            try:
                run_info = self.client.jobs.get_run(run_id)
                state = run_info.state.life_cycle_state.value

                if state in ['TERMINATED', 'SKIPPED']:
                    result_state = (
                        run_info.state.result_state.value
                        if run_info.state.result_state
                        else 'UNKNOWN'
                    )
                    execution_time = time.time() - start_time

                    if result_state == 'SUCCESS':
                        print(
                            f'✅ Notebook executed successfully! '
                            f'({format_execution_time(execution_time)})'
                        )

                        # Try to get notebook output
                        output = self.get_notebook_output(run_id)

                        return {
                            'status': 'SUCCESS',
                            'run_id': run_id,
                            'run_page_url': run_info.run_page_url,
                            'execution_time': execution_time,
                            'output': output
                        }
                    else:
                        error_msg = safe_get_error_message(run_info.state.__dict__)
                        print(f'❌ Notebook execution failed: {result_state}')
                        return {
                            'status': 'FAILED',
                            'run_id': run_id,
                            'run_page_url': run_info.run_page_url,
                            'error_state': result_state,
                            'error_message': error_msg
                        }

                elif state in ['PENDING', 'RUNNING']:
                    print(f'⏳ Execution in progress... ({state})')
                    time.sleep(10)
                else:
                    print(f'❓ Unexpected state: {state}')
                    break

            except Exception as e:
                print(f'❌ Error checking run status: {e}')
                break

        print(f'⏰ Execution timed out after {timeout_seconds} seconds')
        return {
            'status': 'TIMEOUT',
            'run_id': run_id,
            'timeout_seconds': timeout_seconds
        }

    def _detect_notebook_format(self, file_path: str):
        """Detect notebook format from file extension."""
        from databricks.sdk.service.workspace import ExportFormat

        if file_path.endswith('.py'):
            return ExportFormat.SOURCE
        elif file_path.endswith('.ipynb'):
            return ExportFormat.JUPYTER
        elif file_path.endswith('.sql'):
            return ExportFormat.SQL
        else:
            return ExportFormat.SOURCE

    def test_simple_notebook(self, test_notebook_path: str,
                           cluster_id: Optional[str] = None) -> bool:
        """Test execution with a simple notebook.

        Args:
            test_notebook_path: Path to test notebook in workspace
            cluster_id: Optional cluster ID

        Returns:
            True if test succeeds, False otherwise
        """
        print('🧪 Testing notebook execution...')
        result = self.run_notebook(
            notebook_path=test_notebook_path,
            cluster_id=cluster_id,
            timeout_seconds=120
        )
        return result.get('status') == 'SUCCESS'

    def run_notebook_with_retry(self, notebook_path: str, max_retries: int = 2,
                               **kwargs) -> Dict[str, Any]:
        """Run notebook with automatic retry on failure.

        Args:
            notebook_path: Path to notebook in workspace
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments passed to run_notebook

        Returns:
            Dictionary with execution results
        """
        for attempt in range(max_retries + 1):
            if attempt > 0:
                print(f'🔄 Retry attempt {attempt}/{max_retries}')
                time.sleep(30)  # Wait before retry

            result = self.run_notebook(notebook_path, **kwargs)

            if result.get('status') == 'SUCCESS':
                return result
            elif attempt == max_retries:
                print(f'❌ Failed after {max_retries + 1} attempts')
                return result
            else:
                print(f'⚠️ Attempt {attempt + 1} failed, retrying...')

        return result
