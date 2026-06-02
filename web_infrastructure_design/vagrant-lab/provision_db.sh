#!/bin/bash
# Provision Database Server (MySQL)
set -e

apt-get update
apt-get install -y mysql-server

# Secure MySQL installation (minimal for lab)
mysql -e "CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'holberton123';"
mysql -e "CREATE DATABASE IF NOT EXISTS holberton_db;"
mysql -e "GRANT ALL PRIVILEGES ON holberton_db.* TO 'appuser'@'%';"
mysql -e "FLUSH PRIVILEGES;"

# Bind to all interfaces (lab only, NOT production!)
sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

systemctl restart mysql
systemctl enable mysql

echo "MySQL configured. DB: holberton_db | User: appuser | Pass: holberton123"
