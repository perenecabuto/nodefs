from distutils.core import setup

setup(
    name='nodefs',
    version='0.1-beta',
    packages=['lib', 'lib.selectors', 'tests', 'tests.fixtures'],
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split("\n"),
    scripts=['mounter.py'],
)
