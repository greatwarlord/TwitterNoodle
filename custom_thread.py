import threading



class CustomThread (threading.Thread):
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