pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
    }

    environment {
        APP_NAME = "alzheimers_app"
        IMAGE_NAME = "alzheimers_app_image"
    }

    stages {
        stage('Install Docker CLI') {
            steps {
                echo '⚙️ Installing Docker CLI inside container...'
                sh '''
                    apt-get update && apt-get install -y docker.io
                '''
            }
        }

        stage('Checkout') {
            steps {
                echo '📦 Cloning repository...'
                git branch: 'main', url: 'https://github.com/rishav-ghosh/alzheimers_webapp.git'
            }
        }

        stage('Setup Python & DVC') {
            steps {
                echo '🐍 Installing Python dependencies...'
                sh '''
                    pip install --no-cache-dir -r requirements.txt
                    pip install --no-cache-dir "dvc[all]"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Run Container') {
            steps {
                echo '🚀 Running Docker container...'
                sh '''
                    docker run -d --name ${APP_NAME} -p 5000:5000 ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up containers...'
            sh '''
                docker stop ${APP_NAME} || true
                docker rm ${APP_NAME} || true
            '''
        }
        success {
            echo '✅ Build and container run successful!'
        }
        failure {
            echo '❌ Build failed. Check logs above.'
        }
    }
}
