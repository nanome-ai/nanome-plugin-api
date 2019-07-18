import nanome
from nanome._internal._macro._macro import _Macro

class Macro(_Macro):
    def __init__(self, title = "", description = "", logic = ""):
        self.title = title
        self.description = description
        self.logic = logic
        super(Macro, self).__init__()

    @property
    @classmethod
    def plugin_identifier(cls):
        return cls._plugin_identifier
    
    @plugin_identifier.setter
    @classmethod
    def plugin_identifier(cls, value):
        cls._plugin_identifier = value

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value

    @property
    def logic(self):
        return self._logic
    
    @logic.setter
    def logic(self, value):
        self._logic = value

    def save(self, all_users = False):
        self._save(all_users)

    def run(self):
        self._run()

    def delete(self, all_users = False):
        self._delete(all_users)

    @classmethod
    def stop(cls):
        cls._stop()
    
    @classmethod
    def get_live(cls, callback):
        return cls._get_live(callback)


_Macro._create = Macro