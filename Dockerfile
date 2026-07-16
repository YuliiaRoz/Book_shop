# 1. Use a lightweight official Python runtime as a base image
FROM python:3.12-slim

# 2. Set environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy only dependency files first to leverage Docker layer caching
COPY requirements.txt .

# 5. Install dependencies without saving pip cache files
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application source code
COPY . .

RUN chmod +x /app/docker-entrypoint.sh

## 7. Create a non-root user and switch to it for security
#RUN useradd -u 8888 appuser && chown -R appuser /app
#USER appuser

# 8. Expose the port your application listens on (e.g., 8000)
EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# 9. Define the default command to run your app (e.g., a FastAPI or Flask app)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

