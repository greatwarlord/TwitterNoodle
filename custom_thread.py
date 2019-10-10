import threading



class CustomThread (threading.Thread):

        def __init__(self):
            super(CustomThread, self).__init__()
            self._stop_event = threading.Event()

        def custom_setup(self, _task, _is_looped):
            self.task = _task
            self.is_looped = _is_looped
            #self.daemon = True

        def run (self):
                if self.is_looped:
                    while True:
                        self.task()
                else:
                    self.task()

        def stop(self):
            self._stop_event.set()

        def stopped(self):
            return self._stop_event.is_set()