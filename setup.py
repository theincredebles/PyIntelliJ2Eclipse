from setuptools import setup

setup(
  name = 'PyIntelliJ2Eclipse',
  packages = ['PyIntelliJ2Eclipse'], # this must be the same as the name above
  version = '0.1',
  description = 'A convenient python utility to convert IntelliJ IDEA project files to Eclipse project files',
  author = 'Viswanath Kumar Skand Priya, Bharath Thiruveedula',
  author_email = 'kspviswa.github@gmail.com',
  url = 'https://github.com/theincredebles/PyIntelliJ2Eclipse',
  download_url = '',
  keywords = ['build', 'intellij', 'eclipse'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    ],
  install_requires=[
    'xmltodict',
    'xmljson',
    'ordereddict',
    'lxml',
    'progressbar'
    ],
)
