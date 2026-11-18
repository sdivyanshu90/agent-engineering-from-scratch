"""D47-D48: SQLite owner/session revision journal and checkpoints."""
class Journal:
    def __init__(self,path): raise NotImplementedError
    def append(self,owner,session,expected_revision,kind,payload): raise NotImplementedError
    def checkpoint(self,owner,session,name,state,expected_revision): raise NotImplementedError
    def resume(self,owner,session,name): raise NotImplementedError
