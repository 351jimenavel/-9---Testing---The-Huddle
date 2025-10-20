from _helpers import make_client, send_line, recv_line, close_client

def test_order_preserved(server_running):
    host, port, server = server_running

    a = make_client(host, port)
    b = make_client(host, port)

    send_line(a, "m1")
    send_line(a, "m2")
    send_line(a, "m3")

    assert recv_line(b) == "m1"
    assert recv_line(b) == "m2"
    assert recv_line(b) == "m3"

    # Limpieza
    for s in (a, b):
        close_client(s)