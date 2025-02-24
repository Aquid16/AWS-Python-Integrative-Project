import boto3
from my_config import get_args

session = boto3.session.Session()
ec2 = session.resource('ec2', region_name='us-east-1')
ec2_inst = session.client('ec2', region_name='us-east-1')

REQUIRED_TAG_KEY = 'Made by'
REQUIRED_TAG_VALUE = 'CLI'
INSTANCE_LIMIT = 2

def get_conf(inst_type):
    if inst_type == "t3.nano":
        configuration = open("t3-nano-configurations.txt").readlines()
    elif inst_type == "t4g.nano":
        configuration = open("t4g-nano-configurations.txt").readlines()

    conf_dict = {}
    for line in configuration:
        key, value = line.strip().split(':')
        conf_dict[key.strip()] = value.strip()

    return conf_dict

def launch_instance(num_of_instances, image_id, instance_type, subnet_id, security_group):
    for i in range(int(num_of_instances)):
        try:
            print("Creating and EC2 instance")
            instances = ec2.create_instances(
                #DryRun = True,
                ImageId= image_id,
                MinCount=1,
                MaxCount=1,
                InstanceType= instance_type,
                NetworkInterfaces = [
                    {
                        'DeviceIndex' : 0,
                        'SubnetId' : subnet_id,
                        'Groups' : [
                            security_group
                        ],
                        'AssociatePublicIpAddress' : False
                    }
                ],
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': REQUIRED_TAG_KEY,
                                'Value': REQUIRED_TAG_VALUE
                            },
                            {
                                'Key': 'Owner',
                                'Value': 'SharonSinelnikov'
                            },
                            {
                                'Key': 'Name',
                                'Value': f'{args.name}-{instance_type}-{i+1}'
                            }
                        ]
                    }
                ],
            )
            print_instance_id(instances)


        except Exception as e:
            print(e)

def print_instance_id(instances):
    for instance in instances:
        print(f"Instance: {instance.instance_id} was created by the CLI")

def get_instance_count():
    ec2_instances = ec2_inst.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped'],
                'Name': 'tag:Made by',
                'Values': ['CLI']
            }
        ]
    )
    instances = [
        ins
        for reservation in ec2_instances["Reservations"]
        for ins in reservation["Instances"]
        if ins['State']['Name'] == 'running' or ins['State']['Name'] == 'stopped'
    ]

    return len(instances)

def create_instance():
    current_instance_count = get_instance_count()

    if current_instance_count < INSTANCE_LIMIT:
        if args.amount.isdigit() and 0 < int(args.amount) <= 2:
            config_dict = get_conf(args.type)
            if args.type == "t3.nano":
                if args.os.lower() == "ubuntu":
                    launch_instance(args.amount, config_dict['ubuntu-image-id'], args.type, config_dict['subnet-id'],
                                config_dict['security-group'])

                elif args.os.lower() == "amazon-linux":
                    launch_instance(args.amount, config_dict['amazon-linux-image-id'], args.type, config_dict['subnet-id'],
                                config_dict['security-group'])

            elif args.type == "t4g.nano":
                if args.os.lower() == "ubuntu":
                    launch_instance(args.amount, config_dict['ubuntu-image-id'], args.type, config_dict['subnet-id'],
                                config_dict['security-group'])

                elif args.os.lower() == "amazon-linux":
                    launch_instance(args.amount, config_dict['amazon-linux-image-id'], args.type, config_dict['subnet-id'],
                                config_dict['security-group'])
        else:
            print("Please make sure you're setting amount as digit and not less than 1 or more than 2")
    else:
        print(f"Instance creation is blocked! {INSTANCE_LIMIT} instances already exist")
        return

def list_instances():
    ec2_instances = ec2_inst.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped', 'stopping'],
                'Name': 'tag:Made by',
                'Values': ['CLI']
            }
        ]
    )

    for reservation in ec2_instances["Reservations"]:
        for ins in reservation["Instances"]:
            if (ins['State']['Name'] == 'running' or ins['State']['Name'] == 'stopped'
                    or ins['State']['Name'] == 'stopping'):
                print(f"Instance: {ins['InstanceId']}, State: {ins['State']['Name']}")

def manage_instance():
    ec2_tags = ec2_inst.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [
                    args.instance_id
                ]
            }
        ]
    )
    tags = {tag['Key']: tag['Value'] for tag in ec2_tags['Tags']}
    if REQUIRED_TAG_KEY in tags:
        if tags[REQUIRED_TAG_KEY] == REQUIRED_TAG_VALUE:
            print("Tag was found")
            if args.operation.lower() == "start":
                ec2_inst.start_instances(
                    InstanceIds=[
                        f'{args.instance_id}'
                    ]
                )

                print(f"Instance {args.instance_id} is now Starting!")

            elif args.operation.lower() == "stop":
                ec2_inst.stop_instances(
                    InstanceIds=[
                        f'{args.instance_id}'
                    ]
                )

                print(f"Instance {args.instance_id} is now Stopping!")

    else:
        print("Tag was not found")

# def terminate_instance():
#     ec2_tags = ec2_inst.describe_tags(
#         Filters=[
#             {
#                 'Name': 'resource-id',
#                 'Values': [
#                     args.instance_id
#                 ]
#             }
#         ]
#     )
#
#     tags = {tag['Key']: tag['Value'] for tag in ec2_tags['Tags']}
#     if REQUIRED_TAG_KEY in tags:
#         if tags[REQUIRED_TAG_KEY] == REQUIRED_TAG_VALUE:
#             print("Tag was found")
#             ec2_inst.terminate_instances(
#                 InstanceIds=[
#                     f'{args.instance_id}'
#                 ]
#             )
#
#             print(f"Instance {args.instance_id} is now being terminated!")
#     else:
#         print("Tag was not found")


args = get_args()

match args.resource:
    case "create-instance":
        create_instance()

    case  "list-instances":
        list_instances()

    case "manage-instance":
        manage_instance()

    # case "terminate-instance":
    #     terminate_instance()