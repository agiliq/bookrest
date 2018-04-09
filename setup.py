from setuptools import find_packages, setup

version = "0.1.4"

setup(
    name='bookrest',
    version=version,
    url='https://www.agiliq.com/apps/bookrest/',
    author_email='hello@agiliq.com',
    long_description=open("README.md").read(),
    license='BSD',
    description='The easiest way to add a Django and DRF powered API to any project',
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['example']),
    install_requires=['django>=2.0.0', 'djangorestframework>=3.8.0'],
)
