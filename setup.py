# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

PROJECT_DIR = os.path.dirname(__file__)

setup(
    name='nodefs',
    version='0.1-beta',
    url='https://github.com/perenecabuto/nodefs.git',
    author="Felipe Ramos",
    author_email="perenecabuto@gmail.com",
    description="Generic fuse fs mapper for any purpose",
    long_description=open(os.path.join(PROJECT_DIR, 'README.md')).read(),
    keywords="Fuse, Python",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    #install_requires=open('requirements.txt').read().splitlines(),
    #install_requires=[
        #'django>=1.4',
        #'PIL==1.1.7',
        #'South>=0.7.6',
        #'django-extra-views>=0.2,<0.6',
        #'django-haystack==2.0.0-beta',
        #'django-treebeard==1.61',
        #'sorl-thumbnail==11.12',
        #'python-memcached==1.48',
        #'django-sorting==0.1',
        #'Babel==0.9.6',
    #],
    #dependency_links=['http://github.com/toastdriven/django-haystack/tarball/master#egg=django-haystack-2.0.0-beta'],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    #classifiers=[
        #'Environment :: Web Environment',
        #'Framework :: Django',
        #'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License',
        #'Operating System :: Unix',
        #'Programming Language :: Python'
    #]
)
