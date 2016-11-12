try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Script Parse Engine',
    'author': 'bapril',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'bapril@gmail.com.',
    'version': '0.0.3',
    'install_requires': ['nose'],
    'packages': ['script_parse_engine'],
    'scripts': [],
    'name': 'script_parse_engine'
}

setup(**config)
