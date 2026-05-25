# Stage 1: Build the frontend static files
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve the backend FastAPI server along with the frontend static files
FROM python:3.11-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY backend/ /app/

# Copy the built frontend static files to backend/static
COPY --from=frontend-builder /app/frontend/out /app/static

# Copy master database to appropriate place
COPY ELITE_HR_Master_Dashboard.xlsx /ELITE_HR_Master_Dashboard.xlsx

# Set environment variables
ENV PORT=7860
EXPOSE 7860

# Run FastAPI using uvicorn on port 7860 for Hugging Face Spaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
