import hashlib
from pathlib import Path
import tempfile
import unittest
from forgeagent.policy import Workspace, PolicyDenied, TestExecutor
from forgeagent.skills import load_skill, load_reference, SkillError

class PolicyTests(unittest.TestCase):
 def test_patch_requires_exact_human_approval_and_is_one_use(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a.txt';p.write_text('before')
   w=Workspace(d); h=hashlib.sha256(b'before').hexdigest()
   proposal=w.propose_patch('a.txt',h,'after',session_id='s',tool_name='edit',arguments={'path':'a.txt'})
   pid=proposal['proposal_id']
   with self.assertRaises(PolicyDenied):w.apply_approved(pid,session_id='s',tool_name='edit',arguments={'path':'a.txt'})
   with self.assertRaises(PolicyDenied):w.approve_patch(pid,session_id='s',tool_name='edit',arguments={'path':'other'})
   w.approve_patch(pid,session_id='s',tool_name='edit',arguments={'path':'a.txt'})
   self.assertEqual(w.apply_approved(pid,session_id='s',tool_name='edit',arguments={'path':'a.txt'}),hashlib.sha256(b'after').hexdigest())
   with self.assertRaises(PolicyDenied):w.apply_approved(pid,session_id='s',tool_name='edit',arguments={'path':'a.txt'})
 def test_mutating_arguments_after_proposal_does_not_change_approval_binding(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a.txt';p.write_text('before');w=Workspace(d);args={'path':'a.txt','nested':{'mode':'safe'}}
   h=hashlib.sha256(b'before').hexdigest();x=w.propose_patch('a.txt',h,'after',session_id='s',tool_name='edit',arguments=args);args['nested']['mode']='changed'
   w.approve_patch(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a.txt','nested':{'mode':'safe'}})
   self.assertEqual(w.apply_approved(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a.txt','nested':{'mode':'safe'}}),hashlib.sha256(b'after').hexdigest())
 def test_read_bound_does_not_read_unbounded_file(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'large';p.write_bytes(b'x'*10000);w=Workspace(d)
   with self.assertRaises(PolicyDenied):w.read_text('large',max_bytes=5)
 def test_export_restore_never_restores_approval(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a';p.write_text('before');h=hashlib.sha256(b'before').hexdigest();w=Workspace(d)
   x=w.propose_patch('a',h,'after',session_id='s',tool_name='edit',arguments={'path':'a'});receipt=w.export_proposal(x['proposal_id'])
   w.approve_patch(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a'})
   resumed=Workspace(d);resumed.restore_proposal(receipt)
   with self.assertRaises(PolicyDenied):resumed.apply_approved(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a'})
   resumed.approve_patch(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a'})
   resumed.apply_approved(x['proposal_id'],session_id='s',tool_name='edit',arguments={'path':'a'})
   with self.assertRaises(PolicyDenied):resumed.restore_proposal(receipt)
 def test_sensitive_paths_and_type_exact_approval_binding(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'.env').write_text('secret');(root/'safe.txt').write_text('old');w=Workspace(root)
   for name in ('.env','.env.local','.aws/credentials','.git/config','id_rsa','private.pem'):
    with self.subTest(name=name),self.assertRaises(PolicyDenied):w.read_text(name)
   h=hashlib.sha256(b'old').hexdigest();x=w.propose_patch('safe.txt',h,'new',session_id='s',tool_name='e',arguments={'flag':1})
   with self.assertRaises(PolicyDenied):w.approve_patch(x['proposal_id'],session_id='s',tool_name='e',arguments={'flag':True})
 def test_reconcile_pending_applied_conflict(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'file';p.write_text('old');w=Workspace(d);h=hashlib.sha256(b'old').hexdigest();x=w.propose_patch('file',h,'new',session_id='s',tool_name='e',arguments={});pid=x['proposal_id'];receipt=w.export_proposal(pid)
   self.assertEqual(w.reconcile_proposal(pid),'pending');p.write_text('other');self.assertEqual(w.reconcile_proposal(receipt),'conflict');p.write_text('new');self.assertEqual(w.reconcile_proposal(receipt),'applied')
 def test_oversized_patch_source_rejected_before_full_read(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'large';p.write_bytes(b'x'*70000);w=Workspace(d)
   with self.assertRaises(PolicyDenied):w.propose_patch('large',hashlib.sha256(p.read_bytes()).hexdigest(),'y',session_id='s',tool_name='e',arguments={})
 def test_reject_path_escape_and_symlinks(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'root';root.mkdir();outside=Path(d)/'secret';outside.write_text('x')
   (root/'link').symlink_to(outside)
   w=Workspace(root)
   with self.assertRaises(PolicyDenied):w.read_text('../secret')
   with self.assertRaises(PolicyDenied):w.read_text('link')
 def test_stale_revision_and_no_isolation_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a';p.write_text('one');w=Workspace(d);h=hashlib.sha256(b'one').hexdigest()
   x=w.propose_patch('a',h,'two',session_id='s',tool_name='e',arguments={});w.approve_patch(x['proposal_id'],session_id='s',tool_name='e',arguments={});p.write_text('changed')
   with self.assertRaises(PolicyDenied):w.apply_approved(x['proposal_id'],session_id='s',tool_name='e',arguments={})
  with self.assertRaises(PolicyDenied):TestExecutor().run(['python','-c','pass'],cwd='.')
 def test_skill_content_is_untrusted_and_reference_is_explicit(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'hello';root.mkdir();(root/'SKILL.md').write_text('---\nname: hello\ndescription: A sample\n---\nRead only.\n');(root/'references').mkdir();(root/'references'/'x.md').write_text('details')
   skill=load_skill(root);self.assertFalse(skill['trusted']);self.assertEqual(load_reference(root,'references/x.md'),'details')
   with self.assertRaises(SkillError):load_reference(root,'../outside')
