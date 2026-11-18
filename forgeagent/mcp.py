"""Small offline MCP 2025-11-25 stdio client for the supported tool subset."""
import json
import subprocess
import os
import select
import threading

PROTOCOL_VERSION = '2025-11-25'
MAX_LINE = 1_000_000


class MCPError(ValueError):
    pass


def _strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result: raise MCPError('duplicate JSON key')
            result[key]=value
        return result
    def constant(_): raise MCPError('non-finite JSON number')
    try: return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=constant)
    except (UnicodeDecodeError,ValueError,RecursionError) as error: raise MCPError('invalid JSON frame') from error


class StdioClient:
    """Launch and own one MCP server subprocess; supports tools only, no HTTP."""
    def __init__(self, command, timeout=3.0):
        if not isinstance(command,(list,tuple)) or not command or any(not isinstance(x,str) for x in command): raise ValueError('command must be argv')
        self.proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        self.timeout=timeout; self.next_id=1; self.initialized=False; self._buffer=bytearray(); self._poisoned=False; self._lock=threading.Lock()
        os.set_blocking(self.proc.stdout.fileno(),False)
        try:
            result=self._request('initialize',{'protocolVersion':PROTOCOL_VERSION,'capabilities':{},'clientInfo':{'name':'forgeagent','version':'1.0.0'}})
            if result.get('protocolVersion') != PROTOCOL_VERSION: raise MCPError('unsupported negotiated version')
            self._send({'jsonrpc':'2.0','method':'notifications/initialized'})
            self.initialized=True
        except BaseException:
            self.close(); raise

    def _send(self, value):
        if self._poisoned or self.proc.poll() is not None: raise MCPError('client is closed or poisoned')
        raw=json.dumps(value,separators=(',',':'),ensure_ascii=False).encode('utf-8')+b'\n'
        if len(raw)>MAX_LINE: raise MCPError('request too large')
        self.proc.stdin.write(raw); self.proc.stdin.flush()

    def _read_frame(self):
        deadline=__import__('time').monotonic()+self.timeout
        while True:
            pos=self._buffer.find(b'\n')
            if pos>=0:
                frame=bytes(self._buffer[:pos]); del self._buffer[:pos+1]
                if not frame or len(frame)+1>MAX_LINE: raise MCPError('empty or oversized frame')
                return frame
            if len(self._buffer)>=MAX_LINE: raise MCPError('frame too large')
            remaining=deadline-__import__('time').monotonic()
            if remaining<=0:
                self._poisoned=True; self.close(); raise TimeoutError('MCP response timeout; session closed')
            ready,_,_=select.select([self.proc.stdout],[],[],remaining)
            if not ready:
                self._poisoned=True; self.close(); raise TimeoutError('MCP response timeout; session closed')
            try: chunk=os.read(self.proc.stdout.fileno(),min(65536,MAX_LINE-len(self._buffer)))
            except BlockingIOError: continue
            if not chunk: raise EOFError('MCP server closed stdout')
            self._buffer.extend(chunk)

    def _request(self, method, params=None):
        with self._lock:
            return self._request_locked(method,params)

    def _request_locked(self, method, params=None):
        identifier=self.next_id; self.next_id+=1
        request={'jsonrpc':'2.0','id':identifier,'method':method}
        if params is not None: request['params']=params
        try:
            self._send(request)
            response=_strict_json(self._read_frame())
        except BaseException:
            self._poisoned=True; self.close(); raise
        valid=(isinstance(response,dict) and response.get('jsonrpc')=='2.0' and
               type(response.get('id')) is int and response.get('id')==identifier and
               (('result' in response) != ('error' in response)) and
               set(response)<= {'jsonrpc','id','result','error'})
        if valid and 'error' in response:
            error=response['error']
            valid=(isinstance(error,dict) and type(error.get('code')) is int and
                   isinstance(error.get('message'),str))
        if not valid:
            self._poisoned=True; self.close(); raise MCPError('invalid or mismatched response')
        if response.get('error'): raise MCPError('remote JSON-RPC error')
        return response['result']

    def list_tools(self):
        result=self._request('tools/list')
        if not isinstance(result,dict) or not isinstance(result.get('tools'),list): raise MCPError('malformed tools/list result')
        return result['tools']

    def call_tool(self,name,arguments):
        if not isinstance(name,str) or not isinstance(arguments,dict): raise ValueError('tool name and object arguments required')
        result=self._request('tools/call',{'name':name,'arguments':arguments})
        if not isinstance(result,dict) or not isinstance(result.get('content'),list) or type(result.get('isError')) is not bool:
            raise MCPError('malformed tools/call result')
        return result

    def close(self):
        if self.proc.poll() is None:
            try: self.proc.stdin.close()
            except OSError: pass
            try: self.proc.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired: self.proc.terminate();
            try: self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired: self.proc.kill(); self.proc.wait()
        for stream in (self.proc.stdout,self.proc.stderr):
            if stream:
                try: stream.close()
                except OSError: pass

    def __enter__(self): return self
    def __exit__(self,*_): self.close()
