from os.path import join
from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

def parse_requirements(requirements, ignore=('setuptools',)):
    with open(requirements) as f:
        packages = set()
        for line in f:
            line = line.strip()
            if line.startswith(('#', '-r', '--')):
                continue
            if '#egg=' in line:
                line = line.split('#egg=')[1]
            pkg = line.strip()
            if pkg not in ignore:
                packages.add(pkg)
        return tuple(packages)

setup(
    name='permasigner',
    version='1.0.0',
    description=('Permanently signs IPAs on jailbroken iDevices (persists on stock).'),
    license='BSD-3-Clause',
    url='https://github.com/itsnebulalol/permasigner',
    python_requires=">=3.7",
    packages=['permasigner'],
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'permasigner = permasigner.__main__:main',
        ]
    },
    keywords='python, windows, macos, linux, docker, cli, open-source, ios, command-line-app, cli-app, hacktoberfest, procursu,s permasign, permasigner',
    include_package_data=True,
    author='Nebula',
    install_requires=parse_requirements('requirements.txt'),
    author_email='me@itsnebula.net',
)