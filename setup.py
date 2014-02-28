import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'requests'
]

setup(
    name='pyJenkins',
    version='0.0.1',
    license='AGPLv3',
    description='python bindings for Jenkins API',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: CI :: Jenkins",
        "License :: GNU Affero General Public License v3",
        "Topic :: Jenkins"
    ],
    autho="Chris Loukas <commixon>",
    author_email="commixon@gmail.com",
    url="https://github.com/commixon/pyJenkins",
    keywords="CI Continuous Integration Jenkins Hudson Testing API",
    packages=find_packages('pyjenkins'),
    package_dir={'':'pyjenkins'},
    namespace_packages=['pyjenkins'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_require=requires,
    test_suite='pyJenkins',
)