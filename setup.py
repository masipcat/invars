from setuptools import find_packages
from setuptools import setup


def get_version():
    with open("VERSION") as f:
        return f.readline().strip()


setup(
    name="invars",
    version=get_version(),
    description="Single assignment variables",
    author="Jordi Masip",
    author_email="jordi@masip.cat",
    url="https://github.com/masipcat/invars",
    license="GNU",
    zip_safe=True,
    include_package_data=True,
    package_data={"": ["*.txt", "*.md"]},
    packages=find_packages(),
    install_requires=["click~=7.0.0", "setuptools"],
    extras_require={"test": ["pytest~=4.0.1"]},
    entry_points={"console_scripts": ["invars = invars.invars:main"]},
)
