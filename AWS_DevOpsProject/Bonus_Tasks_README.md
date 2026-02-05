## Network Architecture Diagram:


                                   Internet
                                       │
                                       ▼
                          ┌────────────────────────┐
                          │  Internet Gateway      │
                          │  devops-igw            │
                          └───────────┬────────────┘
                                      │
                ┌─────────────────────┴─────────────────────┐
                │                                           │
                ▼                                           ▼
    ┌─────────────────────────┐              ┌─────────────────────────┐
    │  Public Subnet 1        │              │  Public Subnet 2        │
    │  10.0.1.0/24            │              │  10.0.2.0/24            │
    │  eu-west-1a             │              │  eu-west-1b             │
    │                         │              │                         │
    │  ┌──────────────────┐   │              │  ┌──────────────────┐   │
    │  │ Bastion EC2      │   │              │  │ Jenkins ALB      │   │
    │  │ bastion-sg       │   │              │  │ alb-sg           │   │
    │  └──────────────────┘   │              │  └────────┬─────────┘   │
    │                         │              │           │             │
    │  ┌──────────────────┐   │              │           │             │
    │  │ NAT Gateway      │   │              │           │             │
    │  │ devops-ntgw      │   │              │           │             │
    │  └────────┬─────────┘   │              │           │             │
    └───────────┼─────────────┘              └───────────┼─────────────┘
                │                                        │
                │ (Routes 0.0.0.0/0)                     │ (/jenkins path)
                │                                        │
                ▼                                        ▼
    ┌───────────────────────────────────────────────────────────────┐
    │                    Private Subnets                            │
    ├──────────────────────────┬────────────────────────────────────┤
    │  Private Subnet Jenkins  │  Private Subnet App                │
    │  10.0.3.0/24             │  10.0.4.0/24                       │
    │  eu-west-1a              │  eu-west-1b                        │
    │                          │                                    │
    │  ┌──────────────────┐    │  ┌──────────────────┐              │
    │  │ Jenkins EC2      │    │  │ App EC2          │              │
    │  │ jenkins-sg       │◄───┼──┤ app-sg           │              │
    │  │ Port: 8080       │    │  │                  │              │
    │  └──────────────────┘    │  └──────────────────┘              │
    │                          │                                    │
    │  Target: jenkins-tg      │                                    │
    └──────────────────────────┴────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │                Backend Infrastructure                       │
    ├─────────────────────────────────────────────────────────────┤
    │  S3 Bucket: devops-s3-terraform-state-suman                 │
    │  DynamoDB: terraform-lock-table                             │
    └─────────────────────────────────────────────────────────────┘









## Cost Breakdown by Component:

### EC2 Instances: $58.74/month (45%)

| Resource | Type | Monthly Cost |
|----------|------|--------------|
| Bastion EC2 | t3.micro + 20GB | $9.19 |
| Jenkins EC2 | t3.medium + 30GB | $32.77 |
| App EC2 | t3.small + 20GB | $16.78 |

### Networking: $70.40/month (54%)

| Resource | Monthly Cost |
|----------|--------------|
| NAT Gateway (incl. data) | $37.35 |
| Application Load Balancer | $19.35 |
| Data Transfer | $13.70 |

### Storage & Other: $1.44/month (1%)

| Resource | Monthly Cost |
|----------|--------------|
| S3 (Terraform state) | $0.02 |
| DynamoDB (state locking) | $0.02 |
| ECR (container registry) | $1.40 |

### Cost Distribution:

Total Monthly: $129.88

├── NAT Gateway: $37.35 (29%)
├── Jenkins EC2: $32.77 (25%)
├── ALB: $19.35 (15%)
├── App EC2: $16.78 (13%)
├── Data Transfer: $13.70 (11%)
├── Bastion EC2: $9.19 (7%)
└── Storage/Other: $1.44 (1%)



## Codebase Structure:

terraform-backend/
└── main.tf

terraform-aws-infra/
├── backend.tf
├── provider.tf
├── variables.tf
├── vpc.tf
├── subnets.tf
├── igw.tf
├── nat.tf
├── route_tables.tf
├── security_groups.tf
├── ec2.tf
├── alb.tf
└── outputs.tf




nodejs-docker-jenkins-demo/
├── vote/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── stylesheets/
│           └── style.css
└── Jenkinsfile


ansible-config/
├── inventory/
│   └── hosts.ini
└── playbooks/
    └── install-docker.yml











