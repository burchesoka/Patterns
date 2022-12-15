class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class Logger(metaclass=MetaSingleton):
    """ Single object e.g. database connection, logger etc. """


if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2
