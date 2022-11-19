import setuptools

with open('README.md') as f:
    long_desc = f.read()

setuptools.setup(
    name='consoleiotools',
    description='Some console tools for inputs and outputs',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/kyan001/PyConsoleIOTools',
    author='Kai Yan',
    author_email='kai@kyan001.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='console input output tool',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=['consoleiotools'],
    install_requires=['rich'],
    extras_require={'dev': ['build', 'wheel', 'pycodestyle']},
    package_data={},
    data_files=[],
    entry_points={},
)
