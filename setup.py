import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiohttp-extracts",
    version="0.0.1a1",
    author="jorektheglitch",
    author_email="jorektheglitch@yandex.ru",
    description="Sugar library for aiohttp handlers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorektheglitch/aiohttp-extracts",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
