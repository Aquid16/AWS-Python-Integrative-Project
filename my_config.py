"""This file holds all the options for the resource creation and their arguments options for the CLI"""

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Create an AWS resource using Pulumi.", add_help=True)
    subparser = parser.add_subparsers(dest="resource", required=True, help="Resource to create")

    # EC2 Subparser
    create_instance = subparser.add_parser("create-instance", help="Create an EC2 instance")
    create_instance.add_argument("--type", type=str, required=True, help="The type of EC2 instance (t3.nano or t4g.nano)")
    create_instance.add_argument("--ami", type=str, required=True, help="The AMI type the EC2 instance should be (Ubuntu or Amazon Linux")
    create_instance.add_argument("--amount", type=str, required=True, help="The amount of instances to create 1 or 2")
    create_instance.add_argument("--region", type=str, required=True, help="The region where the instance should be created")

    # S3 Subparser
    create_bucket = subparser.add_parser("create-bucket", help="Create an S3 bucket")
    create_bucket.add_argument("--name", type=str, required=True, help="The name of the S3 bucket to create")
    create_bucket.add_argument("--type", type=str, required=True, help="The type of the S3 bucket (Public or Private)")
    create_bucket.add_argument("--region", type=str, required=True, help="The region where the instance should be created")

    # Route53 Subparser
    create_zone = subparser.add_parser("create-zone", help="Create a Route 53 zone")
    create_zone.add_argument("--domain-name", type=str, required=True, help="The domain name for the Route 53 zone")
    create_zone.add_argument("--region", type=str, required=True, help="The region where the instance should be created")

    return parser.parse_args()