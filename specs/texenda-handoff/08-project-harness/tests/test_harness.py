"""Synthetic coordination tests. These are NOT Texenda application/provider/security acceptance."""
import importlib.util, json, tempfile, unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('harness',Path(__file__).resolve().parents[1]/'harness.py')
hm=importlib.util.module_from_spec(spec);spec.loader.exec_module(hm)

class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=self.base/'repo';self.pkg=self.base/'pkg'
        self.clock=[1700000000.0];self.pkg.mkdir();self.root.mkdir()
        (self.pkg/'05-implementation').mkdir();(self.pkg/'07-agent-orchestration').mkdir();(self.pkg/'01-foundation').mkdir()
        w=lambda i,deps,paths,tier=2,review=1,activation='AUTHORITATIVE DECISION': {'id':i,'dependencies':deps,'allowed_paths':paths,'recommended_model_tier':tier,'independent_review_tier':review,'activation':activation,'external_gates_for_activation':['VAL-01'] if activation=='REQUIRES EXTERNAL VALIDATION' else [],'authoritative_references':['kernel.md']}
        self.plan={'package_version':'test','work_packages':[w('WP-00',[],['src/a']),w('WP-01',['WP-00'],['src/b']),w('WP-02',[],['src/a/sub']),w('WP-03',[],['src/c']),w('WP-04',[],['src/d'],activation='REQUIRES EXTERNAL VALIDATION'),w('WP-05',[],['src/e'],activation='DEFER UNTIL TRIGGERED')]}
        (self.pkg/'05-implementation/work-packages.json').write_text(json.dumps(self.plan))
        (self.pkg/'01-foundation/external-validation-gates.json').write_text(json.dumps({'gates':[{'id':'VAL-01'}]}))
        (self.pkg/'07-agent-orchestration/context-routing.json').write_text(json.dumps({'kernel':['kernel.md'],'always_for_assignment':[]}))
        (self.pkg/'kernel.md').write_text('A synthetic kernel.\n')
        self.h=hm.Harness(self.root,self.pkg,lambda:self.clock[0]);self.h.init();self.seq=0;self.cand='a'*40;self.head='b'*40
    def tearDown(self):self.tmp.cleanup()
    def ev(self,kind,wid='WP-00',candidate=None,status='PASS',**extra):
        self.seq+=1;p=f'evidence/{self.seq}.json';log=self.root/f'evidence/{self.seq}.log';log.parent.mkdir(exist_ok=True);log.write_text('Synthetic fixture evidence, not application evidence.\n')
        e={'schema_version':'1.0','kind':kind,'task_id':wid,'candidate_revision':candidate or self.cand,'summary':'Synthetic test record','checks':[{'id':'fixture','required':True,'status':status,'command_or_procedure':'synthetic fixture','evidence_path':str(log.relative_to(self.root)),'sha256':hm.file_hash(log)}]}
        e.update(extra);(self.root/p).write_text(json.dumps(e));return p
    def begin(self,wid='WP-00',agent='human:author'):
        self.h.admit(wid,'astra');x=self.h.assign(wid,'astra',agent,2,human=True);self.h.start(wid,agent,x['fence']);return x['fence']
    def submit(self,wid='WP-00',status='PASS'):
        fence=self.begin(wid);paths=self.h.work[wid]['allowed_paths'];record=self.ev('submission',wid,changed_paths=[paths[0]+'/file.txt'],status=status)
        self.h.submit(wid,'human:author',fence,self.cand,record);return record
    def reviewed(self,wid='WP-00'):
        self.submit(wid);r=self.ev('review',wid);self.h.review(wid,'human:reviewer',1,self.cand,r,human=True)
    def integrated(self,wid='WP-00'):
        self.reviewed(wid);r=self.ev('integration',wid,integrated_revision=self.head,runtime_stopped=True)
        self.h.integrate(wid,'astra',self.cand,self.head,r)
    def roster(self):
        r=self.ev('roster',qualifications=[{'tier':2,'model_id':'synthetic-test-model','runtime_id':'test','client_version':'test','sign_in_mode':'test','reasoning_effort':'test','capabilities':['read','edit','test'],'billing_mode':'api','verified_at':hm.utc(self.clock[0]),'expires_at':hm.utc(self.clock[0]+86400)}]);self.h.roster('human:owner',r)
    def test_init_is_non_overwriting(self):
        with self.assertRaises(hm.Denied):self.h.init()
    def test_initial_ready_respects_dependencies_and_deferral(self):self.assertEqual(self.h.ready(),['WP-00','WP-02','WP-03','WP-04'])
    def test_incomplete_dependency_denied(self):
        with self.assertRaises(hm.Denied):self.h.admit('WP-01','astra')
    def test_unknown_package_denied(self):
        with self.assertRaises(hm.Denied):self.h.admit('WP-99','astra')
    def test_unverified_model_fails_closed(self):
        self.h.admit('WP-00','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-00','astra','agent:a',2)
    def test_weaker_tier_rejected(self):
        self.h.admit('WP-00','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-00','astra','human:a',3,human=True)
    def test_fake_human_label_rejected(self):
        self.h.admit('WP-00','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-00','astra','agent:a',2,human=True)
    def test_overlapping_leases_block_even_expired(self):
        self.begin();self.clock[0]+=4000;self.h.admit('WP-02','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-02','astra','human:b',2,human=True)
    def test_disjoint_parallel_assignments_allowed(self):
        self.begin();self.h.admit('WP-03','astra');self.h.assign('WP-03','astra','human:b',2,human=True)
    def test_default_writer_limit_is_enforced(self):
        self.begin();self.h.admit('WP-03','astra');self.h.assign('WP-03','astra','human:b',2,human=True);self.h.admit('WP-04','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-04','astra','human:c',2,human=True)
    def test_wrong_fence_cannot_start(self):
        self.h.admit('WP-00','astra');self.h.assign('WP-00','astra','human:author',2,human=True)
        with self.assertRaises(hm.Denied):self.h.start('WP-00','human:author',99)
    def test_expired_lease_cannot_submit(self):
        f=self.begin();self.clock[0]+=4000
        with self.assertRaises(hm.Denied):self.h.submit('WP-00','human:author',f,self.cand,self.ev('submission',changed_paths=['src/a/f']))
    def test_no_path_traversal(self):
        for p in ['../secret','/secret','C:/secret','src/./x','src/../x','src\\x']:
            with self.subTest(p=p),self.assertRaises(hm.Denied):hm.under(self.root,p,False)
    def test_evidence_symlink_denied(self):
        (self.root/'leak').symlink_to(self.pkg/'kernel.md')
        with self.assertRaises(hm.Denied):self.h.evidence('leak')
    def test_out_of_scope_changed_path_denied(self):
        f=self.begin()
        with self.assertRaises(hm.Denied):self.h.submit('WP-00','human:author',f,self.cand,self.ev('submission',changed_paths=['src/b/unsafe']))
    def test_changed_evidence_detected(self):
        r=self.submit();p=self.root/r;p.write_text(p.read_text()+' ')
        with self.assertRaises(hm.Denied):self.h.review('WP-00','human:reviewer',1,self.cand,self.ev('review'),human=True)
    def test_missing_test_log_denied(self):
        r=self.ev('submission',changed_paths=['src/a/f']);e=json.loads((self.root/r).read_text());(self.root/e['checks'][0]['evidence_path']).unlink()
        with self.assertRaises(hm.Denied):self.h.evidence(r)
    def test_author_cannot_review(self):
        self.submit()
        with self.assertRaises(hm.Denied):self.h.review('WP-00','human:author',1,self.cand,self.ev('review'),human=True)
    def test_insufficient_review_tier_denied(self):
        self.submit()
        with self.assertRaises(hm.Denied):self.h.review('WP-00','human:reviewer',2,self.cand,self.ev('review'),human=True)
    def test_not_run_cannot_pass_review(self):
        self.submit(status='NOT_RUN')
        with self.assertRaises(hm.Denied):self.h.review('WP-00','human:reviewer',1,self.cand,self.ev('review'),human=True)
    def test_stale_candidate_denied(self):
        self.submit()
        with self.assertRaises(hm.Denied):self.h.review('WP-00','human:reviewer',1,self.head,self.ev('review',candidate=self.head),human=True)
    def test_integration_without_stop_proof_denied(self):
        self.reviewed()
        with self.assertRaises(hm.Denied):self.h.integrate('WP-00','astra',self.cand,self.head,self.ev('integration',integrated_revision=self.head,runtime_stopped=False))
    def test_merge_semantic_change_requires_review(self):
        self.reviewed()
        with self.assertRaises(hm.Denied):self.h.integrate('WP-00','astra',self.cand,self.head,self.ev('integration',integrated_revision=self.head,runtime_stopped=True,conflict_resolution_changed_semantics=True))
    def test_complete_requires_integration(self):
        self.reviewed()
        with self.assertRaises(hm.Denied):self.h.complete('WP-00','astra')
    def test_lifecycle_and_dependency_release(self):
        self.integrated();self.h.complete('WP-00','astra');self.assertIn('WP-01',self.h.ready());self.assertEqual(self.h.status()['tasks']['WP-00']['state'],'completed')
    def test_activation_gate_not_assumed(self):
        self.integrated('WP-04')
        with self.assertRaises(hm.Denied):self.h.complete('WP-04','astra')
    def test_activation_gate_scope_checked(self):
        self.integrated('WP-04');r=self.ev('gate',gate_id='VAL-01',scope='test only',expires_at=hm.utc(self.clock[0]+1000),work_packages=['WP-03']);self.h.gate('human:owner',r)
        with self.assertRaises(hm.Denied):self.h.complete('WP-04','astra')
    def test_activation_gate_matching_scope_completes(self):
        self.integrated('WP-04');r=self.ev('gate',gate_id='VAL-01',scope='synthetic test gate',expires_at=hm.utc(self.clock[0]+1000),work_packages=['WP-04']);self.h.gate('human:owner',r);self.h.complete('WP-04','astra')
    def test_recovery_requires_stop_and_fence(self):
        self.begin();r=self.ev('recovery',runtime_stopped=False,previous_fence=1,observed_revision=self.cand)
        with self.assertRaises(hm.Denied):self.h.recover('WP-00','astra',r)
    def test_recovery_increments_fence(self):
        f=self.begin();r=self.ev('recovery',runtime_stopped=True,previous_fence=f,observed_revision=self.cand);self.h.recover('WP-00','astra',r)
        self.assertEqual(self.h.status()['tasks']['WP-00']['state'],'admitted');self.assertEqual(self.h.status()['tasks']['WP-00']['fence'],2)
    def test_state_corruption_detected(self):
        s=json.loads(self.h.statefile.read_text());s['tasks']['WP-00']['state']='completed';self.h.statefile.write_text(json.dumps(s))
        with self.assertRaises(hm.Denied):self.h.status()
    def test_receipt_chain_corruption_detected(self):
        s=json.loads(self.h.statefile.read_text());s['events'][0]['actor']='impostor';self.h.statefile.write_text(json.dumps(s))
        with self.assertRaises(hm.Denied):self.h.status()
    def test_baseline_change_requires_explicit_migration(self):
        p=self.pkg/'05-implementation/work-packages.json';p.write_text(p.read_text()+' ');h=hm.Harness(self.root,self.pkg,lambda:self.clock[0])
        with self.assertRaises(hm.Denied):h.status()
    def test_context_overflow_does_not_truncate(self):
        c=self.h.context('WP-00',max_bytes=1);self.assertEqual(c['status'],'NEEDS_NARROWING');self.assertTrue(c['context_files'])
    def test_deferred_requires_observed_trigger(self):
        with self.assertRaises(hm.Denied):self.h.admit('WP-05','astra')
        r=self.ev('trigger','WP-05');self.h.admit('WP-05','astra',r)
    def test_api_model_requires_budget(self):
        self.roster();self.h.admit('WP-00','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-00','astra','agent:a',2)
    def test_qualified_model_and_budget_allow_assignment(self):
        self.roster();self.h.budget('human:owner',5,self.ev('budget'));self.h.admit('WP-00','astra');r=self.h.assign('WP-00','astra','agent:a',2,budget_usd=1);self.assertEqual(r['model'],'synthetic-test-model')
    def test_qualification_expiry_denies_assignment(self):
        self.roster();self.clock[0]+=86401;self.h.admit('WP-00','astra')
        with self.assertRaises(hm.Denied):self.h.assign('WP-00','astra','agent:a',2)
    def test_checkpoint_does_not_extend_without_request(self):
        f=self.begin();before=json.loads(self.h.statefile.read_text())['tasks']['WP-00']['lease']['expires_at'];self.clock[0]+=10;self.h.checkpoint('WP-00','human:author',f,self.ev('checkpoint'));after=json.loads(self.h.statefile.read_text())['tasks']['WP-00']['lease']['expires_at'];self.assertEqual(before,after)

if __name__=='__main__':unittest.main(verbosity=2)
