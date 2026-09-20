# Deploy a EC2 con GitHub Actions + AWS Academy

## Prerrequisitos

1. Cuenta de AWS Academy con acceso a laboratorios
2. GitHub repository con acceso a secrets
3. MongoDB Atlas (o MongoDB local)
4. Firebase项目 configurado

## Primer Setup

### 1. Generar clave SSH

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/classic-library-key -N "" -C "classic-library-deploy"
```

### 2. Configurar GitHub Secrets

Ve a tu repository > Settings > Secrets and variables > Actions

Agrega estos secrets:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | Credenciales AWS Academy | `ASIA...` |
| `AWS_SECRET_ACCESS_KEY` | Credenciales AWS Academy | `wJalr...` |
| `AWS_SESSION_TOKEN` | Token temporal AWS Academy | `FwoG...` |
| `SSH_PUBLIC_KEY` | Clave pública SSH | `ssh-rsa AAAA...` |
| `SSH_PRIVATE_KEY` | Clave privada SSH | `-----BEGIN OPENSSH...` |
| `VITE_FIREBASE_API_KEY` | Firebase API Key | `AIza...` |
| `VITE_FIREBASE_AUTH_DOMAIN` | Firebase Auth Domain | `project.firebaseapp.com` |
| `VITE_FIREBASE_PROJECT_ID` | Firebase Project ID | `my-project` |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase Storage Bucket | `project.appspot.com` |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase Sender ID | `123456789` |
| `VITE_FIREBASE_APP_ID` | Firebase App ID | `1:123:web:abc` |

### 3. Configurar credenciales AWS Academy

Cada vez que inicias un laboratorio:

1. Ve a **AWS Details** en tu laboratorio
2. Copia las credenciales `aws configure`
3. Actualiza los secrets en GitHub:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_SESSION_TOKEN`

```bash
# Usando GitHub CLI
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_SESSION_TOKEN
```

## Despliegue

### Deploy automático

El workflow se ejecuta automáticamente al hacer push a `main`:

```bash
git push origin main
```

### Deploy manual

Ve a GitHub > Actions > Deploy to EC2 > Run workflow

Selecciona una acción:
- `deploy`: Crear/actualizar infraestructura y desplegar
- `plan`: Solo planificar cambios (sin aplicar)
- `destroy`: Eliminar toda la infraestructura

## Estructura de archivos

```
├── .github/workflows/deploy.yml    # Workflow de CI/CD
├── infra/
│   ├── main.tf                     # Configuración principal Terraform
│   ├── variables.tf                # Variables de entrada
│   ├── outputs.tf                  # Outputs de Terraform
│   ├── user_data.sh                # Script de setup de la instancia
│   └── terraform.tfvars.example    # Ejemplo de variables
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
    │   └─→ Crea instancia EC2 en AWS
    │
    └─→ Job 2: Deploy Application
        ├─→ Copia archivos al EC2
        ├─→ Configura variables de entorno
        ├─→ Ejecuta docker-compose
        └─→ Health check
```

## Comandos Útiles

```bash
# Conectarse a la instancia
ssh -i ~/.ssh/classic-library-key.pem ec2-user@<IP>

# Ver logs en la instancia
docker-compose -f /app/docker-compose.prod.yml logs -f

# Reiniciar servicios
docker-compose -f /app/docker-compose.prod.yml restart

# Actualizar deploy
cd /app && docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### El workflow falla al crear infraestructura

- Verifica que las credenciales de AWS Academy sean válidas
- Asegúrate de que el laboratorio esté activo

### La aplicación no responde

- SSH a la instancia y verifica los contenedores:
  ```bash
  docker ps
  docker-compose -f /app/docker-compose.prod.yml logs
  ```

### Error de conexión a MongoDB

- Verifica que `MONGO_URI` sea correcto
- Asegúrate de que MongoDB Atlas permita conexiones desde la IP de EC2
