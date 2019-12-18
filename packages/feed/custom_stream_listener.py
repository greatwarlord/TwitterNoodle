from tweepy import StreamListener 



class CustomStreamListener(StreamListener):

    def __init__(self, _destination, _stream_toggle, _warn_verbosity):
        super(CustomStreamListener,self).__init__()
        self.destination = _destination
        self.stream_toggle = _stream_toggle
        self.warn_verbosity = _warn_verbosity

    def on_status(self, status):
        self.destination.append(status) if self.stream_toggle else self.out_warn("Stream OFF")

    def on_error(self, status_code):
        # // AA: 420 is the error code when a rate limit is reached
        if status_code == 420: 
            self.out_warn("Recieved rate limit warning, stopping stream")
            self.stream_toggle = False
            return False
        else:
            self.out_warn(f"misc error: {status_code}")

    def out_warn(self, msg):
        print(msg) if not self.warn_verbosity else ...





