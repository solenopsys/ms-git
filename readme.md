# Docker
docker build  -f containers/git-api.Dockerfile -t registry.local/git_api:latest .
docker push registry.local/git_api:latest
docker build -f containers/git-http.Dockerfile  -t registry.local/git_http:latest .
docker push registry.local/git_http:latest

# Helm
helm package .\install

## Registry width helm cli
helm push git-0.1.0.tgz  oci://helm.local --insecure-skip-tls-verify

## Registry width direct http
curl --data-binary "@git-0.1.0.tgz" http://helm.local/api/charts

# Env Vars
GitRootDir = /home/alexstorm/sources/GitAPI/git_test
Host = localhost
Port = 8180

