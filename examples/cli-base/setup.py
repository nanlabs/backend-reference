from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('VERSION.txt') as f:
    version = f.read().splitlines()

setup(
    name="python command base",
    version=str(version),
    py_modules=['src'],
    package_dir={"": "src"},
    install_requires=required,
    author=', '.join(["mnq78"]),
    author_email=', '.join(["matias.quiroga@nan-labs.com"]),
    entry_points='''
        [console_scripts]
        pycmd=app:start
    ''',
    description="Developer tool CLI base.",
)
