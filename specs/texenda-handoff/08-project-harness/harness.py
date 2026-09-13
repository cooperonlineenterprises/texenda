#!/usr/bin/env python3
"""Texenda file-native coordination scaffold. No model launch, network, git merge or production effect.

POSIX/WSL, Python >=3.10, standard library only. Actor names/evidence assertions are not
cryptographic identity. Use runtime sandbox, protected Git review and human release controls.
"""
from __future__ import annotations
import argparse, contextlib, copy, datetime as dt, fcntl, hashlib, json, os
from pathlib import Path, PurePosixPath
import re, sys, tempfile, time
from typing import Any, Callable

class Denied(ValueError):
    """A state/contract precondition was not satisfied; nothing was committed."""

def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
def digest(obj: Any) -> str: return hashlib.sha256(canonical(obj)).hexdigest()
def file_hash(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def utc(ts: float) -> str: return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()
def parse_time(value: str) -> float:
    try:
        d=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
        if d.tzinfo is None: raise ValueError('timezone missing')
        return d.timestamp()
    except (TypeError,ValueError,AttributeError) as exc: raise Denied('explicit ISO8601 timezone required') from exc

def safe_rel(value: str) -> str:
    if not isinstance(value,str) or not value or '\\' in value or '\x00' in value:
        raise Denied('invalid relative path')
    p=PurePosixPath(value)
    if p.is_absolute() or any(x in ('..','.') for x in value.split('/')) or ':' in value or value.endswith('/'):
        raise Denied('absolute, traversal, dot, drive and trailing slash paths forbidden')
    return str(p)

def under(root: Path, value: str, must_exist: bool=True) -> Path:
    rel=safe_rel(value);p=root/rel
    cur=root
    for part in PurePosixPath(rel).parts:
        cur=cur/part
        if cur.is_symlink(): raise Denied('symlink path forbidden')
    try:p.resolve().relative_to(root.resolve())
    except ValueError as exc:raise Denied('path escapes root') from exc
    if must_exist and not p.is_file():raise Denied('evidence/reference file missing: '+rel)
    return p

def overlap(a: str,b: str) -> bool:
    return a==b or a.startswith(b+'/') or b.startswith(a+'/')

def revision(v: str) -> str:
    if not isinstance(v,str) or not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})',v):
        raise Denied('candidate must be a full 40/64 lowercase hex revision or tree digest')
    return v

