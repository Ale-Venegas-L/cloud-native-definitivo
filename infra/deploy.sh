#!/bin/bash
set -e

echo "=== Classic Library - AWS Deployment ==="
echo ""

# Verificar herramientas
echo "Verificando herramientas..."
command -v terraform >/dev/null 2>&1 || { echo "Error: terraform no esta instalado"; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "Error: aws cli no esta instalado"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Error: docker no esta instalado"; exit 1; }
echo "✓ Todas las herramientas disponibles"
echo ""

# Configurar AWS
echo "Configurando AWS..."
aws configure
echo ""

# Inicializar Terraform
echo "Inicializando Terraform..."
cd terraform
terraform init
echo ""

# Plan de ejecucion
echo "Generando plan de ejecucion..."
terraform plan -out=tfplan
echo ""

# Preguntar si continuar
read -p "¿Desea aplicar los cambios? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Aplicando cambios..."
    terraform apply tfplan
    
    # Obtener informacion
    echo ""
    echo "=== Informacion del despliegue ==="
    MONGODB_IP=$(terraform output -raw mongodb_private_ip)
    ALB_DNS=$(terraform output -raw alb_dns_name)
    
    echo "MongoDB IP: $MONGODB_IP"
    echo "ALB DNS: $ALB_DNS"
    echo ""
    
    # Construir y subir imagenes
    echo "Construyendo imagenes Docker..."
    
    # Backend
    echo "Construyendo backend..."
    docker build -t classic-library-backend:latest -f ../backend/Dockerfile ../backend
    
    # Frontend
    echo "Construyendo frontend..."
    cd ../frontend
    docker build -t classic-library-frontend:latest -f ../terraform/docker/frontend.Dockerfile .
    cd ../terraform
    
    # Login a ECR
    echo "Iniciando sesion en ECR..."
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com
    
    # Tags
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ECR_BACKEND="$ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/classic-library-backend"
    ECR_FRONTEND="$ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/classic-library-frontend"
    
    docker tag classic-library-backend:latest $ECR_BACKEND:latest
    docker tag classic-library-frontend:latest $ECR_FRONTEND:latest
    
    # Push
    echo "Subiendo imagenes a ECR..."
    docker push $ECR_BACKEND:latest
    docker push $ECR_FRONTEND:latest
    
    echo ""
    echo "=== Despliegue completado ==="
    echo "Frontend: http://$ALB_DNS"
    echo "Backend API: http://$ALB_DNS/api"
    echo "Swagger: http://$ALB_DNS/api/docs"
else
    echo "Despliegue cancelado"
fi
