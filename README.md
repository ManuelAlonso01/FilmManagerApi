# FilmManagerApi



**FilmManagerApi** es la versión **API** del servicio original **[FilmManager](https://github.com/ManuelAlonso01/filmManager)**. Mientras que el primer repositorio era una aplicación web monolítica que utilizaba templates de Django para renderizar HTML, esta nueva versión desacopla totalmente el backend.

Se tomó la decisión estratégica de construir esta API para modernizar la arquitectura del sistema, permitiendo que el servidor sea agnóstico al cliente. Esto deja el proyecto abierto a futuras modificaciones o **implementaciones en el frontend** utilizando tecnologías como **React**, **Vue** o **aplicaciones móviles**, sin necesidad de alterar la lógica de negocio.

## 🎨 Frontend Incluido

Este proyecto incluye un **frontend completo** desarrollado con HTML, CSS y JavaScript vanilla que consume todos los endpoints de la API. Características principales:

- ✅ **Interfaz moderna y responsiva**
- ✅ **Autenticación completa** (login/registro)
- ✅ **Gestión automática de tokens JWT** con refresh automático
- ✅ **Gestión completa de películas/series** (CRUD)
- ✅ **Estadísticas detalladas** y visualización de datos
- ✅ **Servidor local incluido** para evitar problemas de CORS

### 🚀 Cómo usar el frontend

1. **Inicio rápido (recomendado):**
   ```bash
   python start.py
   ```
   Esto iniciará tanto la API como el frontend automáticamente.

2. **Inicio manual:**
   ```bash
   # Terminal 1 - API
   python manage.py runserver

   # Terminal 2 - Frontend
   cd frontend
   python server.py
   ```

3. **Abre tu navegador en:** `http://localhost:3000`

El frontend incluye documentación detallada en `frontend/README.md`.

## Stack Tecnológico Principal

* **Framework**: Django con Django REST Framework (DRF) para la construcción de los endpoints.

* **Autenticación**: SimpleJWT para el manejo de tokens de acceso seguros y sin estado (stateless).

* **Base de Datos**: SQLite (desarrollo) con una estructura de modelos heredada del proyecto original.

## Flujo para Usuarios Nuevos

Para comenzar a utilizar la API, un usuario debe seguir este proceso:

 * **Registro**: Enviar una petición POST al endpoint /register/ con un cuerpo JSON que contenga username y password.

Si el registro es exitoso, el sistema crea el usuario y devuelve inmediatamente un **par de tokens** (refresh y access).

* **Obtención de Token (Login)**: Si ya tienes una cuenta, puedes obtener tus tokens enviando tus credenciales vía POST al endpoint /token/.

Uso del Token y Acceso a Endpoints
La API utiliza JWT (JSON Web Tokens) para proteger sus recursos. Para acceder a los endpoints protegidos (como listar, subir o editar películas), debes incluir el token de acceso en la cabecera de cada petición.

**Cabecera Obligatoria: Authorization: Bearer <tu_access_token>**

## Endpoints Protegidos Disponibles

* **Listar Películas (GET /movie-list/)**: Devuelve un JSON con todas las películas cargadas por el usuario autenticado.

* **Subir Película (POST /subir/)**: Permite registrar una nueva obra enviando los datos requeridos (título, URL del póster, duración, descripción y calificación).

* **Editar Película (PATCH /movie-edit/<id_pelicula>/)**: Permite la actualización parcial de los datos de una película existente, siempre que el usuario sea el propietario del recurso.

* **Estadísticas (GET /resumen/)**: Genera un reporte detallado con métricas como tiempo total invertido, nota media y tops personalizados basándose en el historial del usuario.

## Mejoras Técnicas Implementadas
* **Seguridad de Acceso**: El sistema utiliza la clase IsAuthenticated de DRF para asegurar que ningún usuario pueda ver o modificar datos de otros.