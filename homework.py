from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    # MESSAGE - универсальная константа типа str для метода get_message
    # для вывода сообщения с использованием метода
    # .format и позиционными аргументами:
    MESSAGE: str = (
                    'Тип тренировки: {0}; '
                    'Длительность: {1} ч.; '
                    'Дистанция: {2} км; '
                    'Ср. скорость: {3} км/ч; '
                    'Потрачено ккал: {4}.'
                   )

    def get_message(self) -> str:
        # Возвращает MESSAGE c использованием метода .format
        # с подставленными позиционными аргументами и форматированием
        # числовых значений до трех знаков после запятой.
        # Lля единообразия заменил форматирование до трех знаков
        # после запятой при помощи f-строк на метод .format
        return self.MESSAGE.format(
                                   self.training_type,
                                   "{:.3f}".format(self.duration),
                                   "{:.3f}".format(self.distance),
                                   "{:.3f}".format(self.speed),
                                   "{:.3f}".format(self.calories)
                                  )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    DUR_IN_M: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * self.duration * self.DUR_IN_M)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_EXPON: float = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.weight +
                (self.get_mean_speed() ** self.COEFF_EXPON // self.height)
                * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.DUR_IN_M)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    code_classes: dict[str, Training] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking}
    try:
        return code_classes[workout_type](*data)
    except KeyError:
        print('Код тренировки не найден. Исполнение программы остановлено')
        quit()
        # здесь, на мой взгляд нужна остановка программы,
        # так как без принудительного выхода функция show_training_info будет
        # ждать атрибут


def main(training: Training) -> None:
    """Главная функция."""
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
