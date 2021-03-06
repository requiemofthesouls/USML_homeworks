#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import randint
import sys

CAR_SPECS = {
    'ferrary': {"max_speed": 340, "drag_coef": 0.324, "time_to_max": 26},
    'bugatti': {"max_speed": 407, "drag_coef": 0.39, "time_to_max": 32},
    'toyota': {"max_speed": 180, "drag_coef": 0.25, "time_to_max": 40},
    'lada': {"max_speed": 180, "drag_coef": 0.32, "time_to_max": 56},
    'sx4': {"max_speed": 180, "drag_coef": 0.33, "time_to_max": 44},
}


class Car:
    def __init__(self, model, specs):
        self.__model = model
        self.__specs = specs
        self.__time = None
        self.__distance = None

    def get_model(self):
        return self.__model

    def get_specs(self):
        return self.__specs

    def get_result_time(self):
        return self.__time

    def get_result_distance(self):
        return self.__distance

    def set_result(self, time, distance):
        self.__time = time
        self.__distance = distance


class Weather:
    """ Можно попробовать применить шаблон Observer
    Наблюдатель будет уведомлять о изменении погоды """

    def __init__(self, wind_speed=20):
        self.__wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self.__wind_speed)


class Competition:  # Singleton and chain of responsobillity patterns
    instance = None

    def __new__(cls, arg):
        if cls.instance is None:
            cls.instance = super(Competition, cls).__new__(cls)
        return cls.instance

    def __init__(self, distance=10000):
        self.__distance = distance

    def start(self, competitors, weather):
        for competitor_name in competitors:
            competitor_time = 0
            car = competitor_name.get_specs()

            for distance in range(self.__distance):
                _wind_speed = weather.get_wind_speed()

                if competitor_time == 0:
                    _speed = 1
                else:
                    _speed = (competitor_time /
                              car["time_to_max"]) * car['max_speed']
                    if _speed > _wind_speed:
                        _speed -= (car['drag_coef'] * _wind_speed)

                competitor_time += float(1) / _speed
            if competitor_name.get_result_time():
                print(f'Car <{competitor_name.get_model()}> '
                      f'previous result: {competitor_name.get_result_time()}, distance {competitor_name.get_result_distance()}m')
                competitor_name.set_result(competitor_time, self.__distance)
            else:
                competitor_name.set_result(competitor_time, self.__distance)
            print(f'Car <{competitor_name.get_model()}> result: {competitor_time}, distance {self.__distance}m')


class CompetitionGiver:
    """ Цепочка обязанностей """

    def __init__(self):
        super(CompetitionGiver, self).__init__()
        self.__competitors = []

    def add_competitors(self, competitor):
        self.__competitors.append(competitor)

    def get_competitors(self):
        return self.__competitors

    def handle_competition(self):
        competition.start(self.get_competitors(), weather)


competition = Competition(10000)
weather = Weather()

ferrary = Car('ferrary', CAR_SPECS['ferrary'])
bugatti = Car('bugatti', CAR_SPECS['bugatti'])
toyota = Car('toyota', CAR_SPECS['toyota'])
lada = Car('lada', CAR_SPECS['lada'])
sx4 = Car('sx4', CAR_SPECS['sx4'])


competitors = (ferrary, bugatti, toyota, lada, sx4)
competition_giver = CompetitionGiver()

for competitor in competitors:
    competition_giver.add_competitors(competitor)

print(competition_giver.handle_competition())
competition = Competition(5000)
print(competition_giver.handle_competition())
