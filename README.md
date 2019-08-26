# taskzmq
Simple task queue using Zero MQ


##How it works:

Client  ===> Server
zmq.PUSH ==> zmq.PULL

task is Serialized by pickles
