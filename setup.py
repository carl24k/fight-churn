import setuptools
import pkg_resources
import pathlib
# from pip._internal.req import parse_requirements


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fightchurn",
    version="0.0.1",
    author="Carl Gold",
    author_email="carl24k@fightchurnwithdata.com",
    description="Code from the book Fighting Churn With Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carl24k/fight-churn",
    project_urls={
        "Bug Tracker": "https://github.com/carl24k/fight-churn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['fightchurn',
              'fightchurn.listings',
              'fightchurn.listings.chap3',
              'fightchurn.listings.chap5',
              'fightchurn.listings.chap6',
              'fightchurn.listings.chap7',
              'fightchurn.listings.chap8',
              'fightchurn.listings.chap9',
              'fightchurn.listings.chap10'],
    scripts=['fightchurn/run_churn_listing.py'],
    python_requires=">=3.6",
    install_requires= install_requires
)
