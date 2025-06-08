from setuptools import setup, find_packages

setup(
    name="marlin-configurator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml>=6.0',
        'pyserial>=3.5',
        'pygments>=2.13.0',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'marlin-configurator=GUI.main_window:main',
        ],
    },
    author="Nsfr750",
    author_email="nsfr750@yandex.com",
    description="Marlin Firmware Configuration Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Nsfr750/marlin-configurator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
