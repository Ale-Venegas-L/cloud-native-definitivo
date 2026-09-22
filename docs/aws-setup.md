# Guía de configuración AWS — Cognito + API Gateway

Pasos para configurar manualmente los servicios AWS requeridos por Classic Library.

---

## 1. AWS Cognito User Pool

### 1.1 Crear User Pool

1. Ir a **AWS Console → Amazon Cognito → User Pools → Create user pool**
2. Configurar:
   - **Pool name**: `classic-library-users`
   - **Devedn option**: Email
3. En **Configure sign-in experience**:
   - Habilitar: Email, Google (se configura después)
4. En **Configure security requirements**:
   - Contraseña: Mínimo 8 caracteres
   - MFA: Opcional (recomendado OFF para desarrollo)
5. En **Configure sign-up experience**:
   - Auto-confirmar usuarios: Deshabilitado
   - Habilitar attribute verification: Deshabilitado
6. En **Configure message delivery**:
   - Email: Send email with Cognito (para desarrollo)
7. En **Integrate your app**:
   - User pool name: `classic-library-users`
   - Initial app client: **Public client** (no client secret)
   - App client name: `classic-library-web`
   - Callback URL(s): `http://localhost:5173/callback`
   - Sign-out URL(s): `http://localhost:5173/`
   - Allowed OAuth flows: Authorization code grant
   - Allowed OAuth scopes: OpenID, Email, Profile
8. Crear el User Pool

### 1.2 Configurar Google como Identity Provider

1. Ir a **Google Cloud Console → APIs & Services → Credentials**
2. Crear OAuth 2.0 Client ID:
   - Application type: Web application
   - Authorized redirect URIs: `https://classic-library-users.auth.us-east-1.amazoncognito.com/oauth2/idpresponse`
3. Copiar **Client ID** y **Client Secret**
4. En Cognito → **Sign-in experience → Federation → Identity providers**
5. Agregar provider: Google
6. Pegar Client ID y Client Secret de Google
7. Associar Google provider con el User Pool

### 1.3 Crear custom attributes

1. En Cognito → **User pool properties → Custom attributes**
2. Agregar:
   - `admin` — Type: Number (0/1), Mutable: Yes
   - `permissions` — Type: String, Mutable: Yes
3. **Importante**: Los custom attributes solo se pueden crear al crear el User Pool. Si ya existe, crear uno nuevo con estos atributos.

### 1.4 Configurar Pre Token Generation Lambda

Esta Lambda inyecta los custom claims en el JWT.

1. Ir a **AWS Lambda → Create function**
   - Name: `cognito-pre-token-generation`
   - Runtime: Python 3.12
2. Pegar el siguiente código:

```python
import json
import os
import boto3

def lambda_handler(event, context):
    cognito = boto3.client('cognito-idp')
    
    user_attributes = event['request']['userAttributes']
    sub = user_attributes['sub']
    
    # Get custom attributes from Cognito
    try:
        user = cognito.admin_get_user(
            UserPoolId=os.environ['USER_POOL_ID'],
            Username=sub
        )
        
        custom_attrs = {
            attr['Name']: attr['Value']
            for attr in user.get('UserAttributes', [])
            if attr['Name'].startswith('custom:')
        }
        
        # Add custom claims to token
        claims_to_add = {}
        
        admin_value = custom_attrs.get('custom:admin', '0')
        claims_to_add['custom:admin'] = admin_value == '1' or admin_value.lower() == 'true'
        
        permissions = custom_attrs.get('custom:permissions', '')
        claims_to_add['custom:permissions'] = permissions
        
        event['response'] = {
            'claimsOverrideDetails': {
                'claimsToAddOrOverride': {
                    'custom:admin': str(claims_to_add['custom:admin']).lower(),
                    'custom:permissions': claims_to_add['custom:permissions']
                }
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        event['response'] = {'claimsOverrideDetails': {}}
    
    return event
```

3. Agregar variable de entorno: `USER_POOL_ID` = tu User Pool ID
4. Asignar permisos IAM a la Lambda:
   - `cognito-idp:AdminGetUser`
5. En Cognito → **User pool properties → Lambda triggers → Pre token generation**
6. Seleccionar la Lambda creada

### 1.5 Crear usuario de prueba

1. En Cognito → **Users → Create user**
   - Username: `admin@example.com`
   - Email: `admin@example.com`
   - Temporary password: `Admin123!`
2. Asignar custom attribute admin:
   ```bash
   aws cognito-admin update-user-attributes \
     --user-pool-id us-east-1_XXXXX \
     --username admin@example.com \
     --user-attributes Name=custom:admin,Value=true
   ```

### 1.6 Obtener valores para configuración

- **User Pool ID**: Cognito → User pool details → Pool ID
- **App Client ID**: Cognito → App clients → Client ID
- **Domain**: Cognito → Domain → Your domain prefix (ej: `classic-library`)

---

## 2. AWS API Gateway (REST API)

### 2.1 Crear REST API

1. Ir a **AWS Console → API Gateway → Create API**
2. Seleccionar **REST API** (no HTTP API)
3. Configurar:
   - Protocol: REST
   - Create new API: New API
   - API name: `classic-library-api`
   - Endpoint type: Regional

### 2.2 Crear Resources

Crear los siguientes resources (rutas):

```
/api
/api/v1
/api/v1/books
/api/v1/books/{id}
/api/v1/authors
/api/v1/authors/{id}
/api/v1/authors/{id}/books
/api/v1/auth
/api/v1/auth/me
/api/v1/health
```

