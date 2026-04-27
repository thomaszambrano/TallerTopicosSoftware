# Evidencias del Proyecto

Esta carpeta contiene las capturas de pantalla requeridas como evidencia del funcionamiento del proyecto.

## Capturas Requeridas

| Archivo | Contenido |
|---------|-----------|
| `01-swagger-ui.png` | Swagger UI en http://localhost:8000/docs |
| `02-docker-logs.png` | Logs de Docker con `docker-compose logs` |
| `03-docker-running.png` | Docker Desktop o `docker ps` mostrando el contenedor activo |
| `04-api-call-products.png` | Request GET a `/products` desde Postman/Insomnia |
| `05-api-call-chat.png` | Request POST a `/chat` con respuesta de la IA |
| `06-database.png` | Base de datos SQLite con productos cargados |

## Instrucciones para Generar las Evidencias

1. Iniciar la aplicación con Docker: `docker-compose up --build`
2. Abrir `http://localhost:8000/docs` para la evidencia de Swagger
3. Ejecutar `docker-compose logs` en la terminal para logs
4. Abrir Docker Desktop o ejecutar `docker ps` para el estado de contenedores
5. Usar Postman o Insomnia para los llamados a la API
6. Usar DB Browser for SQLite o VS Code SQLite Viewer para la base de datos
