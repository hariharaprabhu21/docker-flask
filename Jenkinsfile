pipeline {
    agent any

    environment {
        IMAGE_NAME = "hariharaprabhu/myflask"
        IMAGE_TAG  = "v1"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

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
    }
}