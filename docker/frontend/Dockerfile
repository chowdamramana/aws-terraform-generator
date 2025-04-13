FROM node:20 AS build
WORKDIR /app
COPY frontend/package.json .
# Generate package-lock.json during build
RUN npm install --package-lock-only && npm install
COPY frontend .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]