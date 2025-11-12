pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'task-manager'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Pre-check') {
            steps {
                echo "Проверяем окружение..."
                script {
                    // Проверяем доступность Docker
                    sh 'docker --version'
                    sh 'docker info | grep "Server Version"'
                    
                    // Проверяем файлы проекта
                    sh 'ls -la'
                    sh 'test -f Dockerfile && echo "✅ Dockerfile найден" || echo "❌ Dockerfile не найден"'
                    sh 'test -f requirements.txt && echo "✅ requirements.txt найден" || echo "❌ requirements.txt не найден"'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Собираем Docker образ..."
                script {
                    try {
                        // Пробуем собрать с кэшем
                        sh 'docker build --pull -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                    } catch (Exception e) {
                        echo "Ошибка сборки: ${e}"
                        // Пробуем альтернативный базовый образ
                        sh '''
                        cat > Dockerfile.alternative << "DOCKERFILE"
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
DOCKERFILE
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG}-alt -f Dockerfile.alternative .
                        '''
                    }
                }
            }
        }
        
        stage('Test Basic') {
            steps {
                echo "Запускаем базовые тесты..."
                script {
                    // Проверяем структуру проекта
                    sh 'find . -name "*.py" | wc -l'
                    sh 'test -f main.py && echo "✅ main.py существует"'
                    sh 'test -d app && echo "✅ папка app существует"'
                    
                    // Проверяем зависимости
                    sh 'test -f requirements.txt && cat requirements.txt'
                }
            }
        }
    }
    
    post {
        always {
            echo "Сборка ${env.BUILD_NUMBER} завершена"
            // Очистка
            sh 'docker system prune -f || true'
        }
        success {
            echo "✅ Сборка успешна!"
            // Показываем информацию о собранном образе
            sh 'docker images | grep ${DOCKER_IMAGE} || true'
        }
        failure {
            echo "❌ Сборка провалилась"
        }
    }
}
