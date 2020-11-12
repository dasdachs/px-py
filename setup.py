from setuptools import setup, find_packages


setup(
    name="px_py",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={"": "px"},
)
