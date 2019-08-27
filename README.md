# taskzmq
Simple task queue using Zero MQ

## Why I make this:
- Want some light weight task queue to work on Windows without Redis/RabbitMQ combination
- Huey example just doesn't work on Windows :(
- Corporate policies force me to use Windows

## How it works:

                 Task
    Client   ===========> Server
    zmq.PUSH -----------> zmq.PULL
- Client send task to server by sending messages through zmq
- task is Serialized by pickles/cloudpickles
- Result backend -- To be added
- Server can do the work itself or call for joblib/ other subprocess management that is suitable for windows.

## Example:
Server Definitions <br/>
tasks.py 
```python
from TaskZMQ import TaskZMQ
tasks = TaskZMQ()

@tasks.task
def do_some_thing(n):
    return n+1

if __name__ == '__main__':
    tasks.run_server()
```
Run the server: python tasks.py <br/>
From interactive console or others execution method:
```python
from tasks import do_some_thing
# Execute do_some_thing
do_some_thing(10)
# Make server do the works:
do_some_thing.delayed(10)
```

