from my_config import get_args

args = get_args()

if args.resource == "create-instance":
    import ec2_create
# elif args.resource == "create-bucket":
#     import s3_create
# elif args.resource == "create-zone":
#     import zone_create