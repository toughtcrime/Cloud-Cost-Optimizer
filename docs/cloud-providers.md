# Cloud Providers

## AWS

### Supported Resources
- EC2 Instances
- EBS Volumes
- RDS Databases
- S3 Buckets

### Required Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "ec2:StopInstances",
                "rds:Describe*",
                "s3:List*",
                "s3:Get*",
                "cloudwatch:GetMetricStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```

### Metrics Analyzed
- CPU Utilization
- Memory Usage
- Disk I/O
- Network Traffic

## Azure

### Supported Resources
- Virtual Machines
- Managed Disks
- Storage Accounts
- SQL Databases

### Required Permissions
- Reader role for monitoring
- Contributor role for optimization actions

### Metrics Analyzed
- CPU Percentage
- Memory Usage
- Disk Operations
- Network Throughput

## Google Cloud Platform

### Supported Resources
- Compute Engine Instances
- Persistent Disks
- Cloud Storage
- Cloud SQL

### Required Permissions
```yaml
roles:
  - roles/compute.viewer
  - roles/monitoring.viewer
  - roles/storage.objectViewer
  - roles/cloudsql.viewer
```

### Metrics Analyzed
- CPU Utilization
- Memory Usage
- Disk Usage
- Network Usage

## Adding New Providers

### Implementation Steps
1. Create provider class in `src/cloud_optimizer.py`
2. Implement resource analysis methods
3. Add provider-specific configuration
4. Update documentation

### Required Methods
```python
def analyze_resources(self) -> Dict:
    """Analyze provider resources."""
    pass

def stop_resources(self, resource_ids: List[str]):
    """Stop underutilized resources."""
    pass

def get_metrics(self, resource_id: str) -> Dict:
    """Get resource metrics."""
    pass
```
