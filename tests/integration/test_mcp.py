"""Offline protocol tests against the real stdio subprocess entry point."""
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from forgeagent.mcp import MCPError, StdioClient, PROTOCOL_VERSION


class MCPSubprocessTests(unittest.TestCase):
    def test_initialize_discover_call_and_clean_exit(self):
        with StdioClient([sys.executable,'-m','forgeagent.mcp_server']) as client:
            tools=client.list_tools()
            self.assertEqual({t['name'] for t in tools},{'echo','add'})
            self.assertEqual(client.call_tool('echo',{'text':'protocol'})['content'][0]['text'],'protocol')
            self.assertEqual(client.call_tool('add',{'a':3,'b':4})['content'][0]['text'],'7')
            self.assertTrue(client.call_tool('missing',{})['isError'])
            with self.assertRaises(MCPError): client._request('resources/list')
        self.assertIsNotNone(client.proc.poll())

    def test_concurrent_calls_keep_request_response_pairs_serialized(self):
        with StdioClient([sys.executable,'-m','forgeagent.mcp_server']) as client:
            with ThreadPoolExecutor(max_workers=2) as pool:
                first=pool.submit(client.call_tool,'echo',{'text':'first'})
                second=pool.submit(client.call_tool,'echo',{'text':'second'})
                self.assertEqual(first.result()['content'][0]['text'],'first')
                self.assertEqual(second.result()['content'][0]['text'],'second')

    def test_negotiated_version_is_pinned(self):
        self.assertEqual(PROTOCOL_VERSION,'2025-11-25')

    def test_bad_duplicate_json_and_timeout_close_child(self):
        duplicate='import sys; sys.stdin.readline(); print("{\\\"jsonrpc\\\":\\\"2.0\\\",\\\"id\\\":1,\\\"id\\\":1,\\\"result\\\":{}}",flush=True)'
        with self.assertRaises(MCPError):
            StdioClient([sys.executable,'-c',duplicate])
        sleeper='import sys,time; sys.stdin.readline(); time.sleep(3)'
        with self.assertRaises((MCPError,TimeoutError)):
            StdioClient([sys.executable,'-c',sleeper],timeout=.1)

    def test_malformed_and_oversized_frames_fail_closed(self):
        malformed='import sys; sys.stdin.readline(); sys.stdout.write("not-json\\n"); sys.stdout.flush()'
        with self.assertRaises(MCPError):
            StdioClient([sys.executable,'-c',malformed])
        oversized='import sys; sys.stdin.readline(); print("x"*1000001,flush=True)'
        with self.assertRaises(MCPError):
            StdioClient([sys.executable,'-c',oversized],timeout=1)

    def test_server_rejects_invalid_ids_and_preinitialized_calls(self):
        import subprocess
        pre='{"jsonrpc":"2.0","id":9,"method":"tools/list"}\n'
        proc=subprocess.run([sys.executable,'-m','forgeagent.mcp_server'],input=pre.encode(),stdout=subprocess.PIPE,timeout=2)
        response=__import__('json').loads(proc.stdout.decode().splitlines()[0])
        self.assertEqual(response['id'],9)
        self.assertIn('error',response)
        bad='{"jsonrpc":"2.0","id":[],"method":"initialize","params":{}}\n'
        proc=subprocess.run([sys.executable,'-m','forgeagent.mcp_server'],input=bad.encode(),stdout=subprocess.PIPE,timeout=2)
        self.assertEqual(proc.returncode,2)
        self.assertEqual(proc.stdout,b'')
