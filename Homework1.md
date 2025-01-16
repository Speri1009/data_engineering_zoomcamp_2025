# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run

What's the version of `pip` in the image?

- 24.3.1

Docker file changes
FROM python:3.12.8
RUN pip --version

Result pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
      POSTGRES_DB: "ny_taxi"
    ports:
      - "5433:5432"
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433

## Prepare Postgres

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:

1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles

SQL

```
    SELECT
        CASE
            WHEN trip_distance <= 1 THEN 'Up to 1 mile'
            WHEN trip_distance > 1 AND trip_distance <= 3 THEN 'Between 1 and 3 miles'
            WHEN trip_distance > 3 AND trip_distance <= 7 THEN 'Between 3 and 7 miles'
            WHEN trip_distance > 7 AND trip_distance <= 10 THEN 'Between 7 and 10 miles'
            WHEN trip_distance > 10 THEN 'Over 10 miles'
            ELSE 'Unknown'
        END AS distance_category,
    COUNT(*)
    FROM green_tripdata_2019
    GROUP BY 1
    ORDER BY 1 DESC
```

Answer:

- 104,838; 199,013; 109,645; 27,688; 35,202

## Question 4. Longest trip for each day

SQL

```
    SELECT
        DATE(lpep_pickup_datetime),
        trip_distance
    FROM green_tripdata_2019
    GROUP BY 1,2
    ORDER BY 2 DESC
    LIMIT 5
```

Answer:

- 2019-10-31(515.89 miles)

## Question 5. Three biggest pickup zones

SQL

```
    SELECT
        tz."Zone",
        SUM(total_amount)  AS total_amount
    FROM green_tripdata_2019 gt
    LEFT JOIN taxi_zones tz ON tz."LocationID" = gt."PULocationID"
    WHERE date(lpep_pickup_datetime) = '2019-10-18'
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 3
```

Answer:

- East Harlem North, East Harlem South, Morningside Heights

## Question 6. Largest tip

SQL

```
    SELECT
    	tzd."Zone",
    	gt."tip_amount"  AS Tip_amount
    FROM green_tripdata_2019 gt
    LEFT JOIN taxi_zones tzp ON tzp."LocationID" = gt."PULocationID"
    LEFT JOIN taxi_zones tzd ON tzd."LocationID" = gt."DOLocationID"
    WHERE date_trunc('month',DATE(lpep_pickup_datetime)) = '2019-10-01'
        AND tzp."Zone" = 'East Harlem North'
    ORDER BY 2 DESC
    LIMIT 1
```

Answer:

- Yorkville West (87.3 $)

## Terraform

## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:

- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-aprove, terraform destroy
- terraform init, terraform apply -auto-aprove, terraform destroy
- terraform import, terraform apply -y, terraform rm
