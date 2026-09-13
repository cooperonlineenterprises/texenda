#!/usr/bin/env python3
"""Offline structural/traceability/link checker for the handoff; not application acceptance.

Standard library only. Optional --write-report writes this check's result; --checksums
verifies finalized SHA256SUMS without updating files. No network or production calls.
"""
from __future__ import annotations
import argparse, ast, hashlib, json, re, sys
from pathlib import Path
from urllib.parse import unquote
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def slug(s):
    s=re.sub(r'<[^>]*>','',s).strip().lower();s=re.sub(r'[^\w\s\-]','',s);return re.sub(r'\s','-',s)
def files():return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write-report',type=Path);ap.add_argument('--checksums',action='store_true');args=ap.parse_args()
    checks=[];errors=[];warnings=[]
    def check(name,fn):
        before=len(errors)
        try:fn()
        except Exception as e:errors.append(name+': '+str(e))
        checks.append({'check':name,'status':'PASS' if len(errors)==before else 'FAIL'})
    def require(condition,message):
        if not condition:raise ValueError(message)
    def jsons():
        for p in files():
            if p.suffix=='.json':json.loads(p.read_text())
    check('JSON parse',jsons)
    def originals():
        for r in load('09-reference/original-artifact-integrity.json'):
            p=ROOT/r['path'];require(p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'prior artifact changed: '+r['path'])
    check('Prior artifacts byte integrity',originals)
    auth=load('01-foundation/authority-register.json');wps=load('05-implementation/work-packages.json')['work_packages'];wd={w['id']:w for w in wps}
    acs=load('06-migration-and-production/acceptance-catalog.json')['criteria'];ad={a['id']:a for a in acs}
    invs=load('01-foundation/invariant-index.json')['invariants'];iv={a['id']:a for a in invs}
    gates=load('01-foundation/external-validation-gates.json')['gates'];gd={g['id']:g for g in gates}
    def authority():
        require(auth['decision_required_now']==[],'unresolved immediate decision')
        expected={'AUTHORITATIVE DECISION','DECISION REQUIRED NOW','REVERSIBLE DEFAULT','DEFER UNTIL TRIGGERED','REQUIRES EXTERNAL VALIDATION'}
        require(set(auth['decision_status_vocabulary'])==expected,'decision status vocabulary drift')
        owners=auth['current_normative_owners'];require(len({o['topic'] for o in owners})==len(owners),'duplicate topic authority')
        for o in owners:require((ROOT/o['path']).is_file(),'missing owner '+o['path'])
        require(len(gd)==14,'external gate lost/duplicated')
        for g in gates:require(g['status']=='REQUIRES EXTERNAL VALIDATION' and g['evidence_status']=='UNVERIFIED','unverified gate represented as cleared '+g['id'])
    check('Decision status and authority ownership',authority)
    def graph():
        require(len(wd)==44,'WP lost/duplicated')
        done=set();visiting=set()
        def visit(w):
            if w in visiting:raise ValueError('dependency cycle '+w)
            if w in done:return
            require(w in wd,'missing dependency '+w);visiting.add(w)
            for d in wd[w]['dependencies']:visit(d)
            visiting.remove(w);done.add(w)
        for w in wd:visit(w)
        for w in wps:
            for fld in ('objective','scope','inputs','expected_outputs','acceptance_criteria','verification_requirements','handoff_requirements'):require(bool(w.get(fld)),'missing WP contract '+w['id']+' '+fld)
            require(w['recommended_model_tier'] in [1,2,3] and w['independent_review_tier'] in [1,2,3],'invalid tier')
            if w['risk_level'] in ('high','critical'):require(w['independent_review_tier']==1,'missing strong independent review '+w['id'])
            for r in w['authoritative_references']:require((ROOT/r).is_file(),'missing WP context '+r)
            for g in w['external_gates_for_activation']:require(g in gd,'unknown gate '+g)
            for a in w['acceptance_ids']:require(a in ad,'unknown acceptance '+a)
            for p in w['allowed_paths']:require(not p.startswith('/') and '..' not in p.split('/') and '\\' not in p,'unsafe WP path '+p)
        require('WP-32' not in wd['WP-42']['dependencies'],'voice/AI incorrectly made mandatory for mature email')
        require('WP-07' in wd['WP-11']['dependencies'],'journal not before live-effect executor')
        require('WP-15' in wd['WP-27']['dependencies'],'proposal infra not before writable AI')
    check('WP DAG, bounded contracts, gates and routing',graph)
    def trace():
        require(len(ad)==125 and len(iv)==30,'acceptance/invariant count mismatch')
        for a in acs:
            require(a['execution_status']=='NOT RUN' and not a['evidence'],'package falsely implies product test passed')
            require(bool(a['exercise']) and bool(a['pass_condition']),'missing test oracle')
            for i in a['invariants']:require(i in iv,'unknown invariant '+i)
            for w in a['work_packages']:require(w in wd,'unknown test WP '+w)
            require((ROOT/a['source']).is_file(),'test source missing')
        ts=load('10-validation/requirement-traceability.json')['invariants']
        require({r['requirement_id'] for r in ts}==set(iv),'traceability misses invariant')
        for r in ts:require(bool(r['acceptance_ids'] or r['harness_tests']),'uncovered invariant '+r['requirement_id'])
    check('Acceptance and requirement traceability, no product PASS',trace)
    def profiles():
        rows=load('06-migration-and-production/release-profiles.json')['profiles'];pd={p['id']:p for p in rows}
        visiting=set();done=set()
        def rec(i):
            require(i in pd,'unknown profile');require(i not in visiting,'profile cycle')
            if i in done:return
            visiting.add(i)
            for x in pd[i]['parents']:rec(x)
            visiting.remove(i);done.add(i)
        for p in rows:
            rec(p['id'])
            for a in p['required_criteria']:require(a in ad,'unknown profile criterion '+a)
            for g in p['requires_gates']:require(g in gd,'unknown profile gate '+g)
            for w in p['requires_work_packages']:require(w in wd,'unknown profile WP '+w)
    check('Release profile closure',profiles)
    def commands():
        rows=load('03-domain-and-architecture/command-catalog.json')['commands'];require(len({r['name'] for r in rows})==49,'command count/duplicate')
        for r in rows:
            require(r['risk_class'] in ['C0','C1','C2','C3','C4'],'risk class drift')
            require(bool(r['required_capability']) and bool(r['actor_types']),'missing command authority')
            if r['name'] in ('ReleaseSafetyHold','ActivateDelegation','TransferSendingAuthority','ReleaseRecoveryHold'):require(r['actor_types']==['human'],'AI/agent privileged authority exposed')
            if r['name'] in ('AssignTag','SetAttribute'):require('consequence_dependent' in r['approval'],'transitive-effect risk not reviewed')
    check('Command authority metadata',commands)
    def adr():
        s=(ROOT/'01-foundation/adr-set.md').read_text();blocks=re.split(r'(?=#### ADR-)',s)[1:]
        require(len(blocks)==35,'ADR count drift')
        for b in blocks:
            for term in ['Decision','Status','Context','Chosen approach','Material alternatives','Why chosen','Consequences','What remains reversible','Revisit trigger','Dependencies']:
                require(term in b,'ADR field absent '+b.splitlines()[0]+' '+term)
    check('ADR required fields',adr)
    def model():
        m=load('07-agent-orchestration/model-routing.json');require(m['target_roster_status']=='UNVERIFIED','target roster falsely qualified');require(all(v is None for v in m['active_bindings'].values()),'unverified active model binding');require(m['new_api_spend_authorized_usd']==0,'spending authorized by package')
        probe=load('10-validation/packaging-runtime-probe.json');require(probe['authenticated_model_roster']=='UNVERIFIED','probe implies authenticated models')
    check('Model availability and spending truth',model)
    def no_runner():
        tree=ast.parse((ROOT/'08-project-harness/harness.py').read_text());bad={'socket','requests','httpx','openai','subprocess'}
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):require(not any(a.name.split('.')[0] in bad for a in n.names),'harness contains external runner/network import')
            if isinstance(n,ast.ImportFrom):require((n.module or '').split('.')[0] not in bad,'harness contains external runner/network import')
    check('Harness non-runner boundary (static)',no_runner)
    def source():
        ss=load('09-reference/source-register.json')['sources'];require(len({x['id'] for x in ss})==len(ss),'source IDs duplicate')
        for r in ss:require(bool(r['urls']) and bool(r['current_validation']),'source lacks evidence status')
        c=load('09-reference/conversation-record.json');require('PARTIAL' in c['coverage'],'archive overstates fidelity')
        require(auth['source_archive_complete_verbatim'] is False,'verbatim completion falsely claimed')
        ids=[r['id'] for r in c['records']];require(len(ids)==len(set(ids)) and len(ids)>=25,'conversation lineage missing')
    check('Source/archive provenance',source)
    def links():
        for p in files():
            if p.suffix!='.md' or 'prior-artifacts' in p.parts:continue
            raw=p.read_text();raw=re.sub(r'```.*?```','',raw,flags=re.S)
            for match in re.finditer(r'\[[^\]\n]+\]\(([^)\n]+)\)',raw):
                link=match[1].strip().split(' "')[0].strip('<>')
                if re.match(r'^(https?://|mailto:|urn:)',link):continue
                if link.startswith('sandbox:'):raise ValueError('stale sandbox link in normative/current doc '+str(p.relative_to(ROOT)))
                path,_,anchor=link.partition('#');target=(p.parent/unquote(path)).resolve() if path else p
                try:target.relative_to(ROOT)
                except ValueError:raise ValueError('link escapes package '+link+' in '+str(p.relative_to(ROOT)))
                require(target.exists(),'broken link '+link+' in '+str(p.relative_to(ROOT)))
                if anchor and target.is_file() and target.suffix=='.md':
                    body=target.read_text();ids=set(re.findall(r'id=[\"\']([^\"\']+)',body));ids|={slug(h) for h in re.findall(r'^#+\s+(.+)$',body,re.M)}
                    require(unquote(anchor) in ids,'broken anchor '+link+' in '+str(p.relative_to(ROOT)))
    check('Current Markdown local links and anchors',links)
    def manifest():
        m=load('manifest.json')['artifacts'];actual={str(p.relative_to(ROOT)) for p in files()};listed={r['path'] for r in m}
        require(len(m)==len(listed),'duplicate manifest entry');require(actual==listed,'manifest mismatch: missing '+str(sorted(actual-listed))+' extra '+str(sorted(listed-actual)))
        for r in m:
            for k in ('purpose','authority_level','primary_consumers','dependencies'):require(k in r,'manifest field absent')
            for d in r['dependencies']:require(d in actual,'missing manifest dependency '+d)
    check('Manifest completeness',manifest)
    if args.checksums:
        def sums():
            rows=(ROOT/'SHA256SUMS').read_text().splitlines();seen=set()
            for row in rows:
                val,path=row.split('  ',1);require(path not in seen,'duplicate checksum');seen.add(path);p=ROOT/path;require(p.is_file() and sha(p)==val,'checksum mismatch '+path)
            require(seen=={str(p.relative_to(ROOT)) for p in files() if p.name!='SHA256SUMS'},'checksum coverage mismatch')
        check('Final package checksums',sums)
    report={'package_version':'1.1.0','checked_at':datetime.now(timezone.utc).isoformat(),'result':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'warnings':warnings,'counts':{'files':len(files()),'work_packages':len(wps),'product_acceptance_criteria':len(acs),'invariants':len(invs),'adrs':35,'external_gates':len(gates)},'scope':'Offline package structure/traceability/link checks only. Synthetic harness unit tests reported separately. No application/production/provider/security/legal qualification performed.','archive_limitation':'No complete verbatim conversation export; exact prior artifacts plus explicitly abridged turn record.'}
    if args.write_report:
        path=args.write_report if args.write_report.is_absolute() else ROOT/args.write_report;path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
