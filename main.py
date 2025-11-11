from flask import Flask
from app.database import init_database
from app.routes import register_routes
import os

def create_app():
	#Фабрика приложений Flask - создает и настраивает приложение
	#Создаем экземпляр Flask приложения
	app = Flask(__name__)

	#Устанавливаем секретный ключ для сессий
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

	#Инициализируем базу данных
	init_database(app)

	#Регистрируем API маршруты
	register_routes(app)

	#Простой маршрут для проверки работы
	@app.route('/')
	def hello():
		return jsonify({
			'message': 'Task Manager API работает!',
			'endpoints': {
				'GET /api/tasks': 'Получить все задачи',
				'GET /api/tasks/<id>': 'Получить задачу по ID',
				'POST /api/tasks': 'Создать новую задачу',
				'PUT /api/tasks/<id>': 'Обновить задачу',
				'DELETE /api/tasks/<id>': 'Удалить задачу'
			}
		})

	return app

if __name__ == '__main__':
	app = create_app()
	#Запускаем приложение

	#debug=True - включение режима отладки
	#host='0.0.0.0' - делает приложение доступным извне
	app.run(debug=True, host='0.0.0.0', port=5000)
