#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from google.cloud import compute_v1
from google.cloud import billing
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CloudResourceOptimizer:
    def __init__(self):
        load_dotenv()
        self.aws_enabled = bool(os.getenv('AWS_ACCESS_KEY_ID'))
        self.azure_enabled = bool(os.getenv('AZURE_SUBSCRIPTION_ID'))
        self.gcp_enabled = bool(os.getenv('GOOGLE_CLOUD_PROJECT'))
        
    def analyze_aws_resources(self) -> Dict:
        """Analyze AWS resources for optimization opportunities."""
        if not self.aws_enabled:
            logger.warning("AWS credentials not configured")
            return {}

        try:
            ec2 = boto3.client('ec2')
            cloudwatch = boto3.client('cloudwatch')
            rds = boto3.client('rds')
            s3 = boto3.client('s3')
            
            results = {
                'underutilized_ec2': [],
                'unused_ebs': [],
                'underutilized_rds': [],
                's3_optimizations': []
            }
            
            # EC2 Analysis
            instances = ec2.describe_instances()
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    if instance['State']['Name'] == 'running':
                        metrics = cloudwatch.get_metric_statistics(
                            Namespace='AWS/EC2',
                            MetricName='CPUUtilization',
                            Dimensions=[{'Name': 'InstanceId', 'Value': instance['InstanceId']}],
                            StartTime=datetime.utcnow() - timedelta(hours=24),
                            EndTime=datetime.utcnow(),
                            Period=3600,
                            Statistics=['Average']
                        )
                        
                        if metrics['Datapoints'] and sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints']) < 10:
                            results['underutilized_ec2'].append({
                                'InstanceId': instance['InstanceId'],
                                'InstanceType': instance['InstanceType'],
                                'AverageUtilization': sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints'])
                            })

            # EBS Volume Analysis
            volumes = ec2.describe_volumes()
            for volume in volumes['Volumes']:
                if volume['State'] == 'available':  # Unattached volumes
                    results['unused_ebs'].append({
                        'VolumeId': volume['VolumeId'],
                        'Size': volume['Size'],
                        'VolumeType': volume['VolumeType'],
                        'State': 'Unattached'
                    })

            # RDS Analysis
            db_instances = rds.describe_db_instances()
            for db in db_instances['DBInstances']:
                metrics = cloudwatch.get_metric_statistics(
                    Namespace='AWS/RDS',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db['DBInstanceIdentifier']}],
                    StartTime=datetime.utcnow() - timedelta(hours=24),
                    EndTime=datetime.utcnow(),
                    Period=3600,
                    Statistics=['Average']
                )
                
                if metrics['Datapoints'] and sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints']) < 10:
                    results['underutilized_rds'].append({
                        'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                        'InstanceClass': db['DBInstanceClass'],
                        'Engine': db['Engine'],
                        'AverageUtilization': sum(d['Average'] for d in metrics['Datapoints']) / len(metrics['Datapoints'])
                    })

            # S3 Analysis
            buckets = s3.list_buckets()
            for bucket in buckets['Buckets']:
                # Get bucket metrics
                metrics = cloudwatch.get_metric_statistics(
                    Namespace='AWS/S3',
                    MetricName='BucketSizeBytes',
                    Dimensions=[{'Name': 'BucketName', 'Value': bucket['Name']}],
                    StartTime=datetime.utcnow() - timedelta(days=30),
                    EndTime=datetime.utcnow(),
                    Period=86400,
                    Statistics=['Average']
                )
                
                # Get lifecycle rules
                try:
                    lifecycle = s3.get_bucket_lifecycle_configuration(Bucket=bucket['Name'])
                except ClientError:
                    lifecycle = {'Rules': []}
                
                results['s3_optimizations'].append({
                    'BucketName': bucket['Name'],
                    'HasLifecycle': bool(lifecycle.get('Rules')),
                    'SizeBytes': metrics['Datapoints'][-1]['Average'] if metrics['Datapoints'] else 0,
                    'Recommendation': 'Add lifecycle rules' if not lifecycle.get('Rules') else None
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing AWS resources: {str(e)}")
            return {}

    def analyze_azure_resources(self) -> Dict:
        """Analyze Azure resources for optimization opportunities."""
        if not self.azure_enabled:
            logger.warning("Azure credentials not configured")
            return {}

        try:
            credential = DefaultAzureCredential()
            subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
            compute_client = ComputeManagementClient(credential, subscription_id)
            monitor_client = MonitorManagementClient(credential, subscription_id)
            
            vms = compute_client.virtual_machines.list_all()
            underutilized = []
            
            for vm in vms:
                metrics = monitor_client.metrics.list(
                    resource_uri=vm.id,
                    timespan=f"{(datetime.utcnow() - timedelta(hours=24)).isoformat()}/{datetime.utcnow().isoformat()}",
                    interval='PT1H',
                    metricnames='Percentage CPU'
                )
                
                if metrics.value:
                    avg_cpu = sum(t.average for t in metrics.value[0].timeseries[0].data if t.average is not None) / \
                             len([t for t in metrics.value[0].timeseries[0].data if t.average is not None])
                    
                    if avg_cpu < 10:
                        underutilized.append({
                            'VMName': vm.name,
                            'Size': vm.hardware_profile.vm_size,
                            'AverageUtilization': avg_cpu
                        })
            
            return {'underutilized_vms': underutilized}
            
        except Exception as e:
            logger.error(f"Error analyzing Azure resources: {str(e)}")
            return {}

    def analyze_gcp_resources(self) -> Dict:
        """Analyze GCP resources for optimization opportunities."""
        if not self.gcp_enabled:
            logger.warning("GCP credentials not configured")
            return {}

        try:
            instance_client = compute_v1.InstancesClient()
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            
            request = compute_v1.ListZonesRequest(project=project_id)
            zones = compute_v1.ZonesClient().list(request=request)
            
            underutilized = []
            for zone in zones:
                request = compute_v1.ListInstancesRequest(
                    project=project_id,
                    zone=zone.name
                )
                instances = instance_client.list(request=request)
                
                for instance in instances:
                    if instance.status == 'RUNNING':
                        underutilized.append({
                            'InstanceName': instance.name,
                            'MachineType': instance.machine_type,
                            'Zone': zone.name
                        })
            
            return {'underutilized_instances': underutilized}
            
        except Exception as e:
            logger.error(f"Error analyzing GCP resources: {str(e)}")
            return {}

    def generate_optimization_report(self) -> Dict:
        """Generate a comprehensive optimization report."""
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'aws': self.analyze_aws_resources(),
            'azure': self.analyze_azure_resources(),
            'gcp': self.analyze_gcp_resources()
        }
        
        total_savings = 0
        recommendations = []
        
        if 'underutilized_ec2' in report['aws']:
            for instance in report['aws']['underutilized_ec2']:
                estimated_savings = 50  # placeholder value
                total_savings += estimated_savings
                recommendations.append(f"Consider stopping or downsizing AWS EC2 instance {instance['InstanceId']}")
        
        if 'underutilized_vms' in report['azure']:
            for vm in report['azure']['underutilized_vms']:
                estimated_savings = 40  # placeholder value
                total_savings += estimated_savings
                recommendations.append(f"Consider stopping or downsizing Azure VM {vm['VMName']}")
        
        if 'underutilized_instances' in report['gcp']:
            for instance in report['gcp']['underutilized_instances']:
                estimated_savings = 45  # placeholder value
                total_savings += estimated_savings
                recommendations.append(f"Consider stopping or downsizing GCP instance {instance['InstanceName']}")
        
        report['estimated_monthly_savings'] = total_savings
        report['recommendations'] = recommendations
        
        return report

    def save_report(self, report: Dict, filename: str = None):
        """Save the optimization report to a file."""
        if filename is None:
            filename = f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved to {filename}")

    def stop_underutilized_resources(self):
        """Stop or hibernate underutilized resources across cloud providers."""
        try:
            # AWS resources
            if self.aws_enabled:
                ec2 = boto3.client('ec2')
                report = self.analyze_aws_resources()
                for instance in report.get('underutilized_ec2', []):
                    logger.info(f"Stopping AWS EC2 instance {instance['InstanceId']}")
                    ec2.stop_instances(InstanceIds=[instance['InstanceId']])

            # Azure resources
            if self.azure_enabled:
                credential = DefaultAzureCredential()
                subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
                compute_client = ComputeManagementClient(credential, subscription_id)
                report = self.analyze_azure_resources()
                for vm in report.get('underutilized_vms', []):
                    logger.info(f"Stopping Azure VM {vm['VMName']}")
                    resource_group = vm['VMName'].split('/')[4]
                    compute_client.virtual_machines.begin_deallocate(resource_group, vm['VMName'])

            # GCP resources
            if self.gcp_enabled:
                instance_client = compute_v1.InstancesClient()
                project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
                report = self.analyze_gcp_resources()
                for instance in report.get('underutilized_instances', []):
                    logger.info(f"Stopping GCP instance {instance['InstanceName']}")
                    zone = instance['Zone']
                    request = compute_v1.StopInstanceRequest(
                        project=project_id,
                        zone=zone,
                        instance=instance['InstanceName']
                    )
                    instance_client.stop(request=request)

        except Exception as e:
            logger.error(f"Error stopping underutilized resources: {str(e)}")

    def scheduled_optimization(self):
        """Run optimization tasks on a schedule."""
        report = self.generate_optimization_report()
        self.save_report(report)
        
        # Stop underutilized resources if automatic optimization is enabled
        if os.getenv('AUTO_OPTIMIZE', 'false').lower() == 'true':
            self.stop_underutilized_resources()
