# Configuration Guide

## Environment Variables

### AWS Configuration
```ini
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region
```

### Azure Configuration
```ini
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
```

### GCP Configuration
```ini
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

### Optimization Settings
```ini
AUTO_OPTIMIZE=false
CPU_THRESHOLD=10
MEMORY_THRESHOLD=15
OPTIMIZATION_INTERVAL_HOURS=6
```

## Thresholds

### CPU Utilization
- Default: 10%
- Recommended range: 5-20%
- Configure with: `CPU_THRESHOLD`

### Memory Utilization
- Default: 15%
- Recommended range: 10-25%
- Configure with: `MEMORY_THRESHOLD`

### Analysis Window
- Default: 24 hours
- Configurable in code: `ANALYSIS_WINDOW_HOURS`

## Automation

### Automatic Resource Management
Set `AUTO_OPTIMIZE=true` to enable automatic:
- Stopping of underutilized instances
- Snapshot cleanup
- Storage tier optimization

### Schedule Configuration
- Default interval: 6 hours
- Configure with: `OPTIMIZATION_INTERVAL_HOURS`
- Valid range: 1-24 hours

## Report Configuration

### Report Location
Reports are saved in:
- Default: `./reports/`
- Format: JSON
- Naming: `optimization_report_YYYYMMDD_HHMMSS.json`

### Report Retention
- Default: 30 days
- Configure in code: `REPORT_RETENTION_DAYS`

## Logging

### Log Levels
```python
# In src/main.py
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for more detail
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Log File
- Default: Standard output
- For file logging, modify the logging configuration:
```python
logging.basicConfig(
    filename='optimizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```
