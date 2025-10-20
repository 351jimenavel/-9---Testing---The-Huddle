from _helpers import make_client, send_line, recv_line
import pytest
import time

def test_broadcast(server_running):
    host, port, server = server_running

    a = make_client(host, port)
    b = make_client(host, port)
    c = make_client(host, port)

    # (Opcional) mini reintento hasta ver 3 conectados, por concurrencia
    for _ in range(20):
        if server.registry.size() == 3:
            break
        time.sleep(0.01)

    # A envia 
    send_line(a, "PING")

    # B y c deben recibir exactamente "PING"
    assert recv_line(b) == "PING"
    assert recv_line(c) == "PING"

    # A no recibe su propio mensaje
    assert recv_line(a) is None

    # Limpieza
    for s in (a, b, c):
        try:
            import socket as _s
            try: s.shutdown(_s.SHUT_RDWR)
            except OSError: pass
        finally:
            s.close()