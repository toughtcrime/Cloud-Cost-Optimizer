import os
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Automatically mock environment variables for all tests."""
    with patch.dict(os.environ, {
        'AWS_ACCESS_KEY_ID': 'test_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret',
        'AWS_DEFAULT_REGION': 'us-east-1',
        'AZURE_SUBSCRIPTION_ID': 'test_subscription',
        'AZURE_TENANT_ID': 'test_tenant',
        'AZURE_CLIENT_ID': 'test_client',
        'AZURE_CLIENT_SECRET': 'test_secret',
        'GOOGLE_CLOUD_PROJECT': 'test_project',
        'GOOGLE_APPLICATION_CREDENTIALS': '/path/to/test/credentials.json',
        'AUTO_OPTIMIZE': 'false',
        'CPU_THRESHOLD': '10',
        'MEMORY_THRESHOLD': '15',
        'OPTIMIZATION_INTERVAL_HOURS': '6'
    }):
        yield
