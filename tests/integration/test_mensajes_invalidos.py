from _helpers import make_client, send_line, recv_line, close_client
import time

def test_invalid_messages_not_broadcast(server_running):
    host, port, server = server_running
    A = make_client(host, port)
    B = make_client(host, port)

    invalidos = ["", " ", "a"*51, "hola\r", "\t hola"]

    for msg in invalidos:
        send_line(A, msg)
        assert recv_line(B) is None # No llega nada a B

    close_client(A)
    close_client(B)