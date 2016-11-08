import os
from setuptools import setup

version = {}
with open(os.path.join('gitcher', '__init__.py'), 'r') as f:
    exec(f.read(), version)

with open('requirements.txt', 'r') as f:
    reqs = f.read().splitlines()

setup(
    name='gitcher',
    version=version['__version__'],
    url='https://github.com/butomo1989/gitcher',
    description='Git config manager',
    author='Budi Utomo',
    author_email='budi.ut.1989@gmail.com',
    keywords='git config manager',
    install_requires=reqs,
    py_modules=['cli', 'utils'],
    entry_points={'console_scripts': 'gitcher=gitcher.cli:main'}
)
