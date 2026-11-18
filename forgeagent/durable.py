"""SQLite event journal and small workflow/checkpoint primitives (Week 8).

The journal provides local atomicity and optimistic revisions. It cannot make an
external side effect exactly once: a crash after the effect and before recording
its result leaves an operation pending/unknown and requires reconciliation.
"""
from dataclasses import dataclass
import hashlib
import json
import sqlite3
from contextlib import closing


class Conflict(ValueError): pass
class InvalidWorkflow(ValueError): pass


@dataclass(frozen=True)
class Step:
    identifier: str
    after: tuple[str,...]=()
    def __post_init__(self):
        if not isinstance(self.identifier,str) or not self.identifier:
            raise InvalidWorkflow("nonempty string step id required")
        if not isinstance(self.after,tuple) or any(not isinstance(x,str) or not x for x in self.after):
            raise InvalidWorkflow("dependencies must be a tuple of nonempty string IDs")
        if len(set(self.after))!=len(self.after): raise InvalidWorkflow("duplicate dependency")


def plan(steps):
    steps=list(steps)
    if any(not isinstance(s,Step) for s in steps): raise InvalidWorkflow("Step records required")
    ids=[s.identifier for s in steps]
    if len(set(ids)) != len(ids) or any(not i for i in ids): raise InvalidWorkflow("duplicate/empty step id")
    known=set(ids); done=set(); pending=list(steps); layers=[]
    if any(set(s.after)-known for s in steps): raise InvalidWorkflow("missing dependency")
    while pending:
        ready=[s for s in pending if set(s.after)<=done]
        if not ready: raise InvalidWorkflow("dependency cycle")
        ready.sort(key=lambda s:s.identifier); layers.append(tuple(ready));done.update(s.identifier for s in ready)
        pending=[s for s in pending if s not in ready]
    return tuple(layers)


def verify_plan(steps, layers):
    expected=plan(steps)
    if tuple(tuple(x) for x in layers)!=expected: raise InvalidWorkflow("plan does not match deterministic DAG")
    return True


def _json(value):
    try: return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError): raise ValueError("value must be finite JSON data") from None


