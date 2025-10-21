from _helpers import make_client, close_client
import time

'''
Verifica que varios clientes pueden conectarse al servidor
Que el registry refleje la cantidad correcta de conexiones
Que las desconexiones se detecten y limpien correctamente
'''


def test_multiple_clients_connect_and_disconnect(server_running):
    host, port, server = server_running

    a = make_client(host, port)
    b = make_client(host, port)

    # mini reintento para dar tiempo al accept_loop
    for _ in range(20):               # ~200ms
        if server.registry.size() == 2:
            break
        time.sleep(0.01)

    assert server.registry.size() == 2

    # Cerrar b
    try:
        import socket as _s
        try:
            b.shutdown(_s.SHUT_RDWR)
        except OSError:
            pass
        b.close()
    finally:
        pass

    # mini reintento: el server necesita un tick para limpiar
    for _ in range(20):
        if server.registry.size() == 1:
            break
        time.sleep(0.01)
    assert server.registry.size() == 1

    # cerrar a
    close_client(a)
    