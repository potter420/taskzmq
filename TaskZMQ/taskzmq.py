import zmq
from functools import wraps
import pickle
import joblib
import time

class TaskZMQ():
    
    def __init__(self):
        self.context = zmq.Context()
        self.taskdb = {}
        self.server = "tcp://127.0.0.1:5555"
        
    def create_socket(self, *arg):
        return self.context.socket(*arg)
    
    def task(self, fn):
        self.taskdb[fn.__name__] = fn
        @wraps(fn)
        def delayed(*arg,**kwarg):
            socket = self.create_socket(zmq.PUSH)
            socket.connect(self.server)
            task = {'task':fn.__name__, 'arg':arg, 'kwarg':kwarg}
            socket.send(pickle.dumps(task))
            socket.close()
            return task
        fn.delayed = delayed
        return fn
    
    def start_server(self):
        socket = self.create_socket(zmq.PULL)
        socket.bind(self.server)
        print('START SERVER @%s'%self.server)
        print('TASK LIST: ', ', '.join(self.taskdb.keys()))
        while True:
            try:
                message = socket.recv()
                msg = pickle.loads(message)
                a =  time.perf_counter()
                print('Executing: ', msg['task'])
                res = self.taskdb[msg['task']](*msg['arg'],**msg['kwarg'])
                print('Finished {task} in {time:.6f}s return: {res}'.format(task=msg['task'], time = time.perf_counter()-a, res = res) )
            except KeyboardInterrupt:
                print("W: interrupt received, stopping…")
                break
        socket.close()
        self.context.term()
        
