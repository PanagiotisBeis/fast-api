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
                APP_SERVER_IP = '18.196.197.231'
                CONTAINER_NAME = 'service-status-api'
                APP_PORT = '8000'
            }

            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'app-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    sh '''
                        cat > inventory.ini <<EOF
[app]
${APP_SERVER_IP} ansible_user=${SSH_USER} ansible_ssh_private_key_file=${SSH_KEY} ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF

                        cat > deploy.yml <<EOF
- name: Deploy FastAPI container
  hosts: app
  become: yes

  tasks:
    - name: Pull application image
      community.docker.docker_image:
        name: "${DOCKER_IMAGE}:${IMAGE_TAG}"
        source: pull

    - name: Stop and remove old container
      community.docker.docker_container:
        name: "${CONTAINER_NAME}"
        state: absent

    - name: Run new container
      community.docker.docker_container:
        name: "${CONTAINER_NAME}"
        image: "${DOCKER_IMAGE}:${IMAGE_TAG}"
        state: started
        restart_policy: always
        ports:
          - "${APP_PORT}:8000"

    - name: Check application health
      uri:
        url: "http://localhost:${APP_PORT}/health"
        method: GET
        status_code: 200
EOF

                        ansible-galaxy collection install community.docker
                        ansible-playbook -i inventory.ini deploy.yml
                    '''
                }
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
