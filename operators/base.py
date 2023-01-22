from abc import ABCMeta, abstractmethod


class BaseOperator(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self):
        pass
