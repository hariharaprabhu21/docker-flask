pipeline {
    agent any

    environment {
        IMAGE_NAME = "hariharaprabhu21/myflask"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Verify Docker') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                    '''
                }
            }
        }
    }
}