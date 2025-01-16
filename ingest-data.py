print("Hello World")

#!/usr/bin/env python
# coding: utf-8
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    # engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")
    # test_engine = engine.connect()
    df_zones = pd.read_csv("taxi_zone_lookup.csv")
    df_zones.to_sql(name="taxi_zones", con=engine, if_exists="append")
    print(df_zones.head(10))
    df = pq.read_metadata("green_tripdata_2019-10.parquet")

    file = pq.ParquetFile("green_tripdata_2019-10.parquet")
    table = file.read()
    print(table.schema)
    df = table.to_pandas()
    print(df.head(10))
    print(pd.io.sql.get_schema(df, name=table_name, con=engine))
    batches_iter = file.iter_batches(batch_size=100000)
    batches_iter

    # Take the first batch for testing
    df = next(batches_iter).to_pandas()
    print(df.head(10))

    t_start = time()
    count = 0
    for batch in file.iter_batches(batch_size=100000):
        count += 1
        batch_df = batch.to_pandas()
        print(f"inserting batch {count}...")
        b_start = time()

        batch_df.to_sql(name=table_name, con=engine, if_exists="append")
        b_end = time()
        print(f"inserted! time taken {b_end - b_start:10.3f} seconds.\n")

    t_end = time()
    print(
        f"Completed! Total time taken was {t_end - t_start:10.3f} seconds for {count} batches."
    )


## upload new table for zones


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data to Postgres")
    parser.add_argument("--user", required=True, help="Postgres username")
    parser.add_argument("--password", required=True, help="Postgres password")
    parser.add_argument("--host", required=True, help="Postgres host")
    parser.add_argument("--port", required=True, help="Postgres port")
    parser.add_argument("--db", required=True, help="Postgres database name")
    parser.add_argument("--table_name", required=True, help="Target table name")

    # Parse the arguments and pass to main()
    args = parser.parse_args()
    main(args)
