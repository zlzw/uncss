import os
from setuptools import setup
from setuptools import find_packages

install_requires = [
    "requests", "cssselect", "lxml", "cssutils", "redis", "discover", "stagecoach-apy"
]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="stagecoach-uncss",
    version="1.0.0",
    description="Scan your page automatically and create new CSS files removing all the unused CSS",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
        open(os.path.join(base_dir, "CHANGELOG.rst"), "r").read()
    ]),
    data_files=['uncss/api/config/settings.yml', 'uncss/api/config/routes.yml'],
    url="https://github.com/stagecoachio/uncss",
    author="Felix Carmona",
    author_email="mail@felixcarmona.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite="tests.get_tests",
)
