# --- Development Stage ---
FROM node:20-alpine AS development

WORKDIR /workspace/frontend

# Copy dependencies manifest
COPY package*.json ./

# Install development dependencies
RUN npm install

# Copy frontend source files
COPY . .

# Run Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
