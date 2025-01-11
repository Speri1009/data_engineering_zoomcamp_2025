# Use a base Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files
COPY ingest-data.py /app/
COPY yellow_tripdata_2024-01.parquet /app/
COPY green_tripdata_2019-09.parquet /app/
COPY requirements.txt /app/

# Expose the PostgreSQL port (optional, not required for this script)
EXPOSE 5432

# Prevent Python output buffering
ENV PYTHONUNBUFFERED=1

ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=ny_taxi

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files into the container

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "ingest-data.py"]
