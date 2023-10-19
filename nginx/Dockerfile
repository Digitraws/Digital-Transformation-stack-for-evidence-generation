FROM nginx:stable

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install inotify-tools -y

COPY ./nginxReloader.sh /usr/local/openresty/bin/nginxReloader.sh
COPY ./docker-entrypoint.sh /usr/local/openresty/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/openresty/bin/nginxReloader.sh
RUN chmod +x /usr/local/openresty/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/openresty/bin/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
