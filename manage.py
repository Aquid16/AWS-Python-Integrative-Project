from my_config import get_args

args = get_args()

match args.resource:
    case "create-instance" | "list-instances" | "manage-instance": #| "terminate-instance":
        import ec2
    case "create-bucket" | "list-buckets" | "upload-file": #| "delete-bucket":
        import s3
    case "create-zone" | "update-record" | "delete-record": #| "delete-zone" :
        import route53