"""Tests for SDK execution functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os

# Skip tests if databricks.sdk is not available (since it's not a hard dependency)
databricks_sdk = pytest.importorskip("databricks.sdk", reason="databricks.sdk not available")

from src.templates.dbx_execution.utils import (
    create_workspace_client,
    poll_until_complete,
    format_execution_time,
    safe_get_error_message
)
from src.templates.dbx_execution.sql_executor import SQLExecutor
from src.templates.dbx_execution.notebook_executor import NotebookExecutor


class TestUtils:
    """Test utility functions."""

    def test_format_execution_time(self):
        """Test execution time formatting."""
        assert format_execution_time(30.5) == "30.5s"
        assert format_execution_time(90) == "1.5m"
        assert format_execution_time(3661) == "1.0h"

    def test_safe_get_error_message(self):
        """Test error message extraction."""
        # Test with error key
        response = {"error": "Test error"}
        assert safe_get_error_message(response) == "Test error"

        # Test with message key
        response = {"message": "Test message"}
        assert safe_get_error_message(response) == "Test message"

        # Test with state_message key
        response = {"state_message": "Test state"}
        assert safe_get_error_message(response) == "Test state"

        # Test with no recognized keys
        response = {"unknown": "value"}
        assert safe_get_error_message(response) == "Unknown error occurred"

    @patch('src.templates.dbx_execution.utils.WorkspaceClient')
    def test_create_workspace_client_with_profile(self, mock_client):
        """Test client creation with profile."""
        create_workspace_client(profile="test-profile")
        mock_client.assert_called_once_with(profile="test-profile")

    @patch('src.templates.dbx_execution.utils.WorkspaceClient')
    def test_create_workspace_client_with_credentials(self, mock_client):
        """Test client creation with direct credentials."""
        create_workspace_client(
            host="https://test.databricks.com",
            token="test-token"
        )
        mock_client.assert_called_once_with(
            host="https://test.databricks.com",
            token="test-token"
        )

    @patch('src.templates.dbx_execution.utils.WorkspaceClient')
    def test_create_workspace_client_default(self, mock_client):
        """Test client creation with defaults."""
        create_workspace_client()
        mock_client.assert_called_once_with()

    def test_poll_until_complete_success(self):
        """Test polling until completion - success case."""
        call_count = 0

        def mock_status():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {"state": "RUNNING"}
            else:
                return {"state": "SUCCESS", "result": "completed"}

        with patch('time.sleep'):  # Speed up test
            result = poll_until_complete(mock_status, timeout_seconds=60, poll_interval=1)

        assert result["state"] == "SUCCESS"
        assert result["result"] == "completed"

    def test_poll_until_complete_timeout(self):
        """Test polling until completion - timeout case."""
        def mock_status():
            return {"state": "RUNNING"}

        with patch('time.time', side_effect=[0, 0, 10, 70]):  # Simulate timeout
            with patch('time.sleep'):
                result = poll_until_complete(mock_status, timeout_seconds=60, poll_interval=1)

        assert result["state"] == "TIMEOUT"
        assert "timed out" in result["message"]


class TestSQLExecutor:
    """Test SQL execution functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.executor = SQLExecutor(self.mock_client)

    def test_init(self):
        """Test SQLExecutor initialization."""
        assert self.executor.client == self.mock_client

    def test_execute_sql_file_not_found(self):
        """Test SQL file execution with missing file."""
        result = self.executor.execute_sql_file(
            "/nonexistent/file.sql",
            "warehouse-id"
        )

        assert result["status"] == "ERROR"
        assert "File not found" in result["error"]

    def test_execute_sql_file_success(self):
        """Test SQL file execution success."""
        # Create temporary SQL file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as f:
            f.write("SELECT 1 as test")
            temp_path = f.name

        try:
            # Mock successful execution
            with patch.object(self.executor, 'execute_sql') as mock_execute:
                mock_execute.return_value = {"status": "SUCCESS", "row_count": 1}

                result = self.executor.execute_sql_file(temp_path, "warehouse-id")

                mock_execute.assert_called_once_with(
                    query="SELECT 1 as test",
                    warehouse_id="warehouse-id",
                    catalog=None,
                    schema=None,
                    parameters=None,
                    timeout_seconds=300
                )
                assert result["status"] == "SUCCESS"
        finally:
            os.unlink(temp_path)

    @patch('time.sleep')
    def test_wait_for_sql_completion_success(self, mock_sleep):
        """Test SQL completion waiting - success case."""
        # Mock statement execution response
        mock_statement = Mock()
        mock_statement.status.state.value = "SUCCEEDED"
        mock_statement.manifest.total_row_count = 5
        mock_statement.manifest.schema.columns = [
            Mock(name="col1"),
            Mock(name="col2")
        ]

        self.mock_client.statement_execution.get_statement.return_value = mock_statement

        # Mock result data
        mock_result = Mock()
        mock_result.data_array = [["val1", "val2"], ["val3", "val4"]]
        self.mock_client.statement_execution.get_statement_result_chunk_n.return_value = mock_result

        result = self.executor._wait_for_sql_completion("stmt-id", 300, 0)

        assert result["status"] == "SUCCESS"
        assert result["statement_id"] == "stmt-id"
        assert "execution_time" in result
        assert result["row_count"] == 2  # Length of mock data

    @patch('time.sleep')
    def test_wait_for_sql_completion_failure(self, mock_sleep):
        """Test SQL completion waiting - failure case."""
        mock_statement = Mock()
        mock_statement.status.state.value = "FAILED"
        mock_statement.status.message = "Query failed"

        self.mock_client.statement_execution.get_statement.return_value = mock_statement

        result = self.executor._wait_for_sql_completion("stmt-id", 300, 0)

        assert result["status"] == "FAILED"
        assert result["statement_id"] == "stmt-id"
        assert "error" in result

    def test_list_warehouses_success(self):
        """Test warehouse listing success."""
        mock_warehouse = Mock()
        mock_warehouse.id = "wh-123"
        mock_warehouse.name = "Test Warehouse"
        mock_warehouse.state.value = "RUNNING"
        mock_warehouse.cluster_size = "Small"
        mock_warehouse.min_num_clusters = 1
        mock_warehouse.max_num_clusters = 5

        self.mock_client.warehouses.list.return_value = [mock_warehouse]

        result = self.executor.list_warehouses()

        assert len(result) == 1
        assert result[0]["id"] == "wh-123"
        assert result[0]["name"] == "Test Warehouse"
        assert result[0]["state"] == "RUNNING"

    def test_list_warehouses_error(self):
        """Test warehouse listing error."""
        self.mock_client.warehouses.list.side_effect = Exception("API Error")

        result = self.executor.list_warehouses()

        assert result == []

    def test_get_warehouse_status_success(self):
        """Test warehouse status retrieval success."""
        mock_warehouse = Mock()
        mock_warehouse.id = "wh-123"
        mock_warehouse.name = "Test Warehouse"
        mock_warehouse.state.value = "RUNNING"
        mock_warehouse.health.value = "HEALTHY"

        self.mock_client.warehouses.get.return_value = mock_warehouse

        result = self.executor.get_warehouse_status("wh-123")

        assert result["id"] == "wh-123"
        assert result["name"] == "Test Warehouse"
        assert result["state"] == "RUNNING"
        assert result["health"] == "HEALTHY"

    def test_test_warehouse_connection_success(self):
        """Test warehouse connection test success."""
        with patch.object(self.executor, 'execute_sql') as mock_execute:
            mock_execute.return_value = {"status": "SUCCESS"}

            result = self.executor.test_warehouse_connection("wh-123")

            assert result is True
            mock_execute.assert_called_once_with(
                "SELECT 1 as test", "wh-123", timeout_seconds=60
            )

    def test_test_warehouse_connection_failure(self):
        """Test warehouse connection test failure."""
        with patch.object(self.executor, 'execute_sql') as mock_execute:
            mock_execute.return_value = {"status": "ERROR"}

            result = self.executor.test_warehouse_connection("wh-123")

            assert result is False


