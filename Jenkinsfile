pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '5')) 
  }

  environment {
    DATA_CONTAINER_NAME="stage-area-pkg.voms-${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}"
  }

  stages{
    stage('package') {
      steps {
        deleteDir()
        git(url: 'https://github.com/italiangrid/pkg.voms.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos6'
        sh '''
        pushd rpm 
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area repo'
        sh 'docker rm -f ${DATA_CONTAINER_NAME}'
        archiveArtifacts 'repo/**'
      }
    }
  }
}
