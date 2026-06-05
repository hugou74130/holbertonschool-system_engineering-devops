# 1. Distributed Web Infrastructure

![Distributed Web Infrastructure](./assets/1-distributed_web_infrastructure.png)

## Diagram Explanation

**The scenario:** A user types `www.foobar.com` in their browser.

**The request flow:**

1. **DNS** — The browser asks the DNS: "What is the IP of `www.foobar.com`?" → Answer: Load Balancer's IP
2. The request arrives on the **Load Balancer (HAproxy)**
3. **HAproxy distributes** the request to one of the two servers according to the **Round Robin** algorithm
4. The **chosen server** processes the request: Nginx → App Server → MySQL
5. The response goes back up to the user

---

### Why We Add Each Element

| Element | Why We Add It |
|---------|---------------|
| **Load Balancer (HAproxy)** | Distribute traffic between the 2 servers to avoid overloading a single one |
| **2nd server** | Redundancy + double processing capacity |
| **Primary-Replica MySQL** | The Primary handles writes, the Replica handles reads = we can scale read queries |

---

### Technical Specifics

- **LB Algorithm: Round Robin** — Requests arrive one by one: request 1 → server 1, request 2 → server 2, request 3 → server 1, etc. It is simple and fair.

- **Active-Active vs Active-Passive:**
  - **Active-Active** (what we use here) → Both servers process requests **at the same time**. All power is used.
  - **Active-Passive** → One server works, the other waits in standby. If the first goes down, the second takes over. Less efficient but simpler.

- **MySQL Primary-Replica (Master-Slave):**
  - The **Primary** receives all write queries (INSERT, UPDATE, DELETE)
  - It writes these changes to a **binary log**
  - The **Replica** connects to the Primary, reads the binary log, and applies the same changes to its own copy of the data
  - It is **asynchronous** — the Replica may have a slight lag behind the Primary

- **Difference Primary vs Replica for the application:**
  - The **Primary** accepts **reads + writes**
  - The **Replica** accepts only **reads** (read-only)

---

## Issues

- 🔴 **The load balancer is a SPOF** — If it goes down, no more distribution = site dead
- 🔴 **No firewall** — The servers are exposed directly to the Internet
- 🔴 **No HTTPS** — Traffic is in clear text, interceptable by an attacker
- 🔴 **No monitoring** — We don't know if something is broken or slow
- 🔴 **Same components on each server** — If we want more DB power, we are forced to also add Nginx + App Server on the same machine, which is not optimal
