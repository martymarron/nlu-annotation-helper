from setuptools import setup, find_packages

setup(
    name='nlu-annotation-helper',
    version='1.1.0',
    description="""
    NLU annotation helper is a command line tool to partially automate annotation.
    """,
    platforms="OS Platform: Mac OSX, Python version: 3.0+",
    license="For Amazon internal use only. All rights served. ",
    url="https://wiki.labcollab.net/confluence/display/AIQ/Alexa+International+Quality+%28AIQ%29+Home",
    packages=find_packages(where="src", exclude=("tests",)),
    package_dir={"": "src"},
    install_requires=["langdetect"],
    extras_require={
        "dev": [
            "pytest",
            "pytest_mock"
        ]
    },
    entry_points="""\
    [console_scripts]
    nlu-annotation-helper = nlu_annotation_helper.cli:main
    """,
    author='Masashi Kurita (alias: maskurit@)',
    author_email='maskurit@amazon.co.jp'
)
