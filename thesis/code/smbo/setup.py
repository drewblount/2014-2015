from setuptools import setup

setup(name='smbo',
      version='0.1',
      description='a sequential model-based optimization framework',
      url='http://github.com/drewblount/smbo',
      author='Drew Blount',
      author_email='dblount@reed.edu',
      license='MIT',
      packages=['smbo'],
      install_requires=[
          'numpy',
          'matplotlib',
      ],
      zip_safe=False)
