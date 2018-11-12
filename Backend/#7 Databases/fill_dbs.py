import psycopg2
import pymongo
import csv


def fill_postgres():
    conn = psycopg2.connect(dbname='taxi_db', user='postgres', host='localhost', password=1)
    cursor = conn.cursor()

    cursor.execute('rollback;')

    cursor.execute("DROP TABLE IF EXISTS trip_data")
    cursor.execute("DROP TABLE IF EXISTS taxi_zone")

    cursor.execute(
        """
        CREATE TABLE taxi_zone (
        location_id  int UNIQUE,
        borough      char(50),
        zone         char(50),
        service_zone char(50));
        """)

    cursor.execute(
        """
        CREATE TABLE trip_data (
        VendorID                 int,
        tpep_pickup_datetime     timestamp,
        tpep_dropoff_datetime    timestamp,
        passenger_count          int,
        trip_distance            real,
        RatecodeID               int,
        store_and_fwd_flag       char,
        PULocationID             int references taxi_zone (location_id) ON DELETE CASCADE,
        DOLocationID             int references taxi_zone (location_id) ON DELETE CASCADE,
        payment_type             int,
        fare_amount              real,
        extra                    real,
        mta_tax                  real,
        tip_amount               real,
        tolls_amount             real,
        improvement_surcharge    real,
        total_amount             real);
        """)

    with open('taxi_zone.csv', 'r') as f:
        next(f)  # Skip the header row.
        cursor.copy_from(f, 'taxi_zone', sep=',')

    with open('tripdata.csv', 'r') as f:
        next(f)  # Skip the header row.
        print(f.readline())
        cursor.copy_from(f, 'trip_data', sep=',')

    # Быстро посмотреть количество строк в таблице
    # SELECT reltuples::bigint AS rows FROM pg_class where relname='trip_data';

    conn.commit()
    cursor.close()


def fill_mongodb():
    client = pymongo.MongoClient('localhost', 27017)
    taxi_db = client.taxi_db

    with open('taxi_zone.csv') as f:
        taxi_zones = csv.DictReader(f)
        for row in taxi_zones:
            taxi_db['taxi_zones'].insert_one(row)
            print(row)

    with open('tripdata.csv') as f:
        trip_data = csv.DictReader(f)
        for row in trip_data:
            taxi_db['trip_data'].insert_one(row)
            print(row)


if __name__ == '__main__':
    fill_postgres()
    fill_mongodb()
