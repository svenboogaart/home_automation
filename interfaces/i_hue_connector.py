from abc import ABCMeta, abstractmethod


class IHueConnector(metaclass=ABCMeta):

    @abstractmethod
    def run_put_request(self, path, data):
        pass

    @abstractmethod
    def run_get_request(self, path):
        pass
