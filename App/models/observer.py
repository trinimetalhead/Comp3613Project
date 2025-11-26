from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, subject, event_type, **kwargs):
        pass


# Subject is a plain mixin (do not inherit from ABC) so it can be
# combined with SQLAlchemy declarative models without metaclass conflicts.
class Subject:
    # Global observers receive notifications from all subjects
    _global_observers: List[Observer] = []

    @classmethod
    def attach_global(cls, observer: Observer):
        if observer not in cls._global_observers:
            cls._global_observers.append(observer)

    @classmethod
    def detach_global(cls, observer: Observer):
        if observer in cls._global_observers:
            cls._global_observers.remove(observer)

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type, **kwargs):
        # Notify instance observers
        for obs in list(self._observers):
            try:
                obs.update(self, event_type, **kwargs)
            except Exception:
                # swallow observer errors to avoid breaking business logic
                pass

        # Notify global observers
        for obs in list(self.__class__._global_observers):
            try:
                obs.update(self, event_type, **kwargs)
            except Exception:
                pass
