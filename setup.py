import setuptools

with open("README.md") as f:
    long_description = f.read()


setuptools.setup(
    name='fotosort',
    version='1.0',
    scripts=['bin/fotosort'],
    author="Sandro Kalbermatter",
    author_email="",
    description="Fotosort is a program for quickly copying or moving pictures from different events into different folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalsan/fotosort",
    packages=setuptools.find_packages(),
    package_data={'': ['qml/*', 'images/*']},
    include_package_data=True,
    license='GPLv3',
    install_requires=[
        'pillow',
        'pyyaml',
        'pyside2',
        'appdirs'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
)
