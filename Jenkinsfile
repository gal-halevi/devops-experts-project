pipeline {
    agent none

    environment {
        DOCKER_IMAGE = 'galhalevi/counter-app'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    options {
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
    }

    stages {
        stage("Tests") {
            agent {
                label 'mac'
            }
            steps {
                checkout scm

                sh '''
                    set -eu

                    mkdir -p reports
                    export PIP_CACHE_DIR="$PWD/.pip-cache"
                    mkdir -p "$PIP_CACHE_DIR"

                    rm -rf .venv
                    python3.12 -m venv .venv
                    . .venv/bin/activate
                    
                    python -m pip install -U pip
                    python -m pip install -r src/requirements-dev.txt

                    python -m pytest \
                        --junitxml=reports/pytest.xml \
                        --cov \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-fail-under=0 \
                        -v tests/

                    python -m coverage report --show-missing
                '''
            }
            post {
                always {
                    junit "reports/pytest.xml"
                    archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: false, fingerprint: true
                    recordCoverage(
                        tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']],
                        sourceCodeRetention: 'LAST_BUILD',
                        enabledForFailure: true
                    )
                }
            }
        }
        stage("Build & Push Docker Image") {
            agent {
                label 'mac'
            }
            steps {
                checkout scm

                script {
                    def shaTag = "sha-${env.GIT_COMMIT.take(7)}"
                    def latestTag = 'latest'

                    def imageRef = "${env.DOCKER_IMAGE}:${shaTag}"

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                        sh """
                            set -eu

                            echo "\$DH_TOKEN" | docker login -u "\$DH_USER" --password-stdin

                            docker build \\
                                --tag ${imageRef} \\
                                --tag ${env.DOCKER_IMAGE}:${latestTag} \\
                                src/

                            # Cleanup function to remove container on exit
                            cid=""
                            cleanup() {
                                if [ -n "\$cid" ]; then
                                docker rm -f "\$cid" >/dev/null 2>&1 || true
                                fi
                            }
                            trap cleanup EXIT

                            # Run container on an available port on host and check health endpoint
                            cid=\$(docker run -d -p 0:5000 ${imageRef})
                            hostPort=\$(docker port \$cid 5000/tcp | awk -F: 'NR==1 {print \$NF}')
                            curl -fsS --retry-connrefused --retry 5 "http://localhost:\$hostPort/healthz"

                            docker push ${imageRef}

                            # Push 'latest' only from main
                            if [ "${env.BRANCH_NAME}" = "main" ]; then
                              docker push ${env.DOCKER_IMAGE}:${latestTag}
                            else
                              echo "Skipping 'latest' push on branch: ${env.BRANCH_NAME}"
                            fi
                        """
                    }
                }
            }
        }

        stage("Deploy to Kubernetes") {
            // when {
            //     branch 'main'
            // }
            agent {
                label 'mac'
            }
            steps {
                checkout scm
                script {
                    def shaTag = "sha-${env.GIT_COMMIT.take(7)}"
                    sh """
                        set -eu

                        kubectl config current-context
                        kubectl get nodes

                        helm upgrade --install counter-app ./chart/flask-counter \\
                            --namespace default --create-namespace \\
                            --set image.repository=${env.DOCKER_IMAGE} \\
                            --set image.tag=${shaTag} \\
                            --wait --timeout 2m
                    """
                }
            }
        }
    }
}