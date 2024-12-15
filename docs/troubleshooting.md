# Troubleshooting Guide

## Common Issues

### Authentication Errors

#### AWS Credentials
```
Error analyzing AWS resources: botocore.exceptions.ClientError: An error occurred (UnauthorizedOperation)
```

**Solution:**
1. Check AWS credentials in `.env` file
2. Verify IAM permissions
3. Confirm AWS region setting

#### Azure Authentication
```
Error analyzing Azure resources: azure.core.exceptions.ClientAuthenticationError
```

**Solution:**
1. Verify Azure credentials in `.env`
2. Check service principal permissions
3. Confirm subscription status

#### GCP Authentication
```
Error analyzing GCP resources: google.auth.exceptions.DefaultCredentialsError
```

**Solution:**
1. Check service account key path
2. Verify project ID
3. Confirm API enablement

### Resource Access Issues

#### Unable to List Resources
```
Error: Access denied while listing resources
```

**Solution:**
1. Check minimum required permissions
2. Verify resource group access
3. Confirm API quotas

#### Metric Collection Failures
```
Error: Could not retrieve metrics for resource
```

**Solution:**
1. Check monitoring API access
2. Verify metric availability
3. Confirm time range validity

## Performance Optimization

### High Memory Usage
If the tool is using excessive memory:

1. Adjust batch sizes:
```python
BATCH_SIZE = 100  # Reduce if memory usage is high
```

2. Implement pagination:
```python
def get_resources(self, page_size=100):
    page_token = None
    while True:
        resources, page_token = self.list_resources(page_size, page_token)
        yield resources
        if not page_token:
            break
```

### Slow Analysis

If analysis is taking too long:

1. Optimize API calls:
   - Use batch operations
   - Implement caching
   - Reduce analysis window

2. Configure parallel processing:
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    aws_future = executor.submit(self.analyze_aws_resources)
    azure_future = executor.submit(self.analyze_azure_resources)
    gcp_future = executor.submit(self.analyze_gcp_resources)
```

## Logging and Debugging

### Enable Debug Logging
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Log File Analysis
Check specific components:
```bash
# AWS-related issues
grep "AWS" optimizer.log

# Azure-related issues
grep "Azure" optimizer.log

# GCP-related issues
grep "GCP" optimizer.log
```

## Support Resources

### Community Support
- GitHub Issues
- Stack Overflow tags: 
  - `cloud-cost-optimizer`
  - `aws-optimization`
  - `azure-optimization`
  - `gcp-optimization`

### Cloud Provider Support
- [AWS Support](https://aws.amazon.com/support/)
- [Azure Support](https://azure.microsoft.com/support/)
- [GCP Support](https://cloud.google.com/support/)
