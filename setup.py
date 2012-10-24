from distutils.core import setup

setup(
    name='nodefs',
    version='0.1-beta',
    packages=['lib', 'lib.selectors', 'tests', 'tests.fixtures'],
    long_description=open('README.md').read(),
    requires=[r.split("==")[0] for r in open('requirements.txt').read().split("\n") if r],
    scripts=['mounter.py'],
    data_files=['README.md', 'requirements.txt'],
    install_dirs=['.'],
)
