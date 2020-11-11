from setuptools import setup, find_packages

import consoleiotools

setup(
    name='consoleiotools',
    version=consoleiotools.__version__,
    description='Some console tools for inputs and outputs',
    long_description='Some console tools for inputs and outputs, by Kyan',
    url='https://github.com/kyan001/PyConsoleIOTools',
    author='Kai Yan',
    author_email='kai@kyan001.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='console input output tool',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["consoleiotools"],
    install_requires=['colorama'],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={},
)
