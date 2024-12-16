# Gestor de Tareas con Python, Streamlit y SQLAlchemy

## Descripción del Proyecto

Esta es una aplicación de gestión de tareas desarrollada en Python utilizando Streamlit para la interfaz de usuario y SQLAlchemy para la persistencia de datos. La aplicación permite a los usuarios agregar, listar, completar y eliminar tareas, además de exportar e importar tareas desde archivos JSON.

## Características Principales

- 📝 Agregar nuevas tareas
- 📋 Listar todas las tareas
- ✅ Marcar tareas como completadas
- 🗑️ Eliminar tareas específicas
- 🗑️ Eliminar todas las tareas completadas
- 💾 Exportar tareas a un archivo JSON
- 📂 Importar tareas desde un archivo JSON

## Requisitos Previos

- Python 3.8 o superior
- pip
- venv (entorno virtual de Python)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Manvepa/gestionTareas
cd gestion-tareas
```

### 2. Crear y Activar Entorno Virtual

#### En Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
gestion_tareas/
│
├── venv/                 # Entorno virtual
├── src/                  # Código fuente
│   ├── __init__.py
│   ├── models.py          # Modelos de base de datos
│   ├── database.py        # Configuración de base de datos
│   ├── task_manager.py    # Lógica de gestión de tareas
│   └── app.py             # Interfaz de Streamlit
│
├── .scannerwork/         # SonarScanner
├── data/                 # Carpeta para almacenar datos
│   └── tasks.db           # Base de datos SQLite
├── test/                 # Carpeta para pruebas unitarias de la aplicación
│   └── test_task_manager.py  # Pruebas unitaria de la lógica de gestión de tareas
│
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación del proyecto
```

## Ejecución de la Aplicación

```bash
# Activar entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

# Ejecutar la aplicación
streamlit run src/app.py

# Ejecutar pruebas unitarias
pytest
```

## Uso de la Aplicación

1. **Agregar Tarea**: 
   - Selecciona "Agregar Tarea" en el menú
   - Introduce el título y descripción de la tarea
   - Haz clic en "Agregar"

2. **Listar Tareas**:
   - Selecciona "Listar Tareas"
   - Verás todas las tareas con su estado (✅ completada, ❌ pendiente)

3. **Completar Tarea**:
   - Selecciona "Completar Tarea"
   - Elige la tarea a completar
   - Haz clic en "Marcar como Completada"

4. **Eliminar Tarea**:
   - Selecciona "Eliminar Tarea"
   - Elige la tarea a eliminar
   - Haz clic en "Eliminar Tarea"

5. **Exportar Tareas**:
   - Selecciona "Exportar Tareas"
   - Introduce un nombre de archivo
   - Haz clic en "Exportar"

6. **Importar Tareas**:
   - Selecciona "Importar Tareas"
   - Sube un archivo JSON con tareas
   - Haz clic en "Importar"

## Tecnologías Utilizadas

- 🐍 Python
- 🌊 Streamlit
- 💾 SQLAlchemy
- 📦 SQLite
