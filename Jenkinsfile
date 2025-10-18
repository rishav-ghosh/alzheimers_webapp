pipeline {
    agent any

    environment {
        IMAGE_NAME = "alzheimers_webapp"
        CONTAINER_NAME = "alzheimers_app"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/your-username/alzheimers_webapp.git'
            }
        }

        stage('Setup Python & DVC') {
            steps {
                echo "Installing dependencies..."
                sh 'pip install dvc[all]'
                sh 'dvc pull'   // fetch model files tracked by DVC
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                echo "Running Flask app container..."
                sh '''
                docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
                sleep 10
                docker ps
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning up containers..."
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            '''
        }
    }
}
