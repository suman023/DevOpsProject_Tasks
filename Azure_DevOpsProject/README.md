# What We Built
A two-region Azure cloud infrastructure connecting East US and East US 2 using VPN, with web servers, a backend server, firewall, and resilient storage — all deployed via ARM templates.

### Task 1 — Virtual Networks
Created two isolated VNets and connected them via peering.<br/>

### Network Configuration Summary
| Resource | Value | Location |
| :--- | :--- | :--- |
| **Virtual Network** | `EastUS-VNet` | East US |
| **Address Space** | `10.0.0.0/16` | East US |
| **Virtual Network** | `EastUS2-VNet` | East US 2 |
| **Address Space** | `10.1.0.0/16` | East US 2 |
| **Peering Type** | Bidirectional | N/A |
| **Peering Status** | Connected | N/A |
<br/>

### Task 2 — Virtual Machines, Load Balancer, Bastion, Firewall
Deployed 3 VMs with high availability, secure admin access, and social media blocking.<br/>

### Infrastructure Components
| Resource | Detail |
| :--- | :--- |
| **Web Servers** | `w1`, `w2` — 10.0.1.4, 10.0.1.5 — `Standard_B2ms` |
| **Backend Server** | `WS11` — 10.1.1.4 — `Standard_B2ms` |
| **Availability Set** | `WebAvailabilitySet` — 2 FD, 5 UD — 99.95% SLA |
| **Load Balancer** | `WebLoadBalancer` — Standard SKU (Ports 80, 443) |
| **Azure Bastion** | Standard — Browser RDP (No public IPs) |
| **Azure Firewall** | Web filtering (Social Media & Video streaming blocked) |
| **Route Table** | `RT-WS11-Firewall` — Next Hop: Azure Firewall |
<br/>

### Task 3 — NSGs and VPN Gateways
Secured both subnets and created an encrypted tunnel between regions.<br/>
### Security & Connectivity Configuration


| Resource | Detail |
| :--- | :--- |
| **NSG-EastUS** | Blocks direct RDP/SSH from Internet (web-subnet) |
| **NSG-EastUS2** | Blocks direct RDP/SSH + Allows SMB (Port 445) for S: drive |
| **VpnGateway-EastUS** | `VpnGw2AZ`, Gen2, BGP ASN: `65001` |
| **VpnGateway-EastUS2** | `VpnGw2AZ`, Gen2, BGP ASN: `65002` |
| **VPN Connections** | Dual connections (EastUS ↔ EastUS2) — **Connected** |
| **Encryption** | `AES-256 IPsec` — Shared Key: `AzureVpn@Proj2024!` |

<br/>

### Task 4 — Storage and S: Drive
Deployed resilient storage with three access methods and a file share mapped as S: drive on WS11.<br/>
### Storage & File Share Configuration


| Resource | Detail |
| :--- | :--- |
| **eastussuman023** | `Standard_LRS`, East US — HTTPS only, TLS 1.2 |
| **eastus2suman023** | `Standard_GRS`, East US 2 — Replicated to West US 2 |
| **Access Methods** | SAS Token (30 days), Access Keys, RBAC (Storage Blob Data Contributor) |
| **ws11-share** | 100 GB SMB Share — Mapped as `S:` on WS11 (`/persistent:yes`) |

<br/>

## Architecture Diagram

