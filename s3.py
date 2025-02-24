import boto3
import json
from my_config import get_args
from botocore.exceptions import ClientError

session = boto3.session.Session()
s3 = session.client('s3', region_name='us-east-1', endpoint_url="https://s3.amazonaws.com")

REQUIRED_TAG_KEY = 'Made by'
REQUIRED_TAG_VALUE = 'CLI'
PREFIX = "cli-"

args = get_args()
flag = True

def create_bucket(_flag):
    try:
        if args.access.lower() == 'public':
            assurance = input("Are you sure you want to create the bucket public? (yes/no) ").lower()
            if assurance == "yes":
                _flag = False
            elif assurance == "no":
                raise Exception("The operation has stopped, please re-enter the command with --access private")
            else:
                raise Exception("That was not a valid option")

        s3.create_bucket(Bucket=PREFIX + args.name)
        s3.put_bucket_tagging(
            Bucket=PREFIX + args.name,
            Tagging={
                'TagSet': [
                    {
                        'Key': 'Made by',
                        'Value': 'CLI'
                    },
                    {
                        'Key': 'Owner',
                        'Value': 'SharonSinelnikov'
                    }
                ]
            }
        )

        bucket = s3.put_public_access_block(
            Bucket=PREFIX + args.name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': _flag,
                'IgnorePublicAcls': _flag,
                'BlockPublicPolicy': _flag,
                'RestrictPublicBuckets': _flag
            }
        )

        if not _flag:
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "Statement",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject"
                        ],
                        "Resource": f"arn:aws:s3:::{PREFIX + args.name}/*"
                    }
                ]
            }

            policy_json = json.dumps(bucket_policy)

            s3.put_bucket_policy(Bucket=PREFIX + args.name, Policy=policy_json)
        print("Bucket created:", bucket)
    except ClientError as e:
        print("Error:", e)

def list_buckets():
    try:
        buckets = s3.list_buckets(
            Prefix=PREFIX,
            BucketRegion='us-east-1'
        )

        matching_buckets=[]

        for bucket in buckets["Buckets"]:
            bucket_name = bucket['Name']

            try:
                tag_response = s3.get_bucket_tagging(Bucket=bucket_name)
                s3_tags = tag_response['TagSet']

                for tag in s3_tags:
                    if tag['Key'] == REQUIRED_TAG_KEY and tag['Value'] == REQUIRED_TAG_VALUE:
                        matching_buckets.append(bucket_name)
                        break

            except ClientError as e:
                print(f"Error getting tags for bucket {bucket_name}: {e}")

        if matching_buckets:
            for bucket in matching_buckets:
                print(bucket)

        else:
            print("No buckets that were created by the CLI tool were found")

    except ClientError as e:
        print(f"Error listing buckets: {e}")

def upload_file():
    try:
        tagging_response = s3.get_bucket_tagging(
            Bucket=args.name
        )
        s3_tags = tagging_response['TagSet']

        for tag in s3_tags:
            if tag['Key'] == REQUIRED_TAG_KEY and tag['Value'] == REQUIRED_TAG_VALUE:
                s3.upload_file(args.path, args.name, args.key)
                print("File was uploaded successfully")

    except Exception as e:
        print(e)

# def delete_bucket():
#     try:
#         tagging_response = s3.get_bucket_tagging(
#             Bucket=args.name
#         )
#         s3_tags = tagging_response['TagSet']
#
#         for tag in s3_tags:
#             if tag['Key'] == REQUIRED_TAG_KEY and tag['Value'] == REQUIRED_TAG_VALUE:
#                 s3.delete_bucket(
#                     Bucket=args.name
#                 )
#                 print(f"Bucket {args.name} was deleted successfully")
#
#     except Exception as e:
#         print(e)


match args.resource:
    case "create-bucket":
        create_bucket(flag)

    case "list-buckets":
        list_buckets()

    case "upload-file":
        upload_file()

    # case "delete-bucket":
    #     delete_bucket()