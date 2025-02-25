pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/hello-world:latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/sharmah9713/sharmah9713.git'
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
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: 'https://index.docker.io/v1/']) {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }
    }
}
