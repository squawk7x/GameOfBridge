import selectors
import socket
import pickle
import Bridge

cardset = Bridge.Deck()
#bridge = Bridge.Bridge(3, True)
#cardset.show_blind()
blindstring = pickle.dumps(cardset)
#bridgestring = pickle.dumps(bridge)

sel = selectors.DefaultSelector()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    print('received', repr(data), 'from', conn)
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(blindstring)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


sock = socket.socket()
sock.bind(('localhost', 54321))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
