import threading
from queue import Queue
import time
import random

DISEASES = ('Боль', 'Жажда', 'Бессоница', 'Дедлайн')
DAY_TIME = 24
RITE_TIME = 2
IDENTIFY_DISEASE_TIME = 0.01


class Redneck:
    def __init__(self, id_):
        self._id = id_
        self._disease = None
        self._disease_time = None

    @property
    def id(self):
        return self._id

    @property
    def disease(self):
        return self._disease

    @disease.setter
    def disease(self, value):
        self._disease = value

    @disease.deleter
    def disease(self):
        self._disease = None

    def __del__(self):
        if self._disease:
            print(f'Мирный житель №{self.id} умер от болезни "{self.disease}"')


class TeamBuild:
    @classmethod
    def identify_healer(cls, infected_dude):
        """ Определяет болезнь, возвращает объект нужного знахаря."""
        time.sleep(IDENTIFY_DISEASE_TIME)
        if infected_dude.disease == 'Боль':
            return PainHealer
        elif infected_dude.disease == 'Жажда':
            return ThirstHealer
        elif infected_dude.disease == 'Бессоница':
            return InsomniaHealer
        elif infected_dude.disease == 'Дедлайн':
            return DeadlineHealer


class PainHealer:
    heal_queue = Queue()

    @classmethod
    def heal(cls, infected_dude):
        if infected_dude.disease == 'Боль':
            time.sleep(RITE_TIME)
            print(f'Исцеляю "{infected_dude.disease}"')
            infected_dude.disease = None
        else:
            print(f'Я не знаю как вылечить "{infected_dude.disease}"')


class ThirstHealer:
    heal_queue = Queue()

    @classmethod
    def heal(cls, infected_dude):
        if infected_dude.disease == 'Жажда':
            print(f'Исцеляю "{infected_dude.disease}"')
            time.sleep(RITE_TIME)
            infected_dude.disease = None
        else:
            print(f'Я не знаю как вылечить "{infected_dude.disease}"')


class InsomniaHealer:
    heal_queue = Queue()

    @classmethod
    def heal(cls, infected_dude):
        if infected_dude.disease == 'Бессоница':
            print(f'Исцеляю "{infected_dude.disease}"')
            time.sleep(RITE_TIME)
            infected_dude.disease = None
        else:
            print(f'Я не знаю как вылечить "{infected_dude.disease}"')


class DeadlineHealer:
    heal_queue = Queue()

    @classmethod
    def heal(cls, infected_dude):
        if infected_dude.disease == 'Дедлайн':
            print(f'Исцеляю "{infected_dude.disease}"')
            time.sleep(RITE_TIME)
            infected_dude.disease = None
        else:
            print(f'Я не знаю как вылечить "{infected_dude.disease}"')


class TeamBuildThread(threading.Thread):
    def __init__(self, infected_queue: Queue):
        super().__init__()
        self.infected_queue = infected_queue

    def run(self):
        while True:
            if self.infected_queue.empty():
                break
            else:
                infected_dude = self.infected_queue.get()
                healer = TeamBuild.identify_healer(infected_dude)
                healer.heal_queue.put(infected_dude)
                self.infected_queue.task_done()


class HealingThread(threading.Thread):
    def __init__(self, healer):
        super().__init__()
        self.healer = healer

    def run(self):
        while True:
            infected_dude = self.healer.heal_queue.get()
            self.healer.heal(infected_dude)
            HEALED_CITIZENS.append(infected_dude)
            self.healer.heal_queue.task_done()
            # !TODO: Исправить костыль
            if self.healer.heal_queue.empty():  # Иначе потоки не завершаются
                break


CITIZENS = [Redneck(x) for x in range(1, 31)]
INFECTED = Queue()
HEALED_CITIZENS = []


def infect_citizens(citizens: list, infected: Queue):
    for i in range(10):
        dude = random.choice(citizens)
        dude.disease = random.choice(DISEASES)
        citizens.remove(dude)
        infected.put(dude)


def main():
    infect_citizens(CITIZENS, INFECTED)

    teambuild = TeamBuildThread(INFECTED)

    pain_healer = HealingThread(PainHealer)
    thirst_healer = HealingThread(ThirstHealer)
    insomnia_healer = HealingThread(InsomniaHealer)
    deadline_healer = HealingThread(DeadlineHealer)

    teambuild.start()

    pain_healer.start()
    thirst_healer.start()
    insomnia_healer.start()
    deadline_healer.start()

    INFECTED.join()
    teambuild.join()

    pain_healer.join()
    thirst_healer.join()
    insomnia_healer.join()
    deadline_healer.join()

    print(HEALED_CITIZENS)


if __name__ == '__main__':
    main()
