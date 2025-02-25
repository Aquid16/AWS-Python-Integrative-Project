import boto3
from my_config import get_args

session = boto3.session.Session()
route53 = session.client('route53', region_name='us-east-1')

REQUIRED_TAG_KEY = 'Made by'
REQUIRED_TAG_VALUE = 'CLI'

args = get_args()

def make_new_record_set(record_type, domain_name, new_value):
    record_set = {
        'Name': domain_name,
        'Type': record_type,
        'TTL': 300,
        'ResourceRecords':[{'Value': new_value}]
    }

    return record_set

def get_record_details(hosted_zone_id, domain_name, record_type):
    record_sets = route53.list_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        StartRecordName=domain_name,
        StartRecordType=record_type,
        MaxItems="1"
    )

    for record in record_sets["ResourceRecordSets"]:
        if record["Name"] == domain_name + "." and record["Type"] == record_type:
            print("Found the record")
            return record # Return the full record details

    print("No record was found")
    return None # No matching record was found

def create_zone():
    try:
        zones = route53.create_hosted_zone(
            Name=f'{args.name}.{args.domain}',
            CallerReference=str(hash(f'{args.name}.{args.domain}')),
        )

        print("Hosted Zone Created successfully!")
        zone_id = zones['HostedZone']['Id'].split('/')[-1]
        zone_name = zones['HostedZone']['Name']
        print(f"Hosted Zone Name: {zone_name}, Hosted Zone Id: {zone_id}")

        route53.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=[
                {
                    'Key': 'Made by',
                    'Value': 'CLI'
                },
                {
                    'Key': 'Owner',
                    'Value': 'SharonSinelnikov'
                }
            ]
        )

    except Exception as e:
        print(e)

def delete_zone():
    try:
        route53.delete_hosted_zone(
            Id=args.id
        )

        print(f"Hosted Zone {args.id} was deleted successfully!")

    except Exception as e:
        print(e)

def update_record():
    try:
        zones = route53.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=args.id
        )

        tags = {tag['Key']: tag['Value'] for tag in zones['ResourceTagSet']['Tags']}

        if REQUIRED_TAG_KEY in tags:
            if tags[REQUIRED_TAG_KEY] == REQUIRED_TAG_VALUE:
                print("Has required tag")
                new_set = make_new_record_set(args.type, args.domain_name, args.new_value)
                route53.change_resource_record_sets(
                    HostedZoneId=args.id,
                    ChangeBatch={
                        'Comment': 'Updating/Modifying DNS record',
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': new_set
                            }
                        ]
                    }
                )

        print("Record was updated")

    except Exception as e:
        print(e)

def delete_record():
    try:
        zones = route53.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=args.id
        )

        tags = {tag['Key']: tag['Value'] for tag in zones['ResourceTagSet']['Tags']}

        if REQUIRED_TAG_KEY in tags:
            if tags[REQUIRED_TAG_KEY] == REQUIRED_TAG_VALUE:
                print("Has required tag")
                record_to_delete = get_record_details(args.id, args.domain_name, args.type)
                route53.change_resource_record_sets(
                    HostedZoneId=args.id,
                    ChangeBatch={
                        'Comment': 'Deleting DNS record',
                        'Changes': [
                            {
                                'Action': 'DELETE',
                                'ResourceRecordSet': record_to_delete
                            }
                        ]
                    }
                )

        print("Record was deleted")

    except Exception as e:
        print(e)

match args.resource:
    case "create-zone":
        create_zone()

    case "update-record":
        update_record()

    case "delete-record":
        delete_record()

    case "delete-zone":
        delete_zone()