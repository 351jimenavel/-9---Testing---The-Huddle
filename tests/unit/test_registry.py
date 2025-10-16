import pytest 
from chat.registry import ClientRegistry

# 1) Alta simple
def test_add_un_cliente_incrementa_tamanho():
    registro = ClientRegistry(100)
    ok = registro.add("c1")

    assert ok, "The variable 'ok' is not True"
    assert registro.contains("c1")
    assert registro.size() == 1

# 2) Alta duplicada (decisión: ignorar y retornar False)
def test_add_duplicado_no_incrementa_y_retorna_false():
    registro = ClientRegistry(100)
    registro.add("c1")
    ok_dup = registro.add("c1")

    assert not ok_dup
    assert registro.size() == 1

# 3) Baja idempotente (segunda vez retorna False, no explota)
def test_remove_idempotente():
    registro = ClientRegistry(100)
    registro.add("c1")
    ok1 = registro.remove("c1")
    ok2 = registro.remove("c1")

    assert ok1
    assert not ok2
    assert not registro.contains("c1")
    assert registro.size() == 0

# 4) Multiples clientes: consistencia tras altas y bajas
def test_multiple_altas_y_baja_intermedia():
    registro = ClientRegistry(100)
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

# 5. IDs invalidos (vacio, espacios, tipos no str)
def test_ids_invalidos_rechazados_en_add_y_contains():
    registro = ClientRegistry(100)

    for invalido in ["", "  ", None, 123, []]:
        assert not registro.add(invalido)
        assert not registro.contains(invalido)
    assert registro.size() == 0

# 6. Normalizacion de bordes (strip)
def test_ids_con_espacios_borde_se_normalizan():
    registro = ClientRegistry(100)
    registro.add("  c1  ")
    assert registro.contains("c1")
    assert registro.contains("  c1  ")
    assert registro.size() == 1

# 7. Clear deja el registro limpio
def test_clear_vacia_registro():
    registro = ClientRegistry(100)
    registro.add("c1")
    registro.add("c2")
    registro.clear()
    assert registro.size() == 0
    assert registro.list() == []

# 8. Limite de capacidad
def test_max_clients_limita_altas():
    # Simular MAX_CLIENTS = 2
    MAX_CLIENTS = 2
    registro = ClientRegistry(MAX_CLIENTS)


    assert registro.add("c1")
    assert registro.add("c2")
    assert not registro.add("c3")
    assert registro.size() == 2