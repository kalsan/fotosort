import setuptools

with open("README.md") as f:
    long_description = f.read()

with open('fotosort/VERSION') as f:
    version = f.read()


setuptools.setup(
    name='fotosort',
    version=version,
    scripts=['bin/fotosort'],
    author="Sandro Kalbermatter",
    author_email="",
    description="Fotosort is a program for quickly copying or moving pictures from different events into different folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalsan/fotosort",
    packages=setuptools.find_packages(),
    package_data={'': ['qml/*', 'images/*', 'VERSION']},
    include_package_data=True,
    license='GPLv3',
    install_requires=[
        'pillow',
        'pyyaml',
        'pyside6',
        'appdirs'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
