pipeline {
    agent any
    stages {
        stage('Clonar código') {
            steps {
                script {
                    checkout scm
                }
            }
        }
        stage('Construir imagen Docker') {
            steps {
                bat 'docker build -t mi_app .'
            }
        }
        stage('Ejecutar contenedor') {
            steps {
                bat 'docker run -d -p 5000:5000 --name mi_app_container mi_app'
            }
        }
        stage('Verificar contenedores') {
            steps {
                bat 'docker ps'
            }
        }
    }
}