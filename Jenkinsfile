pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'task-manager'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                echo "Собираем Docker образ..."
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo "Запускаем базовые тесты..."
                script {
                    // Проверяем что приложение собирается
                    sh 'find . -name "*.py" | wc -l'
                    sh 'ls -la'
                    
                    // Проверяем что основные файлы на месте
                    sh 'test -f main.py && echo "✅ main.py существует"'
                    sh 'test -f requirements.txt && echo "✅ requirements.txt существует"'
                    sh 'test -d app && echo "✅ папка app существует"'
                }
            }
        }
        
        stage('Run Container Test') {
            steps {
                echo "Тестируем контейнер..."
                script {
                    // Запускаем контейнер и проверяем что он работает
                    def testContainer = docker.run("${DOCKER_IMAGE}:${DOCKER_TAG}", "-d -p 5000:5000")
                    sleep 10  // Ждем запуска контейнера
                    
                    // Проверяем что приложение отвечает
                    sh 'curl -f http://localhost:5000/ || echo "Приложение не ответило"'
                    
                    // Останавливаем тестовый контейнер
                    testContainer.stop()
                }
            }
        }
    }
    
    post {
        always {
            echo "Сборка ${env.BUBUILD_NUMBER} завершена"
            // Останавливаем все запущенные контейнеры
            sh 'docker stop $(docker ps -q) 2>/dev/null || true'
        }
        success {
            echo "✅ Сборка успешна!"
        }
        failure {
            echo "❌ Сборка провалилась"
        }
    }
}
