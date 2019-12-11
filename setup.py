import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='rss_reader_by_Coromilly',
    version='2.21',
    author='Aleksandr_Levdansky',
    author_email='coromilly@gmail.com',
    description='Pure Python command-line RSS reader',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Coromilly/epam-q4-2019/tree/project',
    packages=['rss_reader'],
    install_requires=['beautifulsoup4', 'feedparser', 'requests'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': 'rss-reader = rss_reader.rss_reader:main'
    },
    python_requires='>=3.7'
)
