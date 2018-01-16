#!/bin/bash
set -ex
TRAVIS_REPO_SLUG=${TRAVIS_REPO_SLUG:-italiangrid/pkg.voms}
TRAVIS_JOB_ID=${TRAVIS_JOB_ID:-0}
DATA_CONTAINER_NAME="stage-area-pkg.voms-${TRAVIS_JOB_ID}"

export PING_SLEEP=30s
export BUILD_OUTPUT=$(pwd)/travis/travis-build.out

upload_report() {
  BUILD_REPORT_URL=${PKG_NEXUS_HOST}/repository/${PKG_NEXUS_REPONAME}/travis-build.out
  curl --user "${PKG_NEXUS_USERNAME}:${PKG_NEXUS_PASSWORD}" --upload-file travis/travis-build.out \
      ${PKG_NEXUS_HOST}/repository/${PKG_NEXUS_REPONAME}/travis-build.out

  echo "Build report available at:"
  echo ${BUILD_REPORT_URL}
}

dump_output() {
   echo Tailing the last 1000 lines of output:
   tail -1000 $BUILD_OUTPUT
}

error_handler() {
  echo ERROR: An error was encountered with the build.
  upload_report
  dump_output
  exit 1
}

trap 'error_handler' ERR

# Setup stage area container
docker create -v /stage-area --name ${DATA_CONTAINER_NAME} \
  italiangrid/pkg.base:centos6

bash -c "while true; do echo \$(date) - building ...; sleep $PING_SLEEP; done" &

PING_LOOP_PID=$!

pushd rpm
export PKG_NEXUS_REPONAME="travis/${TRAVIS_REPO_SLUG}/${TRAVIS_JOB_ID}"
bash build.sh >> ${BUILD_OUTPUT} 2>&1
popd
echo "pkg.voms build completed succesfully!"
kill ${PING_LOOP_PID}

upload_report
