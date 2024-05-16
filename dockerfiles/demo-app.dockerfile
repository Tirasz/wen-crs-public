FROM node:18.18.2-alpine3.18 as build

ARG ELASTIC_CLIENT
ARG DUMMY_CLIENT

ENV ELASTIC_CLIENT=$ELASTIC_CLIENT
ENV DUMMY_CLIENT=$DUMMY_CLIENT

WORKDIR /app

COPY ../src/demo-app .

RUN chmod +rwx ./init.sh

RUN ./init.sh

RUN npm install --force

RUN npm run build:prod

FROM cgr.dev/chainguard/nginx

COPY --from=build /app/dist/demo-app /usr/share/nginx/html

EXPOSE 8080