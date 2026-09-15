#!/usr/bin/env python3
"""Read-only interpretation of Texenda's mapped-existing adoption contract.

The ordinary self-check uses repository-owned contracts only. Maintenance mode
accepts a stock 1.0.0 planner observation on stdin; it never runs that planner,
follows an origin source path, writes output files, qualifies a source, creates
a migration seed, or adopts/upgrades a Blueprint.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path, PurePosixPath
import stat
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.agent/scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as facade
import validate_contract as contract
from common import (ValidationError, load_json, loads, require,
                    reject_private_name, resolved_directory, sha, stable_file_bytes)

ORIGIN = '.project-blueprint-origin.json'
MAX_STOCK_BYTES = 1024 * 1024
STOCK_FIELDS = {
    'schema_version', 'authority', 'target', 'requested_profile', 'blueprint_version',
    'existing', 'origin', 'existing_top_level_names', 'collisions',
    'candidate_new_paths', 'required_sequence', 'non_transfer_rules',
}
ARCHIVE_INDEX = contract.HOME + '/archive/checkpoints/'


def strict_json(raw):
    """Also reject exponent overflow, which JSON parse_constant does not see."""
    value = loads(raw)

    def finite(item):
        if isinstance(item, float):
            require(math.isfinite(item), 'nonfinite JSON number')
        elif isinstance(item, dict):
            for child in item.values():
                finite(child)
        elif isinstance(item, list):
            for child in item:
                finite(child)

    finite(value)
    return value


def relative_name(value):
    require(isinstance(value, str) and bool(value), 'path must be a nonempty string')
    reject_private_name(value, 'planner path')
    require(not PurePosixPath(value).is_absolute()
            and not any(character in value for character in ('\\', ':', '\x00', '\n', '\r'))
            and all(part not in ('', '.', '..', '.git', '.texenda', 'private-inputs')
                    for part in value.split('/')),
            'planner path is not a confined repository-relative path')
    return value


def presence(root, name):
    """Inspect only named path metadata; never follow a symlink or read content."""
    parts = relative_name(name).split('/')
    path = root
    for index, part in enumerate(parts):
        path = path / part
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            return False
        require(not stat.S_ISLNK(mode), 'planner path contains a symlink')
        require(stat.S_ISREG(mode) or stat.S_ISDIR(mode), 'planner path is not regular')
        require(index == len(parts) - 1 or stat.S_ISDIR(mode),
                'planner path has a non-directory parent')
    return True


def local_contract(root):
    reject_private_name(str(root), 'repository root')
    require(not {'.git', '.texenda'} & set(Path(root).parts), 'local state is not a repository root')
    root = resolved_directory(Path(root), 'repository root')
    sources = {name: stable_file_bytes(root / name, 'interpretation source')
               for name in (ORIGIN, contract.CROSSWALK)}
    for raw in sources.values():
        strict_json(raw)
    # These functions are imported from this interpreter's own repository,
    # never from a path in stdin or the origin record.
    origin = facade.validate_origin(root)
    crosswalk = facade.validate_crosswalk_correction(root)
    require(presence(root, 'specs/texenda-handoff/01-foundation/authority-register.json'),
            'sealed topic-owner register is missing')
    contract.validate(crosswalk, load_json(root / contract.BASELINE),
                      load_json(root / contract.MANIFEST), root=root)
    require(origin['adoption_contract'] == contract.CROSSWALK
            and crosswalk['blueprint']['selected_source'] == origin['selected_source']
            and crosswalk['blueprint']['selected_version'] == origin['selected_version']
            and crosswalk['profile'] == origin['profile'],
            'origin and crosswalk selection disagree')
    inventory = crosswalk['blueprint_path_inventory']
    require(isinstance(inventory, list) and len(inventory) == len(set(inventory)) == 85,
            'crosswalk must map all 85 selected planner paths exactly once')
    rows = crosswalk['mappings']
    require(isinstance(rows, list) and len(rows) == 85
            and sorted(row['blueprint_path'] for row in rows) == sorted(inventory),
            'missing, extra or duplicate crosswalk mapping')
    observed = {}
    for row in rows:
        require(row['role'] in contract.ROLES, 'unknown mapping role')
        name = relative_name(row['blueprint_path'])
        mapped = row['mapped_path']
        if mapped is None:
            require(row['role'] in {'deferred', 'not_applicable'}, 'missing required mapping')
        elif isinstance(mapped, str) and mapped.startswith('/'):
            require(mapped == ARCHIVE_INDEX and row['role'] == 'historical_source',
                    'mapping escapes the repository or permitted archive index')
            # The sole external mapping is an index. Do not inspect archive content.
        else:
            require(isinstance(mapped, str) and bool(mapped), 'mapping path is malformed')
            presence(root, relative_name(mapped.rstrip('/')))
        observed[name] = 'collision' if presence(root, name) else 'candidate_new'
    require(all(stable_file_bytes(root / name, 'interpretation source') == raw
                for name, raw in sources.items()), 'interpretation sources changed during check')
    return root, origin, crosswalk, observed, sources


def validate_stock(plan, root, origin, observed):
    require(isinstance(plan, dict) and set(plan) == STOCK_FIELDS,
            'stock plan is not the closed supported observation shape')
    require(plan['schema_version'] == 'project-blueprint.adoption-plan.v1',
            'unknown stock planner schema')
    require(plan['target'] == str(root), 'stock target differs from the explicit repository root')
    require(plan['requested_profile'] == origin['profile'] == 'high-assurance',
            'stock profile differs from the selected profile')
    require(plan['blueprint_version'] == origin['selected_version'] == '1.0.0',
            'stock version differs from the selected structural reference')
    require(plan['origin'] == {
        'status': 'valid_shape_not_fully_validated', 'blueprint_version': None,
        'profile': 'high-assurance', 'harness_kernel_version': None,
    }, 'stock origin observation differs from the selected planner limitation')
    require(isinstance(plan['authority'], str), 'stock authority observation must be text')
    for key in ('existing_top_level_names', 'required_sequence', 'non_transfer_rules'):
        require(isinstance(plan[key], list) and all(isinstance(item, str) for item in plan[key]),
                'stock observation list is malformed: ' + key)
    require(isinstance(plan['existing'], dict), 'stock existing observation must be an object')
    partitions = []
    for field, kind in (('collisions', 'collision'), ('candidate_new_paths', 'candidate_new')):
        paths = plan[field]
        require(isinstance(paths, list) and all(isinstance(item, str) for item in paths),
                'stock path partition must be a string array')
        require(len(paths) == len(set(paths)), 'duplicate stock path')
        for name in paths:
            relative_name(name)
        partitions.append(set(paths))
        require(set(paths) == {name for name, value in observed.items() if value == kind},
                'stock partition is stale, missing, extra, overlapping or misclassified: ' + field)
    require(not partitions[0] & partitions[1]
            and partitions[0] | partitions[1] == set(observed),
            'stock partitions must cover exactly the mapped inventory without overlap')


def interpret(root, stock_plan=None):
    root, origin, crosswalk, observed, sources = local_contract(root)
    if stock_plan is not None:
        validate_stock(stock_plan, root, origin, observed)
    rows = [{key: row[key] for key in ('blueprint_path', 'mapped_path', 'concern_id',
                                      'role', 'equivalence', 'reason')}
            | {'observed_path_state': observed[row['blueprint_path']]}
            for row in crosswalk['mappings']]
    return {
        'schema_version': 'texenda.adoption-interpretation.v1',
        'status': 'PASS',
        'scope': 'current local origin/crosswalk consistency and exact path partition only',
        'repository_root': str(root),
        'source_hashes': {name: sha(raw) for name, raw in sources.items()},
        'current_epoch': crosswalk['current_epoch'],
        'selected_reference': {
            'version': origin['selected_version'], 'profile': origin['profile'],
            'adoption_mode': origin['adoption_mode'],
            'qualification': origin['reference_qualification'],
            'descriptor_sha256': origin['selected_reference_descriptor_sha256'],
        },
        'clean_candidate_observation': {
            key: origin['clean_candidate'][key] for key in
            ('committed_version', 'revision', 'tree', 'qualified', 'adopted', 'qualification_checks')
        },
        'dirty_candidate_observation': {
            key: origin['dirty_checkout_observation'][key] for key in
            ('working_version', 'version_committed', 'qualified', 'adopted')
        },
        'stock_plan_validated': stock_plan is not None,
        'stock_origin_observation': stock_plan['origin'] if stock_plan is not None else None,
        'counts': {'mapped_paths': len(rows), **dict(Counter(observed.values()))},
        'roles': dict(sorted(Counter(row['role'] for row in rows).items())),
        'mapped_dispositions': rows,
        'boundary': {
            'authority': 'derived_non_authoritative_view', 'permission_grant': False,
            'writes': False, 'executes_source_or_planner': False,
            'qualifies_blueprint': False, 'adopts_or_upgrades': False,
            'manufactures_seed': False, 'reads_private_content': False,
            'imports_project_facts': False,
        },
        'freshness': 'Re-run for changed source hashes or path membership; no saved view is live authority.',
        'limitations': [
            'Stock origin is retained as an observation; local v3 interpretation does not repair the stock planner.',
            'Selected 1.0.0 remains structural only; clean 4.2.0 remains PASS/PASS/FAIL; dirty 4.3.0 is uncommitted.',
            'No reviewed upgrade seed exists and no upgrade is approved or applied.',
            'No explicit writes; OS-managed atime may advance on read.',
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path,
                        help='Explicit canonical absolute repository directory.')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='Offline repository-owned self-check.')
    mode.add_argument('--stock-plan', choices=('-',), help='Read stock planner JSON only from stdin.')
    args = parser.parse_args(argv)
    try:
        plan = None
        if args.stock_plan:
            raw = sys.stdin.buffer.read(MAX_STOCK_BYTES + 1)
            require(len(raw) <= MAX_STOCK_BYTES, 'stock plan exceeds the one-MiB input bound')
            plan = strict_json(raw)
            require(isinstance(plan, dict), 'stock plan must be a JSON object')
        result = interpret(args.root, plan)
        if args.check:
            result = {key: result[key] for key in (
                'schema_version', 'status', 'scope', 'source_hashes', 'current_epoch',
                'selected_reference', 'counts', 'roles', 'boundary', 'limitations')}
    except (ValidationError, contract.ContractError, ValueError, OSError, KeyError,
            TypeError, AttributeError, StopIteration, RecursionError) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc), 'writes': False}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
