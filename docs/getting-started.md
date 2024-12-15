# Getting Started

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Access to cloud provider accounts
- Cloud provider credentials

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cloud-cost-optimizer.git
cd cloud-cost-optimizer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Docker Installation

1. Build the image:
```bash
docker build -t cloud-cost-optimizer .
```

2. Run with Docker:
```bash
docker run -d \
    -v $(pwd)/reports:/app/reports \
    -v $(pwd)/.env:/app/.env \
    --name cost-optimizer \
    cloud-cost-optimizer
```

## First Run

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` with your cloud credentials

3. Run the optimizer:
```bash
python run.py
```

## Verifying Installation

1. Check the logs:
```bash
tail -f optimizer.log
```

2. Look for the first optimization report in the `reports` directory:
```bash
ls -l reports/
```

## Next Steps

- Configure [optimization thresholds](configuration.md#thresholds)
- Set up [automated resource management](configuration.md#automation)
- Review [cloud provider setup](cloud-providers.md)
