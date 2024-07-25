class Mediator:
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'subscribers'):
            self.subscribers = {}

    def subscribe(self, event_name, callback):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    def publish(self, event_name, *args, **kwargs):
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                callback(*args, **kwargs)