import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'requests'
]

setup(
    name='JenkinsPy',
    version='0.0.1',
    license='AGPLv3',
    description='python bindings for Jenkins API',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    auth="Chris Loukas <commixon>",
    author="commixon",
    author_email="commixon@gmail.com",
    url="https://github.com/commixon/pyJenkins",
    keywords="CI Continuous Integration Jenkins Hudson Testing API",
    packages=find_packages('JenkinsPy'),
    package_dir={'':'JenkinsPy'},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_suite='JenkinsPy',
)
