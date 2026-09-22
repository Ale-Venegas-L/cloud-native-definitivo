# Deploy a EC2 con GitHub Actions + AWS Academy

## Requerimientos

| Requisito | Descripcion |
|-----------|-------------|
| Cuenta AWS Academy | Acceso a laboratorios temporales con credenciales |
| GitHub repository | Con acceso a secrets y branch `aws` |
| GitHub CLI (`gh`) | Opcional, para gestionar secrets desde terminal |
| Clave SSH | Generada localmente, la publica se sube a AWS |
| Cognito User Pool | Pre-creado en AWS Academy (ver seccion 1) |

---

## 1. Cognito User Pool (pre-creado)

El User Pool se crea manualmente en AWS Academy antes del primer deploy.

| Dato | Valor |
|------|-------|
| User Pool ID | `us-east-1_GPg9HQGJP` |
| App Client ID | `6e10hnmqf023ioa06qo72nejbd` |
| Domain prefix | `us-east-1gpg9hqgjp` |
| Callback URL | `https://d84l1y8p4kdic.cloudfront.net/callback` |
| Logout URL | `https://d84l1y8p4kdic.cloudfront.net/` |

### Callback URLs del App Client

Configurar en Cognito > User Pool > App clients > classic-library-users:
- **Allowed callback URLs**: `https://d84l1y8p4kdic.cloudfront.net/callback`
- **Allowed sign-out URLs**: `https://d84l1y8p4kdic.cloudfront.net/`

---

## 2. Secrets de GitHub

Necesitas configurar **7 secrets** en tu repositorio.

### Secrets permanentes

| Secret | Descripcion | Valor |
|--------|-------------|-------|
| `SSH_PRIVATE_KEY` | Clave privada SSH completa | `cat ~/.ssh/classic-library-key` |
| `AWS_ACCESS_KEY_ID` | Credencial temporal del laboratorio | AWS Academy > AWS Details |
| `AWS_SECRET_ACCESS_KEY` | Credencial temporal del laboratorio | AWS Academy > AWS Details |
| `AWS_SESSION_TOKEN` | Token temporal del laboratorio | AWS Academy > AWS Details |
| `COGNITO_USER_POOL_ID` | ID del User Pool existente | `us-east-1_GPg9HQGJP` |
| `COGNITO_APP_CLIENT_ID` | ID del App Client | `6e10hnmqf023ioa06qo72nejbd` |
| `COGNITO_DOMAIN` | Dominio del hosted UI | `us-east-1gpg9hqgjp` |

### Configurar secrets con GitHub CLI

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/classic-library-key
gh secret set AWS_ACCESS_KEY_ID        # pegar valor
gh secret set AWS_SECRET_ACCESS_KEY    # pegar valor
gh secret set AWS_SESSION_TOKEN        # pegar valor
gh secret set COGNITO_USER_POOL_ID <<< "us-east-1_GPg9HQGJP"
gh secret set COGNITO_APP_CLIENT_ID <<< "6e10hnmqf023ioa06qo72nejbd"
gh secret set COGNITO_DOMAIN <<< "us-east-1gpg9hqgjp"
```

---

## 3. Flujo de trabajo con laboratorios AWS Academy

Cada vez que inicias un laboratorio, las credenciales AWS cambian. Debes actualizarlas **antes** de cada deploy.

```bash
# Copiar credenciales desde AWS Academy > AWS Details
gh secret set AWS_ACCESS_KEY_ID
# Pegar: ASIA...

gh secret set AWS_SECRET_ACCESS_KEY
# Pegar: wJalr...

gh secret set AWS_SESSION_TOKEN
# Pegar: FwoG...
```

Los secrets de Cognito (`COGNITO_*`) NO cambian entre laboratorios.

---

## 4. Primer Setup (una sola vez)

### 4.1 Generar clave SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/classic-library-key -N "" -C "classic-library-deploy"
```

