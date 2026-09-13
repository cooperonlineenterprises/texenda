#!/usr/bin/env python3
"""Dry-run-first installer for an empty Texenda repo. No git, network, model or app installation."""
import argparse, shutil, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--target',type=Path,required=True);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
    source=Path(__file__).resolve().parents[1];target=a.target.absolute()
    # Reject symlink ancestors and source/target nesting to avoid overwrite/recursive copy.
    for p in [target,*target.parents]:
        if p.is_symlink():ap.error('symlink target/ancestor forbidden')
    target=target.resolve()
    if source==target or source in target.parents or target in source.parents:ap.error('source and target must not contain each other')
    if target.exists():
        if not target.is_dir():ap.error('target is not a directory')
        extra=[p.name for p in target.iterdir() if p.name!='.git']
        if extra:ap.error('target must be empty or .git-only; found: '+', '.join(extra[:8]))
    print('Target:',target,'\nCopy package → specs/texenda-handoff\nWrite AGENTS.md, .gitignore and .codex/config.toml.example\nNo application implementation or dependencies installed.')
    if not a.apply:
        print('DRY RUN only. Re-run with --apply after review.');return 0
    target.mkdir(parents=True,exist_ok=True)
    dest=target/'specs/texenda-handoff'
    shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.texenda'))
    text=(source/'08-project-harness/root-AGENTS.md.template').read_text().replace('<HANDOFF_ROOT>','specs/texenda-handoff')
    (target/'AGENTS.md').write_text(text)
    (target/'.codex').mkdir();shutil.copy2(source/'08-project-harness/codex-config.toml.example',target/'.codex/config.toml.example')
    (target/'.gitignore').write_text('.texenda/\n.env\n.env.*\n!.env.example\nnode_modules/\n__pycache__/\n*.pyc\n')
    print('Installed. Read specs/texenda-handoff/README.md and start WP-00.');return 0
if __name__=='__main__':sys.exit(main())
