from time import time
import psycopg2
import pymongo

"""
ЗАПРОСЫ
0. получение списка поездок, которые произошли в указанном промежутке
1. постраничный вывод данных о поездках
2. вывести список зон с количеством начал и окончаний поездок в этой зоне
3. вывести среднее количество поездок по часам
4. вывести среднее количество поездок по дням недели
5. вывести распределение поездок по типам оплаты
Для каждого запроса посчитать время выполнения и записать в сводную таблицу.
"""

conn = psycopg2.connect(dbname='taxi_db', user='postgres', host='localhost', password=1)
cursor = conn.cursor()


def benchmark(func):
    """Подсчет производительности компонентов"""

    def wrapper(*args, **kwargs):
        t = time()
        res = func(*args, **kwargs)
        print(func.__name__, time() - t)
        return res

    return wrapper


query1 = """
            SELECT *
            FROM trip_data
            WHERE 
                trip_data.tpep_pickup_datetime 
                BETWEEN '2018-01-01 00:00:00.000000' AND 
                '2018-01-01 02:00:00.000000'
            AND trip_data.tpep_dropoff_datetime 
                BETWEEN '2018-01-01 00:00:00.000000' AND 
                '2018-01-01 02:00:00.000000'
         """

query2 = "SELECT * FROM trip_data LIMIT 20 OFFSET 10"

query3 = """
            SELECT StartTrips.zone, StartRides, EndRides
            FROM (SELECT DISTINCT taxi_zone.zone, 
                    COUNT(trip_data.pulocationid) AS StartRides
                  FROM taxi_zone,
                       trip_data
                  WHERE trip_data.pulocationid = taxi_zone.location_id
                  GROUP BY taxi_zone.zone
                  ORDER BY StartRides DESC) as StartTrips,
            
                 (SELECT DISTINCT taxi_zone.zone, 
                    COUNT(trip_data.dolocationid) AS EndRides
                  FROM taxi_zone,
                       trip_data
                  WHERE trip_data.dolocationid = taxi_zone.location_id
                  GROUP BY taxi_zone.zone
                  ORDER BY EndRides DESC) as EndTrips
            WHERE StartTrips.zone = EndTrips.zone
         """

query4 = """
            SELECT h.hour, COUNT(*) as current_hour_trips,
                   sum(count(*)*1.0) over() as total_trips,
                   cast(count(*)/(sum(count(*)*1.0) over()) * 100 as decimal(6, 1)) as avg
            FROM (SELECT (23 - offs) AS hour
                  FROM generate_series(0, 23, 1) AS offs) h
                   LEFT OUTER JOIN trip_data td
                     ON h.hour = date_part('hour', td.tpep_pickup_datetime)
            GROUP BY h.hour
            ORDER BY avg
         """

query5 = """
             SELECT to_char(trip_data.tpep_pickup_datetime, 'DAY') AS DayGroup,
                COUNT(*) as total_trips,
                cast(count(*) / (sum(count(*) * 1.0) over ()) * 100 as decimal(6, 1)) as avg
             FROM trip_data
             GROUP BY DayGroup
             ORDER BY avg
         """

query6 = """
             SELECT trip_data.payment_type, COUNT(*)
             FROM trip_data
             GROUP BY trip_data.payment_type
         """

queries = (query1, query2, query3, query4, query5, query6)


@benchmark
def execute_query(query_):
    cursor.execute(query_)


for i, query in enumerate(queries):
    execute_query(query)
    print(i)

conn.close()

""" 
Результаты
0. execute_query 0.4045290946960449
1. execute_query 0.0013396739959716797
2. execute_query 2.4090802669525146
3. execute_query 7.0151917934417725
4. execute_query 2.9786691665649414
5. execute_query 1.2459440231323242
"""
