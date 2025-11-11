pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'task-manager'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', 
                url: 'git@github.com:allnewyou/task-manager.git'
               

            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Запускаем контейнер для тестов
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
                        sh 'python -m pytest tests/ -v'
                    }
                }
            }
        }
        
        stage('Deploy to Registry') {
            steps {
                script {
                    // Здесь можно пушить в Docker Registry
                    // docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                    //     docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                    // }
                    echo "Image ${DOCKER_IMAGE}:${DOCKER_TAG} готов к деплою"
                }
            }
        }
    }
    
    post {
        always {
            echo "Сборка ${env.BUILD_NUMBER} завершена"
            cleanWs()
        }
        success {
            echo "✅ Сборка успешна!"
        }
        failure {
            echo "❌ Сборка провалилась"
        }
    }
}
