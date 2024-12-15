# Cloud Cost Optimizer 🚀

A powerful tool for analyzing and optimizing cloud resource costs across AWS, Azure, and Google Cloud Platform (GCP). This tool helps identify underutilized resources and provides automated cost-saving recommendations.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Multi-Cloud Support**: Analyze resources across AWS, Azure, and GCP
- **Resource Analysis**: 
  - EC2 instances, EBS volumes, RDS databases, and S3 buckets in AWS
  - Virtual Machines, Managed Disks, and Storage Accounts in Azure
  - Compute Engine instances and Cloud Storage in GCP
- **Automated Optimization**: Automatically stop or hibernate idle resources
- **Scheduled Monitoring**: Regular analysis and reporting (default: every 6 hours)
- **Cost Savings Estimation**: Calculate potential monthly savings
- **Detailed Reporting**: Generate comprehensive JSON reports
- **Docker Support**: Easy deployment using containers

## 📋 Prerequisites

- Python 3.9 or higher
- Docker (optional)
- Cloud provider credentials:
  - AWS: Access Key and Secret Key
  - Azure: Subscription ID, Tenant ID, Client ID, and Secret
  - GCP: Service Account Key

## 🚀 Quick Start

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cloud-cost-optimizer.git
   cd cloud-cost-optimizer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.template .env
   # Edit .env with your cloud credentials and settings
   ```

5. Run the optimizer:
   ```bash
   python run.py
   ```

### Docker Installation

1. Build the Docker image:
   ```bash
   docker build -t cloud-cost-optimizer .
   ```

2. Run the container:
   ```bash
   docker run -d \
       -v $(pwd)/reports:/app/reports \
       -v $(pwd)/.env:/app/.env \
       --name cost-optimizer \
       cloud-cost-optimizer
   ```

3. View logs:
   ```bash
   docker logs -f cost-optimizer
   ```

### Project Structure
```
cloud-cost-optimizer/
├── src/
│   ├── __init__.py
│   ├── cloud_optimizer.py  # Core optimizer class
│   └── main.py            # Main application logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_cloud_optimizer.py
├── run.py                 # Entry point script
├── requirements.txt
├── .env.template
├── .gitignore
├── .dockerignore
├── Dockerfile
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Configure the following variables in your `.env` file:

```ini
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=your_region

# Azure Credentials
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# GCP Credentials
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# Optimization Settings
AUTO_OPTIMIZE=false
CPU_THRESHOLD=10
MEMORY_THRESHOLD=15
OPTIMIZATION_INTERVAL_HOURS=6
```

### Resource Analysis Thresholds

- **CPU Utilization**: Resources with average CPU usage below `CPU_THRESHOLD` (default: 10%)
- **Memory Usage**: Resources with average memory usage below `MEMORY_THRESHOLD` (default: 15%)
- **Time Window**: Analysis based on the last 24 hours of metrics
- **Storage**: Identifies unused volumes and suboptimal storage configurations

## 💰 How It Works

### Resource Analysis

The tool performs deep analysis of your cloud resources:

#### 1. Usage Metrics Collection
- **CPU Utilization**: Identifies instances running below `CPU_THRESHOLD` (default: 10%)
- **Memory Usage**: Flags resources using less than `MEMORY_THRESHOLD` (default: 15%)
- **Storage Analysis**: Detects unused volumes and suboptimal storage configurations
- **Network Patterns**: Analyzes network usage patterns for right-sizing

#### 2. Cost Analysis
- Calculates current spending per resource
- Identifies potential savings based on usage patterns
- Suggests cheaper alternatives (e.g., reserved instances, spot instances)

### Optimization Methods

#### 1. Automatic Resource Management
When `AUTO_OPTIMIZE=true`:
- Stops/hibernates underutilized instances
- Deletes unused volumes
- Resizes overprovisioned resources
- Moves infrequently accessed data to cheaper storage tiers

#### 2. AWS Optimizations
- EC2 instance right-sizing
- EBS volume optimization
- S3 lifecycle policies
- RDS instance optimization

#### 3. Azure Optimizations
- VM size recommendations
- Disk storage optimization
- Unused resource cleanup
- Reserved instance recommendations

#### 4. GCP Optimizations
- Compute Engine right-sizing
- Storage class optimization
- Sustained use discount analysis
- Preemptible VM recommendations

### Reporting and Monitoring

#### 1. Cost Savings Reports
- Detailed breakdown of potential savings
- Resource-specific recommendations
- Historical usage patterns
- Implementation priority suggestions

#### 2. Continuous Monitoring
- Runs every `OPTIMIZATION_INTERVAL_HOURS` (default: 6)
- Tracks optimization impact
- Alerts on new saving opportunities
- Monitors resource usage trends

### Example Savings

```json
{
    "monthly_savings_summary": {
        "compute_optimization": "$1,200",
        "storage_optimization": "$300",
        "reserved_instances": "$500",
        "total_potential": "$2,000"
    },
    "actions_taken": {
        "stopped_instances": 5,
        "resized_instances": 3,
        "storage_optimized": "2TB"
    }
}
```

## 📊 Reports

Reports are generated in JSON format and saved in the `reports` directory. Each report includes:

```json
{
    "timestamp": "2024-12-15T09:39:52+01:00",
    "aws": {
        "underutilized_ec2": [...],
        "unused_ebs": [...],
        "underutilized_rds": [...],
        "s3_optimizations": [...]
    },
    "azure": {
        "underutilized_vms": [...]
    },
    "gcp": {
        "underutilized_instances": [...]
    },
    "estimated_monthly_savings": 150.25,
    "recommendations": [
        "Consider stopping AWS EC2 instance i-1234567890abcdef0",
        "Add lifecycle rules to S3 bucket my-bucket"
    ]
}
```

## 🔄 Continuous Operation

The tool runs continuously with:
- Initial analysis upon startup
- Scheduled analysis every 6 hours (configurable)
- Automatic resource optimization (if enabled)
- Continuous report generation

### Running in Background

Using systemd (recommended for production):
```bash
# Create service file
sudo nano /etc/systemd/system/cloud-optimizer.service

# Service file content
[Unit]
Description=Cloud Cost Optimizer
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/cloud-cost-optimizer
ExecStart=/path/to/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable cloud-optimizer
sudo systemctl start cloud-optimizer
```

## 🛠️ Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run specific test file
pytest tests/test_cloud_optimizer.py
```

### Adding New Cloud Providers

To add support for a new cloud provider:
1. Create a new method in `CloudResourceOptimizer` class
2. Implement resource analysis logic
3. Add provider-specific configuration in `.env.template`
4. Update tests and documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the documentation:
  - [Getting Started](docs/getting-started.md)
  - [Configuration Guide](docs/configuration.md)
  - [Cloud Providers](docs/cloud-providers.md)
  - [API Reference](docs/api-reference.md)
  - [Troubleshooting](docs/troubleshooting.md)