```
                        INTERNET
                           |
                    ┌──────┴──────┐
                    │Load Balancer│  ← Public IP
                    │ HTTP / HTTPS│
                    └──────┬──────┘
                           │
    ┌──────────────────────┼──────────────────────────┐
    │      EastUS-VNet   10.0.0.0/16   East US        │
    │                                                 │
    │  web-subnet  10.0.1.0/24   [NSG-EastUS]         │
    │  ┌─────────────┐   ┌─────────────┐              │
    │  │     w1      │   │     w2      │              │
    │  │  10.0.1.4   │   │  10.0.1.5   │              │
    │  │ Windows 2022│   │ Windows 2022│              │
    │  └─────────────┘   └─────────────┘              │
    │                                                 │
    │  AzureBastionSubnet  10.0.0.0/27                │
    │  ┌──────────────────────────────────┐           │
    │  │    Azure Bastion (Standard)      │ ← Browser RDP
    │  └──────────────────────────────────┘           │
    │                                                 │
    │  GatewaySubnet  10.0.2.0/24                     │
    │  ┌──────────────────────────────────┐           │
    │  │   VpnGateway-EastUS (VpnGw2AZ)   │           │
    │  │   BGP ASN: 65001                 │           │
    │  └────────────────┬─────────────────┘           │
    │                   │ IPsec AES-256               │
    └───────────────────┼─────────────────────────────┘
                        │  VNet Peering +
                        │  VPN Tunnel
    ┌───────────────────┼──────────────────────────────┐
    │      EastUS2-VNet   10.1.0.0/16   East US 2      │
    │                   │                              │
    │  ┌────────────────┴─────────────────┐            │
    │  │   VpnGateway-EastUS2 (VpnGw2AZ)  │            │
    │  │   BGP ASN: 65002                 │            │
    │  └──────────────────────────────────┘            │
    │                                                  │
    │  ws11-subnet  10.1.1.0/24   [NSG-EastUS2]        │
    │  Route: 0.0.0.0/0 → Firewall (RT-WS11-Firewall)  │
    │  ┌─────────────┐                                 │
    │  │    WS11     │                                 │
    │  │  10.1.1.4   │                                 │
    │  │ Windows 2022│                                 │
    │  └──────┬──────┘                                 │
    │         │  all outbound traffic                  │
    │         ▼                                        │
    │  AzureFirewallSubnet  10.1.3.0/24                │
    │  ┌──────────────────────────────────┐            │
    │  │    Azure Firewall (Standard)     │            │
    │  │    Blocks: Facebook, Instagram   │            │
    │  │    Twitter/X, TikTok, LinkedIn   │            │
    │  │    Reddit, YouTube               │            │
    │  │    Allows: all other web traffic │            │
    │  └──────────────────────────────────┘            │
    │                                                  │
    └──────────────────────────────────────────────────┘

STORAGE
┌─────────────────────────────────┐  ┌──────────────────────────────────────┐
│  eastussuman023  (East US)      │  │  eastus2suman023  (East US 2)        │
│  SKU: Standard_LRS              │  │  SKU: Standard_GRS                   │
│  3 copies - same data centre    │  │  Replicated to West US 2             │
│  Access: SAS + Keys + RBAC      │  │  File Share: ws11-share → S: drive   │
└─────────────────────────────────┘  └──────────────────────────────────────┘
```

---

## Repository Structure

```GitHub Repo Structure
azure-course-project/
    ├── task1-deployment.json + task1-parameters.json
    ├── task2-deployment.json + task2-parameters.json
    ├── task3-deployment.json + task3-parameters.json
    └── task4-deployment.json + task4-parameters.json
```

---

## Prerequisites

```bash
# 1. Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# 2. Login
az login

# 3. Check your subscription
az account show --query "{name:name, id:id}" -o table
```

---

## Deploy — Task by Task

### Setup

```bash
az login
az group create --name rg-azure-project --location eastus
```

### Task 1 — Virtual Networks and Peering

```bash
az deployment group create \
  --resource-group rg-azure-project \
  --template-file task1-deployment.json \
  --parameters @task1-parameters.json
```
### Task 2 — VMs, Load Balancer, Bastion, Firewall

```bash
az deployment group create \
  --resource-group rg-azure-project \
  --template-file task2-deployment.json \
  --parameters task2-parameters.json \
  adminPassword="YourP@ssw0rd123!"
```
### Task 3 — NSGs and VPN Gateways

> ⏱ **This step takes 30-45 minutes** — VPN Gateways are slow to provision.

```bash
az deployment group create \
  --resource-group rg-azure-project \
  --template-file task3-deployment.json \
  --parameters task3-parameters.json
```

### Task 4 — Storage, RBAC, and S: Drive

```bash
# Get your AAD Object ID first (needed for RBAC)
USER_OID=$(az ad signed-in-user show --query id -o tsv)

az deployment group create \
  --resource-group rg-azure-project \
  --template-file task4-deployment.json \
  --parameters task4-parameters.json \
  storageEastUSName=eastussuman023 \
  storageEastUS2Name=eastus2suman023 \
  userObjectId="$USER_OID"
```

**Map S: drive manually (if needed):**
```cmd
# Run on WS11 via Bastion (CMD as Administrator)
net use S: \\eastus2suman023.file.core.windows.net\ws11-share /user:Azure\eastus2suman023 "<key1>" /persistent:yes
```

**Get key from CLI:**
```bash
az storage account keys list -n eastus2suman023 -g rg-azure-project --query "[0].value" -o tsv
```

**Generate SAS Token:**
```bash
az storage account generate-sas \
  --account-name eastussuman023 \
  --account-key $(az storage account keys list -n eastussuman023 -g rg-azure-project --query "[0].value" -o tsv) \
  --resource-types co --services b \
  --permissions rwdlacup \
  --expiry $(date -u -d "+30 days" +%Y-%m-%dT%H:%MZ) \
  --https-only -o tsv
```

---

## Cleanup

```bash
az group delete --name rg-azure-project --yes --no-wait
```
