import pulumi
import pulumi_aws as aws
import pulumi.automation as auto
from my_config import get_args

class EC2InstanceStack(pulumi.ComponentResource):
    def __init__(self, name, args, opts=None):
        super().__init__("custom:aws:EC2InstanceStack", name, {}, opts)

        if args.amount.isdigit():
            for i in range(int(args.amount)):
                # Configuration
                subnet_id = 'subnet-03ece7b5e0c74220a'
                security_group_id = 'sg-0b779267b4b8ad388'
                owner = 'SharonSinelnikov'

                aws_provider = aws.Provider("aws", region=args.region)

                stack = auto.create_or_select_stack(stack_name="EC2", project_name="IntegrativePythonProject", program="Pulumi Program")

                self.ec2_instance = aws.ec2.Instance(f"Sharon-Server-{i+1}",
                                        instance_type=args.type,
                                        ami=args.ami,
                                        subnet_id=subnet_id,
                                        vpc_security_group_ids=[security_group_id],
                                        tags={"Name": f"Sharon-Server-{i+1}", "Owner": owner, "Made_by": "CLI"},
                                        opts=pulumi.ResourceOptions(provider=aws_provider, retain_on_delete=True)
                                         )
                self.register_outputs({
                    "instance_id": self.ec2_instance.id
                })

# Ensure Pulumi executes inside a stack
args = get_args()
if args.resource == "create-instance":
    instance_stack = EC2InstanceStack("EC2", args)
    pulumi.export("instance_id", instance_stack.ec2_instance.id)