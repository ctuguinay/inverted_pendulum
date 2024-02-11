from setuptools import find_packages, setup

# Dependencies
with open("requirements.txt") as f:
    requirements = f.readlines()
INSTALL_REQUIRES = [t.strip() for t in requirements]

setup(
    name="inverted_pendulum",
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
