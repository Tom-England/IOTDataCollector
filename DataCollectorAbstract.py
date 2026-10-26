from abc import ABC, abstractmethod

class DataCollectorAbstract(ABC):
    @abstractmethod
    def Collect(self):
        pass
    
    @abstractmethod
    def Process(self):
        pass