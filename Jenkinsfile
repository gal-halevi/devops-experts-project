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
                docker {
                    image 'python:3.12-slim'
                }
            }
            steps {
                checkout scm

                sh '''
                    set -eu

                    mkdir -p reports
                    export PIP_CACHE_DIR="$PWD/.pip-cache"
                    mkdir -p "$PIP_CACHE_DIR"

                    rm -rf .venv
                    python -m venv .venv
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
                docker {
                    image 'docker:27-cli'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                checkout scm

                script {
                    def shaTag = "sha-${env.GIT_COMMIT.take(7)}"
                    def safeBranchName = env.BRANCH_NAME.toLowerCase().replaceAll('/', '-')
                    def branchBuild = "${safeBranchName}-b${env.BUILD_NUMBER}"
                    def latestTag = 'latest'

                    def imageRef = "${env.DOCKER_IMAGE}:${shaTag}"

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                        sh """
                            set -eu

                            # Install curl (docker:*-cli is Alpine-based)
                            apk add --no-cache curl >/dev/null

                            echo "\$DH_TOKEN" | docker login -u "\$DH_USER" --password-stdin

                            docker build \\
                                --tag ${imageRef} \\
                                --tag ${env.DOCKER_IMAGE}:${branchBuild} \\
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

                            cid=\$(docker run -d -p 5000:5000 ${imageRef})
                            curl -fsS --retry-connrefused --retry 5 http://localhost:5000/healthz

                            docker push ${imageRef}
                            docker push ${env.DOCKER_IMAGE}:${branchBuild}

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
    }
}