def atomic_write(path: Path,obj: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.write-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as out:
            out.write(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False).encode()+b'\n');out.flush();os.fsync(out.fileno())
        os.replace(tmp,path)
        dfd=os.open(path.parent,os.O_RDONLY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

class Harness:
    def __init__(self,root: Path,package: Path,clock: Callable[[],float]=time.time):
        self.root=root.resolve();self.package=package.resolve();self.clock=clock
        self.dir=self.root/'.texenda';self.statefile=self.dir/'state.json'
        if self.dir.is_symlink():raise Denied('state directory cannot be a symlink')
        self.plan=json.loads((self.package/'05-implementation/work-packages.json').read_text())
        self.work={w['id']:w for w in self.plan['work_packages']}
        if len(self.work)!=len(self.plan['work_packages']):raise Denied('duplicate work package ID')
        self.package_hash=file_hash(self.package/'05-implementation/work-packages.json')
    @contextlib.contextmanager
    def locked(self):
        self.root.mkdir(parents=True,exist_ok=True);self.dir.mkdir(exist_ok=True)
        lock=self.dir/'state.lock'
        if lock.is_symlink() or self.statefile.is_symlink():raise Denied('state files cannot be symlinks')
        with lock.open('a+') as f:
            fcntl.flock(f,fcntl.LOCK_EX)
            try:yield
            finally:fcntl.flock(f,fcntl.LOCK_UN)
    def _read(self):
        if not self.statefile.is_file():raise Denied('run init first')
        s=json.loads(self.statefile.read_text());self._check(s);return s
    def _check(self,s):
        if s.get('version')!='1.0' or s.get('work_package_digest')!=self.package_hash:
            raise Denied('state format or work-package baseline changed; explicitly migrate state')
        prev='0'*64
        for e in s['events']:
            body={k:v for k,v in e.items() if k!='hash'}
            if e['previous_hash']!=prev or digest(body)!=e['hash']:raise Denied('receipt chain corrupt')
            prev=e['hash']
        if s['events'] and s['events'][-1]['state_digest']!=digest({k:v for k,v in s.items() if k!='events'}):
            raise Denied('state differs from last receipt')
    def _event(self,s,actor,op,task=None):
        if not actor or len(actor)>200:raise Denied('actor required')
        e={'sequence':len(s['events'])+1,'at':utc(self.clock()),'actor':actor,'operation':op,'task_id':task,
           'previous_hash':s['events'][-1]['hash'] if s['events'] else '0'*64,
           'state_digest':digest({k:v for k,v in s.items() if k!='events'})}
        e['hash']=digest(e);s['events'].append(e)
    def change(self,actor,op,fn,task=None):
        with self.locked():
            s=self._read();new=copy.deepcopy(s);result=fn(new)
            self._event(new,actor,op,task);atomic_write(self.statefile,new)
            return result
    def init(self,actor='human:owner'):
        with self.locked():
            if self.statefile.exists():raise Denied('state already exists; never overwrite to resume')
            s={'version':'1.0','package_version':self.plan['package_version'],'work_package_digest':self.package_hash,
               'budget_usd':0.0,'budget_approval':None,'max_concurrent_writers':2,'roster':[],'gates':{},'events':[],
               'tasks':{w:{'state':'planned','fence':0,'lease':None,'assignment':None,'candidate':None,
                    'submission':None,'review':None,'integration':None,'checkpoint':None,'trigger':None,'history':[]} for w in self.work}}
            self._event(s,actor,'init');atomic_write(self.statefile,s)
        return {'initialized':str(self.statefile),'tasks':len(self.work),'models_verified':False}
    def status(self):
        with self.locked():s=self._read()
        tasks={k:{'state':t['state'],'fence':t['fence'],'agent':(t['assignment'] or {}).get('agent'),
                  'expired_lease':bool(t['lease'] and t['lease']['expires_at']<=self.clock())} for k,t in s['tasks'].items()}
        return {'budget_usd':s['budget_usd'],'verified_tiers':[q['tier'] for q in s['roster'] if parse_time(q['expires_at'])>self.clock()],
                'tasks':tasks,'receipt_count':len(s['events'])}
    def ready(self):
        with self.locked():s=self._read()
        return [w for w,t in s['tasks'].items() if t['state']=='planned' and all(s['tasks'][d]['state']=='completed' for d in self.work[w]['dependencies']) and self.work[w]['activation']!='DEFER UNTIL TRIGGERED']
    def evidence(self,rel,kind=None,task=None,candidate=None,require_pass=False):
        path=under(self.root,rel);e=json.loads(path.read_text())
        if not isinstance(e,dict) or e.get('schema_version')!='1.0':raise Denied('invalid evidence envelope')
        if kind and e.get('kind')!=kind:raise Denied('wrong evidence kind')
        if task and e.get('task_id')!=task:raise Denied('evidence task mismatch')
        if candidate and e.get('candidate_revision')!=candidate:raise Denied('evidence candidate mismatch')
        if not isinstance(e.get('summary'),str) or not e['summary'].strip():raise Denied('evidence summary required')
        checks=e.get('checks',[])
        if not isinstance(checks,list):raise Denied('checks must be a list')
        ids=set()
        for c in checks:
            if not isinstance(c,dict) or not c.get('id') or c['id'] in ids:raise Denied('invalid/duplicate evidence check')
            ids.add(c['id'])
            if c.get('status') not in ('PASS','FAIL','NOT_RUN','NOT_APPLICABLE'):raise Denied('invalid check status')
            if not isinstance(c.get('required'),bool):raise Denied('check required flag must be boolean')
            if c['status'] in ('PASS','FAIL'):
                log=under(self.root,c.get('evidence_path',''))
                if file_hash(log)!=c.get('sha256'):raise Denied('test log hash mismatch')
                if not c.get('command_or_procedure'):raise Denied('test command/procedure required')
        if require_pass:
            required=[c for c in checks if c['required']]
            if not required or any(c['status']!='PASS' for c in required):raise Denied('all required checks must have PASS evidence; NOT RUN cannot pass')
        return {'path':safe_rel(rel),'sha256':file_hash(path)},e
    def recheck(self,ref,**kwargs):
        if not ref:raise Denied('missing evidence')
        actual,e=self.evidence(ref['path'],**kwargs)
        if actual['sha256']!=ref['sha256']:raise Denied('evidence changed since recorded')
        return e
    def roster(self,actor,record):
        if not actor.startswith('human:'):raise Denied('owner must attest actual runtime qualification')
        ref,e=self.evidence(record,'roster',require_pass=True)
        qs=e.get('qualifications',[])
        if not qs:raise Denied('no qualified model records')
        seen=set()
        for q in qs:
            if q.get('tier') not in (1,2,3) or q['tier'] in seen:raise Denied('one binding per tier')
            seen.add(q['tier'])
            for k in ['model_id','runtime_id','client_version','sign_in_mode','reasoning_effort','capabilities','billing_mode']:
                if not q.get(k):raise Denied('missing runtime qualification '+k)
            if q['billing_mode'] not in ('api','subscription'):raise Denied('unknown billing mode')
            if not isinstance(q['capabilities'],list):raise Denied('capabilities must be list')
            if parse_time(q['verified_at'])>self.clock()+60 or parse_time(q['expires_at'])<=self.clock():raise Denied('qualification stale/future')
            if parse_time(q['expires_at'])-parse_time(q['verified_at'])>30*86400:raise Denied('qualification valid at most 30 days; refresh after runtime/account/model change')
        return self.change(actor,'set-roster',lambda s:s.update(roster=[dict(q,evidence=ref) for q in qs]))
    def budget(self,actor,usd,record):
        if not actor.startswith('human:') or not isinstance(usd,(int,float)) or not 0<=usd<=100000:
            raise Denied('bounded owner-approved development budget required')
        ref,_=self.evidence(record,'budget',require_pass=True)
        return self.change(actor,'set-budget',lambda s:s.update(budget_usd=usd,budget_approval=ref))
    def gate(self,actor,record):
        if not actor.startswith('human:'):raise Denied('gate requires accountable human attestation')
        ref,e=self.evidence(record,'gate',require_pass=True);gid=e.get('gate_id')
        allowed={g['id'] for g in json.loads((self.package/'01-foundation/external-validation-gates.json').read_text())['gates']}
        if gid not in allowed or not e.get('scope') or parse_time(e.get('expires_at',''))<=self.clock():raise Denied('gate ID, scope and unexpired evidence required')
        return self.change(actor,'record-gate',lambda s:s['gates'].update({gid:{'evidence':ref,'scope':e['scope'],'expires_at':e['expires_at'],'owner':actor}}))
    def admit(self,wid,actor,trigger=None):
        def f(s):
            t=self.task(s,wid,'planned')
            if any(s['tasks'][d]['state']!='completed' for d in self.work[wid]['dependencies']):raise Denied('incomplete prerequisites')
            if self.work[wid]['activation']=='DEFER UNTIL TRIGGERED':
                if not trigger:raise Denied('deferred work needs observed trigger evidence')
                ref,_=self.evidence(trigger,'trigger',wid,require_pass=True);t['trigger']=ref
            t['state']='admitted'
        return self.change(actor,'admit',f,wid)
    def task(self,s,wid,*states):
        if wid not in self.work:raise Denied('unknown work package')
        t=s['tasks'][wid]
        if states and t['state'] not in states:raise Denied('task state '+t['state']+' not in '+','.join(states))
        return t
    def qualified(self,s,tier,human=False):
        if human:return None
        qs=[q for q in s['roster'] if q['tier']==tier and parse_time(q['expires_at'])>self.clock()]
        if not qs:raise Denied('target model tier not runtime-qualified')
        self.recheck(qs[0]['evidence'],kind='roster',require_pass=True);return qs[0]
    def assign(self,wid,actor,agent,tier,human=False,budget_usd=0,max_tokens=50000,max_seconds=3600):
        def f(s):
            t=self.task(s,wid,'admitted')
            if tier not in (1,2,3) or tier>self.work[wid]['recommended_model_tier']:raise Denied('tier below work-package requirement; decompose rather than under-route')
            if human!=agent.startswith('human:'):raise Denied('explicit human assignment must match human: principal')
            q=self.qualified(s,tier,human)
            if not 0<=budget_usd<=s['budget_usd'] or not 0<max_tokens<=1000000 or not 0<max_seconds<=28800:raise Denied('invalid task budget or bounds')
            used=sum((v['assignment'] or {}).get('budget_usd',0) + sum((h.get('assignment') or {}).get('budget_usd',0) for h in v['history']) for v in s['tasks'].values())
            if used+budget_usd>s['budget_usd']:raise Denied('development allowance exhausted; owner must increase')
            if q and q['billing_mode']=='api' and budget_usd<=0:raise Denied('API work needs positive owner-authorized development spend allowance')
            if sum(bool(v['lease']) for v in s['tasks'].values())>=s['max_concurrent_writers']:raise Denied('writer concurrency limit reached; serialize or approve a reviewed limit change')
            paths=[safe_rel(p) for p in self.work[wid]['allowed_paths']]
            for other,ot in s['tasks'].items():
                if other!=wid and ot['lease']:
                    if any(overlap(p,op) for p in paths for op in ot['lease']['paths']):
                        raise Denied('edit lease conflicts with '+other+'; expired leases require proved recovery')
            t['fence']+=1;t['lease']={'paths':paths,'owner':agent,'expires_at':self.clock()+max_seconds,'fence':t['fence']}
            t['assignment']={'agent':agent,'tier':tier,'human':human,'model':None if human else q['model_id'],'runtime':None if human else q['runtime_id'],'budget_usd':budget_usd,'max_tokens':max_tokens,'max_seconds':max_seconds}
            t['state']='assigned';return {'task':wid,'fence':t['fence'],'model':t['assignment']['model'],'paths':paths}
        return self.change(actor,'assign',f,wid)
    def owned(self,t,actor,fence):
        if not t['lease'] or t['lease']['owner']!=actor or t['fence']!=fence:raise Denied('actor/fence mismatch')
        if t['lease']['expires_at']<=self.clock():raise Denied('lease expired; obtain stop/recovery evidence')
    def start(self,wid,actor,fence):
        def f(s):
            t=self.task(s,wid,'assigned');self.owned(t,actor,fence);self.qualified(s,t['assignment']['tier'],t['assignment']['human']);t['state']='running'
        return self.change(actor,'start',f,wid)
    def checkpoint(self,wid,actor,fence,record,extend_seconds=0):
        def f(s):
            t=self.task(s,wid,'running');self.owned(t,actor,fence)
            ref,_=self.evidence(record,'checkpoint',wid);t['checkpoint']=ref
            if extend_seconds:
                if not 0<extend_seconds<=3600:raise Denied('extension limited to one hour')
                t['lease']['expires_at']=self.clock()+extend_seconds
        return self.change(actor,'checkpoint',f,wid)
    def submit(self,wid,actor,fence,candidate,record):
        candidate=revision(candidate)
        def f(s):
            t=self.task(s,wid,'running');self.owned(t,actor,fence)
            ref,e=self.evidence(record,'submission',wid,candidate)
            changed=e.get('changed_paths',[])
            if not isinstance(changed,list) or not changed:raise Denied('changed paths required')
            for p in changed:
                safe_rel(p)
                if not any(p==a or p.startswith(a+'/') for a in t['lease']['paths']):raise Denied('unadmitted changed path '+p)
            t.update(state='submitted',candidate=candidate,submission=ref,review=None,integration=None)
        return self.change(actor,'submit',f,wid)
    def review(self,wid,actor,tier,candidate,record,approve=True,human=False):
        candidate=revision(candidate)
        def f(s):
            t=self.task(s,wid,'submitted')
            if t['candidate']!=candidate:raise Denied('stale review candidate')
            if actor==t['assignment']['agent']:raise Denied('author cannot independently review own work')
            if human!=actor.startswith('human:'):raise Denied('human review flag/principal mismatch')
            if tier not in (1,2,3) or tier>self.work[wid]['independent_review_tier']:raise Denied('review tier insufficient')
            self.qualified(s,tier,human)
            self.recheck(t['submission'],kind='submission',task=wid,candidate=candidate,require_pass=approve)
            ref,_=self.evidence(record,'review',wid,candidate,require_pass=approve)
            t['review']={'actor':actor,'tier':tier,'candidate':candidate,'evidence':ref,'approved':approve}
            t['state']='reviewed' if approve else 'running'
            if not approve:t['review']=None;t['integration']=None
        return self.change(actor,'approve-review' if approve else 'request-changes',f,wid)
    def integrate(self,wid,actor,candidate,integrated,record):
        candidate=revision(candidate);integrated=revision(integrated)
        def f(s):
            t=self.task(s,wid,'reviewed')
            if t['candidate']!=candidate:raise Denied('stale integration candidate')
            self.recheck(t['submission'],kind='submission',task=wid,candidate=candidate,require_pass=True)
            self.recheck(t['review']['evidence'],kind='review',task=wid,candidate=candidate,require_pass=True)
            ref,e=self.evidence(record,'integration',wid,candidate,require_pass=True)
            if e.get('integrated_revision')!=integrated:raise Denied('integration head mismatch')
            if e.get('conflict_resolution_changed_semantics',False):raise Denied('semantic merge change requires new candidate and independent review')
            if not e.get('runtime_stopped'):raise Denied('must prove author runtime stopped before releasing edit lease')
            t['integration']={'actor':actor,'candidate':candidate,'integrated_revision':integrated,'evidence':ref};t['state']='integrated';t['lease']=None
        return self.change(actor,'record-integration',f,wid)
    def complete(self,wid,actor):
        def f(s):
            t=self.task(s,wid,'integrated');self.recheck(t['integration']['evidence'],kind='integration',task=wid,candidate=t['candidate'],require_pass=True)
            if self.work[wid]['activation']=='REQUIRES EXTERNAL VALIDATION':
                for gid in self.work[wid]['external_gates_for_activation']:
                    g=s['gates'].get(gid)
                    if not g or parse_time(g['expires_at'])<=self.clock():raise Denied('activation evidence missing/expired: '+gid)
                    e=self.recheck(g['evidence'],kind='gate',require_pass=True)
                    if wid not in e.get('work_packages',[]):raise Denied('gate evidence does not cover this work package: '+gid)
            t['state']='completed'
        return self.change(actor,'complete',f,wid)
    def block(self,wid,actor,record):
        def f(s):
            t=self.task(s,wid)
            if t['state'] in ('completed','cancelled'):raise Denied('terminal task cannot be blocked')
            ref,_=self.evidence(record,'checkpoint',wid);t['checkpoint']=ref;t['state']='blocked'
        return self.change(actor,'block',f,wid)
    def recover(self,wid,actor,record,cancel=False):
        def f(s):
            t=self.task(s,wid)
            if t['state'] in ('completed','cancelled','planned'):raise Denied('cannot recover terminal or never-admitted task')
            ref,e=self.evidence(record,'recovery',wid,require_pass=True)
            if e.get('runtime_stopped') is not True or e.get('previous_fence')!=t['fence']:raise Denied('recovery requires current fence and actual runtime-stop evidence')
            revision(e.get('observed_revision',''))
            t['history'].append({'candidate':t['candidate'],'assignment':t['assignment'],'submission':t['submission'],'review':t['review'],'integration':t['integration'],'recovery':ref})
            t.update(state='cancelled' if cancel else 'admitted',lease=None,assignment=None,candidate=None,submission=None,review=None,integration=None);t['fence']+=1
        return self.change(actor,'cancel' if cancel else 'recover',f,wid)
    def context(self,wid,out=None,max_bytes=200000):
        if wid not in self.work:raise Denied('unknown work package')
        w=self.work[wid];layers=json.loads((self.package/'07-agent-orchestration/context-routing.json').read_text())
        paths=list(dict.fromkeys(layers['kernel']+w['authoritative_references']+layers['always_for_assignment']))
        entries=[];total=0
        for p in paths:
            f=under(self.package,p);b=f.stat().st_size;total+=b
            entries.append({'path':p,'sha256':file_hash(f),'bytes':b})
        pack={'schema_version':'1.0','work_package_id':wid,'package_version':self.plan['package_version'],'work_package':w,'context_files':entries,'total_reference_bytes':total,'max_bytes':max_bytes,'status':'NEEDS_NARROWING' if total>max_bytes else 'READY','instructions':'Read referenced sections needed for this package; request a narrower approved context pack rather than silently truncate. Archive not included by default.'}
        if out:atomic_write(under(self.root,out,False),pack)
        return pack

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--package',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='cmd',required=True)
    for name in ['init','status','ready','check']:q=sub.add_parser(name);q.add_argument('--actor',default='human:owner')
    for name in ['set-roster','record-gate']:
        q=sub.add_parser(name);q.add_argument('--actor',required=True);q.add_argument('--record',required=True)
    q=sub.add_parser('set-budget');q.add_argument('--actor',required=True);q.add_argument('--record',required=True);q.add_argument('--usd',type=float,required=True)
    for name in ['admit','assign','start','checkpoint','submit','review','integrate','complete','block','recover','cancel','context']:
        q=sub.add_parser(name);q.add_argument('task');q.add_argument('--actor',default='astra')
        if name=='admit':q.add_argument('--trigger')
        if name=='assign':
            q.add_argument('--agent',required=True);q.add_argument('--tier',type=int,required=True);q.add_argument('--human',action='store_true');q.add_argument('--budget-usd',type=float,default=0);q.add_argument('--max-tokens',type=int,default=50000);q.add_argument('--max-seconds',type=int,default=3600)
        if name in ['start','checkpoint','submit']:q.add_argument('--fence',type=int,required=True)
        if name in ['checkpoint','submit','review','integrate','block','recover','cancel']:q.add_argument('--record',required=True)
        if name in ['submit','review','integrate']:q.add_argument('--candidate',required=True)
        if name=='checkpoint':q.add_argument('--extend-seconds',type=int,default=0)
        if name=='review':q.add_argument('--tier',type=int,required=True);q.add_argument('--human',action='store_true');q.add_argument('--reject',action='store_true')
        if name=='integrate':q.add_argument('--integrated',required=True)
        if name=='context':q.add_argument('--out');q.add_argument('--max-bytes',type=int,default=200000)
    a=p.parse_args(argv)
    try:
        h=Harness(a.root,a.package)
        if a.cmd=='init':r=h.init(a.actor)
        elif a.cmd in ['status','ready']:r=getattr(h,a.cmd)()
        elif a.cmd=='check':h.status();r={'integrity':'PASS','meaning':'local state/receipt integrity only; not production readiness'}
        elif a.cmd=='set-roster':r=h.roster(a.actor,a.record)
        elif a.cmd=='record-gate':r=h.gate(a.actor,a.record)
        elif a.cmd=='set-budget':r=h.budget(a.actor,a.usd,a.record)
        elif a.cmd=='admit':r=h.admit(a.task,a.actor,a.trigger)
        elif a.cmd=='assign':r=h.assign(a.task,a.actor,a.agent,a.tier,a.human,a.budget_usd,a.max_tokens,a.max_seconds)
        elif a.cmd=='start':r=h.start(a.task,a.actor,a.fence)
        elif a.cmd=='checkpoint':r=h.checkpoint(a.task,a.actor,a.fence,a.record,a.extend_seconds)
        elif a.cmd=='submit':r=h.submit(a.task,a.actor,a.fence,a.candidate,a.record)
        elif a.cmd=='review':r=h.review(a.task,a.actor,a.tier,a.candidate,a.record,not a.reject,a.human)
        elif a.cmd=='integrate':r=h.integrate(a.task,a.actor,a.candidate,a.integrated,a.record)
        elif a.cmd=='complete':r=h.complete(a.task,a.actor)
        elif a.cmd=='block':r=h.block(a.task,a.actor,a.record)
        elif a.cmd in ['recover','cancel']:r=h.recover(a.task,a.actor,a.record,a.cmd=='cancel')
        elif a.cmd=='context':r=h.context(a.task,a.out,a.max_bytes)
        else:raise Denied('unknown command')
        print(json.dumps(r if r is not None else {'ok':True},indent=2));return 0
    except (Denied,OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)},indent=2),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
