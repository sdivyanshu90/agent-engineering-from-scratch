"""A bounded, human-approved coding agent assembled from ForgeAgent components.

The model can search, read, propose an exact replacement, and request an isolated
test run. It cannot approve its own proposal and receives no general shell tool.
"""
from __future__ import annotations

import asyncio
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import re
import sys

from .runtime import Agent, Budgets, Registry, Tool
from .policy import Workspace, TestExecutor, PolicyDenied


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class RepoTools:
    """Read-only repository search plus explicit patch proposal and test request."""
    def __init__(self, workspace: Workspace, *, session_id: str,
                 test_backend=None, max_files=200, max_file_bytes=2400):
        self.workspace = workspace
        self.session_id = session_id
        self.journal = None
        self.owner = None
        self.max_files, self.max_file_bytes = max_files, max_file_bytes
        self.executor = TestExecutor(test_backend)
        self._proposals = {}
        self._proposal_arguments = {}

    def _paths(self):
        paths = []
        pending = [self.workspace.root]
        visited = 0
        excluded = {".git", ".venv", "__pycache__", "node_modules", ".aws",
                    ".ssh", ".codex", ".agents", "secrets"}
        while pending:
            current = pending.pop()
            with os.scandir(current) as entries:
                for entry in entries:
                    visited += 1
                    if visited > self.max_files * 8:
                        raise PolicyDenied("workspace search entry limit exceeded")
                    if entry.name.casefold() in excluded or entry.is_symlink():
                        continue
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(path)
                    elif entry.is_file(follow_symlinks=False):
                        try:
                            self.workspace._path(path.relative_to(self.workspace.root).as_posix())
                        except PolicyDenied:
                            continue
                        paths.append(path.relative_to(self.workspace.root).as_posix())
        return sorted(paths)[:self.max_files]

    def evidence(self, query: str):
        """Retrieve one exact, revision-bound passage using the Week 6 baseline."""
        from .grounding import extract_answer
        from .retrieval import BM25, chunk_text

        if not query.strip() or len(query.encode()) > 512:
            raise ValueError("query out of range")
        chunks = []
        for relative in self._paths():
            try:
                source = self.workspace.read_text(relative, self.max_file_bytes)
            except (OSError, UnicodeError, PolicyDenied):
                continue
            chunks.extend(chunk_text(relative, source, lines=8, overlap=1))
        index = BM25(chunks)
        answer = extract_answer(query, index)
        citations = []
        for citation in answer.citations:
            chunk = index.chunks[citation.chunk_id]
            citations.append({**asdict(citation), "path": chunk.path,
                              "start_line": chunk.start_line, "end_line": chunk.end_line})
        return {"text": answer.text, "abstained": answer.abstained, "citations": citations}

    def search(self, query: str, limit: int=5):
        if not query.strip() or len(query.encode()) > 512 or type(limit) is not int or not 1 <= limit <= 5:
            raise ValueError("query and limit out of range")
        terms=set(re.findall(r"[a-z0-9_]+",query.casefold()))
        hits=[]
        for relative in self._paths():
            try: text=self.workspace.read_text(relative,self.max_file_bytes)
            except (OSError,UnicodeError,PolicyDenied): continue
            score=sum(len(terms & set(re.findall(r"[a-z0-9_]+",line.casefold()))) for line in text.splitlines())
            if score:
                best=next((i for i,line in enumerate(text.splitlines(),1) if terms & set(re.findall(r"[a-z0-9_]+",line.casefold()))),1)
                rows=text.splitlines()
                hits.append({"path":relative,"score":score,"line":best,"snippet":rows[best-1][:240]})
        return sorted(hits,key=lambda x:(-x["score"],x["path"]))[:limit]

    def read(self, path: str):
        text=self.workspace.read_text(path,self.max_file_bytes)
        return {"path":path,"text":text,"sha256":sha256_text(text),"bytes":len(text.encode())}

    def propose(self, path: str, expected_sha256: str, replacement_text: str):
        args={"path":path,"expected_sha256":expected_sha256,"replacement_text":replacement_text}
        proposal=self.workspace.propose_patch(path,expected_sha256,replacement_text,
            session_id=self.session_id,tool_name="propose_patch",arguments=args)
        self._proposals[proposal["proposal_id"]]=proposal
        self._proposal_arguments[proposal["proposal_id"]]=args
        return {**proposal,"approval_required":True,
                "review_sha256":sha256_text(json.dumps({"path":path,"before":expected_sha256,
                    "after":proposal["after_sha256"]},sort_keys=True,separators=(",",":")))}

    def approve_and_apply(self, proposal_id: str, review_sha256: str):
        """Human UI callback; caller must show the exact replacement before invoking."""
        proposal=self._proposals.get(proposal_id)
        args=self._proposal_arguments.get(proposal_id)
        if proposal is None or args is None: raise PolicyDenied("proposal unavailable")
        expected=sha256_text(json.dumps({"path":proposal["path"],"before":proposal["before_sha256"],
            "after":proposal["after_sha256"]},sort_keys=True,separators=(",",":")))
        if review_sha256 != expected: raise PolicyDenied("review digest mismatch")
        self.workspace.approve_patch(proposal_id,session_id=self.session_id,
            tool_name="propose_patch",arguments=args)
        if self.journal is None:
            return self.workspace.apply_approved(proposal_id,session_id=self.session_id,
                tool_name="propose_patch",arguments=args)
        before=proposal["before_sha256"];after=proposal["after_sha256"]
        payload={"proposal_id":proposal_id,"path":proposal["path"],"before_sha256":before,
                 "after_sha256":after,"review_sha256":review_sha256}
        revision=self.journal.revision(self.owner,self.session_id)
        self.journal.append(self.owner,self.session_id,revision,"patch_approved",payload)
        operation_id="apply-"+proposal_id
        intent=self.journal.intent(self.owner,self.session_id,operation_id,payload)
        if intent["status"]=="complete":
            if sha256_text(self.workspace.read_text(proposal["path"]))!=after:
                raise PolicyDenied("completed operation revision changed")
            return after
        current=sha256_text(self.workspace.read_text(proposal["path"]))
        if current==after:
            if intent["status"]!="unknown":
                self.journal.resolve(self.owner,self.session_id,operation_id,intent["digest"],result={"sha256":after})
            return after
        if intent["status"]=="unknown":
            raise PolicyDenied("unknown operation requires operator reconciliation")
        if current!=before:
            self.journal.resolve(self.owner,self.session_id,operation_id,intent["digest"],unknown=True)
            raise PolicyDenied("ambiguous patch state; operator reconciliation required")
        result=self.workspace.apply_approved(proposal_id,session_id=self.session_id,
            tool_name="propose_patch",arguments=args)
        if result!=after: raise PolicyDenied("applied content digest mismatch")
        self.journal.resolve(self.owner,self.session_id,operation_id,intent["digest"],result={"sha256":result})
        return result

    def export_proposals(self):
        receipts = []
        for identifier in sorted(self._proposals):
            try:
                receipts.append(self.workspace.export_proposal(identifier))
            except PolicyDenied:
                # The workspace consumed this receipt at apply time.
                continue
        return receipts

    def restore_proposals(self, receipts):
        for receipt in receipts:
            self.workspace.restore_proposal(receipt)
            # Week 9 receipts preserve the exact proposal ID and binding while
            # intentionally discarding approval state across process restart.
            proposal=receipt.get("proposal",receipt)
            binding=proposal.get("binding",{})
            identifier=proposal.get("id") or receipt.get("proposal_id")
            arguments=binding.get("arguments")
            if not identifier or not isinstance(arguments,dict):
                raise ValueError("invalid durable proposal receipt")
            self._proposals[identifier]={"proposal_id":identifier,"path":binding["path"],
                "before_sha256":binding["revision"],"after_sha256":binding["replacement"]}
            self._proposal_arguments[identifier]=arguments

    def run_tests(self):
        # Fixed argv: model supplied strings are never interpreted as commands.
        return self.executor.run((sys.executable, "-m", "unittest", "discover", "-s", "tests"),
            cwd=self.workspace.root,timeout=30)

    def registry(self):
        registry=Registry()
        async def search(query,limit=5): return self.search(query,limit)
        async def read_file(path): return self.read(path)
        async def retrieve_evidence(query): return self.evidence(query)
        async def propose_patch(path,expected_sha256,replacement_text):
            return self.propose(path,expected_sha256,replacement_text)
        async def run_tests(): return await asyncio.to_thread(self.run_tests)
        registry.register(Tool("search_repo","Find matching lines in bounded repository files.",{
            "type":"object","properties":{"query":{"type":"string","maxLength":512},"limit":{"type":"integer","minimum":1,"maximum":5}},
            "required":["query"],"additionalProperties":False},search,"read"))
        registry.register(Tool("retrieve_evidence", "Retrieve an exact quote with its repository revision.", {
            "type": "object", "properties": {"query": {"type": "string", "maxLength": 512}},
            "required": ["query"], "additionalProperties": False}, retrieve_evidence, "read"))
        registry.register(Tool("read_file","Read one bounded UTF-8 repository file and its content hash.",{
            "type":"object","properties":{"path":{"type":"string","maxLength":512}},"required":["path"],"additionalProperties":False},read_file,"read"))
        registry.register(Tool("propose_patch","Propose a complete replacement bound to the file's current SHA-256.",{
            "type":"object","properties":{"path":{"type":"string","maxLength":512},"expected_sha256":{"type":"string","maxLength":64},
                "replacement_text":{"type":"string","maxLength":12000}},"required":["path","expected_sha256","replacement_text"],"additionalProperties":False},propose_patch,"write"))
        registry.register(Tool("run_tests","Request the fixed test command through an injected isolation backend.",{
            "type":"object","properties":{},"required":[],"additionalProperties":False},run_tests,"read"))
        return registry


