# DevOpsProject_Tasks
UpGrad Tasks

☁️ AWS Tasks Summary:

This project involved the complete setup and use of AWS services to design, deploy, and manage a secure, automated cloud infrastructure. A custom Virtual Private Cloud (VPC) was created with both public and private subnets distributed across multiple Availability Zones to ensure high availability and fault tolerance. Internet connectivity was enabled using an Internet Gateway for public resources and a NAT Gateway for private resources.

Compute resources were provisioned using Amazon EC2, including a Bastion host for secure access, a Jenkins server for CI/CD operations, and an Application server for running the containerized application. Security was enforced through carefully configured Security Groups, ensuring least-privilege access between components.

An Application Load Balancer (ALB) was configured to securely expose Jenkins to the internet while keeping backend instances private. Amazon Elastic Container Registry (ECR) was used to store Docker images, enabling seamless integration with Jenkins for automated deployments. Amazon S3 and DynamoDB were used to manage Terraform remote state with versioning and state locking.

Overall, the AWS services were integrated following best practices for security, scalability, and automation, forming a robust foundation for the DevOps workflow implemented in this project.
