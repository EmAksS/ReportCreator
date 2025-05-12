FROM node:18-alpine

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install

# Копирование проекта
COPY . .

# Сборка проекта (если нужно)
RUN npm run build

# Запуск сервера разработки (или serve для production)
CMD ["npm", "start"]