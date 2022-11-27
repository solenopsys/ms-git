#!/bin/sh

build_push(){
  docker buildx build   -f containers/git-api.Dockerfile  --platform ${ARCHS} -t ${REGISTRY}/alexstorm-git-api:latest  --push .
  docker buildx build   -f containers/git-http.Dockerfile   --platform ${ARCHS} -t ${REGISTRY}/alexstorm-git-http:latest   --push .
}

helm_build_push(){
  FN=${NAME}-${VER}.tgz
  rm ${FN}
  helm package ./install --version ${VER}
  curl --data-binary "@${FN}" http://helm.alexstorm.solenopsys.org/api/charts
}

REGISTRY=registry.alexstorm.solenopsys.org
NAME=alexstorm-git-wrapper
ARCHS="linux/amd64,linux/arm64"
VER=0.1.22

build_push
helm_build_push





