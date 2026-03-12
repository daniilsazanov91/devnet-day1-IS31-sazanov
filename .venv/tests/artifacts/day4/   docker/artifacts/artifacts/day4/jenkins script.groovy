pipeline {
    agent any

    stages {

        stage('Preparation') {
            steps {
                echo 'Preparing build'
            }
        }

        stage('Build') {
            steps {
                echo 'Building application'
            }
        }

        stage('Results') {
            steps {
                echo 'Build finished'
            }
        }

    }
}
