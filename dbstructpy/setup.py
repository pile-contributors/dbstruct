try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tools for dealing with database schema',
    'author': 'Nicu Tofan',
    'url': 'https://github.com/pile-contributors/pile-tools',
    'download_url': 'https://github.com/pile-contributors/dbstruct',
    'author_email': 'nicu.tofan@gmail.com',
    'version': '0.1dev',
    'install_requires': ['nose', 'appdirs', 'generateDS'],
    'packages': [],
    'package_data': {
        'schema': ['share/dbstruct.xsd'],
    },
    'scripts': ['bin/dbstruct.py'],
    'name': 'pile'
}

setup(**config)
