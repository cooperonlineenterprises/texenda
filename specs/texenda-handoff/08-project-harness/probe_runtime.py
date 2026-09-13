#!/usr/bin/env python3
"""Read-only local tool probe. Does not enumerate authenticated models or read credentials."""
import json, platform, shutil, subprocess, sys
from datetime import datetime, timezone

def main():
    results={}
    for tool in ('codex','node','pnpm','git','docker','python3'):
        path=shutil.which(tool)
        row={'present':bool(path),'path':path,'version':None}
        if path:
            try:
                r=subprocess.run([path,'--version'],capture_output=True,text=True,timeout=5,check=False)
                row['version']=(r.stdout or r.stderr).strip()[:300];row['exit_code']=r.returncode
            except (OSError,subprocess.TimeoutExpired) as e:row['error']=type(e).__name__
        results[tool]=row
    print(json.dumps({'observed_at':datetime.now(timezone.utc).isoformat(),'platform':platform.system(),'tools':results,'authenticated_model_roster':'UNVERIFIED','note':'Tool presence/public docs do not establish model entitlement, capability or price. No credential/environment variables read.'},indent=2))
if __name__=='__main__':main()
