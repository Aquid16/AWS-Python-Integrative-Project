"""This file holds all the options for the resource creation and their arguments options for the CLI"""

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Create an AWS resource using Pulumi.", add_help=True)
    subparser = parser.add_subparsers(dest="resource", required=True, help="*(Required) Resource to create")

    # EC2 Subparser
    create_instance = subparser.add_parser("create-instance", help="Create an EC2 instance")
    create_instance.add_argument("--type", type=str, required=True,
                                 help="*(Required) The type of EC2 instance (t3.nano or t4g.nano)")
    create_instance.add_argument("--os", type=str, required=True,
                                 help="*(Required) The OS type the EC2 instance should be (ubuntu or amazon-linux")
    create_instance.add_argument("--name", type=str, required=True,
                                 help="*(Required) The name you want to assign to the instance/s")
    create_instance.add_argument("--amount", type=str, required=True,
                                 help="*(Required) The amount of instances to create 1 or 2")
# -------------
    subparser.add_parser("list-instances", help="List all EC2 instances created by the CLI")
# -------------
    manage_instance = subparser.add_parser("manage-instance",
                                           help="Manage, Start and Stop an EC2 instance")
    manage_instance.add_argument("--instance-id", type=str, required=True,
                                 help="*(Required) The ID of the instance you want to manage")
    manage_instance.add_argument("--operation", type=str, required=True,
                                 help="*(Required) The operation you want to perform on the instance (Start or Stop)")
# ------------
#     terminate_instance = subparser.add_parser("terminate-instance", help="Terminates an EC2 instance")
#     terminate_instance.add_argument("--instance-id", type=str, required=True, help="The ID of the instance to be terminated")

    # S3 Subparser
    create_bucket = subparser.add_parser("create-bucket", help="Create an S3 bucket")
    create_bucket.add_argument("--name", type=str, required=True,
                               help="*(Required) The name of the S3 bucket to create")
    create_bucket.add_argument("--access", type=str, required=True,
                               help="*(Required) The access you want for the S3 bucket (Public or Private)")
# -------------
    subparser.add_parser("list-buckets", help="List all the buckets created by the CLI")
# -------------
    upload_to_bucket = subparser.add_parser("upload-file", help="Uploads a file to the S3 bucket")
    upload_to_bucket.add_argument("--path", type=str,
                                  help="*(Required) The path to the file you want to upload")
    upload_to_bucket.add_argument("--name", type=str, required=True,
                                  help="*(Required) The bucket you want to upload to (Must include the prefix 'cli-')")
    upload_to_bucket.add_argument("--key", type=str, required=True,
                                  help="*(Required) The name of the file as it will be shown in the bucket")
# -------------
#     delete_bucket = subparser.add_parser("delete-bucket", help="Delete an S3 bucket")
#     delete_bucket.add_argument("--name", type=str, required=True,
#                                help="The name of the bucket you want to delete (Must include the prefix 'cli-')")

    # Route53 Subparser
    create_zone = subparser.add_parser("create-zone", help="Create a Route53 DNS zone")
    create_zone.add_argument("--name", type=str, required=True,
                             help="*(Required) The name for the DNS zone")
    create_zone.add_argument("--domain", type=str, required=True,
                             help="*(Required) The domain for the DNS zone")
# -----------
    delete_zone = subparser.add_parser("delete-zone", help="Delete a Route53 zone")
    delete_zone.add_argument("--id", type=str, required=True,
                             help="*(Required) The ID of the DNS zone yoy want to delete")

    update_zone = subparser.add_parser("update-record", help="Update a record inside an already existing Route53 DNS zone")
    update_zone.add_argument("--id", type=str, required=True,
                             help="*(Required) The ID of the DNS zone you want to update/modify")
    update_zone.add_argument("--domain-name", type=str, required=True,
                             help="*(Required) The domain name of the DNS zone you want to update/modify")
    update_zone.add_argument("--type", type=str, required=True,
                             help="*(Required) The type of record you want to update/modify")
    update_zone.add_argument("--new-value", type=str, required=True,
                             help="*(Required) The new value of the record you want to update/modify")
# ------------
#     delete_record = subparser.add_parser("delete-record", help="Delete a record inside the DNS zone")
#     delete_record.add_argument("--id", type=str, required=True,
#                                help="*(Required) The ID of the DNS zone you want to delete")
#     delete_record.add_argument("--domain-name", type=str, required=True,
#                                help="*(Required) The domain name of the DNS zone you want to delete")
#     delete_record.add_argument("--type", type=str, required=True,
#                                help="*(Required) The type of record you want to delete")
#     delete_record.add_argument("--values", type=str, required=True,
#                                help="*(Required) A list of exact values the record you want to delete has")

    return parser.parse_args()