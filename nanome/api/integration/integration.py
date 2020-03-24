from nanome.util import Logs

class Integration():
    def __init__(self):
        self.hydrogen_add = None
        self.hydrogen_remove = None
        self.calculate_esp = None

    def _call(self, name, request):
        callback = getattr(self, name, None)
        if callback == None:
            Logs.warning("Integration", name, "called without being set by the plugin")
            return
        callback(request)
