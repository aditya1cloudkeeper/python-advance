def check_mfa_for_users():
    iam_client = boto3.client("iam")
    users = iam_client.list_users()["Users"]
    
    with open("iam_users_mfa.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IAMUserName", "MFAEnabled"])
        
        for user in users:
            mfa_devices = iam_client.list_mfa_devices(UserName=user["UserName"])['MFADevices']
            writer.writerow([user["UserName"], bool(mfa_devices)])

def check_public_sg():
    ec2_client = boto3.client("ec2")
    security_groups = ec2_client.describe_security_groups()["SecurityGroups"]
    
    with open("public_security_groups.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["SGName", "Port", "AllowedIP"])
        
        for sg in security_groups:
            for rule in sg["IpPermissions"]:
                for ip_range in rule.get("IpRanges", []):
                    if ip_range["CidrIp"] == "0.0.0.0/0":
                        writer.writerow([sg["GroupName"], rule.get("FromPort", "All"), ip_range["CidrIp"]])