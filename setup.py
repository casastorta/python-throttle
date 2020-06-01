from distutils.core import setup

setup(
    name="Throttle",
    version="0.1dev",
    packages=["throttle"],
    license="GPLv3",
    long_description=open("ReadMe.md").read(),
    package_dir={"": "src"},
    # install_requires=[],
)
