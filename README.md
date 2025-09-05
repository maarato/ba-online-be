# Business Analyst Backend API

Backend API para el chatbot Business Analyst con integración de LLMs usando LangChain.

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido
- **LangChain**: Integración con múltiples LLMs
- **Groq & OpenAI**: Soporte para ambos proveedores
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **CORS**: Configurado para frontend NextJS

## 🛠️ Tecnologías

- **Python 3.8+**
- **FastAPI** - Framework web
- **LangChain** - Integración con LLMs
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **SQLite/PostgreSQL** - Base de datos

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd ba-backend
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias:**

**Opción 1 - Instalación simple (recomendada):**
```bash
pip install -r requirements-simple.txt
```

**Opción 2 - Instalación robusta (si hay conflictos):**
```bash
# Windows
install-clean.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

**Opción 3 - Corrección rápida de importaciones:**
```bash
# Si hay errores de importación
fix_imports.bat
```

**Opción 4 - Instalación manual:**
```bash
pip install fastapi uvicorn python-multipart pydantic pydantic-settings python-dotenv sqlalchemy structlog
pip install langchain langchain-community langchain-groq langchain-openai
pip install httpx alembic
```

4. **Configurar variables de entorno:**
```bash
cp env.example .env
```

Edita `.env` con tu configuración:
```env
# LLM Configuration
GROQ_API_KEY=tu_groq_api_key
OPENAI_API_KEY=tu_openai_api_key
DEFAULT_LLM_PROVIDER=groq

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Ejecutar el servidor:**
```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

## 🔌 Endpoints de la API

### Autenticación
- `POST /auth/device/init` - Inicializar dispositivo

### Chat
- `POST /chat/stream` - Procesar mensaje del chat

### Briefs
- `POST /brief/save` - Guardar brief del proyecto
- `GET /brief/{brief_id}` - Obtener brief por ID

### Leads
- `POST /leads/create` - Crear lead
- `GET /leads/{lead_id}` - Obtener lead por ID

## 🤖 Configuración de LLMs

### Groq
1. Obtén tu API key en [Groq Console](https://console.groq.com/)
2. Configura `GROQ_API_KEY` en `.env`
3. Establece `DEFAULT_LLM_PROVIDER=groq`

### OpenAI
1. Obtén tu API key en [OpenAI Platform](https://platform.openai.com/)
2. Configura `OPENAI_API_KEY` en `.env`
3. Establece `DEFAULT_LLM_PROVIDER=openai`

## 🏗️ Estructura del Proyecto

```
ba-backend/
├── app/
│   ├── api/                 # Endpoints de la API
│   │   ├── auth.py         # Autenticación
│   │   ├── chat.py         # Chat con LLM
│   │   ├── brief.py        # Gestión de briefs
│   │   └── leads.py        # Gestión de leads
│   ├── core/               # Configuración central
│   │   ├── config.py       # Configuración
│   │   ├── database.py     # Base de datos
│   │   └── logging.py      # Logging
│   ├── models/             # Modelos de base de datos
│   │   ├── brief.py        # Modelo de brief
│   │   ├── chat.py         # Modelo de chat
│   │   └── lead.py         # Modelo de lead
│   ├── schemas/            # Esquemas Pydantic
│   │   ├── brief.py        # Esquemas de brief
│   │   ├── chat.py         # Esquemas de chat
│   │   └── lead.py         # Esquemas de lead
│   └── services/           # Servicios de negocio
│       └── llm_service.py  # Servicio de LLM
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── README.md              # Documentación
```

## 🔧 Desarrollo

### Ejecutar en modo desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Documentación de la API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Logs
Los logs se generan en formato JSON estructurado usando `structlog`.

## 🚀 Despliegue

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Entorno de Producción
```env
DEBUG=false
DATABASE_URL=postgresql://user:password@localhost/business_analyst
SECRET_KEY=your-production-secret-key
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📝 Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `GROQ_API_KEY` | API key de Groq | - |
| `OPENAI_API_KEY` | API key de OpenAI | - |
| `DEFAULT_LLM_PROVIDER` | Proveedor por defecto | `groq` |
| `DATABASE_URL` | URL de base de datos | `sqlite:///./business_analyst.db` |
| `ALLOWED_ORIGINS` | URLs permitidas para CORS | `http://localhost:3000` |

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
