pipeline {
    agent none

    environment {
        DOCKER_IMAGE = 'galhalevi/counter-app'
        PIP_DISABLE_PIP_VERSION_CHECK=1
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
    }
}