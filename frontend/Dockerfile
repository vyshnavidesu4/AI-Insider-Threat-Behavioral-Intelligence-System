FROM node:20-alpine

WORKDIR /app

COPY package.json ./
# If package-lock.json exists, copy it as well
COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
