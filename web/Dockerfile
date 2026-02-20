########## Build study ##########
FROM node:22-alpine AS build_study

RUN npm install -g pnpm@10

WORKDIR /app/study
COPY study/package.json study/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY study/src ./src
COPY study/static ./static
COPY study/components.json study/eslint.config.js study/svelte.config.js study/tsconfig.json study/vite.config.ts ./
RUN pnpm build

########## Final Nginx image with both sites ##########
FROM nginx:1.27.0

RUN apt-get update && apt-get install ca-certificates -y && update-ca-certificates

ARG host=0.0.0.0
ARG port=3000
ARG ssl_port=3001

RUN openssl req -trustout -x509 -newkey rsa:4096 -sha256 -nodes \
    -keyout /etc/ssl/private/pingpong-self-signed.key \
    -out /etc/ssl/certs/pingpong-self-signed.crt \
    -days 3650 \
    -subj "/C=US/ST=MA/L=Cambridge/O=Harvard Kennedy School/OU=CPL/CN=pingpong-web.private"

ENV NGINX_LISTEN=$host:$port
ENV NGINX_LISTEN_SSL=$host:$ssl_port
ENV NGINX_SSL_CERT=/etc/ssl/certs/pingpong-self-signed.crt
ENV NGINX_SSL_CERT_KEY=/etc/ssl/private/pingpong-self-signed.key

# Use the nginx template stored at repo web/ level
COPY default.conf.template /etc/nginx/templates/
COPY --from=build_study   /app/study/build   /usr/share/nginx/html/study
