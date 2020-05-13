@Library('alauda-cicd') _

// global variables for pipeline
def RELEASE_BUILD = ""
def BRANCH = ""

pipeline {
    agent {label 'python-3.6'}
    options {
        skipDefaultCheckout()
    }
    environment {
        // repository name
        FOLDER = "."
        REPOSITORY = "ares"
        // repo user
        OWNER = "mathildetech"

        TAG_CREDENTIALS="alaudabot-bitbucket"

        DEPLOYMENT_NAME = "ares"
        PROXY_CREDENTIALS_ID = "proxy"
        DINGTALK_ROBOT = "ares-robot"

        TEST_IMAGE = "index.alauda.cn/alaudak8s/ares"
        SONOBUOY_IMAGE = "index.alauda.cn/alaudaorg/qaimages:sonobuoy"
    }
    stages {
        stage('Checkout') {
			steps {
				script {
					dir(FOLDER) {
						container('tools') {
							// checkout code
							def scmVars
							retry(2) { scmVars = checkout scm }
							release = deploy.release(scmVars)

							RELEASE_BUILD = release.version
							RELEASE_VERSION = release.majorVersion
							BRANCH = release.chartBranch
							if (release.change["branch"]){
							    BRANCH = release.change["branch"].replace("/", "-")
							}
							CASE_PATH = release.change["title"]
							echo """
								release ${RELEASE_VERSION}
								version ${RELEASE_BUILD}
								branch ${BRANCH}
								change case_path ${CASE_PATH}
								change ${release.chartBranch}
							"""
							sh "rm -rf report;mkdir report"
						}
					}
				}
			}
		}
        stage('CI') {
            steps {
                script {
                    container("tools"){
                        sh "apt update -y;apt install -y python3-pip"
                        sh "pip3 install flake8==3.7.9"
                        echo "run flake8..."
                        sh "flake8"
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    container("tools"){
                        IMAGE = deploy.dockerBuildWithRegister(
                            dockerfile: "Dockerfile", //Dockerfile
                            address: "alaudak8s/ares",
                            tag: "${BRANCH}", // tag
                        )
                        IMAGE.start().push().push(RELEASE_BUILD)
                        if (BRANCH == "master"){
                            IMAGE.push("latest")
                        }
                    }
                }
            }
        }
        stage('Test') {
            when {
                not {
                    branch "master"
                }
                not {
                    branch "release*"
                }
            }
            steps {
                script {
                    container("tools"){
                        // 准备kubectl
                        sh """
                            kubectl config set-cluster automation --server=https://94.191.89.53:6443 --insecure-skip-tls-verify=true
                            kubectl config set-credentials automation --token=eyJhbGciOiJSUzI1NiIsImtpZCI6IlpVNzBRMkFTZmxENDVyYnR0WEZzaXpYQzVxMnF0Y3hFUTlpaUlBVE82SEUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVycm9sZS1hZ2dyZWdhdGlvbi1jb250cm9sbGVyLXRva2VuLXpwdnh2Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImNsdXN0ZXJyb2xlLWFnZ3JlZ2F0aW9uLWNvbnRyb2xsZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI0NTJkMTI4Ny03MGNjLTRkZGYtODNkYi1jNGJhODExYzFlNWIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06Y2x1c3RlcnJvbGUtYWdncmVnYXRpb24tY29udHJvbGxlciJ9.taGR1f4dU65HgQjaIByvj4A58yQwghA1ZHoNEfHMvYr_zezL8DHmplzNCIJXOuc3EAL07raARSjiR3Kask17NbybzXTk8TAHb66dCRivGlTnS3xeiDi4PhPVvcUeNJ4rThawFyQEiwcqNlOr4axWIP4q9APf-5lZeGTDRrzCs8mYF58fHxLAl2xgWlI2H5se-1TAWbte0n16gqUv7LtArSAxtFecJakHuG4KwhmzclU8sOaQGdhcrega-kPp7CXsgkYuSUvapP5AEKwySNNIIvZ8V_EckGK5edtS_egYatNU3jenJYxMVO0I1zrTq72fm7VR_v7tgkgz9_yOSehQQw
                            kubectl config set-context automation --cluster=automation --user=automation
                            kubectl config use-context automation
                        """
                        api_image = "${TEST_IMAGE}:${RELEASE_BUILD}"
                        // 获取时间戳 当做测试的ns
                        sh "date +%Y%m%d%H%M > current_date"
                        def date = readFile "current_date"
                        date = date.replace("\n", "")
                        try {
                            // 生成测试yaml
                            sh "sonobuoy gen plugin --name ares-pr --image ${api_image} -e TESTCASES='${CASE_PATH}' -e CASE_TYPE= -e RESOURCE_PREFIX=${BRANCH} > ares-pr.yaml"
                            sh "sonobuoy run --sonobuoy-image ${SONOBUOY_IMAGE} --plugin ares-pr.yaml -n ares-${date} --rbac=Enable --context=automation --wait"
                        }
                        catch (Exception exc) {
                            echo "${exc}"
                            throw(exc)
                        }
                        finally {
                            // 拷贝测试数据
                            def result_tar = sh script: "sonobuoy retrieve -n ares-${date}", returnStdout: true
                            sh "rm -rf api_report;mkdir api_report"
                            sh "sonobuoy delete -n ares-${date}"
                            // 检查测试结果
                            sh "apt-get install -y language-pack-zh-hans;pip3 install requests==2.18.4"
                            env.PYTHONIOENCODING="utf-8"
                            sh "python3 api_script/check_api_result.py ares-pr ${result_tar}"
                        }
                    }
                }
            }
        }
        stage('restore-cluster') {
            when {
                not {
                    branch "master"
                }
                not {
                    branch "release*"
                }
            }
            steps {
                script {
                    container("tools"){
                        try {
                            sh "rm ~/.kube/config"
                        }
                        catch (Exception exc) {
                            echo "${exc}"
                        }
                    }
                }
            }
        }
        stage('Tag git') {
			when {
				expression {
					release.shouldTag()
				}
				anyOf {
				    branch "master";
				    branch "release*"
				}
			}
			steps {
				script {
					dir(FOLDER) {
						container('tools') {
							deploy.gitTag(
								TAG_CREDENTIALS,
								RELEASE_BUILD,
								OWNER,
								REPOSITORY
							)
						}
					}
				}
			}
		}
        stage('Chart Update') {
            when {
                 expression {
                     // TODO: Change when charts are ready
                     release.shouldUpdateChart()
                 }
                 anyOf {
				    branch "master";
				    branch "release*"
				}
             }
            steps {
                script {
                    deploy.triggerChart([
                        chart: DEPLOYMENT_NAME,
                        component: DEPLOYMENT_NAME,
                        version: RELEASE_VERSION,
                        imageTag: RELEASE_BUILD,
                        branch: release.chartBranch,
                        prBranch: release.change["branch"],
                        env: release.environment
                    ]).start()
                }
            }
        }
    }

    post {
        always {
            script {
                container('tools') {
                    deploy.alaudaNotification notification: [name: 'apitest-notification', namespace: 'cpaas-system']
                }
                archiveArtifacts allowEmptyArchive: true, artifacts: "api_report/**", fingerprint: true
                junit allowEmptyResults: true, testResults: 'api_report/*.xml'
            }
        }
    }
}