def attach_mcp_tools(registry: Registry, client, *, allowlist, read_only):
    """Attach explicitly allowlisted MCP tools as read-only model tools.

    The MCP server's description is untrusted metadata. Schemas outside the
    runtime's small closed-object subset are rejected instead of widened.
    """
    from .runtime import Rejected
    allowed=set(allowlist); safe=set(read_only)
    if not safe <= allowed: raise ValueError("read-only names must be allowlisted")
    for item in client.list_tools():
        name=item.get("name")
        if name not in safe: continue
        schema=item.get("inputSchema")
        if not isinstance(schema,dict) or schema.get("type")!="object" or schema.get("additionalProperties") is not False:
            raise Rejected("mcp_closed_schema_required")
        if any(spec.get("type") not in {"string","integer","boolean"} for spec in schema.get("properties",{}).values()):
            raise Rejected("mcp_schema_subset")
        async def invoke(_name=name,**arguments):
            # stdio MCP is blocking. Its server-side timeout is still required:
            # cancelling this await cannot stop the worker thread or remote tool.
            result=await asyncio.to_thread(client.call_tool,_name,arguments)
            if result.get("isError"): raise ValueError("mcp_tool_error")
            content=result["content"]
            encoded=json.dumps(content,ensure_ascii=False)
            if len(encoded.encode())>4096: raise ValueError("mcp_observation_limit")
            return content
        registry.register(Tool(name,"MCP read tool (remote output is untrusted).",schema,invoke,"read"))
    return registry


