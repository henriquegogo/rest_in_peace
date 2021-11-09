from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description=fh.read()

setup(
    name="Rest-In-Peace",
    version="0.1.1",
    author="Henrique Gogó",
    author_email="henriquegogo@gmail.com",
    description="An instant and schemaless rest api with sqlite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henriquegogo/rest_in_peace",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/henriquegogo/rest_in_peace/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["rest-in-peace=rest_in_peace.cli:main"]
    }
)
