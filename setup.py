import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='mmd',
    version='1.0.0',
    url='https://github.com/karthikramasamy/cmpe287/',
    license='BSD',
    maintainer='Karthik Ramasamy',
    description='The Metamorphic Malware Detection app built for the SJSU CMPE-287 Spring 2019 course.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'matplotlib',
        'networkx',
        'tabulate'
    ],
    extras_require={
        'test': [
            'matplotlib',
            'pytest',
            'pytest-cov',
            'coverage',
        ],
    },
)
