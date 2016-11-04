import os
import json
import subprocess

import click

HOME_PATH = os.path.expanduser("~")
PROFILE_PATH = '/'.join([HOME_PATH, '.gitcher'])
PROFILE_FILE = '/'.join([PROFILE_PATH, 'profiles.json'])

# Enable flag -h
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Check .gitchanger folder
os.makedirs(PROFILE_PATH, exist_ok=True)

# Check profiles.json file
if not os.path.isfile(PROFILE_FILE):
    with open(PROFILE_FILE, 'a'):
        os.utime(PROFILE_FILE, None)


def get_all_profiles(file: str = PROFILE_FILE) -> json:
    """
    Get all profiles from given profiles.json.

    :param file: path of profiles.json
    :return: content of profiles.json
    """
    with open(file, 'r') as config:
        content = config.read()
        return json.loads(content) if content else None


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
def list():
    """List profiles."""
    profiles = get_all_profiles()

    if profiles:
        pos = 1
        for item in profiles.items():
            key = item[0]
            info = item[1]
            click.echo('[{pos}] {profile} [name:{name}, email:{email}]'.format(
                pos=pos, profile=key, name=info.get('name'), email=info.get('email')
            ))
            pos += 1
    else:
        click.echo('--no profile--')


@cli.command()
def create():
    """Create a new profile."""
    click.echo('creating a new profile')
    profile_name = click.prompt('Enter profile name', type=str).strip()
    github_name = click.prompt('Enter github name', type=str).strip()
    github_email = click.prompt('Enter github email', type=str).strip()

    with open(PROFILE_FILE, "r+") as config:
        content = config.read()
        accounts = json.loads(content) if content else {}
        accounts[profile_name] = {"name": github_name, "email": github_email}
        config.seek(0)
        config.write(json.dumps(accounts))
        click.echo('profile is successfully created')


@cli.command()
@click.option('-glob/-loc', default=False, help="-glob to use global config.")
@click.option('-p', '--profile', required=True, help='profile name')
def switch(glob, profile):
    """Login with given profile."""

    profiles = get_all_profiles()
    if profiles:
        selected_profile = profiles.get(profile)
        if selected_profile:
            command = 'git config {type} '.format(type='--global' if glob else '')

            subprocess.check_call(''.join([command, '{key} "{value}"'.format(key='user.name',
                                                                             value=selected_profile.get('name'))]),
                                  shell=True)
            subprocess.check_call(''.join([command, '{key} "{value}"'.format(key='user.email',
                                                                             value=selected_profile.get('email'))]),
                                  shell=True)
        else:
            click.echo('profile {p} cannot be found!'.format(p=profile))
    else:
        click.echo('cannot login, because no profile is found!')


if __name__ == '__main__':
    cli()
