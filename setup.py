from setuptools import setup, find_packages, distutils


setup(name='SheetLog',
      version='0.1',
      description='Log to google sheet',
      url='http://github.com/tobyclh/sheetlog',
      author='tobyclh',
      author_email='tobyclh@gmail.com',
      license='GNU',
      packages=find_packages(),
      zip_safe=True,
      include_package_data=False)
