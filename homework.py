from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: ClassVar[int] = 60
    """Базовый класс тренировки."""

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод реализован в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79
    MIN_IN_HOUR: ClassVar[int] = 60
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    height: float
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100
    MIN_IN_H: ClassVar[int] = 60
    CONST_DEGREE: ClassVar[int] = 2
    """Тренировка: спортивная ходьба."""

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (((self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** self.CONST_DEGREE)
                    / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    length_pool: int
    count_pool: int
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 1.38
    COEFFICIENT_3: ClassVar[float] = 1.1
    COEFFICIENT_4: ClassVar[int] = 2
    """Тренировка: плавание."""

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        COEFFICIENT_3 = 1.1
        COEFFICIENT_4 = 2
        return ((self.get_mean_speed() + COEFFICIENT_3)
                * COEFFICIENT_4 * self.weight * self.duration)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    read_workout: dict[str, type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
    type_training = read_workout.get(workout_type, None)
    if not type_training:
        raise NameError
    return type_training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
