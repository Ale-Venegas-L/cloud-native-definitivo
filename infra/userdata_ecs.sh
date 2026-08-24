#!/bin/bash
set -e

yum update -y
yum install -y aws-cli

cat > /etc/ecs/ecs.config << EOF
ECS_CLUSTER=${cluster_name}
ECS_BACKEND_TASK_CONTAINER=backend
ECS_FRONTEND_TASK_CONTAINER=frontend
EOF

echo "ECS agent configured for cluster: ${cluster_name}"
