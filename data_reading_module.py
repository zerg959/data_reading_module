from dataclasses import dataclass


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    MIN_IN_HOUR = 60.0

    action: int
    duration: float
    weight: float

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    RUN_KF_1: int = 18
    RUN_KF_2: float = 20
    MIN_IN_HOUR: int = 60

    def get_spent_calories(self):
        return ((self.RUN_KF_1 * self.get_mean_speed() - self.RUN_KF_2) *
                self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    height: float

    WLK_KF_1: float = 0.035
    WLK_KF_2: float = 0.029

    def get_spent_calories(self):
        return (
                (self.WLK_KF_1 * self.weight +
                 (self.get_mean_speed() ** 2 // self.height)
                 * self.WLK_KF_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    length_pool: float
    count_pool: int

    LEN_STEP: float = 1.38
    SWIM_KF_1: float = 1.1
    SWIM_KF_2: int = 2

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool /
                self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SWIM_KF_1) * self.SWIM_KF_2 *
                self.weight)


def read_package(workout_type, data):
    workout_types = {
        'SWM': Swimming,
        'WLK': SportsWalking,
        'RUN': Running
    }
    if workout_type in workout_types:
        try:
            return workout_types[workout_type](*data)
        except ValueError:
            return 'Unknown workout'


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
