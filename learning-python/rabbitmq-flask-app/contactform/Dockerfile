FROM nginx:alpine
## Copy new config file setting port to 8080
COPY ./default.conf /etc/nginx/conf.d/
COPY ./index.html /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
