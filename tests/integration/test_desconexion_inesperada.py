from _helpers import make_client, send_line, recv_line, close_client
import time

def test_disconnect_during_session(server_running):
    host, port, server = server_running
    A = make_client(host, port)
    B = make_client(host, port)
    C = make_client(host, port)

    # cerrar B abruptamente
    B.close()

    # Reintento hasta que registry refleje 2 conectados
    for _ in range(20):
        if server.registry.size() == 2:
            break
        time.sleep(0.05)

    assert server.registry.size() == 2

    # enviar mensaje y verificar que C lo recibe
    time.sleep(0.05)
    send_line(A, "Hola")
    assert recv_line(C, timeout=1.5) == "Hola"

    for s in (A, C):
        close_client(s)