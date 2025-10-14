from db import DataBase
import pytest

@pytest.fixture # Setup step, will give a fresh data/instance before running tests
def db():
    ''' Provides a fresh instance of the DataBase class before each tes and cleans up after the testt'''
    database = DataBase()
    yield database  # provide the fixture instance
    database.data.clear()   # cleanup step (not needed for in-memory, but useful for real DBs)

def test_add_user(db):
    db.add_user(1, "Alice")
    assert db.get_user(1) == "Alice"

def test_add_duplicate_user(db):
    db.add_user(1, "Alice")
    with pytest.raises(ValueError, match="User already exists"):
        db.add_user(1, "Bob")

def test_delete_user(db):
    db.add_user(2, "Alice")
    db.delete_user(2)
    assert db.get_user(2) is None