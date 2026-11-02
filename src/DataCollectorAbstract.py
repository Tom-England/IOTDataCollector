from abc import ABC, abstractmethod

class DataCollectorAbstract(ABC):
    @abstractmethod
    def collect(self):
        pass
    
    @abstractmethod
    def process(self):
        pass
    
    def collect_then_process(self):
        data = self.collect()
        self.process(data)

    @abstractmethod
    def flush(self):
        pass