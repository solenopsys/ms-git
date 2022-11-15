FROM alpine:latest

RUN apk add --update nginx && \
    apk add --update git-daemon && \
    apk add --update fcgiwrap && \
    apk add --update spawn-fcgi && \
    rm -rf /var/cache/apk/*


COPY  ./containers/nginx.conf /etc/nginx/nginx.conf

CMD spawn-fcgi -s /run/fcgi.sock /usr/bin/fcgiwrap && \
    nginx -g "daemon off;"
