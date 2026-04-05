FROM node:20-slim

RUN apt-get update && \
    apt-get install -y python3 make g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY tsconfig.json ./
COPY paths.json more_paths.json ./
COPY src/ ./src/

RUN npm run build

RUN npm prune --omit=dev 2>/dev/null; exit 0

ENV NODE_ENV=production

CMD ["node", "dist/index.js"]
