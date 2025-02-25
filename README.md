# AWS-Python Integrative Project

## Overview

This project demonstrates the integration of various AWS services using Python. It serves as a practical example of how to leverage AWS resources to build scalable and efficient applications.

## Features

- **Service Integration**: Showcases the seamless integration between services such as EC2, S3 and Route53 at of now.
- **Automation**: Implements automation scripts for resource provisioning and management.
- **Scalability**: Provides examples of scaling applications using AWS tools.
- **Security**: Incorporates best practices for securing AWS resources and data.

## Prerequisites

Before you begin, ensure you have the following:

- **AWS Account**: An active AWS account with sufficient permissions.
- **AWS CLI**: Installed and configured on your local machine. [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- **Python 3.x**: Ensure Python is installed. [Download Python](https://www.python.org/downloads/)

## Installation

Clone this repository:

```bash
git clone [https://github.com/DolevTB/PyhtonProject.git](https://github.com/Aquid16/AWS-Python-Integrative-Project.git)
cd AWS-Python-Integrative-Project
```

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

**AWS Credentials**: Ensure your AWS credentials are configured. You can set them up using the AWS CLI:

```bash
aws configure
```
Alternatively, set the following environment variables:

```bash
export AWS_ACCESS_KEY_ID='your-access-key-id'
export AWS_SECRET_ACCESS_KEY='your-secret-access-key'
export AWS_DEFAULT_REGION='your-preferred-region'
```

## Usage

Run the CLI tool with:

```bash
python manage.py
```
For more help, use -h or --help at any stage:

```bash
python manage.py -h
```

```bash
python manage.py --help
```

Run the UI tool with:

```bash
python gui.py
```

## Project Structure

```
.
├── manage.py              # Main CLI script to be run
├── ec2.py              # All EC2 functions
├── s3.py              # All S3 functions
├── route53.py              # All Route53 functions
├── gui.py              # Everything GUI related
├── my_config.py              # Parser for the CLI arguments
├── t3-nano-configurations.txt     # Configuration to be able to create t3.nano EC2 Instance
├── t4g-nano-configurations.txt     # Configuration to be able to create t4g.nano EC2 Instance
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
