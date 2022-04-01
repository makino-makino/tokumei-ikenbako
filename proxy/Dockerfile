FROM nginx:alpine

# set BASIC authenticate password
ARG INCUBATOR_PASS

RUN apk add apache2-utils
RUN htpasswd -bc /etc/nginx/.htpasswd incubator "$INCUBATOR_PASS" 