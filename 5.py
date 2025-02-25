def find_unused_ec2():
    cloudwatch = boto3.client("cloudwatch")
    ec2_client = boto3.client("ec2")
    instances = ec2_client.describe_instances()["Reservations"]
    
    for reservation in instances:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime='2024-01-01T00:00:00Z',
                EndTime='2024-12-31T23:59:59Z',
                Period=86400,
                Statistics=['Average']
            )
            
            avg_cpu = sum([datapoint["Average"] for datapoint in metrics.get("Datapoints", [])]) / (len(metrics.get("Datapoints", [])) or 1)
            if avg_cpu < 10:
                print(f"Instance {instance_id} has low CPU utilization.")

def find_idle_rds():
    rds_client = boto3.client("rds")
    instances = rds_client.describe_db_instances()["DBInstances"]
    
    for instance in instances:
        if instance["DBInstanceStatus"] == "available":
            print(f"RDS Instance {instance['DBInstanceIdentifier']} is running but might be idle.")

if _name_ == "_main_":
    list_ec2_instance_types()
    list_billed_regions()
    check_mfa_for_users()
    check_public_sg()
    find_unused_ec2()
    find_idle_rds()