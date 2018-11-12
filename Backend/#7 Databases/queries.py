import psycopg2
import pymongo

"""
ЗАПРОСЫ
получение списка поездок, которые произошли в указанном промежутке
постраничный вывод данных о поездках
вывести список зон с количеством начал и окончаний поездок в этой зоне
вывести среднее количество поездок по часам
вывести среднее количество поездок по дням недели
вывести распределение поездок по типам оплаты
Для каждого запроса посчитать время выполнения и записать в сводную таблицу.
"""

query1 = """
            SELECT *
            FROM trip_data
            WHERE trip_data.tpep_pickup_datetime 
                BETWEEN '2018-01-01 00:00:00.000000' AND '2018-01-01 02:00:00.000000'
            AND trip_data.tpep_dropoff_datetime 
                BETWEEN '2018-01-01 00:00:00.000000' AND '2018-01-01 02:00:00.000000'
         """

query2 = f"SELECT * FROM trip_data LIMIT 20 OFFSET {i}"

query3 = """
            SELECT StartTrips.zone, StartRides, EndRides
            FROM (SELECT DISTINCT taxi_zone.zone, COUNT(trip_data.pulocationid) AS StartRides
                  FROM taxi_zone,
                       trip_data
                  WHERE trip_data.pulocationid = taxi_zone.location_id
                  GROUP BY taxi_zone.zone
                  ORDER BY StartRides DESC) as StartTrips,
            
                 (SELECT DISTINCT taxi_zone.zone, COUNT(trip_data.dolocationid) AS EndRides
                  FROM taxi_zone,
                       trip_data
                  WHERE trip_data.dolocationid = taxi_zone.location_id
                  GROUP BY taxi_zone.zone
                  ORDER BY EndRides DESC) as EndTrips
            WHERE StartTrips.zone =EndTrips.zone

         """
