from os import path
from setuptools import setup
# To use a consistent encoding
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orthoproj',
    packages=['orthoproj'],
    version='0.0.2',
    description='Python package to create an Orthogonal Projection of 3D '
                'data with full axes synchronisation',
    long_description=long_description,
    url='https://github.com/apbard/orthoproj',
    author='Alessandro Pietro Bardelli',
    author_email='',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords=['orthogonal projections', 'visualisation', 'plot'],
    install_requires=['matplotlib'],
)
