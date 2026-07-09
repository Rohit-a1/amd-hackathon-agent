FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent code
COPY main.py .

# Create input/output directories so they exist
RUN mkdir -p /input /output

# The entry point of our agent
CMD ["python", "main.py"]
