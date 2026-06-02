# 1. Distributed Web Infrastructure

## Infrastructure Diagram

![Distributed Web Infrastructure](./assets/1-distributed_web_infrastructure.png)

## Why Each Additional Element Was Added

1. **Load Balancer (HAproxy)**
   - Distributes incoming traffic across multiple servers to prevent any single server from being overwhelmed.
   - Provides a single entry point, masking the backend server topology from users.

2. **Second Server**
   - Eliminates the single point of failure at the application layer.
   - Allows horizontal scaling and redundancy. If one server fails, the other continues to serve traffic.

3. **Primary-Replica Database Cluster**
   - The **Primary (Master)** handles all write operations (INSERT, UPDATE, DELETE).
   - The **Replica (Slave)** handles read operations (SELECT), offloading read traffic from the Primary.
   - Provides data redundancy and failover capability for the database.

## Specifics

- **What distribution algorithm is the load balancer configured with, and how does it work?**
  HAproxy is configured with the **Round Robin** algorithm. It distributes requests sequentially to each server in the pool. When a request arrives, it goes to Server 1, the next to Server 2, the next back to Server 1, and so on. This ensures an even distribution of load across all healthy backend servers.

- **Is the load balancer enabling an Active-Active or Active-Passive setup?**
  This setup is **Active-Active**. Both servers are actively receiving and processing requests simultaneously. In an **Active-Passive** setup, one server handles all traffic while the other remains on standby, only taking over if the active server fails.

- **How does a Primary-Replica (Master-Slave) cluster work?**
  The Primary node receives all write queries and logs them to a binary log. The Replica node connects to the Primary and reads the binary log, applying the same changes to its own copy of the data asynchronously. The application writes to the Primary and reads from the Replica, splitting the load.

- **What is the difference between the Primary and Replica nodes regarding the application?**
  The application sends **all write queries** to the Primary node. It sends **read queries** to the Replica node. If the application were to send writes to the Replica, data inconsistency would occur because the Replica is read-only by design.

## Issues with this Infrastructure

1. **Where are SPOFs?**
   - The **Load Balancer** is a SPOF. If HAproxy fails, no traffic can reach any server.
   - The **Primary database node** is a SPOF. If it fails, write operations stop entirely until a failover occurs.

2. **Security issues**
   - **No firewalls**: Servers and database are exposed to the public internet. Any open port is a potential attack vector.
   - **No HTTPS**: Traffic between the user and the load balancer travels unencrypted. Passwords, session tokens, and sensitive data can be intercepted.

3. **No monitoring**
   - There is no visibility into server health, traffic patterns, or performance metrics. You cannot detect failures, bottlenecks, or attacks proactively. Problems are only discovered when users report them.
