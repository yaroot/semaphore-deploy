#!/usr/bin/env python

from __future__ import division, print_function

import json
import click
from requests import Session

requests = Session()


def lookup_project(addr, token, name):
    r = requests.get(addr + '/api/projects', headers={'Authorization': 'Bearer ' + token})

    def f(p): return p['name'] == name

    projects = filter(f, r.json())
    if len(projects) == 0:
        assert False, "Can't find project named <{}>".format(name)
    elif len(projects) > 1:
        assert False, "Found more than 1 project named <{}>".format(name)
    return projects[0]['id']


def lookup_template(addr, token, project_id, name):
    r = requests.get(addr + '/api/project/{}/templates'.format(project_id),
                     headers={'Authorization': 'Bearer ' + token})

    def f(t):
        return 'alias' in t and t['alias'] == name

    templates = filter(f, r.json())
    if len(templates) == 0:
        assert False, "Can't find template named <{}>".format(name)
    elif len(templates) > 1:
        assert False, "Found more then 1 template named <{}>".format(name)

    return templates[0]['id']


def deploy(addr, token, project_id, payload):
    print('> Deploying project={}, {}'.format(project_id, payload))
    r = requests.post(addr + '/api/project/{}/tasks'.format(project_id), headers={'Authorization': 'Bearer ' + token},
                      json=payload)
    print('< {} {}'.format(r, r.text))


def parse_env(input):
    envs = {}
    for x in input:
        if '=' in x:
            a, b = x.split('=', 1)
            envs[a] = b
    return envs


@click.command()
@click.option('addr', '--addr', envvar='SEMAPHORE_ADDR', required=True, help='address of the semaphore server')
@click.option('token', '--token', envvar='SEMAPHORE_TOKEN', required=True, help='token to access semaphore server')
@click.option('--project', '-p', required=True, help='project name')
@click.option('--template', '-t', required=True, help='template name')
@click.option('--dry-run', is_flag=True, help='dry run')
@click.option('--playbook', help='override playbook')
@click.option('--debug', is_flag=True, help='debug mode')
@click.option('--environment', '-e', multiple=True)
def main(addr, token, project, template, dry_run, playbook, debug, environment):
    addr = addr.rstrip('/')
    payload = {}
    envs = parse_env(environment)
    if debug: payload['debug'] = True
    if dry_run: payload['dry_run'] = True
    if playbook: payload['playbook'] = playbook
    if envs: payload['environment'] = json.dumps(envs)

    project_id = lookup_project(addr, token, project)
    template_id = lookup_template(addr, token, project_id, template)
    payload['template_id'] = template_id

    deploy(addr, token, project_id, payload)


if __name__ == '__main__':
    main()
