# DevOpsProject_Tasks
UpGrad Tasks
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

☁️ AWS Tasks Summary:

This project involved the complete setup and use of AWS services to design, deploy, and manage a secure, automated cloud infrastructure. A custom Virtual Private Cloud (VPC) was created with both public and private subnets distributed across multiple Availability Zones to ensure high availability and fault tolerance. Internet connectivity was enabled using an Internet Gateway for public resources and a NAT Gateway for private resources.

Compute resources were provisioned using Amazon EC2, including a Bastion host for secure access, a Jenkins server for CI/CD operations, and an Application server for running the containerized application. Security was enforced through carefully configured Security Groups, ensuring least-privilege access between components.

An Application Load Balancer (ALB) was configured to securely expose Jenkins to the internet while keeping backend instances private. Amazon Elastic Container Registry (ECR) was used to store Docker images, enabling seamless integration with Jenkins for automated deployments. Amazon S3 and DynamoDB were used to manage Terraform remote state with versioning and state locking.

Overall, the AWS services were integrated following best practices for security, scalability, and automation, forming a robust foundation for the DevOps workflow implemented in this project.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

☁️ BookMyShow GCP Scalability Project Summary:

This project demonstrates scaling a BookMyShow-style ticketing platform on Google Cloud Platform across 7 tasks. Starting from a single Flask VM with in-memory data, the architecture was evolved step by step into a production-ready system.

Task 1 deployed a baseline VM and ran Locust load tests, recording p95 latency of 430ms at 1000 users.

Task 2 replaced the single VM with a Managed Instance Group of 2 to 5 VMs behind a Global Load Balancer at IP 34.95.101.123 with auto-scaling triggered at 60% CPU. 

Task 3 introduced Cloud SQL MySQL 8.0 with a primary instance at 34.180.32.191 for writes and a read replica at 34.47.176.241 for reads, replacing in-memory data with persistent storage. 

Task 4 moved static files to Cloud Storage and served them through Cloud CDN with a one year cache for CSS and JS files, reducing app server load by 15%. 

Task 5 load tested the full scaled architecture and achieved p95 latency of 180ms at 1000 users — a 54% improvement over baseline — with zero failures including a flash sale spike test of 500 sudden users processing 20,062 requests. 

Task 6 created preemptible batch VMs saving 79% on batch workloads, set up Pub/Sub billing alerts, and stopped the unused baseline VM saving around $25 per month. 

Task 7 configured three alert policies for CPU above 80%, latency above 1000ms, and instance count above 4, plus a live dashboard with four monitoring panels. 

The project proved that auto-scaling, read/write database splitting, CDN caching, and deep health checks together can handle flash sale traffic with zero failures and sub-200ms response times.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
