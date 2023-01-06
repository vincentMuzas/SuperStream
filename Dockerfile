FROM node:latest

WORKDIR /usr/src/SuperStream
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 22
EXPOSE 8080
EXPOSE 3000
EXPOSE 80

CMD ["npm", "start"]
#CMD [""node", "server.js""]