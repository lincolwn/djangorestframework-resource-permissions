from setuptools import setup

try:
    with open('README.md') as file:
        long_desc = file.read()
except IOError:
    long_desc = ''

setup(
    name='drf-resource-permissions',
    version='0.1.0',
    description=('Tool to make easy implement different levels of access '
        'permissions rules on django rest framework.'),
    author='Lincolwn Martins',
    author_email='lincolwn@gmail.com',
    url='https://github.com/lincolwn/djangorestframework-resource-permissions',
    keywords='django rest framework permissions',
    packages=['resource_permissions'],
    license='MIT License',
    long_description=long_desc,
    include_package_data=True,
    install_requires=[]
)