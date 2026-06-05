# 2. Secured and Monitored Web Infrastructure

![Secured and Monitored Web Infrastructure](./assets/2-secured_and_monitored_web_infrastructure.png)

## Diagram Explanation

**The scenario:** A user types `www.foobar.com` in their browser.

**The request flow:**

1. **DNS** — The browser asks the DNS: "What is the IP of `www.foobar.com`?"
2. The request arrives in **HTTPS** (port 443) on the **Edge Firewall**
3. The Firewall filters malicious traffic and lets it pass through to the **Load Balancer**
4. **HAproxy** receives the request, terminates the SSL (decrypts HTTPS → HTTP)
5. The request passes through the **Firewalls** of the application servers
6. The **chosen server** processes the request: Nginx → App Server → MySQL
7. The **Monitoring Client** on each server collects metrics and sends them to the monitoring service
8. The response goes back up to the user

---

### Why We Add Each Element

| Element | Why We Add It |
|---------|---------------|
| **3 Firewalls** | One on each server to filter incoming/outgoing traffic. Blocks unauthorized access, limits open ports. |
| **SSL Certificate** | To serve `www.foobar.com` in **HTTPS**. Encrypts traffic between the browser and the server. |
| **3 Monitoring Clients** | Agents that collect logs and metrics on each server and send them to a monitoring system (e.g., Sumologic). |

---

### Technical Specifics

- **Why HTTPS:** If someone intercepts network traffic ("man in the middle" attack), the data is encrypted — they cannot read the content (passwords, personal data, etc.).

- **Monitoring — how it collects:**
  - The monitoring client runs on each server
  - It reads the **logs** (Nginx access logs, application errors)
  - It reads the **system metrics** (CPU, RAM, disk, network)
  - It sends all of this to a central dashboard where we can visualize and configure alerts

- **Monitoring QPS (Queries Per Second):**
  - Configure an alert that triggers if the number of requests per second exceeds a threshold
  - Example: "If QPS > 1000 for more than 5 minutes → send an email/Slack alert"

---

## Issues

- 🔴 **SSL termination at the load balancer** — The LB decrypts HTTPS, but traffic between the LB and the internal servers remains in HTTP (unencrypted). If someone has access to the internal network, they can read the data.
- 🔴 **A single MySQL Master** — If the Primary goes down, no one can write to the DB anymore. The application can no longer create/modify data.
- 🔴 **Same components on all servers** — We cannot scale independently. Ex: if we need more DB power, we are forced to also add Nginx + App Server on the same machine.
