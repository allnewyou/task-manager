from flask import jsonify, request
from .models import db, Task

def register_routes(app):
    """
    Регистрируем все API маршруты в приложении Flask
    """

    # GET /api/tasks - Получить все задачи
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        try:
            tasks = Task.query.all()
            tasks_data = [task.to_dict() for task in tasks]
            
            return jsonify({
                'status': 'success',
                'data': tasks_data,
                'count': len(tasks_data)
            }), 200
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Ошибка при получении задач: {str(e)}'
            }), 500

    # GET /api/tasks/<id> - Получить задачу по ID
    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        try:
            task = Task.query.get(task_id)
            
            if not task:
                return jsonify({
                    'status': 'error',
                    'message': f'Задача с ID {task_id} не найдена'
                }), 404
            
            return jsonify({
                'status': 'success',
                'data': task.to_dict()
            }), 200
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Ошибка при получении задачи: {str(e)}'
            }), 500

    # POST /api/tasks - Создать новую задачу
    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        try:
            data = request.get_json()
            
            if not data or not data.get('title'):
                return jsonify({
                    'status': 'error',
                    'message': 'Заголовок задачи обязателен'
                }), 400
            
            new_task = Task(
                title=data['title'],
                description=data.get('description', ''),
                completed=data.get('completed', False)
            )
            
            db.session.add(new_task)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Задача успешно создана',
                'data': new_task.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'Ошибка при создании задачи: {str(e)}'
            }), 500

    # PUT /api/tasks/<id> - Обновить задачу
    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        try:
            task = Task.query.get(task_id)
            if not task:
                return jsonify({
                    'status': 'error',
                    'message': f'Задача с ID {task_id} не найдена'
                }), 404
            
            data = request.get_json()
            
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'completed' in data:
                task.completed = data['completed']
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Задача успешно обновлена',
                'data': task.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'Ошибка при обновлении задачи: {str(e)}'
            }), 500

    # DELETE /api/tasks/<id> - Удалить задачу
    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        try:
            task = Task.query.get(task_id)
            if not task:
                return jsonify({
                    'status': 'error',
                    'message': f'Задача с ID {task_id} не найдена'
                }), 404
            
            db.session.delete(task)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Задача успешно удалена'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'Ошибка при удалении задачи: {str(e)}'
            }), 500
