import streamlit as st
import os
from task_manager import TaskManager

# Definir constantes
MENU_AGREGAR_TAREA = "Agregar Tarea"
MENU_LISTAR_TAREAS = "Listar Tareas"
MENU_COMPLETAR_TAREA = "Completar Tarea"
MENU_ELIMINAR_TAREA = "Eliminar Tarea"
MENU_ELIMINAR_TAREAS_COMPLETADAS = "Eliminar Tareas Completadas"
MENU_EXPORTAR_TAREAS = "Exportar Tareas"
MENU_IMPORTAR_TAREAS = "Importar Tareas"

def main():
    # Título de la página
    st.set_page_config(page_title="Gestor de Tareas", page_icon="📋", layout="centered")
    st.markdown("""
    <style>
    .css-ffhzg2 {
        padding-top: 10px;
        padding-bottom: 10px;
        background-color: #f4f4f4;
    }
    .css-1d391kg {
        background-color: #4CAF50;
    }
    .css-ffhzg2 h1 {
        font-size: 2.5rem;
        color: #333;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Gestor de Tareas 📝")
    
    menu = [
        MENU_AGREGAR_TAREA, 
        MENU_LISTAR_TAREAS, 
        MENU_COMPLETAR_TAREA, 
        MENU_ELIMINAR_TAREA, 
        MENU_ELIMINAR_TAREAS_COMPLETADAS, 
        MENU_EXPORTAR_TAREAS, 
        MENU_IMPORTAR_TAREAS
    ]
    choice = st.sidebar.selectbox("Menú", menu)

    if choice == MENU_AGREGAR_TAREA:
        agregar_tarea()

    elif choice == MENU_LISTAR_TAREAS:
        listar_tareas()

    elif choice == MENU_COMPLETAR_TAREA:
        completar_tarea()

    elif choice == MENU_ELIMINAR_TAREA:
        eliminar_tarea()

    elif choice == MENU_ELIMINAR_TAREAS_COMPLETADAS:
        eliminar_tareas_completadas()

    elif choice == MENU_EXPORTAR_TAREAS:
        exportar_tareas()

    elif choice == MENU_IMPORTAR_TAREAS:
        importar_tareas()

def agregar_tarea():
    st.subheader("Agregar Nueva Tarea")
    title = st.text_input("Título de la Tarea", placeholder="Escribe el título aquí")
    description = st.text_area("Descripción", placeholder="Escribe la descripción de la tarea aquí")
    
    if st.button("Agregar", key="add_task"):
        if TaskManager.add_task(title, description):
            st.success("Tarea agregada exitosamente", icon="✅")
        else:
            st.error("Error al agregar tarea", icon="❌")

def listar_tareas():
    st.subheader("Listado de Tareas")
    tasks = TaskManager.list_tasks()
    
    for task in tasks:
        task_status = "✅" if task.completed else "❌"
        st.markdown(f"**ID:** {task.id} | {task_status} **{task.title}** - {task.description}", unsafe_allow_html=True)

def completar_tarea():
    st.subheader("Completar Tarea")
    tasks = TaskManager.list_tasks()
    task_ids = [task.id for task in tasks if not task.completed]
    
    selected_task = st.selectbox("Seleccionar Tarea", task_ids)
    
    if st.button("Marcar como Completada"):
        if TaskManager.mark_task_complete(selected_task):
            st.success("Tarea completada", icon="✅")
        else:
            st.error("Error al completar tarea", icon="❌")

def eliminar_tarea():
    st.subheader("Eliminar Tarea Específica")
    tasks = TaskManager.list_tasks()
    task_ids = [task.id for task in tasks]
    
    selected_task = st.selectbox("Seleccionar Tarea a Eliminar", task_ids)
    
    if st.button("Eliminar Tarea"):
        if TaskManager.delete_task(selected_task):
            st.success("Tarea eliminada", icon="✅")
        else:
            st.error("Error al eliminar tarea", icon="❌")

def eliminar_tareas_completadas():
    if st.button("Eliminar Tareas Completadas"):
        if TaskManager.delete_completed_tasks():
            st.success("Tareas completadas eliminadas", icon="✅")
        else:
            st.error("Error al eliminar tareas", icon="❌")

def exportar_tareas():
    st.subheader("Exportar Tareas")
    filename = st.text_input("Nombre del archivo", "tareas_exportadas.json")
    
    if st.button("Exportar", key="export_tasks"):
        filepath = os.path.join('data', filename)
        if TaskManager.export_tasks(filepath):
            st.success(f"Tareas exportadas a {filepath}", icon="✅")
        else:
            st.error("Error al exportar tareas", icon="❌")

def importar_tareas():
    st.subheader("Importar Tareas")
    uploaded_file = st.file_uploader("Selecciona un archivo JSON", type=['json'])
    
    if uploaded_file is not None:
        filepath = os.path.join('data', uploaded_file.name)
        
        # Guardar archivo temporal
        with open(filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Importar"):
            if TaskManager.import_tasks(filepath):
                st.success("Tareas importadas exitosamente", icon="✅")
            else:
                st.error("Error al importar tareas", icon="❌")

if __name__ == "__main__":
    main()
