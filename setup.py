from setuptools import setup, find_packages

setup(
    name='montecarlo',
    version='0.1',
    description='A Monte Carlo simulator with Die, Game, and Analyzer classes.',
    url='https://github.com/csh4bj/FinalProject',
    author='Cameron Her',
    author_email='csh4bj@virginia.edu',
    packages=find_packages(),
    install_requires=['pandas','numpy'],
)