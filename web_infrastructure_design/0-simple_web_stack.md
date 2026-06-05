# 0. Simple Web Stack

![Simple Web Stack](./assets/0-simple_web_stack.png)

## Diagram Explanation

**The scenario:** A user types `www.foobar.com` in their browser.

**The request flow:**

1. **DNS** — The browser asks the DNS: "What is the IP of `www.foobar.com`?" → Answer: `8.8.8.8`
2. The HTTP request arrives on the **single server**
3. **Web Server (Nginx)** — Receives the request. If it is static files (HTML, CSS, images), it serves them directly
4. **Application Server** — If the request requires computation (e.g., generating a dynamic page), Nginx forwards it to the app server which executes the code
5. **Database (MySQL)** — If the application needs data, it queries the database
6. The response goes back up to the user

**Communication:** The server communicates with the user's computer via the **TCP/IP protocol** (HTTP on port 80).

---

### Component Definitions

- **A server** is a physical or virtual machine, usually located in a data center, that runs an OS.
- **The role of the domain** (`www.foobar.com`) is to provide a human-readable name that points to the server's IP via DNS.
- **`www.foobar.com` is an A record** because it resolves directly to an IP address (`8.8.8.8`).
- **The role of the web server (Nginx)** is to serve web pages and static content (HTML, CSS, images).
- **The role of the application server** is to compute dynamic content (execute business logic).
- **The role of the database (MySQL)** is to store the application's persistent data.
- **The code base** contains the application's files.
- **The server communicates** with the user's computer via the network (TCP/IP protocol).

---

## Issues

- 🔴 **SPOF (Single Point of Failure)** — A single server. If the machine goes down, the site is dead. No backup.
- 🔴 **Downtime during deployment** — When we deploy new code, we need to restart Nginx. The site is offline during this time.
- 🔴 **Impossible to scale** — If traffic increases, the server saturates. We cannot add capacity without rebuilding everything.
