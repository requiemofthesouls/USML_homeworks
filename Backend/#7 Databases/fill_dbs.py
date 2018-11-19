from datetime import datetime
from time import time
import psycopg2
import pymongo
import csv

__data__ = 'http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml'


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
    t = time()
    client = pymongo.MongoClient('localhost', 27017)
    taxi_db = client.taxi_db

    with open('taxi_zone.csv') as f:
        taxi_zones = csv.DictReader(f)
        for row in taxi_zones:
            row['LocationID'] = int(row['LocationID'])
            taxi_db['taxi_zones'].insert_one(row)
            print(row)

    with open('tripdata.csv') as f:
        trip_data = csv.DictReader(f)
        for row in trip_data:
            # TODO: Marshmallow
            row['VendorID'] = int(row['VendorID'])
            row['tpep_pickup_datetime'] = \
                datetime.strptime(row['tpep_pickup_datetime'], '%Y-%m-%d %H:%M:%S')
            row['tpep_dropoff_datetime'] = \
                datetime.strptime(row['tpep_dropoff_datetime'], '%Y-%m-%d %H:%M:%S')
            row['passenger_count'] = int(row['passenger_count'])
            row['trip_distance'] = float(row['trip_distance'])
            row['RatecodeID'] = int(row['RatecodeID'])
            row['PULocationID'] = int(row['PULocationID'])
            row['DOLocationID'] = int(row['DOLocationID'])
            row['payment_type'] = int(row['payment_type'])
            row['payment_type'] = int(row['payment_type'])
            row['fare_amount'] = float(row['fare_amount'])
            row['extra'] = float(row['extra'])
            row['mta_tax'] = float(row['mta_tax'])
            row['tip_amount'] = float(row['tip_amount'])
            row['tolls_amount'] = float(row['tolls_amount'])
            row['improvement_surcharge'] = float(row['improvement_surcharge'])
            row['total_amount'] = float(row['total_amount'])

            taxi_db['trip_data'].insert_one(row)
            print(row)
    print(f'Total fill time {time() - t}s')  # Total fill time 3224.3s (53.7 minutes)


if __name__ == '__main__':
    # fill_postgres()
    fill_mongodb()
