from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

requirements = [
    'numpy'
    'librosa'
    'matplotlib'
    'librosa'
    'pyosc'
]

setup(
    name='threshlds-ga',
    version='0.0.1',
    description='Genetic algorithm for searching chaos',
    long_description=readme,
    author='David Kant',
    author_email='david.kant@gmail.com',
    url='https://davidkantportfolio.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements
)
