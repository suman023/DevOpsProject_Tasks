# 🚀 DevOps Project: Terraform, Ansible & Jenkins CI/CD on AWS

## 📌 Project Overview

This repository contains an **end-to-end DevOps project** demonstrating the practical implementation of:

- **Infrastructure as Code (Terraform)**
- **Configuration Management (Ansible)**
- **CI/CD Automation (Jenkins, Docker, Amazon ECR)**

The project provisions AWS infrastructure, automatically configures servers, and deploys a containerized application using a Jenkins CI/CD pipeline.

**AWS Region:** eu-west-1 (Ireland)

---

## 🧩 Project Tasks

### 🔹 Task-1: Infrastructure Provisioning (Terraform)
- Custom VPC with public and private subnets
- Internet Gateway and NAT Gateway
- Route tables (public & private)
- Security Groups (Bastion, Jenkins, App, ALB)
- EC2 Instances:
  - Bastion Host
  - Jenkins Server
  - Application Server
- Application Load Balancer (ALB)
- Terraform Remote Backend:
  - S3 (state storage)
  - DynamoDB (state locking)

---

### 🔹 Task-2: Configuration Management (Ansible)
- Automated Docker installation
- Bastion host used as Ansible control node
- Jenkins and App EC2 configured as managed nodes
- Idempotent playbooks for repeatable execution

---

### 🔹 Task-3: CI/CD Pipeline (Jenkins + Docker + ECR)
- Jenkins pulls code from GitHub
- Docker image built using Dockerfile
- Image pushed to Amazon ECR
- Jenkins deploys container on App EC2 via SSH
- Old container stopped and replaced with new one

---

## 📁 Codebase Structure

All code is maintained in a **single GitHub repository**, logically separated by task.

---

### 🔹 Terraform Backend (Remote State)
terraform-backend/
└── main.tf

Used to create:
- S3 bucket for Terraform state
- DynamoDB table for state locking

---

### 🔹 Terraform Infrastructure (Task-1)
```
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
```

---


---

### 🔹 Ansible Configuration (Task-2)
```
ansible-config/
├── inventory/
│ └── hosts.ini
└── playbooks/
└── install-docker.yml 

```
### 🔹 Application & CI/CD (Task-3)
```
nodejs-docker-jenkins-demo/
├── vote/
│ ├── app.py
│ ├── requirements.txt
│ ├── Dockerfile
│ ├── templates/
│ │ └── index.html
│ └── static/
│ └── stylesheets/
│ └── style.css
└── Jenkinsfile
```
---

## ⚙️ How to Execute the Project
---
Terraform (Task-1)
```bash
cd terraform-backend
terraform init
terraform apply

cd ../terraform-aws-infra
terraform init
terraform plan
terraform apply

Ansible (Task-2)
cd ansible-config
ansible all -m ping
ansible-playbook playbooks/install-docker.yml

Jenkins (Task-3)

Configure Jenkins Pipeline using Jenkinsfile
Trigger Build Now
Application gets deployed automatically on App EC2

Cost Distribution (Estimated Monthly)

Total Estimated Monthly Cost: $129.88
├── NAT Gateway        : $37.35  (29%)
├── Jenkins EC2        : $32.77  (25%)
├── Application Load Balancer (ALB)
│                      $19.35  (15%)
├── App EC2            : $16.78  (13%)
├── Data Transfer      : $13.70  (11%)
├── Bastion EC2        : $9.19   (7%)
└── Storage / Other    : $1.44   (1%)
