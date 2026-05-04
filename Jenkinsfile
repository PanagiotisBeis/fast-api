pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "pbeis/fast-api"
        IMAGE_TAG = "1.0.${BUILD_NUMBER}"
        LATEST_TAG = "latest"
    }

    stages {
        stage('Git Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/PanagiotisBeis/fast-api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKER_IMAGE:$IMAGE_TAG .
                    docker tag $DOCKER_IMAGE:$IMAGE_TAG $DOCKER_IMAGE:$LATEST_TAG
                '''
            }
        }

        stage('Login and Push to Docker Hub') {
            environment {
                DOCKER_HUB = credentials('fast-api')
            }

            steps {
                sh '''
                    echo "$DOCKER_HUB_PSW" | docker login -u "$DOCKER_HUB_USR" --password-stdin
                    docker push $DOCKER_IMAGE:$IMAGE_TAG
                    docker push $DOCKER_IMAGE:$LATEST_TAG
                '''
            }
        }

        stage('Deploy with Ansible') {
            environment {
                CONTAINER_NAME = 'service-status-api'
                APP_PORT = '8000'
            }

            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    ),
                    usernamePassword(
                        credentialsId: 'fast-api',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        ansible-playbook \
                        -i ansible/inventory.ini \
                        ansible/deploy.yml \
                        --private-key "$SSH_KEY" \
                        -u "$SSH_USER" \
                        -e "image=$DOCKER_IMAGE:$IMAGE_TAG" \
                        -e "container_name=$CONTAINER_NAME" \
                        -e "app_port=$APP_PORT" \
                        -e "dockerhub_username=$DOCKERHUB_USERNAME" \
                        -e "dockerhub_token=$DOCKERHUB_TOKEN"
                    '''
                }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Image deployed: $DOCKER_IMAGE:$IMAGE_TAG"
        }

        failure {
            echo "Pipeline failed."
        }
    }
}