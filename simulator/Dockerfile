# simulator/Dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production image
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
