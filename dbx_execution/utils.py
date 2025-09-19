"""Common utilities for Databricks SDK execution."""

import time
from typing import Any, Dict, Optional

from databricks.sdk import WorkspaceClient


def create_workspace_client(profile: Optional[str] = None,
                           host: Optional[str] = None,
                           token: Optional[str] = None) -> WorkspaceClient:
    """Create WorkspaceClient with flexible authentication.

    Args:
        profile: Databricks CLI profile name
        host: Workspace URL (if not using profile)
        token: Personal access token (if not using profile)

    Returns:
        Configured WorkspaceClient instance
    """
    if profile:
        return WorkspaceClient(profile=profile)
    elif host and token:
        return WorkspaceClient(host=host, token=token)
    else:
        # Use default authentication (environment variables or default profile)
        return WorkspaceClient()


def poll_until_complete(get_status_func, timeout_seconds: int = 300,
                       poll_interval: int = 10) -> Dict[str, Any]:
    """Generic polling utility for long-running operations.

    Args:
        get_status_func: Function that returns status dict with 'state' key
        timeout_seconds: Maximum time to wait
        poll_interval: Seconds between status checks

    Returns:
        Final status dictionary
    """
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            status = get_status_func()
            state = status.get('state', '').upper()

            if state in ['TERMINATED', 'SKIPPED', 'SUCCESS', 'FAILED', 'CANCELLED']:
                return status
            elif state in ['PENDING', 'RUNNING', 'EXECUTING']:
                print(f'⏳ Operation in progress... ({state})')
                time.sleep(poll_interval)
            else:
                print(f'❓ Unknown state: {state}')
                break

        except Exception as e:
            print(f'❌ Error checking status: {e}')
            break

    return {
        'state': 'TIMEOUT',
        'message': f'Operation timed out after {timeout_seconds} seconds'
    }


def format_execution_time(seconds: float) -> str:
    """Format execution time in human-readable format."""
    if seconds < 60:
        return f'{seconds:.1f}s'
    elif seconds < 3600:
        return f'{seconds/60:.1f}m'
    else:
        return f'{seconds/3600:.1f}h'


def safe_get_error_message(response: Dict[str, Any]) -> str:
    """Safely extract error message from API response."""
    if 'error' in response:
        return str(response['error'])
    elif 'message' in response:
        return str(response['message'])
    elif 'state_message' in response:
        return str(response['state_message'])
    else:
        return 'Unknown error occurred'
