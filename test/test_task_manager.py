import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Task
from task_manager import TaskManager
import json
import os

@pytest.fixture(scope="module")
def db_session():
    # Usar SQLite en memoria para pruebas
    engine = create_engine('sqlite:///data/tasks.db', connect_args={'check_same_thread': False})
    print(f"Usando base de datos: {engine.url}")  # Depuración
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# Test de agregar tarea
def test_add_task(db_session):
    # Asegurarse de que las tareas sean visibles después del commit
    initial_count = db_session.query(Task).count()
    print(f"Cantidad inicial de tareas: {initial_count}")  # Depuración

    result = TaskManager.add_task("Test Task", "Test Description")

    # Asegurémonos de hacer commit después de agregar la tarea
    db_session.commit()  
    new_count = db_session.query(Task).count()
    assert result == True
    assert new_count == initial_count + 1  # Verifica que el número de tareas aumentó

# Test de listar tareas
def test_list_tasks(db_session):
    TaskManager.add_task("List Test", "List Description")
    tasks = TaskManager.list_tasks()
    assert len(tasks) > 0

# Test para marcar tarea como completada
def test_mark_task_complete(db_session):
    # Crear una tarea para marcar como completada
    TaskManager.add_task("Complete Test Task", "Test Description for completing")
    task = db_session.query(Task).filter(Task.title == "Complete Test Task").first()

    # Asegurarse de que la tarea no esté completada inicialmente
    assert task.completed == False
    
    # Marcar la tarea como completada
    result = TaskManager.mark_task_complete(task.id)
    db_session.commit()  # Realizamos commit para hacer efectivos los cambios
    
    # Recargar la tarea para verificar si se marcó correctamente como completada
    task = db_session.query(Task).filter(Task.id == task.id).first()
    assert result == True
    assert task.completed == True  # Verifica que la tarea esté completada

# # Test para eliminar tarea
# def test_delete_task(db_session):
#     # Crear una tarea para eliminar
#     TaskManager.add_task("Delete Test Task", "Test Description for deleting")
#     db_session.commit()  # Hacer commit para asegurarse de que la tarea se guarde en la base de datos
#     task = db_session.query(Task).filter(Task.title == "Delete Test Task").first()
#     print(f"Tarea agregada con ID: {task.id}")  # Imprimir ID para confirmar creación

#     # Verificar que la tarea existe antes de eliminarla
#     assert task is not None
#     print(f"Tarea a eliminar: {task.id}, Titulo: {task.title}")

#     # Eliminar la tarea
#     TaskManager.delete_task(task.id)
#     db_session.commit()  # Commit para hacer efectivos los cambios

#     # Verificar si la tarea fue eliminada consultando nuevamente
#     deleted_task = db_session.query(Task).filter(Task.id == task.id).first()
#     assert deleted_task is None  # La tarea ya no debería existir
#     print(f"Tarea con ID {task.id} eliminada")


# def test_delete_completed_tasks(db_session):
#     # Crear tareas, algunas completadas y otras no
#     TaskManager.add_task("Delete Completed Test Task 1", "Description")
#     TaskManager.add_task("Delete Completed Test Task 2", "Description")
#     db_session.commit()  # Hacer commit para asegurarse de que las tareas se guarden en la base de datos
#     task1 = db_session.query(Task).filter(Task.title == "Delete Completed Test Task 1").first()
#     task2 = db_session.query(Task).filter(Task.title == "Delete Completed Test Task 2").first()

#     # Verificar que ambas tareas fueron creadas correctamente
#     print(f"Tareas creadas. Task 1 ID: {task1.id}, Task 2 ID: {task2.id}")

#     # Marcar una tarea como completada
#     TaskManager.mark_task_complete(task1.id)
#     db_session.commit()  # Commit para hacer efectivos los cambios
#     print(f"Tarea 1 completada: {task1.id}, Titulo: {task1.title}")

#     # Asegurarnos que la tarea 1 está completada y la tarea 2 no
#     assert task1.completed == True
#     assert task2.completed == False

#     # Eliminar tareas completadas
#     result = TaskManager.delete_completed_tasks()
#     db_session.commit()  # Commit para hacer efectivos los cambios
#     print(f"Tareas completadas eliminadas.")

#     # Verificar que la tarea completada ha sido eliminada
#     task1_deleted = db_session.query(Task).filter(Task.id == task1.id).first()
#     assert task1_deleted is None  # La tarea completada debería ser eliminada
#     print(f"Tarea completada con ID {task1.id} eliminada.")


# Test para exportar tareas
def test_export_tasks(db_session):
    # Crear tareas para exportar
    TaskManager.add_task("Export Test Task 1", "Description 1")
    TaskManager.add_task("Export Test Task 2", "Description 2")
    
    # Exportar las tareas a un archivo JSON
    tasks = TaskManager.list_tasks()
    tasks_data = [{"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for task in tasks]
    export_file_path = 'data/exported_tasks.json'
    
    with open(export_file_path, 'w') as f:
        json.dump(tasks_data, f, indent=4)
    
    # Verificar que el archivo fue creado y contiene datos
    assert os.path.exists(export_file_path) == True
    with open(export_file_path, 'r') as f:
        exported_data = json.load(f)
        assert len(exported_data) > 0  # Verificar que hay tareas exportadas

# Test para importar tareas
def test_import_tasks(db_session):
    # Preparar un archivo JSON con tareas para importar
    tasks_data = [
        {"id": 1, "title": "Imported Task 1", "description": "Description 1", "completed": False},
        {"id": 2, "title": "Imported Task 2", "description": "Description 2", "completed": True}
    ]
    import_file_path = 'data/imported_tasks.json'
    
    with open(import_file_path, 'w') as f:
        json.dump(tasks_data, f, indent=4)

    # Simular la importación de tareas desde el archivo
    with open(import_file_path, 'r') as f:
        imported_tasks = json.load(f)
        for task_data in imported_tasks:
            TaskManager.add_task(task_data['title'], task_data['description'])
    
    # Verificar que las tareas han sido importadas
    tasks = db_session.query(Task).filter(Task.title.like("Imported Task%")).all()
    assert len(tasks) == 2
    assert tasks[0].title == "Imported Task 1"
    assert tasks[1].title == "Imported Task 2"
