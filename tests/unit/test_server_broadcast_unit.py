
from unittest.mock import Mock
from chat.refact_server import Server

def test_broadcast_no_echo_unit():
    srv = Server("127.0.0.1", 0)
    a, b, c = Mock(), Mock(), Mock()
    # Inyectamos sockets falsos
    srv.sockets_por_id = {"A": a, "B": b, "C": c}

    srv.broadcast(from_id="A", text="Ping")

    a.sendall.assert_not_called()            # no eco. Verifica que no se lo haya llamado.
    b.sendall.assert_called_once()          # Verifica que se haya llamado exactamente una vez
    c.sendall.assert_called_once()
    
    args, _ = b.sendall.call_args   # ultimos argumentos usados.
    assert args[0] == b"Ping\n"
