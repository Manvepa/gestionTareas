from sqlalchemy.orm import sessionmaker
from database import get_session
from models import Task

class TaskManager:
    @staticmethod
    def add_task(title, description):
        try:
            # Obtener la sesión y realizar las operaciones en una transacción
            with next(get_session()) as session:
                new_task = Task(title=title, description=description, completed=False)
                session.add(new_task)
                session.commit()  # Commit una vez se agrega la tarea
                print(f"Tarea agregada con ID: {new_task.id}")  # Depuración
                return True
        except Exception as e:
            print(f"Error al agregar tarea: {e}")
            session.rollback()  # Si ocurre un error, hacer rollback
            return False
    
    @staticmethod
    def list_tasks(completed=None):
        try:
            with next(get_session()) as session:
                if completed is None:
                    return session.query(Task).all()
                return session.query(Task).filter(Task.completed == completed).all()
        except Exception as e:
            print(f"Error al listar tareas: {e}")
            return []


    @staticmethod
    def mark_task_complete(task_id):
        try:
            with next(get_session()) as session:
                task = session.query(Task).filter(Task.id == task_id).first()
                if task and not task.completed:
                    task.completed = True
                    session.commit()  # Confirmamos el cambio al marcar como completada
                    return True
                return False  # Si la tarea ya está completada o no existe
        except Exception as e:
            print(f"Error al marcar tarea como completada: {e}")
            return False

    @staticmethod
    def delete_task(task_id):
        try:
            with next(get_session()) as session:
                task = session.query(Task).filter(Task.id == task_id).first()
                if task:
                    session.delete(task)
                    session.commit()  # Confirmamos el cambio al eliminar la tarea
                    session.refresh(task)
                    print("Tareas completadas eliminadas.")  # Depuración
                    return True
                return False
        except Exception as e:
            print(f"Error al eliminar tarea: {e}")
            return False
    
    @staticmethod
    def delete_completed_tasks():
        try:
            with next(get_session()) as session:
                # Deleting completed tasks
                completed_tasks = session.query(Task).filter(Task.completed == True).all()
                for task in completed_tasks:
                    session.delete(task)  # Eliminamos cada tarea completada individualmente
                session.commit()  # Confirmamos los cambios
                print("Tareas completadas eliminadas.")  # Depuración
                return True
        except Exception as e:
            print(f"Error al eliminar tareas completadas: {e}")
            return False
