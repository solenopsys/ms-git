FROM node:alpine

RUN apk add --no-cache tini git \
    && yarn global add git-http-server  # \

WORKDIR /home/git

ENTRYPOINT ["tini", "--", "git-http-server", "-p", "8080",   "/home/git"]