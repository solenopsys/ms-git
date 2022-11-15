import time

import zmq
import struct

def test_send():
    print('START')
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    #socket.connect("tcp://localhost:5575")
    socket.connect("tcp://10.23.92.23:30007")
    context = zmq.Context()
    date_binary2 = '{"type":"repositoriesList","params":{"name":"bla"}}'.encode('ascii')
    print("RESULT2", send(socket, '{"type":"repositoryInit","params":{"name":"hcf-dgraph"}}'.encode('ascii')))


def send(socket,date_binary):

    buff = bytearray(8)
    struct.pack_into("L", buff, 0, 2212)
    struct.pack_into("H", buff, 4, 2)
    struct.pack_into("H", buff, 6, 1)
    print('subs %x', buff)
    print(date_binary)
    socket.send(buff + date_binary)
    print("wait")
    return socket.recv()



if __name__ == '__main__':
    test_send()