class TestNotebookExecutor:
    """Test notebook execution functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.executor = NotebookExecutor(self.mock_client)

    def test_init(self):
        """Test NotebookExecutor initialization."""
        assert self.executor.client == self.mock_client

    def test_run_notebook_success_serverless(self):
        """Test notebook execution success with serverless."""
        # Mock job submission
        mock_response = Mock()
        mock_response.run_id = 12345
        self.mock_client.jobs.submit.return_value = mock_response

        # Mock completion waiting
        with patch.object(self.executor, '_wait_for_completion') as mock_wait:
            mock_wait.return_value = {"status": "SUCCESS", "run_id": 12345}

            result = self.executor.run_notebook("/path/to/notebook")

            assert result["status"] == "SUCCESS"
            assert result["run_id"] == 12345

    def test_run_notebook_success_with_cluster(self):
        """Test notebook execution success with cluster."""
        mock_response = Mock()
        mock_response.run_id = 12345
        self.mock_client.jobs.submit.return_value = mock_response

        with patch.object(self.executor, '_wait_for_completion') as mock_wait:
            mock_wait.return_value = {"status": "SUCCESS", "run_id": 12345}

            result = self.executor.run_notebook(
                "/path/to/notebook",
                cluster_id="cluster-123",
                parameters={"param1": "value1"}
            )

            assert result["status"] == "SUCCESS"

    def test_run_notebook_error(self):
        """Test notebook execution error."""
        self.mock_client.jobs.submit.side_effect = Exception("Submit failed")

        result = self.executor.run_notebook("/path/to/notebook")

        assert result["status"] == "ERROR"
        assert "Submit failed" in result["error"]

    def test_validate_notebook_exists_true(self):
        """Test notebook existence validation - exists."""
        self.mock_client.workspace.get_status.return_value = Mock()

        result = self.executor.validate_notebook_exists("/path/to/notebook")

        assert result is True

    def test_validate_notebook_exists_false(self):
        """Test notebook existence validation - not exists."""
        self.mock_client.workspace.get_status.side_effect = Exception("Not found")

        result = self.executor.validate_notebook_exists("/path/to/notebook")

        assert result is False

    def test_detect_notebook_format(self):
        """Test notebook format detection."""
        from databricks.sdk.service.workspace import ExportFormat

        assert self.executor._detect_notebook_format("test.py") == ExportFormat.SOURCE
        assert self.executor._detect_notebook_format("test.ipynb") == ExportFormat.JUPYTER
        assert self.executor._detect_notebook_format("test.sql") == ExportFormat.SQL
        assert self.executor._detect_notebook_format("test.txt") == ExportFormat.SOURCE

    def test_get_notebook_output_success(self):
        """Test notebook output retrieval success."""
        mock_output = Mock()
        mock_output.notebook_output.result = "Output result"
        mock_output.notebook_output.truncated = False

        self.mock_client.jobs.get_run_output.return_value = mock_output

        result = self.executor.get_notebook_output(12345)

        assert result["result"] == "Output result"
        assert result["truncated"] is False

    def test_get_notebook_output_no_output(self):
        """Test notebook output retrieval with no output."""
        mock_output = Mock()
        mock_output.notebook_output = None

        self.mock_client.jobs.get_run_output.return_value = mock_output

        result = self.executor.get_notebook_output(12345)

        assert result["result"] is None
        assert result["truncated"] is False

    def test_list_clusters_success(self):
        """Test cluster listing success."""
        mock_cluster = Mock()
        mock_cluster.cluster_id = "cluster-123"
        mock_cluster.cluster_name = "Test Cluster"
        mock_cluster.state.value = "RUNNING"
        mock_cluster.node_type_id = "i3.xlarge"
        mock_cluster.num_workers = 2

        self.mock_client.clusters.list.return_value = [mock_cluster]

        result = self.executor.list_clusters()

        assert len(result) == 1
        assert result[0]["cluster_id"] == "cluster-123"
        assert result[0]["cluster_name"] == "Test Cluster"

    def test_test_simple_notebook_success(self):
        """Test simple notebook test success."""
        with patch.object(self.executor, 'run_notebook') as mock_run:
            mock_run.return_value = {"status": "SUCCESS"}

            result = self.executor.test_simple_notebook("/test/notebook")

            assert result is True

    def test_run_notebook_with_retry_success_first_try(self):
        """Test notebook retry - success on first try."""
        with patch.object(self.executor, 'run_notebook') as mock_run:
            mock_run.return_value = {"status": "SUCCESS"}

            result = self.executor.run_notebook_with_retry("/path/to/notebook", max_retries=2)

            assert result["status"] == "SUCCESS"
            assert mock_run.call_count == 1

    @patch('time.sleep')
    def test_run_notebook_with_retry_success_second_try(self, mock_sleep):
        """Test notebook retry - success on second try."""
        with patch.object(self.executor, 'run_notebook') as mock_run:
            mock_run.side_effect = [
                {"status": "FAILED"},
                {"status": "SUCCESS"}
            ]

            result = self.executor.run_notebook_with_retry("/path/to/notebook", max_retries=2)

            assert result["status"] == "SUCCESS"
            assert mock_run.call_count == 2

    @patch('time.sleep')
    def test_run_notebook_with_retry_all_fail(self, mock_sleep):
        """Test notebook retry - all attempts fail."""
        with patch.object(self.executor, 'run_notebook') as mock_run:
            mock_run.return_value = {"status": "FAILED"}

            result = self.executor.run_notebook_with_retry("/path/to/notebook", max_retries=2)

            assert result["status"] == "FAILED"
            assert mock_run.call_count == 3  # Initial + 2 retries