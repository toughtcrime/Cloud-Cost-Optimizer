#!/usr/bin/env python3
import logging
import schedule
import time
from cloud_optimizer import CloudResourceOptimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the cloud resource optimizer."""
    optimizer = CloudResourceOptimizer()
    
    # Run immediately once
    optimizer.scheduled_optimization()
    
    # Schedule regular runs
    schedule.every(6).hours.do(optimizer.scheduled_optimization)
    
    logger.info("Cloud Resource Optimizer started. Running every 6 hours.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)
