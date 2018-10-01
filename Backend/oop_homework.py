from random import randint

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

    def get_model(self):
        return self.__model

    def get_specs(self):
        return self.__specs


class Weather:
    def __init__(self, wind_speed=20):
        self.__wind_speed = wind_speed

    def get_wind_speed(self):
        return randint(0, self.__wind_speed)


class Competition:
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

            print ("Car <%s> result: %f" % (competitor_name.get_model(), competitor_time))


competition = Competition()
weather = Weather()

ferrary = Car('ferrary', CAR_SPECS['ferrary'])
bugatti = Car('bugatti', CAR_SPECS['bugatti'])
toyota = Car('toyota', CAR_SPECS['toyota'])
lada = Car('lada', CAR_SPECS['lada'])
sx4 = Car('sx4', CAR_SPECS['sx4'])

competitors = (ferrary, bugatti, toyota, lada, sx4)
competition.start(competitors, weather)


