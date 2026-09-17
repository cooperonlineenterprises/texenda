#!/usr/bin/env python3
"""Read-only composition of the one ADR-owned effective implementation plan.

This module reads repository sources only. It neither opens a ledger nor grants
permission or records acceptance. Its JSON output is a disposable projection.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

DECISION = 'docs/decisions/ADR-0008-integrated-initial-product-and-effective-plan.md'
SCHEMA = 'tooling/coordination/schemas/effective-plan.schema.json'
MARKER = '<!-- texenda-initial-product-contract -->'
PACKAGE = 'specs/texenda-handoff/'
BASES = {
    'sealed_catalog_sha256': (PACKAGE + '05-implementation/work-packages.json',
        '9ad162070c27e4c765ba145fc8a35d31dc288482453daaa39ec0bb6add8bd8d8'),
    'sealed_profiles_sha256': (PACKAGE + '06-migration-and-production/release-profiles.json',
        '869813ada7d0ea1a829cdad9204b35c67fd2631707fbbfbab50a315a3a3b8b15'),
    'sealed_acceptance_sha256': (PACKAGE + '06-migration-and-production/acceptance-catalog.json',
        'e6bf0bb96152e4fbcd9b4da13817f0a06ca4e57cd5502c4b329a4cc216ee7e58'),
}
WPS = {f'WP-{number:02}' for number in range(44)}
GATES = {f'VAL-{number:02}' for number in range(1, 15)}
EXTENSIONS = {f'AC-IP{number:02}' for number in range(1, 19)}
POST_ACTIVATION_CRITERIA = {'AC-M04', 'AC-M05', 'AC-M06', 'AC-M07', 'AC-M09'}
FORBIDDEN_SYNTHETIC = {'WP-17', 'WP-18', 'WP-20', 'WP-30', 'WP-33',
                       'WP-34', 'WP-35', 'WP-36', 'WP-37', 'WP-38', 'WP-42', 'WP-43'}


class PlanError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PlanError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    def reject_constant(value):
        raise PlanError('nonfinite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)


def relative_path(value):
    if (not isinstance(value, str) or not value or '\\' in value or '\x00' in value
            or value.startswith('/') or any(part in ('', '.', '..') for part in value.split('/'))
            or PurePosixPath(value).as_posix() != value):
        raise PlanError('unsafe repository path: ' + str(value))
    return value


def read_source(root, relative):
    """No-follow descriptor walk and stable regular-file read; never write."""
    parts = relative_path(relative).split('/')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    directory_flags = flags | os.O_DIRECTORY
    root = Path(root)
    if root.is_symlink() or '..' in root.parts or root.absolute() != root.resolve():
        raise PlanError('repository root must be canonical and non-symlink')
    descriptors = [os.open(root, directory_flags)]
    identities = [os.fstat(descriptors[0])]
    try:
        for part in parts[:-1]:
            descriptors.append(os.open(part, directory_flags, dir_fd=descriptors[-1]))
            identities.append(os.fstat(descriptors[-1]))
        fd = os.open(parts[-1], flags, dir_fd=descriptors[-1])
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise PlanError('source must be a regular file: ' + relative)
            raw = stream.read()
            after = os.fstat(stream.fileno())
        fields = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_size,
                                value.st_mtime_ns, value.st_ctime_ns)
        visible = os.stat(parts[-1], dir_fd=descriptors[-1], follow_symlinks=False)
        if fields(before) != fields(after) or fields(before) != fields(visible):
            raise PlanError('source changed during read: ' + relative)
        for index, part in enumerate([None, *parts[:-1]]):
            visible = (root.lstat() if index == 0 else
                       os.stat(part, dir_fd=descriptors[index - 1], follow_symlinks=False))
            opened = identities[index]
            if (visible.st_dev, visible.st_ino, visible.st_mode) != (opened.st_dev, opened.st_ino, opened.st_mode):
                raise PlanError('source directory changed during read: ' + relative)
        return raw
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def validate_schema(value, schema, document=None, location='$'):
    """Validate the deliberately small standard JSON Schema vocabulary we use.

    The checked-in schemas are the closed shape owner, not a second plan. Unknown
    schema keywords are rejected so an unsupported rule cannot silently disappear.
    """
    document = schema if document is None else document
    supported = {'$schema', '$id', '$defs', '$ref', 'title', 'description', 'type', 'const',
                 'enum', 'required', 'properties', 'additionalProperties', 'items',
                 'minItems', 'maxItems', 'uniqueItems', 'minLength', 'pattern', 'minimum'}
    if not isinstance(schema, dict) or set(schema) - supported:
        raise PlanError('unsupported schema vocabulary at ' + location)
    if '$ref' in schema:
        ref = schema['$ref']
        if not ref.startswith('#/$defs/') or ref[8:] not in document.get('$defs', {}):
            raise PlanError('unknown schema reference: ' + str(ref))
        return validate_schema(value, document['$defs'][ref[8:]], document, location)
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'integer': int, 'boolean': bool}
    if kind is not None and (kind not in types or type(value) is not types[kind]):
        raise PlanError('invalid ' + str(kind) + ' at ' + location)
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        raise PlanError('constant mismatch at ' + location)
    if 'enum' in schema and not any(type(value) is type(item) and value == item for item in schema['enum']):
        raise PlanError('unknown value at ' + location)
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        if set(schema.get('required', [])) - set(value):
            raise PlanError('missing fields at ' + location)
        if schema.get('additionalProperties') is False and set(value) - set(properties):
            raise PlanError('unknown fields at ' + location)
        for key in set(value) & set(properties):
            validate_schema(value[key], properties[key], document, location + '.' + key)
    if isinstance(value, list):
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', len(value)):
            raise PlanError('wrong list length at ' + location)
        if schema.get('uniqueItems') and len({canonical(item) for item in value}) != len(value):
            raise PlanError('duplicate list item at ' + location)
        for index, item in enumerate(value):
            if 'items' in schema:
                validate_schema(item, schema['items'], document, f'{location}[{index}]')
    if isinstance(value, str):
        if len(value.strip()) < schema.get('minLength', 0):
            raise PlanError('empty text at ' + location)
        if 'pattern' in schema and re.fullmatch(schema['pattern'], value) is None:
            raise PlanError('invalid text at ' + location)
    if type(value) is int and value < schema.get('minimum', value):
        raise PlanError('invalid integer at ' + location)


def keyed(rows, label):
    result = {}
    for row in rows:
        if row['id'] in result:
            raise PlanError('duplicate ' + label + ' ID: ' + row['id'])
        result[row['id']] = row
    return result


def closure(graph, roots, label):
    result, visiting = set(), set()
    def visit(node):
        if node not in graph:
            raise PlanError('unknown ' + label + ' reference: ' + str(node))
        if node in visiting:
            raise PlanError(label + ' cycle at ' + node)
        if node in result:
            return
        visiting.add(node)
        for child in graph[node]:
            visit(child)
        visiting.remove(node)
        result.add(node)
    for root in roots:
        visit(root)
    return result


def patch_rows(rows, updates, label):
    mapping = keyed(rows, label)
    keyed(updates, label + ' update')
    for update in updates:
        identifier = update['id']
        if identifier not in mapping:
            raise PlanError('unknown ' + label + ' update: ' + identifier)
        row = mapping[identifier]
        if set(update['replace']) & set(update['append']):
            raise PlanError('replace/append overlap: ' + identifier)
        for field, value in update['replace'].items():
            if field not in row:
                raise PlanError('replacement of absent field: ' + field)
            row[field] = copy.deepcopy(value)
        for field, additions in update['append'].items():
            if field not in row:
                raise PlanError('append to absent field: ' + field)
            if isinstance(row[field], str):
                row[field] = ' '.join([row[field], *additions])
            elif isinstance(row[field], list):
                if any(item in row[field] for item in additions):
                    raise PlanError('duplicate appended item: ' + identifier + '.' + field)
                row[field].extend(copy.deepcopy(additions))
            else:
                raise PlanError('unsupported append field: ' + field)
    return mapping


class EffectivePlan:
    def __init__(self, contract, catalog, profiles, acceptance, source_refs):
        self.contract, self.catalog, self.profiles, self.acceptance = contract, catalog, profiles, acceptance
        self.source_refs = source_refs
        self.changed_work_packages = sorted(row['id'] for row in contract['work_package_updates'])
        self.work = keyed(catalog['work_packages'], 'work package')
        self.release_profiles = keyed(profiles['profiles'], 'profile')
        self.digest = digest({'contract': contract, 'catalog': catalog, 'profiles': profiles,
                              'acceptance': acceptance})

    def profile_closure(self, identifier):
        ancestors = closure({key: row['parents'] for key, row in self.release_profiles.items()},
                            [identifier], 'profile')
        rows = [self.release_profiles[key] for key in sorted(ancestors)]
        packages = closure({key: row['dependencies'] for key, row in self.work.items()},
                           [wid for row in rows for wid in row['requires_work_packages']], 'work package')
        return {'id': identifier, 'profiles': sorted(ancestors), 'work_packages': sorted(packages),
                'required_criteria': sorted({value for row in rows for value in row['required_criteria']}),
                'requires_gates': sorted({value for row in rows for value in row['requires_gates']}),
                'evidence_mode': self.release_profiles[identifier].get('evidence_mode', 'real-qualified'),
                'requirements_by_profile': [
                    {'id': row['id'], 'evidence_mode': row.get('evidence_mode', 'real-qualified'),
                     'required_criteria': row['required_criteria'], 'requires_gates': row['requires_gates']}
                    for row in rows],
                'evidence_status': 'NOT_ASSESSED',
                'meaning': 'Requirements only. Synthetic evidence never passes real acceptance or external gates.'}

    def summary(self):
        return {'id': self.contract['id'], 'effective_plan_digest': self.digest,
                'source_refs': self.source_refs, 'work_packages': len(self.work),
                'changed_work_packages': self.changed_work_packages,
                'acceptance_extensions': len(self.contract['acceptance_extensions']),
                'additional_profiles': len(self.contract['additional_profiles']),
                'profiles': [self.profile_closure(row['id']) for row in self.contract['additional_profiles']],
                'requires_explicit_activation': True, 'live_state_checked': False,
                'product_implementation': 'NOT_ASSESSED'}


def load_plan(root):
    root = Path(root).absolute()
    refs = []
    def source(path):
        raw = read_source(root, path)
        refs.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        return raw
    adr = source(DECISION).decode('utf-8')
    if adr.count(MARKER) != 1:
        raise PlanError('exactly one marked effective-plan contract block required')
    blocks = re.findall(re.escape(MARKER) + r'\s*```json\s*\n(.*?)\n```', adr, re.DOTALL)
    if len(blocks) != 1 or len(re.findall(r'^```json\s*$', adr, re.MULTILINE)) != 1:
        raise PlanError('missing or duplicate machine JSON block')
    contract = load_json(blocks[0])
    schema = load_json(source(SCHEMA))
    validate_schema(contract, schema)
    documents = []
    for pin, (path, expected) in BASES.items():
        raw = source(path)
        if contract[pin] != expected or hashlib.sha256(raw).hexdigest() != expected:
            raise PlanError('sealed base hash mismatch: ' + path)
        documents.append(load_json(raw))
    catalog, profiles, acceptance = copy.deepcopy(documents)
    base_work = keyed(documents[0]['work_packages'], 'sealed work package')
    base_profiles = keyed(documents[1]['profiles'], 'sealed profile')
    criteria = keyed(acceptance['criteria'], 'sealed criterion')
    if set(base_work) != WPS or len(criteria) != 125:
        raise PlanError('sealed catalog/acceptance identity mismatch')
    work = patch_rows(catalog['work_packages'], contract['work_package_updates'], 'work package')
    extensions = keyed(contract['acceptance_extensions'], 'extension')
    if set(extensions) != EXTENSIONS or set(extensions) & set(criteria):
        raise PlanError('acceptance extension IDs must be AC-IP01 through AC-IP18')
    for row in extensions.values():
        if not set(row['work_packages']) <= WPS or not set(row['sealed_criteria']) <= set(criteria):
            raise PlanError('unknown extension reference: ' + row['id'])
    acceptance['criteria'].extend(copy.deepcopy(contract['acceptance_extensions']))
    all_criteria = set(criteria) | set(extensions)
    for row in work.values():
        if not set(row['acceptance_ids']) <= all_criteria:
            raise PlanError('unknown work-package acceptance ID: ' + row['id'])
        if not set(row['external_gates_for_activation']) <= GATES:
            raise PlanError('unknown work-package gate: ' + row['id'])
        for path in row['allowed_paths']:
            relative_path(path)
        for path in row['authoritative_references']:
            read_source(root, PACKAGE + relative_path(path))
        if row['id'] != 'WP-32' and not set(base_work[row['id']]['external_gates_for_activation']) <= set(row['external_gates_for_activation']):
            raise PlanError('sealed work-package gate removed: ' + row['id'])
    closure({key: row['dependencies'] for key, row in work.items()}, WPS, 'work package')
    additional = keyed(contract['additional_profiles'], 'additional profile')
    if set(additional) != {'initial-synthetic', 'initial-production'} or set(additional) & set(base_profiles):
        raise PlanError('unexpected additional profile IDs')
    profiles['profiles'].extend(copy.deepcopy(contract['additional_profiles']))
    if [row['id'] for row in contract['profile_updates']] != [
            'email-pilot', 'assisted-workspace', 'external-agent']:
        raise PlanError('only the three named initial component profiles are amended')
    merged_profiles = patch_rows(profiles['profiles'], contract['profile_updates'], 'profile')
    for row in merged_profiles.values():
        if (not set(row['requires_work_packages']) <= WPS
                or not set(row['required_criteria']) <= all_criteria
                or not set(row['requires_gates']) <= GATES):
            raise PlanError('unknown profile requirement: ' + row['id'])
    plan = EffectivePlan(contract, catalog, profiles, acceptance, refs)
    for identifier in merged_profiles:
        plan.profile_closure(identifier)
    synthetic = plan.profile_closure('initial-synthetic')
    production = plan.profile_closure('initial-production')
    pilot = plan.profile_closure('email-pilot')
    initial_real_criteria = set().union(*(set(base_profiles[key]['required_criteria'])
        for key in ('email-pilot', 'mature-email', 'assisted-workspace', 'external-agent')))
    initial_real_criteria -= POST_ACTIVATION_CRITERIA
    for identifier, parents in (('assisted-workspace', ['initial-production']),
                                ('external-agent', ['assisted-workspace'])):
        component = merged_profiles[identifier]
        if component['parents'] != parents or any(
                component[key] != base_profiles[identifier][key]
                for key in ('required_criteria', 'requires_gates', 'requires_work_packages')):
            raise PlanError('initial component profile ancestry or own obligations changed')
        if {'WP-20', 'WP-33'} & set(plan.profile_closure(identifier)['work_packages']):
            raise PlanError('initial interaction profile depends on later rollout')
    if (merged_profiles['voice'] != base_profiles['voice']
            or merged_profiles['mature-email'] != base_profiles['mature-email']):
        raise PlanError('optional voice or mature-email obligations changed')
    if (set(contract['synthetic_forbidden_dependencies']) != FORBIDDEN_SYNTHETIC
            or set(synthetic['work_packages']) & FORBIDDEN_SYNTHETIC
            or synthetic['requires_gates'] or additional['initial-synthetic']['parents']
            or synthetic['evidence_mode'] != 'synthetic'
            or set(synthetic['required_criteria']) != EXTENSIONS - {'AC-IP17', 'AC-IP18'}):
        raise PlanError('synthetic stage crosses real qualification boundary')
    if (additional['initial-production']['parents'] != ['initial-synthetic']
            or production['evidence_mode'] != 'real-qualified'
            or not (set(base_profiles['email-pilot']['requires_gates']) | {'VAL-09', 'VAL-11'}) <= set(production['requires_gates'])
            or not initial_real_criteria <= set(production['required_criteria'])
            or POST_ACTIVATION_CRITERIA & set(production['required_criteria'])
            or not set(base_profiles['email-pilot']['required_criteria']) <= set(pilot['required_criteria'])
            or 'WP-20' not in pilot['work_packages']
            or not (EXTENSIONS - {'AC-IP18'}) <= set(production['required_criteria'])
            or 'AC-IP18' in production['required_criteria']
            or 'AC-IP18' in work['WP-17']['acceptance_ids']
            or merged_profiles['email-pilot']['parents'] != ['initial-production']):
        raise PlanError('initial production cannot bypass real qualification or baseline gates')
    if ('WP-15' not in work['WP-12']['dependencies']
            or set(work['WP-18']['acceptance_ids']) != {'AC-M01', 'AC-M02', 'AC-IP11', 'AC-IP12'}):
        raise PlanError('acquisition approval or discovery stage boundary mismatch')
    if (work['WP-32']['external_gates_for_activation']
            or work['WP-32']['activation'] != 'AUTHORITATIVE DECISION'
            or any(not {'VAL-09', 'VAL-11'} <= set(work[wid]['external_gates_for_activation'])
                   for wid in ('WP-17', 'WP-20', 'WP-33', 'WP-42'))):
        raise PlanError('synthetic/real work-package gate boundary mismatch')
    # A complete second read rejects source changes while the projection was built.
    for ref in refs:
        raw = read_source(root, ref['path'])
        if hashlib.sha256(raw).hexdigest() != ref['sha256'] or len(raw) != ref['bytes']:
            raise PlanError('plan source changed during composition: ' + ref['path'])
    return plan


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--json', action='store_true', help='emit the disposable effective projection')
    args = parser.parse_args(argv)
    try:
        plan = load_plan(args.root)
        value = plan.summary()
        value['integrity'] = 'PASS'
        if args.json:
            value.update(contract=plan.contract, catalog=plan.catalog,
                         release_profiles=plan.profiles, acceptance=plan.acceptance)
        print(json.dumps(value, indent=2, sort_keys=True))
        return 0
    except (PlanError, OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({'integrity': 'FAIL', 'reason': str(exc)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
