pipeline {
    agent any

    environment {
        APP_NAME = "alzheimers_app"
        IMAGE_NAME = "alzheimers_app_image"
    }

    stages {

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
                    python3 -m pip install --upgrade pip
                    pip3 install -r requirements.txt --break-system-packages
                    pip3 install "dvc[all]" --break-system-packages
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
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} -p 5000:5000 ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build and container run successful!'
            echo '🌐 Visit: http://localhost:5000'
        }
        failure {
            echo '❌ Build failed. Check logs above.'
        }
    }
}
