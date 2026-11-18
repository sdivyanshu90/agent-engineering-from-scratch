"""Owned-workspace policy; not a race-proof OS sandbox."""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import stat
import tempfile
import threading

class PolicyDenied(ValueError): pass

def _digest(data): return hashlib.sha256(data).hexdigest()
def _canonical_args(value):
    if not isinstance(value,dict): raise PolicyDenied('arguments must be an object')
    try: encoded=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError,RecursionError) as error: raise PolicyDenied('arguments must be JSON data') from error
    if len(encoded.encode())>8192: raise PolicyDenied('arguments too large')
    return encoded

class Workspace:
    """Guard ordinary owned workspace use; hostile concurrent writers need OS isolation."""
    MAX_FILE_BYTES=65536
    _DENIED_PARTS={'.git','.aws','.codex','.agents','.venv','.ssh','__pycache__'}
    _PRIVATE_NAMES={'id_rsa','id_ed25519','id_ecdsa','id_dsa','private_key','credentials'}
    _PRIVATE_SUFFIXES={'.pem','.key','.p12','.pfx','.keystore'}
    def __init__(self,root):
        self.root=Path(root).resolve(strict=True)
        if not self.root.is_dir(): raise ValueError('workspace must be a directory')
        self._proposals={};self._lock=threading.RLock()

    def _path(self,relative,*,must_exist=False):
        if not isinstance(relative,str) or not relative or '\\' in relative or '\x00' in relative: raise PolicyDenied('invalid relative path')
        rel=PurePosixPath(relative)
        if rel.is_absolute() or any(part in ('..','.') for part in rel.parts): raise PolicyDenied('path traversal')
        lowered=[p.lower() for p in rel.parts]
        name=lowered[-1] if lowered else ''
        if any(p in self._DENIED_PARTS for p in lowered) or name.startswith('.env') or name in self._PRIVATE_NAMES or Path(name).suffix in self._PRIVATE_SUFFIXES:
            raise PolicyDenied('sensitive path denied')
        current=self.root
        for part in rel.parts:
            current=current/part
            if current.is_symlink(): raise PolicyDenied('symbolic link rejected')
        resolved=current.resolve(strict=must_exist)
        if resolved!=self.root and self.root not in resolved.parents: raise PolicyDenied('path escape')
        return resolved

    @staticmethod
    def _bounded_bytes(path,limit):
        if type(limit) is not int or not 1<=limit<=Workspace.MAX_FILE_BYTES: raise PolicyDenied('invalid byte limit')
        with path.open('rb') as stream: data=stream.read(limit+1)
        if len(data)>limit: raise PolicyDenied('file too large')
        return data

    def read_text(self,relative,max_bytes=MAX_FILE_BYTES):
        path=self._path(relative,must_exist=True)
        if not path.is_file(): raise PolicyDenied('regular file required')
        return self._bounded_bytes(path,max_bytes).decode('utf-8')

    def propose_patch(self,relative,expected_sha256,replacement_text,*,session_id,tool_name,arguments):
        path=self._path(relative,must_exist=True)
        if not path.is_file() or not isinstance(replacement_text,str): raise PolicyDenied('regular file and text replacement required')
        replacement=replacement_text.encode('utf-8')
        if len(replacement)>self.MAX_FILE_BYTES: raise PolicyDenied('patch too large')
        old=self._bounded_bytes(path,self.MAX_FILE_BYTES)
        if not isinstance(expected_sha256,str) or _digest(old)!=expected_sha256: raise PolicyDenied('stale content hash')
        if not all(isinstance(x,str) and x for x in (session_id,tool_name)): raise PolicyDenied('approval identity')
        args_json=_canonical_args(arguments); frozen_args=json.loads(args_json)
        binding={'session':session_id,'tool':tool_name,'arguments':frozen_args,'arguments_canonical':args_json,'path':relative,'revision':expected_sha256,'replacement':_digest(replacement)}
        proposal={'id':secrets.token_urlsafe(18),'binding':binding,'replacement':replacement_text}
        self._proposals[proposal['id']]={'proposal':proposal,'approved':False,'used':False}
        return {'proposal_id':proposal['id'],'path':relative,'before_sha256':expected_sha256,'after_sha256':binding['replacement']}

    def export_proposal(self,proposal_id):
        """JSON-safe trusted-host receipt. No approval state is exported."""
        item=self._proposals.get(proposal_id)
        if not item or item['used']: raise PolicyDenied('unknown or consumed proposal')
        p=item['proposal'];return {'id':p['id'],'binding':dict(p['binding']),'replacement':p['replacement']}

    def restore_proposal(self,receipt):
        """Restore host-journal proposal as unapproved; human review must repeat."""
        if not isinstance(receipt,dict) or set(receipt)!={'id','binding','replacement'}: raise PolicyDenied('invalid proposal receipt')
        identifier,binding,replacement=receipt['id'],receipt['binding'],receipt['replacement']
        required={'session','tool','arguments','arguments_canonical','path','revision','replacement'}
        if not isinstance(identifier,str) or not identifier or identifier in self._proposals: raise PolicyDenied('invalid or duplicate proposal id')
        if not isinstance(binding,dict) or set(binding)!=required or not isinstance(replacement,str): raise PolicyDenied('invalid proposal binding')
        if not all(isinstance(binding[k],str) and binding[k] for k in ('session','tool','path','revision','replacement','arguments_canonical')): raise PolicyDenied('invalid proposal fields')
        args_json=_canonical_args(binding['arguments'])
        if args_json!=binding['arguments_canonical']: raise PolicyDenied('noncanonical proposal arguments')
        raw=replacement.encode('utf-8')
        if len(raw)>self.MAX_FILE_BYTES or _digest(raw)!=binding['replacement']: raise PolicyDenied('proposal replacement mismatch')
        if len(binding['revision'])!=64 or any(c not in '0123456789abcdef' for c in binding['revision']): raise PolicyDenied('invalid source digest')
        self._path(binding['path'],must_exist=True)
        p={'id':identifier,'binding':json.loads(json.dumps(binding)),'replacement':replacement}
        self._proposals[identifier]={'proposal':p,'approved':False,'used':False}

    def approve_patch(self,proposal_id,*,session_id,tool_name,arguments):
        item=self._proposals.get(proposal_id)
        if not item or item['used']: raise PolicyDenied('unknown or consumed proposal')
        b=item['proposal']['binding']
        if (b['session'],b['tool'],b['arguments_canonical'])!=(session_id,tool_name,_canonical_args(arguments)): raise PolicyDenied('approval binding mismatch')
        item['approved']=True

    def reconcile_proposal(self,receipt_or_id):
        """Classify an interrupted apply without replaying or granting approval."""
        if isinstance(receipt_or_id,str):
            item=self._proposals.get(receipt_or_id)
            if not item: raise PolicyDenied('unknown proposal')
            p=item['proposal']
        else:
            if not isinstance(receipt_or_id,dict) or set(receipt_or_id)!={'id','binding','replacement'}: raise PolicyDenied('invalid proposal receipt')
            p=receipt_or_id
        b=p['binding'];path=self._path(b['path'],must_exist=True)
        current=_digest(self._bounded_bytes(path,self.MAX_FILE_BYTES))
        if current==b['replacement']: return 'applied'
        if current==b['revision']: return 'pending'
        return 'conflict'

    def apply_approved(self,proposal_id,*,session_id,tool_name,arguments):
        with self._lock:
            item=self._proposals.get(proposal_id)
            if not item or not item['approved'] or item['used']: raise PolicyDenied('approval required or consumed')
            p=item['proposal'];b=p['binding']
            if (b['session'],b['tool'],b['arguments_canonical'])!=(session_id,tool_name,_canonical_args(arguments)): raise PolicyDenied('approval binding mismatch')
            path=self._path(b['path'],must_exist=True)
            old=self._bounded_bytes(path,self.MAX_FILE_BYTES)
            if _digest(old)!=b['revision']: raise PolicyDenied('stale content hash')
            # Atomic replace avoids partially written target bytes. It does not close
            # the hostile concurrent rename race between path validation and replace.
            mode=stat.S_IMODE(path.stat().st_mode);fd,tmp=tempfile.mkstemp(prefix='.forgeagent-',dir=path.parent)
            item['used']=True
            try:
                with os.fdopen(fd,'wb') as stream:
                    stream.write(p['replacement'].encode('utf-8'));stream.flush();os.fsync(stream.fileno())
                os.chmod(tmp,mode);os.replace(tmp,path)
                dirfd=os.open(path.parent,os.O_RDONLY)
                try: os.fsync(dirfd)
                finally: os.close(dirfd)
            finally:
                try: os.unlink(tmp)
                except FileNotFoundError: pass
            return _digest(self._bounded_bytes(path,self.MAX_FILE_BYTES))

@dataclass
class TestExecutor:
    """Delegates to a separately supplied isolation backend; never runs a shell."""
    backend: object=None
    def run(self,command,*,cwd,timeout=10):
        if self.backend is None: raise PolicyDenied('isolated execution backend unavailable')
        if not isinstance(command,(list,tuple)) or not command or any(not isinstance(x,str) for x in command): raise PolicyDenied('argv required')
        return self.backend.run(tuple(command),cwd=cwd,timeout=timeout)
