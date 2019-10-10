


class DataObjStateEnum():
    def __init__(self):
        pass # // AA: not implemented

class DataObj():
    def __init__(self):
        self.handle = None
        self.text = None
        self.coordinates = None
        self.location = None
        #self.id = None

        # // AA: Twitter obj entities might be worth looking into

        self.possible_states = None # // AA: not implemented
        self.state = "Empty"