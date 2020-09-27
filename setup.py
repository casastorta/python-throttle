from distutils.core import setup

setup(
    name="Throttle",
    version="0.9.1",
    packages=["throttle"],
    author="Vedran Krivokuca",
    author_email="pydev@krivokuca.dev",
    license="MIT",
    description="Throttle just about anything",
    long_description=open("ReadMe.md").read(),
    package_dir={"": "src"},
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
)
