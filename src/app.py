import streamlit as st
import os
from task_manager import TaskManager

def main():
    st.title("Gestor de Tareas")
    
    menu = [
        "Agregar Tarea", 
        "Listar Tareas", 
        "Completar Tarea", 
        "Eliminar Tarea", 
        "Eliminar Tareas Completadas", 
        "Exportar Tareas", 
        "Importar Tareas"
    ]
    choice = st.sidebar.selectbox("Menú", menu)
    
    if choice == "Agregar Tarea":
        st.subheader("Agregar Nueva Tarea")
        title = st.text_input("Título de la Tarea")
        description = st.text_area("Descripción")
        
        if st.button("Agregar"):
            if TaskManager.add_task(title, description):
                st.success("Tarea agregada exitosamente")
            else:
                st.error("Error al agregar tarea")
    
    elif choice == "Listar Tareas":
        st.subheader("Listado de Tareas")
        tasks = TaskManager.list_tasks()
        
        for task in tasks:
            task_status = "✅" if task.completed else "❌"
            st.write(f"ID: {task.id} | {task_status} {task.title} - {task.description}")
    
    elif choice == "Completar Tarea":
        st.subheader("Completar Tarea")
        tasks = TaskManager.list_tasks()
        task_ids = [task.id for task in tasks if not task.completed]
        
        selected_task = st.selectbox("Seleccionar Tarea", task_ids)
        
        if st.button("Marcar como Completada"):
            if TaskManager.mark_task_complete(selected_task):
                st.success("Tarea completada")
            else:
                st.error("Error al completar tarea")
    
    elif choice == "Eliminar Tarea":
        st.subheader("Eliminar Tarea Específica")
        tasks = TaskManager.list_tasks()
        task_ids = [task.id for task in tasks]
        
        selected_task = st.selectbox("Seleccionar Tarea a Eliminar", task_ids)
        
        if st.button("Eliminar Tarea"):
            if TaskManager.delete_task(selected_task):
                st.success("Tarea eliminada")
            else:
                st.error("Error al eliminar tarea")
    
    elif choice == "Eliminar Tareas Completadas":
        if st.button("Eliminar Tareas Completadas"):
            if TaskManager.delete_completed_tasks():
                st.success("Tareas completadas eliminadas")
            else:
                st.error("Error al eliminar tareas")
    
    elif choice == "Exportar Tareas":
        st.subheader("Exportar Tareas")
        filename = st.text_input("Nombre del archivo", "tareas_exportadas.json")
        
        if st.button("Exportar"):
            filepath = os.path.join('data', filename)
            if TaskManager.export_tasks(filepath):
                st.success(f"Tareas exportadas a {filepath}")
            else:
                st.error("Error al exportar tareas")
    
    elif choice == "Importar Tareas":
        st.subheader("Importar Tareas")
        uploaded_file = st.file_uploader("Selecciona un archivo JSON", type=['json'])
        
        if uploaded_file is not None:
            filepath = os.path.join('data', uploaded_file.name)
            
            # Guardar archivo temporal
            with open(filepath, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            if st.button("Importar"):
                if TaskManager.import_tasks(filepath):
                    st.success("Tareas importadas exitosamente")
                else:
                    st.error("Error al importar tareas")

if __name__ == "__main__":
    main()