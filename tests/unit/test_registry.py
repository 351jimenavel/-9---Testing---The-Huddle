import pytest 
from chat.registry import ClientRegistry


def test_add_un_cliente_incrementa_tamanho():
    registro = ClientRegistry()
    ok = registro.add("c1")

    assert ok, "The variable 'ok' is not True"
    assert registro.contains("c1")
    assert registro.size() == 1

def test_add_duplicado_no_incrementa_y_retorna_false():
    registro = ClientRegistry()
    registro.add("c1")
    ok_dup = registro.add("c1")

    assert not ok_dup
    assert registro.size() == 1