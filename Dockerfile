# Use a base Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY script.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the default command
CMD ["python", "script.py"]
