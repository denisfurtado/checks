from time import sleep

class StatusBar:
    def __init__(self):
        self.step_count = 0
        self.size = 30
    
    def do_step(self, msg):
        msg = f'# {self.step_count} {msg}'
        self.step_count += 1
        self.size = max(self.size, len(msg))
        msg = msg.ljust(self.size)
        print(msg, end='\r')
    
    def end_step(self, msg):
        pass

BAR = StatusBar()

def step(name):
    def named_step(func):
        def wrapper(*args, **kwargs):
            BAR.do_step(name)
            result =  func(*args, **kwargs)
            BAR.end_step(name)
            return result
            
        return wrapper
    return named_step

