# API Reference

## CloudResourceOptimizer

### Constructor
```python
def __init__(self):
    """Initialize the Cloud Resource Optimizer."""
```

### Methods

#### analyze_aws_resources
```python
def analyze_aws_resources(self) -> Dict:
    """
    Analyze AWS resources for optimization opportunities.
    
    Returns:
        Dict containing analysis results for EC2, EBS, RDS, and S3 resources
    """
```

#### analyze_azure_resources
```python
def analyze_azure_resources(self) -> Dict:
    """
    Analyze Azure resources for optimization opportunities.
    
    Returns:
        Dict containing analysis results for VMs and related resources
    """
```

#### analyze_gcp_resources
```python
def analyze_gcp_resources(self) -> Dict:
    """
    Analyze GCP resources for optimization opportunities.
    
    Returns:
        Dict containing analysis results for Compute Engine instances
    """
```

#### generate_optimization_report
```python
def generate_optimization_report(self) -> Dict:
    """
    Generate a comprehensive optimization report.
    
    Returns:
        Dict containing optimization recommendations and savings estimates
    """
```

#### save_report
```python
def save_report(self, report: Dict, filename: str = None):
    """
    Save the optimization report to a file.
    
    Args:
        report: Dict containing the optimization report
        filename: Optional custom filename for the report
    """
```

#### stop_underutilized_resources
```python
def stop_underutilized_resources(self):
    """
    Stop or hibernate underutilized resources across cloud providers.
    """
```

#### scheduled_optimization
```python
def scheduled_optimization(self):
    """
    Run optimization tasks on a schedule.
    """
```

## Report Format

### Structure
```python
{
    "timestamp": str,
    "aws": {
        "underutilized_ec2": List[Dict],
        "unused_ebs": List[Dict],
        "underutilized_rds": List[Dict],
        "s3_optimizations": List[Dict]
    },
    "azure": {
        "underutilized_vms": List[Dict]
    },
    "gcp": {
        "underutilized_instances": List[Dict]
    },
    "estimated_monthly_savings": float,
    "recommendations": List[str]
}
```

### Example Response
```json
{
    "timestamp": "2024-12-15T09:42:33+01:00",
    "aws": {
        "underutilized_ec2": [
            {
                "InstanceId": "i-1234567890abcdef0",
                "InstanceType": "t2.xlarge",
                "AverageUtilization": 5.2
            }
        ]
    },
    "estimated_monthly_savings": 150.25,
    "recommendations": [
        "Consider stopping AWS EC2 instance i-1234567890abcdef0"
    ]
}