class EventJournal:
    def __init__(self,path):
        self.path=str(path)
        if self.path==":memory:": raise ValueError("use a file-backed database")
        with closing(self._connect()) as c:
            c.executescript("""CREATE TABLE IF NOT EXISTS sessions(owner TEXT, session TEXT, revision INTEGER NOT NULL, PRIMARY KEY(owner,session));
            CREATE TABLE IF NOT EXISTS events(owner TEXT,session TEXT,revision INTEGER,kind TEXT,payload TEXT,PRIMARY KEY(owner,session,revision));
            CREATE TABLE IF NOT EXISTS checkpoints(owner TEXT,session TEXT,name TEXT,revision INTEGER,state TEXT,PRIMARY KEY(owner,session,name));
            CREATE TABLE IF NOT EXISTS operations(owner TEXT,session TEXT,op_id TEXT,digest TEXT,status TEXT,result TEXT,PRIMARY KEY(owner,session,op_id));""")
    def _connect(self): return sqlite3.connect(self.path,timeout=5,isolation_level=None)
    @staticmethod
    def _scope(owner,session):
        if not isinstance(owner,str) or not owner or not isinstance(session,str) or not session:
            raise ValueError("owner and session required")
    def revision(self,owner,session):
        self._scope(owner,session)
        with closing(self._connect()) as c:
            row=c.execute("SELECT revision FROM sessions WHERE owner=? AND session=?",(owner,session)).fetchone()
        return row[0] if row else 0
    def append(self,owner,session,expected_revision,kind,payload):
        self._scope(owner,session)
        if type(expected_revision) is not int or expected_revision<0: raise ValueError("nonnegative integer expected_revision required")
        if not isinstance(kind,str) or not kind or len(kind)>128: raise ValueError("event kind required")
        encoded=_json(payload)
        if len(encoded.encode())>65536: raise ValueError("event payload exceeds 64 KB")
        with closing(self._connect()) as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT revision FROM sessions WHERE owner=? AND session=?",(owner,session)).fetchone()
            current=row[0] if row else 0
            if current!=expected_revision: c.rollback();raise Conflict(f"expected {expected_revision}, found {current}")
            new=current+1
            c.execute("INSERT INTO sessions VALUES(?,?,?) ON CONFLICT(owner,session) DO UPDATE SET revision=excluded.revision",(owner,session,new))
            c.execute("INSERT INTO events VALUES(?,?,?,?,?)",(owner,session,new,kind,encoded));c.commit()
        return new
    def events(self,owner,session,after=0):
        self._scope(owner,session)
        if type(after) is not int or after<0: raise ValueError("nonnegative revision required")
        with closing(self._connect()) as c: rows=c.execute("SELECT revision,kind,payload FROM events WHERE owner=? AND session=? AND revision>? ORDER BY revision",(owner,session,after)).fetchall()
        return [{"revision":r,"kind":k,"payload":json.loads(p)} for r,k,p in rows]
    def checkpoint(self,owner,session,name,state,expected_revision):
        self._scope(owner,session)
        if not isinstance(name,str) or not name or len(name)>128: raise ValueError("checkpoint name must be 1..128 characters")
        if type(expected_revision) is not int or expected_revision<0: raise ValueError("nonnegative integer expected_revision required")
        encoded=_json(state)
        if len(encoded.encode())>1_000_000: raise ValueError("checkpoint exceeds 1 MB")
        with closing(self._connect()) as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT revision FROM sessions WHERE owner=? AND session=?",(owner,session)).fetchone()
            revision=row[0] if row else 0
            if revision!=expected_revision: c.rollback();raise Conflict(f"expected {expected_revision}, found {revision}")
            c.execute("INSERT INTO checkpoints VALUES(?,?,?,?,?) ON CONFLICT(owner,session,name) DO UPDATE SET revision=excluded.revision,state=excluded.state",(owner,session,name,revision,encoded));c.commit()
        return {"owner":owner,"session":session,"name":name,"revision":revision,"state":json.loads(encoded)}
    def resume(self,owner,session,name):
        self._scope(owner,session)
        if not isinstance(name,str) or not name or len(name)>128: raise ValueError("checkpoint name must be 1..128 characters")
        with closing(self._connect()) as c: row=c.execute("SELECT revision,state FROM checkpoints WHERE owner=? AND session=? AND name=?",(owner,session,name)).fetchone()
        if row is None: raise KeyError(name)
        return {"revision":row[0],"state":json.loads(row[1]),"events":self.events(owner,session,row[0])}
    def intent(self,owner,session,op_id,payload):
        self._scope(owner,session)
        if not isinstance(op_id,str) or not op_id or len(op_id)>128: raise ValueError("operation ID must be 1..128 characters")
        encoded=_json(payload)
        if len(encoded.encode())>65536: raise ValueError("operation payload exceeds 64 KB")
        digest=hashlib.sha256(encoded.encode()).hexdigest()
        with closing(self._connect()) as c:
            c.execute("BEGIN IMMEDIATE");row=c.execute("SELECT digest,status,result FROM operations WHERE owner=? AND session=? AND op_id=?",(owner,session,op_id)).fetchone()
            if row:
                c.rollback()
                if row[0]!=digest: raise Conflict("operation id bound to different intent")
                return {"digest":row[0],"status":row[1],"result":None if row[2] is None else json.loads(row[2]),"created":False}
            c.execute("INSERT INTO operations VALUES(?,?,?,?,?,NULL)",(owner,session,op_id,digest,"pending"));c.commit()
        return {"digest":digest,"status":"pending","result":None,"created":True}
    def resolve(self,owner,session,op_id,digest,*,result=None,unknown=False):
        self._scope(owner,session)
        if not isinstance(op_id,str) or not op_id or len(op_id)>128: raise ValueError("operation ID must be 1..128 characters")
        if not isinstance(digest,str) or len(digest)!=64: raise ValueError("SHA-256 digest required")
        if type(unknown) is not bool: raise ValueError("unknown must be bool")
        status="unknown" if unknown else "complete";encoded=None if unknown else _json(result)
        if encoded is not None and len(encoded.encode())>65536: raise ValueError("operation result exceeds 64 KB")
        with closing(self._connect()) as c:
            c.execute("BEGIN IMMEDIATE");row=c.execute("SELECT digest,status FROM operations WHERE owner=? AND session=? AND op_id=?",(owner,session,op_id)).fetchone()
            if row is None or row[0]!=digest: c.rollback();raise Conflict("unknown operation or digest mismatch")
            if row[1] in {"complete","unknown"}:
                previous=c.execute("SELECT result FROM operations WHERE owner=? AND session=? AND op_id=?",(owner,session,op_id)).fetchone()[0]
                if row[1]!=status or previous!=encoded:
                    c.rollback();raise Conflict("terminal operation receipt is immutable")
                c.rollback()
                return {"digest":digest,"status":status,"result":result if not unknown else None}
            c.execute("UPDATE operations SET status=?,result=? WHERE owner=? AND session=? AND op_id=?",(status,encoded,owner,session,op_id));c.commit()
        return {"digest":digest,"status":status,"result":result if not unknown else None}
    def operation(self,owner,session,op_id):
        self._scope(owner,session)
        with closing(self._connect()) as c: row=c.execute("SELECT digest,status,result FROM operations WHERE owner=? AND session=? AND op_id=?",(owner,session,op_id)).fetchone()
        if row is None: return None
        return {"digest":row[0],"status":row[1],"result":None if row[2] is None else json.loads(row[2])}
