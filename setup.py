from setuptools import setup, find_packages


long_description = open('README.rst').read()

setup(
    name='PyHomeSeer',
    version='0.0.1',
    license='MIT',
    url='https://github.com/legrego/pyhomeseer',
    author='Larry Gregory',
    author_email='lgregorydev@gmail.com',
    description='Python module to talk to HomeSeer 3.',
    long_description=long_description,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
