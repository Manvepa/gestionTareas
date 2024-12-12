import json
from database import session
from models import Task

class TaskManager:
    @staticmethod
    def add_task(title, description):
        try:
            new_task = Task(title=title, description=description)
            session.add(new_task)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al agregar tarea: {e}")
            return False
    
    @staticmethod
    def list_tasks():
        return session.query(Task).all()
    
    @staticmethod
    def mark_task_complete(task_id):
        try:
            task = session.query(Task).get(task_id)
            if task:
                task.completed = True
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error al marcar tarea: {e}")
            return False
    
    @staticmethod
    def delete_task(task_id):
        try:
            task = session.query(Task).get(task_id)
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar tarea: {e}")
            return False
    
    @staticmethod
    def delete_completed_tasks():
        try:
            session.query(Task).filter(Task.completed == True).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar tareas: {e}")
            return False
    
    @staticmethod
    def export_tasks(filename):
        try:
            tasks = session.query(Task).all()
            task_list = [
                {
                    "title": task.title, 
                    "description": task.description, 
                    "completed": task.completed
                } for task in tasks
            ]
            
            with open(filename, 'w') as f:
                json.dump(task_list, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al exportar tareas: {e}")
            return False
    
    @staticmethod
    def import_tasks(filename):
        try:
            with open(filename, 'r') as f:
                task_list = json.load(f)
            
            # Limpiar tareas existentes
            session.query(Task).delete()
            
            # Importar nuevas tareas
            for task_data in task_list:
                new_task = Task(
                    title=task_data['title'], 
                    description=task_data['description'], 
                    completed=task_data['completed']
                )
                session.add(new_task)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al importar tareas: {e}")
            return False