#!/bin/bash
# Provision Load Balancer (HAproxy)
set -e

apt-get update
apt-get install -y haproxy

# Configure HAproxy with Round Robin to web1 and web2
cat > /etc/haproxy/haproxy.cfg << 'EOF'
global
    log /dev/log    local0
    log /dev/log    local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server web1 192.168.56.11:80 check
    server web2 192.168.56.12:80 check
EOF

systemctl restart haproxy
systemctl enable haproxy

echo "HAproxy configured. Access http://192.168.56.10 to test Round Robin."
