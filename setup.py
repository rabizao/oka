"""Setup for oka package."""
import setuptools

NAME = "oka"


VERSION = '0.0.1'


AUTHOR = 'Rafael A. Bizao, Davi Pereira-Santos'


AUTHOR_EMAIL = 'rabizao@gmail.com'


DESCRIPTION = 'Client to interact with OKA repository'


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


LICENSE = 'GPL3'


URL = 'https://github.com/rabizao/oka'


DOWNLOAD_URL = 'https://github.com/automated-data-science/oka/releases'


CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: GPL3 License',
               'Natural Language :: English',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8']

SETUP_REQUIRES = ['flake8', 'autopep8', 'wheel']


INSTALL_REQUIRES = [
    'aiuna @ git+https://github.com/davips/aiuna.git@master#egg=package1.0',
    'tatu @ git+https://github.com/davips/tatu.git@master#egg=package1.0',
    'transf @ git+https://github.com/davips/transf.git@master#egg=package1.0',
    'cruipto @ git+https://github.com/davips/cruipto.git@master#egg=package1.0',
    'python-dotenv', 'requests'
]


EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov',
    ]
}

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE
)