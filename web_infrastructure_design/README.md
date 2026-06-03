<div align="center">

# Web Infrastructure Design

*From a single server to a resilient, monitored, multi-tier architecture.*

</div>

<p align="center">
  <img src="https://img.shields.io/badge/Progress-100%25-success?style=for-the-badge" alt="Progress 100%">
  <img src="https://img.shields.io/badge/Whiteboarded-4%2F4-blue?style=for-the-badge" alt="Whiteboarded 4/4">
</p>

---

## Description

This project is a journey through modern web infrastructure design, entirely explored through whiteboarding and conceptual diagrams. Starting from a classic **LAMP stack** on a single machine, we incrementally build toward a fully distributed, secured, and monitored architecture.

Each task breaks down the *why* behind every component — because knowing how to draw the box is easy; explaining what happens when the box breaks is what separates a technician from an engineer.

> **No code to run here.** This repository is a collection of diagrams, explanations, and infrastructure narratives. Every architecture was drawn from memory and explained out loud during review.

---

## Learning Objectives

By the end of this project, you can confidently:

- **Whiteboard** a complete web stack from DNS resolution to database replication in under 30 minutes.
- **Explain** the role and interaction of every layer: web server, application server, load balancer, database, firewall, and monitoring agent.
- **Identify** Single Points of Failure (SPOF) and propose concrete redundancy strategies.
- **Defend** architectural choices regarding Active-Active vs Active-Passive, SSL termination, and separation of concerns.
- **Speak the language**: DNS A records, LAMP stack, HAproxy algorithms, Primary-Replica clustering, QPS, and horizontal scaling.

---

## Concepts & Technologies

| Layer | Component | Role |
|-------|-----------|------|
| **Edge** | DNS (A Record) | Resolves `www.foobar.com` to the public IP |
| **Edge** | HAproxy / Load Balancer | Distributes traffic, terminates SSL, ensures high availability |
| **Web** | Nginx | Serves static assets, reverse-proxies dynamic requests |
| **App** | Application Server | Executes business logic (e.g., Gunicorn) |
| **Data** | MySQL (Primary-Replica) | Persistent storage with read replicas for scaling |
| **Security** | Firewall (UFW) | Filters traffic at network boundaries |
| **Security** | SSL/TLS Certificate | Encrypts data in transit (HTTPS) |
| **Observability** | Monitoring Client | Collects metrics, logs, and alerts (e.g., Sumologic) |

---

## Requirements

- **OS**: Ubuntu 20.04 LTS
- **No executable code** — diagrams and explanations only
- A `README.md` at the root is mandatory
- Each task must include a whiteboarded diagram, screenshotted and linked in the answer file
- Reviews are conducted **live and unscripted**: no computer, no notes, just you and the marker

---

## Quick Start

```bash
git clone https://github.com/hugou74130/holbertonschool-system_engineering-devops.git
cd holbertonschool-system_engineering-devops/web_infrastructure_design
```

Browse any task file to see the diagram and its full technical breakdown:

```bash
cat 0-simple_web_stack.md
cat 1-distributed_web_infrastructure.md
cat 2-secured_and_monitored_web_infrastructure.md
cat 3-scale_up.md
```

---

## Project Structure

```
web_infrastructure_design/
├── README.md                                    # You are here
├── 0-simple_web_stack.md                        # Task 0: Single-server LAMP stack
├── 1-distributed_web_infrastructure.md          # Task 1: HAproxy + 2 servers + Primary-Replica DB
├── 2-secured_and_monitored_web_infrastructure.md # Task 2: Firewalls, HTTPS, monitoring agents
├── 3-scale_up.md                                # Task 3: Clustered LB, separated tiers
└── assets/
    ├── 0-simple_web_stack.png
    ├── 1-distributed_web_infrastructure.png
    ├── 2-secured_and_monitored_web_infrastructure.png
    └── 3-scale_up.png
```

---

## Task Overview

### Task 0 — Simple Web Stack
- **Status**: Mandatory
- **Focus**: Design a single-server infrastructure for `www.foobar.com` (A record → `8.8.8.8`).
- **Stack**: Nginx → App Server → MySQL on one machine.
- **Key takeaway**: Understand the request flow and spot the obvious weaknesses (SPOF, maintenance downtime, no scaling).

---

### Task 1 — Distributed Web Infrastructure
- **Status**: Mandatory
- **Focus**: Split the stack across three servers with a load balancer and a Primary-Replica database.
- **Key questions**: Round Robin vs leastconn? Active-Active vs Active-Passive? How does the Replica stay in sync?
- **Key takeaway**: Distribution removes some SPOFs but introduces new ones (load balancer, Primary DB). Security and monitoring are still missing.

---

### Task 2 — Secured and Monitored Web Infrastructure
- **Status**: Mandatory
- **Focus**: Harden the architecture with firewalls, SSL termination, and monitoring clients.
- **Key questions**: Why HTTPS? Why terminate SSL at the LB? How do you measure QPS?
- **Key takeaway**: Security and observability are not optional. Even with these additions, identical component stacking and a single writable DB node remain architectural debts.

---

### Task 3 — Scale Up
- **Status**: Advanced
- **Focus**: Evolve into a true 3-tier architecture with clustered load balancers and dedicated servers per role.
- **Key takeaway**: Separation of concerns is the foundation of horizontal scaling. Each tier can now be optimized, replaced, or scaled independently without affecting the others.

---

## Author

**Hugo** — *Student at Holberton School*

- Track: `holbertonschool-system_engineering-devops`
- Project: `web_infrastructure_design`
- GitHub: [@hugou74130](https://github.com/hugou74130)

> *"The best time to draw your architecture was before the outage. The second best time is now."*
