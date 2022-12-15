class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        print(cls._instances)
        return cls._instances[cls]


class Logger(metaclass=MetaSingleton):
    """  """


if __name__ == "__main__":
    logger1 = Logger()
    logger2 = Logger()
    print(logger1 is logger2)







#
#
# class MetaSingleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class Logger(metaclass=MetaSingleton):
#     pass
#
#
# logger1 = Logger()
# logger2 = Logger()
#
# print(logger1 is logger2)
