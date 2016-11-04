from setuptools import setup

with open('requirements.txt', 'r') as f:
    reqs = f.read().splitlines()

setup(
    name='GitCher',
    install_requires=reqs,
    py_modules=['cli', 'utils'],
    entry_points='''
        [console_scripts]
        gitcher=cli:cli
    '''
)
