# Deploy a EC2 con GitHub Actions + AWS Academy

## Prerrequisitos

1. Cuenta de AWS Academy con acceso a laboratorios
2. GitHub repository con acceso a secrets

## Infraestructura自动izada (Terraform)

El workflow despliega automáticamente:

- **EC2**: Instancia Amazon Linux 2023 con Docker
- **Cognito**: User Pool, App Client, dominio hosted UI, Lambda Pre Token Generation
- **API Gateway**: REST API con CORS, authorizer Cognito, todas las rutas
- **Lambda**: Pre Token Generation para inyectar custom claims (admin, permissions)

## Primer Setup

### 1. Generar clave SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/classic-library-key -N "" -C "classic-library-deploy"
```

### 2. Configurar GitHub Secrets

Ve a tu repository > Settings > Secrets and variables > Actions

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | Credenciales AWS Academy | `ASIA...` |
| `AWS_SECRET_ACCESS_KEY` | Credenciales AWS Academy | `wJalr...` |
| `AWS_SESSION_TOKEN` | Token temporal AWS Academy | `FwoG...` |
| `SSH_PRIVATE_KEY` | Clave privada SSH | `-----BEGIN OPENSSH...` |

**Nota**: Los valores de Cognito (`VITE_COGNITO_*`) ya NO necesitan configurarse como secrets. Terraform los crea automáticamente y el workflow los injecta al deploy.

### 3. Configurar credenciales AWS Academy

Cada vez que inicias un laboratorio:

```bash
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_SESSION_TOKEN
```

## Despliegue

### Deploy automático

El workflow se ejecuta automáticamente al hacer push a `aws`:

```bash
git push origin aws
```

### Deploy manual

Ve a GitHub > Actions > Desplegar en EC2 > Run workflow

Selecciona una acción:
- `deploy`: Crear/actualizar infraestructura y desplegar
- `plan`: Solo planificar cambios (sin aplicar)
- `destroy`: Eliminar toda la infraestructura

## Outputs de Terraform

Después del deploy, Terraform exporta:

| Output | Descripción |
|--------|-------------|
| `public_ip` | IP pública de la EC2 |
| `cognito_user_pool_id` | ID del User Pool |
| `cognito_app_client_id` | ID del App Client |
| `cognito_domain` | Dominio del hosted UI |
| `api_gateway_url` | URL del API Gateway (prod) |
| `api_gateway_url_dev` | URL del API Gateway (dev) |

## Estructura de archivos

```
├── .github/workflows/deploy.yml    # Workflow de CI/CD
├── infra/
│   ├── main.tf                     # EC2 + Security Group + Key Pair
│   ├── cognito.tf                  # User Pool, App Client, Domain, Lambda trigger
│   ├── lambda.tf                   # Lambda Pre Token Generation + IAM
│   ├── api_gateway.tf              # REST API, Resources, Methods, CORS, Authorizer
│   ├── variables.tf                # Variables de entrada
│   ├── outputs.tf                  # Outputs de Terraform
│   ├── user_data.sh                # Script de setup de la instancia
│   ├── terraform.tfvars.example    # Ejemplo de variables
│   └── lambda/
│       └── pre_token_generation.py # Código Lambda
├── backend/
│   ├── Dockerfile.prod             # Dockerfile de producción
│   └── ...
├── frontend/
│   ├── Dockerfile.prod             # Dockerfile de producción
│   └── nginx.conf                  # Configuración Nginx
└── docker-compose.prod.yml         # Compose de producción
```

## Arquitectura del Despliegue

```
GitHub Actions
    │
    ├─→ Job 1: Infrastructure (Terraform)
    │   ├─→ Crea EC2 + Security Group + Key Pair
    │   ├─→ Crea Cognito User Pool + App Client + Domain
    │   ├─→ Crea Lambda Pre Token Generation
    │   └─→ Crea API Gateway REST + Resources + Authorizer
    │
    └─→ Job 2: Deploy Application
        ├─→ Copia archivos al EC2
        ├─→ Configura variables de entorno (Cognito, MongoDB)
        ├─→ Ejecuta docker-compose
        └─→ Health check
```

## API Gateway

El API Gateway expone la API en:

```
https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/api/v1
```

Rutas configuradas:

| Ruta | Métodos | Auth |
|------|---------|------|
| `/api/v1/books` | GET, POST, PUT, DELETE | NONE |
| `/api/v1/books/{id}` | GET, PUT, DELETE | NONE |
| `/api/v1/authors` | GET, POST, PUT, DELETE | NONE |
| `/api/v1/authors/{id}` | GET, PUT, DELETE | NONE |
| `/api/v1/authors/{id}/books` | GET | NONE |
| `/api/v1/auth/me` | GET | Cognito JWT |
| `/api/v1/health` | GET | NONE |

**Nota**: El authorizer Cognito está configurado en `auth/me`. Los métodos protegidos se pueden habilitar cambiando `authorization = "NONE"` a `authorization = "COGNITO_USER_POOLS"` en `infra/api_gateway.tf`.

## Cognito

- **Hosted UI**: `https://{domain}.auth.us-east-1.amazoncognito.com`
- **Login**: Email + password
- **Custom claims**: `custom:admin`, `custom:permissions`
- **Lambda**: Pre Token Generation inyecta claims en el JWT

### Google Identity Provider (manual)

Google IdP requiere configuración manual en Google Cloud Console:

1. Crear OAuth 2.0 Client ID en Google Cloud
2. Configurar Cognito como trusted provider
3. Asociar al User Pool

Ver `docs/aws-setup.md` para instrucciones detalladas.

## Comandos Útiles

```bash
# Conectarse a la instancia
ssh -i ~/.ssh/classic-library-key ec2-user@<IP>

# Ver logs en la instancia
docker compose -f /app/docker-compose.prod.yml logs -f

# Reiniciar servicios
docker compose -f /app/docker-compose.prod.yml restart
```

## Variables de Terraform

| Variable | Default | Descripción |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | Región AWS |
| `project_name` | `classic-library` | Nombre del proyecto |
| `instance_type` | `t2.micro` | Tipo de instancia EC2 |
| `admin_email` | `admin@example.com` | Email del admin |
| `admin_temp_password` | `Admin123!` | Password temporal del admin |
| `callback_urls` | `["http://localhost:5173/callback"]` | OAuth callbacks |
| `logout_urls` | `["http://localhost:5173/"]` | OAuth logout URLs |

## Troubleshooting

### El workflow falla al crear infraestructura

- Verifica que las credenciales de AWS Academy sean válidas
- Asegúrate de que el laboratorio esté activo

### La aplicación no responde

- SSH a la instancia y verifica los contenedores:
  ```bash
  docker ps
  docker compose -f /app/docker-compose.prod.yml logs
  ```

### Error de conexión a MongoDB

- MongoDB corre localmente en el EC2 dentro del contenedor `mongodb`
- Verifica que esté corriendo: `docker ps | grep mongodb`
- Reinicia si es necesario: `docker compose -f /app/docker-compose.prod.yml restart mongodb`

### API Gateway retorna 403

- Verificar que el JWT sea válido y no esté expirado
- Verificar que el authorizer esté configurado correctamente
