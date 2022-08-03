from setuptools import setup, find_packages

# python setup.py sdist
setup(
    name="rainwater_drainage_calculations",
    version="0.1",
    description="Collection of calculation method for rainwater drainage",
    author="Rafał Buczyński",
    packages=["rainwater_drainage_calculations"],
    install_requires=["requests", "pandas", "numpy", "matplotlib"],
)