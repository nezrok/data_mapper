from setuptools import setup

setup(
    name='data_mapper',
    version='0.1',
    description='The best data mapper in the world',
    url='xxx',
    author='Claudius Korzen',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=[
      'data_mapper',
      'data_mapper.database',
      'data_mapper.mapper',
      'data_mapper.model',
      'data_mapper.test'
    ],
    include_package_data=True,
    zip_safe=False
)