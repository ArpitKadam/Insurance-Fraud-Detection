# Step 1: Use a compatible base image
FROM python:3.9-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get install -y awscli

# Step 4: Add the `src` directory to PYTHONPATH
ENV PYTHONPATH=/app/src

# Step 5: Copy the rest of the application code
COPY . /app

# Step 6: Expose the application port
EXPOSE 5000

# Step 7: Run the application
CMD ["python", "app.py"]

