MAX_CLIENTS = 100

class ClientRegistry:

    def __init__(self):
        self._ids = set()

    def _es_id_valido(self, id):

        if not isinstance(id, str):
            return False
        
        if id.strip() == "":
            return False
        return True
    
    def add(self, id):
        if not self._es_id_valido(id):
            return False
        
        if MAX_CLIENTS is not None and len(self._ids) >= MAX_CLIENTS:
            return False
        
        id_normalizado = id.strip()
        if id_normalizado in self._ids:
            return False
        
        self._ids.add(id_normalizado)
        return True

    def remove(self, id):
        if not self._es_id_valido(id):
            return False
        
        id_normalizado = id.strip()
        if id_normalizado in self._ids:
            self._ids.discard(id_normalizado)
            return True
        return False
    
    def contains(self, id):
        if not self._es_id_valido(id):
            return False
        return (id.strip() in self._ids)
    
    def list(self):
        return list(self._ids)
    
    def size(self):
        return len(self._ids)
    
    def clear(self):
        self._ids.clear()

