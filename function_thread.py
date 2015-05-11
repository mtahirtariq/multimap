from threading import Thread


class FunctionThread(Thread):
    def __init__(self, function, *args):
        super(FunctionThread, self).__init__()
        self.function = function
        self.args = args
        self.response = None

    def run(self):
        self.response = self.function(*self.args)

