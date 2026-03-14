# BookMyShow — GCP Scalability Project

Scaling a BookMyShow ticketing app from a single VM to a production-ready GCP architecture.

**GCP Project:** `upgradlabs-1749732686213`
**Region:** `asia-south1` (Mumbai)
**Load Balancer IP:** `34.95.101.123`

---

## Architecture

```
Users
  |
  v
Global Load Balancer  (34.95.101.123)
  |
  |-- /api/*    --> Managed Instance Group (2-5 Flask VMs, auto-scaling)
  |                       |
  |                 Cloud SQL Primary  34.180.32.191  (writes)
  |                 Cloud SQL Replica  34.47.176.241  (reads)
  |
  |-- /static/* --> Cloud CDN --> Cloud Storage (HTML, CSS, JS)
  |
  v
Cloud Monitoring (3 alerts + live dashboard)
```

---

## Tasks

| Task   | What Was Done                                 | Key Resource                    |
| ------ | --------------------------------------------- | ------------------------------- |
| Task 1 | Baseline Flask VM + Locust load test          | `bms-monolith` — 35.200.237.254 |
| Task 2 | Managed Instance Group + Global Load Balancer | LB IP — 34.95.101.123           |
| Task 3 | Cloud SQL Primary + Read Replica              | Primary — 34.180.32.191         |
| Task 4 | Cloud CDN + Cloud Storage for static files    | `bms-static-backend`            |
| Task 5 | Load testing scaled architecture              | 20,062 requests, 0 failures     |
| Task 6 | Preemptible VMs + billing alerts              | 79% cost saving on batch        |
| Task 7 | Cloud Monitoring, alerts, dashboard           | 3 policies + BMS Dashboard      |

---

## Results

```
Metric               Before (Task 1)    After (Task 5)
-------------------  -----------------  ----------------
p95 latency          430 ms             180 ms  (54% faster)
Avg at 1000 users    265 ms             200 ms  (25% faster)
Failures             0%                 0%
VM failure recovery  100% outage        under 30 seconds
```

---

---

## Tech Stack

- **App:** Python Flask
- **Compute:** GCP Compute Engine (MIG, auto-scaling)
- **Database:** Cloud SQL MySQL 8.0 (Primary + Replica)
- **CDN:** Cloud CDN + Cloud Storage
- **Load Balancer:** Global HTTP Load Balancer
- **Load Testing:** Locust
- **Monitoring:** Cloud Monitoring, Cloud Logging
