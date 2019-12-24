import os
import io
from setuptools import find_packages, setup

here = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))

# allow setup.py to be run from any path
os.chdir(here)

with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()

about = {}
with io.open(os.path.join(here, 'cinepyle', 'version.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with io.open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as readme:
    README = readme.read()

install_requires = [
 'imdbpy @ git+https://github.com/alberanid/imdbpy@master#egg=imdbpy',
 'opchoice @ git+https://github.com/ibreschi/OpChoice@master#egg=opchoice'
]
packages = find_packages()
namespaces = ['cinepyle']

setup(
	name=about['__title__'],
	version=about['__version__'],
	description=about['__description__'],
	author=about['__author__'],
	author_email=about['__author_email__'],
	license=about['__license__'],
	data_files=[('', ['requirements.txt'])],
	include_package_data=True,
	long_description=README,
	long_description_content_type='text/markdown',
	setup_requires=requirements,
	install_requires=install_requires,
	packages=packages,
	classifiers=[
	    'Operating System :: OS Independent',
	    'Programming Language :: Python',
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 3.4',
	    'Programming Language :: Python :: 3.5',
	    'Programming Language :: Python :: 3.6',
	    'Programming Language :: Python :: 3.7',
	    ]
	)
