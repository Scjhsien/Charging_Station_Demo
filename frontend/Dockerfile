FROM node:18-alpine AS build-stage
WORKDIR /app
COPY . .
RUN npm install
RUN npm install -D @types/node
RUN npm run build

FROM nginx:alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
