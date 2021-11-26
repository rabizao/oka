import setuptools

NAME = "oka"

VERSION = "0.2108.0"

AUTHOR = 'Rafael A. Bizao, Davi P. dos Santos'

AUTHOR_EMAIL = 'rabizao@gmail.com'

DESCRIPTION = 'Python client for oka'

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

LICENSE = 'GPL3'

URL = 'https://github.com/davips/lange'

DOWNLOAD_URL = 'https://github.com/davips/lange/releases'

CLASSIFIERS = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
]


INSTALL_REQUIRES = [
    'requests', 'python-dotenv', 'idict'
]

EXTRAS_REQUIRE = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
}

SETUP_REQUIRES = ['wheel']

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    packages=setuptools.find_packages(),
    setup_requires=SETUP_REQUIRES,
    url=URL,
    keywords='data, repository, archive, data science, machine learning',  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/rabizao/oka/issues',
        'Source': 'https://github.com/rabizao/oka',
    },
)

package_dir = {'': '.'}  # For IDEs like Intellij to recognize the package.