Para cada resource:
1. Seleccionar el padre → Actions → Create Resource
2. Enable API Gateway CORS: Sí

### 2.3 Crear Methods

Para cada resource, crear los métodos correspondientes:

| Resource | Methods |
|---|---|
| `/api/v1/books` | GET, POST |
| `/api/v1/books/{id}` | GET, PUT, DELETE |
| `/api/v1/authors` | GET, POST |
| `/api/v1/authors/{id}` | GET, PUT, DELETE |
| `/api/v1/authors/{id}/books` | GET |
| `/api/v1/auth/me` | GET |
| `/api/v1/health` | GET |

Para cada method:
1. Seleccionar resource → Actions → Create Method
2. Integration type: HTTP Proxy
3. HTTP method: ANY
4. Endpoint URL: `http://localhost:8000` (para desarrollo local)
5. Use path override: `/api/v1/{proxy}`

**Nota**: Para producción, el endpoint URL será la URL del backend en ECS/EC2.

### 2.4 Configurar CORS

1. Seleccionar resource `/api/v1`
2. Actions → Enable CORS
3. Configurar:
   - Access-Control-Allow-Origin: `http://localhost:5173`
   - Access-Control-Allow-Headers: `Content-Type,Authorization`
   - Access-Control-Allow-Methods: `GET,POST,PUT,DELETE,OPTIONS`
4. Aplicar

### 2.5 Desplegar API

1. Actions → Deploy API
2. Deployment stage: [New Stage]
3. Stage name: `dev`
4. Deploy
5. Copiar la **Invoke URL** (ej: `https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev`)

### 2.6 Configurar JWT Authorizer

1. En API Gateway → **Authorization → Authorizers → Create New Authorizer**
2. Configurar:
   - Name: `CognitoAuthorizer`
   - Type: Cognito
   - Cognito User Pool: Seleccionar `classic-library-users`
   - Token Source: Authorization header
   - Token Validation: `Bearer `
3. Crear

### 2.7 Aplicar Authorizer a métodos protegidos

Para cada método POST, PUT, DELETE:
1. Seleccionar el method
2. Method Request → Authorization
3. Seleccionar `CognitoAuthorizer`
4. Save

Los métodos GET públicos (books, authors, health) no necesitan authorizer.

---

## 3. CORS en API Gateway

CORS se configura en dos niveles:

### 3.1 En API Gateway (ya configurado en 2.4)

API Gateway responde automáticamente a preflight OPTIONS requests.

### 3.2 En el backend (FastAPI)

El backend ya tiene CORS configurado en `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Cuando el backend esté en AWS, agregar el dominio de API Gateway a `allow_origins`:

```python
allow_origins=[
    settings.FRONTEND_URL,
    "http://127.0.0.1:5173",
    "https://xxxxxx.execute-api.us-east-1.amazonaws.com"
]
```

---

## 4. IAM Roles y Policies

### 4.1 Role para invocar el backend

1. Ir a **AWS IAM → Roles → Create role**
2. Trusted entity: AWS Service
3. Service: API Gateway
4. Attach policies:
   - `AmazonAPIGatewayInvokeFullAccess` (para desarrollo)
5. Role name: `api-gateway-invoke-backend`

### 4.2 Policy para Lambda Pre Token Generation

La Lambda necesita permisos para leer usuarios de Cognito:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "cognito-idp:AdminGetUser",
      "Resource": "arn:aws:cognito-idp:us-east-1:ACCOUNT_ID:userpool/USER_POOL_ID"
    }
  ]
}
```

---

## 5. Variables de entorno

### Backend (.env)

```env
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
COGNITO_APP_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Frontend (.env)

```env
VITE_COGNITO_DOMAIN=classic-library.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_REGION=us-east-1
```

---

## 6. Verificación

### 6.1 Probar login

1. Iniciar backend y frontend localmente
2. Ir a `http://localhost:5173/login`
3. Click "Iniciar sesión"
4. Redirige a Cognito Hosted UI
5. Login con Google
6. Redirige de vuelta a `/callback`
7. Token procesado, redirige a `/admin`

### 6.2 Probar API Gateway

```bash
# Sin token (debería funcionar para GET públicos)
curl https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/api/v1/books

# Con token (para POST)
curl -X POST https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/api/v1/books \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","author_id":"xxx","country":"Test","publication_year":2024,"genre":"Test"}'

# Sin token en ruta protegida (debería fallar 401)
curl -X POST https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/api/v1/books \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 6.3 Verificar JWT

Decodificar el token en https://jwt.io y verificar:
- `iss` = `https://cognito-idp.us-east-1.amazonaws.com/us-east-1_XXXXXXXXX`
- `aud` = tu App Client ID
- `custom:admin` = `true` o `false`
- `exp` > timestamp actual

---

## Troubleshooting

| Problema | Solución |
|---|---|
| CORS error en navegador | Verificar que API Gateway CORS esté habilitado y el backend tenga el origin correcto |
| 401 en API Gateway | Verificar que el JWT sea válido, no esté expirado, y el authorizer esté configurado |
| custom claims vacíos | Verificar que la Lambda Pre Token Generation esté configurada y funcionando |
| Login loop | Verificar que callback URL coincida exactamente en Cognito y en el frontend |
| Token no se renueva | Implementar refresh token flow (no implementado aún) |
