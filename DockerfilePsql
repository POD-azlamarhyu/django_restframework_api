FROM postgres:15.7-bullseye

ENV LANGUAGE ja_JP:ja
ENV TZ JST-9
ENV TERM xterm
ENV TZ Asia/Tokyo
RUN apt-get update && apt-get install -y
RUN mkdir -p /psql/data
COPY . ./psql/data
WORKDIR /psql/data
EXPOSE 5432