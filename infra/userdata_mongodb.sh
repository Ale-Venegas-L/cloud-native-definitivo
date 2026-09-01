#!/bin/bash
set -e

yum update -y
yum install -y mongodb-org

cat > /etc/mongod.conf << 'EOF'
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
storage:
  dbPath: /var/lib/mongo
net:
  port: ${mongodb_port}
  bindIp: 0.0.0.0
security:
  authorization: enabled
EOF

mkdir -p /var/log/mongodb
mkdir -p /var/lib/mongo
chown -R mongod:mongod /var/log/mongodb
chown -R mongod:mongod /var/lib/mongo

systemctl enable mongod
systemctl start mongod

echo "MongoDB started on port ${mongodb_port}"
