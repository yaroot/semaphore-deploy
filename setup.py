import os
from setuptools import setup

_version = os.environ.get('TRAVIS_TAG', '0.0.0')

setup(
    name='semaphore-deploy',
    version=_version,
    packages=['semaphore_deploy'],
    # scripts=['semaphore'],
)