class CodingSession:
    """Agent execution, bounded context, and optional durable JSON checkpoints."""
    def __init__(self, provider, workspace: Workspace, *, owner="local", session_id="coding",
                 test_backend=None, journal=None, budgets=None, model="offline-fixture", read_only=False):
        self.owner,self.session_id=owner,session_id
        self.journal=journal
        self.repo=RepoTools(workspace,session_id=session_id,test_backend=test_backend)
        self.repo.journal=journal
        self.repo.owner=owner
        self.registry=self.repo.registry()
        self.read_only = read_only
        allowed = {"search_repo", "read_file", "retrieve_evidence"}
        if not read_only:
            allowed.update({"propose_patch", "run_tests"})
        self.agent=Agent(provider, self.registry, allowed,
            model=model,budgets=budgets or Budgets(steps=8,tools=12,tokens=8192,seconds=30,tool_seconds=5))
        self.context=[]

    def save_context(self, items):
        """Persist compact, untrusted memory as text plus explicit source refs."""
        from .context import compact
        result=compact(items,max_chars=1200)
        self.context=[{"text":result.text,"source_refs":list(result.source_refs),
                       "source_revisions":list(result.source_revisions),"authority":result.authority}]
        return self.context[0]

    @staticmethod
    def select_memory(items, query, *, token_budget, now, reserved=()):
        from .context import select_context
        return select_context(items,query,token_budget=token_budget,now=now,reserved=reserved)

    def attach_mcp(self, client, *, allowlist, read_only):
        before=set(self.registry.tools)
        attach_mcp_tools(self.registry,client,allowlist=allowlist,read_only=read_only)
        added=set(self.registry.tools)-before
        self.agent.allowed=frozenset(set(self.agent.allowed)|added)
        return sorted(added)

    async def run(self, task: str, *, resume=False):
        state=None
        revision=0
        if resume:
            if self.journal is None: raise ValueError("resume requires a durable journal")
            saved=self.journal.resume(self.owner,self.session_id,"agent")
            state,revision=saved["state"],saved["revision"]
            # Recover the narrow crash window after the append but before the
            # separate checkpoint upsert. Snapshot events are full JSON state.
            tail=self.journal.events(self.owner,self.session_id,after=revision)
            snapshots=[event for event in tail if event["kind"]=="agent_snapshot"]
            if snapshots:
                state=snapshots[-1]["payload"]["snapshot"]
                revision=snapshots[-1]["revision"]
                self.journal.checkpoint(self.owner,self.session_id,"agent",state,revision)
            revision=self.journal.revision(self.owner,self.session_id)
            self.context = state.get("coding", {}).get("context", [])
            if state.get("coding",{}).get("proposals"):
                self.repo.restore_proposals(state["coding"]["proposals"])
        elif self.journal is not None:
            revision=self.journal.revision(self.owner,self.session_id)
        async def checkpoint(snapshot):
            nonlocal revision
            if self.journal is not None:
                snapshot=dict(snapshot)
                snapshot["coding"]={"proposals":self.repo.export_proposals(),"context":self.context}
                revision=self.journal.append(self.owner,self.session_id,revision,"agent_snapshot",{
                    "snapshot":snapshot})
                self.journal.checkpoint(self.owner,self.session_id,"agent",snapshot,revision)
        kwargs={"resume":state,"checkpoint":checkpoint if self.journal else None}
        if self.context:
            task = json.dumps({"task": task, "untrusted_compacted_context": self.context}, ensure_ascii=False, sort_keys=True)
        return await self.agent.run(task, allow_write=not self.read_only, **kwargs)
