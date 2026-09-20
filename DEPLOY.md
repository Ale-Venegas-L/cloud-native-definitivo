# Deploy a EC2 con GitHub Actions + AWS Academy

## Requerimientos

| Requisito | Descripcion |
|-----------|-------------|
| Cuenta AWS Academy | Acceso a laboratorios temporales con credenciales |
| GitHub repository | Con acceso a secrets y branch `aws` |
| GitHub CLI (`gh`) | Opcional, para gestionar secrets desde terminal |
| Clave SSH | Generada localmente, la publica se sube a AWS |

## Secrets necesarios

Solo necesitas configurar **4 secrets**. Los valores de Cognito y API Gateway se generan automaticamente via Terraform.

### Secrets permanentes

| Secret | Descripcion | Como obtenerlo |
|--------|-------------|----------------|
| `SSH_PRIVATE_KEY` | Clave privada SSH completa | `cat ~/.ssh/classic-library-key` |
| `AWS_ACCESS_KEY_ID` | Credencial temporal del laboratorio | AWS Academy > AWS Details |
| `AWS_SECRET_ACCESS_KEY` | Credencial temporal del laboratorio | AWS Academy > AWS Details |
| `AWS_SESSION_TOKEN` | Token temporal del laboratorio | AWS Academy > AWS Details |

### Secrets que YA NO necesitas

Terraform crea automaticamente: Cognito User Pool, App Client, Domain, API Gateway, Lambda.
Los outputs se inyectan al EC2 durante el deploy.

---

## Flujo de trabajo con laboratorios AWS Academy

Cada vez que inicias un laboratorio, las credenciales AWS cambian. Debes actualizarlas **antes** de cada deploy.

### Opcion 1: GitHub CLI (recomendado)

```bash
gh secret set AWS_ACCESS_KEY_ID
# Pegar: ASIA...

gh secret set AWS_SECRET_ACCESS_KEY
# Pegar: wJalr...

gh secret set AWS_SESSION_TOKEN
# Pegar: FwoG...
```

### Opcion 2: Interfaz de GitHub

1. Repository > **Settings** > **Secrets and variables** > **Actions**
2. Editar cada secret y pegar el nuevo valor

### Opcion 3: Script automatizado

```bash
#!/bin/bash
# update-secrets.sh - Ejecutar al inicio de cada laboratorio
echo "Pega tu AWS_ACCESS_KEY_ID:"
read -s AWS_KEY && gh secret set AWS_ACCESS_KEY_ID <<< "$AWS_KEY"

echo "Pega tu AWS_SECRET_ACCESS_KEY:"
read -s AWS_SECRET && gh secret set AWS_SECRET_ACCESS_KEY <<< "$AWS_SECRET"

echo "Pega tu AWS_SESSION_TOKEN:"
read -s AWS_TOKEN && gh secret set AWS_SESSION_TOKEN <<< "$AWS_TOKEN"

echo "Secrets actualizados."
```

---

## Primer Setup (una sola vez)

### 1. Generar clave SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/classic-library-key -N "" -C "classic-library-deploy"
```

### 2. Configurar SSH_PRIVATE_KEY

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/classic-library-key
```

### 3. Configurar credenciales del primer laboratorio

```bash
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_SESSION_TOKEN
```

---

## Despliegue

### Deploy automatico

El workflow se ejecuta automaticamente al hacer push a `aws`:

```bash
git push origin aws
```

### Deploy manual

Ve a GitHub > Actions > Desplegar en EC2 > Run workflow

Selecciona una accion:
- `deploy`: Crear/actualizar infraestructura y desplegar
- `plan`: Solo planificar cambios (sin aplicar)
- `destroy`: Eliminar toda la infraestructura

---

## Outputs de Terraform

Despues del deploy, Terraform exporta:

| Output | Descripcion |
|--------|-------------|
| `public_ip` | IP publica de la EC2 |
| `cognito_user_pool_id` | ID del User Pool |
| `cognito_app_client_id` | ID del App Client |
| `cognito_domain` | Dominio del hosted UI |
| `api_gateway_url` | URL del API Gateway (prod) |
| `api_gateway_url_dev` | URL del API Gateway (dev) |

---

## Estructura de archivos

```
.github/workflows/deploy.yml    # Workflow de CI/CD
infra/
  main.tf                       # EC2 + Security Group + Key Pair
  cognito.tf                    # User Pool, App Client, Domain, Lambda trigger
  lambda.tf                     # Lambda Pre Token Generation + IAM
  api_gateway.tf                # REST API, Resources, Methods, CORS, Authorizer
  variables.tf                  # Variables de entrada
  outputs.tf                    # Outputs de Terraform
  user_data.sh                  # Script de setup de la instancia
  lambda/pre_token_generation.py # Codigo Lambda
backend/Dockerfile.prod
frontend/Dockerfile.prod
frontend/nginx.conf
docker-compose.prod.yml
```

---

## Arquitectura del Despliegue

```
GitHub Actions
    |
    |-- Job 1: Infrastructure (Terraform)
    |   |-- Crea EC2 + Security Group + Key Pair
    |   |-- Crea Cognito User Pool + App Client + Domain
    |   |-- Crea Lambda Pre Token Generation
    |   +-- Crea API Gateway REST + Resources + Authorizer
    |
    +-- Job 2: Deploy Application
        |-- Copia archivos al EC2 (SCP)
        |-- Configura .env (Cognito, MongoDB, IP)
        |-- Ejecuta docker-compose build + up
        +-- Health check (/api/v1/health)
```

---

## Variables de Terraform

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | Region AWS |
| `project_name` | `classic-library` | Nombre del proyecto |
| `instance_type` | `t2.micro` | Tipo de instancia EC2 |
| `admin_email` | `admin@example.com` | Email del admin Cognito |
| `admin_temp_password` | `Admin123!` | Password temporal del admin |
| `callback_urls` | `["http://localhost:5173/callback"]` | OAuth callbacks |
| `logout_urls` | `["http://localhost:5173/"]` | OAuth logout URLs |

---

## Troubleshooting

### Workflow falla en "Limpiar recursos AWS existentes"

- Las credenciales AWS Academy expiraron o el laboratorio termino
- Actualizar secrets con `gh secret set AWS_ACCESS_KEY_ID` etc.

### Workflow falla en Terraform Apply

- Verificar que `terraform validate` pase localmente
- Revisar si hay recursos huérfanos: `aws ec2 describe-instances --filters "Name=tag:Name,Values=classic-library-ec2"`

### Frontend no carga (pantalla blanca)

- Verificar que `VITE_API_URL` este embebido en el build
- SSH y revisar: `docker exec frontend grep -r 'api/v1' /usr/share/nginx/html/assets/`

### API no responde

- SSH y verificar contenedores: `docker ps`
- Verificar logs: `docker compose -f /app/docker-compose.prod.yml logs backend`
- Verificar MongoDB: `docker ps | grep mongodb`
