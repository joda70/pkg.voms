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
        git(url: 'https://github.com/italiangrid/pkg.voms.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name stage-area-pkg.voms-${BUILD_NUMBER} italiangrid/pkg.base:centos6'
        sh '''
        pushd rpm 
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp stage-area-pkg.voms-${BUILD_NUMBER}:/stage-area repo'
        sh 'docker rm -f stage-area-pkg.voms-${BUILD_NUMBER}'
        archiveArtifacts 'repo/**'
      }
    }
  }
}
