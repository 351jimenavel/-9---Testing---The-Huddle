import pytest 
from chat.registry import ClientRegistry


def test_add_un_cliente_incrementa_tamanho():
    registro = ClientRegistry()
    ok = registro.add("c1")

    assert ok, "The variable 'ok' is not True"
    assert registro.contains("c1")
    assert registro.size() == 1

# 2) Alta duplicada (decisión: ignorar y retornar False)
def test_add_duplicado_no_incrementa_y_retorna_false():
    registro = ClientRegistry()
    registro.add("c1")
    ok_dup = registro.add("c1")

    assert not ok_dup
    assert registro.size() == 1

# 3) Baja idempotente (segunda vez retorna False, no explota)
def test_remove_idempotente():
    registro = ClientRegistry()
    registro.add("c1")
    ok1 = registro.remove("c1")
    ok2 = registro.remove("c1")

    assert ok1
    assert not ok2
    assert not registro.contains("c1")
    assert registro.size() == 0

# 4) Multiples clientes: consistencia tras altas y bajas
def test_multiple_altas_y_baja_intermedia():
    registro = ClientRegistry()
    registro.add("c1")
    registro.add("c2")
    registro.add("c3")

    assert registro.size() == 3
    registro.remove("c2")
    lista = registro.list()

    assert "c1" in lista
    assert "c3" in lista
    assert "c2" not in lista
    assert registro.size() == 2