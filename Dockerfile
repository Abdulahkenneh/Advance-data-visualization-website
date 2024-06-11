# Dockerfile
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

# Add a script to filter out pywin32 on non-Windows systems
RUN grep -v "pywin32" requirements.txt > temp_requirements.txt && \
    pip install --no-cache-dir -r temp_requirements.txt

# Copy project
COPY . /app/

# Install any necessary dependencies for code execution
RUN pip install --no-cache-dir markdown2 pygments

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
