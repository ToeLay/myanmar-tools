import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "myanmar-tools",
    version = "0.0.1",
    author = "Toe Lay",
    author_email = "toelay.tnz@gmail.com",
    description = "Detect the Zawgyi-One font encoding",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/google/myanmar-tools",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.6"
)