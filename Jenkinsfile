pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "sharmah9713/sharmah9713:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/sharmah9713/Harshu_test.git'
            }
        }

        stage('Build') {
            steps {
                sh 'javac HelloWorld.java'
                sh 'echo Build Successful'
            }
        }

        stage('Package') {
            steps {
                sh 'tar -czf hello-world.tar.gz HelloWorld.class'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'docker-hub-token', variable: 'DOCKER_HUB_PASS')]) {
                    sh """
                    echo "$DOCKER_HUB_PASS" | docker login -u "sharmah9713" --password-stdin
                    docker push $DOCKER_IMAGE
                    """
                }
            }
        }
    }
}