### 4.2 Configurar secrets

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/classic-library-key
gh secret set COGNITO_USER_POOL_ID <<< "us-east-1_GPg9HQGJP"
gh secret set COGNITO_APP_CLIENT_ID <<< "6e10hnmqf023ioa06qo72nejbd"
gh secret set COGNITO_DOMAIN <<< "us-east-1gpg9hqgjp"
```

### 4.3 Configurar credenciales del primer laboratorio

```bash
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_SESSION_TOKEN
```

---

## 5. Despliegue

### Deploy automatico

El workflow se ejecuta automaticamente al hacer push a `aws`:

```bash
git push origin aws
```

### Deploy manual

Ve a GitHub > Actions > Desplegar en EC2 > Run workflow

Selecciona una accion:
- `deploy`: Crear/actualizar infraestructura y desplegar
- `destroy`: Eliminar toda la infraestructura

---

## 6. Outputs de Terraform

Despues del deploy, Terraform exporta:

| Output | Descripcion |
|--------|-------------|
| `public_ip` | IP publica de la EC2 |
| `ssh_command` | Comando SSH para conectarse |
| `cognito_user_pool_id` | ID del User Pool |
| `cognito_app_client_id` | ID del App Client |
| `cognito_domain` | Dominio del hosted UI |
| `api_gateway_url` | URL del API Gateway (prod) |
| `api_gateway_url_dev` | URL del API Gateway (dev) |

---

## 7. Variables de Terraform

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | Region AWS |
| `project_name` | `classic-library` | Nombre del proyecto |
| `instance_type` | `t2.micro` | Tipo de instancia EC2 |
| `ami_id` | `ami-09179a962fadf762b` | AMI Amazon Linux 2023 |
| `enable_cognito` | `false` | Crear Cognito via Terraform (requiere permisos IAM) |
| `existing_cognito_user_pool_id` | `""` | User Pool ID existente |
| `existing_cognito_app_client_id` | `""` | App Client ID existente |
| `existing_cognito_domain` | `""` | Domain prefix del hosted UI |
| `callback_urls` | `[localhost, cloudfront]` | OAuth callback URLs |
| `logout_urls` | `[localhost, cloudfront]` | OAuth logout URLs |
| `admin_email` | `admin@example.com` | Email del admin Cognito |
| `admin_temp_password` | `Admin123!` | Password temporal del admin |

---

## 8. Estructura de archivos

```
.github/workflows/deploy.yml      # Workflow de CI/CD
infra/
  main.tf                         # EC2 + Security Group + Key Pair
  cognito.tf                      # User Pool, App Client, Domain (opcional)
  lambda.tf                       # Lambda Pre Token Generation + IAM (opcional)
  api_gateway.tf                  # REST API, Resources, Methods, CORS, Authorizer
  variables.tf                    # Variables de entrada
  outputs.tf                      # Outputs de Terraform
  user_data.sh                    # Script de setup de la instancia
  lambda/pre_token_generation.py  # Codigo Lambda
backend/Dockerfile.prod
frontend/Dockerfile.prod
frontend/nginx.conf
docker-compose.prod.yml
```

---

## 9. Arquitectura del Despliegue

```
GitHub Actions
    |
    |-- Job 1: Infrastructure (Terraform)
    |   |-- Crea EC2 + Security Group + Key Pair
    |   |-- Crea API Gateway REST + Resources + CORS + Authorizer
    |   +-- (Opcional) Crea Cognito + Lambda si enable_cognito=true
    |
    +-- Job 2: Deploy Application
        |-- Copia archivos al EC2 (SCP)
        |-- Configura .env (Cognito, MongoDB, IP)
        |-- Ejecuta docker-compose build + up
        +-- Health check (/api/v1/health)

EC2 Instance
    |-- Frontend (nginx:80) --> CloudFront (HTTPS)
    |-- Backend (uvicorn:8000) --> API Gateway --> Backend
    +-- MongoDB (27017)
```

---

## 10. Troubleshooting

### Workflow falla en "Limpiar recursos AWS existentes"

- Las credenciales AWS Academy expiraron o el laboratorio termino
- Actualizar secrets con `gh secret set AWS_ACCESS_KEY_ID` etc.

### InvalidKeyPair.Duplicate

El key pair ya existe de un deploy anterior. El workflow lo elimina automaticamente, pero si falla:
```bash
aws ec2 delete-key-pair --key-name classic-library-key
```

### InvalidGroup.Duplicate

El security group ya existe. El workflow lo elimina automaticamente, pero si falla:
```bash
# Buscar y terminar instancias que lo usan
aws ec2 describe-instances --filters "Name=key-name,Values=classic-library-key" --query "Reservations[].Instances[].InstanceId" --output text
aws ec2 terminate-instances --instance-ids <ID>
aws ec2 delete-security-group --group-name classic-library-sg
```

### Frontend no carga (pantalla blanca)

- Verificar que `VITE_API_URL` este embebido en el build
- SSH y revisar: `docker exec frontend grep -r 'api/v1' /usr/share/nginx/html/assets/`

### API no responde

- SSH y verificar contenedores: `docker ps`
- Verificar logs: `docker compose -f /app/docker-compose.prod.yml logs backend`
- Verificar MongoDB: `docker ps | grep mongodb`

### crypto.subtle is undefined

Este error ocurre cuando el frontend se sirve por HTTP (no HTTPS). El polyfill SHA-256 en `frontend/src/lib/cognito.ts` maneja este caso automaticamente.
