from flask import jsonify, request
from .models import db, Task

def register_routes(app):
	#Регистрируем все API маршруты в приложении Flask
	#GET /api/tasks - получить все задачи
	@app.route('/api/tasks', methods=['GET'])
	def get_tasks():
		#Метод для получения всех задач
		try:
			#Получаем все задачи
			tasks = Task.query.all()
			#Преобразуем каждую задачу в словарь
			tasks_data = [task.to_dict() for task in tasks]

			#Возвращаем JSON ответ
			return jsonify({
				'status': 'success',
				'data': tasks_data,
				'count': len(tasks_data)
			}), 200 #200 - успешный статус

		except Exception as e:
			#В случае ошибки возвращаем сообщение об ошибке
			return jsonify({
				'status': 'error',
				'message': f'Ошибка при получении задач: {str(e)}'
			}), 500 #500 - Ошибка сервера

	#GET /api/tasks/<id> - Получить задачу по ID
	@app.route('/api/tasks/<int:task_id>', methods=['GET'])
	def get_task(task_id):
		#Получаем одну задачу по её ID
		try:
			#Ищем задачу в базе данных по её ID
			task = Task.query.get(task_id)

			#Если задача не найдена
			if not task:
				return jsonify({
					'status': 'error'
					'message': f'Задача с ID {task_id} не найдена'
				}), 404 #404 - не найдено

			#Возвращаем найденную задачу
			return jsonify({
				'status': 'success'
				'data': task.to_dict()
			}), 200

		except Exception as e:
			return jsonify({
				'status': 'error',
				'message': f'Ошибка при получении задачи: {str(e)}'
			}), 500

	#POST /api/tasks - Создать новую задачу
	@app.route('/api/tasks', methods=['POST'])
	def create_task():
		#Создаем новую задачу из данных JSON
		try:
			#Получаем данные из тела запроса
			task = request.get_json()

			#Проверяем, что заголовок предоставлен
			if not data or not data.get('title'):
				return jsonify({
					'status': 'error',
					'message': 'Заголовок задачи обязателен!'
				}), 400

			#Создаем новую задачу
			new_task = Task(
				title=data['title'],
				description=data.get('description', ''),
				completed=data.get('completed', False)
			)

			#Добавляем задачу в базу данных
			db.session.add(new_task)
			db.session.commit()

			#Возвращаем созданную задачу
			return jsonify({
				'status': 'success',
				'message': 'Задача успешно создана',
				'data': new_task.to_dict()
			}), 201 #201 - Создано

			except Exception as e:
				#Откатываем изменения в случае ошибки
				db.session.rollback()
				return jsonify({
					'status': 'error',
					'message': f'Ошибка при создании задачи: {str(e)}'
				}), 500

	#PUT /api/tasks/<id> - Обновить задачу
	@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
	def update_task(task_id):
		#Полностью обновляем задачу
		try:
			task = Task.query.get(task_id)
			if not task:
				return jsonify({
					'status': 'error',
					'message': f'Задача с ID {task_id} не найдена'
				}), 404

			data = request.get_json()

			#Обновляем поля задачи
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

	#DELETE /api/tasks/<id> - Удалить задачу
	@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
	def delete_task(task_id):
		#Удаляем задачу по ID
		try:
			task = Task.query.get(task_id)
			if not task:
				return jsonify({
					'status': 'error',
					'message': f'Задача с ID {task_id} не найдена'
				}), 404

			#Удаляем задачу из базы данных
			db.session.delete(task)
			db.session.commit()

			return jsonify({
				'status': 'success',
				'message': 'Задача успешно удалено'
			}), 200

		except Exception as e:
			db.session.rollback()
			return jsonify({
				'status': 'error',
				'message': f'Ошибка при удалении задачи: {str(e)}'
			}), 500
