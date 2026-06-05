# 3. Scale Up

![Scale Up Infrastructure](./assets/3-scale_up.png)

## Diagram Explanation

**The scenario:** A user types `www.foobar.com` in their browser.

**The request flow:**

1. **DNS** — The browser asks the DNS: "What is the IP of `www.foobar.com`?" → Answer: Virtual IP of the Load Balancer Cluster
2. The request arrives on the **Load Balancer Cluster** (HAproxy 1 or HAproxy 2)
3. If HAproxy 1 goes down, HAproxy 2 takes over automatically (failover)
4. The LB distributes the request to a **Web Server** (Nginx only)
5. Nginx serves static files and reverse-proxies to an **App Server**
6. The App Server executes the business logic and queries the **MySQL Cluster** if needed
7. MySQL Primary handles writes, Replica handles reads
8. The response goes back up to the user

---

### Why We Add Each Element

| Element | Why We Add It |
|---------|---------------|
| **1 additional server** | More redundancy and capacity |
| **2nd Load Balancer (HAproxy)** | Configured in **cluster** with the first one. If one LB goes down, the other takes over automatically. |
| **Separation of components** | Each type of server does ONE THING only: web, application, or database |

---

### Technical Specifics

**Tier Separation:**

- **Web Servers only** — Nginx. Serve static assets and reverse-proxy to the app servers.
- **Application Servers only** — Execute business logic (Gunicorn, uWSGI, etc.).
- **Database Servers only** — MySQL Primary-Replica. Handle only data.

**Why separate:** Each component has different resource needs:
- The **DB** needs a lot of RAM and fast disk (SSD)
- The **web server** needs network bandwidth
- The **app server** needs CPU

By separating them, we can scale each tier independently according to its needs. Ex: if traffic increases but DB writes don't, we just add web servers.

**The LB in Active-Active Cluster:**
- Both load balancers are active simultaneously
- They share configuration and state
- If one goes down, the other continues to distribute traffic — **no more SPOF at the LB level**

---

## Evolution Recap

```
STEP 0: 1 all-in-one server
  ❌ SPOF | ❌ No scale | ❌ Deployment downtime

STEP 1: 3 servers + LB + DB Primary-Replica
  ✅ Server redundancy | ✅ Scale DB reads
  ❌ LB = SPOF | ❌ No security | ❌ No monitoring

STEP 2: + Firewalls + HTTPS + Monitoring
  ✅ Secured | ✅ Monitored | ✅ Encrypted
  ❌ SSL termination at LB | ❌ 1 single Master DB | ❌ Mixed components

STEP 3: LB Cluster + Separate Tiers
  ✅ No more LB SPOF | ✅ Independent scale per tier
```
