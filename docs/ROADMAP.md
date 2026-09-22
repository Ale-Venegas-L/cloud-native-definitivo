# Hoja de ruta de entrega - Classic Library

## Hito 1 - Fundación segura e identidad

Estado: en progreso

- [x] Introducir el contrato `/api/v1`.
- [x] Agregar el límite de autenticación modular de FastAPI.
- [x] Proteger todas las operaciones de escritura con el rol admin.
- [x] Agregar estado de sesión de Vue, guards de rutas y cliente API autenticado.
- [x] Agregar pruebas base de autorización.
- [x] Migrar de Firebase Authentication a AWS Cognito (ADR-002).
- [x] Implementar flujo OAuth 2.0 Authorization Code + PKCE.
- [x] Verificación JWT en backend vía endpoint JWKS de Cognito.
- [x] Lambda de Pre Token Generation para claims personalizados.
- [ ] Configurar Cognito User Pool y App Client en AWS Console.
- [ ] Configurar API Gateway REST API con JWT Authorizer.
- [ ] Completar prueba de smoke de login real en navegador con Cognito.

## Hito 1.5 - Experiencia de interfaz

Estado: completo

- [x] Consolidar el sistema de diseño editorial y espaciado responsivo.
- [x] Agregar navegación pública y administrativa responsiva.
- [x] Agregar estados de carga, error, vacío y reintento.
- [x] Rediseñar vistas de inicio, catálogo, autenticación y autorización.
- [x] Agregar portadas reales, fallbacks, filtros, ordenamiento y detalles de libro.
- [x] Agregar panel operacional responsivo y tarjetas CRUD móvil.
- [x] Agregar confirmación de acciones destructivas y formularios de contenido completos.
- [x] Agregar controles de tema claro/oscuro persistentes y mejoras de accesibilidad.
- [x] Optimizar e integrar el hero de inicio como WebP.

## Hito 2 - Integridad del dominio

- Validar identificadores de MongoDB sin devolver errores 500.
- Forzar relaciones libro-autor.
- Definir política de eliminación de autores.
- Deshabilitar fallback de base de datos en memoria fuera de tests y desarrollo local explícito.
- Agregar índices, paginación y respuestas de error consistentes.

## Hito 3 - Calidad y delivery

- Agregar tests de componentes y rutas del frontend.
- Expandir cobertura de unit tests e integración del backend.
- Agregar linting, type checking y gates de seguridad CI.
- Producir imágenes de contenedor de producción y checks de salud/disponibilidad.

## Hito 4 - AWS API Gateway

Estado: en progreso

- [x] Seleccionar REST API más JWT Authorizer vía ADR-002.
- [x] Migrar proveedor de identidad de Firebase a Cognito.
- [ ] Crear API Gateway REST API con proxy integration.
- [ ] Configurar CORS en API Gateway.
- [ ] Configurar rol IAM para invocación API Gateway → Backend.
- [ ] Validar issuer, audience, firma y expiración de Cognito en el edge.
- [ ] Agregar throttling, validación de requests, logs y métricas.
- [ ] Agregar WAF usando la arquitectura seleccionada en el ADR.
