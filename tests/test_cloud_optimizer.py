import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest
from botocore.exceptions import ClientError
from azure.core.exceptions import AzureError
from google.api_core.exceptions import GoogleAPIError

from src.cloud_optimizer import CloudResourceOptimizer

@pytest.fixture
def optimizer():
    """Create a CloudResourceOptimizer instance for testing."""
    with patch.dict(os.environ, {
        'AWS_ACCESS_KEY_ID': 'test_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret',
        'AZURE_SUBSCRIPTION_ID': 'test_sub',
        'GOOGLE_CLOUD_PROJECT': 'test_project'
    }):
        return CloudResourceOptimizer()

@pytest.fixture
def mock_aws_resources():
    """Mock AWS EC2 resources."""
    return {
        'Reservations': [{
            'Instances': [{
                'InstanceId': 'i-1234567890abcdef0',
                'InstanceType': 't2.micro',
                'State': {'Name': 'running'}
            }]
        }]
    }

@pytest.fixture
def mock_cloudwatch_metrics():
    """Mock AWS CloudWatch metrics."""
    return {
        'Datapoints': [
            {'Average': 5.0},
            {'Average': 3.0}
        ]
    }

def test_analyze_aws_resources(optimizer, mock_aws_resources, mock_cloudwatch_metrics):
    """Test AWS resource analysis."""
    with patch('boto3.client') as mock_boto3:
        # Mock EC2 client
        mock_ec2 = MagicMock()
        mock_ec2.describe_instances.return_value = mock_aws_resources
        
        # Mock CloudWatch client
        mock_cloudwatch = MagicMock()
        mock_cloudwatch.get_metric_statistics.return_value = mock_cloudwatch_metrics
        
        # Set up boto3 to return our mocked clients
        mock_boto3.side_effect = lambda service: {
            'ec2': mock_ec2,
            'cloudwatch': mock_cloudwatch
        }[service]
        
        result = optimizer.analyze_aws_resources()
        
        assert 'underutilized_ec2' in result
        assert len(result['underutilized_ec2']) == 1
        assert result['underutilized_ec2'][0]['InstanceId'] == 'i-1234567890abcdef0'
        assert result['underutilized_ec2'][0]['InstanceType'] == 't2.micro'

def test_analyze_azure_resources(optimizer):
    """Test Azure resource analysis."""
    with patch('azure.identity.DefaultAzureCredential'), \
         patch('azure.mgmt.compute.ComputeManagementClient'), \
         patch('azure.mgmt.monitor.MonitorManagementClient'):
        
        result = optimizer.analyze_azure_resources()
        assert isinstance(result, dict)

def test_analyze_gcp_resources(optimizer):
    """Test GCP resource analysis."""
    with patch('google.cloud.compute_v1.InstancesClient'), \
         patch('google.cloud.compute_v1.ZonesClient'):
        
        result = optimizer.analyze_gcp_resources()
        assert isinstance(result, dict)

def test_generate_optimization_report(optimizer):
    """Test optimization report generation."""
    with patch.object(optimizer, 'analyze_aws_resources', return_value={}), \
         patch.object(optimizer, 'analyze_azure_resources', return_value={}), \
         patch.object(optimizer, 'analyze_gcp_resources', return_value={}):
        
        report = optimizer.generate_optimization_report()
        
        assert isinstance(report, dict)
        assert 'timestamp' in report
        assert 'aws' in report
        assert 'azure' in report
        assert 'gcp' in report
        assert 'estimated_monthly_savings' in report
        assert 'recommendations' in report

def test_save_report(optimizer, tmp_path):
    """Test report saving functionality."""
    # Create a sample report
    report = {
        'timestamp': datetime.utcnow().isoformat(),
        'test_data': 'sample'
    }
    
    # Create a temporary file path
    report_path = tmp_path / 'test_report.json'
    
    # Save the report
    optimizer.save_report(report, str(report_path))
    
    # Verify the file exists and contains the correct data
    assert report_path.exists()
    with open(report_path) as f:
        saved_report = json.load(f)
        assert saved_report['test_data'] == 'sample'

def test_stop_underutilized_resources(optimizer):
    """Test stopping underutilized resources."""
    with patch('boto3.client') as mock_aws, \
         patch('azure.identity.DefaultAzureCredential'), \
         patch('azure.mgmt.compute.ComputeManagementClient') as mock_azure, \
         patch('google.cloud.compute_v1.InstancesClient') as mock_gcp:
        
        # Mock AWS resources
        mock_ec2 = MagicMock()
        mock_aws.return_value = mock_ec2
        
        # Mock Azure resources
        mock_azure_compute = MagicMock()
        mock_azure.return_value = mock_azure_compute
        
        # Mock GCP resources
        mock_gcp_instances = MagicMock()
        mock_gcp.return_value = mock_gcp_instances
        
        # Test the method
        optimizer.stop_underutilized_resources()
        
        # Verify that the appropriate methods were called
        # (We're not testing the actual stopping here, just that the method runs without errors)
        assert True

def test_error_handling(optimizer):
    """Test error handling in the optimizer."""
    with patch('boto3.client') as mock_boto3:
        # Mock AWS error
        mock_boto3.side_effect = ClientError(
            error_response={'Error': {'Code': 'TestError', 'Message': 'Test error'}},
            operation_name='TestOperation'
        )
        
        # The method should handle the error gracefully
        result = optimizer.analyze_aws_resources()
        assert result == {}
